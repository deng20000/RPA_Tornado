# 多阶段构建的Dockerfile
# 用于构建RPA Tornado应用的Docker镜像

# 构建阶段
FROM python:3.11-slim as builder

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 创建虚拟环境并安装Python依赖
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 生产阶段
FROM python:3.11-slim as production

# 设置环境变量
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH"

# 创建非root用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 设置工作目录
WORKDIR /app

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p /app/logs /app/data && \
    chown -R appuser:appuser /app

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 8888 9090

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8888/health || exit 1

# 启动命令
CMD ["python", "main.py"]

# 开发阶段（用于开发环境）
FROM production as development

# 切换回root用户安装开发依赖
USER root

# 安装开发依赖
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    pytest-asyncio \
    black \
    flake8 \
    mypy \
    pre-commit

# 切换回非root用户
USER appuser

# 开发环境启动命令（支持热重载）
CMD ["python", "main.py", "--reload"]