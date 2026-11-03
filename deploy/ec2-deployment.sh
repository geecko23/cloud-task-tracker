
#!/bin/bash
set -euo pipefail

# Validate the artifact name
: "${FILE:?FILE variable is required}"

# Download deployment artifact
aws s3 cp \
    "s3://cloud-task-tracker-deploy/jenkins-deployments/${FILE}" \
    "/tmp/${FILE}"

# Extract application files as appuser
sudo -u appuser unzip -o "/tmp/${FILE}" -d /opt/cloud/

# Create virtual environment if it doesn't exist
if [ ! -d /opt/cloud/venv ]; then
    sudo -u appuser python3 -m venv /opt/cloud/venv
fi

# Install application dependencies as appuser
sudo -u appuser /opt/cloud/venv/bin/python -m pip install \
    -r /opt/cloud/requirements.txt

# Restart application service
sudo systemctl restart cloud-task-tracker

# Verify application health
curl -f http://127.0.0.1/health

echo "Deployment successful: ${FILE}"
