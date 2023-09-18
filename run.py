# -*- coding: utf-8 -*-
# @Time : 2023/9/17 21:33
# @Author : DanYang
# @File : run.py
# @Software : PyCharm
from datetime import datetime

from flask import render_template, Flask, request

from db.Database import Database
from db.DataSearch import cut_word, call_similarities

app = Flask(__name__)
global filter_data

HOST = "127.0.0.1"
PORT = 8080


@app.route("/")
def index():
    global data, vectorizer, tfidf_matrix, filter_data
    database = Database("./database/xjtu.db")
    data = database.select_data("*", "xjtuEA", None)
    data = [dict(zip(("id", "title", "date", "link"), i)) for i in data]
    filter_data = data.copy()

    return render_template("index.html", data=data)


@app.route("/filter", methods=["POST"])
def filter_date():
    global filter_data
    filter_data = data.copy()
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    if not (start_date and end_date):
        return render_template("index.html", data=data)

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    filter_data = []
    for d in data:
        date_obj = datetime.strptime(d["date"], "%Y-%m-%d")
        if start_date <= date_obj <= end_date:
            filter_data.append(d)
    return render_template("index.html", data=filter_data)


@app.route("/search", methods=["POST"])
def search_data():
    key_word = request.form.get("key_word")
    vectorizer, tfidf_matrix = cut_word(filter_data)
    similarities = call_similarities(vectorizer, tfidf_matrix, key_word)

    return render_template("index.html", data=[filter_data[i] for i in similarities])


app.run(HOST, PORT, debug=True)
