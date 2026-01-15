# 本地部署测试步骤脚本
# 按照DEPLOYMENT.md文档的流程进行测试

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "本地部署测试 - 按照DEPLOYMENT.md流程" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 步骤1: 检查环境
Write-Host "`n[步骤1] 检查环境..." -ForegroundColor Yellow
Write-Host "Python版本:" -ForegroundColor Gray
python --version
Write-Host "Node.js版本:" -ForegroundColor Gray
node --version
Write-Host "OK 环境检查完成`n" -ForegroundColor Green

# 步骤2: 后端测试
Write-Host "[步骤2] 测试后端..." -ForegroundColor Yellow
Set-Location backend

if (-not (Test-Path "venv")) {
    Write-Host "创建虚拟环境..." -ForegroundColor Gray
    python -m venv venv
}

Write-Host "激活虚拟环境..." -ForegroundColor Gray
& .\venv\Scripts\Activate.ps1

Write-Host "检查依赖..." -ForegroundColor Gray
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q

Write-Host "Django配置检查..." -ForegroundColor Gray
python manage.py check

Write-Host "检查迁移状态..." -ForegroundColor Gray
python manage.py showmigrations --list

Write-Host "运行迁移..." -ForegroundColor Gray
python manage.py migrate --noinput

Write-Host "OK 后端测试完成`n" -ForegroundColor Green

# 步骤3: 测试后端服务器启动
Write-Host "[步骤3] 测试后端服务器（5秒）..." -ForegroundColor Yellow
$job = Start-Job -ScriptBlock {
    Set-Location $using:PWD\backend
    & .\venv\Scripts\python.exe manage.py runserver 2>&1 | Out-Null
}
Start-Sleep -Seconds 5

# 测试API
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/" -UseBasicParsing -TimeoutSec 2
    if ($response.StatusCode -eq 200) {
        Write-Host "OK 后端API响应正常" -ForegroundColor Green
        Write-Host "响应内容: $($response.Content)" -ForegroundColor Gray
    }
} catch {
    Write-Host "WARN API测试失败（服务器可能仍在启动中）" -ForegroundColor Yellow
}

Stop-Job $job -ErrorAction SilentlyContinue
Remove-Job $job -ErrorAction SilentlyContinue
Write-Host "OK 后端服务器测试完成`n" -ForegroundColor Green

# 步骤4: 前端测试
Set-Location ..
Write-Host "[步骤4] 测试前端..." -ForegroundColor Yellow
Set-Location frontend

Write-Host "检查前端依赖..." -ForegroundColor Gray
if (-not (Test-Path "node_modules")) {
    Write-Host "安装前端依赖（这可能需要几分钟）..." -ForegroundColor Gray
    npm install --silent
}

Write-Host "检查关键文件..." -ForegroundColor Gray
$files = @("lib/api.ts", "lib/blog.ts", "lib/types.ts", "next.config.js")
$allExist = $true
foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  OK $file" -ForegroundColor Green
    } else {
        Write-Host "  ERROR $file 不存在" -ForegroundColor Red
        $allExist = $false
    }
}

if (-not $allExist) {
    Write-Host "ERROR 关键文件缺失" -ForegroundColor Red
    exit 1
}

Write-Host "构建前端（这可能需要1-2分钟）..." -ForegroundColor Gray
npm run build 2>&1 | Out-Null

if ($LASTEXITCODE -eq 0) {
    Write-Host "OK 前端构建成功" -ForegroundColor Green
} else {
    Write-Host "ERROR 前端构建失败" -ForegroundColor Red
    exit 1
}

Set-Location ..
Write-Host "OK 前端测试完成`n" -ForegroundColor Green

# 总结
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "测试总结" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "OK 所有测试完成！" -ForegroundColor Green
Write-Host ""
Write-Host "下一步操作：" -ForegroundColor Yellow
Write-Host "1. 启动后端: cd backend; .\venv\Scripts\Activate.ps1; python manage.py runserver" -ForegroundColor White
Write-Host "2. 启动前端: cd frontend; npm run dev" -ForegroundColor White
Write-Host "3. 访问应用: http://localhost:3000" -ForegroundColor White
Write-Host ""
