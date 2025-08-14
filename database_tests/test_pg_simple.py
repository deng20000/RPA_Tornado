#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的 PostgreSQL 连接测试
尝试不同的连接方式和编码设置
"""

import psycopg2
import os
import sys

def test_connection_with_encoding():
    """测试带有明确编码设置的连接"""
    print("=== 测试 1: 基本连接 ===")
    try:
        # 设置环境变量
        os.environ['PGCLIENTENCODING'] = 'UTF8'
        
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=5432,
            database="rpa_tornado",
            user="dbadmin",
            password="admin123"
        )
        
        # 设置连接编码
        conn.set_client_encoding('UTF8')
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print(f"✅ 连接成功! PostgreSQL 版本: {result[0][:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_connection_with_trust():
    """测试使用 trust 认证的连接"""
    print("\n=== 测试 2: 使用 postgres 用户 ===")
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=5432,
            database="postgres",
            user="postgres",
            password="postgres"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT current_database(), current_user;")
        result = cursor.fetchone()
        print(f"✅ 连接成功! 数据库: {result[0]}, 用户: {result[1]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False

def test_connection_without_password():
    """测试不使用密码的连接（trust 模式）"""
    print("\n=== 测试 3: Trust 模式连接 ===")
    try:
        conn = psycopg2.connect(
            host="127.0.0.1",
            port=5432,
            database="rpa_tornado",
            user="dbadmin"
            # 不提供密码，依赖 trust 认证
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT current_database(), current_user;")
        result = cursor.fetchone()
        print(f"✅ Trust 连接成功! 数据库: {result[0]}, 用户: {result[1]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Trust 连接失败: {e}")
        return False

if __name__ == "__main__":
    print("PostgreSQL 连接测试")
    print("=" * 50)
    print(f"Python 版本: {sys.version}")
    print(f"psycopg2 版本: {psycopg2.__version__}")
    print(f"当前编码: {sys.getdefaultencoding()}")
    print("=" * 50)
    
    # 运行所有测试
    tests = [
        test_connection_with_encoding,
        test_connection_with_trust,
        test_connection_without_password
    ]
    
    success_count = 0
    for test in tests:
        if test():
            success_count += 1
    
    print(f"\n=== 测试结果 ===")
    print(f"成功: {success_count}/{len(tests)}")
    
    if success_count > 0:
        print("\n✅ 至少有一种连接方式成功，PostgreSQL 配置正常！")
        print("现在可以尝试在 DBeaver 中使用相同的连接参数。")
    else:
        print("\n❌ 所有连接方式都失败，需要进一步诊断。")