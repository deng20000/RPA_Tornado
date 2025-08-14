import requests

cookies = {
    # 'hasIMClient': '0',
    # 'sajssdk_2015_cross_new_user': '1',
    # 'platform_version': '19.0.0',
    # 'fingerprint_time': '1750214503906',
    # 'fingerprint_version': '3.3.3',
    # 'fingerprint': 'T2gAPg11FWwHNUdnwVSajJw0hootM6jQQEr9WzMcRL19rNHeDVBFdNYD5KtQSI4nf2Q%3D',
    # 'set_id': '13200',
    # 'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2256521961%22%2C%22first_id%22%3A%2219780e99bcf1bb0-0fc632b55794af-26011e51-1821369-19780e99bd022e1%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3ODBlOTliY2YxYmIwLTBmYzYzMmI1NTc5NGFmLTI2MDExZTUxLTE4MjEzNjktMTk3ODBlOTliZDAyMmUxIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiNTY1MjE5NjEifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2256521961%22%7D%2C%22%24device_id%22%3A%2219780e99bcf1bb0-0fc632b55794af-26011e51-1821369-19780e99bd022e1%22%7D',
    # 'Hm_lvt_925e072f764b8f193431ee7c9099e6f5': '1750214536',
    # 'HMACCOUNT': 'EF9684A43BDDE7C9',
    # 'Hm_lvt_70f5e1eeec2ad1e9ad4430afacfe1d29': '1750214536',
    # 'SENTRY_MAJOR_CUSTOMER': 'false',
    # 'perf_dv6Tr4n': '1',
    # 'man-machine-token': '140%23y3uo9FDozzP8ZQo2%2BbOF4pN8s9zGgdCwFv0ie6S%2FUh%2B5NZKkuq5HMlV2zc0eCHij4Fhhlp1zzXBiSLzozbzxVKDza3h%2Fzzrb22U3lp1xzA1iVXE%2FtFzx2Dc33z%2F%2FEHmijDapVrMn79%2FQCGKQA44d%2FQ72lQpGncnlAH7CFZW0NuzdgIgy3szi9ypStuODa%2B5KTwud%2FXeb1GtLBVdToKZ5nBTJHLRhJmQKsYM%2F48tegFlJiFCW6LTLCLDTROIIgRrEgbzk36zxCbSs5paE%2FzhclZgoZGkGjOwL5mi7CGy1p9J6D7NOWVbnIf4GdPfSULXhEWaJYyXQMAwBWtTUsM%2FEeFZvwuEZTVENhAzcUTKT3MmjFepuqnVUrjgpeq4XlBxefxN28dRA66az5iS1COpFVNwUizVtuhrtJN7C%2BOp0zY%2FO%2F6wsadencca8desIm9wuYIVGOGAl41WqmlQYJxTTLYjVGE8NjopepwYyxvcVAP7UO8OF8rCf6KjCRv9gqCyWUQhjiwFjx6aiYi7KI%2BOfHXXHPb2GAbW0sdsvKvXE5S4mSRd7mikX9XQma3%2FtIMeD%2FQNy%2F%2BR%2BrZ%2FFICPRI6WkYPmZEc6amajSig3YKhAO95fXg565%2BTRbqclv4L%2BkK5PdZWAz%2FmzUQwGVoY6XW%2B5fG6bU8PAvP32rCgmHeEnEcr3UQwQb0qI5lxW%2FKaDtzR%2Fwv80SewliZzcVpnUV%2FiIyhpsDAsPW%2F7c4Ie5YbtJwlt4jyPcTHrEvIzWBV86UASEbL37sNSwjwczLgBjiyJzbWQBxsYgyKn8v5vt27x%2FT%2B7Tn7zhPlY1Fk7AAbURict5ZEIzBrPSZfOwXnb2A3R3eW6dtEK3paciv46E5Ez8RB%2FPvV8zRqHBkNWQ5ou0mpMlk%2FcVV7VJfSePkAJ4lbZvxg%2F9euivxgGDZixj1S2JVzsMAlS6JIZFsc04ldOE1EPBNWCOHvj5a68TL2mt5YST4b8x5PklYfG5orqY0qFNoq4NcF3%2BjTDrajWPlBkaRm%2FPhzQ%3D%3D',
    'pskey': 'abcd1b7b469221039bbeb7413f2ae6f9fb36087cb46175454e75fb3f5980c352',
    'account': 'daniel.chen%40gl-inet.com',
    'clientId': '360408',
    'userId': '56521961',
    'pskey_exist': '1',
    'authToken': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODE3NTM1OTEsImRhdGEiOnsiY2xpZW50SWQiOjM2MDQwOCwidXNlcklkIjo1NjUyMTk2MX19.DZkHFu0STo86ZvA0TfbAddHeeHqVKIfrAPQ6KYCTbAM',
    'tfstk': 'g8I-BdmuDSVkmIjJnTzmtH8kA2y0srXPr_WsxBAoRsCAgs5lE9XIdkChgU2PK9OdJI1XZ_blKY7VsOilqz-nv3-eA5VgjlvlUH-QPyR_qbkXCdZnA49W4ng8ZjU8jlXPF4U227rGxEAfUQABAUTBhmO2L4tBR4wvGppZRb1CO-dXQL9SVQgWhxO2dHOCOHwAhIJpABGD6JAj8BidSmOBy9VBIDiCDLLboTAfFTeHEUd1FIF_1iKByC6WMDNWuEjk9IS_irBVOa1k36ETMh_NMML6vuhweZ69cQx_WqKRn_S9VGF-qKYpwZsWkviBcnAdswC8w4R5rsLwhEMLbKfMGTS5kJlfF1AJVKT0fRBXRZjy7gVj2h_NE3bC1S0kNNpC4LjGXdmxsCpnP-ex828W3oasfSxrwPqvHC28-2ueoP9vs-Hr82879KdgnM0E8E3O.',
    # 'acw_tc': '0a27773317502188151038618e6252b12b0fca0b1f4efbe2a5abf5772629c1',
    # 'Hm_lpvt_70f5e1eeec2ad1e9ad4430afacfe1d29': '1750218905',
    # 'Hm_lpvt_925e072f764b8f193431ee7c9099e6f5': '1750218905',
    # 'TAB_ONLY_TIMER_FETCH_USER_UUID': '12673e8f',
    # 'socket-alive': '{%22status%22:%221%22%2C%22user_id%22:%2256521961%22}',
    # 'socket-uuid': '7f2df22d',
    # 'socket-self-checking-timestamp': '1750218923373',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    # 'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'b3': '7f14e0256cd73b35df2a6059c5a051d7-44f77cb041af5700-1',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://crm.xiaoman.cn',
    # 'priority': 'u=1, i',
    'referer': 'https://crm.xiaoman.cn/crm/leads/list?curPage=1&pageSize=20&show_all=1&user_num=%5B1%5D&user_id=%5B%5D&filter=%7B%22user_num%22%3A%5B1%5D%2C%22show_all%22%3A1%7D&filters=%7B%22keyword%22%3A%22%22%2C%22show_all%22%3A1%2C%22search_field%22%3A%22%22%7D&keyword=&search_field=',
    # 'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin',
    # 'traceparent': '00-7f14e0256cd73b35df2a6059c5a051d7-44f77cb041af5700-01',
    # 'uber-trace-id': '7f14e0256cd73b35df2a6059c5a051d7:44f77cb041af5700:0:1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    # 'x-b3-spanid': '44f77cb041af5700',
    # 'x-b3-traceid': '7f14e0256cd73b35df2a6059c5a051d7',
    # 'cookie': 'hasIMClient=0; sajssdk_2015_cross_new_user=1; platform_version=19.0.0; fingerprint_time=1750214503906; fingerprint_version=3.3.3; fingerprint=T2gAPg11FWwHNUdnwVSajJw0hootM6jQQEr9WzMcRL19rNHeDVBFdNYD5KtQSI4nf2Q%3D; set_id=13200; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2256521961%22%2C%22first_id%22%3A%2219780e99bcf1bb0-0fc632b55794af-26011e51-1821369-19780e99bd022e1%22%2C%22props%22%3A%7B%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3ODBlOTliY2YxYmIwLTBmYzYzMmI1NTc5NGFmLTI2MDExZTUxLTE4MjEzNjktMTk3ODBlOTliZDAyMmUxIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiNTY1MjE5NjEifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2256521961%22%7D%2C%22%24device_id%22%3A%2219780e99bcf1bb0-0fc632b55794af-26011e51-1821369-19780e99bd022e1%22%7D; Hm_lvt_925e072f764b8f193431ee7c9099e6f5=1750214536; HMACCOUNT=EF9684A43BDDE7C9; Hm_lvt_70f5e1eeec2ad1e9ad4430afacfe1d29=1750214536; SENTRY_MAJOR_CUSTOMER=false; perf_dv6Tr4n=1; man-machine-token=140%23y3uo9FDozzP8ZQo2%2BbOF4pN8s9zGgdCwFv0ie6S%2FUh%2B5NZKkuq5HMlV2zc0eCHij4Fhhlp1zzXBiSLzozbzxVKDza3h%2Fzzrb22U3lp1xzA1iVXE%2FtFzx2Dc33z%2F%2FEHmijDapVrMn79%2FQCGKQA44d%2FQ72lQpGncnlAH7CFZW0NuzdgIgy3szi9ypStuODa%2B5KTwud%2FXeb1GtLBVdToKZ5nBTJHLRhJmQKsYM%2F48tegFlJiFCW6LTLCLDTROIIgRrEgbzk36zxCbSs5paE%2FzhclZgoZGkGjOwL5mi7CGy1p9J6D7NOWVbnIf4GdPfSULXhEWaJYyXQMAwBWtTUsM%2FEeFZvwuEZTVENhAzcUTKT3MmjFepuqnVUrjgpeq4XlBxefxN28dRA66az5iS1COpFVNwUizVtuhrtJN7C%2BOp0zY%2FO%2F6wsadencca8desIm9wuYIVGOGAl41WqmlQYJxTTLYjVGE8NjopepwYyxvcVAP7UO8OF8rCf6KjCRv9gqCyWUQhjiwFjx6aiYi7KI%2BOfHXXHPb2GAbW0sdsvKvXE5S4mSRd7mikX9XQma3%2FtIMeD%2FQNy%2F%2BR%2BrZ%2FFICPRI6WkYPmZEc6amajSig3YKhAO95fXg565%2BTRbqclv4L%2BkK5PdZWAz%2FmzUQwGVoY6XW%2B5fG6bU8PAvP32rCgmHeEnEcr3UQwQb0qI5lxW%2FKaDtzR%2Fwv80SewliZzcVpnUV%2FiIyhpsDAsPW%2F7c4Ie5YbtJwlt4jyPcTHrEvIzWBV86UASEbL37sNSwjwczLgBjiyJzbWQBxsYgyKn8v5vt27x%2FT%2B7Tn7zhPlY1Fk7AAbURict5ZEIzBrPSZfOwXnb2A3R3eW6dtEK3paciv46E5Ez8RB%2FPvV8zRqHBkNWQ5ou0mpMlk%2FcVV7VJfSePkAJ4lbZvxg%2F9euivxgGDZixj1S2JVzsMAlS6JIZFsc04ldOE1EPBNWCOHvj5a68TL2mt5YST4b8x5PklYfG5orqY0qFNoq4NcF3%2BjTDrajWPlBkaRm%2FPhzQ%3D%3D; pskey=abcd1b7b469221039bbeb7413f2ae6f9fb36087cb46175454e75fb3f5980c352; account=daniel.chen%40gl-inet.com; clientId=360408; userId=56521961; pskey_exist=1; authToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODE3NTM1OTEsImRhdGEiOnsiY2xpZW50SWQiOjM2MDQwOCwidXNlcklkIjo1NjUyMTk2MX19.DZkHFu0STo86ZvA0TfbAddHeeHqVKIfrAPQ6KYCTbAM; tfstk=g8I-BdmuDSVkmIjJnTzmtH8kA2y0srXPr_WsxBAoRsCAgs5lE9XIdkChgU2PK9OdJI1XZ_blKY7VsOilqz-nv3-eA5VgjlvlUH-QPyR_qbkXCdZnA49W4ng8ZjU8jlXPF4U227rGxEAfUQABAUTBhmO2L4tBR4wvGppZRb1CO-dXQL9SVQgWhxO2dHOCOHwAhIJpABGD6JAj8BidSmOBy9VBIDiCDLLboTAfFTeHEUd1FIF_1iKByC6WMDNWuEjk9IS_irBVOa1k36ETMh_NMML6vuhweZ69cQx_WqKRn_S9VGF-qKYpwZsWkviBcnAdswC8w4R5rsLwhEMLbKfMGTS5kJlfF1AJVKT0fRBXRZjy7gVj2h_NE3bC1S0kNNpC4LjGXdmxsCpnP-ex828W3oasfSxrwPqvHC28-2ueoP9vs-Hr82879KdgnM0E8E3O.; acw_tc=0a27773317502188151038618e6252b12b0fca0b1f4efbe2a5abf5772629c1; Hm_lpvt_70f5e1eeec2ad1e9ad4430afacfe1d29=1750218905; Hm_lpvt_925e072f764b8f193431ee7c9099e6f5=1750218905; TAB_ONLY_TIMER_FETCH_USER_UUID=12673e8f; socket-alive={%22status%22:%221%22%2C%22user_id%22:%2256521961%22}; socket-uuid=7f2df22d; socket-self-checking-timestamp=1750218923373',
}

data = {
    'lead_id': '',
    'archive_flag': '1',
    'company_hash_id': '',
    'company_hash_origin': '',
    'data': '{"lead":{"country":"","homepage":"","name":"test1","origin_list":"","company_name":"","26847097814254":"","biz_type":"","intention_level":"","annual_procurement":"","timezone":"","ad_keyword":"","address":"","image_list":"","remark":"","inquiry_country":"","ai_status":""},"customers":[{"growth_level":0,"main_customer_flag":1,"name":"test1","email":"","contact":"","tel_list":"","gender":"","post":"","remark":"","image_list":"","47310691380844":"","47311072554476":"","47311219468602":"","47312964436243":""}]}',
    'trail_rebuild': '1',
}

response = requests.post('https://crm.xiaoman.cn/api/leadV2Write/submitLead', cookies=cookies, headers=headers, data=data)
print(response.status_code)

