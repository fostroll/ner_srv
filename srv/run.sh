#!/bin/sh

if [ $1 -eq "prod" ]; then
    python ./main.py prod
else
    python ./main.py
fi
