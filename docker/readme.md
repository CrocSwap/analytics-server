# Docker Scripts for API Server

This directory contains several shell scripts to help manage the Docker environment for the API server. Before running these scripts, make sure your environment variables are set up in the `.env file`. These variables are sourced before each Docker command.
## Details of each script:
These scripts were created to help people automate the docker process. However, if you are familiar with docker, you can grab the Dockerfile in the root directory, and the .env, and do everything manually.

1. `build.sh` : This script builds your Docker image. It sources your environment variables, kills a running container named 'audit_process' if it exists, prunes your Docker environment, and then builds a Docker image named 'audit_tools'.
2. `run.sh`: This script runs your Docker container. It sources your environment variables, removes a container named 'audit_process' if it exists, and then runs a Docker container with the name 'audit_process', mapping the port specified in your environment variables to 8080 inside the container, and using the 'audit_tools' image.
3. `connect.sh`: This script connects to a running container named 'audit_process'. This is really just for debugging only. You can likely ignore this script.
4. `remove.sh`: This script removes a docker container.
5. `stop.sh`: This script stops a running container named 'audit_process'.
