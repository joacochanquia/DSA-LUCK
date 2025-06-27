#!/bin/bash

docker build -t ctf-project-fix .

if command -v docker-compose &> /dev/null; then
  echo "docker-compose is installed (legacy version)."
	docker-compose up
else
	docker compose up
fi