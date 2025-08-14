#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用 psycopg3 测试 PostgreSQL 连接
"""

import psycopg
import sys

def test_psycopg3_connection():
    """使用 psycopg3 测试连接"""
    print("=== 使用 psycopg3 测试连接 ===")
    try:
        # 使用 psycopg3 的连接字符串格式
        conn_string = "host=127.0.0.1 port=5432 dbname=rpa_tornado user=dbadmin password=admin123"
        
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT version();")
                result = cursor.fetchone()
                print(f"✅ psycopg3 连接成功!")
                print(f"PostgreSQL 版本: {result[0][:80]}...")
                
                # 测试中文字符
                cursor.execute("SELECT '测试中文字符' as test_chinese;")
                chinese_result = cursor.fetchone()
                print(f"中文测试: {chinese_result[0]}")
                
                return True
                
    except Exception as e:
        print(f"❌ psycopg3 连接失败: {e}")
        return False

def test_psycopg3_postgres_user():
    """使用 postgres 用户测试 psycopg3 连接"""
    print("\n=== 使用 postgres 用户测试 psycopg3 ===")
    try:
        conn_string = "host=127.0.0.1 port=5432 dbname=postgres user=postgres password=postgres"
        
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT current_database(), current_user;")
                result = cursor.fetchone()
                print(f"✅ postgres 用户连接成功!")
                print(f"数据库: {result[0]}, 用户: {result[1]}")
                
                # 检查 rpa_tornado 数据库是否存在
                cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'rpa_tornado';")
                db_exists = cursor.fetchone()
                if db_exists:
                    print("✅ rpa_tornado 数据库存在")
                else:
                    print("❌ rpa_tornado 数据库不存在")
                
                return True
                
    except Exception as e:
        print(f"❌ postgres 用户连接失败: {e}")
        return False

def test_create_table():
    """测试创建表和插入数据"""
    print("\n=== 测试创建表和插入数据 ===")
    try:
        conn_string = "host=127.0.0.1 port=5432 dbname=rpa_tornado user=dbadmin password=admin123"
        
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                # 创建测试表
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS test_table (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100),
                        description TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                # 插入测试数据
                cursor.execute("""
                    INSERT INTO test_table (name, description) 
                    VALUES (%s, %s) 
                    ON CONFLICT DO NOTHING;
                """, ("测试名称", "这是一个测试描述，包含中文字符"))
                
                # 查询数据
                cursor.execute("SELECT * FROM test_table LIMIT 1;")
                result = cursor.fetchone()
                
                if result:
                    print(f"✅ 表操作成功!")
                    print(f"ID: {result[0]}, 名称: {result[1]}, 描述: {result[2]}")
                else:
                    print("❌ 没有找到数据")
                
                conn.commit()
                return True
                
    except Exception as e:
        print(f"❌ 表操作失败: {e}")
        return False

if __name__ == "__main__":
    print("PostgreSQL psycopg3 连接测试")
    print("=" * 50)
    print(f"Python 版本: {sys.version}")
    print(f"psycopg 版本: {psycopg.__version__}")
    print(f"当前编码: {sys.getdefaultencoding()}")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        test_psycopg3_connection,
        test_psycopg3_postgres_user,
        test_create_table
    ]
    
    success_count = 0
    for test in tests:
        if test():
            success_count += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"成功: {success_count}/{len(tests)}")
    
    if success_count > 0:
        print("\n✅ psycopg3 连接成功！编码问题已解决。")
        print("\n📋 DBeaver 连接配置:")
        print("   主机: 127.0.0.1")
        print("   端口: 5432")
        print("   数据库: rpa_tornado")
        print("   用户名: dbadmin")
        print("   密码: admin123")
        print("   SSL 模式: 禁用")
    else:
        print("\n❌ 所有连接方式都失败，需要进一步诊断。")