# 本地部署测试 - 快速开始

按照以下步骤在本地测试部署：

## 第一步：启动后端

打开**第一个PowerShell窗口**：

```powershell
cd backend
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

应该看到：
```
Starting development server at http://127.0.0.1:8000/
```

## 第二步：启动前端

打开**第二个PowerShell窗口**：

```powershell
cd frontend
npm run dev
```

应该看到：
```
  ▲ Next.js 14.2.35
  - Local:        http://localhost:3000
```

## 第三步：访问应用

打开浏览器访问：
- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

## 快速测试命令

### 测试后端API

```powershell
# 测试API根路径
Invoke-RestMethod -Uri http://localhost:8000/api/

# 测试文章列表
Invoke-RestMethod -Uri http://localhost:8000/api/blog/posts/

# 测试分类列表
Invoke-RestMethod -Uri http://localhost:8000/api/blog/categories/
```

### 创建测试数据

访问 http://localhost:8000/admin/，登录后创建：
1. 分类（Category）
2. 标签（Tag）
3. 文章（Post）

## 验证清单

- [ ] 后端服务器启动成功
- [ ] 前端服务器启动成功
- [ ] 可以访问首页
- [ ] API端点返回数据
- [ ] Django Admin可访问
- [ ] 可以创建文章
- [ ] 文章列表正常显示

## 故障排查

如果遇到问题，请参考：
- `LOCAL_DEPLOYMENT_TEST.md` - 详细测试指南
- `backend/TROUBLESHOOTING.md` - 故障排查指南
