"""
退货追踪数据处理模块配置文件

该文件包含模块运行所需的各种配置参数，
包括地区设置、文件路径、Excel格式等。

使用方法：
    from config import CONFIG
    print(CONFIG['DEFAULT_INPUT_FILE'])
"""

# ==================== 基本配置 ====================

# 默认配置字典
CONFIG = {
    # 文件路径配置
    'DEFAULT_INPUT_FILE': 'test.json',           # 默认输入文件名
    'OUTPUT_DIR': '.',                           # 输出目录
    'BACKUP_DIR': './backup',                    # 备份目录
    
    # 日期格式配置
    'DATE_FORMAT': '%Y-%m-%d',                   # 日期格式
    'FILENAME_DATE_FORMAT': '%Y年%m月%d日',       # 文件名中的日期格式
    'TIMESTAMP_UNIT': 1000,                      # 时间戳单位（毫秒）
    
    # Excel配置
    'EXCEL_EXTENSION': '.xlsx',                  # Excel文件扩展名
    'SHEET_NAME_TEMPLATE': {
        'amazon': '亚马逊-买家退货-{region}',      # 亚马逊工作表名称模板
        'shopify': 'shopfiy-{region}买家退货',    # Shopify工作表名称模板
        'removal': '亚马逊移除-{region}'          # 移除工作表名称模板
    },
    
    # 数据验证配置
    'REQUIRED_FIELDS': [                         # 必需字段列表
        '订单号', '产品型号', '数量', '购买渠道',
        '退货时间', '购买时间', '退货点', '客户是否寄回(寄回单号）'
    ],
    
    # 调试配置
    'DEBUG_MODE': True,                          # 调试模式开关
    'VERBOSE_LOGGING': True,                     # 详细日志开关
    'SHOW_PROGRESS': True,                       # 显示处理进度
}

# ==================== 地区和平台配置 ====================

# 亚马逊欧洲国家代码
AMAZON_EU_COUNTRIES = [
    'IT',  # 意大利
    'DE',  # 德国
    'FR',  # 法国
    'ES',  # 西班牙
    'NL',  # 荷兰
    'SE',  # 瑞典
    'TR',  # 土耳其
    'PL',  # 波兰
    'BE'   # 比利时
]

# 地区映射配置
REGION_MAPPING = {
    'US': '美国',
    'EU': '欧洲',
    'UK': '英国'
}

# 平台识别规则
PLATFORM_RULES = {
    'amazon': {
        'US': ['Amazon US'],
        'UK': ['Amazon UK'],
        'EU': [f'Amazon {country}' for country in AMAZON_EU_COUNTRIES]
    },
    'shopify': {
        'US': ['US'],
        'UK': ['UK'],
        'EU': AMAZON_EU_COUNTRIES
    }
}

# 站点字段名称变体（支持多种命名方式）
SITE_FIELD_VARIANTS = [
    'shopify站点',
    'Shopify站点',
    'shopify_site',
    'site',
    '站点'
]

# ==================== Excel表格配置 ====================

# Excel表头配置
EXCEL_HEADERS = [
    '表中来源数据',
    '店铺',
    '订单号',
    '产品型号',
    '数量',
    '购买渠道',
    '退货时间',
    '购买时间',
    '退货点',
    '客户是否寄回'
]

# Excel样式配置
EXCEL_STYLES = {
    'header': {
        'font': {'bold': True, 'color': 'FFFFFF'},
        'fill': {'patternType': 'solid', 'fgColor': '366092'},
        'alignment': {'horizontal': 'center', 'vertical': 'center'}
    },
    'data': {
        'alignment': {'horizontal': 'left', 'vertical': 'center'},
        'border': {'style': 'thin'}
    }
}

# ==================== 错误处理配置 ====================

# 错误消息模板
ERROR_MESSAGES = {
    'file_not_found': '文件未找到: {filename}',
    'json_parse_error': 'JSON解析错误: {error}',
    'empty_file': '文件内容为空: {filename}',
    'invalid_data': '数据格式无效: {details}',
    'excel_export_error': 'Excel导出失败: {error}',
    'permission_error': '文件权限错误: {filename}'
}

# 警告消息模板
WARNING_MESSAGES = {
    'missing_field': '缺少字段 "{field}" 在订单 {order_id} 中',
    'invalid_timestamp': '无效时间戳 "{timestamp}" 在订单 {order_id} 中',
    'unknown_site': '未知站点 "{site}" 在订单 {order_id} 中',
    'empty_value': '空值字段 "{field}" 在订单 {order_id} 中'
}

# ==================== 性能配置 ====================

# 性能相关配置
PERFORMANCE_CONFIG = {
    'BATCH_SIZE': 1000,                          # 批处理大小
    'MAX_MEMORY_USAGE': 512 * 1024 * 1024,      # 最大内存使用（512MB）
    'PROGRESS_UPDATE_INTERVAL': 100,             # 进度更新间隔
    'ENABLE_MULTIPROCESSING': False,             # 是否启用多进程
    'MAX_WORKERS': 4                             # 最大工作进程数
}

# ==================== 日志配置 ====================

# 日志配置
LOGGING_CONFIG = {
    'level': 'INFO',                             # 日志级别
    'format': '%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    'file': 'return_tracking.log',               # 日志文件名
    'max_size': 10 * 1024 * 1024,               # 最大日志文件大小（10MB）
    'backup_count': 5                            # 日志文件备份数量
}

# ==================== 验证函数 ====================

def validate_config():
    """
    验证配置文件的有效性
    
    检查所有必需的配置项是否存在且有效，
    如果发现问题会抛出相应的异常。
    
    Raises:
        ValueError: 当配置项无效时
        KeyError: 当缺少必需配置项时
    """
    # 检查必需的配置项
    required_keys = [
        'DEFAULT_INPUT_FILE', 'OUTPUT_DIR', 'DATE_FORMAT',
        'EXCEL_EXTENSION', 'REQUIRED_FIELDS'
    ]
    
    for key in required_keys:
        if key not in CONFIG:
            raise KeyError(f"缺少必需的配置项: {key}")
    
    # 验证文件扩展名
    if not CONFIG['EXCEL_EXTENSION'].startswith('.'):
        raise ValueError("Excel扩展名必须以'.'开头")
    
    # 验证日期格式
    try:
        from datetime import datetime
        datetime.now().strftime(CONFIG['DATE_FORMAT'])
        datetime.now().strftime(CONFIG['FILENAME_DATE_FORMAT'])
    except ValueError as e:
        raise ValueError(f"无效的日期格式: {e}")
    
    # 验证地区映射
    if not all(region in REGION_MAPPING for region in ['US', 'EU', 'UK']):
        raise ValueError("地区映射配置不完整")
    
    print("✅ 配置验证通过")


def get_config(key, default=None):
    """
    安全获取配置值
    
    Args:
        key (str): 配置键名
        default: 默认值
        
    Returns:
        配置值或默认值
    """
    return CONFIG.get(key, default)


def update_config(key, value):
    """
    更新配置值
    
    Args:
        key (str): 配置键名
        value: 新的配置值
    """
    CONFIG[key] = value
    print(f"配置已更新: {key} = {value}")


# ==================== 环境检测 ====================

def check_environment():
    """
    检查运行环境
    
    检查必需的Python库是否已安装，
    以及文件权限等环境因素。
    
    Returns:
        bool: 环境检查是否通过
    """
    import sys
    
    print("检查运行环境...")
    
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("❌ Python版本过低，需要3.6或更高版本")
        return False
    
    # 检查必需的库
    required_modules = ['json', 'datetime', 'openpyxl', 'os']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"❌ 缺少必需的库: {', '.join(missing_modules)}")
        return False
    
    # 检查文件权限
    import os
    output_dir = CONFIG['OUTPUT_DIR']
    if not os.access(output_dir, os.W_OK):
        print(f"❌ 输出目录无写入权限: {output_dir}")
        return False
    
    print("✅ 环境检查通过")
    return True


# ==================== 初始化 ====================

if __name__ == "__main__":
    """
    配置文件测试
    """
    print("退货追踪数据处理模块 - 配置文件")
    print("=" * 50)
    
    # 验证配置
    try:
        validate_config()
    except Exception as e:
        print(f"❌ 配置验证失败: {e}")
        exit(1)
    
    # 检查环境
    if not check_environment():
        print("❌ 环境检查失败")
        exit(1)
    
    # 显示当前配置
    print("\n当前配置:")
    print("-" * 30)
    for key, value in CONFIG.items():
        print(f"{key}: {value}")
    
    print("\n地区映射:")
    print("-" * 30)
    for code, name in REGION_MAPPING.items():
        print(f"{code}: {name}")
    
    print("\n✅ 配置文件测试完成")