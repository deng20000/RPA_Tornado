# 使用提醒:
# 1. xbot包提供软件自动化、数据表格、Excel、日志、AI等功能
# 2. package包提供访问当前应用数据的功能，如获取元素、访问全局变量、获取资源文件等功能
# 3. 当此模块作为流程独立运行时执行main函数
# 4. 可视化流程中可以通过"调用模块"的指令使用此模块

import xbot
from xbot import print, sleep
from .import package
from .package import variables as glv
import requests
import json
import sys
def main(args):
    # # API 基础 URL
    
    resume = glv["g_未过滤简历"]
    # 动态改变
    jd = glv["g_岗位要求"]

     # 先格式化简历
    formatted_resume = call_coze_api(resume)
    if not formatted_resume:
        return                                                                          
    print(formatted_resume) 
    score_result = call_api(formatted_resume, jd)
    print(score_result)
    final_result = chat_with_agent(str(score_result))
    print(final_result)
    return final_result

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def call_api(resume, jd):
    """调用简历匹配API"""
    # API 基础 URL
    base_url = "http://8.129.18.122:8888/resume-matcher"
    api_url = f"{base_url}"
    headers = {"Content-Type": "application/json"}
    data = {"resume": resume, "jd": jd}
    response = requests.post(api_url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"API 调用失败，状态码: {response.status_code}")
        return None

def call_coze_api(resume):
    """格式化简历"""
    headers = {
        # Bearer pat_FD1G0p5WXAnFJpR7T5mbY9PLamZYar92xwBC0Ne5oOuSTP0jz2wovKhNnYu5t2lk
        'Authorization': 'Bearer pat_oHquPE1uc8DYL3117YeG2R7tQQ75wjkXsXwz5Wj8kt18ZwO2H0AJO3wEdCdbvf6H',
        'Content-Type': 'application/json',
    }
    json_data = {
        'parameters': {'USER_INPUT': resume},
        'bot_id': '7486755604041039935',
        'is_async': False,
        'workflow_id': '7486816386658271247',
    }
    response = requests.post('https://api.coze.cn/v1/workflow/run', headers=headers, json=json_data)
    print(response)
    if response.status_code == 200:
        response_data = response.json().get("data")
        if response_data:
            try:
                # 将data字段从字符串解析为JSON
                parsed_data = json.loads(response_data)
                # 获取实际的内容数据并返回
                return parsed_data.get("data")
            except json.JSONDecodeError as e:
                print(f"解析data字段失败: {str(e)}")
                return None
        else:
            print("未获取到有效data字段")
            return None
    else:
        print(f"简历格式化失败，状态码: {response.status_code}")
        return None

def chat_with_agent(user_input):
    """简历评分格式化助手"""
    headers = {
        'Authorization': 'Bearer pat_oHquPE1uc8DYL3117YeG2R7tQQ75wjkXsXwz5Wj8kt18ZwO2H0AJO3wEdCdbvf6H',
        'Content-Type': 'application/json',
    }
    
    # 确保user_input是字符串，并且格式化为JSON格式
    try:
        if isinstance(user_input, dict):
            user_input = json.dumps(user_input, ensure_ascii=False)
    except Exception as e:
        print(f"输入数据格式化失败: {str(e)}")
        return None

    json_data = {
        'parameters': {'input': user_input},
        'bot_id': '7487773939247595546',
        'is_async': False,
        'workflow_id': '7487867212624035878',
    }
    
    try:
        response = requests.post('https://api.coze.cn/v1/workflow/run', headers=headers, json=json_data)
        response.raise_for_status()  # 检查HTTP错误
        response_data = response.json().get("data")
        
        if response_data:
            try:
                parsed_data = json.loads(response_data)
                return parsed_data.get("data")
            except json.JSONDecodeError as e:
                print(f"解析data字段失败: {str(e)}")
                print(f"原始data字段内容: {response_data}")
                return None
        else:
            print("未获取到有效data字段")
            print(f"完整API响应: {response.json()}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {str(e)}")
        return None

# print(call_coze_api('''曹园园 刚刚活跃 26岁4年本科在职-考虑机会 期望： 深圳产品认证工程师 优势： 本人性格开朗，乐观向上，爱好广泛，在参与第一次暑期实践时，我们小组在我的带领下取得不错的业绩，我拥有较强的组织能力和适应能力，在某一次工作实践期间即将面临月末工作指标不足时，我们小组的良好的心态和责任感使得在最后天挽狂澜，业绩满额达标。吃苦耐劳，擅于管理，勇于面对挑战。 认证 认证需求 认证方案 测试进度 证书签发 测试安排 报告审核 光伏组件 测试完成 测试情况本人性格开朗，乐观向上，爱好广泛，在参与第一次暑期实践时，我们小组在我的带领下取得不错的业绩，我拥有较强的组织能力和适应能力，在某一次工作实践期间即将面临月末工作指标不足时，我们小组的良好的心态和责任感使得在最后天挽狂澜，业绩满额达标。吃苦耐劳，擅于管理，勇于面对挑战。期望职位 深圳产品认证工程师行业不限14-15K岗位经验 产品认证工程师 3年10个月工作经历 华立科技股份有限公司 认证专员 2024.03 - 至今 负责公司海外事业部认证需求的评估送测 东方日升新能源股份有限公司 产品认证工程师 2021.07 - 2024.03 1.认证方案：依据认证需求规划，明确责任、关键项目和时间，负责公司所分配认证项目的规划和推进事宜。 2.目击测试：负责组件认证测试跟进，追踪现场目击测试情况，按标准要求完成所需测试。 3.报告撰写及审核：根据实验室提供的原始数据，按时完成目击报告的撰写及审核。 4.流程跟进：参与项目认证完成全流程，包括不限于样品送测、测试安排、测试进度、测试完成、报告审核、证书签发。 5.领导安排的其他工作事项项目经历 Practice 负责光伏组件多个国际认证诸如澳洲CEC、巴西Inmetro、英国MCS、沙特SASO、马来西亚MyHijau、韩国KS等等项目的跟进，积极推动公司战略发展。 负责基础认证项目，如期完成相应报告审核及组件认证测试项目签发，为公司销售订单提供有效助力。 负责公司韩国KS对外前期审核资料准备及曾全程作为审核翻译，负责基地生产流程讲解，保证审核顺利完成。项目经验 欧洲MID认证认证项目经理 2024.03 - 至今 负责认证资料的收集准备 对内对接研发，对外沟通机构 认证项目负责人 2021.07 - 至今 独立负责光伏组件多个海外认证诸如澳洲 CEC 、巴西 Inmetro 、英国 MCS、沙特 SASO、UL 等等项目的跟进，积极推动公司战略发展。 仪器仪表行业电表产品海外认证工作包括不限于认证、审厂教育经历 南昌航空大学 科技英语 本科 2017 - 2021 省部共建 在校经历： 一年的干事'''))