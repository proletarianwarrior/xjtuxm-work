# -*- coding: utf-8 -*-
# @Time : 2023/9/16 16:40
# @Author : DanYang
# @File : process.py
# @Software : PyCharm
import os
import asyncio

from db.Database import Database
from crawler.Crawler import Crawler


# 获取爬虫数据结果
def crawl_data():
    xjtu_crawler = Crawler()
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(xjtu_crawler.main())


# 数据库初始化
def create_database(file_path, task_name):
    if not os.path.exists(file_path):
        database = Database(file_path)
        database.create_task(task_name,
                             **{
                                 "id": "INT PRIMARY KEY NOT NULL",
                                 "title": "TEXT NOT NULL",
                                 "date": "DATE NOT NULL",
                                 "link": "TEXT NOT NULL",
                             })
    else:
        database = Database(file_path)
    return database


# 指定总初始化
def main_process(file_path, task_name):
    database = create_database(file_path, task_name)
    data = crawl_data()
    for d in data:
        print(d)
        database.insert_data(task_name, **d)
    print("\033[94mThe database has been successfully initialized\033[0m")


if __name__ == '__main__':
    main_process("./database/xjtu.db", "xjtuEA")

