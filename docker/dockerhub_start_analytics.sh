#!/bin/bash

# Step 1: Pull the Docker image
IMAGE="chhypotenuse/crocswap-analytics"
TAG="latest"
echo "Pulling image $IMAGE..."

docker pull $IMAGE:$TAG

# Step 4: Run the image as a container
echo "Running the container..."
docker run --env-file .env $IMAGE:$TAG

echo "Script execution completed."