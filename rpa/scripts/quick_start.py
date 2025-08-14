#!/usr/bin/env python3
"""
RPA项目快速启动脚本
提供交互式菜单来运行各种RPA任务
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Any

class RPAQuickStart:
    """RPA快速启动器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.scripts = {
            '1': {
                'name': '退货处理',
                'script': 'process_returns.py',
                'description': '处理退货数据，生成统计报告'
            },
            '2': {
                'name': 'Excel数据处理',
                'script': 'process_excel.py',
                'description': '处理Excel文件，整合销售数据'
            },
            '3': {
                'name': 'BPD数据处理',
                'script': 'BpdData.py',
                'description': '处理BPD数据，分析广告效果'
            },
            '4': {
                'name': '新文件处理',
                'script': 'newfile.py',
                'description': '处理新文件，汇总发货数据'
            },
            '5': {
                'name': '项目状态检查',
                'script': 'check_project_status.py',
                'description': '检查项目环境状态'
            },
            '6': {
                'name': '配置验证',
                'script': 'config.py',
                'description': '验证项目配置'
            }
        }
    
    def show_menu(self):
        """显示菜单"""
        print("=" * 60)
        print("🤖 RPA项目快速启动")
        print("=" * 60)
        print()
        
        for key, script in self.scripts.items():
            print(f"{key}. {script['name']}")
            print(f"   {script['description']}")
            print()
        
        print("0. 退出")
        print()
    
    def run_script(self, script_name: str) -> bool:
        """运行脚本"""
        script_path = self.project_root / script_name
        
        if not script_path.exists():
            print(f"❌ 脚本不存在: {script_name}")
            return False
        
        print(f"🚀 正在运行: {script_name}")
        print("-" * 40)
        
        try:
            result = subprocess.run(
                ['uv', 'run', 'python', script_name],
                cwd=self.project_root,
                check=True
            )
            print("-" * 40)
            print(f"✅ {script_name} 执行完成")
            return True
        except subprocess.CalledProcessError as e:
            print("-" * 40)
            print(f"❌ {script_name} 执行失败: {e}")
            return False
        except KeyboardInterrupt:
            print("\n⚠️  用户中断执行")
            return False
    
    def run_interactive(self):
        """运行交互式菜单"""
        while True:
            self.show_menu()
            
            try:
                choice = input("请选择要运行的任务 (0-6): ").strip()
                
                if choice == '0':
                    print("👋 再见！")
                    break
                
                if choice in self.scripts:
                    script_info = self.scripts[choice]
                    print(f"\n📋 任务信息:")
                    print(f"   名称: {script_info['name']}")
                    print(f"   脚本: {script_info['script']}")
                    print(f"   描述: {script_info['description']}")
                    
                    confirm = input("\n确认运行? (y/N): ").strip().lower()
                    if confirm in ['y', 'yes', '是']:
                        self.run_script(script_info['script'])
                    
                    input("\n按回车键继续...")
                else:
                    print("❌ 无效选择，请重新输入")
                    input("按回车键继续...")
                    
            except KeyboardInterrupt:
                print("\n\n👋 再见！")
                break
            except EOFError:
                print("\n\n👋 再见！")
                break
    
    def run_direct(self, script_name: str) -> bool:
        """直接运行指定脚本"""
        if script_name in [s['script'] for s in self.scripts.values()]:
            return self.run_script(script_name)
        else:
            print(f"❌ 未知脚本: {script_name}")
            return False
    
    def list_scripts(self):
        """列出所有可用脚本"""
        print("📋 可用脚本列表:")
        print("-" * 40)
        
        for key, script in self.scripts.items():
            print(f"{key}. {script['name']} ({script['script']})")
            print(f"   {script['description']}")
            print()
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
RPA项目快速启动脚本

用法:
  python quick_start.py                    # 交互式菜单
  python quick_start.py --list             # 列出所有脚本
  python quick_start.py --run <script>     # 直接运行指定脚本
  python quick_start.py --help             # 显示帮助

示例:
  python quick_start.py --run process_returns.py
  python quick_start.py --list

可用脚本:
  process_returns.py    - 退货处理
  process_excel.py      - Excel数据处理
  BpdData.py           - BPD数据处理
  newfile.py           - 新文件处理
  check_project_status.py - 项目状态检查
  config.py            - 配置验证
        """
        print(help_text)

def main():
    """主函数"""
    quick_start = RPAQuickStart()
    
    if len(sys.argv) == 1:
        # 交互式模式
        quick_start.run_interactive()
    elif len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg in ['--help', '-h', 'help']:
            quick_start.show_help()
        elif arg in ['--list', '-l', 'list']:
            quick_start.list_scripts()
        else:
            print(f"❌ 未知参数: {arg}")
            quick_start.show_help()
    elif len(sys.argv) == 3 and sys.argv[1] in ['--run', '-r', 'run']:
        # 直接运行模式
        script_name = sys.argv[2]
        success = quick_start.run_direct(script_name)
        sys.exit(0 if success else 1)
    else:
        print("❌ 参数错误")
        quick_start.show_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 
 