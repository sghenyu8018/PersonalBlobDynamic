# 个人技术博客系统

基于 Next.js + Django 构建的功能完整的个人技术博客系统。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ 功能特性

- ✅ **后台管理系统** - 完整的文章、评论、用户管理
- ✅ **评论系统** - 支持嵌套回复、审核机制、敏感词过滤
- ✅ **阅读量统计** - IP去重，24小时内同一IP只计算一次
- ✅ **点赞功能** - 防刷机制
- ✅ **付费阅读** - 支持部分文章设置为付费可见
- ✅ **分类和标签** - 灵活的文章分类和标签系统
- ✅ **搜索功能** - 支持关键词搜索
- ✅ **静态页面** - 关于我、友链、项目、简历等独立页面
- ✅ **代码高亮** - 使用 Prism.js 自动识别语言并语法着色
- ✅ **Markdown支持** - 完整的Markdown编辑和渲染
- ✅ **SEO优化** - Meta标签、Open Graph、Twitter Card
- ✅ **响应式设计** - 适配各种设备
- ✅ **深色模式** - 支持深色/浅色主题切换

## 🛠 技术栈

### 后端
- **框架**: Django 4.2+
- **API**: Django REST Framework
- **数据库**: SQLite (开发环境)
- **认证**: Session Authentication

### 前端
- **框架**: Next.js 14+ (App Router)
- **语言**: TypeScript
- **UI**: Tailwind CSS
- **Markdown**: React Markdown
- **代码高亮**: Prism.js

### 部署
- **Web服务器**: Nginx
- **反向代理**: Nginx

## 📦 项目结构

```
PersonalBlobDynamic/
├── frontend/              # Next.js 前端项目
│   ├── app/              # App Router 页面
│   │   ├── about/        # 关于我页面
│   │   ├── admin/        # 后台管理
│   │   ├── posts/        # 文章详情页
│   │   └── ...
│   ├── components/       # React 组件
│   └── lib/             # 工具函数和API客户端
├── backend/              # Django 后端项目
│   ├── blog/            # 博客主应用
│   ├── accounts/        # 用户认证应用
│   ├── api/             # API 应用
│   └── config/          # Django 配置
├── nginx/                # Nginx 配置文件
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Node.js 18+
- npm 或 yarn

### 后端设置

1. **进入后端目录**
   ```bash
   cd backend
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行数据库迁移**
   ```bash
   python manage.py migrate
   ```

4. **创建超级用户**
   ```bash
   python manage.py createsuperuser
   ```

5. **启动开发服务器**
   ```bash
   python manage.py runserver
   ```

   后端服务运行在 `http://localhost:8000`

### 前端设置

1. **进入前端目录**
   ```bash
   cd frontend
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **启动开发服务器**
   ```bash
   npm run dev
   ```

   前端服务运行在 `http://localhost:3000`

## 📝 使用说明

### 后台管理

访问 `http://localhost:8000/admin/` 使用Django Admin后台管理系统。

### API接口

API基础URL: `http://localhost:8000/api/`

主要接口：
- `GET /api/blog/posts/` - 获取文章列表
- `GET /api/blog/posts/{slug}/` - 获取文章详情
- `POST /api/blog/posts/{slug}/view/` - 记录阅读量
- `POST /api/blog/posts/{slug}/like/` - 点赞文章
- `GET /api/blog/comments/` - 获取评论列表
- `POST /api/blog/comments/` - 创建评论
- `GET /api/accounts/current-user/` - 获取当前用户信息

详细API文档请参考代码中的序列化器和视图。

## 🔧 配置说明

### 后端配置

主要配置文件：`backend/config/settings.py`

- `DEBUG`: 调试模式（生产环境请设置为False）
- `ALLOWED_HOSTS`: 允许的主机列表
- `CORS_ALLOWED_ORIGINS`: 允许的CORS源

### 前端配置

主要配置文件：`frontend/next.config.ts`

- API代理配置
- 环境变量配置

## 🚢 部署

### 使用Nginx部署

1. **构建前端**
   ```bash
   cd frontend
   npm run build
   ```

2. **收集静态文件（后端）**
   ```bash
   cd backend
   python manage.py collectstatic
   ```

3. **配置Nginx**
   
   复制 `nginx/nginx.conf` 到服务器，根据实际情况修改路径。

4. **启动服务**
   - Django: 使用 gunicorn 或 uwsgi
   - Next.js: `npm start` 或使用PM2
   - Nginx: 配置反向代理

详细部署说明请参考 `nginx/nginx.conf` 文件。

## 📚 开发文档

### 数据库模型

- **Post**: 文章模型
- **Category**: 分类模型
- **Tag**: 标签模型
- **Comment**: 评论模型（支持嵌套）
- **ViewLog**: 阅读量记录
- **Like**: 点赞记录
- **Payment**: 付费记录
- **StaticPage**: 静态页面模型

### API设计

使用Django REST Framework构建RESTful API，支持：
- 分页
- 搜索
- 过滤
- 排序

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。

## 📮 联系方式

如有问题或建议，请提交Issue。

## 🙏 致谢

感谢所有开源项目的贡献者！

---

**注意**: 这是一个开发版本，生产环境使用前请进行充分测试和安全配置。
