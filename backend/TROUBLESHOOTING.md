# 故障排查指南

本文档列出了部署和运行过程中可能遇到的常见问题及解决方案。

## 数据库相关问题

### 1. relation "auth_user" does not exist

**错误信息**：
```
django.db.utils.ProgrammingError: relation "auth_user" does not exist
```

**原因**：数据库迁移未执行，数据库表还没有创建。

**解决方案**：
```bash
# 运行数据库迁移
python manage.py migrate

# 然后再创建超级用户
python manage.py createsuperuser
```

### 2. You have X unapplied migration(s)

**错误信息**：
```
You have 20 unapplied migration(s). Your project may not work properly until you apply the migrations...
```

**原因**：数据库迁移文件存在，但还没有应用到数据库。

**解决方案**：
```bash
# 查看未应用的迁移
python manage.py showmigrations

# 应用所有迁移
python manage.py migrate

# 如果迁移成功，应该看到 "OK" 标记
```

### 3. ModuleNotFoundError: No module named 'psycopg2'

**错误信息**：
```
ModuleNotFoundError: No module named 'psycopg2'
```

**原因**：PostgreSQL适配器未安装。

**解决方案**：
```bash
# 安装PostgreSQL适配器
pip install psycopg2-binary

# 或重新安装所有依赖
pip install -r requirements.txt
```

详细说明请参考 [INSTALL_POSTGRESQL.md](INSTALL_POSTGRESQL.md)

### 4. 数据库连接错误

**错误信息**：
```
django.db.utils.OperationalError: FATAL: password authentication failed for user
```

**原因**：数据库用户名或密码错误，或数据库不存在。

**解决方案**：

1. 检查 `.env` 文件中的数据库配置：
```bash
cat .env | grep DB_
```

2. 确认数据库和用户已创建：
```bash
sudo -u postgres psql -c "\l"  # 列出所有数据库
sudo -u postgres psql -c "\du"  # 列出所有用户
```

3. 测试数据库连接：
```bash
psql -U bloguser -h localhost -d blogdb
```

## Django相关问题

### 5. Invalid HTTP_HOST header

**错误信息**：
```
Invalid HTTP_HOST header: 'xxx'. You may need to add 'xxx' to ALLOWED_HOSTS.
```

**原因**：Django的ALLOWED_HOSTS设置不包含当前访问的域名或IP。

**解决方案**：

编辑 `config/settings.py` 或 `.env` 文件：
```python
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com', 'your-server-ip']
```

或在 `.env` 文件中：
```env
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip
```

### 6. 静态文件404错误

**错误信息**：访问 `/static/` 路径返回404。

**原因**：静态文件未收集或Nginx配置错误。

**解决方案**：

```bash
# 收集静态文件
python manage.py collectstatic --noinput

# 检查静态文件是否存在
ls -la staticfiles/

# 检查Nginx配置中的静态文件路径是否正确
```

### 7. CSRF verification failed

**错误信息**：
```
CSRF verification failed. Request aborted.
```

**原因**：CSRF令牌验证失败，通常是因为CORS或域名配置问题。

**解决方案**：

1. 检查CORS设置（开发环境）：
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://your-domain.com",
]
```

2. 确保前端请求包含正确的CSRF令牌。

## 部署相关问题

### 8. Gunicorn服务无法启动

**错误信息**：
```
Failed to start blog-backend.service
```

**解决方案**：

1. 检查服务状态：
```bash
sudo systemctl status blog-backend
```

2. 查看详细错误日志：
```bash
sudo journalctl -u blog-backend -n 50
```

3. 检查gunicorn配置文件路径和权限：
```bash
ls -la gunicorn_config.py
```

4. 手动测试gunicorn：
```bash
cd /home/blog/PersonalBlobDynamic/backend
source venv/bin/activate
gunicorn --config gunicorn_config.py config.wsgi:application
```

### 9. Nginx 502 Bad Gateway

**错误信息**：Nginx返回502错误。

**原因**：后端服务未运行或无法连接。

**解决方案**：

1. 检查后端服务是否运行：
```bash
sudo systemctl status blog-backend
ps aux | grep gunicorn
```

2. 检查端口是否被占用：
```bash
netstat -tlnp | grep 8000
```

3. 检查Nginx错误日志：
```bash
sudo tail -f /var/log/nginx/blog_error.log
```

4. 测试后端服务：
```bash
curl http://localhost:8000/api/
```

### 10. PM2服务无法启动

**错误信息**：Next.js前端服务无法启动。

**解决方案**：

1. 检查PM2状态：
```bash
pm2 status
pm2 logs blog-frontend
```

2. 检查前端是否已构建：
```bash
ls -la frontend/.next/
```

3. 重新构建和启动：
```bash
cd frontend
npm run build
pm2 restart blog-frontend
```

## 性能问题

### 11. 数据库查询缓慢

**解决方案**：

1. 使用数据库索引
2. 使用 `select_related` 和 `prefetch_related` 优化查询
3. 启用数据库查询缓存
4. 考虑使用Redis缓存热点数据

### 12. 内存不足

**解决方案**：

1. 减少Gunicorn worker数量
2. 优化数据库连接池
3. 使用进程管理器（如PM2）限制内存使用
4. 增加服务器内存或使用swap

## 权限问题

### 13. Permission denied

**错误信息**：
```
Permission denied: '/path/to/file'
```

**解决方案**：

1. 检查文件/目录权限：
```bash
ls -la /path/to/file
```

2. 修改权限：
```bash
sudo chown -R blog:www-data /home/blog/PersonalBlobDynamic
sudo chmod -R 755 /home/blog/PersonalBlobDynamic
```

## 获取帮助

如果以上解决方案都无法解决问题，请：

1. 查看详细的错误日志
2. 检查Django日志文件
3. 查看系统日志：`journalctl -xe`
4. 在GitHub提交Issue，附上错误信息和环境信息

---

**最后更新**: 2026-01-14
