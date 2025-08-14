#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA Tornado 应用主入口
支持多环境配置、优雅启动和关闭
"""

import os
import sys
import signal
import logging
import socket
import subprocess
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    import tornado.ioloop
    import tornado.web
    import tornado.options
    from tornado.options import define, options
    
    # 导入应用配置和路由
    from app.config import settings
    from app.routes import routes
    
    print(f"✅ 成功导入所有依赖模块")
    
except ImportError as e:
    print(f"❌ 导入模块失败: {e}")
    print("请确保已安装所有依赖: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ 启动异常: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


# 定义命令行选项
define("port", default=settings.APP_PORT, help="运行端口", type=int)
define("host", default=settings.APP_HOST, help="监听地址", type=str)
define("debug", default=settings.APP_DEBUG, help="调试模式", type=bool)
define("environment", default=os.getenv('ENVIRONMENT', 'development'), help="运行环境", type=str)
define("kill_port", default=False, help="启动前自动杀掉占用端口的进程", type=bool)


class Application(tornado.web.Application):
    """自定义应用类"""
    
    def __init__(self, routes, **kwargs):
        # 应用设置
        app_settings = {
            'debug': options.debug,
            'autoreload': settings.DEV_RELOAD and options.debug,
            'serve_traceback': options.debug,
            'compress_response': True,
            'cookie_secret': settings.SECRET_KEY,
            'xsrf_cookies': False,  # 根据需要启用CSRF保护
            'static_path': str(project_root / 'static'),  # 静态文件路径
            'template_path': str(project_root / 'templates'),  # 模板路径
        }
        
        # 合并用户提供的设置
        app_settings.update(kwargs)
        
        super().__init__(routes, **app_settings)
        
        # 初始化应用组件
        self._setup_logging()
        self._setup_signal_handlers()
        
        print(f"🚀 应用初始化完成")
        print(f"   - 环境: {options.environment}")
        print(f"   - 调试模式: {options.debug}")
        print(f"   - 自动重载: {app_settings.get('autoreload', False)}")
    
    def _setup_logging(self):
        """设置日志配置"""
        log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
        
        # 创建日志目录
        log_file_path = Path(settings.LOG_FILE)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 配置日志格式
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # 配置根日志记录器
        logging.basicConfig(
            level=log_level,
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(log_file_path, encoding='utf-8')
            ]
        )
        
        # 设置Tornado日志级别
        tornado.options.options.logging = settings.LOG_LEVEL.lower()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"日志系统初始化完成，级别: {settings.LOG_LEVEL}")
    
    def _setup_signal_handlers(self):
        """设置信号处理器，支持优雅关闭"""
        def signal_handler(signum, frame):
            self.logger.info(f"收到信号 {signum}，准备关闭服务器...")
            tornado.ioloop.IOLoop.current().add_callback_from_signal(self._shutdown)
        
        # 注册信号处理器
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        if hasattr(signal, 'SIGHUP'):
            signal.signal(signal.SIGHUP, signal_handler)
    
    def _shutdown(self):
        """优雅关闭服务器"""
        self.logger.info("开始优雅关闭服务器...")
        
        # 停止接受新连接
        self.server.stop()
        
        # 等待现有连接完成
        deadline = tornado.ioloop.IOLoop.current().time() + 10  # 10秒超时
        
        def stop_loop():
            now = tornado.ioloop.IOLoop.current().time()
            # 检查是否还有活跃连接（兼容不同版本的Tornado）
            has_connections = False
            try:
                has_connections = bool(getattr(self.server, '_connections', None))
            except AttributeError:
                pass
            
            if now < deadline and has_connections:
                tornado.ioloop.IOLoop.current().call_later(0.1, stop_loop)
            else:
                tornado.ioloop.IOLoop.current().stop()
                self.logger.info("服务器已关闭")
        
        stop_loop()


def get_local_ip():
    """动态获取本机局域网IP地址"""
    try:
        # 创建一个UDP socket连接到外部地址来获取本机IP
        # 这里使用8.8.8.8作为目标，但实际不会发送数据
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            return local_ip
    except Exception:
        # 如果获取失败，返回默认值
        return "192.168.x.x"


def check_and_kill_port(port: int) -> bool:
    """检查端口占用并杀掉占用进程
    
    Args:
        port: 要检查的端口号
        
    Returns:
        bool: 是否成功处理端口占用
    """
    try:
        # 使用netstat命令检查端口占用
        result = subprocess.run(
            ['netstat', '-ano'], 
            capture_output=True, 
            text=True, 
            encoding='gbk'
        )
        
        if result.returncode != 0:
            print(f"⚠️  无法检查端口占用状态")
            return False
            
        # 查找占用指定端口的进程
        lines = result.stdout.split('\n')
        for line in lines:
            if f':{port}' in line and 'LISTENING' in line:
                # 提取进程ID
                parts = line.split()
                if len(parts) >= 5:
                    pid = parts[-1]
                    print(f"🔍 发现端口 {port} 被进程 {pid} 占用")
                    
                    # 尝试杀掉进程
                    try:
                        kill_result = subprocess.run(
                            ['taskkill', '/F', '/PID', pid],
                            capture_output=True,
                            text=True,
                            encoding='gbk'
                        )
                        
                        if kill_result.returncode == 0:
                            print(f"✅ 成功终止占用端口 {port} 的进程 {pid}")
                            return True
                        else:
                            print(f"❌ 无法终止进程 {pid}: {kill_result.stderr}")
                            return False
                            
                    except Exception as e:
                        print(f"❌ 终止进程时出错: {e}")
                        return False
        
        # 没有找到占用端口的进程
        print(f"✅ 端口 {port} 未被占用")
        return True
        
    except Exception as e:
        print(f"❌ 检查端口占用时出错: {e}")
        return False


def make_app(**kwargs) -> Application:
    """创建应用实例"""
    return Application(routes, **kwargs)


def print_startup_info():
    """打印启动信息"""
    print("\n" + "="*60)
    print(f"🌟 {settings.APP_NAME} v{settings.APP_VERSION}")
    print("="*60)
    print(f"📍 服务地址: http://{options.host}:{options.port}")
    
    if options.host == '0.0.0.0':
        local_ip = get_local_ip()
        print(f"🌐 局域网访问: http://{local_ip}:{options.port}")
        print(f"🏠 本地访问: http://127.0.0.1:{options.port}")
    
    print(f"🔧 运行环境: {options.environment}")
    print(f"🐛 调试模式: {'开启' if options.debug else '关闭'}")
    
    # 显示可用的API端点
    print(f"\n📋 可用的API端点:")
    print(f"   - 健康检查: http://{options.host}:{options.port}{settings.HEALTH_CHECK_ENDPOINT}")
    print(f"   - API文档: 查看 docs/ 目录下的swagger文件")
    
    print("\n💡 提示:")
    print("   - 按 Ctrl+C 优雅停止服务器")
    print("   - 查看 README.md 了解更多使用说明")
    print("="*60 + "\n")


def add_health_check_route():
    """添加健康检查路由"""
    class HealthCheckHandler(tornado.web.RequestHandler):
        def get(self):
            self.write({
                'status': 'healthy',
                'app': settings.APP_NAME,
                'version': settings.APP_VERSION,
                'environment': options.environment
            })
    
    # 将健康检查路由添加到路由列表
    health_route = (settings.HEALTH_CHECK_ENDPOINT, HealthCheckHandler)
    if health_route not in routes:
        routes.insert(0, health_route)


def main():
    """主函数"""
    try:
        # 解析命令行参数
        tornado.options.parse_command_line()
        
        # 检查端口占用（如果启用了kill_port参数）
        if options.kill_port:
            print(f"🔍 检查端口 {options.port} 占用情况...")
            if not check_and_kill_port(options.port):
                print(f"⚠️  端口 {options.port} 处理失败，但继续尝试启动服务器")
        
        # 初始化数据库连接
        try:
            from app.core.database import init_database, create_tables
            print("🗄️  正在初始化数据库连接...")
            init_database()
            create_tables()
            print("✅ 数据库初始化成功")
        except Exception as e:
            print(f"⚠️  数据库初始化失败: {e}")
            print("📝 应用将继续启动，但电商数据看板功能可能不可用")
        
        # 添加健康检查路由
        add_health_check_route()
        
        # 创建应用实例
        app = make_app()
        
        # 启动服务器
        app.server = app.listen(options.port, address=options.host)
        
        # 打印启动信息
        print_startup_info()
        
        # 启动事件循环
        tornado.ioloop.IOLoop.current().start()
        
    except KeyboardInterrupt:
        print("\n👋 收到中断信号，正在关闭服务器...")
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("🔚 服务器已停止")


if __name__ == "__main__":
    main()

    