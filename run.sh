#!/bin/bash
sam local invoke -e events/ping.json -d 5890 PrAutolabellerFunction
