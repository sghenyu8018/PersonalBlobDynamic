# 本地部署测试指南

本文档指导您在本地Windows环境中按照DEPLOYMENT.md的流程进行测试部署。

## 前置条件检查

### 1. 检查Python环境

```powershell
python --version  # 应该是 3.11+
pip --version
```

### 2. 检查Node.js环境

```powershell
node --version  # 应该是 18+
npm --version
```

### 3. 检查磁盘空间

```powershell
Get-PSDrive C | Select-Object Used,Free
```

确保至少有5GB可用空间。

## 后端部署测试

### 步骤1: 创建虚拟环境

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
```

如果遇到执行策略错误，运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 步骤2: 安装依赖

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤3: 配置环境变量（可选）

如果需要使用PostgreSQL，创建 `.env` 文件：

```powershell
# 在backend目录下
@"
SECRET_KEY=django-insecure-test-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=blogdb
DB_USER=bloguser
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
"@ | Out-File -Encoding utf8 .env
```

**注意**：本地测试可以使用SQLite，无需配置PostgreSQL。

### 步骤4: 运行数据库迁移

```powershell
python manage.py migrate
```

### 步骤5: 创建超级用户（可选）

```powershell
python manage.py createsuperuser
```

按提示输入用户名、邮箱和密码。

### 步骤6: 收集静态文件

```powershell
python manage.py collectstatic --noinput
```

### 步骤7: 启动开发服务器

```powershell
python manage.py runserver
```

服务器将在 `http://localhost:8000` 启动。

**测试API**：
- 打开浏览器访问：http://localhost:8000/api/
- 应该看到：`{"message": "个人技术博客 API", "version": "1.0"}`

## 前端部署测试

### 步骤1: 安装依赖

```powershell
cd frontend
npm install
```

### 步骤2: 配置环境变量

创建 `.env.local` 文件：

```powershell
@"
NEXT_PUBLIC_API_URL=http://localhost:8000/api
"@ | Out-File -Encoding utf8 .env.local
```

### 步骤3: 测试构建

```powershell
npm run build
```

构建应该成功完成。如果看到API连接警告，这是正常的（构建时API可能未运行）。

### 步骤4: 启动开发服务器

**在另一个PowerShell窗口中**：

```powershell
cd frontend
npm run dev
```

服务器将在 `http://localhost:3000` 启动。

### 步骤5: 测试前端

1. 打开浏览器访问：http://localhost:3000
2. 应该看到博客首页
3. 如果后端正在运行，应该能看到文章列表（即使为空）

## 完整测试流程

### 1. 启动后端（第一个终端）

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

### 2. 启动前端（第二个终端）

```powershell
cd frontend
npm run dev
```

### 3. 测试功能

#### 测试API端点

```powershell
# 测试API根路径
Invoke-WebRequest -Uri http://localhost:8000/api/ | Select-Object -ExpandProperty Content

# 测试文章列表API
Invoke-WebRequest -Uri http://localhost:8000/api/blog/posts/ | Select-Object -ExpandProperty Content

# 测试分类API
Invoke-WebRequest -Uri http://localhost:8000/api/blog/categories/ | Select-Object -ExpandProperty Content
```

#### 测试Django Admin

1. 访问：http://localhost:8000/admin/
2. 使用创建的超级用户登录
3. 测试创建文章、分类、标签等

#### 测试前端页面

1. **首页**: http://localhost:3000
2. **关于我**: http://localhost:3000/about
3. **友链**: http://localhost:3000/friends
4. **项目**: http://localhost:3000/projects
5. **简历**: http://localhost:3000/resume
6. **后台管理**: http://localhost:3000/admin

## 创建测试数据

### 通过Django Admin

1. 访问 http://localhost:8000/admin/
2. 登录后创建：
   - 分类（Category）
   - 标签（Tag）
   - 文章（Post）

### 通过Django Shell

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py shell
```

```python
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post

# 创建分类
category = Category.objects.create(
    name='技术分享',
    slug='tech',
    description='技术相关文章'
)

# 创建标签
tag1 = Tag.objects.create(name='Python', slug='python')
tag2 = Tag.objects.create(name='Django', slug='django')

# 获取或创建用户
user = User.objects.first()
if not user:
    user = User.objects.create_user('admin', 'admin@example.com', 'password')

# 创建文章
post = Post.objects.create(
    title='测试文章',
    slug='test-post',
    author=user,
    content='# 这是测试文章\n\n这是一篇测试文章的内容。',
    excerpt='这是文章的摘要',
    category=category,
    status='published'
)
post.tags.add(tag1, tag2)

print('测试数据创建成功！')
exit()
```

## 验证功能

### 1. 文章列表

访问 http://localhost:3000，应该能看到刚创建的文章。

### 2. 文章详情

访问 http://localhost:3000/posts/test-post，应该能看到文章详情。

### 3. 评论功能

在文章详情页底部，应该能看到评论表单。

### 4. API测试

使用Postman或curl测试API：

```powershell
# 获取文章列表
Invoke-RestMethod -Uri http://localhost:8000/api/blog/posts/ -Method Get

# 获取文章详情
Invoke-RestMethod -Uri http://localhost:8000/api/blog/posts/test-post/ -Method Get
```

## 常见问题

### 1. 端口被占用

如果8000或3000端口被占用：

**后端**：
```powershell
python manage.py runserver 8001
```

**前端**：
修改 `next.config.js` 中的API地址，或使用环境变量。

### 2. CORS错误

确保 `backend/config/settings.py` 中配置了：

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### 3. 模块找不到

确保：
- 后端虚拟环境已激活
- 前端依赖已安装
- 路径别名配置正确

### 4. 数据库错误

如果使用SQLite，确保 `db.sqlite3` 文件存在且可写。

## 测试检查清单

- [ ] Python虚拟环境创建成功
- [ ] 后端依赖安装完成
- [ ] 数据库迁移成功
- [ ] 后端服务器启动成功（http://localhost:8000）
- [ ] API端点可访问
- [ ] Django Admin可访问
- [ ] 前端依赖安装完成
- [ ] 前端构建成功
- [ ] 前端服务器启动成功（http://localhost:3000）
- [ ] 前端页面可访问
- [ ] API数据能正确显示
- [ ] 可以创建测试数据
- [ ] 文章列表和详情页正常
- [ ] 评论功能正常（如果后端运行）

## 下一步

测试成功后，可以：
1. 创建更多测试数据
2. 测试所有功能模块
3. 准备生产环境部署
4. 配置域名和SSL证书

---

**注意**：本地测试使用SQLite数据库，生产环境建议使用PostgreSQL。
