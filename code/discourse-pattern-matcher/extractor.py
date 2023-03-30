import inspect
import copy
import argparse
from model.detector import Detector
from pathlib import Path
import detect.noun_phrase
from utils.nlp_factory import nlps
from detect.noun_phrase import VALUE_FOR_NP, NP_OF_VALUE, CD_NP, NP_CD
from detect.np_be_binary_value import NP_BE_BINARY_VALUE
from detect.np_be_value import NP_BE_VALUE
from detect.np_if_binary_value import NP_IF_BINARY_VALUE
from detect.np_cd_to_cd import NP_CD_TO_CD
from detect.set_np_to_binary_value import SET_NP_TO_BINARY_VALUE
from detect.set_np_to_value import SET_NP_TO_VALUE
from detect.np_same_as_np import NP_SAME_AS_NP
from detect.np_comp_np import NP_COMP_NP
from detect.np_exist import NP_EXIST
from pymongo import MongoClient
from ssh_pymongo import MongoSession
from detect.np_in_valueset import NP_IN_VALUESET
from detect.np_set_to_value import NP_SET_TO_VALUE
from detect.np_set_to_binary_value import NP_SET_TO_BINARY_VALUE
import warnings
import spacy
import json
import sys
import multiprocessing
import pandas as pd

warnings.filterwarnings('ignore')
npcls_members = [c[1] for c in inspect.getmembers(detect.noun_phrase, inspect.isclass)
                  if c[1].__module__ == 'detect.noun_phrase']
EXCLUDED_SYSTEMS = ["jpos-2.1.4", "skywalking-8.0.1", "rhino-1.6R5", "guava-28.0",
                   "shardingsphere-5.0.0-rc1", "mybatis-3.5.5"]


def is_excluded(sentence):
    if sentence["system"] not in EXCLUDED_SYSTEMS:
        return True
    return False


def merge_noun_phrase_for_fragment(res):
    doc = None
    res = list(res)
    res.sort(key=lambda x: x.end, reverse=True)
    for r in res:
        try:
            if r.start != -1 and r.end != 1 and r.start != r.end:
                if doc is None:
                    doc = copy.deepcopy(r.doc)
                with doc.retokenize() as retokenizer:
                    retokenizer.merge(doc[r.start:r.end])
        except ValueError:
            # print(' | '.join([token.text for token in doc]), r, r.start, r.end)
            continue
    return doc


def merge_np_for_text(text):
    res = set()
    doc = None
    for subclass in npcls_members:
        detector = subclass(text, doc)
        r = detector.match()
        if r is None:
            continue

        merged = merge_noun_phrase_for_fragment(r)
        if merged is not None:
            doc = merged
        res.update(r)
    return doc, res


def collect_sentence(in_json):
    sentences = {}
    key_col = ['system', 'file', 'sentence']
    for item in json.loads(pd.read_csv(in_json).to_json(orient='records')):
        if not is_excluded(item):
            continue
        key = '#'.join([str(item[k]) for k in key_col if k in item and item[k] is not None])
        if key not in sentences:
            sent = {k: item[k] for k in key_col if k in item}
            sentences[key] = sent
    return sentences


def run_detector(text):
    doc, res = merge_np_for_text(text)
    for subclass in Detector.__subclasses__():
        if subclass in npcls_members:
            continue
        detector = subclass(text, doc)
        r = detector.match()
        if r is None:
            continue
        res.update(r)
    return res


def task(sent):
    try:
        fragments = [{'pattern_name': r.pattern_name,
                      'fragment': str(r.fragment),
                      'operands': ', '.join(r.operands).replace(',,', ',')} for r in run_detector(sent['sentence'])]
        sent['fragments'] = fragments
        return sent
    except:
        return sent['sentence']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-in', '--input', dest='in_json')
    args = parser.parse_args()
    res = []
    sentences = collect_sentence(args.in_json)
    with multiprocessing.Pool() as pool:
        for result in pool.map(task, sentences.values()):
            if type(result) == str:
                print(result)
            else:
                res.append(result)
    json.dump(res, open('out_fragments.json', 'w'))

