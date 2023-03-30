from functools import reduce

from model.detector import Detector
import copy
import re


# def extend_op(ops, text):
#     reduce_words = [('and ', ''), ('or ', ''), ('either ', '')]
#     # clean ops
#     res = set([re.sub(r'[^\w\s]', '', reduce(lambda s,r: s.replace(*r), reduce_words, op)) for op in ops])
#
#     # add new elements
#     for t in re.split(',|and|or|either', text):
#         t = re.sub(r'[^\w\s]','',t)
#         res.add(reduce(lambda s,r: s.replace(*r), reduce_words, t).strip())
#     return list(filter(None, res))


class NP_BE_VALUE(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, doc=doc)
        rules = [
            [
                {
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS + ["VERB"]}}
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_words",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]}}
                },
                {
                    "LEFT_ID": "anchor_words",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}}
                }
            ],
            [
                {
                    "RIGHT_ID": "anchor_words",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]}}
                },
                {
                    "LEFT_ID": "anchor_words",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "nsubj"},
                },
                {
                    "LEFT_ID": "anchor_words",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS + ['VERB']}, "DEP": {"NOT_IN": ["nsubj"]}}
                }
            ],
            # conj
            [
                {
                    "RIGHT_ID": "anchor_words",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]}}
                },
                {
                    "LEFT_ID": "anchor_words",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "nsubj"},
                },
                {
                    "LEFT_ID": "anchor_words",
                    "REL_OP": ">",
                    "RIGHT_ID": "sub",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS + ['VERB']}, "DEP": {"NOT_IN": ["nsubj"]}}
                },
                {
                    "LEFT_ID": "sub",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS + ['VERB']}, "DEP": "conj"}
                }
            ],
        #     default to
            [
                {
                    "RIGHT_ID": "default",
                    "RIGHT_ATTRS": {"LEMMA": "default"}
                },
                {
                    "LEFT_ID": "default",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS + ['VERB']}, "DEP": "nsubj"}
                },
                {
                    "LEFT_ID": "default",
                    "REL_OP": ".",
                    "RIGHT_ID": "to",
                    "RIGHT_ATTRS": {"LEMMA": "to"}
                },
                {
                    "LEFT_ID": "to",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS + ["ADV"]}}
                }
            ],
        #  np is the default
            [
                {
                    "RIGHT_ID": "default",
                    "RIGHT_ATTRS": {"LEMMA": "default"}
                },
                {
                    "LEFT_ID": "default",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS + ['VERB']}, "DEP": "nsubj"}
                },
                {
                    "LEFT_ID": "default",
                    "REL_OP": ".",
                    "RIGHT_ID": "to",
                    "RIGHT_ATTRS": {"LEMMA": "to"}
                },
                {
                    "LEFT_ID": "to",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}}
                }
            ],
            [
                {
                    "RIGHT_ID": "anchor_words",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]}}
                },
                {
                    "LEFT_ID": "anchor_words",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "nsubj"},
                },
                {
                    "LEFT_ID": "anchor_words",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": "the default"}
                }
            ],
        #     conj, the default
            [
                {
                    "RIGHT_ID": "anchor_words",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]}}
                },
                {
                    "LEFT_ID": "anchor_words",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "nsubj"},
                },
                {
                    "LEFT_ID": "anchor_words",
                    "REL_OP": ">>",
                    "RIGHT_ID": "conj_anchor_words",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]}, "DEP": "conj"}
                },
                {
                    "LEFT_ID": "conj_anchor_words",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": "the default"}
                }
            ],
        #     define
            [
                {
                    "RIGHT_ID": "anchor_define",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["define", "mark"]}}
                },
                {
                    "LEFT_ID": "anchor_define",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "nsubjpass"},
                },
                {
                    "LEFT_ID": "anchor_define",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_as",
                    "RIGHT_ATTRS": {"LEMMA": "as"}
                },
                {
                    "LEFT_ID": "anchor_as",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}}
                }
            ],
            [
                {
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}},
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ">",
                    "RIGHT_ID": "anchor_define",
                    "RIGHT_ATTRS": {"LEMMA": "define", "DEP": "acl"}
                },
                {
                    "LEFT_ID": "anchor_define",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_with",
                    "RIGHT_ATTRS": {"LEMMA": "with"}
                },
                {
                    "LEFT_ID": "anchor_with",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}}
                }
            ]
        ]
        self.add_pattern('dep', rules)

