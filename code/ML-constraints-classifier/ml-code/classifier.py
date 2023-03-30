#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import json
import os
from sklearn import naive_bayes, svm
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier
import warnings
from sklearn.metrics import confusion_matrix
from pathlib import Path
from MLExpr import MLExpr
from feature_extractor import Processor
from util import evaluation_report, data_info
from datetime import datetime
import time

SYSTEMS = ["apache-ant-1.10.6", "apache-httpcomponents-4.5.9", "argouml-0.35.4", "jedit-5.6pre0",
           "joda_time-2.10.3", "swarm-2.8.11", "checkstyle-8.35", "jabref-5.0", "log4j-2.13.3"]
CSV_COLUMNS = ["model", "system", "best_params", "precision", "recall", "f1",
           "accuracy", "tp", "fp", "tn", "fn", "num_train", "num_pos_trn", "num_neg_trn", "num_test",
           "num_pos_test", "num_neg_test"]
REPEATED_TIMES, SPLIT_TIMES = None, None


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


def printf(*arg, **kwarg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    print(timestamp, *arg, **kwarg)


def launch_model(modelName, x_train, y_train, x_test):
    printf("Start running model {}...".format(modelName))

    if modelName == "linear_svc":
        param_grid = {'C': [0.1, 1, 10],
                      'penalty': ['l1', 'l2']}
        grid = GridSearchCV(svm.LinearSVC(), param_grid, scoring="f1", cv=SPLIT_TIMES, n_jobs=-1)

    if modelName == "nu_svc":
        clf = svm.SVC(kernel = 'rbf')
        clf.fit(x_train, y_train)
        y_pred = clf.predict(x_test)
        return None, y_pred

    elif modelName == "nb_multinomial":
        param_grid = {
            "alpha": [0.0, 0.005, 0.01, 0.1, 0.5, 1.0, 2.0]
        }
        grid = GridSearchCV(naive_bayes.MultinomialNB(), param_grid, scoring="f1", cv=SPLIT_TIMES, n_jobs=-1)

    elif modelName == "randomForest":
        param_grid = {
            'n_estimators': [10, 50, 100],
            'max_features': ['sqrt', 'log2', 0.1, 0.5],
            'max_depth': [5, 6, 7, 8, 9, 10],
            'criterion': ['gini', 'entropy']
        }

        rf = RandomForestClassifier()
        grid = GridSearchCV(rf, param_grid, scoring="f1", cv=SPLIT_TIMES, n_jobs=-1)

    elif modelName == "decisionTree":
        param_grid = {
            'criterion': ['gini', 'entropy'],
            'splitter': ['best', 'random'],
            'max_depth': [6, 8, 10]
        }
        dt = DecisionTreeClassifier()
        grid = GridSearchCV(dt, param_grid, scoring="f1", cv=SPLIT_TIMES, n_jobs=-1)

    elif modelName == "logisticRegression":
        param_grid = {
            "C": [0.01, 0.1, 1, 5, 10, 15, 20],
            "penalty": ["l1", "l2"],
            "solver": ["liblinear"]
        }
        lr = LogisticRegression()
        grid = GridSearchCV(lr, param_grid, scoring="f1", cv=SPLIT_TIMES, n_jobs=-1)

    grid.fit(x_train, y_train)
    best_params = grid.best_params_
    y_pred = grid.predict(x_test)
    return best_params, y_pred


def preprocess(expr):
    dataLists = {}
    df = expr.df
    # cross-system
    for system in SYSTEMS:
        test_index = df.index[df['system'] == system].tolist()
        train_index = df.index[df['system'] != system].tolist()
        processor = Processor(train_index=train_index, test_index=test_index, expr=expr, df=df)
        x_train, y_train, x_test, y_test = processor.transform_data()
        dataLists['cross-{}'.format(system)] = [x_train, y_train, x_test, y_test]

    # randomly
    key_cols = ['system', 'file', 'sentence']
    gss = GroupShuffleSplit(n_splits=REPEATED_TIMES, train_size=.7)
    for i, (train_index, test_index) in enumerate(gss.split(df, df['label'], df[key_cols].astype(str).agg('-'.join, axis=1))):
        processor = Processor(train_index=train_index, test_index=test_index, expr=expr, df=df)
        x_train, y_train, x_test, y_test = processor.transform_data()
        dataLists['{}-fold_{}'.format(SPLIT_TIMES, i)] = [x_train, y_train, x_test, y_test]
    return dataLists


def run(expr: MLExpr, out_dir):
    warnings.filterwarnings('ignore')
    dataLists = preprocess(expr)
    df = pd.DataFrame(columns=["model", "system", "best_params", "precision", "recall", "f1",
                               "accuracy", "tp", "fp", "tn", "fn", "num_train", "num_pos_trn", "num_neg_trn",
                               "num_test",
                               "num_pos_test", "num_neg_test"])
    for system, data in dataLists.items():
        x_train, y_train, x_test, y_test = data
        for modelName in expr.models:
            best_params, y_pred = launch_model(modelName, x_train, y_train, x_test)
            tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
            record = [modelName, system, best_params] + \
                     evaluation_report(y_test, y_pred) + \
                     [tp, fp, tn, fn] + \
                     data_info(y_train, y_test)
            df.loc[len(df)] = record
    df.to_csv(expr.get_out_dir(out_dir) + ".csv", index=False)


if __name__ == '__main__':
    params = json.load(open('../in/config.json', 'r'))
    exprs = []
    REPEATED_TIMES, SPLIT_TIMES = params['times'], params['split_times']
    df = pd.DataFrame(json.load(open(params["data"], 'r')))
    for i in params['experiment']:
        exprs.append(MLExpr(df=df,
                            models=i['models'],
                            use_frag=i['use_frag'],
                            use_sent=i['use_sent'],
                            use_dispat=i['use_dispat'],
                            use_op=i['use_operands'],
                            use_ct=i['use_ct'],
                            smote_ratio=i['smote_ratio']))
        out_dir = 'result/{}'.format(datetime.now().strftime('%m%d%H%M%S'))
        Path(out_dir).mkdir(parents=True, exist_ok=True)
        for i in exprs:
            start = time.time()
            print('[start running]', i)
            run(i, out_dir)
            print("time elapsed", time.time() - start)
