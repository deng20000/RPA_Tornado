#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目工具脚本
提供代码格式化、依赖检查、性能分析等实用功能
"""

import os
import sys
import json
import time
import argparse
import subprocess
from pathlib import Path
from collections import defaultdict

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_command(cmd, cwd=None, capture_output=True):
    """执行命令并返回结果"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd or project_root,
            capture_output=capture_output,
            text=True,
            encoding='utf-8'
        )
        return result
    except Exception as e:
        print(f"❌ 命令执行失败: {e}")
        return None


def format_code():
    """格式化Python代码"""
    print("🎨 格式化Python代码...")
    
    # 查找所有Python文件
    python_files = []
    for pattern in ['**/*.py']:
        python_files.extend(project_root.glob(pattern))
    
    # 排除虚拟环境和缓存目录
    exclude_patterns = ['.venv', '__pycache__', '.git', 'node_modules']
    python_files = [
        f for f in python_files 
        if not any(pattern in str(f) for pattern in exclude_patterns)
    ]
    
    if not python_files:
        print("⚠️  未找到Python文件")
        return False
    
    print(f"📁 找到 {len(python_files)} 个Python文件")
    
    # 尝试使用black格式化
    try:
        # 检查是否安装了black
        result = run_command('python -m black --version')
        if result and result.returncode == 0:
            print("🔧 使用black格式化代码...")
            
            # 格式化所有Python文件
            cmd = f'python -m black --line-length 88 --target-version py38 "{project_root}"'
            result = run_command(cmd, capture_output=False)
            
            if result and result.returncode == 0:
                print("✅ 代码格式化完成")
                return True
            else:
                print("❌ black格式化失败")
        else:
            print("⚠️  未安装black，跳过代码格式化")
            print("💡 安装black: pip install black")
            
    except Exception as e:
        print(f"❌ 格式化失败: {e}")
    
    return False


def check_code_quality():
    """检查代码质量"""
    print("🔍 检查代码质量...")
    
    tools = [
        ('flake8', '代码风格检查'),
        ('pylint', '代码质量分析'),
        ('mypy', '类型检查')
    ]
    
    results = {}
    
    for tool, description in tools:
        print(f"\n🔧 {description} ({tool})...")
        
        try:
            # 检查工具是否可用
            version_result = run_command(f'python -m {tool} --version')
            if not version_result or version_result.returncode != 0:
                print(f"⚠️  {tool} 未安装，跳过")
                continue
            
            # 运行检查
            if tool == 'flake8':
                cmd = f'python -m flake8 "{project_root}/app" --max-line-length=88 --ignore=E203,W503'
            elif tool == 'pylint':
                cmd = f'python -m pylint "{project_root}/app" --output-format=text --score=yes'
            elif tool == 'mypy':
                cmd = f'python -m mypy "{project_root}/app" --ignore-missing-imports'
            
            result = run_command(cmd)
            
            if result:
                results[tool] = {
                    'returncode': result.returncode,
                    'stdout': result.stdout,
                    'stderr': result.stderr
                }
                
                if result.returncode == 0:
                    print(f"✅ {description} 通过")
                else:
                    print(f"⚠️  {description} 发现问题")
                    if result.stdout:
                        print(result.stdout[:500])  # 只显示前500字符
            
        except Exception as e:
            print(f"❌ {tool} 检查失败: {e}")
    
    return results


def analyze_dependencies():
    """分析项目依赖"""
    print("📦 分析项目依赖...")
    
    requirements_file = project_root / 'requirements.txt'
    if not requirements_file.exists():
        print(f"❌ 未找到requirements.txt文件")
        return False
    
    # 读取requirements.txt
    with open(requirements_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    dependencies = []
    categories = defaultdict(list)
    current_category = 'uncategorized'
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            # 检查是否是分类注释
            if line.startswith('#') and '=' in line:
                current_category = line.replace('#', '').strip()
            continue
        
        if '==' in line:
            pkg_name = line.split('==')[0].strip()
            pkg_version = line.split('==')[1].strip()
            dependencies.append((pkg_name, pkg_version))
            categories[current_category].append((pkg_name, pkg_version))
    
    print(f"\n📊 依赖统计:")
    print(f"   总依赖数: {len(dependencies)}")
    print(f"   分类数: {len(categories)}")
    
    # 按分类显示依赖
    for category, deps in categories.items():
        print(f"\n📂 {category} ({len(deps)} 个):")
        for pkg_name, pkg_version in sorted(deps):
            print(f"   - {pkg_name}=={pkg_version}")
    
    # 检查过时的依赖
    print("\n🔍 检查依赖更新...")
    try:
        result = run_command('python -m pip list --outdated --format=json')
        if result and result.returncode == 0:
            outdated = json.loads(result.stdout)
            if outdated:
                print(f"⚠️  发现 {len(outdated)} 个过时的依赖:")
                for pkg in outdated:
                    print(f"   - {pkg['name']}: {pkg['version']} -> {pkg['latest_version']}")
            else:
                print("✅ 所有依赖都是最新的")
    except Exception as e:
        print(f"⚠️  无法检查依赖更新: {e}")
    
    return True


def profile_performance():
    """性能分析"""
    print("⚡ 性能分析...")
    
    # 检查是否有性能分析工具
    tools = ['cProfile', 'line_profiler', 'memory_profiler']
    available_tools = []
    
    for tool in tools:
        try:
            if tool == 'cProfile':
                # cProfile是内置模块
                import cProfile
                available_tools.append(tool)
            else:
                result = run_command(f'python -m {tool} --help')
                if result and result.returncode == 0:
                    available_tools.append(tool)
        except:
            pass
    
    print(f"📋 可用的性能分析工具: {', '.join(available_tools) if available_tools else '无'}")
    
    if not available_tools:
        print("💡 安装性能分析工具:")
        print("   pip install line-profiler memory-profiler")
        return False
    
    # 创建简单的性能测试脚本
    test_script = project_root / 'temp_performance_test.py'
    
    test_code = '''
import time
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_import_performance():
    """测试导入性能"""
    start_time = time.time()
    
    try:
        from app.config import settings
        from app.routes import routes
        import_time = time.time() - start_time
        print(f"模块导入耗时: {import_time:.3f}秒")
        return import_time
    except Exception as e:
        print(f"导入失败: {e}")
        return None

def test_config_loading():
    """测试配置加载性能"""
    start_time = time.time()
    
    try:
        from app.config import get_config
        config = get_config()
        load_time = time.time() - start_time
        print(f"配置加载耗时: {load_time:.3f}秒")
        return load_time
    except Exception as e:
        print(f"配置加载失败: {e}")
        return None

if __name__ == '__main__':
    print("🚀 开始性能测试...")
    
    # 测试导入性能
    import_time = test_import_performance()
    
    # 测试配置加载性能
    config_time = test_config_loading()
    
    print("\n📊 性能测试结果:")
    if import_time:
        print(f"   模块导入: {import_time:.3f}秒")
    if config_time:
        print(f"   配置加载: {config_time:.3f}秒")
'''
    
    try:
        # 写入测试脚本
        with open(test_script, 'w', encoding='utf-8') as f:
            f.write(test_code)
        
        # 运行性能测试
        print("\n🔧 运行性能测试...")
        result = run_command(f'python "{test_script}"', capture_output=False)
        
        # 如果有cProfile，运行详细分析
        if 'cProfile' in available_tools:
            print("\n🔍 详细性能分析...")
            profile_output = project_root / 'performance_profile.txt'
            cmd = f'python -m cProfile -o "{profile_output}" "{test_script}"'
            run_command(cmd)
            
            if profile_output.exists():
                print(f"✅ 性能分析报告已保存: {profile_output}")
        
        return True
        
    except Exception as e:
        print(f"❌ 性能分析失败: {e}")
        return False
    
    finally:
        # 清理临时文件
        if test_script.exists():
            test_script.unlink()


def clean_project():
    """清理项目文件"""
    print("🧹 清理项目文件...")
    
    # 要清理的文件和目录模式
    patterns = [
        '**/__pycache__',
        '**/*.pyc',
        '**/*.pyo',
        '**/*.pyd',
        '**/.pytest_cache',
        '**/.coverage',
        '**/htmlcov',
        '**/*.egg-info',
        '**/build',
        '**/dist',
        '**/.mypy_cache',
        '**/temp_*.py',
        '**/performance_profile.txt'
    ]
    
    removed_count = 0
    
    for pattern in patterns:
        for path in project_root.glob(pattern):
            try:
                if path.is_file():
                    path.unlink()
                    print(f"🗑️  删除文件: {path.relative_to(project_root)}")
                elif path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                    print(f"🗑️  删除目录: {path.relative_to(project_root)}")
                removed_count += 1
            except Exception as e:
                print(f"⚠️  无法删除 {path}: {e}")
    
    print(f"\n✅ 清理完成，删除了 {removed_count} 个文件/目录")
    return True


def generate_project_stats():
    """生成项目统计信息"""
    print("📊 生成项目统计信息...")
    
    stats = {
        'files': defaultdict(int),
        'lines': defaultdict(int),
        'size': defaultdict(int)
    }
    
    # 统计文件
    for file_path in project_root.rglob('*'):
        if file_path.is_file():
            # 排除某些目录
            if any(exclude in str(file_path) for exclude in ['.git', '__pycache__', '.venv']):
                continue
            
            suffix = file_path.suffix or 'no_extension'
            stats['files'][suffix] += 1
            stats['size'][suffix] += file_path.stat().st_size
            
            # 统计代码行数
            if suffix in ['.py', '.js', '.html', '.css', '.yaml', '.yml', '.json']:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        stats['lines'][suffix] += lines
                except:
                    pass
    
    # 输出统计信息
    print("\n📋 项目统计:")
    print("-" * 50)
    
    total_files = sum(stats['files'].values())
    total_size = sum(stats['size'].values())
    total_lines = sum(stats['lines'].values())
    
    print(f"总文件数: {total_files}")
    print(f"总大小: {total_size / (1024*1024):.2f} MB")
    print(f"总代码行数: {total_lines}")
    
    print("\n📂 按文件类型统计:")
    for suffix in sorted(stats['files'].keys()):
        files = stats['files'][suffix]
        size = stats['size'][suffix] / 1024  # KB
        lines = stats['lines'][suffix]
        
        print(f"  {suffix:10} | {files:4d} 文件 | {size:8.1f} KB | {lines:6d} 行")
    
    return stats


def main():
    parser = argparse.ArgumentParser(description='RPA Tornado 项目工具')
    parser.add_argument(
        'command',
        choices=['format', 'check', 'deps', 'profile', 'clean', 'stats', 'all'],
        help='要执行的操作'
    )
    
    args = parser.parse_args()
    
    print(f"🛠️  RPA Tornado 项目工具")
    print("=" * 50)
    
    try:
        if args.command == 'format':
            format_code()
        
        elif args.command == 'check':
            check_code_quality()
        
        elif args.command == 'deps':
            analyze_dependencies()
        
        elif args.command == 'profile':
            profile_performance()
        
        elif args.command == 'clean':
            clean_project()
        
        elif args.command == 'stats':
            generate_project_stats()
        
        elif args.command == 'all':
            print("🚀 执行所有检查...\n")
            
            # 清理项目
            clean_project()
            print()
            
            # 格式化代码
            format_code()
            print()
            
            # 检查代码质量
            check_code_quality()
            print()
            
            # 分析依赖
            analyze_dependencies()
            print()
            
            # 生成统计
            generate_project_stats()
            print()
            
            print("✅ 所有检查完成")
    
    except KeyboardInterrupt:
        print("\n👋 操作已取消")
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()