#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试运行脚本
提供便捷的测试运行命令
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


def run_command(cmd, cwd=None):
    """运行命令"""
    print(f"🔧 执行命令: {cmd}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or PROJECT_ROOT,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 命令执行失败: {e}")
        return False


def run_unit_tests():
    """运行单元测试"""
    print("\n🧪 运行单元测试...")
    cmd = "python -m pytest tests/unit/ -v -m unit"
    return run_command(cmd)


def run_integration_tests():
    """运行集成测试"""
    print("\n🔗 运行集成测试...")
    cmd = "python -m pytest tests/integration/ -v -m integration"
    return run_command(cmd)


def run_api_tests():
    """运行API测试"""
    print("\n🌐 运行API测试...")
    cmd = "python -m pytest tests/integration/ -v -m api"
    return run_command(cmd)


def run_all_tests():
    """运行所有测试"""
    print("\n🚀 运行所有测试...")
    cmd = "python -m pytest tests/ -v"
    return run_command(cmd)


def run_coverage_tests():
    """运行测试覆盖率"""
    print("\n📊 运行测试覆盖率分析...")
    
    # 检查coverage是否安装
    if not run_command("python -m coverage --version"):
        print("⚠️  coverage未安装，正在安装...")
        if not run_command("pip install coverage"):
            print("❌ coverage安装失败")
            return False
    
    # 运行覆盖率测试
    commands = [
        "python -m coverage erase",
        "python -m coverage run -m pytest tests/",
        "python -m coverage report -m",
        "python -m coverage html"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            return False
    
    print("✅ 覆盖率报告已生成: htmlcov/index.html")
    return True


def run_smoke_tests():
    """运行冒烟测试"""
    print("\n💨 运行冒烟测试...")
    cmd = "python -m pytest tests/ -v -m smoke --maxfail=1"
    return run_command(cmd)


def check_test_environment():
    """检查测试环境"""
    print("🔍 检查测试环境...")
    
    # 检查pytest
    if not run_command("python -m pytest --version"):
        print("❌ pytest未安装")
        return False
    
    # 检查测试目录
    tests_dir = PROJECT_ROOT / 'tests'
    if not tests_dir.exists():
        print(f"❌ 测试目录不存在: {tests_dir}")
        return False
    
    # 检查服务是否运行
    try:
        import requests
        response = requests.get("http://127.0.0.1:8888/health", timeout=5)
        if response.status_code == 200:
            print("✅ 测试服务运行正常")
        else:
            print("⚠️  测试服务响应异常")
    except Exception:
        print("⚠️  测试服务未运行，请先启动服务")
    
    print("✅ 测试环境检查完成")
    return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='RPA Tornado 测试运行器')
    parser.add_argument('--type', '-t', 
                       choices=['unit', 'integration', 'api', 'all', 'coverage', 'smoke', 'check'],
                       default='all',
                       help='测试类型')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🧪 RPA Tornado 测试运行器")
    print("=" * 60)
    
    # 切换到项目目录
    os.chdir(PROJECT_ROOT)
    
    success = True
    
    if args.type == 'check':
        success = check_test_environment()
    elif args.type == 'unit':
        success = run_unit_tests()
    elif args.type == 'integration':
        success = run_integration_tests()
    elif args.type == 'api':
        success = run_api_tests()
    elif args.type == 'coverage':
        success = run_coverage_tests()
    elif args.type == 'smoke':
        success = run_smoke_tests()
    elif args.type == 'all':
        success = run_all_tests()
    
    if success:
        print("\n✅ 测试完成")
        sys.exit(0)
    else:
        print("\n❌ 测试失败")
        sys.exit(1)


if __name__ == '__main__':
    main()