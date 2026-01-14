# .cursor/rules
# 个人技术博客系统开发规范 - Cursor Rules（核心功能）

rules:
  - name: "后台管理系统"
    description: |
      必须包含独立的后台管理界面，具体要求：
        - 管理界面路由：/admin 或 /dashboard，需要身份验证和权限验证
        - 文章管理：支持文章的创建、编辑、删除、发布/下架操作（CRUD）
        - 分类/标签管理：支持分类和标签的增删改查
        - 评论管理：支持评论的查看、审核、删除、回复操作
        - 用户管理：支持用户列表查看、角色管理、权限分配（至少区分管理员和普通用户）
        - 系统配置：支持站点基本信息配置、SEO 设置等
        - 数据统计：仪表板展示文章数量、评论数量、阅读量统计等关键指标
        - 权限控制：使用基于角色的访问控制（RBAC），管理员可访问所有功能，普通用户仅可访问自己的内容
    applies_to: ["src/admin/**/*", "src/pages/admin/**/*", "backend/controllers/admin/**/*", "backend/routes/admin/**/*", "backend/middleware/auth.ts"]

  - name: "评论功能"
    description: |
      必须实现完整的评论系统，具体要求：
        - 评论数据模型：包含评论 ID、文章 ID、用户信息、评论内容、父评论 ID（支持嵌套）、创建时间、审核状态等字段
        - 评论提交：前端提供评论表单，支持用户输入评论内容，提交到后端 API
        - 评论展示：在文章详情页展示评论列表，支持按时间排序或按热度排序
        - 嵌套回复：支持多级评论回复，前端需清晰展示回复层级关系（如缩进或树形结构）
        - 评论审核：支持评论审核机制，可设置为自动通过或需要管理员审核，审核通过后才显示
        - 敏感词过滤：自动检测并过滤敏感词，可选择替换为 * 号或直接拒绝提交
        - 防刷机制：限制同一 IP 或用户在短时间内提交评论的频率，防止恶意刷评
        - 安全性：评论内容必须进行 XSS 防护，对用户输入进行转义处理，防止脚本注入
        - 评论通知：可选功能，支持评论被回复时发送通知（邮件或站内消息）
    applies_to: ["src/components/Comment/**/*", "src/components/CommentForm.vue", "backend/models/comment.py", "backend/controllers/comment/**/*", "backend/services/comment_service.py"]

  - name: "阅读量统计"
    description: |
      必须实现准确的阅读量统计和展示功能，具体要求：
        - 统计逻辑：采用 IP 去重或用户 ID 去重机制，同一 IP/用户在一定时间间隔内（如 24 小时）只计算一次阅读量
        - 数据存储：阅读量数据存储在数据库中，每篇文章关联一个阅读量字段，同时可记录详细的阅读日志用于数据分析
        - 实时更新：用户访问文章时，后端 API 检查是否已记录该次访问，如未记录则更新阅读量并记录访问日志
        - 展示位置：在文章详情页的标题下方或文章底部清晰展示阅读量，格式如 "阅读量: 1234" 或 "👁️ 1234 views"
        - 列表页展示：在文章列表页（首页、分类页）也展示每篇文章的阅读量，帮助用户了解文章热度
        - 统计准确性：考虑使用 Redis 等缓存技术记录短期访问记录，避免频繁查询数据库，同时确保统计的准确性
        - 性能优化：阅读量更新操作应异步处理，避免影响文章加载速度，可使用消息队列或后台任务
        - 数据可视化：在后台管理系统的仪表板中展示阅读量趋势图、热门文章排行等数据可视化内容
    applies_to: ["src/components/ArticleView.vue", "src/components/ArticleList.vue", "backend/models/post.py", "backend/services/analytics.py", "backend/controllers/analytics/**/*", "backend/middleware/view_counter.ts"]
