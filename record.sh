#!/bin/bash
# Reverse proxy in the background until this script exits. The authorization replacement must be
# done in a separate process to the recording, otherwise the recording stores the real token.
mitmdump --port 8081 --reverse https://api.github.com \
    --setheader '/~q/Authorization/token REPLACE_ME' \
    --replace !~s!https\://api\.github\.com!http://host.docker.internal:8080 &
MITM_BG_PID=$!
trap "kill $MITM_BG_PID" EXIT

mitmdump --port 8080 --reverse http://localhost:8081 -w flows/github.flow
