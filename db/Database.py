# -*- coding: utf-8 -*-
# @Time : 2023/9/16 20:10
# @Author : DanYang
# @File : Database.py
# @Software : PyCharm
import os
import sqlite3


class Database:
    """
    这个类用于对数据库进行初始化，插入，搜索功能的实现
    """
    def __init__(self, db_filepath):
        db_is_new = not os.path.exists(db_filepath)
        with sqlite3.connect(db_filepath) as self.conn:
            if db_is_new:
                print(f"\033[1;32mCreate database {db_filepath} successfully\033[0m")
            else:
                print(f"\033[1;32mDatabase {db_filepath} exists\033[0m")
        self.cursor = self.conn.cursor()

    def create_task(self, task_name, **columns):
        """
        这个函数用于在数据库中创建表单并设置表单列的名称
        :param task_name: 任务名称
        :param columns: 表单的列
        :return: None
        """
        command_string = "CREATE TABLE IF NOT EXISTS "
        task_string = "{task_name}({column_list})"
        column_list = []
        for key, value in columns.items():
            column_list.append(f"{key} {value}")
        command_string = command_string + task_string.format(task_name=task_name, column_list=",".join(column_list))

        try:
            self.conn.execute(command_string)
            self.conn.commit()
        except Exception as error:
            print("\033[91mException in the creation of a task\033[0m")
            print(error)

    def insert_data(self, task_name, **data):
        """
        这个函数用于将数据插入数据库中
        :param task_name: 任务名称
        :param data: 插入的数据
        :return: None
        """
        command_string = "INSERT INTO "
        task_string = "{task_name}({key_list}) values({value_list})"

        key_list = [str(i) for i in list(data.keys())]
        value_list = ["\"" + str(i) + "\"" if isinstance(i, str) else str(i) for i in list(data.values())]

        command_string = command_string + task_string.format(task_name=task_name,
                                                             key_list=",".join(key_list),
                                                             value_list=",".join(value_list))

        try:
            self.conn.execute(command_string)
            self.conn.commit()
        except Exception as error:
            print("\033[91mException when inserting data\033[0m")
            print(error)

    def select_data(self, v_names, task_name, condition):
        """
        这个函数用于根据列名，搜索条件在指定任务中搜索数据
        :param v_names: 列名
        :param task_name: 任务名
        :param condition: 条件
        :return: 搜索结果
        """
        v_names = ",".join(v_names)
        if condition:
            command_string = "SELECT {v_names} FROM {task_name} WHERE {condition}".format(
                v_names=v_names,
                task_name=task_name,
                condition=condition
            )
        else:
            command_string = "SELECT {v_names} FROM {task_name}".format(
                v_names=v_names,
                task_name=task_name
            )
        self.cursor.execute(command_string)
        search_result = self.cursor.fetchall()

        return search_result


if __name__ == '__main__':
    database = Database("../database/xjtu.db")
    data = database.select_data("*", "xjtuEA", "id BETWEEN 1 AND 15")
    print(data)
