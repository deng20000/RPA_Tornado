import json
from typing import Any
from pathlib import Path

def save_json(data: Any, file_path: str) -> None:
    """
    保存数据为 json 文件
    :param data: 可序列化的数据
    :param file_path: 保存路径
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2) 