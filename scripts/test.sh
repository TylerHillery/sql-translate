#!/usr/bin/env bash

set -e
set -x

coverage run --source=sql_translate --omit=sql_translate/main.py -m pytest
coverage report --show-missing
coverage html --title "${@-coverage}"
