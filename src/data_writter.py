import csv
import os
from typing import List, Dict

def write_results_to_csv(results: List[Dict[str, str]], filepath: str, headers: List[str] = None) -> None:
    """
    将打标器返回的 results 列表写入目标路径的 CSV 文件中（覆盖写入）。
    results 列表每个元素为字典，包含 'text' 和 'pre_label' 键。
    若文件所在目录不存在，会自动创建；若文件已存在，会被覆盖。
    """
    if not results:
        print("警告：results 为空，未写入任何内容。")
        return

    if headers is None:
        headers = ['text', 'pre_label']

    # 确保目录存在
    dir_path = os.path.dirname(filepath)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # 覆盖写入文件（先写表头，再写数据）
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in results:
            filtered_row = {k: row.get(k, '') for k in headers}
            writer.writerow(filtered_row)

    print(f"已成功写入 {len(results)} 条结果至 {filepath}")