# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块

import xbot
from xbot import print, sleep
from .import package
from .package import variables as glv
import os
from collections import Counter
def main(args):
    emails = [
        "peggie.wang@gl-inet.com",
        "kiki.gong@gl-inet.com",
        "raya.ren@gl-inet.com",
        # "stella@gl-inet.com"
    ]

    # 用绝对路径，保证每次都用同一个文件
    index_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "current_email.txt")

    # 读取上次索引，异常时归零
    try:
        if os.path.exists(index_file):
            with open(index_file, "r") as f:
                idx = int(f.read().strip())
        else:
            idx = 0
    except Exception:
        idx = 0

    # 选当前邮箱
    current_email = emails[idx % len(emails)]
    print(f"本次使用邮箱（第{idx % len(emails) + 1}个）：{current_email}")

    # 更新索引
    with open(index_file, "w") as f:
        f.write(str((idx + 1) % len(emails)))
    return current_email
# print(main(""))

def recordemail(emali_list):
    # emails = Counter([])
    result = "业务人员邮箱（用于线索分配以及邮件转发）为："
    for x,y in Counter(emali_list).items():
        result = result+ x +",条数为:" + str(y)+"/n"
    return result
    # return Counter(emali_list)