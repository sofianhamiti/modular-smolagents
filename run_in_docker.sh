#!/bin/bash
set -e

IMAGE_NAME="agent-sandbox"

echo "Building Docker image (uses cache if nothing changed)..."
docker build -t "$IMAGE_NAME" .

echo "Starting interactive container. Type 'python main.py' to run your script. Type 'exit' to stop the container."
docker run --rm -it -p 7860:7860 -v "$PWD":/app -w /app "$IMAGE_NAME" bash
