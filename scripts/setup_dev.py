#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发环境设置脚本
自动配置开发环境，包括依赖安装、环境变量设置等
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 项目根目录
project_root = Path(__file__).parent.parent


def run_command(cmd, cwd=None, check=True):
    """执行命令"""
    print(f"🔧 执行命令: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd or project_root,
            check=check,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        if e.stderr:
            print(f"错误信息: {e.stderr}")
        raise


def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python版本过低: {version.major}.{version.minor}")
        print("请安装Python 3.8或更高版本")
        sys.exit(1)
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")


def check_virtual_env():
    """检查虚拟环境"""
    print("🔍 检查虚拟环境...")
    
    # 检查是否在虚拟环境中
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    
    if in_venv:
        print(f"✅ 当前在虚拟环境中: {sys.prefix}")
        return True
    else:
        print("⚠️  未检测到虚拟环境")
        
        # 检查是否存在.venv目录
        venv_path = project_root.parent / '.venv'
        if venv_path.exists():
            print(f"💡 发现虚拟环境目录: {venv_path}")
            print("请激活虚拟环境后再运行此脚本:")
            print(f"   Windows: {venv_path}\\Scripts\\activate")
            print(f"   Linux/Mac: source {venv_path}/bin/activate")
        else:
            print("💡 建议创建虚拟环境:")
            print(f"   python -m venv {venv_path}")
        
        return False


def install_dependencies():
    """安装依赖"""
    print("📦 安装项目依赖...")
    
    requirements_file = project_root / 'requirements.txt'
    if not requirements_file.exists():
        print(f"❌ 未找到requirements.txt文件: {requirements_file}")
        return False
    
    try:
        # 升级pip
        run_command('python -m pip install --upgrade pip')
        
        # 安装依赖
        run_command(f'pip install -r "{requirements_file}"')
        
        print("✅ 依赖安装完成")
        return True
    except Exception as e:
        print(f"❌ 依赖安装失败: {e}")
        return False


def setup_env_file():
    """设置环境变量文件"""
    print("⚙️  设置环境变量文件...")
    
    env_example = project_root / '.env.example'
    env_file = project_root / '.env'
    
    if not env_example.exists():
        print(f"❌ 未找到.env.example文件: {env_example}")
        return False
    
    if env_file.exists():
        print(f"✅ .env文件已存在: {env_file}")
        return True
    
    try:
        # 复制.env.example到.env
        shutil.copy2(env_example, env_file)
        print(f"✅ 已创建.env文件: {env_file}")
        print("💡 请根据需要修改.env文件中的配置")
        return True
    except Exception as e:
        print(f"❌ 创建.env文件失败: {e}")
        return False


def create_directories():
    """创建必要的目录"""
    print("📁 创建必要的目录...")
    
    directories = [
        'logs',
        'data',
        'uploads',
        'static',
        'templates'
    ]
    
    for dir_name in directories:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ 创建目录: {dir_path}")
        else:
            print(f"📁 目录已存在: {dir_path}")


def check_dependencies():
    """检查关键依赖是否可用"""
    print("🔍 检查关键依赖...")
    
    dependencies = [
        ('tornado', 'Tornado Web框架'),
        ('pydantic', 'Pydantic数据验证'),
        ('aiofiles', '异步文件操作'),
        ('requests', 'HTTP请求库')
    ]
    
    all_ok = True
    for module_name, description in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {description}: {module_name}")
        except ImportError:
            print(f"❌ {description}: {module_name} 未安装")
            all_ok = False
    
    return all_ok


def run_tests():
    """运行测试"""
    print("🧪 运行测试...")
    
    tests_dir = project_root / 'tests'
    if not tests_dir.exists():
        print("⚠️  未找到tests目录，跳过测试")
        return True
    
    try:
        # 尝试运行pytest
        result = run_command('python -m pytest tests/ -v', check=False)
        if result.returncode == 0:
            print("✅ 所有测试通过")
            return True
        else:
            print("⚠️  部分测试失败，请检查")
            return False
    except Exception as e:
        print(f"⚠️  无法运行测试: {e}")
        return False


def print_next_steps():
    """打印后续步骤"""
    print("\n" + "="*60)
    print("🎉 开发环境设置完成！")
    print("="*60)
    print("\n📋 后续步骤:")
    print("1. 检查并修改 .env 文件中的配置")
    print("2. 启动开发服务器:")
    print(f"   python {project_root}/scripts/start.py --env development")
    print("   或者直接运行: python main.py")
    print("3. 访问 http://localhost:8888 查看应用")
    print("4. 查看 README.md 了解更多使用说明")
    print("\n💡 有用的命令:")
    print(f"   - 启动开发服务器: python {project_root}/scripts/start.py")
    print(f"   - 运行测试: python -m pytest tests/")
    print(f"   - 查看API文档: 查看 docs/ 目录")
    print("="*60)


def main():
    """主函数"""
    print("🚀 RPA Tornado 开发环境设置")
    print("="*60)
    
    try:
        # 检查Python版本
        check_python_version()
        
        # 检查虚拟环境
        if not check_virtual_env():
            print("\n⚠️  建议在虚拟环境中运行，是否继续？(y/N): ", end='')
            if input().lower() not in ['y', 'yes']:
                print("👋 设置已取消")
                return
        
        # 创建必要目录
        create_directories()
        
        # 设置环境变量文件
        setup_env_file()
        
        # 安装依赖
        if not install_dependencies():
            print("❌ 依赖安装失败，请手动安装")
            return
        
        # 检查依赖
        if not check_dependencies():
            print("❌ 部分依赖缺失，请检查安装")
            return
        
        # 运行测试
        run_tests()
        
        # 打印后续步骤
        print_next_steps()
        
    except KeyboardInterrupt:
        print("\n👋 设置已取消")
    except Exception as e:
        print(f"❌ 设置失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()