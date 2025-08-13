#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pytest 配置文件
提供测试夹具和全局配置
"""

import pytest
import asyncio
import json
from pathlib import Path
from typing import Dict, Any

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent


@pytest.fixture(scope="session")
def event_loop():
    """创建事件循环用于异步测试"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def base_url():
    """测试服务器基础URL"""
    return "http://127.0.0.1:8888"


@pytest.fixture(scope="session")
def api_headers():
    """API请求头"""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }


@pytest.fixture(scope="session")
def sample_data():
    """测试用例数据"""
    return {
        "seller_id": 109,
        "event_date": "2024-08-05",
        "start_date": "2024-07-01",
        "end_date": "2024-07-31",
        "offset": 0,
        "length": 10
    }


@pytest.fixture
def mock_response_success():
    """模拟成功响应"""
    return {
        "code": 200,
        "message": "success",
        "data": {
            "total": 100,
            "list": []
        }
    }


@pytest.fixture
def mock_response_error():
    """模拟错误响应"""
    return {
        "code": 400,
        "message": "参数错误",
        "data": None
    }


# pytest 配置
pytest_plugins = []

# 测试标记
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.api = pytest.mark.api
pytest.mark.slow = pytest.mark.slow