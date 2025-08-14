import json
import re

# 读取数据
with open('optimized_data_structure_update.json', 'r', encoding='utf-8') as f:
    opt_data = json.load(f)
with open('fetch_inf_update.json', 'r', encoding='utf-8') as f:
    fb_data = json.load(f)['response']

# 找到 GL.iNet+FB 记录
for rec_id, rec in opt_data['records'].items():
    info = rec['basic_info']
    if info['time'] == '2025.07' and info['social_account'] == 'GL.iNet' and info['channel'] == 'FB':
        target_rec = rec
        break

# 获取全局字段映射
fields_mapping = opt_data.get('fields_mapping', {})
reverse_mapping = {v: k for k, v in fields_mapping.items()}

# 自动匹配 fetch_inf 字段到 available_fields
# 规则：去掉fb-前缀、下划线、特殊符号，做模糊匹配

def normalize(s):
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

# 预处理 fetch_inf key 映射
fb_key_map = {}
for k in fb_data.keys():
    norm = normalize(k)
    fb_key_map[norm] = k

# 写入数据（只保留 available_fields 中的字段）
result_data = {}
for fid, fname in target_rec['available_fields'].items():
    norm_name = normalize(fname)
    match_key = None
    for norm_k, orig_k in fb_key_map.items():
        if norm_name in norm_k or norm_k in norm_name:
            match_key = orig_k
            break
    if match_key:
        v = fb_data[match_key]
        # 只写 available_fields 里的字段
        if isinstance(v, dict):
            if 'count' in v:
                result_data[fname] = v['count']
            elif 'list' in v:
                result_data[fname] = v['list']
            elif 'graphData' in v:
                result_data[fname] = v['graphData']
            elif 'overview' in v:
                result_data[fname] = v['overview']
            else:
                result_data[fname] = v
        elif isinstance(v, list):
            result_data[fname] = v
        else:
            result_data[fname] = v
    else:
        result_data[fname] = None

# 写入到目标记录
target_rec['data'] = result_data

# 保存
with open('optimized_data_structure_update_filled.json', 'w', encoding='utf-8') as f:
    json.dump(opt_data, f, ensure_ascii=False, indent=2)

print('字段优化写入完成，已生成 optimized_data_structure_update_filled.json') 