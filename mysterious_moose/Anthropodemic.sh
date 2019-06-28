#!/usr/bin/env bash

if ! [ -d venv/ ]; then
  python -m venv venv
  source venv/Scripts/activate
  python -m pip install -r requirements.txt
else
  source venv/Scripts/activate
fi
python -m src