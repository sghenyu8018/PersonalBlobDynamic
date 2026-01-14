# 前端测试脚本
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "前端环境测试" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

$frontendPath = ".\frontend"

# 检查目录是否存在
if (-not (Test-Path $frontendPath)) {
    Write-Host "❌ frontend目录不存在" -ForegroundColor Red
    exit 1
}

Write-Host "✅ frontend目录存在" -ForegroundColor Green

# 检查package.json
$packageJson = Join-Path $frontendPath "package.json"
if (Test-Path $packageJson) {
    Write-Host "✅ package.json存在" -ForegroundColor Green
    $package = Get-Content $packageJson | ConvertFrom-Json
    Write-Host "   项目名称: $($package.name)" -ForegroundColor Yellow
    Write-Host "   版本: $($package.version)" -ForegroundColor Yellow
} else {
    Write-Host "❌ package.json不存在" -ForegroundColor Red
    exit 1
}

# 检查node_modules
$nodeModules = Join-Path $frontendPath "node_modules"
if (Test-Path $nodeModules) {
    Write-Host "✅ node_modules存在" -ForegroundColor Green
} else {
    Write-Host "⚠️  node_modules不存在，需要运行 npm install" -ForegroundColor Yellow
}

# 检查关键文件
$keyFiles = @(
    "app\layout.tsx",
    "app\page.tsx",
    "lib\api.ts",
    "lib\blog.ts",
    "lib\types.ts",
    "next.config.ts",
    "tsconfig.json",
    "tailwind.config.ts"
)

Write-Host "`n检查关键文件:" -ForegroundColor Cyan
foreach ($file in $keyFiles) {
    $filePath = Join-Path $frontendPath $file
    if (Test-Path $filePath) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file 不存在" -ForegroundColor Red
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "测试完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
