# 本地部署测试脚本
# 使用方法: .\test_deployment.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "本地部署测试脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 检查Python
Write-Host ""
Write-Host "[1/8] 检查Python环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "OK Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR Python未安装或不在PATH中" -ForegroundColor Red
    exit 1
}

# 检查Node.js
Write-Host ""
Write-Host "[2/8] 检查Node.js环境..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "OK Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR Node.js未安装或不在PATH中" -ForegroundColor Red
    exit 1
}

# 检查后端虚拟环境
Write-Host ""
Write-Host "[3/8] 检查后端虚拟环境..." -ForegroundColor Yellow
if (Test-Path "backend\venv") {
    Write-Host "OK 虚拟环境已存在" -ForegroundColor Green
} else {
    Write-Host "WARN 虚拟环境不存在，需要创建" -ForegroundColor Yellow
    Write-Host "  运行: cd backend; python -m venv venv" -ForegroundColor Gray
}

# 检查后端依赖
Write-Host ""
Write-Host "[4/8] 检查后端依赖..." -ForegroundColor Yellow
if (Test-Path "backend\venv\Scripts\python.exe") {
    try {
        $djangoInstalled = & "backend\venv\Scripts\python.exe" -c "import django; print(django.__version__)" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "OK Django已安装: $djangoInstalled" -ForegroundColor Green
        } else {
            Write-Host "WARN Django未安装，需要运行: pip install -r requirements.txt" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "WARN 无法检查Django安装状态" -ForegroundColor Yellow
    }
} else {
    Write-Host "WARN 虚拟环境未激活" -ForegroundColor Yellow
}

# 检查数据库
Write-Host ""
Write-Host "[5/8] 检查数据库..." -ForegroundColor Yellow
if (Test-Path "backend\db.sqlite3") {
    Write-Host "OK SQLite数据库文件存在" -ForegroundColor Green
} else {
    Write-Host "WARN 数据库文件不存在，需要运行迁移" -ForegroundColor Yellow
    Write-Host "  运行: python manage.py migrate" -ForegroundColor Gray
}

# 检查前端依赖
Write-Host ""
Write-Host "[6/8] 检查前端依赖..." -ForegroundColor Yellow
if (Test-Path "frontend\node_modules") {
    Write-Host "OK 前端依赖已安装" -ForegroundColor Green
} else {
    Write-Host "WARN 前端依赖未安装，需要运行: npm install" -ForegroundColor Yellow
}

# 检查前端构建
Write-Host ""
Write-Host "[7/8] 检查前端构建..." -ForegroundColor Yellow
if (Test-Path "frontend\.next") {
    Write-Host "OK 前端已构建" -ForegroundColor Green
} else {
    Write-Host "WARN 前端未构建，需要运行: npm run build" -ForegroundColor Yellow
}

# 检查关键文件
Write-Host ""
Write-Host "[8/8] 检查关键文件..." -ForegroundColor Yellow
$keyFiles = @(
    "backend\manage.py",
    "backend\config\settings.py",
    "frontend\package.json",
    "frontend\next.config.js",
    "frontend\lib\api.ts",
    "frontend\lib\blog.ts"
)

$allExist = $true
foreach ($file in $keyFiles) {
    if (Test-Path $file) {
        Write-Host "OK $file" -ForegroundColor Green
    } else {
        Write-Host "ERROR $file 不存在" -ForegroundColor Red
        $allExist = $false
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "测试完成" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($allExist) {
    Write-Host ""
    Write-Host "OK 所有关键文件存在" -ForegroundColor Green
    Write-Host ""
    Write-Host "下一步：" -ForegroundColor Yellow
    Write-Host "1. 启动后端: cd backend; .\venv\Scripts\Activate.ps1; python manage.py runserver" -ForegroundColor White
    Write-Host "2. 启动前端: cd frontend; npm run dev" -ForegroundColor White
    Write-Host "3. 访问: http://localhost:3000" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "WARN 部分文件缺失，请检查" -ForegroundColor Yellow
}
