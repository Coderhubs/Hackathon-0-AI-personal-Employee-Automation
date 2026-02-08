// PM2 Configuration for Platinum Tier AI Employee
// Ensures 99.9% uptime with auto-restart and monitoring

module.exports = {
  apps: [
    {
      name: 'manager-agent',
      script: 'Agents/manager_agent.py',
      interpreter: 'python3',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        AGENT_TYPE: 'manager'
      },
      error_file: 'Logs/pm2-manager-error.log',
      out_file: 'Logs/pm2-manager-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000
    },
    {
      name: 'gmail-watcher',
      script: 'gmail_watcher.py',
      interpreter: 'python3',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production',
        WATCHER_TYPE: 'gmail'
      },
      error_file: 'Logs/pm2-gmail-error.log',
      out_file: 'Logs/pm2-gmail-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000
    },
    {
      name: 'linkedin-watcher',
      script: 'linkedin_watcher.py',
      interpreter: 'python3',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production',
        WATCHER_TYPE: 'linkedin'
      },
      error_file: 'Logs/pm2-linkedin-error.log',
      out_file: 'Logs/pm2-linkedin-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000
    },
    {
      name: 'filesystem-watcher',
      script: 'filesystem_watcher.py',
      interpreter: 'python3',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production',
        WATCHER_TYPE: 'filesystem'
      },
      error_file: 'Logs/pm2-filesystem-error.log',
      out_file: 'Logs/pm2-filesystem-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000
    },
    {
      name: 'voice-handler',
      script: 'Voice/call_handler.py',
      interpreter: 'python3',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production',
        SERVICE_TYPE: 'voice'
      },
      error_file: 'Logs/pm2-voice-error.log',
      out_file: 'Logs/pm2-voice-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000
    },
    {
      name: 'memory-sync',
      script: 'Memory/conversation_manager.py',
      interpreter: 'python3',
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      watch: false,
      max_memory_restart: '500M',
      env: {
        NODE_ENV: 'production',
        SERVICE_TYPE: 'memory'
      },
      error_file: 'Logs/pm2-memory-error.log',
      out_file: 'Logs/pm2-memory-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000
    },
    {
      name: 'api-server',
      script: 'api_server.py',
      interpreter: 'python3',
      instances: 2,
      exec_mode: 'cluster',
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'production',
        PORT: 8000
      },
      error_file: 'Logs/pm2-api-error.log',
      out_file: 'Logs/pm2-api-out.log',
      log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
      merge_logs: true,
      min_uptime: '10s',
      max_restarts: 10,
      restart_delay: 4000
    }
  ],

  // Deployment configuration
  deploy: {
    production: {
      user: 'deploy',
      host: ['your-server-ip'],
      ref: 'origin/main',
      repo: 'git@github.com:your-repo/platinum-ai.git',
      path: '/var/www/platinum-ai',
      'post-deploy': 'pip install -r requirements.txt && pm2 reload Docker/pm2.config.js --env production',
      env: {
        NODE_ENV: 'production'
      }
    }
  }
};
