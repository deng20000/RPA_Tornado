import json
import os
from datetime import datetime, timedelta
import re
from typing import Dict, List, Any, Optional
from platform_config import get_platform_fields, get_field_mapping, get_platform_file, get_output_file
from facebook_processor import FacebookProcessor

class DataProcessor:
    """数据处理主类"""
    
    def __init__(self):
        self.required_files = [
            "dingding_fields.json",
            "dingding_allfields.json"
        ]
        
        # 初始化Facebook处理器
        self.facebook_processor = FacebookProcessor()

    def check_input_files(self) -> bool:
        """检查input文件夹中的输入文件是否存在"""
        for file in self.required_files:
            input_path = os.path.join("input", file)
            if not os.path.exists(input_path):
                print(f"错误：缺少必要的输入文件 {input_path}")
                return False
        return True

    def load_json_file(self, filename: str) -> Optional[Dict]:
        """从input文件夹加载JSON文件"""
        input_path = os.path.join("input", filename)
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"错误：找不到 {input_path} 文件")
            return None
        except json.JSONDecodeError:
            print(f"错误：{input_path} 文件格式不正确")
            return None

    def save_json_file(self, filename: str, data: Dict) -> None:
        """保存JSON文件到output文件夹"""
        output_path = os.path.join("output", filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"文件已保存：{output_path}")

    def get_yesterday_date(self) -> str:
        """获取昨天的日期格式 YYYY.MM"""
        yesterday = datetime.now() - timedelta(days=1)
        return yesterday.strftime("%Y.%m")

    def filter_yesterday_data(self, allfields_data: Dict) -> Dict:
        """筛选昨天数据"""
        yesterday_date = self.get_yesterday_date()
        filtered_data = {}
        
        for record_id, record_data in allfields_data.get('data', {}).items():
            # 假设时间字段在记录中
            if isinstance(record_data, dict) and '时间' in record_data:
                if record_data['时间'] == yesterday_date:
                    filtered_data[record_id] = record_data
            elif isinstance(record_data, str) and yesterday_date in record_data:
                filtered_data[record_id] = record_data
        
        print(f"筛选出 {len(filtered_data)} 条昨天数据")
        return filtered_data

    def extract_basic_info(self, yesterday_data: Dict) -> Dict:
        """提取基础信息"""
        basic_info = {}
        
        for record_id, record_data in yesterday_data.items():
            if isinstance(record_data, str):
                # 解析格式：时间name+社媒账号+渠道name
                parts = record_data.split('+')
                if len(parts) >= 3:
                    time_name, social_account, channel_name = parts[0], parts[1], parts[2]
                else:
                    time_name, social_account, channel_name = record_data, '', ''
            else:
                # 从字典中提取信息
                time_name = record_data.get('时间', '')
                social_account = record_data.get('社媒账号', '')
                channel_name = record_data.get('渠道', '')
            
            basic_info[record_id] = {
                'time': time_name,
                'social_account': social_account,
                'channel': channel_name,
                'raw_value': record_data
            }
        
        return basic_info

    def standardize_available_fields(self, basic_info: Dict) -> Dict:
        """标准化available_fields"""
        for record_id, record in basic_info.items():
            channel = record['channel']
            record['available_fields'] = get_platform_fields(channel)
        
        return basic_info

    def create_optimized_structure(self, standardized_fields: Dict, fields_data: Dict) -> Dict:
        """创建优化的数据结构"""
        optimized_structure = {
            "metadata": {
                "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "yesterday_date": self.get_yesterday_date(),
                "total_records": len(standardized_fields),
                "total_fields": len(fields_data.get('data', {})),
                "description": "优化的数据结构，结合记录ID和字段映射"
            },
            "fields_dict": fields_data.get('data', {}),
            "records": {}
        }
        
        # 为每个记录创建详细结构
        for record_id, record_info in standardized_fields.items():
            optimized_structure["records"][record_id] = {
                "basic_info": {
                    "time": record_info['time'],
                    "social_account": record_info['social_account'],
                    "channel": record_info['channel'],
                    "raw_value": record_info['raw_value']
                },
                "available_fields": record_info['available_fields'],
                "fields": {}  # 预留字段，用于存储映射后的数据
            }
        
        return optimized_structure

    def process_dingding_data(self) -> Optional[Dict]:
        """主线1：钉钉多维表数据处理"""
        print("开始处理钉钉多维表数据...")
        
        # 加载钉钉数据文件
        fields_data = self.load_json_file("dingding_fields.json")
        allfields_data = self.load_json_file("dingding_allfields.json")
        
        if not fields_data or not allfields_data:
            return None
        
        # 筛选昨天数据
        yesterday_data = self.filter_yesterday_data(allfields_data)
        
        # 提取基础信息
        basic_info = self.extract_basic_info(yesterday_data)
        
        # 标准化available_fields
        standardized_fields = self.standardize_available_fields(basic_info)
        
        # 结构优化
        optimized_structure = self.create_optimized_structure(standardized_fields, fields_data)
        
        # 输出优化结构
        self.save_json_file("optimized_data_structure_update.json", optimized_structure)
        
        print(f"钉钉数据处理完成，生成 {len(optimized_structure['records'])} 条记录")
        return optimized_structure

    def get_source_files(self) -> List[Dict]:
        """从input文件夹获取源数据文件列表"""
        source_files = []
        
        # 检查各种平台的数据文件
        platforms = ["facebook", "youtube", "instagram", "linkedin", "x"]
        
        for platform in platforms:
            filename = get_platform_file(platform)
            if filename:
                input_path = os.path.join("input", filename)
                if os.path.exists(input_path):
                    source_files.append({
                        "type": platform,
                        "filename": input_path
                    })
        
        return source_files

    def process_source_data(self) -> Dict:
        """主线2：网站源数据处理"""
        print("开始处理网站源数据...")
        
        source_files = self.get_source_files()
        processed_data = {}
        
        for file_info in source_files:
            file_type = file_info["type"]
            filename = file_info["filename"]
            
            if file_type == "facebook":
                processed_data["facebook"] = self.process_facebook_data(filename)
            elif file_type == "youtube":
                processed_data["youtube"] = self.process_youtube_data(filename)
            elif file_type == "instagram":
                processed_data["instagram"] = self.process_instagram_data(filename)
            elif file_type == "linkedin":
                processed_data["linkedin"] = self.process_linkedin_data(filename)
            elif file_type == "x":
                processed_data["x"] = self.process_x_data(filename)
        
        return processed_data

    def process_facebook_data(self, fb_file: str) -> Optional[Dict]:
        """Facebook数据处理分支"""
        return self.facebook_processor.process_facebook_data(fb_file)

    def process_youtube_data(self, yt_file: str) -> Optional[Dict]:
        """Youtube数据处理逻辑"""
        print(f"处理Youtube数据：{yt_file}")
        # TODO: 实现Youtube特定的字段映射
        return None

    def process_instagram_data(self, ig_file: str) -> Optional[Dict]:
        """Instagram数据处理逻辑"""
        print(f"处理Instagram数据：{ig_file}")
        # TODO: 实现Instagram特定的字段映射
        return None

    def process_linkedin_data(self, li_file: str) -> Optional[Dict]:
        """LinkedIn数据处理逻辑"""
        print(f"处理LinkedIn数据：{li_file}")
        # TODO: 实现LinkedIn特定的字段映射
        return None

    def process_x_data(self, x_file: str) -> Optional[Dict]:
        """X数据处理逻辑"""
        print(f"处理X数据：{x_file}")
        # TODO: 实现X特定的字段映射
        return None

    def merge_and_fill_data(self, optimized_data: Dict, source_data: Dict) -> Dict:
        """数据合并与更新"""
        print("开始合并和填充数据...")
        
        # 渠道名称映射
        channel_mapping = {
            "FB": "facebook",
            "Youtube": "youtube", 
            "Instagram": "instagram",
            "LinkedIn": "linkedin",
            "X": "x"
        }
        
        for record_id, record in optimized_data['records'].items():
            channel = record['basic_info']['channel']
            mapped_channel = channel_mapping.get(channel, channel.lower())
            
            # 根据渠道获取对应的源数据
            channel_data = source_data.get(mapped_channel)
            
            # 填充数据到优化结构
            if channel_data:
                record['fields'] = channel_data
                print(f"为记录 {record_id} 填充了 {mapped_channel} 数据")
        
        return optimized_data

    def generate_mapping_report(self, final_data: Dict) -> Dict:
        """生成映射报告"""
        print("生成映射报告...")
        
        total_records = len(final_data['records'])
        mapped_records = 0
        
        for record in final_data['records'].values():
            if record.get('fields'):
                mapped_records += 1
        
        success_rate = (mapped_records / total_records * 100) if total_records > 0 else 0
        
        report = {
            "total_records": total_records,
            "mapped_records": mapped_records,
            "mapping_success_rate": f"{success_rate:.2f}%",
            "detailed_mapping": {
                "facebook": "fb_fetch_inf_update.json",
                "youtube": "youtube_fetch_inf_update.json",
                "instagram": "instagram_fetch_inf_update.json",
                "linkedin": "linkedin_fetch_inf_update.json",
                "x": "x_fetch_inf_update.json"
            }
        }
        
        self.save_json_file("mapping_report.json", report)
        return report

    def save_final_output(self, final_data: Dict) -> None:
        """保存最终输出文件"""
        self.save_json_file("optimized_data_structure_update.json", final_data)
        print("数据处理完成，输出文件已生成")

    def main(self) -> None:
        """主程序入口"""
        print("=== 数据处理流程开始 ===")
        
        # 检查输入文件是否存在
        if not self.check_input_files():
            print("错误：缺少必要的输入文件")
            return
        
        try:
            # 执行双主线处理
            optimized_data = self.process_dingding_data()  # 主线1
            source_data = self.process_source_data()       # 主线2
            
            if optimized_data:
                # 合并数据并输出
                final_data = self.merge_and_fill_data(optimized_data, source_data)
                self.generate_mapping_report(final_data)
                self.save_final_output(final_data)
                
                print("=== 数据处理流程完成 ===")
            else:
                print("钉钉数据处理失败")
                
        except Exception as e:
            print(f"处理过程中出现错误: {e}")

def main():
    """主函数"""
    processor = DataProcessor()
    processor.main()

if __name__ == "__main__":
    main()
