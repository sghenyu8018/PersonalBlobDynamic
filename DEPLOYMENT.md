# 部署文档

本文档提供了个人技术博客系统从开发环境到生产环境的完整部署指南。

## 📋 目录

- [环境要求](#环境要求)
- [部署架构](#部署架构)
- [服务器准备](#服务器准备)
- [后端部署（Django）](#后端部署django)
- [前端部署（Next.js）](#前端部署nextjs)
- [Nginx配置](#nginx配置)
- [数据库配置](#数据库配置)
- [域名和SSL配置](#域名和ssl配置)
- [监控和维护](#监控和维护)
- [常见问题](#常见问题)

## 环境要求

### 服务器要求

- **操作系统**: Ubuntu 20.04 LTS 或更高版本（推荐）
- **内存**: 至少 2GB RAM
- **存储**: 至少 20GB 可用空间
- **网络**: 公网IP地址

### 软件要求

- **Python**: 3.11+
- **Node.js**: 18+
- **Nginx**: 1.18+
- **数据库**: PostgreSQL 12+（生产环境推荐）或 SQLite（开发环境）
- **进程管理**: Supervisor 或 systemd（推荐）
- **SSL证书**: Let's Encrypt（免费）

## 部署架构

```
用户请求
    ↓
Nginx (80/443端口)
    ↓
    ├──→ Next.js 前端 (localhost:3000)
    └──→ Django 后端 API (localhost:8000)
            ↓
        PostgreSQL 数据库
```

## 服务器准备

### 1. 更新系统

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. 创建部署用户

```bash
sudo adduser blog
sudo usermod -aG sudo blog
su - blog
```

### 3. 安装基础软件

```bash
# 安装必要工具
sudo apt install -y git curl wget build-essential

# 安装Python和pip
sudo apt install -y python3 python3-pip python3-venv

# 安装Node.js (使用NodeSource)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# 安装Nginx
sudo apt install -y nginx

# 安装PostgreSQL（如果使用）
sudo apt install -y postgresql postgresql-contrib
```

### 4. 安装数据库（PostgreSQL）

```bash
# 切换到postgres用户
sudo -u postgres psql

# 创建数据库和用户
CREATE DATABASE blogdb;
CREATE USER bloguser WITH PASSWORD 'your_secure_password';
ALTER ROLE bloguser SET client_encoding TO 'utf8';
ALTER ROLE bloguser SET default_transaction_isolation TO 'read committed';
ALTER ROLE bloguser SET timezone TO 'Asia/Shanghai';
GRANT ALL PRIVILEGES ON DATABASE blogdb TO bloguser;
\q
```

## 后端部署（Django）

### 1. 克隆代码

```bash
cd /home/blog
git clone https://github.com/sghenyu8018/PersonalBlobDynamic.git
cd PersonalBlobDynamic/backend
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt

# 生产环境额外安装gunicorn
pip install gunicorn

# 如果遇到psycopg2编译问题，可以安装系统依赖
sudo apt install -y libpq-dev python3-dev
pip install psycopg2-binary
```

### 4. 配置环境变量

创建 `.env` 文件：

```bash
nano .env
```

添加以下内容：

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,localhost
DATABASE_URL=postgresql://bloguser:your_secure_password@localhost:5432/blogdb
```

生成SECRET_KEY：

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. 配置Django环境变量

你需要把 `.env` 文件中的内容接入到 Django 配置里，方法如下：

1. 打开/编辑 `config/settings.py` 文件。

2. 找到原本写死 SECRET_KEY、DEBUG、ALLOWED_HOSTS 和数据库信息的地方，把它们用下面的方式替换：

```python
# 引入 decouple 库以读取 .env
from decouple import config
import os

SECRET_KEY = config('SECRET_KEY')  # 从.env获取
DEBUG = config('DEBUG', default=False, cast=bool)  # True/False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# 数据库配置（.env中写明数据库参数，settings里这样读取）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='blogdb'),
        'USER': config('DB_USER', default='bloguser'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# 静态文件（确保有 BASE_DIR 变量定义，一般Django默认有几行）
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 媒体文件
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

- `.env` 文件的内容格式可以参考上文部署说明。
- 修改后，Django 会自动用你 `.env` 文件里的设置。

如果你不会新增字段，直接复制上述代码覆盖你原有的设置部分即可。

### 6. 运行数据库迁移

**重要：必须先运行迁移，然后再创建超级用户！**

```bash
# 首先运行数据库迁移，创建所有表
python manage.py migrate

# 迁移完成后，创建超级用户
python manage.py createsuperuser

# 收集静态文件
python manage.py collectstatic --noinput
```

**注意**：
- 如果看到 "You have X unapplied migration(s)" 的提示，必须先运行 `python manage.py migrate`
- 迁移会创建所有必需的数据库表，包括 auth_user 表
- 只有迁移完成后才能创建超级用户

### 7. 配置Gunicorn

创建 `gunicorn_config.py`：

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
```

### 8. 使用Systemd管理服务

创建systemd服务文件：

```bash
sudo nano /etc/systemd/system/blog-backend.service
```

添加以下内容：

```ini
[Unit]
Description=Blog Backend Gunicorn daemon
After=network.target

[Service]
User=blog
Group=www-data
WorkingDirectory=/home/blog/PersonalBlobDynamic/backend
Environment="PATH=/home/blog/PersonalBlobDynamic/backend/venv/bin"
ExecStart=/home/blog/PersonalBlobDynamic/backend/venv/bin/gunicorn \
    --config /home/blog/PersonalBlobDynamic/backend/gunicorn_config.py \
    config.wsgi:application

Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start blog-backend
sudo systemctl enable blog-backend
sudo systemctl status blog-backend
```

## 前端部署（Next.js）

### 1. 进入前端目录

```bash
cd /home/blog/PersonalBlobDynamic/frontend
```

### 2. 安装依赖

```bash
npm install
```

### 3. 配置环境变量

创建 `.env.production` 文件：

```env
NEXT_PUBLIC_API_URL=https://your-domain.com/api
```

### 4. 构建生产版本

```bash
npm run build
```

### 5. 使用PM2管理进程

安装PM2：

```bash
sudo npm install -g pm2
```

创建PM2配置文件 `ecosystem.config.js`：

```javascript
module.exports = {
  apps: [{
    name: 'blog-frontend',
    script: 'node_modules/next/dist/bin/next',
    args: 'start',
    cwd: '/home/blog/PersonalBlobDynamic/frontend',
    instances: 1,
    exec_mode: 'fork',
    env: {
      NODE_ENV: 'production',
      PORT: 3000
    }
  }]
};
```

启动服务：

```bash
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## Nginx配置

### 1. 创建Nginx配置文件

```bash
sudo nano /etc/nginx/sites-available/blog
```

添加以下配置：

```nginx
upstream django {
    server 127.0.0.1:8000;
}

upstream nextjs {
    server 127.0.0.1:3000;
}

# HTTP重定向到HTTPS
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS服务器
server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;

    # SSL证书配置（使用Let's Encrypt）
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 日志
    access_log /var/log/nginx/blog_access.log;
    error_log /var/log/nginx/blog_error.log;

    # 客户端最大上传大小
    client_max_body_size 100M;

    # 静态文件
    location /static/ {
        alias /home/blog/PersonalBlobDynamic/backend/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # 媒体文件
    location /media/ {
        alias /home/blog/PersonalBlobDynamic/backend/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    # Django API
    location /api/ {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        
        # WebSocket支持（如果需要）
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Next.js前端
    location / {
        proxy_pass http://nextjs;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
}

# Gzip压缩
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json application/javascript;
```

### 2. 启用站点

```bash
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 域名和SSL配置

### 1. 配置DNS

在域名管理面板添加A记录：
- 主机记录: @ 和 www
- 记录值: 服务器IP地址
- TTL: 600

### 2. 安装SSL证书（Let's Encrypt）

```bash
# 安装Certbot
sudo apt install -y certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期测试
sudo certbot renew --dry-run
```

证书会自动配置到Nginx。

## 数据库配置

### PostgreSQL优化

编辑 `/etc/postgresql/12/main/postgresql.conf`：

```conf
# 内存配置（根据服务器内存调整）
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
work_mem = 16MB

# 连接配置
max_connections = 100

# 日志配置
logging_collector = on
log_directory = 'log'
log_filename = 'postgresql-%Y-%m-%d.log'
log_min_duration_statement = 1000
```

重启PostgreSQL：

```bash
sudo systemctl restart postgresql
```

### 数据库备份

创建备份脚本 `/home/blog/backup_db.sh`：

```bash
#!/bin/bash
BACKUP_DIR="/home/blog/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

pg_dump -U bloguser -h localhost blogdb | gzip > $BACKUP_DIR/blogdb_$DATE.sql.gz

# 保留最近30天的备份
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

设置定时任务：

```bash
chmod +x /home/blog/backup_db.sh
crontab -e
```

添加：

```
0 2 * * * /home/blog/backup_db.sh
```

## 监控和维护

### 1. 日志查看

```bash
# Django日志
sudo journalctl -u blog-backend -f

# Nginx日志
sudo tail -f /var/log/nginx/blog_error.log
sudo tail -f /var/log/nginx/blog_access.log

# PM2日志
pm2 logs blog-frontend
```

### 2. 性能监控

安装监控工具：

```bash
# 系统监控
sudo apt install -y htop iotop

# PM2监控
pm2 monit
```

### 3. 定期维护

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 清理日志
sudo journalctl --vacuum-time=30d

# 更新依赖
cd /home/blog/PersonalBlobDynamic/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt

cd /home/blog/PersonalBlobDynamic/frontend
npm update
```

### 4. 代码更新

```bash
cd /home/blog/PersonalBlobDynamic
git pull origin main

# 后端更新
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart blog-backend

# 前端更新
cd ../frontend
npm install
npm run build
pm2 restart blog-frontend
```

## 常见问题

### 1. 502 Bad Gateway

**原因**: Django或Next.js服务未运行

**解决方法**:
```bash
# 检查Django服务
sudo systemctl status blog-backend

# 检查Next.js服务
pm2 status

# 查看错误日志
sudo journalctl -u blog-backend -n 50
pm2 logs blog-frontend
```

### 2. 静态文件404

**原因**: 静态文件未正确收集或Nginx配置错误

**解决方法**:
```bash
# 重新收集静态文件
cd /home/blog/PersonalBlobDynamic/backend
source venv/bin/activate
python manage.py collectstatic --noinput

# 检查文件权限
sudo chown -R blog:www-data /home/blog/PersonalBlobDynamic/backend/staticfiles
sudo chmod -R 755 /home/blog/PersonalBlobDynamic/backend/staticfiles
```

### 3. 数据库连接错误

**原因**: 数据库配置错误或PostgreSQL未运行

**解决方法**:
```bash
# 检查PostgreSQL状态
sudo systemctl status postgresql

# 测试数据库连接
psql -U bloguser -h localhost -d blogdb

# 检查.env文件中的数据库配置
cat /home/blog/PersonalBlobDynamic/backend/.env
```

### 4. 内存不足

**原因**: 服务器内存不足

**解决方法**:
- 增加服务器内存
- 减少Gunicorn worker数量
- 使用数据库连接池
- 启用Nginx缓存

### 5. SSL证书过期

**原因**: Let's Encrypt证书需要每90天续期

**解决方法**:
```bash
# 手动续期
sudo certbot renew

# 检查自动续期是否配置
sudo systemctl status certbot.timer
```

## 安全建议

1. **防火墙配置**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **定期更新系统**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

3. **使用强密码**
   - 数据库密码
   - Django SECRET_KEY
   - 系统用户密码

4. **限制SSH访问**
   - 禁用root登录
   - 使用密钥认证
   - 更改SSH端口

5. **定期备份**
   - 数据库备份
   - 代码备份
   - 媒体文件备份

## 性能优化

1. **启用Nginx缓存**
2. **使用CDN加速静态资源**
3. **数据库查询优化**
4. **使用Redis缓存**
5. **图片压缩和CDN**

## 联系和支持

如有部署问题，请：
1. 查看日志文件
2. 检查服务状态
3. 查看GitHub Issues
4. 提交新的Issue

---

**最后更新**: 2026-01-14
