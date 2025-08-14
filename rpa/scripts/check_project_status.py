#!/usr/bin/env python3
"""
RPA项目状态检查脚本
检查项目环境、依赖、配置等状态
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path
from typing import List, Dict, Any, Tuple

class ProjectStatusChecker:
    """项目状态检查器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.status = {
            'uv_installed': False,
            'dependencies_installed': False,
            'directories_exist': False,
            'config_valid': False,
            'imports_working': False,
            'tests_passing': False
        }
    
    def check_uv_installation(self) -> bool:
        """检查uv是否已安装"""
        try:
            result = subprocess.run(['uv', '--version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ uv已安装: {result.stdout.strip()}")
            self.status['uv_installed'] = True
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ uv未安装")
            self.status['uv_installed'] = False
            return False
    
    def check_dependencies(self) -> bool:
        """检查依赖是否已安装"""
        try:
            # 检查关键依赖
            key_dependencies = [
                'pandas', 'numpy', 'openpyxl', 'requests', 
                'psutil', 'beautifulsoup4', 'colorama'
            ]
            
            missing_deps = []
            for dep in key_dependencies:
                try:
                    importlib.import_module(dep)
                    print(f"✅ {dep} 已安装")
                except ImportError:
                    print(f"❌ {dep} 未安装")
                    missing_deps.append(dep)
            
            if missing_deps:
                print(f"缺少依赖: {', '.join(missing_deps)}")
                self.status['dependencies_installed'] = False
                return False
            else:
                self.status['dependencies_installed'] = True
                return True
        except Exception as e:
            print(f"❌ 检查依赖时出错: {e}")
            self.status['dependencies_installed'] = False
            return False
    
    def check_directories(self) -> bool:
        """检查必要目录是否存在"""
        required_dirs = [
            'data', 'output', 'logs', 'temp', 'tests'
        ]
        
        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                print(f"✅ 目录存在: {dir_name}")
            else:
                print(f"❌ 目录不存在: {dir_name}")
                missing_dirs.append(dir_name)
        
        if missing_dirs:
            print(f"缺少目录: {', '.join(missing_dirs)}")
            self.status['directories_exist'] = False
            return False
        else:
            self.status['directories_exist'] = True
            return True
    
    def check_config(self) -> bool:
        """检查配置文件"""
        try:
            # 检查配置文件
            config_file = self.project_root / 'config.py'
            if config_file.exists():
                print("✅ 配置文件存在")
                
                # 尝试导入配置
                sys.path.insert(0, str(self.project_root))
                import config
                config_instance = config.get_config()
                print(f"✅ 配置加载成功 - 环境: {config.ENVIRONMENT}")
                
                self.status['config_valid'] = True
                return True
            else:
                print("❌ 配置文件不存在")
                self.status['config_valid'] = False
                return False
        except Exception as e:
            print(f"❌ 配置检查失败: {e}")
            self.status['config_valid'] = False
            return False
    
    def check_imports(self) -> bool:
        """检查关键模块导入"""
        try:
            # 检查关键模块
            key_modules = [
                'process_returns',
                'process_excel', 
                'BpdData',
                'newfile',
                'config',
                'utils.logger'
            ]
            
            failed_imports = []
            for module in key_modules:
                try:
                    importlib.import_module(module)
                    print(f"✅ 模块导入成功: {module}")
                except ImportError as e:
                    print(f"❌ 模块导入失败: {module} - {e}")
                    failed_imports.append(module)
            
            if failed_imports:
                print(f"导入失败的模块: {', '.join(failed_imports)}")
                self.status['imports_working'] = False
                return False
            else:
                self.status['imports_working'] = True
                return True
        except Exception as e:
            print(f"❌ 导入检查失败: {e}")
            self.status['imports_working'] = False
            return False
    
    def check_tests(self) -> bool:
        """检查测试"""
        try:
            # 检查测试目录
            tests_dir = self.project_root / 'tests'
            if not tests_dir.exists():
                print("⚠️  测试目录不存在")
                self.status['tests_passing'] = False
                return False
            
            # 运行测试
            result = subprocess.run(['uv', 'run', 'pytest', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ pytest可用")
                
                # 运行简单测试
                test_result = subprocess.run(['uv', 'run', 'pytest', 'tests/', '-v'], 
                                           capture_output=True, text=True, timeout=30)
                if test_result.returncode == 0:
                    print("✅ 测试通过")
                    self.status['tests_passing'] = True
                    return True
                else:
                    print("❌ 测试失败")
                    print(test_result.stdout)
                    print(test_result.stderr)
                    self.status['tests_passing'] = False
                    return False
            else:
                print("❌ pytest不可用")
                self.status['tests_passing'] = False
                return False
        except subprocess.TimeoutExpired:
            print("⚠️  测试超时")
            self.status['tests_passing'] = False
            return False
        except Exception as e:
            print(f"❌ 测试检查失败: {e}")
            self.status['tests_passing'] = False
            return False
    
    def check_project_files(self) -> Dict[str, bool]:
        """检查项目文件"""
        required_files = [
            'pyproject.toml',
            'uv.lock',
            'Makefile',
            'setup_env.py',
            'config.py',
            'README.md',
            'UV_SETUP.md'
        ]
        
        file_status = {}
        for file_name in required_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                print(f"✅ 文件存在: {file_name}")
                file_status[file_name] = True
            else:
                print(f"❌ 文件不存在: {file_name}")
                file_status[file_name] = False
        
        return file_status
    
    def generate_report(self) -> str:
        """生成状态报告"""
        report = []
        report.append("=" * 50)
        report.append("RPA项目状态报告")
        report.append("=" * 50)
        
        # 总体状态
        passed_checks = sum(self.status.values())
        total_checks = len(self.status)
        overall_status = "✅ 通过" if passed_checks == total_checks else "❌ 需要修复"
        
        report.append(f"\n总体状态: {overall_status} ({passed_checks}/{total_checks})")
        
        # 详细状态
        report.append("\n详细状态:")
        for check, status in self.status.items():
            status_icon = "✅" if status else "❌"
            check_name = check.replace('_', ' ').title()
            report.append(f"  {status_icon} {check_name}: {'通过' if status else '失败'}")
        
        # 建议
        report.append("\n建议:")
        if not self.status['uv_installed']:
            report.append("  - 安装uv: powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
        
        if not self.status['dependencies_installed']:
            report.append("  - 安装依赖: uv sync")
        
        if not self.status['directories_exist']:
            report.append("  - 创建目录: python setup_env.py")
        
        if not self.status['config_valid']:
            report.append("  - 检查配置文件")
        
        if not self.status['imports_working']:
            report.append("  - 检查模块导入")
        
        if not self.status['tests_passing']:
            report.append("  - 修复测试")
        
        return "\n".join(report)
    
    def run_all_checks(self) -> Dict[str, Any]:
        """运行所有检查"""
        print("🔍 开始项目状态检查...\n")
        
        # 运行各项检查
        self.check_uv_installation()
        print()
        
        self.check_dependencies()
        print()
        
        self.check_directories()
        print()
        
        self.check_config()
        print()
        
        self.check_imports()
        print()
        
        self.check_tests()
        print()
        
        file_status = self.check_project_files()
        print()
        
        # 生成报告
        report = self.generate_report()
        print(report)
        
        return {
            'status': self.status,
            'file_status': file_status,
            'report': report
        }

def main():
    """主函数"""
    checker = ProjectStatusChecker()
    result = checker.run_all_checks()
    
    # 返回退出码
    passed_checks = sum(checker.status.values())
    total_checks = len(checker.status)
    
    if passed_checks == total_checks:
        print("\n🎉 所有检查通过！")
        sys.exit(0)
    else:
        print(f"\n⚠️  有 {total_checks - passed_checks} 项检查未通过")
        sys.exit(1)

if __name__ == "__main__":
    main() 