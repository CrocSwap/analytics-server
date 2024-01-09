set -a; source ./.env; set +a; 
docker rm audit_process
docker run -d -p $PORT:$PORT --name audit_process audit_tools