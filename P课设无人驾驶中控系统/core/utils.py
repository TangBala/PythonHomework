# core/utils.py
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def load_data(filename):
    """从data文件夹加载一个JSON文件"""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data, filename):
    """将数据保存为一个JSON文件到data文件夹"""
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)