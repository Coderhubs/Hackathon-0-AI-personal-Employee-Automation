#!/bin/bash
# Platinum Tier - Automated Deployment Script
# This script automates the cloud deployment process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DEPLOY_USER="deploy"
APP_DIR="/home/$DEPLOY_USER/platinum-ai"
BACKUP_DIR="/home/$DEPLOY_USER/backups"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "Please run as root (use sudo)"
        exit 1
    fi
}

# Phase 1: Initial Server Setup
setup_server() {
    log_info "Starting server setup..."

    # Update system
    log_info "Updating system packages..."
    apt update && apt upgrade -y

    # Install Docker
    log_info "Installing Docker..."
    if ! command -v docker &> /dev/null; then
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        rm get-docker.sh
    else
        log_info "Docker already installed"
    fi

    # Install Docker Compose
    log_info "Installing Docker Compose..."
    if ! command -v docker-compose &> /dev/null; then
        apt install docker-compose -y
    else
        log_info "Docker Compose already installed"
    fi

    # Install Node.js and PM2
    log_info "Installing Node.js and PM2..."
    if ! command -v node &> /dev/null; then
        curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
        apt install -y nodejs
    else
        log_info "Node.js already installed"
    fi

    if ! command -v pm2 &> /dev/null; then
        npm install -g pm2
    else
        log_info "PM2 already installed"
    fi

    # Create deployment user
    log_info "Creating deployment user..."
    if ! id "$DEPLOY_USER" &>/dev/null; then
        adduser --disabled-password --gecos "" $DEPLOY_USER
        usermod -aG docker $DEPLOY_USER
        usermod -aG sudo $DEPLOY_USER
        log_info "User $DEPLOY_USER created"
    else
        log_info "User $DEPLOY_USER already exists"
    fi

    # Setup firewall
    log_info "Configuring firewall..."
    ufw --force enable
    ufw allow 22/tcp    # SSH
    ufw allow 80/tcp    # HTTP
    ufw allow 443/tcp   # HTTPS
    ufw allow 8000/tcp  # API

    # Setup swap
    log_info "Setting up swap space..."
    if [ ! -f /swapfile ]; then
        fallocate -l 4G /swapfile
        chmod 600 /swapfile
        mkswap /swapfile
        swapon /swapfile
        echo '/swapfile none swap sw 0 0' >> /etc/fstab
        log_info "Swap created"
    else
        log_info "Swap already exists"
    fi

    log_info "Server setup complete!"
}

# Phase 2: Deploy Application
deploy_app() {
    log_info "Deploying application..."

    # Create app directory
    mkdir -p $APP_DIR
    mkdir -p $BACKUP_DIR

    # Set ownership
    chown -R $DEPLOY_USER:$DEPLOY_USER $APP_DIR
    chown -R $DEPLOY_USER:$DEPLOY_USER $BACKUP_DIR

    log_info "Application directories created"
    log_info "Please transfer your code to $APP_DIR"
    log_info "Then run: sudo ./deploy.sh start"
}

# Phase 3: Start Services
start_services() {
    log_info "Starting services..."

    cd $APP_DIR

    # Check if .env exists
    if [ ! -f .env ]; then
        log_error ".env file not found!"
        log_error "Please create .env file with required credentials"
        exit 1
    fi

    # Build Docker images
    log_info "Building Docker images..."
    docker-compose build

    # Start services
    log_info "Starting Docker containers..."
    docker-compose up -d

    # Wait for services to be ready
    log_info "Waiting for services to start..."
    sleep 10

    # Start PM2
    log_info "Starting PM2 processes..."
    su - $DEPLOY_USER -c "cd $APP_DIR && pm2 start Docker/pm2.config.js"
    su - $DEPLOY_USER -c "pm2 save"

    # Setup PM2 startup
    log_info "Configuring PM2 startup..."
    env PATH=$PATH:/usr/bin pm2 startup systemd -u $DEPLOY_USER --hp /home/$DEPLOY_USER

    log_info "Services started successfully!"
}

# Phase 4: Setup Nginx (optional)
setup_nginx() {
    log_info "Setting up Nginx..."

    if [ -z "$1" ]; then
        log_error "Please provide domain name: ./deploy.sh nginx yourdomain.com"
        exit 1
    fi

    DOMAIN=$1

    # Install Nginx
    apt install nginx -y

    # Create Nginx config
    cat > /etc/nginx/sites-available/platinum-ai << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location /voice/webhook {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

    # Enable site
    ln -sf /etc/nginx/sites-available/platinum-ai /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default

    # Test and restart Nginx
    nginx -t
    systemctl restart nginx

    log_info "Nginx configured for $DOMAIN"
    log_info "To setup SSL, run: sudo certbot --nginx -d $DOMAIN"
}

# Phase 5: Setup SSL
setup_ssl() {
    log_info "Setting up SSL..."

    if [ -z "$1" ]; then
        log_error "Please provide domain name: ./deploy.sh ssl yourdomain.com"
        exit 1
    fi

    DOMAIN=$1

    # Install Certbot
    apt install certbot python3-certbot-nginx -y

    # Get certificate
    certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN

    log_info "SSL certificate installed for $DOMAIN"
}

# Phase 6: Setup Backups
setup_backups() {
    log_info "Setting up automated backups..."

    # Create backup script
    cat > $BACKUP_DIR/backup.sh << 'EOF'
#!/bin/bash
# Automated backup script

BACKUP_DIR="/home/deploy/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup Docker volumes
docker run --rm \
  -v platinum_postgres-data:/data \
  -v $BACKUP_DIR:/backup \
  ubuntu tar czf /backup/postgres_$DATE.tar.gz /data

# Backup application data
tar czf $BACKUP_DIR/app_data_$DATE.tar.gz \
  /home/deploy/platinum-ai/Done \
  /home/deploy/platinum-ai/Logs \
  /home/deploy/platinum-ai/Briefings

# Keep only last 7 days
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

    chmod +x $BACKUP_DIR/backup.sh
    chown $DEPLOY_USER:$DEPLOY_USER $BACKUP_DIR/backup.sh

    # Add to crontab
    (crontab -u $DEPLOY_USER -l 2>/dev/null; echo "0 2 * * * $BACKUP_DIR/backup.sh") | crontab -u $DEPLOY_USER -

    log_info "Automated backups configured (daily at 2 AM)"
}

# Status check
check_status() {
    log_info "Checking system status..."

    echo ""
    echo "=== Docker Containers ==="
    docker ps

    echo ""
    echo "=== PM2 Processes ==="
    su - $DEPLOY_USER -c "pm2 status"

    echo ""
    echo "=== Disk Usage ==="
    df -h

    echo ""
    echo "=== Memory Usage ==="
    free -h

    echo ""
    echo "=== API Health Check ==="
    curl -s http://localhost:8000/health | python3 -m json.tool || echo "API not responding"
}

# Stop services
stop_services() {
    log_info "Stopping services..."

    su - $DEPLOY_USER -c "pm2 stop all"
    cd $APP_DIR && docker-compose down

    log_info "Services stopped"
}

# Restart services
restart_services() {
    log_info "Restarting services..."

    cd $APP_DIR
    docker-compose restart
    su - $DEPLOY_USER -c "pm2 restart all"

    log_info "Services restarted"
}

# View logs
view_logs() {
    log_info "Viewing logs..."

    echo "=== PM2 Logs ==="
    su - $DEPLOY_USER -c "pm2 logs --lines 50"
}

# Main script
case "$1" in
    setup)
        check_root
        setup_server
        deploy_app
        ;;
    start)
        check_root
        start_services
        ;;
    stop)
        check_root
        stop_services
        ;;
    restart)
        check_root
        restart_services
        ;;
    status)
        check_status
        ;;
    logs)
        view_logs
        ;;
    nginx)
        check_root
        setup_nginx "$2"
        ;;
    ssl)
        check_root
        setup_ssl "$2"
        ;;
    backup)
        check_root
        setup_backups
        ;;
    *)
        echo "Platinum Tier - Deployment Script"
        echo ""
        echo "Usage: $0 {command} [options]"
        echo ""
        echo "Commands:"
        echo "  setup          - Initial server setup (run once)"
        echo "  start          - Start all services"
        echo "  stop           - Stop all services"
        echo "  restart        - Restart all services"
        echo "  status         - Check system status"
        echo "  logs           - View PM2 logs"
        echo "  nginx DOMAIN   - Setup Nginx for domain"
        echo "  ssl DOMAIN     - Setup SSL certificate"
        echo "  backup         - Setup automated backups"
        echo ""
        echo "Example workflow:"
        echo "  1. sudo ./deploy.sh setup"
        echo "  2. Transfer code to /home/deploy/platinum-ai"
        echo "  3. Create .env file with credentials"
        echo "  4. sudo ./deploy.sh start"
        echo "  5. sudo ./deploy.sh nginx yourdomain.com"
        echo "  6. sudo ./deploy.sh ssl yourdomain.com"
        echo "  7. sudo ./deploy.sh backup"
        exit 1
        ;;
esac

exit 0
