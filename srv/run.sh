#!/bin/sh

if [ "$1" = "prod" ]; then
    python ./main.py prod
else
    python ./main.py
fi
