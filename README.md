# 个人技术博客系统

基于 Next.js + Django 构建的功能完整的个人技术博客系统。

## 技术栈

- **前端**: Next.js 14+ (React, App Router, TypeScript, Tailwind CSS)
- **后端**: Django 4.2+ (REST Framework)
- **数据库**: SQLite (开发阶段)
- **部署**: Nginx

## 项目结构

```
PersonalBlobDynamic/
├── frontend/          # Next.js 前端项目
├── backend/           # Django 后端项目
│   ├── blog/         # 博客主应用
│   ├── accounts/     # 用户认证应用
│   ├── api/          # API 应用
│   └── config/       # Django 配置
└── nginx/            # Nginx 配置
```

## 功能特性

- ✅ 后台管理系统
- ✅ 评论系统（支持嵌套回复）
- ✅ 阅读量统计
- ✅ 点赞功能
- ✅ 付费阅读
- ✅ 分类和标签
- ✅ 搜索功能
- ✅ 静态页面（关于我、友链、项目、简历）
- ✅ 代码高亮
- ✅ SEO 优化
- ✅ 文章目录（TOC）
- ✅ 打赏功能

## 开发环境设置

### 后端（Django）

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

后端服务运行在 `http://localhost:8000`

### 前端（Next.js）

```bash
cd frontend
npm install
npm run dev
```

前端服务运行在 `http://localhost:3000`

## 部署

使用 Nginx 作为反向代理和静态资源服务器。配置文件位于 `nginx/` 目录。

## 许可证

MIT
