"""
数据处理模块测试
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path


class TestDataProcessing:
    """数据处理测试类"""
    
    def test_pandas_import(self):
        """测试pandas导入"""
        assert pd is not None
        assert hasattr(pd, 'read_excel')
        assert hasattr(pd, 'DataFrame')
    
    def test_numpy_import(self):
        """测试numpy导入"""
        assert np is not None
        assert hasattr(np, 'array')
        assert hasattr(np, 'zeros')
    
    def test_dataframe_creation(self):
        """测试DataFrame创建"""
        data = {
            'A': [1, 2, 3],
            'B': ['a', 'b', 'c'],
            'C': [1.1, 2.2, 3.3]
        }
        df = pd.DataFrame(data)
        assert len(df) == 3
        assert list(df.columns) == ['A', 'B', 'C']
    
    def test_excel_operations(self):
        """测试Excel操作"""
        # 创建测试数据
        data = {
            'Column1': [1, 2, 3],
            'Column2': ['A', 'B', 'C']
        }
        df = pd.DataFrame(data)
        
        # 测试Excel写入和读取
        test_file = Path('test_data.xlsx')
        try:
            df.to_excel(test_file, index=False)
            assert test_file.exists()
            
            # 读取Excel文件
            read_df = pd.read_excel(test_file)
            assert len(read_df) == len(df)
            assert list(read_df.columns) == list(df.columns)
        finally:
            # 清理测试文件
            if test_file.exists():
                test_file.unlink()


class TestFileOperations:
    """文件操作测试类"""
    
    def test_path_operations(self):
        """测试路径操作"""
        test_dir = Path('test_directory')
        test_file = test_dir / 'test_file.txt'
        
        try:
            # 创建目录
            test_dir.mkdir(exist_ok=True)
            assert test_dir.exists()
            
            # 创建文件
            test_file.write_text('test content')
            assert test_file.exists()
            assert test_file.read_text() == 'test content'
        finally:
            # 清理
            if test_file.exists():
                test_file.unlink()
            if test_dir.exists():
                test_dir.rmdir()


if __name__ == '__main__':
    pytest.main([__file__]) 