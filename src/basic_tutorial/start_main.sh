#!/bin/bash

#####################
# Example: ./start_main main2
#####################

MAIN=$1  # example "main1"
MAINFILE=$(ls "${MAIN}"*)
MODULE=$(basename "${MAINFILE}" .py)

uvicorn --port 8042 "${MODULE}":app --reload
