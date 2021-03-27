#!/bin/bash
sam local invoke -e events/pull_request.json -d 5890 PrAutolabellerFunction
