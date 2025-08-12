#!/bin/bash

# Avni MCP Server Deployment Script
# This script deploys the Avni MCP server as a systemd service

set -e  # Exit on any error

# Configuration
SERVICE_NAME="avni-mcp-server"
DEPLOY_DIR="/opt/avni-mcp-server"
SERVICE_USER="avni-mcp-user"
SERVICE_GROUP="avni-mcp-grp"
BACKUP_DIR="/opt/backups/avni-mcp-server"
LOG_DIR="/var/log/avni-mcp-server"
LOG_FILE="$LOG_DIR/deploy.log"
CONFIG_FILE="/etc/$SERVICE_NAME.conf"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# Check if running as root or with sudo
if [[ $EUID -ne 0 ]]; then
    error "This script must be run as root or with sudo"
fi

log "Starting deployment of Avni MCP Server..."

# Create service user and group if they don't exist
if ! getent group "$SERVICE_GROUP" &>/dev/null; then
    log "Creating service group: $SERVICE_GROUP"
    groupadd --system "$SERVICE_GROUP"
fi

if ! id "$SERVICE_USER" &>/dev/null; then
    log "Creating service user: $SERVICE_USER"
    useradd --system --home-dir "$DEPLOY_DIR" --shell /bin/bash --gid "$SERVICE_GROUP" "$SERVICE_USER"
fi

# Create directories
log "Creating deployment directories..."
mkdir -p "$DEPLOY_DIR" "$BACKUP_DIR" "$LOG_DIR"
chown "$SERVICE_USER:$SERVICE_GROUP" "$DEPLOY_DIR"
chown "$SERVICE_USER:$SERVICE_GROUP" "$LOG_DIR"

# Stop existing service if running
log "Stopping existing service..."
if systemctl is-active --quiet "$SERVICE_NAME"; then
    systemctl stop "$SERVICE_NAME"
    log "Service stopped successfully"
else
    log "Service was not running"
fi

# Backup current deployment if it exists
if [[ -d "$DEPLOY_DIR/current" ]]; then
    log "Backing up current deployment..."
    backup_name="backup-$(date +%Y%m%d-%H%M%S)"
    mv "$DEPLOY_DIR/current" "$BACKUP_DIR/$backup_name"
    log "Backup created: $BACKUP_DIR/$backup_name"
    
    # Keep only last 5 backups
    cd "$BACKUP_DIR"
    ls -t | tail -n +6 | xargs -r rm -rf
fi

# Extract new deployment
log "Extracting new deployment..."
mkdir -p "$DEPLOY_DIR/current"
cd "$DEPLOY_DIR/current"
tar -xzf "/tmp/avni-mcp-server.tar.gz"
chown -R "$SERVICE_USER:$SERVICE_GROUP" "$DEPLOY_DIR/current"

# Install Python dependencies
log "Installing Python dependencies..."
sudo -u "$SERVICE_USER" bash -c "
    cd '$DEPLOY_DIR/current'
    
    # Install uv if not present
    if ! command -v uv &> /dev/null; then
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH=\"\$HOME/.local/bin:\$PATH\"
    fi
    
    # Install dependencies
    uv sync --no-dev
"

# Setup configuration file
log "Setting up environment configuration..."

# Create config file with production settings
cat > "$CONFIG_FILE" << EOF
# Avni MCP Server Production Configuration
AVNI_BASE_URL=${AVNI_BASE_URL:-https://staging.avniproject.org}
OPENAI_API_KEY=${OPENAI_API_KEY}

# Logging
LOG_LEVEL=INFO

# Server settings  
PORT=8023
HOST=0.0.0.0
TRANSPORT=sse
PYTHONPATH=$DEPLOY_DIR/current
EOF

chown root:root "$CONFIG_FILE"
chmod 644 "$CONFIG_FILE"  # Readable by all, writable by root

# Install systemd service file
log "Installing systemd service..."
cp "/tmp/avni-mcp-server.service" "/etc/systemd/system/$SERVICE_NAME.service"

# Update service file with correct paths
sed -i "s|/opt/avni-mcp-server|$DEPLOY_DIR/current|g" "/etc/systemd/system/$SERVICE_NAME.service"
sed -i "s|User=avni|User=$SERVICE_USER|g" "/etc/systemd/system/$SERVICE_NAME.service"

# Reload systemd and enable service
log "Reloading systemd configuration..."
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"

# Start the service
log "Starting Avni MCP Server..."
systemctl start "$SERVICE_NAME"

# Wait for service to start
sleep 5

# Check service status
if systemctl is-active --quiet "$SERVICE_NAME"; then
    log "✅ Service started successfully!"
    
    # Health check
    log "Performing health check..."
    for i in {1..30}; do
        if curl -f -s http://localhost:8023/health > /dev/null 2>&1; then
            log "✅ Health check passed!"
            break
        elif [[ $i -eq 30 ]]; then
            error "❌ Health check failed after 30 attempts"
        else
            log "Health check attempt $i/30 failed, retrying..."
            sleep 2
        fi
    done
else
    error "❌ Failed to start service"
fi

# Show service status
log "Service status:"
systemctl status "$SERVICE_NAME" --no-pager

# Show recent logs
log "Recent service logs:"
journalctl -u "$SERVICE_NAME" --no-pager -n 10

log "🎉 Deployment completed successfully!"

# Cleanup temp files
rm -f "/tmp/avni-mcp-server.tar.gz" "/tmp/deploy.sh" "/tmp/avni-mcp-server.service"

log "Deployment script finished."