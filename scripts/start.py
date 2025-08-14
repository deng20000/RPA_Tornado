#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用启动脚本
提供不同环境的启动选项
"""

import os
import sys
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def setup_environment(env_name):
    """设置环境变量"""
    os.environ['ENVIRONMENT'] = env_name
    
    # 根据环境设置不同的配置
    if env_name == 'development':
        os.environ.setdefault('APP_DEBUG', 'true')
        os.environ.setdefault('APP_PORT', '8888')
        os.environ.setdefault('LOG_LEVEL', 'DEBUG')
    elif env_name == 'production':
        os.environ.setdefault('APP_DEBUG', 'false')
        os.environ.setdefault('APP_PORT', '80')
        os.environ.setdefault('LOG_LEVEL', 'INFO')
    elif env_name == 'testing':
        os.environ.setdefault('APP_DEBUG', 'true')
        os.environ.setdefault('APP_PORT', '8889')
        os.environ.setdefault('LOG_LEVEL', 'DEBUG')


def start_server(env, port=None, host=None, debug=None):
    """启动服务器"""
    setup_environment(env)
    
    # 构建启动命令参数
    cmd_args = []
    
    if port:
        cmd_args.extend(['--port', str(port)])
    if host:
        cmd_args.extend(['--host', host])
    if debug is not None:
        cmd_args.extend(['--debug', str(debug).lower()])
    
    # 设置命令行参数
    sys.argv.extend(cmd_args)
    
    print(f"🚀 启动 {env} 环境服务器...")
    
    # 导入并启动主应用
    from main import main
    main()


def main():
    parser = argparse.ArgumentParser(description='RPA Tornado 应用启动脚本')
    parser.add_argument(
        '--env', 
        choices=['development', 'production', 'testing'],
        default='development',
        help='运行环境 (默认: development)'
    )
    parser.add_argument(
        '--port', 
        type=int,
        help='服务端口'
    )
    parser.add_argument(
        '--host', 
        default='0.0.0.0',
        help='监听地址 (默认: 0.0.0.0)'
    )
    parser.add_argument(
        '--debug', 
        action='store_true',
        help='启用调试模式'
    )
    parser.add_argument(
        '--no-debug', 
        action='store_true',
        help='禁用调试模式'
    )
    
    args = parser.parse_args()
    
    # 处理调试模式参数
    debug = None
    if args.debug:
        debug = True
    elif args.no_debug:
        debug = False
    
    try:
        start_server(
            env=args.env,
            port=args.port,
            host=args.host,
            debug=debug
        )
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()