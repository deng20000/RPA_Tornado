import json

def fill_value_to_json(json_path, platform, shop, field, value):
    """
    在指定json文件中，按平台、店铺、字段填充值，默认覆盖原文件。
    仅当value为非空字符串时才填充，否则返回False。
    """
    print(f"输入参数：平台={platform}，店铺={shop}，字段={field}，值={value}")

    # 只允许填充非空字符串
    if not isinstance(value, str) or value.strip() == "":
        print("填充值必须为非空字符串，不进行填充。")
        return False

    # 读取json
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 定位到目标
    if platform not in data:
        print(f"平台 {platform} 不存在。")
        return False
    shop_data = data[platform][1]
    if shop not in shop_data:
        print(f"店铺 {shop} 不存在。")
        return False
    if field not in shop_data[shop]:
        print(f"字段 {field} 不存在。")
        return False

    # 填充
    before = shop_data[shop][field]
    shop_data[shop][field] = value
    print(f"填充前：{before}，填充后：{shop_data[shop][field]}")

    # 保存
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("填充成功。")
    return True



# 示例调用
if __name__ == "__main__":
    # 示例：将'12345'填充到Instagram平台下GL.iNet US店铺的Total Followers字段
    fill_value_to_json(
        json_path="市场部社媒账号数据/optimized_data_structure_update_filled.json",
        platform="Instagram",
        shop="GL.iNet US",
        field="Total Followers",
        value="12345"
    )