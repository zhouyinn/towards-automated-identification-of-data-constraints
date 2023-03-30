from model.detector import Detector
from utils.nlp_factory import nlps
from model.detector import extract_merge_range
from model.discourse_pattern import DiscoursePattern
import re

class SET_NP_TO_BINARY_VALUE(Detector):
    def __init__(self, text, doc=None):
        if ' = ' not in text:
            text = text.replace('=', ' = ')
        super().__init__(text, doc=doc)
        rules = [
            # conj
            [
                {
                    "RIGHT_ID": "anchor_set",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["set", "specify", "define"]}}
                },
                {
                    "LEFT_ID": "anchor_set",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_data",
                    # todo: error POS in SpaCy parser
                    "RIGHT_ATTRS": {"POS": {"IN": self.NP_POS + ["VERB"]}},
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": "to"}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ">>",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["true", "false", "on", "off", "non", "empty"]}}
                },
            ],
            # general
            [
                {
                    "RIGHT_ID": "anchor_set",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["set", "specify", "define"]}}
                },
                {
                    "LEFT_ID": "anchor_set",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_data",
                    # todo: error POS in SpaCy parser
                    "RIGHT_ATTRS": {"POS": {"IN": self.NP_POS + ["VERB"]}},
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": "to"}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["true", "false", "on", "off", "non", "empty"]}}
                },
            ],
            [
                {
                    "RIGHT_ID": "op_data",
                    # todo: error POS in SpaCy parser
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS + ["VERB"]}},
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_equal",
                    "RIGHT_ATTRS": {"LEMMA": "="}
                },
                {
                    "LEFT_ID": "anchor_equal",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["true", "false", "on", "off", "non", "empty"]}}
                },
            ],
            # np = binary value
            [
                {
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS + ["VERB", "ADV", "ADJ", "INTJ"]}},
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": "="}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"TAG": {"IN": ["JJ", "VBD", "VBN"]}}
                },
            ],
        ]
        self.add_pattern('dep', rules)

    def _merge_noun_phrase(self):
        rule = [
            [
                {"POS": {"IN": self.NP_POS + ["ADJ", "DET"]}, "LEMMA": {"NOT_IN": ["true", "false"]}, "OP": "+"},
                {"POS": {"IN": self.NP_POS}, "OP": "+"},
            ],
        ]
        self.matcher.add("NOUN", rule)
        matches = self.matcher(self.doc)
        for end, start in extract_merge_range(matches).items():
            with self.doc.retokenize() as retokenizer:
                retokenizer.merge(self.doc[start:end], attrs={"POS": "NOUN"})

    def _match(self):
        res = set()
        for nlp_type in ['clean', 'no_en', 'no_nc']:
            self.doc = nlps[nlp_type](self.text)
            self._merge_noun_phrase()
            for r in super(SET_NP_TO_BINARY_VALUE, self).match():
                r.fragment = re.sub(r'\s*=\s*', '=', r.fragment)
                res.add(r)
            for token in self.doc:
                # print(token.text, '#', token.lemma_, '#',token.dep_, '#',token.tag_, '#',token.pos_)
                tt = re.sub(r'\s*=\s*', '=', token.text)
                if '=' in tt and len(list(filter(len, tt.split('=')))) == 2:
                    res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                             fragment=tt,
                                             operands=tt.split('='),
                                             text=self.text,
                                             start=token.i,
                                             end=token.i))
                elif '=' in tt and len(tt.replace('=', '').strip()) > 0 and token.i + 1 < len(self.doc) and self.doc[token.i + 1].lemma_ in ["true", "false", "on", "off", "non", "empty"]:
                    operands = [tt.replace('=', ''), self.doc[token.i + 1].text]
                    res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                             fragment='='.join(operands),
                                             operands=operands,
                                             text=self.text,
                                             start=token.i,
                                             end=token.i))

        return res

    def match(self):
        res = set()
        res.update(self._match())
        return res