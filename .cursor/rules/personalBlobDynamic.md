# .cursor/rules
# 个人技术博客系统开发规范 - Cursor Rules

rules:
  - name: "架构与部署"
    description: "项目必须采用前后端分离架构，前端为静态站点（如 Next.js / Nuxt / Astro），后端为 RESTful API 或 GraphQL（如 NestJS / Django / FastAPI）。使用 Nginx 作为反向代理和静态资源服务器。"
    applies_to: ["*.ts", "*.js", "*.py", "nginx.conf", "Dockerfile"]

  - name: "后台管理系统"
    description: "必须包含独立的后台管理界面（/admin），支持文章 CRUD、分类/标签管理、评论审核、用户权限控制（至少管理员角色）。"
    applies_to: ["src/admin/**/*", "backend/controllers/admin/**/*"]

  - name: "内容功能"
    description: |
      每篇文章需支持：
        - Markdown 编辑与渲染（含代码高亮，使用 Prism.js 或 Highlight.js）
        - 分类（category）与标签（tag）
        - 草稿状态与定时发布（publish_at 字段）
        - 置顶（pinned）功能
        - 自动生成文章目录（TOC）用于长文导航
    applies_to: ["src/components/Article.vue", "backend/models/post.py", "*.md"]

  - name: "交互功能"
    description: |
      前端必须实现：
        - 点赞（like）功能（防刷机制）
        - 评论系统（支持嵌套回复，需审核或自动过滤敏感词）
        - 阅读量统计（去重 IP 或用户 ID）
        - 打赏入口（展示微信/支付宝二维码、爱发电、Buy Me a Coffee 链接）
    applies_to: ["src/components/InteractionBar.vue", "backend/services/analytics.py"]

  - name: "付费阅读"
    description: "支持部分文章设置为付费可见。未登录或未支付用户仅见摘要。集成 Stripe / 支付宝 / 微信支付（沙箱模式优先），或使用第三方服务（如 LemonSqueezy）。"
    applies_to: ["src/middleware/paywall.ts", "backend/payment/**/*"]

  - name: "静态页面"
    description: "必须包含独立静态页面：/about（关于我）、/friends（友链）、/projects（项目展示）、/resume（简历 PDF 或 HTML）。这些页面应可由 Markdown 或 JSON 配置驱动。"
    applies_to: ["src/pages/about.vue", "content/friends.json", "public/resume.pdf"]

  - name: "搜索与分类"
    description: "全局搜索功能（支持关键词、标签、分类过滤），建议使用 Algolia、Meilisearch 或前端模糊搜索（Fuse.js）。分类页需分页展示。"
    applies_to: ["src/components/SearchBar.vue", "backend/search/indexer.py"]

  - name: "SEO 优化"
    description: |
      所有页面必须自动生成：
        - <title> 和 <meta name='description'>
        - Open Graph (og:) 标签
        - Twitter Card
        - JSON-LD 结构化数据（Article / Person / BlogPosting）
      使用 next-seo、vue-meta 或类似库。
    applies_to: ["src/layouts/Default.vue", "src/utils/seo.ts"]

  - name: "UI/UX 要求"
    description: "界面需简洁美观，响应式设计，深色/浅色主题切换，加载性能优化（Lighthouse > 90）。使用 Tailwind CSS / UnoCSS 或主流 UI 库（如 Naive UI、Element Plus）。"
    applies_to: ["tailwind.config.js", "src/styles/**/*", "*.vue", "*.tsx"]

  - name: "可扩展性"
    description: "代码结构模块化，配置驱动（如 config/blog.json），预留插件接口（如 webhook、通知、AI 摘要）。避免硬编码。"
    applies_to: ["config/**/*", "src/plugins/**/*"]

  - name: "代码高亮"
    description: "所有代码块必须通过 Prism.js 或 Highlight.js 自动识别语言并语法着色。支持行号、复制按钮、主题切换。"
    applies_to: ["src/components/MarkdownRenderer.vue", "prism.theme.css"]

  - name: "安全与性能"
    description: "评论需防 XSS，输入需转义；API 接口限流；静态资源 CDN 加速；Nginx 配置 gzip、缓存、安全头（CSP、X-Frame-Options）。"
    applies_to: ["nginx.conf", "backend/middlewares/security.py"]

  - name: "文档与注释"
    description: "关键函数、API 接口、配置项必须有清晰注释。提供 README.md 说明本地开发、构建、部署流程。"
    applies_to: ["README.md", "*.ts", "*.py"]