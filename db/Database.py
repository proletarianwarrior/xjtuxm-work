# -*- coding: utf-8 -*-
# @Time : 2023/9/16 20:10
# @Author : DanYang
# @File : Database.py
# @Software : PyCharm
import os
import sqlite3


class Database:
    def __init__(self, db_filepath):
        db_is_new = not os.path.exists(db_filepath)
        with sqlite3.connect(db_filepath) as self.conn:
            if db_is_new:
                print(f"\033[1;32mCreate database {db_filepath} successfully\033[0m")
            else:
                print(f"\033[1;32mDatabase {db_filepath} exists\033[0m")
        self.cursor = self.conn.cursor()

    def create_task(self, task_name, **columns):
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


if __name__ == '__main__':
    database = Database("../database/xjtu.db")






