import csv
from typing import List, Dict

def load_data(filepath: str) -> List[Dict[str, str]]:
    """
    读取CSV文件，返回字典列表。
    每一行对应一个字典，键为列标题，值为该列的内容。
    """
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def load_text_column(filepath: str) -> List[str]:
    """
    读取 CSV 文件，返回第二列（text列）的内容列表，每个元素为字符串。
    """
    texts = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row['text'])
    return texts