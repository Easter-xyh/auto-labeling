import os
import json
import urllib.request
import urllib.error
from typing import List, Dict

PROMPT_TEMPLATE = None
API_KEY = os.getenv("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"  

def call_qwen(prompt: str, model: str = "deepseek-v4-pro") -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    data = json.dumps(payload).encode("utf-8")
    
    req = urllib.request.Request(BASE_URL, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise Exception(f"API 请求失败: {e.code} {error_body}")

def predict_labels(texts: List[str]) -> List[Dict[str, str]]:
    """
    对输入的文本列表进行打标，使用全局 PROMPT_TEMPLATE。
    模板中需包含占位符 {text}，例如：
    "请判断以下新闻类别：{text}\n输出：World, Sports, Business, SciTech 之一"
    """
    if PROMPT_TEMPLATE is None:
        raise ValueError("PROMPT_TEMPLATE 未设置，请在调用前为labeller.PROMPT_TEMPLATE赋值")
    
    results = []
    for idx, text in enumerate(texts):
        prompt = PROMPT_TEMPLATE.format(text=text)
        try:
            raw_label = call_qwen(prompt)
            # 后处理：提取有效类别
            cleaned = raw_label.strip()
            valid_labels = {"World", "Sports", "Business", "SciTech"}
            for label in valid_labels:
                if label.lower() in cleaned.lower():
                    cleaned = label
                    break
            pred_label = cleaned
        except Exception as e:
            pred_label = f"ERROR: {str(e)}"

        results.append({"text": text, "pre_label": pred_label})
        print(f"已处理 {idx+1}/{len(texts)} 条")
    
    return results