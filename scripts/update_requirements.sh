#!/usr/bin/env bash

set -e
set -x

uv pip compile requirements.in -o requirements.txt
uv pip compile requirements-dev.in -o requirements-dev.txt
uv pip sync requirements-dev.txt
