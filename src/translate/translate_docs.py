#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
import markdown
import re
import asyncio
from openai import OpenAI

# 加载环境变量
load_dotenv()

class DeepseekTranslator:
    def __init__(self):
        self.api_key = os.getenv('DEEPSEEK_API_KEY')
        if not self.api_key:
            raise ValueError("请在 .env 文件中设置 DEEPSEEK_API_KEY")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )

    async def translate_text(self, text):
        """使用 Deepseek API 翻译文本"""
        messages = [
            {
                "content": """你是一个专业的翻译助手，请将内容翻译成中文。
请遵循以下规则：
1. 保持 Markdown 格式不变
2. 保持代码块、标题、列表等特殊格式不变
3. 保持专业术语的准确性
4. 翻译要通顺自然
5. 不要添加任何解释或注释
6. 直接返回翻译后的文本
7. 确保返回的是中文内容""",
                "role": "system"
            },
            {
                "content": text,
                "role": "user"
            }
        ]

        try:
            print("发送翻译请求...")
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                temperature=0.3,
                max_tokens=4096,
                stream=False
            )
            
            translated_text = response.choices[0].message.content.strip()
            
            # 检查翻译结果是否包含中文
            if not any('\u4e00' <= char <= '\u9fff' for char in translated_text):
                print("警告：翻译结果似乎不包含中文字符！")
                print("翻译结果预览:", translated_text[:200])
                return text  # 如果翻译结果不包含中文，返回原文
            
            return translated_text
        except Exception as e:
            print(f"翻译出错: {str(e)}")
            print("错误详情:", e.__class__.__name__)
            return text

    async def translate_markdown(self, content):
        """翻译整个 Markdown 文档"""
        print("开始翻译文档...")
        print("文档长度:", len(content), "字符")
        translated_content = await self.translate_text(content)
        print("翻译完成")
        print("翻译后长度:", len(translated_content), "字符")
        return translated_content

async def process_markdown_files():
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
        translated_content = await translator.translate_markdown(content)
        
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
    asyncio.run(process_markdown_files()) 