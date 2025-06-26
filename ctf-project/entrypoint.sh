#!/bin/bash
echo "TEST"

pip install -r /requirements.txt

python -m flask run --host=0.0.0.0
