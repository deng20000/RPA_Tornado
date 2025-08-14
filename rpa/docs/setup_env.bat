@echo off
chcp 65001 >nul
echo ================================================
echo RPA项目环境设置 - Windows版本
echo ================================================
echo.

echo 🔄 检查uv是否已安装...
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 uv未安装，正在安装...
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    if %errorlevel% neq 0 (
        echo ❌ uv安装失败，请手动安装
        pause
        exit /b 1
    )
    echo ✅ uv安装完成
) else (
    echo ✅ uv已安装
)

echo.
echo 🔄 创建必要目录...
if not exist "data" mkdir data
if not exist "output" mkdir output
if not exist "logs" mkdir logs
if not exist "temp" mkdir temp
if not exist "tests" mkdir tests
echo ✅ 目录创建完成

echo.
echo 🔄 同步项目依赖...
uv sync
if %errorlevel% neq 0 (
    echo ❌ 依赖同步失败
    pause
    exit /b 1
)

echo.
echo 🔄 更新锁文件...
uv lock
if %errorlevel% neq 0 (
    echo ❌ 锁文件更新失败
    pause
    exit /b 1
)

echo.
echo 🎉 环境设置完成！
echo.
echo 📋 可用的命令:
echo   uv run python process_returns.py  - 运行退货处理
echo   uv run python process_excel.py    - 运行Excel处理
echo   uv run python BpdData.py          - 运行BPD数据处理
echo   uv run python newfile.py          - 运行新文件处理
echo.
echo 🔧 开发命令:
echo   make install-dev  - 安装开发依赖
echo   make test         - 运行测试
echo   make lint         - 代码检查
echo   make format       - 代码格式化
echo   make check        - 类型检查
echo.
pause 