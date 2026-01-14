# PostgreSQL 适配器安装指南

如果在使用PostgreSQL数据库时遇到 `ModuleNotFoundError: No module named 'psycopg2'` 错误，请按照以下步骤解决。

## 方法一：使用psycopg2-binary（推荐）

这是最简单的方法，适用于大多数情况：

```bash
pip install psycopg2-binary
```

## 方法二：从源码编译安装（生产环境推荐）

对于生产环境，推荐从源码编译安装以获得更好的性能：

### Ubuntu/Debian

```bash
# 安装系统依赖
sudo apt update
sudo apt install -y libpq-dev python3-dev build-essential

# 安装psycopg2
pip install psycopg2
```

### CentOS/RHEL

```bash
# 安装系统依赖
sudo yum install -y postgresql-devel python3-devel gcc

# 安装psycopg2
pip install psycopg2
```

## 方法三：使用psycopg3（新版本）

Django 4.2+ 支持psycopg3：

```bash
pip install psycopg[binary]
```

注意：使用psycopg3时，需要在settings.py中确保数据库配置正确。

## 验证安装

安装完成后，可以验证是否安装成功：

```bash
python -c "import psycopg2; print('psycopg2版本:', psycopg2.__version__)"
```

或

```bash
python -c "import psycopg; print('psycopg3安装成功')"
```

## 常见问题

### 1. 编译错误

如果遇到编译错误，确保已安装所有系统依赖：

```bash
sudo apt install -y libpq-dev python3-dev build-essential
```

### 2. 权限问题

如果遇到权限问题，使用虚拟环境：

```bash
source venv/bin/activate
pip install psycopg2-binary
```

### 3. 版本不兼容

如果Django版本过旧，可能需要安装特定版本的psycopg2：

```bash
pip install psycopg2-binary==2.9.3
```

## 重新安装依赖

更新requirements.txt后，重新安装所有依赖：

```bash
pip install -r requirements.txt --upgrade
```
