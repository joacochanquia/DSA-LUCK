#!/bin/bash
echo "Starting CTF Application..."

pip install -r /requirements.txt

cd /www
python app.py
