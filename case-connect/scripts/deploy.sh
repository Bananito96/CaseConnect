#!/bin/bash

# deployment.sh
echo "Pulling latest changes..."
git pull

echo "Building and starting containers..."
docker-compose -f docker-compose.prod.yml up --build -d

echo "Cleaning up old images..."
docker image prune -f

echo "Deployment complete!"