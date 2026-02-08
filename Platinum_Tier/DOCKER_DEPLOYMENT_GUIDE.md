# 🐳 DOCKER DESKTOP INSTALLATION & DEPLOYMENT GUIDE

## ⚠️ DECISION TIME

**Current Status:** Your PM2 system is working perfectly (37+ min uptime, 23 files)

**Question:** Do you have time to install Docker Desktop? (15-30 minutes)

**If YES:** Follow this guide
**If NO:** Stick with PM2 (already production-ready for hackathon)

---

## 📥 STEP 1: INSTALL DOCKER DESKTOP FOR WINDOWS

### Download Docker Desktop:
1. Go to: https://www.docker.com/products/docker-desktop/
2. Click "Download for Windows"
3. Run the installer: `Docker Desktop Installer.exe`

### Installation Steps:
1. **Accept License Agreement**
2. **Configuration:**
   - ✅ Enable WSL 2 (recommended)
   - ✅ Add shortcut to desktop
3. **Install** (takes 5-10 minutes)
4. **Restart Computer** (required)

### After Restart:
1. Open Docker Desktop from Start Menu
2. Wait for Docker Engine to start (2-3 minutes)
3. You'll see "Docker Desktop is running" in system tray

### Verify Installation:
Open PowerShell or Command Prompt:
```bash
docker --version
docker-compose --version
docker ps
```

Expected output:
```
Docker version 24.x.x
Docker Compose version v2.x.x
CONTAINER ID   IMAGE   ...
```

---

## 🛑 STEP 2: STOP PM2 PROCESSES (AVOID PORT CONFLICTS)

Before starting Docker, stop PM2 to free up ports:

```bash
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"
pm2 stop all
pm2 delete all
```

**Why?** Docker containers will use the same ports (8000, 8001, 8002) as PM2.

---

## 🐳 STEP 3: PREPARE DOCKER DEPLOYMENT

### Navigate to Platinum_Tier:
```bash
cd "C:\Users\Dell\Desktop\New folder (3)\AI_personal_Employee\Platinum_Tier"
```

### Check Docker Compose File:
```bash
type Docker\docker-compose.yml
```

### Create .env File (Required):
```bash
copy .env.example .env
```

Then edit `.env` file with your actual credentials:
```
GMAIL_API_KEY=your_key_here
FACEBOOK_TOKEN=your_token_here
INSTAGRAM_TOKEN=your_token_here
TWITTER_API_KEY=your_key_here
VAPI_API_KEY=your_key_here
PINECONE_API_KEY=your_key_here
ODOO_URL=your_odoo_url
ODOO_DB=your_db_name
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password
ENCRYPTION_KEY=your_encryption_key
JWT_SECRET=your_jwt_secret
POSTGRES_PASSWORD=your_postgres_password
GRAFANA_PASSWORD=your_grafana_password
```

**For hackathon demo:** You can use dummy values:
```
GMAIL_API_KEY=demo_key
FACEBOOK_TOKEN=demo_token
INSTAGRAM_TOKEN=demo_token
TWITTER_API_KEY=demo_key
VAPI_API_KEY=demo_key
PINECONE_API_KEY=demo_key
ODOO_URL=http://localhost
ODOO_DB=demo_db
ODOO_USERNAME=admin
ODOO_PASSWORD=admin
ENCRYPTION_KEY=demo_encryption_key_32_characters_long
JWT_SECRET=demo_jwt_secret_key
POSTGRES_PASSWORD=postgres123
GRAFANA_PASSWORD=admin123
```

---

## 🚀 STEP 4: START DOCKER CONTAINERS

### Build and Start All Services:
```bash
docker-compose -f Docker/docker-compose.yml up -d
```

**What this does:**
- Builds Docker images (first time: 5-10 minutes)
- Starts 7 containers:
  1. platinum-ai (main application)
  2. redis (caching)
  3. postgres (database)
  4. chromadb (vector storage)
  5. prometheus (metrics)
  6. grafana (visualization)
  7. (nginx if configured)

**Flags:**
- `-f Docker/docker-compose.yml` = specify config file
- `-d` = detached mode (runs in background)

### First-Time Build (Expect 5-10 Minutes):
```
[+] Building 300.5s (15/15) FINISHED
[+] Running 7/7
 ✔ Container platinum-redis       Started
 ✔ Container platinum-postgres    Started
 ✔ Container platinum-chromadb    Started
 ✔ Container platinum-ai-employee Started
 ✔ Container platinum-prometheus  Started
 ✔ Container platinum-grafana     Started
```

---

## ✅ STEP 5: VERIFY DOCKER DEPLOYMENT

### Check Running Containers:
```bash
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE                    STATUS         PORTS
abc123         platinum-ai:latest       Up 2 minutes   0.0.0.0:8000->8000/tcp
def456         redis:7-alpine           Up 2 minutes   0.0.0.0:6379->6379/tcp
ghi789         postgres:15-alpine       Up 2 minutes   0.0.0.0:5432->5432/tcp
jkl012         chromadb/chroma:latest   Up 2 minutes   0.0.0.0:8003->8000/tcp
mno345         prom/prometheus:latest   Up 2 minutes   0.0.0.0:9090->9090/tcp
pqr678         grafana/grafana:latest   Up 2 minutes   0.0.0.0:3000->3000/tcp
```

### Check Container Logs:
```bash
# All containers
docker-compose -f Docker/docker-compose.yml logs

# Specific container
docker logs platinum-ai-employee

# Follow logs (real-time)
docker logs -f platinum-ai-employee
```

### Check Container Health:
```bash
docker ps --format "table {{.Names}}\t{{.Status}}"
```

---

## 🌐 STEP 6: ACCESS YOUR SERVICES

Once containers are running:

**Main Application:**
- API: http://localhost:8000
- Health Check: http://localhost:8000/health

**Monitoring:**
- Grafana: http://localhost:3000 (admin/admin123)
- Prometheus: http://localhost:9090

**Databases:**
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- ChromaDB: http://localhost:8003

---

## 🎬 STEP 7: DEMO WITH DOCKER

### Show Docker Status:
```bash
docker ps
```

**Say:** "The system is running in 7 Docker containers with auto-restart, health checks, and monitoring."

### Show Container Logs:
```bash
docker logs platinum-ai-employee --tail 20
```

**Say:** "Here's the live activity from the containerized application."

### Show Monitoring Dashboard:
Open browser: http://localhost:3000
**Say:** "This is Grafana showing real-time metrics from all containers."

---

## 🛠️ DOCKER COMMANDS REFERENCE

### Start Containers:
```bash
docker-compose -f Docker/docker-compose.yml up -d
```

### Stop Containers:
```bash
docker-compose -f Docker/docker-compose.yml down
```

### Restart Containers:
```bash
docker-compose -f Docker/docker-compose.yml restart
```

### View Logs:
```bash
docker-compose -f Docker/docker-compose.yml logs -f
```

### Rebuild Containers:
```bash
docker-compose -f Docker/docker-compose.yml up -d --build
```

### Remove Everything:
```bash
docker-compose -f Docker/docker-compose.yml down -v
```

---

## 🆚 PM2 vs DOCKER COMPARISON

### PM2 (Current - Working):
✅ Lightweight (358 MB memory)
✅ Fast startup (instant)
✅ Simple to use
✅ Already working (37+ min uptime)
✅ Perfect for hackathon demo
❌ No containerization
❌ No built-in monitoring dashboard

### Docker (Optional Enhancement):
✅ Full containerization
✅ Includes monitoring (Grafana)
✅ Includes databases (PostgreSQL, Redis)
✅ Production-grade infrastructure
✅ Easy to deploy anywhere
❌ Heavier (1-2 GB memory)
❌ Slower startup (2-3 minutes)
❌ Requires installation (15-30 min)

---

## ⚠️ TROUBLESHOOTING

### Problem: "docker: command not found"
**Solution:** Docker Desktop not installed or not in PATH
- Install Docker Desktop
- Restart terminal after installation

### Problem: "Cannot connect to Docker daemon"
**Solution:** Docker Desktop not running
- Open Docker Desktop application
- Wait for "Docker Desktop is running" message

### Problem: "Port already in use"
**Solution:** PM2 still running or another service using port
```bash
# Stop PM2
pm2 stop all
pm2 delete all

# Or find what's using the port
netstat -ano | findstr :8000
```

### Problem: "Build failed"
**Solution:** Missing dependencies or files
- Check Dockerfile exists
- Check requirements.txt exists
- Check all Python files exist

### Problem: Containers keep restarting
**Solution:** Check logs for errors
```bash
docker logs platinum-ai-employee
```

---

## 🎯 RECOMMENDATION FOR HACKATHON

### If Hackathon is TODAY or TOMORROW:
**Stick with PM2** (already working perfectly)
- ✅ 37+ min uptime proven
- ✅ 23 files created
- ✅ 0 crashes
- ✅ Ready to demo NOW

### If Hackathon is 3+ DAYS AWAY:
**Install Docker** (adds impressive infrastructure)
- ✅ Full containerization
- ✅ Monitoring dashboards
- ✅ Production-grade setup
- ✅ More impressive to judges

---

## 📋 DOCKER INSTALLATION CHECKLIST

- [ ] Download Docker Desktop
- [ ] Install Docker Desktop
- [ ] Restart computer
- [ ] Open Docker Desktop
- [ ] Verify: `docker --version`
- [ ] Stop PM2: `pm2 stop all`
- [ ] Create .env file
- [ ] Run: `docker-compose up -d`
- [ ] Verify: `docker ps`
- [ ] Test: http://localhost:8000/health
- [ ] Open Grafana: http://localhost:3000

---

## 🏆 BOTTOM LINE

**Your PM2 system is ALREADY production-ready for hackathon.**

**Docker is an ENHANCEMENT, not a REQUIREMENT.**

**If you have time:** Install Docker (impressive infrastructure)
**If time is tight:** Stick with PM2 (already working perfectly)

**Both are valid production deployments!**

---

**Need help with Docker installation?**
Follow this guide step-by-step or ask for help at each stage.

**Want to stick with PM2?**
Your system is ready! Use LIVE_DEMO_SCRIPT.txt for your presentation.

---

🚀 **You're ready either way!** 🚀
