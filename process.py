# -*- coding: utf-8 -*-
# @Time : 2023/9/16 16:40
# @Author : DanYang
# @File : run.py
# @Software : PyCharm
import os
import asyncio

from app.Database import Database
from crawler.Crawler import Crawler


def crawl_data():
    xjtu_crawler = Crawler()
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(xjtu_crawler.main())


def create_database(file_path, task_name):
    if not os.path.exists(file_path):
        data = crawl_data()
        database = Database(file_path)
        for d in data:
            database.insert_data(task_name, data=d)
    else:
        database = Database(file_path)
    return database


if __name__ == '__main__':
    

