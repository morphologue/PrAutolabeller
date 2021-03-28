#!/bin/bash
# Reverse proxy in the background until this script exits. The authorization replacement must be
# done in a separate process to the recording, otherwise the recording stores the real token.
mitmdump --listen-port 8081 --mode reverse:https://api.github.com -s mitmproxy/addon.py -q &
mitmdump --listen-port 8080 --listen-host 0.0.0.0 --mode reverse:http://localhost:8081 -w mitmproxy/github.flow
