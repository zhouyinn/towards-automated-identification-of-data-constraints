from model.detector import Detector, is_digit, preprocess_doc
from utils.nlp_factory import nlps
from model.discourse_pattern import DiscoursePattern
from quantulum3 import parser
import re


class NP_OF_VALUE(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, doc=doc)
        rules = [
            [
                {
                    "RIGHT_ID": "anchor_of",
                    "RIGHT_ATTRS": {"LEMMA": "of"}
                },
                {
                    "LEFT_ID": "anchor_of",
                    "REL_OP": ";",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}},
                },
                {
                    "LEFT_ID": "anchor_of",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}},
                },
            ],
            [
                {
                    "RIGHT_ID": "anchor_of",
                    "RIGHT_ATTRS": {"LEMMA": "of"}
                },
                {
                    "LEFT_ID": "anchor_of",
                    "REL_OP": ";",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}},
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}, "DEP": "conj"},
                },
            ],
            [
                {
                    "RIGHT_ID": "anchor_of",
                    "RIGHT_ATTRS": {"LEMMA": "of"}
                },
                {
                    "LEFT_ID": "anchor_of",
                    "REL_OP": ";",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}},
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ">",
                    "RIGHT_ID": "value1",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}, "DEP": "conj"},
                },
                {
                    "LEFT_ID": "value1",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}, "DEP": "conj"},
                },
            ]
        ]
        self.add_pattern('dep', rules)


class VALUE_FOR_NP(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, doc=doc)
        rules = [
            [
                {
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": self.NP_POS}},
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_for",
                    "RIGHT_ATTRS": {"LEMMA": "for"},
                },
                {
                    "LEFT_ID": "anchor_for",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": self.NP_POS}},
                },
            ],
        ]
        self.add_pattern('dep', rules)


class CD_NP(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, 'clean', doc=doc)

    def _match_non_num(self, res):
        try:
            quants = [quant.surface for quant in parser.parse(self.text) if quant is not None]
        except:
            quants = []
        for token in self.doc:
            if is_digit(token) or token.lemma_ in ['negative', 'positive', 'multiple', 'more']:
                if self.doc[token.i:].text in quants or self.doc[token.i + 1:token.i + 2].lemma_ in ['minute', 'second', 'digit', 'view',
                                                                               'line'] \
                        or re.sub(r'[^\w\s]', '', self.doc[token.i + 1:token.i + 2].text).strip() == '':
                    continue

                op_data = self.doc[token.i: token.i + 1]
                op_val = self.doc[token.i + 1: token.i + 2]
                if token.i + 1 != len(self.doc) and self.doc[token.i + 1: token.i + 3].text in ['or more', 'or less']:
                    op_data = self.doc[token.i: token.i + 3]
                    op_val = self.doc[token.i + 3: token.i + 4]
                j = token.i
                while j + 1 != len(self.doc) and self.doc[j + 1].pos_ in self.NP_POS:
                    j += 1
                    op_val = self.doc[token.i+1: j+1]
                operands = [op_data.text, op_val.text]
                res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                         fragment=' '.join(operands),
                                         operands=operands,
                                         text=self.text,
                                         doc=self.doc,
                                         start=-1,
                                         end=-1))

    def match(self):
        res = set()
        self._match_non_num(res)
        rules = [
            {"POS": "NUM"},
            {"POS": "ADJ", "OP": "?"},
            {"POS": {"IN": Detector.NOT_NUM_NP_POS}, "OP": "+", "LEMMA": {"NOT_IN": ["which", "that"]}},
        ]
        self.matcher.add("CD_NP", [rules])
        matches = self.matcher(self.doc)

        for m in matches:
            match_id, start, end = m
            operands = [self.doc[start].text, self.doc[start + 1: end].text]
            res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                     fragment=' '.join(operands),
                                     operands=operands,
                                     text=self.text,
                                     doc=self.doc,
                                     start=start,
                                     end=end))
        return res


class NP_CD(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, 'all', doc)
        rules = [
            [
                {
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NOT_NUM_NP_POS}},
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": "NUM"}
                },
            ],
        ]
        self.doc = preprocess_doc(self.doc)
        self.add_pattern('dep', rules)

    def match(self):
        res = super(NP_CD, self).match()
        rules = [
            [
                {"POS": {"IN": Detector.NOT_NUM_NP_POS}},
                {"POS": {"IN": Detector.NOT_NUM_NP_POS}, "OP": "+"}
            ]
        ]
        self.add_pattern('token', rules)
        matches = self.matcher(self.doc)
        for match in matches:
            match_id, start, end = match
            doc = preprocess_doc(nlps['clean'](self.doc[end - 1].text))
            p = 0
            while p < len(doc) and doc[p].pos_ == 'PUNCT':
                p += 1
            if p < len(doc) and doc[p].pos_ == 'NUM':
                operands = [self.doc[start].text, doc[p].text]
                res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                         fragment=' '.join([self.doc[start].text, doc[:p + 1].text]),
                                         operands=operands,
                                         text=self.text,
                                         doc=self.doc,
                                         start=start,
                                         end=end))
        return res
