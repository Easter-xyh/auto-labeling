"""
主流程：读取AG新闻数据 -> 调用大模型打标 -> 保存结果 -> 计算评估指标
"""

import os
import sys

# 导入各模块
import data_loader
import labeller
import data_writter
import caculating

# 导入提示词模板（会自动设置 labeller.PROMPT_TEMPLATE）
import prompt

def main():
    # 配置路径
    input_csv = r"input\ag_news_test_balanced_40.csv"
    output_csv = r"output\predictions.csv"

    print("=" * 50)
    print("步骤1: 加载数据")
    # 加载文本列
    try:
        texts = data_loader.load_text_column(input_csv)
        print(f"成功加载 {len(texts)} 条新闻文本")
    except Exception as e:
        print(f"数据加载失败: {e}")
        sys.exit(1)

    # 加载真实标签（用于评估）
    try:
        gold_labels = caculating.load_key_column(input_csv)
        print(f"成功加载 {len(gold_labels)} 条真实标签")
    except Exception as e:
        print(f"真实标签加载失败: {e}")
        gold_labels = None

    print("\n步骤2: 调用大模型进行打标")
    print("注意: 每次调用API需要几秒时间，请耐心等待...")
    try:
        results = labeller.predict_labels(texts)
        print(f"打标完成，共生成 {len(results)} 条结果")
    except Exception as e:
        print(f"打标失败: {e}")
        sys.exit(1)

    print("\n步骤3: 保存打标结果")
    try:
        data_writter.write_results_to_csv(results, output_csv)
    except Exception as e:
        print(f"保存结果失败: {e}")

    # 如果真实标签存在，则计算评估指标
    if gold_labels is not None:
        print("\n步骤4: 计算评估指标")
        pred_labels = caculating.extract_labels(results)

        # 确保两个列表长度一致
        min_len = min(len(gold_labels), len(pred_labels))
        gold_labels = gold_labels[:min_len]
        pred_labels = pred_labels[:min_len]

        # 准确率
        matches = caculating.count_matches(pred_labels, gold_labels)
        accuracy = matches / len(gold_labels) if len(gold_labels) > 0 else 0.0
        print(f"\n准确率 (Accuracy): {accuracy:.4f} ({matches}/{len(gold_labels)})")

        # 各类别指标
        classes = ["World", "Sports", "Business", "SciTech"]
        per_class = caculating.compute_metrics_per_class(gold_labels, pred_labels, classes)
        print("\n各类别指标:")
        for c in classes:
            p = per_class[c]["precision"]
            r = per_class[c]["recall"]
            f1 = per_class[c]["f1"]
            print(f"  {c:10s} - Precision: {p:.4f}, Recall: {r:.4f}, F1: {f1:.4f}")

        # 宏平均
        macro = caculating.compute_macro_average(per_class)
        print(f"\n宏平均 (Macro Average) - Precision: {macro['precision']:.4f}, Recall: {macro['recall']:.4f}, F1: {macro['f1']:.4f}")

    print("\n全部完成！")

if __name__ == "__main__":
    main()