#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DBeaver PostgreSQL 连接测试脚本
用于验证数据库连接参数是否正确
"""

import psycopg2
from psycopg2 import sql
import sys
from datetime import datetime

# 数据库连接参数
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'rpa_tornado',
    'user': 'dbadmin',
    'password': 'dbadmin123'
}

def test_connection():
    """
    测试PostgreSQL数据库连接
    """
    print("🔍 开始测试PostgreSQL连接...")
    print(f"📋 连接参数: {DB_CONFIG['user']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    print("-" * 50)
    
    try:
        # 尝试连接数据库
        print("⏳ 正在连接数据库...")
        conn = psycopg2.connect(**DB_CONFIG)
        
        # 创建游标
        cursor = conn.cursor()
        
        # 测试查询
        print("✅ 连接成功！正在执行测试查询...")
        
        # 查询数据库版本
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"📊 数据库版本: {version.split(',')[0]}")
        
        # 查询当前用户
        cursor.execute("SELECT current_user;")
        current_user = cursor.fetchone()[0]
        print(f"👤 当前用户: {current_user}")
        
        # 查询当前数据库
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()[0]
        print(f"🗄️ 当前数据库: {current_db}")
        
        # 查询表数量
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        table_count = cursor.fetchone()[0]
        print(f"📋 公共模式表数量: {table_count}")
        
        # 查询所有表名
        if table_count > 0:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            print("📝 表列表:")
            for table in tables:
                print(f"   - {table[0]}")
        
        # 关闭连接
        cursor.close()
        conn.close()
        
        print("-" * 50)
        print("🎉 数据库连接测试成功！")
        print("💡 您可以在DBeaver中使用相同的连接参数")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ 连接失败: {e}")
        print("\n🔧 可能的解决方案:")
        print("1. 检查PostgreSQL容器是否正在运行: docker ps")
        print("2. 检查端口5432是否被占用")
        print("3. 验证连接参数是否正确")
        return False
        
    except psycopg2.Error as e:
        print(f"❌ 数据库错误: {e}")
        return False
        
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def main():
    """
    主函数
    """
    print(f"🚀 PostgreSQL连接测试 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    success = test_connection()
    
    if success:
        print("\n✅ 测试完成 - 连接正常")
        sys.exit(0)
    else:
        print("\n❌ 测试失败 - 请检查配置")
        sys.exit(1)

if __name__ == "__main__":
    main()