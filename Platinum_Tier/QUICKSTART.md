# 🚀 PLATINUM TIER - QUICK START GUIDE

**Get your Enterprise AI Employee running in the cloud in under 30 minutes**

---

## 📋 PREREQUISITES

Before starting, ensure you have:

- [ ] Cloud VPS account (DigitalOcean, AWS, or GCP)
- [ ] Domain name (optional, but recommended)
- [ ] API keys for integrations (Vapi, Anthropic, etc.)
- [ ] SSH access to your server
- [ ] Git installed locally

---

## 🎯 DEPLOYMENT OPTIONS

### Option A: Automated Deployment (Recommended)
**Time: ~15 minutes**

Use the automated deployment script for fastest setup.

### Option B: Manual Deployment
**Time: ~30 minutes**

Follow the detailed Cloud Migration Guide for full control.

---

## 🚀 OPTION A: AUTOMATED DEPLOYMENT

### Step 1: Provision Server

**DigitalOcean (Recommended):**
```bash
# Create 4GB droplet
doctl compute droplet create platinum-ai \
  --size s-2vcpu-4gb \
  --image ubuntu-22-04-x64 \
  --region nyc1 \
  --ssh-keys <your-ssh-key-id>
```

**Or use web interface:**
1. Go to cloud.digitalocean.com
2. Create Droplet → Ubuntu 22.04 → 4GB RAM
3. Add your SSH key
4. Create

### Step 2: Initial Server Setup

```bash
# SSH into your server
ssh root@<your-server-ip>

# Download deployment script
curl -O https://raw.githubusercontent.com/yourusername/platinum-ai/main/deploy.sh
chmod +x deploy.sh

# Run automated setup
sudo ./deploy.sh setup
```

This will:
- ✅ Install Docker, Docker Compose, Node.js, PM2
- ✅ Create deployment user
- ✅ Configure firewall
- ✅ Setup swap space
- ✅ Create application directories

### Step 3: Transfer Code

**Option 3A: Using Git (Recommended)**
```bash
# On your local machine
cd Platinum_Tier
git init
git add .
git commit -m "Initial Platinum Tier deployment"
git remote add origin <your-repo-url>
git push -u origin main

# On server
su - deploy
git clone <your-repo-url> /home/deploy/platinum-ai
```

**Option 3B: Using SCP**
```bash
# On your local machine
cd Platinum_Tier
tar -czf platinum-ai.tar.gz .
scp platinum-ai.tar.gz deploy@<server-ip>:/home/deploy/

# On server
su - deploy
cd /home/deploy
tar -xzf platinum-ai.tar.gz -C platinum-ai
```

### Step 4: Configure Environment

```bash
# On server
cd /home/deploy/platinum-ai

# Copy example env file
cp .env.example .env

# Edit with your credentials
nano .env
```

**Required credentials:**
```bash
# Minimum required for basic operation
ANTHROPIC_API_KEY=sk-ant-...
ENCRYPTION_KEY=<generate with: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">
POSTGRES_PASSWORD=<secure-password>
REDIS_PASSWORD=<secure-password>
SECRETS_MASTER_PASSWORD=<very-secure-password>

# Optional but recommended
VAPI_API_KEY=<your-vapi-key>
GMAIL_API_KEY=<your-gmail-key>
```

**Generate encryption key:**
```bash
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### Step 5: Start Services

```bash
# Start all services
sudo /home/deploy/platinum-ai/deploy.sh start
```

This will:
- ✅ Build Docker images
- ✅ Start Docker containers (Redis, PostgreSQL, ChromaDB, etc.)
- ✅ Start PM2 processes (7 agents)
- ✅ Configure auto-restart

### Step 6: Verify Deployment

```bash
# Check system status
sudo /home/deploy/platinum-ai/deploy.sh status
```

**Expected output:**
```
=== Docker Containers ===
platinum-ai-employee    running
redis                   running
postgres                running
chromadb                running

=== PM2 Processes ===
manager-agent          online
gmail-watcher          online
linkedin-watcher       online
filesystem-watcher     online
voice-handler          online
memory-sync            online
api-server             online
```

### Step 7: Test API

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2026-02-08T...",
  "version": "1.0.0"
}
```

### Step 8: Setup Domain & SSL (Optional)

```bash
# Setup Nginx for your domain
sudo /home/deploy/platinum-ai/deploy.sh nginx yourdomain.com

# Setup SSL certificate
sudo /home/deploy/platinum-ai/deploy.sh ssl yourdomain.com
```

### Step 9: Setup Automated Backups

```bash
# Configure daily backups
sudo /home/deploy/platinum-ai/deploy.sh backup
```

---

## 🎉 DEPLOYMENT COMPLETE!

Your Platinum Tier AI Employee is now running with:
- ✅ 99.9% uptime (auto-restart on failure)
- ✅ Multi-agent architecture
- ✅ Voice integration (Vapi)
- ✅ Long-term memory (Vector DB)
- ✅ Encrypted credentials
- ✅ Automated backups

---

## 📊 ACCESSING YOUR SYSTEM

### API Endpoints

**Base URL:** `http://your-server-ip:8000` or `https://yourdomain.com`

**Key endpoints:**
```bash
# Health check
GET /health

# System status
GET /status

# Create task
POST /tasks
{
  "content": "Send email to john@example.com",
  "priority": 5
}

# Voice webhook (for Vapi)
POST /voice/webhook

# Memory search
POST /memory/search
{
  "query": "What did we discuss about the project?",
  "top_k": 5
}
```

### Monitoring Dashboards

**Grafana:** `http://your-server-ip:3000`
- Username: admin
- Password: (from .env GRAFANA_ADMIN_PASSWORD)

**Prometheus:** `http://your-server-ip:9090`

### Logs

```bash
# View all PM2 logs
pm2 logs

# View specific agent logs
pm2 logs manager-agent

# View Docker logs
docker-compose logs -f

# View log files
tail -f /home/deploy/platinum-ai/Logs/*.log
```

---

## 🔧 COMMON OPERATIONS

### Start/Stop/Restart

```bash
# Stop all services
sudo ./deploy.sh stop

# Start all services
sudo ./deploy.sh start

# Restart all services
sudo ./deploy.sh restart

# Restart specific PM2 process
pm2 restart manager-agent
```

### View Status

```bash
# Full system status
sudo ./deploy.sh status

# PM2 status only
pm2 status

# Docker status only
docker ps

# Monitor resources
pm2 monit
```

### Update Code

```bash
# Pull latest changes
cd /home/deploy/platinum-ai
git pull

# Rebuild and restart
docker-compose build
sudo ./deploy.sh restart
```

### View Logs

```bash
# All logs
sudo ./deploy.sh logs

# Last 100 lines
pm2 logs --lines 100

# Specific agent
pm2 logs manager-agent --lines 50
```

---

## 🧪 TESTING YOUR DEPLOYMENT

### Run System Tests

```bash
cd /home/deploy/platinum-ai
python3 test_system.py
```

**Expected output:**
```
=== FINAL TEST REPORT ===
Total Tests:  45
Passed:       45
Failed:       0
Pass Rate:    100.0%

✓ All tests passed! System is ready for deployment.
```

### Manual Testing

**1. Test Task Creation:**
```bash
# Create a test task
echo "Test task: Send email to test@example.com" > Needs_Action/TEST_TASK.txt

# Check manager agent logs
pm2 logs manager-agent --lines 20

# Verify task was processed
ls Pending_Approval/
```

**2. Test API:**
```bash
# Health check
curl http://localhost:8000/health

# Create task via API
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"content": "Test API task", "priority": 5}'
```

**3. Test Voice Integration:**
```bash
# Test webhook endpoint
curl -X POST http://localhost:8000/voice/webhook \
  -H "Content-Type: application/json" \
  -d '{"message": {"type": "test"}}'
```

**4. Test Memory:**
```bash
# Add conversation
curl -X POST http://localhost:8000/memory/add \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "test-001",
    "text": "This is a test conversation about project planning",
    "metadata": {"type": "test"}
  }'

# Search memory
curl -X POST http://localhost:8000/memory/search \
  -H "Content-Type: application/json" \
  -d '{"query": "project planning", "top_k": 5}'
```

---

## 🔒 SECURITY CHECKLIST

After deployment, verify:

- [ ] Changed all default passwords in .env
- [ ] Encrypted .env file using secrets manager
- [ ] Firewall configured (only ports 22, 80, 443, 8000 open)
- [ ] SSH key authentication enabled (password auth disabled)
- [ ] SSL certificate installed (if using domain)
- [ ] Backups configured and tested
- [ ] Monitoring alerts configured
- [ ] API rate limiting enabled
- [ ] CORS origins restricted (not using *)

### Encrypt Credentials

```bash
cd /home/deploy/platinum-ai

# Encrypt .env file
python3 Security/secrets_manager.py

# This creates .env.encrypted
# Delete original .env after verification
rm .env
```

---

## 📈 MONITORING & MAINTENANCE

### Daily Checks

```bash
# Quick status check
sudo ./deploy.sh status

# Check disk space
df -h

# Check memory
free -h
```

### Weekly Maintenance

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Check logs for errors
pm2 logs --lines 500 | grep -i error

# Verify backups
ls -lh /home/deploy/backups/
```

### Monthly Tasks

- Review Grafana dashboards
- Test disaster recovery
- Rotate encryption keys
- Optimize database
- Review and archive old logs

---

## 🚨 TROUBLESHOOTING

### Services Won't Start

```bash
# Check Docker
docker ps -a
docker-compose logs

# Check PM2
pm2 status
pm2 logs --err

# Check system resources
free -h
df -h
```

### High Memory Usage

```bash
# Check PM2 memory
pm2 monit

# Restart memory-heavy processes
pm2 restart manager-agent

# Check Docker memory
docker stats
```

### API Not Responding

```bash
# Check if API server is running
pm2 list | grep api-server

# Check API logs
pm2 logs api-server --lines 50

# Test locally
curl http://localhost:8000/health

# Check firewall
sudo ufw status
```

### Database Connection Issues

```bash
# Check PostgreSQL container
docker ps | grep postgres

# Check PostgreSQL logs
docker logs platinum_postgres_1

# Test connection
docker exec -it platinum_postgres_1 psql -U platinum -d platinum_ai
```

### Voice Integration Not Working

```bash
# Check Vapi configuration in .env
cat .env | grep VAPI

# Check voice handler logs
pm2 logs voice-handler

# Test webhook endpoint
curl -X POST http://localhost:8000/voice/webhook \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

---

## 🆘 GETTING HELP

### Check Logs First

```bash
# All logs
sudo ./deploy.sh logs

# Specific component
pm2 logs <component-name>
docker-compose logs <service-name>
```

### Common Issues

1. **Port already in use:** Change ports in docker-compose.yml
2. **Out of memory:** Increase swap or upgrade server
3. **Permission denied:** Check file ownership and permissions
4. **API key invalid:** Verify credentials in .env

### Support Resources

- Documentation: `/home/deploy/platinum-ai/README.md`
- Migration Guide: `/home/deploy/platinum-ai/CLOUD_MIGRATION_GUIDE.md`
- System Tests: `python3 test_system.py`

---

## 🎯 NEXT STEPS

Now that your Platinum Tier system is running:

1. **Configure Integrations**
   - Add Gmail API credentials
   - Setup Vapi phone number
   - Connect social media accounts
   - Configure Odoo ERP

2. **Customize Agents**
   - Modify agent behavior in `Agents/` directory
   - Add new specialist agents
   - Adjust task routing logic

3. **Setup Monitoring**
   - Configure Grafana dashboards
   - Setup email/Slack alerts
   - Create custom metrics

4. **Scale Up**
   - Add more PM2 instances
   - Setup load balancer
   - Enable database replication

---

## 📊 SUCCESS METRICS

Your system is performing well if:

- ✅ Uptime > 99.9% (check with `pm2 status`)
- ✅ API response time < 200ms (check Grafana)
- ✅ Error rate < 0.1% (check logs)
- ✅ Memory usage < 80% (check `free -h`)
- ✅ Disk usage < 80% (check `df -h`)
- ✅ All PM2 processes online (check `pm2 status`)
- ✅ All Docker containers running (check `docker ps`)

---

**🎉 Congratulations! Your Platinum Tier AI Employee is now operational!**

*For detailed information, see CLOUD_MIGRATION_GUIDE.md*
