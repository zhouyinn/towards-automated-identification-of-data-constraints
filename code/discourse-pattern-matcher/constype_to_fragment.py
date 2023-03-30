import json
from model.discourse_pattern import DiscoursePattern
from eval_type import get_start
import argparse
import multiprocessing


class Fragment:
    def __init__(self, system, file, sentence, s_start, data_source, fragment, discourse_pattern, operands, constraint_type,
                 matched_constraint):
        self.system = system
        self.file = file
        self.sentence = sentence
        self.s_start = s_start
        self.data_source = data_source
        self.fragment = fragment
        self.discourse_pattern = discourse_pattern
        self.operands = operands
        self.constraint_type = constraint_type
        self.matched_constraint = matched_constraint


def neg_task(item):
    fs = []
    for f in item["fragments"]:
        discouse_pattern = DiscoursePattern(pattern_name=f["pattern_name"],
                                            fragment=f["fragment"],
                                            operands=f["operands"],
                                            doc=None,
                                            text=item["sentence"],
                                            start=get_start(item["sentence"], f["fragment"]),
                                            end=-1)
        fragment = Fragment(system=item['system'],
                            file=item['file'],
                            sentence=item['sentence'],
                            s_start=item['start'] if 'start' in item else None,
                            data_source="23S-Neg-Sentences",
                            fragment=f["fragment"],
                            discourse_pattern=f["pattern_name"],
                            operands=f["operands"],
                            constraint_type=discouse_pattern.pattern_type,
                            matched_constraint=None)
        fs.append(fragment)
    return fs

def pos_task(item):
    discouse_pattern = DiscoursePattern(pattern_name=item["discourse_pattern"],
                                        fragment=item["fragment"],
                                        operands=item["operands"],
                                        doc=None,
                                        text=item["sentence"],
                                        start=get_start(item["sentence"], item["fragment"]),
                                        end=-1)
    item['constraint_type'] = discouse_pattern.pattern_type
    return item


def get_constraint_type_neg(in_path):
    data = json.load(open(in_path, 'r'))
    res = []
    with multiprocessing.Pool() as pool:
        for result in pool.map(neg_task, data):
            res.extend(result)
    json.dump([ob.__dict__ for ob in res], open('fragments_with_constype.json', 'w'))


def get_constraint_type_pos(in_path):
    data = json.load(open(in_path, 'r'))
    res = []
    with multiprocessing.Pool() as pool:
        for result in pool.map(pos_task, data):
            res.append(result)
    json.dump(res, open('fragments_with_constype.json', 'w'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-in', '--input', dest='in_json')
    parser.add_argument('-p', '--positive', action='store_true', default=False, dest='is_positive')  # option that takes a value
    args = parser.parse_args()
    if args.is_positive:
        get_constraint_type_pos(args.in_json)
    else:
        get_constraint_type_neg(args.in_json)
