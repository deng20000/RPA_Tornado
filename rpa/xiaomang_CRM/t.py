import requests
import urllib3
import sys
sys.stdout.reconfigure(encoding='utf-8')
# 屏蔽 InsecureRequestWarning（仅开发环境）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class XiaomanCRM:
    def __init__(self):
        self.session = requests.Session()
        # 公共 headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json, text/plain, */*',
        })
        self.login_url = 'https://login-api.xiaoman.cn/read/login'
        self.submit_url = 'https://crm.xiaoman.cn/api/leadV2Write/submitLead'

    def login(self):
        payload = {
            'account': 'daniel.chen@gl-inet.com',
            'password': 'defd7d107c79287ce6f64ce002b7f2218403cbf64525819df63055e1a1ca0b24',
            'code': '',
            'is_remember': 'true',
            'return_url': 'https://crm.xiaoman.cn/crm/leads/list?curPage',
            'system_id': 'v5client',
            'need_safe': '0',
        }
        resp = self.session.post(self.login_url, data=payload, verify=False)
        resp.raise_for_status()
        result = resp.json()
        res_code = resp.json()['msg']
        # 登录判定：code==20000 表示成功
        if res_code == "success":
            print("✅ 登录成功")
            # 把 authToken 放到 Authorization header
            print(self.session.cookies)
            token = self.session.cookies.get('authToken')
            if token:
                self.session.headers.update({'Authorization': f'Bearer {token}'})
        else:
            raise RuntimeError(f"❌ 登录失败: {result}")

    def submit_data(self, insert_data: dict):
        resp = self.session.post(self.submit_url, data=insert_data, verify=False)
        resp.raise_for_status()
        result = resp.json()
        # 提交判定：同样用 code==20000
        if result.get('code') == 20000:
            print("📨 数据提交成功")
        else:
            raise RuntimeError(f"⚠️ 数据提交失败: {result}")

if __name__ == '__main__':
    # 你的线索 payload：只要把 data 字段里的 JSON 填好即可
    payload = {
        'lead_id': '',
        'archive_flag': '1',
        'company_hash_id': '',
        'company_hash_origin': '',
        'data': '{"lead":{"name":"测试线索","origin_list":"官网表单","company_name":"测试公司","country":"中国","biz_type":"科技","intention_level":"A"},"customers":[{"name":"联系人小明","main_customer_flag":1,"email":"xiaoming@example.com"}]}',
        'trail_rebuild': '1',
    }

    crm = XiaomanCRM()
    crm.login()
    crm.submit_data(payload)
