#!/bin/bash
set -euo pipefail

FILE="${1:?Usage: deploy.sh <deployment-zip-name>}"

# Download application artifact from S3
aws s3 cp \
    "s3://cloud-task-tracker-deploy/jenkins-deployments/${FILE}" \
    "/tmp/${FILE}" \
    --region us-east-1

# Extract application files as appuser
sudo -u appuser unzip -o "/tmp/${FILE}" -d /opt/cloud/

# Create virtual environment if it doesn't exist
if [ ! -d /opt/cloud/venv ]; then
    sudo -u appuser python3 -m venv /opt/cloud/venv
fi

# Install application dependencies
sudo -u appuser /opt/cloud/venv/bin/python -m pip install \
    -r /opt/cloud/requirements.txt

# Restart application
sudo systemctl restart cloud-task-tracker

# Verify application health
curl -f http://127.0.0.1/health

echo "Deployment successful: ${FILE}"