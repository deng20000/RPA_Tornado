from DrissionPage import Chromium
import time

# 定义一个名为xiaomang的类
class xiaomang:
    # 初始化函数，用于初始化浏览器、邮箱和密码
    def __init__(self,browser=Chromium(),email='daniel.chen@gl-inet.com',password='Goodlife0912'):
        # 将传入的浏览器参数赋值给self.browser
        self.browser = browser
        # 将传入的邮箱参数赋值给self.email
        self.email = email
        # 将传入的密码参数赋值给self.password
        self.password = password
    
    # 定义一个名为xiaomang_login的函数
    def xiaomang_login(self):
        # 创建一个Chromium页面对象
        # browser  = self.browser
        tab = self.browser.latest_tab
        # 访问登录页面
        tab.get('https://login.xiaoman.cn/login?')
        # 检验密码登录是否存在
        is_displayed = tab.wait.ele_displayed("@text()=密码登录",timeout=10)
        if is_displayed:
            tab.ele("@text()=密码登录").click()
            # 等待邮箱输入框出现
            tab.wait.ele_displayed("#email")
            # 找到用户名和密码输入框，并输入相应的值
            tab.ele("#email").input("EMAIL")
            tab.ele("#password").input("PASSWORD")
            tab.run_js("document.querySelector(\"input.agree-checkbox\").click()")
            # 点击记住密码
            tab.ele("#remember").click()
            # 点击登录按钮
            tab.ele("@type=submit").click()
            return True
        else:
            print("已经登录无需登录操作")
            return False
    
    # 定义一个是否需要登录函数


# 定义一个名为xiaomang_login的函数
def xiaomang_login():
    # 创建一个Chromium页面对象
    browser  = Chromium()
    tab = browser.latest_tab
    # 访问登录页面
    # tab = browser.latest_tab  # 获取最新标签页对象
    

    # tab
    # tab.get('https://login.xiaoman.cn/login?')
    tab.ele("@text()=密码登录").click()
    # 检验密码登录是否存在
   
    # 打印结果
    # print(bool_res)
    # # 等待邮箱输入框出现
    # tab.wait.ele_displayed("#email")
    # # 找到用户名和密码输入框，并输入相应的值
    # tab.ele("#email").input("daniel.chen@gl-inet.com")
    # tab.ele("#password").input("Goodlife0912")
    # tab.run_js("document.querySelector(\"input.agree-checkbox\").click()")
    # # 点击记住密码
    # tab.ele("#remember").click()
    # # 点击登录按钮   
    # tab.ele("@type=submit").click()

    
# xiaomang_login()