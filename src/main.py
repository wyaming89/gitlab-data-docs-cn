# -*- coding: utf-8 -*-

import os
import asyncio
import httpx
from bs4 import BeautifulSoup
import html2text
from tqdm import tqdm
from urllib.parse import urljoin, urlparse
import re
import time
from typing import Optional
import aiofiles
from pathlib import Path

class GitLabDocScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.body_width = 0
        self.client = httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            verify=False,  # 禁用SSL验证
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )
        self.visited_urls = set()
        self.max_retries = 3
        self.retry_delay = 2  # 重试延迟秒数
        self.image_dir = 'data/images'
        os.makedirs(self.image_dir, exist_ok=True)
        
    async def get_page_content(self, url: str, retry_count: int = 0) -> Optional[str]:
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            if retry_count < self.max_retries:
                print(f"尝试 {retry_count + 1}/{self.max_retries} 失败: {url}")
                print(f"错误信息: {str(e)}")
                print(f"等待 {self.retry_delay} 秒后重试...")
                await asyncio.sleep(self.retry_delay)
                return await self.get_page_content(url, retry_count + 1)
            else:
                print(f"获取页面失败，已达到最大重试次数: {url}")
                print(f"最终错误: {str(e)}")
                return None

    async def download_image(self, img_url: str, img_path: str) -> bool:
        try:
            response = await self.client.get(img_url)
            response.raise_for_status()
            
            # 确保目录存在
            os.makedirs(os.path.dirname(img_path), exist_ok=True)
            
            # 保存图片
            async with aiofiles.open(img_path, 'wb') as f:
                await f.write(response.content)
            return True
        except Exception as e:
            print(f"下载图片失败 {img_url}: {str(e)}")
            return False

    def convert_to_markdown(self, html_content):
        return self.h2t.handle(html_content)

    def save_markdown(self, content, filepath):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            print(f"保存文件失败 {filepath}: {str(e)}")

    def sanitize_filename(self, filename):
        # 移除非法字符，将空格替换为下划线
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.replace(' ', '_')
        return filename

    def extract_link_text(self, link):
        # 提取链接文本，移除markdown格式
        text = link.get_text().strip()
        # 移除markdown格式的链接文本
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        return text

    async def process_images(self, soup, current_url: str, current_path: str) -> str:
        # 查找所有图片
        images = soup.find_all('img')
        for img in images:
            src = img.get('src')
            if not src:
                continue
                
            # 构建完整的图片URL
            img_url = urljoin(current_url, src)
            
            # 生成图片文件名
            img_filename = self.sanitize_filename(os.path.basename(src))
            img_path = os.path.join(self.image_dir, current_path, img_filename)
            
            # 下载图片
            if await self.download_image(img_url, img_path):
                # 更新图片src为相对路径
                relative_path = os.path.join('..', '..', 'images', current_path, img_filename)
                img['src'] = relative_path.replace('\\', '/')
        
        return str(soup)

    def extract_content(self, soup):
        # 查找td_content div
        content_div = soup.find('div', class_='td-content')
        if not content_div:
            return None
            
        # 移除不需要的元素
        for element in content_div.find_all(['script', 'style']):
            element.decompose()
            
        # 移除所有class属性
        for element in content_div.find_all(True):
            if 'class' in element.attrs:
                del element['class']
                
        return content_div

    async def process_page(self, url):
        if url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        print(f"正在处理页面: {url}")
        
        html_content = await self.get_page_content(url)
        if not html_content:
            return

        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 获取页面标题
            title = soup.find('h1')
            if title:
                title = title.get_text().strip()
            else:
                title = urlparse(url).path.split('/')[-1]

            # 提取主要内容
            content_div = self.extract_content(soup)
            if not content_div:
                print(f"未找到主要内容: {url}")
                return

            # 处理图片
            current_path = urlparse(url).path.lstrip('/')
            content_html = await self.process_images(content_div, url, current_path)

            # 转换内容为Markdown
            markdown_content = self.convert_to_markdown(content_html)
            
            # 保存文件
            filepath = os.path.join('data', 'markdown', current_path, 'index.md')
            self.save_markdown(markdown_content, filepath)
            
            # 查找所有链接
            links = soup.find_all('a', href=True)
            tasks = []
            
            for link in links:
                href = link.get('href')
                if not href:
                    continue
                    
                # 构建完整URL
                full_url = urljoin(url, href)
                
                # 检查是否是同一域名下的链接
                if not full_url.startswith(self.base_url):
                    continue
                    
                # 提取链接文本作为文件名
                link_text = self.extract_link_text(link)
                if not link_text:
                    continue
                    
                # 创建文件名
                filename = self.sanitize_filename(link_text)
                
                # 保存链接内容
                link_content = await self.get_page_content(full_url)
                if link_content:
                    link_soup = BeautifulSoup(link_content, 'html.parser')
                    link_content_div = self.extract_content(link_soup)
                    if link_content_div:
                        # 处理子页面的图片
                        link_content_html = await self.process_images(link_content_div, full_url, current_path)
                        link_markdown = self.convert_to_markdown(link_content_html)
                        link_filepath = os.path.join('data', 'markdown', current_path, f"{filename}.md")
                        self.save_markdown(link_markdown, link_filepath)
                        
                        # 递归处理子页面
                        tasks.append(self.process_page(full_url))
            
            # 等待所有子任务完成
            if tasks:
                await asyncio.gather(*tasks)
            
            return title
        except Exception as e:
            print(f"处理页面时出错 {url}: {str(e)}")
            return None

    async def scrape(self):
        print("开始抓取GitLab企业数据平台文档...")
        try:
            await self.process_page(self.base_url)
            print("文档抓取完成！")
        except Exception as e:
            print(f"抓取过程中出错: {str(e)}")
        
    async def close(self):
        try:
            await self.client.aclose()
        except Exception as e:
            print(f"关闭客户端时出错: {str(e)}")

async def main():
    base_url = "https://handbook.gitlab.com/handbook/enterprise-data/platform/"
    scraper = GitLabDocScraper(base_url)
    try:
        await scraper.scrape()
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main()) 