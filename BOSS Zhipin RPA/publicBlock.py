from .package import variables as glv
from datetime import datetime
import json

def work_experience(r1: str, r2: list, r3: list):
    k1 = glv["g_简历正文关键字列表"]
    keywords = [kw.strip().upper() for kw in k1]  # 关键词清洗
    rn = (r1 + "".join(r2)).upper()
    
    # 关键词检测
    found_keywords = [kw for kw in keywords if kw in rn]
    keyword_ok = len(found_keywords) >= 1
    if glv["g_工作时间要求"] == "最近两份工作平均每份大于1年":
        # 工作时长检测（新逻辑）
        duration_ok = check_experience(r3)
    elif glv["g_工作时间要求"] == "不限":
        duration_ok = True
    
    # 构建原因说明
    reasons = []
    if not keyword_ok:
        missing = len(keywords) - len(found_keywords)
        reasons.append(f"缺少{missing}个关键点")
    else:
        missing = "存在关键点:" + ",".join(found_keywords)
        reasons.append(missing)
    reasons.append(glv["g_工作时间要求"])
    return ("合适" if keyword_ok and duration_ok else "不合适", "；".join(reasons))

def check_experience(periods):
    if len(periods) < 2:
        return False
    
    # 检查最近两段经历
    for period in periods[:2]:
        if ' - ' not in period:
            return False
        
        start_str, end_str = period.split(' - ')
        try:
            start = parse_date(start_str)
            end = parse_date(end_str)
            months = (end[0] - start[0])*12 + (end[1] - start[1])
            if months < 12:  # 任意一段小于12个月即符合条件
                return False
        except:
            continue
    
    return True  # 最近两段经历都超过1年

def parse_date(s):
    if s == '至今':
        now = datetime.now()
        return (now.year, now.month)
    year, month = map(int, s.split('.'))
    return (year, month)


def file_use(filepath,data):
    # 写入 JSON 文件，确保使用 UTF-8 编码
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    