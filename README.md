# AG News 自动打标项目 – 大模型评测方向笔试题

本项目使用阿里云 DashScope 兼容模式调用 DeepSeek 模型，对 AG News 数据集（40 条平衡采样新闻）进行自动分类打标，并输出评估指标（准确率、各类别 Precision/Recall/F1、宏平均）。

本项目在制作时借助了deepseek，具体对话链接在此处https://chat.deepseek.com/share/de6u0yj4ejxenhfjly

## 项目结构

├── input/ # 存放输入数据（需手动创建）

│ └── ag_news_test_balanced_40.csv

├── output/ # 输出目录（程序自动创建）

│ └── predictions.csv # 打标结果

├── data_loader.py # 数据读取模块

├── labeller.py # 模型调用与打标核心

├── prompt.py # 提示词模板配置

├── caculating.py # 指标计算（准确率、F1等）

├── data_writter.py # 结果写入 CSV

├── pipeline.py # 主流程脚本

└── README.md



## 功能模块

| 模块 | 功能 |
|------|------|
| `data_loader` | 读取 CSV 文件，提取 `text` 列 |
| `labeller` | 调用 DeepSeek API，使用提示词对每条新闻分类 |
| `prompt` | 设置分类提示词，限定输出 World/Sports/Business/SciTech |
| `caculating` | 计算准确率、各类别精确率/召回率/F1、宏平均 |
| `data_writter` | 将预测结果写入 CSV（自动创建目录/表头） |
| `pipeline` | 编排整体流程：加载→打标→保存→评估 |

## 环境要求

- Python 3.7+
- 阿里云 DashScope API Key（开通 DeepSeek 模型服务）
- 网络可访问 `dashscope.aliyuncs.com`

## 配置与安装

1. **克隆/下载本项目**
2. **安装依赖**（仅使用标准库，无需额外安装）
3. **设置环境变量**（Windows 示例）：
   ```cmd
   set DASHSCOPE_API_KEY=sk-xxxxxxxxxxxxxxxx
   ```
4. **准备数据**
将ag_news_test_balanced_40.csv 放入 input/ 文件夹。
5. **运行项目**
   ```cmd
   python pipeline.py
   ```
## 输出示例

==================================================

步骤1: 加载数据
成功加载 40 条新闻文本
成功加载 40 条真实标签

步骤2: 调用大模型进行打标...
已处理 1/40 条
...
打标完成，共生成 40 条结果

步骤3: 保存打标结果
已成功写入 40 条结果至 output\predictions.csv

步骤4: 计算评估指标

准确率 (Accuracy): 0.8250 (33/40)

各类别指标:
  World      - Precision: 0.8000, Recall: 0.7273, F1: 0.7619
  Sports     - Precision: 0.9000, Recall: 0.9000, F1: 0.9000
  Business   - Precision: 0.8182, Recall: 0.9000, F1: 0.8571
  SciTech    - Precision: 0.8000, Recall: 0.7273, F1: 0.7619

宏平均 (Macro Average) - Precision: 0.8295, Recall: 0.8136, F1: 0.8202

全部完成！
