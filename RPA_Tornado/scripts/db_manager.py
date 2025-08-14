#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库管理脚本
提供数据库初始化、迁移、备份等功能
"""

import os
import sys
import json
import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self):
        self.project_root = project_root
        self.data_dir = self.project_root / 'data'
        self.backup_dir = self.data_dir / 'backups'
        
        # 确保目录存在
        self.data_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
    
    def get_db_files(self):
        """获取所有数据库文件"""
        db_files = []
        
        # 查找SQLite数据库文件
        for pattern in ['*.db', '*.sqlite', '*.sqlite3']:
            db_files.extend(self.data_dir.glob(pattern))
        
        # 查找应用数据目录中的数据库文件
        app_data_dir = self.project_root / 'app' / 'unprocessed_data'
        if app_data_dir.exists():
            for pattern in ['*.db', '*.sqlite', '*.sqlite3']:
                db_files.extend(app_data_dir.glob(pattern))
        
        return list(set(db_files))  # 去重
    
    def init_database(self):
        """初始化数据库"""
        print("🗄️  初始化数据库...")
        
        # 创建主数据库
        main_db = self.data_dir / 'main.db'
        
        try:
            with sqlite3.connect(main_db) as conn:
                cursor = conn.cursor()
                
                # 创建系统表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS system_info (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        key TEXT UNIQUE NOT NULL,
                        value TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # 创建日志表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS app_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        level TEXT NOT NULL,
                        message TEXT NOT NULL,
                        module TEXT,
                        function TEXT,
                        line_number INTEGER,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # 创建配置表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS app_config (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        section TEXT NOT NULL,
                        key TEXT NOT NULL,
                        value TEXT,
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(section, key)
                    )
                """)
                
                # 插入初始数据
                cursor.execute("""
                    INSERT OR REPLACE INTO system_info (key, value) 
                    VALUES ('db_version', '1.0.0')
                """)
                
                cursor.execute("""
                    INSERT OR REPLACE INTO system_info (key, value) 
                    VALUES ('initialized_at', ?)
                """, (datetime.now().isoformat(),))
                
                conn.commit()
                
            print(f"✅ 数据库初始化完成: {main_db}")
            return True
            
        except Exception as e:
            print(f"❌ 数据库初始化失败: {e}")
            return False
    
    def backup_database(self, db_file=None):
        """备份数据库"""
        if db_file:
            db_files = [Path(db_file)]
        else:
            db_files = self.get_db_files()
        
        if not db_files:
            print("⚠️  未找到数据库文件")
            return False
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        success_count = 0
        
        for db_file in db_files:
            if not db_file.exists():
                print(f"⚠️  数据库文件不存在: {db_file}")
                continue
            
            try:
                # 创建备份文件名
                backup_name = f"{db_file.stem}_{timestamp}.backup"
                backup_path = self.backup_dir / backup_name
                
                # 使用SQLite的备份API
                with sqlite3.connect(db_file) as source:
                    with sqlite3.connect(backup_path) as backup:
                        source.backup(backup)
                
                print(f"✅ 备份完成: {db_file.name} -> {backup_name}")
                success_count += 1
                
            except Exception as e:
                print(f"❌ 备份失败 {db_file.name}: {e}")
        
        print(f"\n📊 备份统计: {success_count}/{len(db_files)} 个数据库备份成功")
        return success_count > 0
    
    def restore_database(self, backup_file, target_db=None):
        """恢复数据库"""
        backup_path = Path(backup_file)
        
        if not backup_path.exists():
            print(f"❌ 备份文件不存在: {backup_file}")
            return False
        
        if not target_db:
            # 从备份文件名推断目标数据库
            backup_name = backup_path.stem
            if '_' in backup_name:
                db_name = '_'.join(backup_name.split('_')[:-1]) + '.db'
                target_db = self.data_dir / db_name
            else:
                print("❌ 无法确定目标数据库，请指定target_db参数")
                return False
        else:
            target_db = Path(target_db)
        
        try:
            # 如果目标数据库存在，先备份
            if target_db.exists():
                print(f"⚠️  目标数据库已存在，先进行备份...")
                self.backup_database(target_db)
            
            # 恢复数据库
            with sqlite3.connect(backup_path) as source:
                with sqlite3.connect(target_db) as target:
                    source.backup(target)
            
            print(f"✅ 数据库恢复完成: {backup_path.name} -> {target_db.name}")
            return True
            
        except Exception as e:
            print(f"❌ 数据库恢复失败: {e}")
            return False
    
    def list_backups(self):
        """列出所有备份"""
        backup_files = list(self.backup_dir.glob('*.backup'))
        
        if not backup_files:
            print("📁 未找到备份文件")
            return
        
        print(f"📋 备份文件列表 ({len(backup_files)} 个):")
        print("-" * 60)
        
        for backup_file in sorted(backup_files, key=lambda x: x.stat().st_mtime, reverse=True):
            stat = backup_file.stat()
            size = stat.st_size
            mtime = datetime.fromtimestamp(stat.st_mtime)
            
            # 格式化文件大小
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size / (1024 * 1024):.1f} MB"
            
            print(f"📄 {backup_file.name}")
            print(f"   大小: {size_str}")
            print(f"   时间: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
    
    def check_database(self, db_file=None):
        """检查数据库完整性"""
        if db_file:
            db_files = [Path(db_file)]
        else:
            db_files = self.get_db_files()
        
        if not db_files:
            print("⚠️  未找到数据库文件")
            return False
        
        all_ok = True
        
        for db_file in db_files:
            if not db_file.exists():
                print(f"❌ 数据库文件不存在: {db_file}")
                all_ok = False
                continue
            
            try:
                with sqlite3.connect(db_file) as conn:
                    cursor = conn.cursor()
                    
                    # 检查数据库完整性
                    cursor.execute("PRAGMA integrity_check")
                    result = cursor.fetchone()[0]
                    
                    if result == 'ok':
                        print(f"✅ 数据库完整性检查通过: {db_file.name}")
                        
                        # 获取表信息
                        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                        tables = cursor.fetchall()
                        print(f"   表数量: {len(tables)}")
                        
                        # 获取数据库大小
                        size = db_file.stat().st_size
                        if size < 1024 * 1024:
                            size_str = f"{size / 1024:.1f} KB"
                        else:
                            size_str = f"{size / (1024 * 1024):.1f} MB"
                        print(f"   文件大小: {size_str}")
                    else:
                        print(f"❌ 数据库完整性检查失败: {db_file.name}")
                        print(f"   错误: {result}")
                        all_ok = False
                        
            except Exception as e:
                print(f"❌ 检查数据库失败 {db_file.name}: {e}")
                all_ok = False
        
        return all_ok
    
    def export_data(self, db_file, output_file=None):
        """导出数据为JSON格式"""
        db_path = Path(db_file)
        
        if not db_path.exists():
            print(f"❌ 数据库文件不存在: {db_file}")
            return False
        
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = self.data_dir / f"{db_path.stem}_export_{timestamp}.json"
        else:
            output_file = Path(output_file)
        
        try:
            with sqlite3.connect(db_path) as conn:
                conn.row_factory = sqlite3.Row  # 使结果可以按列名访问
                cursor = conn.cursor()
                
                # 获取所有表
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [row[0] for row in cursor.fetchall()]
                
                export_data = {}
                
                for table in tables:
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    
                    # 转换为字典列表
                    export_data[table] = [
                        dict(row) for row in rows
                    ]
                
                # 写入JSON文件
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2, default=str)
                
                print(f"✅ 数据导出完成: {output_file}")
                print(f"   表数量: {len(tables)}")
                
                # 统计记录数
                total_records = sum(len(records) for records in export_data.values())
                print(f"   总记录数: {total_records}")
                
                return True
                
        except Exception as e:
            print(f"❌ 数据导出失败: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='RPA Tornado 数据库管理工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 初始化命令
    subparsers.add_parser('init', help='初始化数据库')
    
    # 备份命令
    backup_parser = subparsers.add_parser('backup', help='备份数据库')
    backup_parser.add_argument('--db', help='指定要备份的数据库文件')
    
    # 恢复命令
    restore_parser = subparsers.add_parser('restore', help='恢复数据库')
    restore_parser.add_argument('backup_file', help='备份文件路径')
    restore_parser.add_argument('--target', help='目标数据库文件')
    
    # 列出备份命令
    subparsers.add_parser('list-backups', help='列出所有备份')
    
    # 检查命令
    check_parser = subparsers.add_parser('check', help='检查数据库完整性')
    check_parser.add_argument('--db', help='指定要检查的数据库文件')
    
    # 导出命令
    export_parser = subparsers.add_parser('export', help='导出数据为JSON')
    export_parser.add_argument('db_file', help='数据库文件路径')
    export_parser.add_argument('--output', help='输出文件路径')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    db_manager = DatabaseManager()
    
    try:
        if args.command == 'init':
            db_manager.init_database()
        
        elif args.command == 'backup':
            db_manager.backup_database(args.db)
        
        elif args.command == 'restore':
            db_manager.restore_database(args.backup_file, args.target)
        
        elif args.command == 'list-backups':
            db_manager.list_backups()
        
        elif args.command == 'check':
            db_manager.check_database(args.db)
        
        elif args.command == 'export':
            db_manager.export_data(args.db_file, args.output)
        
    except KeyboardInterrupt:
        print("\n👋 操作已取消")
    except Exception as e:
        print(f"❌ 操作失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()