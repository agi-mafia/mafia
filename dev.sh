#!/bin/bash

# Stop any existing containers
docker-compose down

# Rebuild the containers
docker-compose build

# Start the containers in detached mode
docker-compose up -d

# Show logs
docker-compose logs -f
