"""
Facebook数据处理器
专门处理Facebook相关的数据映射和转换
"""

import json
import os
from typing import Dict, List, Any, Optional
from platform_config import FACEBOOK_FIELD_MAPPING

class FacebookProcessor:
    """Facebook数据处理器"""
    
    def __init__(self):
        self.field_mapping = FACEBOOK_FIELD_MAPPING
    
    def parse_facebook_raw_data(self, fb_raw_data: Dict) -> Dict:
        """解析Facebook原始数据"""
        # 提取response部分
        response_data = fb_raw_data.get('response', {})
        return response_data
    
    def find_keys_by_prefix(self, data: Dict, prefix: str) -> List[str]:
        """使用前缀模糊匹配查找键"""
        matching_keys = []
        
        for key in data.keys():
            if key.startswith(prefix):
                matching_keys.append(key)
        
        return matching_keys
    
    def extract_value_by_jsonpath(self, data: Dict, keys: List[str]) -> Any:
        """使用jsonpath模板提取数据"""
        values = []
        
        for key in keys:
            if key in data:
                value_obj = data[key]
                if isinstance(value_obj, dict):
                    if 'count' in value_obj:
                        values.append(value_obj['count'])
                    elif 'list' in value_obj:
                        values.append(value_obj['list'])
                    elif 'graphData' in value_obj:
                        values.append(value_obj['graphData'])
                    elif 'overview' in value_obj:
                        values.append(value_obj['overview'])
                    else:
                        values.append(value_obj)
                elif isinstance(value_obj, list):
                    values.append(value_obj)
                else:
                    values.append(value_obj)
        
        # 聚合值（求和或其他操作）
        if values:
            if all(isinstance(v, (int, float)) for v in values):
                return sum(values)
            else:
                return values[0] if len(values) == 1 else values
        
        return None
    
    def map_facebook_fields(self, fb_data: Dict) -> Dict:
        """Facebook字段映射"""
        mapped_data = {}
        
        for field_name, field_pattern in self.field_mapping.items():
            # 使用前缀模糊匹配
            matched_keys = self.find_keys_by_prefix(fb_data, field_pattern)
            
            if matched_keys:
                # 使用jsonpath模板提取数据
                field_value = self.extract_value_by_jsonpath(fb_data, matched_keys)
                mapped_data[field_name] = field_value
            else:
                mapped_data[field_name] = None
        
        return mapped_data
    
    def process_facebook_data(self, fb_file: str) -> Optional[Dict]:
        """处理Facebook数据"""
        print(f"处理Facebook数据：{fb_file}")
        
        try:
            # 加载Facebook原始数据
            with open(fb_file, 'r', encoding='utf-8') as f:
                fb_raw_data = json.load(f)
        except FileNotFoundError:
            print(f"错误：找不到 {fb_file} 文件")
            return None
        except json.JSONDecodeError:
            print(f"错误：{fb_file} 文件格式不正确")
            return None
        
        # 解析Facebook原始数据
        fb_structured_data = self.parse_facebook_raw_data(fb_raw_data)
        
        # Facebook字段映射
        fb_mapped_data = self.map_facebook_fields(fb_structured_data)
        
        # 输出更新后的Facebook数据
        output_path = os.path.join("output", "fb_fetch_inf_update.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(fb_mapped_data, f, ensure_ascii=False, indent=2)
        
        print("Facebook数据处理完成")
        return fb_mapped_data
    
    def get_mapping_statistics(self, mapped_data: Dict) -> Dict:
        """获取映射统计信息"""
        total_fields = len(self.field_mapping)
        mapped_fields = sum(1 for value in mapped_data.values() if value is not None)
        success_rate = (mapped_fields / total_fields * 100) if total_fields > 0 else 0
        
        return {
            "total_fields": total_fields,
            "mapped_fields": mapped_fields,
            "success_rate": f"{success_rate:.2f}%",
            "mapped_fields_list": [field for field, value in mapped_data.items() if value is not None],
            "unmapped_fields_list": [field for field, value in mapped_data.items() if value is None]
        } 