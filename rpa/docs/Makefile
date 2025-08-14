.PHONY: help install install-dev sync lock clean test lint format check

# 默认目标
help:
	@echo "RPA项目 - uv环境管理"
	@echo ""
	@echo "可用命令:"
	@echo "  install      - 安装生产依赖"
	@echo "  install-dev  - 安装开发依赖"
	@echo "  sync         - 同步依赖到虚拟环境"
	@echo "  lock         - 更新锁文件"
	@echo "  clean        - 清理缓存和临时文件"
	@echo "  test         - 运行测试"
	@echo "  lint         - 代码检查"
	@echo "  format       - 代码格式化"
	@echo "  check        - 类型检查"

# 安装生产依赖
install:
	uv sync --no-dev

# 安装开发依赖
install-dev:
	uv sync

# 同步依赖到虚拟环境
sync:
	uv sync

# 更新锁文件
lock:
	uv lock

# 清理缓存和临时文件
clean:
	uv cache clean
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

# 运行测试
test:
	uv run pytest

# 代码检查
lint:
	uv run flake8 .

# 代码格式化
format:
	uv run black .

# 类型检查
check:
	uv run mypy .

# 运行RPA脚本
run-returns:
	uv run python process_returns.py

run-excel:
	uv run python process_excel.py

run-bpd:
	uv run python BpdData.py

run-newfile:
	uv run python newfile.py

# 项目状态检查
status:
	uv run python check_project_status.py

# 配置验证
config:
	uv run python config.py

# 快速启动
quick-start:
	uv run python quick_start.py

# 列出可用脚本
list-scripts:
	uv run python quick_start.py --list 