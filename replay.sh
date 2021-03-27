#!/bin/bash
mitmdump --port 8080 --reverse http://localhost:8081 --server-replay flows/github.flow
