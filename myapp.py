# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from collections import Counter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')


app = Flask(__name__)
try:
    df = pd.read_csv('results.csv')
except FileNotFoundError:
    df = pd.DataFrame({'age': [], 'gender': [], 'education': [], 'word': []})
    df.to_csv('results.csv')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/stats')
def stats():
    try:
        os.remove('/static/plot.png')
    except OSError:
        pass
    input_df = pd.read_csv('results.csv')
    try:
        contents = dict(respondents_number=len(input_df),
                        min_age=input_df.age.min(),
                        max_age=input_df.age.max(),
                        mean_age=round(input_df.age.mean()),
                        url='static/plot.png')
    except ValueError:
        return render_template('no_stats.html')
    labels, values = zip(*Counter(input_df['word']).items())
    indexes = np.arange(len(labels))
    width = 0.5
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.savefig('static/plot.png')
    return render_template('stats.html', **contents)


@app.route('/process', methods=['get'])
def answer_process():
    gender = request.args.get('gender')
    education = request.args.get('education')
    age = request.args.get('age')
    word = request.args.get('word')
    if age == '':
        return redirect(url_for('form'))
    word_dict = {'lastik': 'Ластик', 'sterka': 'Стёрка', 'rezinka': 'Резинка'}
    df.loc[len(df.index)] = [age, gender, education, word_dict[word]]
    df.to_csv('results.csv', index=False)
    return redirect(url_for('spasibo'))


@app.route('/spasibo')
def spasibo():
    return render_template('spasibo.html',)


if __name__ == '__main__':
    app.run(debug=False)
