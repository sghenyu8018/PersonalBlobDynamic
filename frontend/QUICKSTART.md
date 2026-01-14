# 前端快速启动指南

## 启动开发服务器

在 `frontend` 目录下运行：

```bash
npm run dev
```

开发服务器将启动在 **http://localhost:3000**

## 重要提示

### 1. 确保后端服务运行

前端需要连接到Django后端API。在启动前端之前，确保后端服务正在运行：

```bash
# 在另一个终端窗口
cd backend
python manage.py runserver
```

后端默认运行在：**http://localhost:8000**

### 2. API代理配置

前端通过Next.js的rewrites功能代理API请求到后端：

- 前端请求：`/api/*`
- 实际转发到：`http://localhost:8000/api/*`

配置文件：`next.config.js`

### 3. 首次启动

如果是首次启动，需要先安装依赖：

```bash
cd frontend
npm install
npm run dev
```

## 常见命令

```bash
# 开发模式
npm run dev

# 生产构建
npm run build

# 启动生产服务器
npm start

# 代码检查
npm run lint
```

## 访问地址

- **前端**: http://localhost:3000
- **后端API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

## 故障排查

如果遇到问题：

1. **端口被占用**：检查3000端口是否被其他程序占用
2. **依赖问题**：删除 `node_modules` 和 `package-lock.json`，重新运行 `npm install`
3. **API连接失败**：确保后端服务正在运行
