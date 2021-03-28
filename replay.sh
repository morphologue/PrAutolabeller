#!/bin/bash
mitmdump --listen-port 8080 --listen-host 0.0.0.0 --mode reverse:http://localhost:8081 --server-replay mitmproxy/github.flow
