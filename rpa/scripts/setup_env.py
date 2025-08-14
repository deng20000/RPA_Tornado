#!/usr/bin/env python3
"""
RPA项目环境设置脚本
用于初始化uv环境和安装依赖
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """运行命令并处理错误"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} 完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} 失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False

def check_uv_installed():
    """检查uv是否已安装"""
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_uv():
    """安装uv"""
    system = platform.system().lower()
    
    if system == "windows":
        # Windows安装
        command = "powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\""
    elif system == "darwin":
        # macOS安装
        command = "curl -LsSf https://astral.sh/uv/install.sh | sh"
    else:
        # Linux安装
        command = "curl -LsSf https://astral.sh/uv/install.sh | sh"
    
    return run_command(command, "安装uv")

def setup_project():
    """设置项目环境"""
    print("🚀 开始设置RPA项目环境...")
    
    # 检查uv是否已安装
    if not check_uv_installed():
        print("📦 uv未安装，正在安装...")
        if not install_uv():
            print("❌ uv安装失败，请手动安装")
            return False
    
    # 创建虚拟环境并安装依赖
    commands = [
        ("uv sync", "同步项目依赖"),
        ("uv lock", "更新锁文件"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def create_directories():
    """创建必要的目录"""
    directories = [
        "data",
        "output", 
        "logs",
        "temp",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 创建目录: {directory}")

def main():
    """主函数"""
    print("=" * 50)
    print("RPA项目环境设置")
    print("=" * 50)
    
    # 创建必要目录
    create_directories()
    
    # 设置项目环境
    if setup_project():
        print("\n🎉 环境设置完成！")
        print("\n📋 可用的命令:")
        print("  uv run python process_returns.py  - 运行退货处理")
        print("  uv run python process_excel.py    - 运行Excel处理")
        print("  uv run python BpdData.py          - 运行BPD数据处理")
        print("  uv run python newfile.py          - 运行新文件处理")
        print("\n🔧 开发命令:")
        print("  make install-dev  - 安装开发依赖")
        print("  make test         - 运行测试")
        print("  make lint         - 代码检查")
        print("  make format       - 代码格式化")
        print("  make check        - 类型检查")
    else:
        print("\n❌ 环境设置失败，请检查错误信息")
        sys.exit(1)

if __name__ == "__main__":
    main() 