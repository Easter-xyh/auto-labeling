import labeller

# 设置提示词模板
labeller.PROMPT_TEMPLATE = """
你是一个专业的新闻分类器，你需要判断以下新闻文本属于哪个新闻类别。

你只能从以下四个类别中选择一个输出：World, Sports, Business, SciTech。

新闻文本：
{text}

你的输出格式必须是“类别：World/Sports/Business/SciTech”，禁止输出其它格式或其它内容。
"""