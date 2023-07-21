#!/bin/bash

IMG_NAME="default_image"

# Build the Docker image
docker build -t "$IMG_NAME" .

# Run the Docker container
#docker-compose run my_app "$IMG_NAME"
docker run -it -v "$(pwd):/app" "$IMG_NAME" bash
