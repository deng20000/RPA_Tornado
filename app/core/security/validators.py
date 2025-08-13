# 数据验证器模块
# 提供请求数据验证和输入清理功能

import re
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from app.core.exceptions import ValidationError


def validate_request_data(data: Dict[str, Any], rules: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    验证请求数据
    
    Args:
        data: 请求数据
        rules: 验证规则
            {
                'field_name': {
                    'required': True/False,
                    'type': str/int/float/list/dict,
                    'min_length': int,
                    'max_length': int,
                    'pattern': str (正则表达式),
                    'choices': [可选值列表]
                }
            }
    
    Returns:
        Dict: 验证后的数据
        
    Raises:
        ValidationError: 验证失败时抛出
    """
    validated_data = {}
    errors = []
    
    for field_name, field_rules in rules.items():
        value = data.get(field_name)
        
        # 检查必填字段
        if field_rules.get('required', False) and value is None:
            errors.append(f"字段 '{field_name}' 是必填的")
            continue
        
        # 如果字段不是必填且值为None，跳过验证
        if value is None:
            continue
        
        # 类型验证
        expected_type = field_rules.get('type')
        if expected_type and not isinstance(value, expected_type):
            errors.append(f"字段 '{field_name}' 类型错误，期望 {expected_type.__name__}，实际 {type(value).__name__}")
            continue
        
        # 字符串长度验证
        if isinstance(value, str):
            min_length = field_rules.get('min_length')
            max_length = field_rules.get('max_length')
            
            if min_length is not None and len(value) < min_length:
                errors.append(f"字段 '{field_name}' 长度不能少于 {min_length} 个字符")
                continue
            
            if max_length is not None and len(value) > max_length:
                errors.append(f"字段 '{field_name}' 长度不能超过 {max_length} 个字符")
                continue
            
            # 正则表达式验证
            pattern = field_rules.get('pattern')
            if pattern and not re.match(pattern, value):
                errors.append(f"字段 '{field_name}' 格式不正确")
                continue
        
        # 选择值验证
        choices = field_rules.get('choices')
        if choices and value not in choices:
            errors.append(f"字段 '{field_name}' 值必须是 {choices} 中的一个")
            continue
        
        validated_data[field_name] = value
    
    if errors:
        raise ValidationError("数据验证失败", {'errors': errors})
    
    return validated_data


def sanitize_input(value: Union[str, Dict, List]) -> Union[str, Dict, List]:
    """
    清理输入数据，防止XSS攻击
    
    Args:
        value: 输入值
        
    Returns:
        清理后的值
    """
    if isinstance(value, str):
        # 移除潜在的危险字符
        dangerous_chars = ['<', '>', '"', "'", '&']
        for char in dangerous_chars:
            value = value.replace(char, '')
        return value.strip()
    
    elif isinstance(value, dict):
        return {k: sanitize_input(v) for k, v in value.items()}
    
    elif isinstance(value, list):
        return [sanitize_input(item) for item in value]
    
    return value


def validate_date_format(date_str: str, format_str: str = '%Y-%m-%d') -> bool:
    """
    验证日期格式
    
    Args:
        date_str: 日期字符串
        format_str: 日期格式
        
    Returns:
        bool: 是否为有效日期格式
    """
    try:
        datetime.strptime(date_str, format_str)
        return True
    except ValueError:
        return False


def validate_json_string(json_str: str) -> bool:
    """
    验证JSON字符串格式
    
    Args:
        json_str: JSON字符串
        
    Returns:
        bool: 是否为有效JSON格式
    """
    try:
        json.loads(json_str)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def validate_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email: 邮箱地址
        
    Returns:
        bool: 是否为有效邮箱格式
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    验证手机号格式（中国大陆）
    
    Args:
        phone: 手机号
        
    Returns:
        bool: 是否为有效手机号格式
    """
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))