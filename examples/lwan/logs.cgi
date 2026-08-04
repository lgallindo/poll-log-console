#!/bin/sh
# Example CGI — place under cgi-bin/ when using lwan/CGI.
printf 'Content-Type: application/json\r\n\r\n'
echo '[{"time":"00:00:00.000","msg":"[SYS] lwan cgi stub","type":"sys"}]'
