# 🚀 PLATINUM TIER - CLOUD MIGRATION STRATEGY

**From:** Gold Tier (Local Windows)
**To:** Platinum Tier (Cloud VPS with 99.9% Uptime)

---

## 📋 MIGRATION OVERVIEW

### Current State (Gold Tier)
- Windows batch scripts (start_gold_tier.bat)
- Manual process management
- Local file system
- No auto-restart
- Single machine dependency

### Target State (Platinum Tier)
- Docker containers
- PM2 process management
- Cloud VPS (DigitalOcean/AWS/GCP)
- Auto-restart on failure
- 99.9% uptime guarantee
- Horizontal scaling ready

---

## 🎯 MIGRATION STEPS

### Phase 1: Preparation (Day 1)

#### 1.1 Choose Cloud Provider

**Recommended: DigitalOcean**
- Cost-effective ($20-40/month for 4GB RAM droplet)
- Simple interface
- Good documentation
- Managed databases available

**Alternatives:**
- AWS EC2 (more complex, more features)
- Google Cloud Compute Engine
- Linode
- Vultr

#### 1.2 Server Specifications

**Minimum Requirements:**
```
CPU: 2 vCPUs
RAM: 4GB
Storage: 80GB SSD
OS: Ubuntu 22.04 LTS
```

**Recommended:**
```
CPU: 4 vCPUs
RAM: 8GB
Storage: 160GB SSD
OS: Ubuntu 22.04 LTS
```

#### 1.3 Prepare Gold Tier System

```bash
# 1. Copy Gold Tier to Platinum Tier
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee"
cp -r Gold_Tier/* Platinum_Tier/

# 2. Test locally with Docker
cd Platinum_Tier
docker build -t platinum-ai-test .
docker run -d platinum-ai-test

# 3. Verify all components work
docker ps
docker logs <container_id>
```

---

### Phase 2: Cloud Setup (Day 1-2)

#### 2.1 Create VPS Instance

**DigitalOcean Example:**
```bash
# Using doctl CLI
doctl compute droplet create platinum-ai \
  --size s-2vcpu-4gb \
  --image ubuntu-22-04-x64 \
  --region nyc1 \
  --ssh-keys <your-ssh-key-id>

# Or use web interface:
# 1. Go to cloud.digitalocean.com
# 2. Create Droplet
# 3. Choose Ubuntu 22.04
# 4. Select 4GB RAM plan
# 5. Add SSH key
# 6. Create
```

#### 2.2 Initial Server Setup

```bash
# SSH into server
ssh root@<your-server-ip>

# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Install Node.js and PM2
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
npm install -g pm2

# Create deployment user
adduser deploy
usermod -aG docker deploy
usermod -aG sudo deploy

# Setup firewall
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 8000/tcp  # API
ufw enable
```

#### 2.3 Setup Swap (Important for 4GB RAM)

```bash
# Create 4GB swap
fallocate -l 4G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

---

### Phase 3: Deployment (Day 2)

#### 3.1 Transfer Code to Server

**Option A: Git (Recommended)**
```bash
# On local machine, push to GitHub
cd Platinum_Tier
git init
git add .
git commit -m "Initial Platinum Tier commit"
git remote add origin <your-repo-url>
git push -u origin main

# On server
su - deploy
git clone <your-repo-url> /home/deploy/platinum-ai
cd /home/deploy/platinum-ai
```

**Option B: SCP**
```bash
# On local machine
cd Platinum_Tier
tar -czf platinum-ai.tar.gz .
scp platinum-ai.tar.gz deploy@<server-ip>:/home/deploy/

# On server
tar -xzf platinum-ai.tar.gz
```

#### 3.2 Setup Environment Variables

```bash
# On server
cd /home/deploy/platinum-ai

# Create .env file
nano .env

# Add all credentials:
GMAIL_API_KEY=your_key
FACEBOOK_TOKEN=your_token
INSTAGRAM_TOKEN=your_token
TWITTER_API_KEY=your_key
VAPI_API_KEY=your_key
PINECONE_API_KEY=your_key
ODOO_URL=your_url
ODOO_DB=your_db
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password
ENCRYPTION_KEY=your_encryption_key
POSTGRES_PASSWORD=your_postgres_password
GRAFANA_PASSWORD=your_grafana_password

# Secure the file
chmod 600 .env
```

#### 3.3 Encrypt Credentials

```bash
# Use secrets manager to encrypt .env
python3 Security/secrets_manager.py

# This creates .env.encrypted
# Delete original .env after verification
rm .env
```

#### 3.4 Build and Deploy

```bash
# Build Docker image
docker build -t platinum-ai:latest .

# Start services with docker-compose
docker-compose up -d

# Verify all containers running
docker ps

# Check logs
docker-compose logs -f
```

---

### Phase 4: PM2 Setup (Day 2)

#### 4.1 Configure PM2

```bash
# Start PM2 with ecosystem file
pm2 start Docker/pm2.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup systemd
# Run the command it outputs

# Verify PM2 status
pm2 status
pm2 monit
```

#### 4.2 PM2 Monitoring

```bash
# View logs
pm2 logs

# View specific app logs
pm2 logs manager-agent

# Monitor resources
pm2 monit

# Restart specific app
pm2 restart manager-agent

# Restart all
pm2 restart all
```

---

### Phase 5: Domain & SSL (Day 2-3)

#### 5.1 Setup Domain

```bash
# Point your domain to server IP
# Add A record: platinum-ai.yourdomain.com -> <server-ip>

# Install Nginx
apt install nginx -y

# Configure Nginx
nano /etc/nginx/sites-available/platinum-ai

# Add configuration:
server {
    listen 80;
    server_name platinum-ai.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /voice/webhook {
        proxy_pass http://localhost:8001;
    }
}

# Enable site
ln -s /etc/nginx/sites-available/platinum-ai /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

#### 5.2 Setup SSL with Let's Encrypt

```bash
# Install Certbot
apt install certbot python3-certbot-nginx -y

# Get SSL certificate
certbot --nginx -d platinum-ai.yourdomain.com

# Auto-renewal is configured automatically
# Test renewal
certbot renew --dry-run
```

---

### Phase 6: Monitoring & Backup (Day 3)

#### 6.1 Setup Monitoring

```bash
# PM2 monitoring is already active

# Access Grafana dashboard
# http://<server-ip>:3000
# Login with credentials from .env

# Access Prometheus
# http://<server-ip>:9090
```

#### 6.2 Setup Automated Backups

```bash
# Create backup script
nano /home/deploy/backup.sh

#!/bin/bash
# Backup script for Platinum AI

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

# Make executable
chmod +x /home/deploy/backup.sh

# Add to crontab
crontab -e

# Add line:
0 2 * * * /home/deploy/backup.sh
```

---

### Phase 7: Testing & Validation (Day 3)

#### 7.1 Functionality Tests

```bash
# Test API endpoint
curl http://localhost:8000/health

# Test voice webhook
curl -X POST http://localhost:8001/voice/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'

# Check PM2 status
pm2 status

# Check Docker containers
docker ps

# Check logs
pm2 logs --lines 50
docker-compose logs --tail=50
```

#### 7.2 Load Testing

```bash
# Install Apache Bench
apt install apache2-utils -y

# Test API performance
ab -n 1000 -c 10 http://localhost:8000/health

# Monitor during test
pm2 monit
```

#### 7.3 Failure Recovery Test

```bash
# Kill a process and verify auto-restart
pm2 stop manager-agent
# Wait 5 seconds
pm2 status
# Should show "online" again

# Stop Docker container
docker stop platinum-ai-employee
# Wait 10 seconds
docker ps
# Should be running again (restart: unless-stopped)
```

---

## 📊 UPTIME CALCULATION

### Target: 99.9% Uptime

**Allowed Downtime:**
- Per Year: 8.76 hours
- Per Month: 43.8 minutes
- Per Week: 10.1 minutes
- Per Day: 1.44 minutes

### Achieving 99.9% Uptime

**1. Auto-Restart (PM2)**
- Restarts failed processes in <5 seconds
- Handles memory leaks with max_memory_restart
- Exponential backoff for persistent failures

**2. Docker Health Checks**
- Monitors container health every 30 seconds
- Auto-restarts unhealthy containers
- Prevents cascading failures

**3. Monitoring & Alerts**
- Prometheus metrics
- Grafana dashboards
- Email alerts on failures

**4. Redundancy**
- Multiple PM2 instances
- Database replication (optional)
- Load balancer ready

---

## 💰 COST ESTIMATE

### Monthly Costs

**DigitalOcean Droplet (4GB):** $24/month
**Managed PostgreSQL (optional):** $15/month
**Backups (20GB):** $2/month
**Domain:** $12/year ($1/month)
**SSL Certificate:** Free (Let's Encrypt)

**Total:** ~$42/month

### Cost Optimization

**Use Reserved Instances:** Save 20-30%
**Use Spot Instances:** Save up to 70% (less reliable)
**Self-host Database:** Save $15/month
**Use CloudFlare:** Free CDN and DDoS protection

---

## 🔧 MAINTENANCE

### Daily
- Check PM2 status: `pm2 status`
- Review logs: `pm2 logs --lines 100`
- Check disk space: `df -h`

### Weekly
- Review Grafana dashboards
- Check backup integrity
- Update dependencies: `apt update && apt upgrade`

### Monthly
- Rotate logs
- Review security updates
- Test disaster recovery
- Optimize database

---

## 🚨 DISASTER RECOVERY

### Backup Strategy
- **Automated daily backups** at 2 AM
- **7-day retention** for quick recovery
- **Monthly archives** for long-term storage
- **Off-site backup** to S3/Spaces

### Recovery Procedure

```bash
# 1. Provision new server
# 2. Install Docker, PM2
# 3. Restore from backup

# Restore PostgreSQL
docker run --rm \
  -v platinum_postgres-data:/data \
  -v /path/to/backup:/backup \
  ubuntu tar xzf /backup/postgres_YYYYMMDD.tar.gz -C /

# Restore application data
tar xzf /path/to/backup/app_data_YYYYMMDD.tar.gz -C /

# 4. Start services
docker-compose up -d
pm2 start Docker/pm2.config.js

# 5. Verify
pm2 status
docker ps
```

---

## ✅ MIGRATION CHECKLIST

### Pre-Migration
- [ ] Choose cloud provider
- [ ] Create VPS instance
- [ ] Setup SSH keys
- [ ] Configure firewall
- [ ] Install Docker, PM2, Node.js

### Migration
- [ ] Transfer code to server
- [ ] Setup environment variables
- [ ] Encrypt credentials
- [ ] Build Docker images
- [ ] Start services with docker-compose
- [ ] Configure PM2
- [ ] Setup domain and SSL

### Post-Migration
- [ ] Test all endpoints
- [ ] Verify auto-restart
- [ ] Setup monitoring
- [ ] Configure backups
- [ ] Load testing
- [ ] Document procedures

### Ongoing
- [ ] Monitor uptime
- [ ] Review logs daily
- [ ] Update dependencies weekly
- [ ] Test backups monthly
- [ ] Optimize performance quarterly

---

## 🎯 SUCCESS METRICS

- **Uptime:** >99.9%
- **Response Time:** <200ms (API)
- **Error Rate:** <0.1%
- **Recovery Time:** <30 seconds
- **Backup Success:** 100%

---

*Platinum Tier - Cloud Migration Strategy*
*Target: 99.9% Uptime with Docker + PM2*
