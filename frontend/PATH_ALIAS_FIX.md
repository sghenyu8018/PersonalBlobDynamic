# 路径别名问题修复指南

如果仍然遇到 `Module not found: Can't resolve '@/lib/blog'` 错误，请尝试以下步骤：

## 方法1：清理构建缓存并重新构建

```bash
# 删除构建缓存
rm -rf .next
rm -rf node_modules/.cache

# 重新构建
npm run build
```

## 方法2：检查配置文件

确保以下文件配置正确：

### 1. next.config.js
确保包含webpack配置：
```javascript
webpack: (config, { isServer }) => {
  if (!isServer) {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname),
    }
  }
  return config
}
```

### 2. tsconfig.json
确保包含：
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

### 3. jsconfig.json（如果使用JavaScript）
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

## 方法3：使用相对路径（临时解决方案）

如果路径别名仍然不工作，可以临时使用相对路径：

将 `@/lib/blog` 改为 `../lib/blog` 或 `../../lib/blog`（根据文件位置）

## 方法4：验证文件结构

确保文件结构如下：
```
frontend/
├── lib/
│   ├── api.ts
│   ├── blog.ts
│   └── types.ts
├── components/
├── app/
└── next.config.js
```

## 验证配置

运行以下命令验证：
```bash
# 检查文件是否存在
ls -la lib/blog.ts

# 检查Next.js配置
cat next.config.js | grep -A 10 webpack
```
