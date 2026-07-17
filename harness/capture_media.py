#!/usr/bin/env python3
"""Regenerate docs/media from the sample apps (Playwright + ImageMagick)."""
from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "docs" / "media"
APPS_DIR = MEDIA / "apps"
THUMBS_DIR = APPS_DIR / "thumbs"
HERO = MEDIA / "hero.png"

APPS = [
    {
        "name": "cpm-term",
        "port": 8771,
        "script": ROOT / "examples" / "cpm-term" / "app.py",
        "action": "cpm",
    },
    {
        "name": "net-status",
        "port": 8772,
        "script": ROOT / "examples" / "net-status" / "app.py",
        "action": "refresh",
    },
    {
        "name": "echo-lab",
        "port": 8773,
        "script": ROOT / "examples" / "echo-lab" / "app.py",
        "action": "echo",
    },
    {
        "name": "simple-css",
        "port": 8774,
        "script": ROOT / "examples" / "simple-css" / "app.py",
        "action": "ping",
    },
    {
        "name": "water-css",
        "port": 8775,
        "script": ROOT / "examples" / "water-css" / "app.py",
        "action": "note",
    },
]

VIEWPORT = {"width": 1280, "height": 720}
THUMB_WIDTH = 320


def py_bin() -> str:
    venv = ROOT / ".venv" / "bin" / "python"
    return str(venv) if venv.is_file() else sys.executable


def port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", port)) == 0


def wait_http(url: str, timeout: float = 15.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1) as r:
                if r.status < 500:
                    return
        except (urllib.error.URLError, TimeoutError, OSError):
            pass
        time.sleep(0.2)
    raise RuntimeError(f"timeout waiting for {url}")


def start_apps() -> list[subprocess.Popen]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src" / "python") + (
        f":{env['PYTHONPATH']}" if env.get("PYTHONPATH") else ""
    )
    py = py_bin()
    started: list[subprocess.Popen] = []
    for app in APPS:
        if port_open(app["port"]):
            print(f"  attach  {app['name']} :{app['port']}")
            continue
        print(f"  start   {app['name']} :{app['port']}")
        log = open(f"/tmp/plc-capture-{app['name']}.log", "w")
        proc = subprocess.Popen(
            [py, str(app["script"])],
            cwd=str(ROOT),
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        started.append(proc)
    for app in APPS:
        wait_http(f"http://127.0.0.1:{app['port']}/")
    return started


def stop_apps(procs: list[subprocess.Popen]) -> None:
    for p in procs:
        p.terminate()
    for p in procs:
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()


def convert_bin() -> str:
    for name in ("convert", "magick"):
        path = subprocess.run(["which", name], capture_output=True, text=True)
        if path.returncode == 0 and path.stdout.strip():
            return path.stdout.strip()
    raise RuntimeError("ImageMagick convert/magick not found")


def run_convert(args: list[str]) -> None:
    cmd = [convert_bin(), *args]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"convert failed: {' '.join(cmd)}\n{r.stderr}")


def expand_console(page) -> None:
    page.wait_for_selector(".dos-console", timeout=10000)
    console = page.locator(".dos-console").first
    if console.evaluate("el => el.classList.contains('is-minimized')"):
        page.locator("[data-dos-header]").first.click()
        page.wait_for_timeout(300)


def do_action(page, action: str) -> None:
    if action == "cpm":
        page.fill("#line", "DIR")
        page.press("#line", "Enter")
    elif action == "refresh":
        page.click("#refresh")
    elif action == "echo":
        page.fill("#msg", "hello from capture")
        page.click("#send")
    elif action == "ping":
        page.click("#ping")
    elif action == "note":
        page.fill("#t", "capture note")
        page.click("form#f button[type=submit]")
    page.wait_for_timeout(1200)


def capture_apps() -> dict[str, Path]:
    from playwright.sync_api import sync_playwright

    APPS_DIR.mkdir(parents=True, exist_ok=True)
    THUMBS_DIR.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
        )
        for app in APPS:
            url = f"http://127.0.0.1:{app['port']}/"
            page = context.new_page()
            page.goto(url, wait_until="networkidle")
            expand_console(page)
            do_action(page, app["action"])
            out = APPS_DIR / f"{app['name']}.png"
            page.screenshot(path=str(out), full_page=False)
            page.close()
            thumb = THUMBS_DIR / f"{app['name']}.png"
            run_convert([str(out), "-resize", f"{THUMB_WIDTH}x", str(thumb)])
            paths[app["name"]] = out
            print(f"  wrote   {out.relative_to(ROOT)}")
            print(f"  thumb   {thumb.relative_to(ROOT)}")
        browser.close()
    return paths


def build_hero(paths: dict[str, Path]) -> None:
    """Dark slate canvas + simple-css page + framed console crop from cpm-term."""
    MEDIA.mkdir(parents=True, exist_ok=True)
    base = paths["simple-css"]
    inset_src = paths["cpm-term"]
    work = MEDIA / "_hero_work"
    work.mkdir(exist_ok=True)
    canvas = work / "canvas.png"
    page_scaled = work / "page.png"
    inset = work / "inset.png"
    framed = work / "framed.png"

    # 1600x900 dark slate
    run_convert(
        [
            "-size",
            "1600x900",
            "xc:#1a1f26",
            str(canvas),
        ]
    )
    # Scale main page into left/center
    run_convert(
        [
            str(base),
            "-resize",
            "1100x",
            str(page_scaled),
        ]
    )
    # Crop lower-right console region from cpm-term (approx floating widget)
    run_convert(
        [
            str(inset_src),
            "-gravity",
            "SouthEast",
            "-crop",
            "480x360+24+24",
            "+repage",
            str(inset),
        ]
    )
    # Polaroid-ish frame
    run_convert(
        [
            str(inset),
            "-bordercolor",
            "#f5f0e6",
            "-border",
            "14x18",
            "-bordercolor",
            "#2a3038",
            "-border",
            "2x2",
            "-background",
            "none",
            "-rotate",
            "3",
            str(framed),
        ]
    )
    # Composite page onto canvas
    composed = work / "composed.png"
    run_convert(
        [
            str(canvas),
            str(page_scaled),
            "-geometry",
            "+40+80",
            "-composite",
            str(composed),
        ]
    )
    # Composite framed inset
    run_convert(
        [
            str(composed),
            str(framed),
            "-geometry",
            "+1050+420",
            "-composite",
            str(HERO),
        ]
    )
    # Cleanup work dir
    for f in work.iterdir():
        f.unlink()
    work.rmdir()
    print(f"  wrote   {HERO.relative_to(ROOT)}")


def main() -> int:
    print("poll-log-console: regenerate docs/media")
    started: list[subprocess.Popen] = []
    try:
        started = start_apps()
        paths = capture_apps()
        build_hero(paths)
    finally:
        stop_apps(started)
    print("done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
