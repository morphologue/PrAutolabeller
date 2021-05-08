#!/bin/bash
sam local invoke -e events/${1:-pull_request}.json -d 5890 PrAutolabellerFunction
