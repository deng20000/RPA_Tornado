from app.ecommerce_dashboard.routes import routes as ecommerce_routes

all_routes = []
all_routes += ecommerce_routes

import tornado.ioloop
import tornado.web

if __name__ == "__main__":
    app = tornado.web.Application(all_routes, debug=True)
    app.listen(8888)
    print("Tornado server started at http://127.0.0.1:8888 (debug mode)")
    tornado.ioloop.IOLoop.current().start() 