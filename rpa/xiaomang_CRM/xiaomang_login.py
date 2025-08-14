import requests
import urllib3
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 可选：关闭 SSL 证书验证警告（不推荐用于生产环境）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class XiaomanCRM:
    def __init__(self):
        self.session = requests.Session()
        self.login_url = 'https://login-api.xiaoman.cn/read/login'
        self.submit_url = 'https://crm.xiaoman.cn/api/leadV2Write/submitLead'

    def login(self):
        headers = {
            'Host': 'login-api.xiaoman.cn',
            'accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'origin': 'https://login.xiaoman.cn',
            'referer': 'https://login.xiaoman.cn/',
        }

        data = {
            'account': 'daniel.chen@gl-inet.com',
            'password': 'defd7d107c79287ce6f64ce002b7f2218403cbf64525819df63055e1a1ca0b24',
            'code': '',
            'is_remember': 'true',
            'return_url': 'https://crm.xiaoman.cn/crm/leads/list?curPage',
            'system_id': 'v5client',
            'need_safe': '0',
        }

        response = self.session.post(self.login_url, headers=headers, data=data, verify=False)
        print("登录返回的cookie:",response.cookies.get_dict())
        print("登录返回信息11:",response.headers)
        
        
        # self.session = requests.Session()
        # if response.status_code == 200:
        print("登录返回信息:",response.json())
        res_code = response.json()['msg']
        if res_code=='success':
            print("✅ 登录成功")
        else:
            raise Exception(f"❌ 登录失败，状态码：{res_code}")

    def submit_data(self, insert_data):
        
        response = self.session.post(self.submit_url, data=insert_data, verify=False)
        print(response.json())
        if response.json()['code'] == 200:
        # if response.status_code == 200:
            print("📨 数据提交成功")
        else:
            print("⚠️ 数据提交失败，状态码：", response.json()['code'],"返回异常信息为：",response.json()['msg'])
            print("返回内容：", response.text)


if __name__ == '__main__':
    payload = {
    'lead_id': '',
    'archive_flag': '1',
    'company_hash_id': '',
    'company_hash_origin': '',
    'data': '{"lead":{"country":"","homepage":"","name":"test1332432","origin_list":"","company_name":"","26847097814254":"","biz_type":"","intention_level":"","annual_procurement":"","timezone":"","ad_keyword":"","address":"","image_list":"","remark":"","inquiry_country":"","ai_status":""},"customers":[{"growth_level":0,"main_customer_flag":1,"name":"test1","email":"","contact":"","tel_list":"","gender":"","post":"","remark":"","image_list":"","47310691380844":"","47311072554476":"","47311219468602":"","47312964436243":""}]}',
    'trail_rebuild': '1',
}

    crm = XiaomanCRM()
    crm.login()
    crm.submit_data(payload)
