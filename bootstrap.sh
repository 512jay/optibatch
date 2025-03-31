#!/bin/bash
set -e

python -m venv env
source env/bin/activate
pip install -r requirements.txt
black .
pytest
