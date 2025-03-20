# GitLab企业数据平台文档抓取工具

这个项目用于抓取GitLab企业数据平台文档并将其保存为Markdown格式。

## 环境要求

- Python 3.10
- uv (Python包管理工具)

## 功能特点

- 抓取GitLab企业数据平台文档
- 将文档转换为Markdown格式
- 保持文档的层级结构
- 保存图片和链接

## 使用方法

1. 安装uv（如果尚未安装）：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. 创建虚拟环境并安装依赖：
```bash
uv venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
uv pip install -r requirements.txt
```

3. 运行脚本：
```bash
python src/main.py
```

## 项目结构

```
.
├── README.md
├── requirements.txt
├── src/
│   └── main.py
└── data/
    └── markdown/
```

## 输出

抓取的文档将保存在 `data/markdown/` 目录下，保持原有的目录结构。 