# -*- coding: utf-8 -*-
# @Time : 2023/9/18 13:42
# @Author : DanYang
# @File : DataSearch.py
# @Software : PyCharm
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# jieba分词
def tokenize(text):
    return " ".join(jieba.cut(text))


# 生成tfidf矩阵和特征向量
def cut_word(words):
    tokenized_titles = [tokenize(title["title"]) for title in words]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(tokenized_titles)

    return vectorizer, tfidf_matrix


# 计算指定关键词和每条数据的相似度并给出排序结果
def call_similarities(vectorizer, tfidf_matrix, key_word):
    user_query_vector = vectorizer.transform([tokenize(key_word)])
    similarities = cosine_similarity(user_query_vector, tfidf_matrix)
    sorted_indices = similarities.argsort()[0][::-1]

    return sorted_indices

