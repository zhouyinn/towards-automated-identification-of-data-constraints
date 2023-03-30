import spacy
import multiprocessing
import pandas as pd
import json

nlp = spacy.load("en_core_web_sm")
EXCLUDED_SYSTEMS = ["jpos-2.1.4", "skywalking-8.0.1", "rhino-1.6R5", "guava-28.0",
                   "shardingsphere-5.0.0-rc1", "mybatis-3.5.5"]


def is_excluded(constraint):
    """
    :param constraint
    :return: whether to exclude constraints during preprocessing
    """
    if constraint["poorly_written"] == "well-written" and \
        constraint["system"] not in EXCLUDED_SYSTEMS and \
        constraint["filter"] is None:
        return True
    return False


def get_npos(text, n):
    res = []
    tokens = [t.pos_ for t in nlp(text)]
    for i in range(1, n + 1):
        for j in range(len(tokens) - i + 1):
            res.append(' '.join(tokens[j:j + i]))
    return res


def get_ngrams(text, n):
    res = []
    tokens = text.split()
    for i in range(1, n + 1):
        for j in range(len(tokens) - i + 1):
            res.append(' '.join(tokens[j:j + i]))
    return res


def pos_task(cons):
    if not is_excluded(cons): return None
    return {
        "label": 1,
        "_id": cons['_id'],
        "system": cons['system'],
        "file": cons['file'],
        "sentence": cons['sentence'],
        "fragment": cons['constraint_text'],
        "dispat": cons['discourse_pattern'],
        "operands": cons['operands'],
        "constraint_type": cons["constraint_type"],
        "f_npos": get_npos(cons['constraint_text'], 3),
        "f_ngrams": get_npos(cons['constraint_text'], 3),
        "s_npos": get_npos(cons['sentence'], 3),
        "s_ngrams": get_ngrams(cons['sentence'], 3),
        "o_npos": get_npos(cons['operands'], 3),
        "o_ngrams": get_npos(cons['operands'], 3),
    }


def neg_task(item):
    if item["system"] in EXCLUDED_SYSTEMS: return None
    return {
        "label": 0,
        "_id": None,
        "system": item['system'],
        "file": item['file'],
        "sentence": item['sentence'],
        "fragment": item['fragment'],
        "dispat": item['discourse_pattern'],
        "operands": item['operands'],
        "constraint_type": item["constraint_type"],
        "f_npos": get_npos(item['fragment'], 3),
        "f_ngrams": get_npos(item['fragment'], 3),
        "s_npos": get_npos(item['sentence'], 3),
        "s_ngrams": get_ngrams(item['sentence'], 3),
        "o_npos": get_npos(item['operands'], 3),
        "o_ngrams": get_npos(item['operands'], 3),
    }


def preprocess_data(in_pos, in_neg):
    res = []
    pos_data = json.loads(pd.read_csv(in_pos).to_json(orient='records'))
    neg_data = json.loads(pd.read_csv(in_neg).to_json(orient='records'))
    with multiprocessing.Pool() as pool:
        for result in pool.map(pos_task, pos_data):
            if result is not None: res.append(result)
    with multiprocessing.Pool() as pool:
        for result in pool.map(neg_task, neg_data):
            if result is not None: res.append(result)
    json.dump(res, open('data.json', 'w'))


if __name__ == '__main__':
    params = json.load(open('../in/config.json', 'r'))
    preprocess_data(params['in_pos'], params['in_neg'])
