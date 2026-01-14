# Changelog

本文档记录了项目的所有重要变更。

## [1.0.0] - 2026-01-14

### 新增功能

#### 后端（Django）
- ✅ 完整的Django项目结构（使用Django REST Framework）
- ✅ 用户认证系统（注册、登录、登出、权限检查）
- ✅ 数据库模型：
  - 文章（Post）：支持Markdown、分类、标签、草稿/发布、置顶、付费等功能
  - 分类（Category）和标签（Tag）
  - 评论（Comment）：支持嵌套回复
  - 阅读量记录（ViewLog）：IP去重统计
  - 点赞记录（Like）
  - 付费记录（Payment）
  - 静态页面（StaticPage）
- ✅ RESTful API接口：
  - 文章CRUD API
  - 分类和标签API
  - 评论API（支持嵌套回复）
  - 阅读量统计API
  - 点赞API
- ✅ Django Admin后台管理
- ✅ 评论安全功能（敏感词过滤、XSS防护）
- ✅ 权限控制（付费阅读权限类）
- ✅ CORS配置（支持前后端分离）

#### 前端（Next.js）
- ✅ Next.js 14项目（App Router、TypeScript、Tailwind CSS）
- ✅ 页面：
  - 首页（文章列表）
  - 文章详情页（支持Markdown渲染和代码高亮）
  - 后台管理页面
  - 静态页面（关于我、友链、项目、简历）
- ✅ React组件：
  - PostList（文章列表组件）
  - PostContent（文章内容组件，集成Prism.js代码高亮）
  - CommentSection（评论区域组件）
  - CommentList（评论列表组件，支持嵌套显示）
  - CommentForm（评论表单组件）
- ✅ API客户端封装
- ✅ TypeScript类型定义
- ✅ SEO优化（Metadata配置）

#### 部署配置
- ✅ Nginx配置文件（反向代理、静态资源、Gzip压缩、安全头）
- ✅ 项目文档（README.md）

### 技术栈

- **后端**: Django 4.2+, Django REST Framework, SQLite
- **前端**: Next.js 14+, React 18+, TypeScript, Tailwind CSS
- **代码高亮**: Prism.js
- **Markdown渲染**: React Markdown
- **部署**: Nginx

### 功能特性

1. **文章管理**
   - Markdown编辑和渲染
   - 分类和标签系统
   - 草稿/发布状态
   - 定时发布
   - 置顶功能
   - 付费文章支持

2. **交互功能**
   - 评论系统（支持嵌套回复）
   - 点赞功能
   - 阅读量统计（IP去重）
   - 评论审核机制

3. **安全特性**
   - 评论敏感词过滤
   - XSS防护
   - 权限控制（RBAC）

4. **SEO优化**
   - Meta标签
   - Open Graph标签
   - Twitter Card

### 已知问题

- 评论功能需要文章ID，已修复
- 部分前端功能需要连接后端API进行完整测试

### 后续计划

- [ ] 完善后台管理系统功能
- [ ] 实现支付集成（微信/支付宝）
- [ ] 添加全文搜索功能
- [ ] 实现文章目录（TOC）自动生成
- [ ] 添加打赏功能页面
- [ ] 性能优化和缓存策略
- [ ] 添加单元测试和集成测试

---

## 版本说明

版本格式遵循 [语义化版本](https://semver.org/lang/zh-CN/)：
- MAJOR：不兼容的API修改
- MINOR：向下兼容的功能性新增
- PATCH：向下兼容的问题修正
