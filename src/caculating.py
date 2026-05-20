import csv
from typing import List, Dict, Any
from collections import defaultdict

def extract_labels(results: List[Dict[str, str]]) -> List[str]:
    """从打标器返回的结果列表中提取预测标签"""
    return [item["pre_label"] for item in results]

def load_key_column(filepath: str) -> List[str]:
    """读取 CSV 文件，返回第三列（gold_label列）的内容列表"""
    keys = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            keys.append(row['gold_label'])
    return keys

def count_matches(list1: List[Any], list2: List[Any]) -> int:
    """一一比较两个列表对应位置的元素，返回相同位置且相同元素的数量"""
    min_len = min(len(list1), len(list2))
    matches = 0
    for i in range(min_len):
        if list1[i] == list2[i]:
            matches += 1
    return matches

def compute_metrics_per_class(gold_labels: List[str], pred_labels: List[str], classes: List[str]) -> Dict[str, Dict[str, float]]:
    """
    计算每个类别的精确率、召回率、F1。
    输入：
        gold_labels: 真实标签列表
        pred_labels: 预测标签列表
        classes: 所有可能的类别列表，如 ["World", "Sports", "Business", "SciTech"]
    输出：
        字典，键为类别名，值为 {"precision": p, "recall": r, "f1": f}
    """
    # 初始化混淆矩阵计数，字典
    tp = {c: 0 for c in classes}
    fp = {c: 0 for c in classes}
    fn = {c: 0 for c in classes}
    
    for gold, pred in zip(gold_labels, pred_labels): # 配对真实标签和预测标签成对
        if gold not in classes:
            continue
        if pred not in classes:
            # 预测标签无效，视为该类别负例，只增加 FN 对于真实类别
            fn[gold] += 1
            continue
        if gold == pred:
            tp[gold] += 1
        else:
            fp[pred] += 1
            fn[gold] += 1
    
    metrics = {}
    for c in classes:
        p = tp[c] / (tp[c] + fp[c]) if (tp[c] + fp[c]) > 0 else 0.0
        r = tp[c] / (tp[c] + fn[c]) if (tp[c] + fn[c]) > 0 else 0.0
        f1 = 2 * p * r / (p + r) if (p + r) > 0 else 0.0
        metrics[c] = {"precision": p, "recall": r, "f1": f1}
    return metrics

def compute_macro_average(metrics: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """
    计算宏平均的精确率、召回率、F1。
    输入 metrics 为 compute_metrics_per_class 返回的字典。
    返回 {"precision": macro_p, "recall": macro_r, "f1": macro_f1}
    """
    classes = list(metrics.keys())
    if not classes:
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}
    macro_p = sum(metrics[c]["precision"] for c in classes) / len(classes)
    macro_r = sum(metrics[c]["recall"] for c in classes) / len(classes)
    macro_f1 = sum(metrics[c]["f1"] for c in classes) / len(classes)
    return {"precision": macro_p, "recall": macro_r, "f1": macro_f1}
