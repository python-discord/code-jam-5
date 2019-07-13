#!/usr/bin/env bash

if ! [ -d venv/ ]; then
  python3.7 -m venv venv
  source venv/bin/activate
  python3.7 -m pip install -r requirements.txt
else
  source venv/bin/activate
fi
python3.7 -m src
