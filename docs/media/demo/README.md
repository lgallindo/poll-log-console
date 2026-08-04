# Demo media (README)

| File | Role |
|------|------|
| [pipeline-dag.gif](pipeline-dag.gif) | Faux data-pipeline DAG + console (unlabeled README embed) |
| [monitor-echo.gif](monitor-echo.gif) | Echo lab recording |
| [monitor-net-status.gif](monitor-net-status.gif) | Net status recording |
| [console-tricks.gif](console-tricks.gif) | Minimize / expand, activity, CSS reposition |
| [enterprise-deploy-audit.png](enterprise-deploy-audit.png) | Enterprise deploy-desk still (replaces README mark slot) |
| [enterprise-backoffice-audit.png](enterprise-backoffice-audit.png) | Enterprise back-office still |
| [funny-mail-chat-monitor.png](funny-mail-chat-monitor.png) | Chat/mail-as-log still |

Regenerate motion (repo root, `.venv` + Playwright):

```bash
.venv/bin/python .local/scripts/capture_readme_demos.py
.venv/bin/python .local/scripts/capture_console_tricks.py
.venv/bin/python .local/scripts/capture_pipeline_dag_gif.py
```

Parent: [../](../).
