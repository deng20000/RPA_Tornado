import json
from collections import defaultdict
from datetime import datetime, timedelta

def extract_and_optimize(input_data_path, allfields_path, need_data_path, output_path):
    """
    读取原始数据、字段定义和需求字段，按规则输出优化结构。
    每个ID对应一条钉钉数据，并且只处理昨天月份的数据。
    
    :param input_data_path: 原始数据json路径
    :param allfields_path: 字段定义json路径
    :param need_data_path: 需求字段json路径
    :param output_path: 输出文件路径
    """
    # 获取昨天的月份字符串（如2025.06）
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_month = yesterday.strftime('%Y.%m')
    
    # 1. 读取原始数据和配置
    with open(input_data_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    with open(allfields_path, 'r', encoding='utf-8') as f:
        allfields = json.load(f)[0]  # 取第一个表头定义

    with open(need_data_path, 'r', encoding='utf-8') as f:
        need_data = json.load(f)

    # 2. 构建字段名到ID的映射，便于后续查找
    field_name_to_id = {field['name']: field['id'] for field in allfields}

    # 3. 渠道名到平台名的映射（与need_data.json保持一致）
    platform_map = {
        'FB': 'Facebook',
        'IG': 'Instagram',
        'Youtube': 'YouTube',
        'LinkedIn': 'LinkedIn',
        'X': 'X',
        'Tiktok': 'Tiktok'
    }

    # 4. 获取昨天的月份字符串（如2024.06）
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_month = yesterday.strftime('%Y.%m')

    # 5. 生成输出结构
    total_result = {}
    for platform_key in need_data:
        # 只处理need_data中定义的平台
        # 1. 字段名到字段id的映射（key不加_id）
        field_id_map = {}
        for field in need_data[platform_key]:
            field_id_map[field] = field_name_to_id.get(field, "")
        # 时间和社媒账号字段id
        field_id_map["时间"] = field_name_to_id.get("时间", "")
        field_id_map["社媒账号"] = field_name_to_id.get("社媒账号", "")

        # 2. 按ID组织数据
        data_by_id = {}
        for item in raw_data:
            fields = item.get('fields', {})
            # 检查时间是否匹配昨天的月份
            time_field = fields.get('时间', {})
            if isinstance(time_field, dict):
                item_month = time_field.get('name', '')
            else:
                item_month = time_field
            if item_month != yesterday_month:
                continue

            channel_info = fields.get('渠道', {})
            channel_name = channel_info.get('name', '')
            platform = platform_map.get(channel_name, None)
            if platform != platform_key:
                continue

            item_id = item.get('id', '')
            if not item_id:
                continue

            record = {}
            for field in need_data[platform_key]:
                value = ''
                field_data = fields.get(field, '')
                if isinstance(field_data, dict):
                    value = field_data.get('name', '')
                else:
                    value = field_data
                record[field] = value
            # 添加基础字段
            record['时间'] = yesterday_month
            record['社媒账号'] = fields.get('社媒账号', '')
            record['id'] = item_id
            # 将数据添加到以ID为键的字典中
            data_by_id[item_id] = record

        # 将数据按社媒账号分组
        account_data = {}
        for item_id, record in data_by_id.items():
            account_name = record['社媒账号']
            if account_name not in account_data:
                account_data[account_name] = record

        # 合成平台结构为数组形式
        total_result[platform_key] = [
            field_id_map,  # 第一个元素是字段映射
            account_data   # 第二个元素是按社媒账号分组的数据
        ]
    
    print(f"处理完成，共提取 {len(total_result)} 个平台的数据。")
    # 6. 输出为新文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(total_result, f, ensure_ascii=False, indent=2)

    print(f"数据提取完成，结果已保存为 {output_path}")


# 示例调用
if __name__ == "__main__":
    extract_and_optimize(
        input_data_path='dingding_data.json',
        allfields_path='dingding_allfields.json',
        need_data_path='need_data.json',
        output_path='optimized_data_structure_update_filled.json'
    )
    # # 提取id和内容
    # id_list, data_list = extract_id_and_data_from_file(
    #     'optimized_data_structure_update_filled.json',
    #     platform='Facebook'  # 可换成Instagram、X等
    # # )
    # print("ID列表：", id_list)
    # print("字段数据列表：", data_list)