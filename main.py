try:
    print("main.py start")
    import tornado.ioloop
    import tornado.web
    print("before import routes")
    from app.routes import routes
    print("after import routes")

    def make_app():
        """创建 Tornado 应用实例，供测试和生产使用"""
        return tornado.web.Application(routes, debug=True)

    if __name__ == "__main__":
        app = make_app()
        app.listen(8888)
        print("Tornado server started at http://127.0.0.1:8888 (debug mode)")
        tornado.ioloop.IOLoop.current().start()
except Exception as e:
    print("启动异常：", e)
    import traceback; traceback.print_exc() 

    