set -a; source .env; set +a; 
docker kill audit_process
docker system prune -a -f