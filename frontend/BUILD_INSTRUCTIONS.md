# 构建说明

如果遇到路径别名问题，请按照以下步骤操作：

## 1. 更新代码

```bash
cd /home/blog/PersonalBlobDynamic
git pull origin main
cd frontend
```

## 2. 清理缓存

```bash
# 删除构建缓存
rm -rf .next
rm -rf node_modules/.cache

# 如果问题仍然存在，可以清理并重新安装依赖
rm -rf node_modules package-lock.json
npm install
```

## 3. 验证配置文件

检查 `next.config.js` 应该包含：

```javascript
webpack: (config) => {
  config.resolve.alias = {
    ...config.resolve.alias,
    '@': path.resolve(__dirname),
  }
  return config
}
```

检查 `tsconfig.json` 应该包含：

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

## 4. 重新构建

```bash
npm run build
```

## 5. 如果仍然失败

检查文件是否存在：
```bash
ls -la lib/blog.ts
ls -la lib/types.ts
ls -la lib/api.ts
```

如果文件存在但构建仍然失败，可能需要重启开发服务器或重新安装依赖。
