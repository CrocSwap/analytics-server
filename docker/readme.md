# Docker Scripts for API Server

This directory contains several shell scripts to help manage the Docker environment for an API server.

Before running these scripts, make sure your environment variables are set up in the .env file. These variables are sourced before each Docker command.

To run these scripts from the root of your project directory, use the bash command followed by the script's relative path. For example, to run the build.sh script, use: bash ./docker/build.sh

Details of each script:

1. build.sh: This script builds your Docker image. It sources your environment variables, kills a running container named 'audit_process' if it exists, prunes your Docker environment, and then builds a Docker image named 'audit_tools'.

2. connect.sh: This script connects to a running container named 'audit_process'. Make sure the container is running before you try to connect.

3. remove.sh: This script removes a docker container.

4. run.sh: This script runs your Docker container. It sources your environment variables, removes a container named 'audit_process' if it exists, and then runs a Docker container with the name 'audit_process', mapping the port specified in your environment variables to 5000 inside the container, and using the 'audit_tools' image.

5. stop.sh: This script stops a running container named 'audit_process'.

Please note that you need Docker installed and correctly configured on your machine to run these scripts.