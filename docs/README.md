# GitLab 企业数据平台文档（中文版）

本仓库包含 GitLab 企业数据平台文档的中文翻译，为数据工程、分析和平台管理提供全面的指导。

## 项目结构

```
.
├── README_EN.md           # 英文说明文档
├── docs/
│   ├── zh-CN/            # 中文文档
│   │   ├── images/       # 文档图片
│   │   └── SQL_Style_Guide.md  # SQL 风格指南
│   └── README.md         # 中文说明文档
├── data/
│   └── markdown/         # 原始英文 Markdown 文件
├── src/
│   └── translate/        # 翻译相关脚本
│       └── translate_docs.py  # 文档翻译主脚本
├── .env.example         # 环境变量配置模板
└── pyproject.toml       # 项目配置和依赖管理
```

## 文档概述

文档涵盖以下主要领域：

### 数据工程
- **数据源和管道**
  - 数据源管理
  - ETL 流程
  - 数据管道架构

- **数据仓库**
  - 企业数据仓库 (EDW) 架构
  - Snowflake 集成和优化
  - 数据建模和转换

### 分析和可视化
- **Tableau 集成**
  - 开发者指南和最佳实践
  - 管理员指南
  - 样式指南
  - 技巧和窍门

- **数据分析工具**
  - Python 开发环境
  - RStudio 设置和使用
  - Jupyter notebooks
  - dbt 数据转换

### 平台管理
- **基础设施**
  - AWS 集成
  - 数据基础设施设置
  - 数据科学的 CI/CD 流程

- **数据治理**
  - GDPR 合规性
  - 数据安全
  - 访问控制和权限

### 开发标准
- **编码标准**
  - SQL 风格指南
  - Python 编码标准
  - 数据工程最佳实践

## 特性

- GitLab 企业数据平台文档的完整中文翻译
- 保持原始文档结构和格式
- 包含所有图片和图表
- 使用 Git LFS 高效存储图片
- Markdown 格式便于阅读和编辑
- 全面覆盖数据工程和分析主题
- 支持使用 Deepseek API 自动翻译文档

## 快速开始

1. 克隆仓库：
```bash
git clone https://github.com/wyaming89/gitlab-data-docs-cn.git
```

2. 安装 uv 工具（如果尚未安装）：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. 安装依赖：
```bash
uv venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
uv pip install -e .
```

4. 配置环境变量：
```bash
cp .env.example .env
# 编辑 .env 文件，添加您的 Deepseek API 密钥
```

5. 运行翻译脚本：
```bash
python src/translate/translate_docs.py
```

6. 查看文档：
```bash
cd docs/zh-CN
```

## 文档分类

### 核心文档
- 数据团队平台概述
- 企业数据仓库
- 数据源和管道
- 数据基础设施

### 开发指南
- SQL 风格指南
- Python 指南
- dbt 指南
- RStudio 指南
- Jupyter 指南

### 分析工具
- Tableau 指南
  - 开发者指南
  - 管理员指南
  - 样式指南
  - 技巧和窍门

### 平台管理
- AWS 集成
- Snowflake 优化
- 数据科学的 CI/CD
- 数据治理

## 自动翻译功能

本项目提供了使用 Deepseek API 自动翻译文档的功能：

1. 将原始英文 Markdown 文件放在 `data/markdown` 目录下
2. 配置 Deepseek API 密钥（在 `.env` 文件中）
3. 运行翻译脚本：
```bash
python src/translate/translate_docs.py
```

翻译后的文件将保存在 `docs/zh-CN` 目录下，保持原始目录结构。

### 翻译特性
- 保持 Markdown 格式
- 保留代码块、标题和列表格式
- 智能分段翻译
- 显示翻译进度
- 错误处理和日志记录

## 贡献

欢迎贡献！请随时提交 Pull Request。我们鼓励：
- 翻译改进
- 技术准确性更新
- 添加更多示例和用例
- 错误修复和更正

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件。

## 致谢

- 原始文档：[GitLab 企业数据平台](https://handbook.gitlab.com/handbook/enterprise-data/platform/)
- GitLab 团队提供的优秀文档
- 本翻译项目的贡献者和维护者 