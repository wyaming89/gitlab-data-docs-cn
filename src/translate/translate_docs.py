#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
import markdown
import re

# 加载环境变量
load_dotenv()

class DeepseekTranslator:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("请在 .env 文件中设置 DEEPSEEK_API_KEY")
        
        self.api_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def translate_text(self, text):
        """使用 Deepseek API 翻译文本"""
        prompt = f"""请将以下英文文本翻译成中文，保持专业性和准确性：

{text}

请直接返回翻译结果，不要包含任何解释或其他内容。"""

        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"翻译出错: {str(e)}")
            return text

    def translate_markdown(self, content):
        """翻译 Markdown 内容，保持格式"""
        # 分割 Markdown 内容为段落
        paragraphs = content.split('\n\n')
        translated_paragraphs = []

        for paragraph in tqdm(paragraphs, desc="翻译进度"):
            if not paragraph.strip():
                translated_paragraphs.append(paragraph)
                continue

            # 检查是否是代码块
            if paragraph.startswith('```'):
                translated_paragraphs.append(paragraph)
                continue

            # 检查是否是标题
            if paragraph.startswith('#'):
                translated_paragraphs.append(paragraph)
                continue

            # 检查是否是列表项
            if paragraph.strip().startswith(('-', '*', '+')):
                translated_paragraphs.append(paragraph)
                continue

            # 翻译普通文本
            translated = self.translate_text(paragraph)
            translated_paragraphs.append(translated)

        return '\n\n'.join(translated_paragraphs)

def process_markdown_files():
    """处理 data/markdown 目录下的所有 Markdown 文件"""
    translator = DeepseekTranslator()
    markdown_dir = Path("data/markdown")
    output_dir = Path("docs/zh-CN")
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 处理所有 Markdown 文件
    for md_file in markdown_dir.glob("**/*.md"):
        print(f"\n处理文件: {md_file}")
        
        # 读取文件内容
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 翻译内容
        translated_content = translator.translate_markdown(content)
        
        # 创建相对路径
        relative_path = md_file.relative_to(markdown_dir)
        output_path = output_dir / relative_path
        
        # 确保输出文件的目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存翻译后的文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(translated_content)
        
        print(f"已保存翻译文件: {output_path}")

if __name__ == "__main__":
    process_markdown_files() 