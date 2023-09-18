# -*- coding: utf-8 -*-
# @Time : 2023/9/16 20:57
# @Author : DanYang
# @File : Crawler.py
# @Software : PyCharm
import re
import asyncio

import aiohttp
from tenacity import retry, stop_after_attempt, wait_fixed
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 每页的信息数量
STEP = 15
# 最大页数
MAX_NUM = 208
PAGE = ("",) + tuple(range(1, MAX_NUM))[::-1]
# 协程运行的最大任务量
MAX_TASKS = 5
BASE_URL = "http://dean.xjtu.edu.cn/jxxx/xytz/"


class Crawler:
    """
    这个类用来爬取xjtu教务处官网的学业通知相关信息，爬取内容为标题，日期，链接
    """
    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.132 Safari/537.36',
        }
        self.semaphore = asyncio.Semaphore(MAX_TASKS)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1), reraise=True)
    async def get_html(self, url):
        """
        这是一个根据网址爬取html源码的函数
        :param url: 爬取的网站
        :return: 爬取的html源码
        """
        async with self.semaphore:
            print(f"\033[32mScraping {url} ... ...\033[0m")
            try:
                response = await self.session.get(url, headers=self.headers)
            except Exception as error:
                print(f"\033[91mException while crawling {url}\033[0m")
                print(error)
                return
            return await response.text()

    async def parse_html(self, url):
        """
        这是一个根据网址获取爬取数据并对数据进行解析的函数
        :param url: 爬取的网址
        :return: 解析的结果
        """
        text = await self.get_html(url)
        num = re.search("(\d+)", url)
        num = 0 if not num else MAX_NUM - int(num.group(1))
        soup = BeautifulSoup(text, "lxml")

        pattern_dict = {
            "title": "div>div.list-li>a",
            "date": "div>div.list-li>span",
            "link": "div>div.list-li>a",
        }
        result_data = []

        for name, pattern in pattern_dict.items():
            result = soup.select(pattern)
            result = result[6:21] if len(result) == 29 else result
            if name == "title" or name == "date":
                result_data.append([r.text for r in result])
            elif name == "link":
                result_data.append([r["href"] for r in result])
        result_data.insert(0, list(range(num * STEP + 1, num * STEP + len(result) + 1)))

        result_json = []
        for data in zip(*result_data):
            result = dict(zip(["id", "title", "date", "link"], data))
            result_json.append(result)
        return result_json

    def create_page_url(self, url, page):
        if page:
            new_url = urljoin(url, f"{page}.htm")
        else:
            return url[:-1] + ".htm"
        return new_url

    async def main(self):
        urls = [self.create_page_url(BASE_URL, p) for p in PAGE]
        tasks = [self.parse_html(url) for url in urls]
        results = await asyncio.gather(*tasks)
        new_results = []
        for pos, r in enumerate(results):
            new_results.extend(r)
        await self.session.close()
        return new_results


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    d = Crawler()
    result = loop.run_until_complete(d.main())
