from model.detector import Detector
from model.discourse_pattern import DiscoursePattern
from utils.nlp_factory import nlps
from model.detector import clean_text
from model.detector import extract_merge_range
import re


class NP_IF_BINARY_VALUE(Detector):
    def __init__(self, text, doc=None):
        self.prev_text = text
        text = re.sub(r'\s*,?\s*(-|,|which)\s*if\s*', ' is ', text, flags=re.IGNORECASE)
        super().__init__(text, doc=doc)
        rules = [
            [
                {
                    "RIGHT_ID": "anchor_action",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show", ":"]}}
                },
                {
                    "LEFT_ID": "anchor_action",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": {"IN": ["nsubj", "nsubjpass"]}},
                },
                {
                    "LEFT_ID": "anchor_action",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": ["ADJ", "VERB"]}}
                },

            ],
            [
                {
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"TAG": {"IN": ["JJ", "VBD", "VBN"]}}
                },
                {
                    "LEFT_ID": "op_val",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": {"IN": ["nsubjpass", "nsubj"]}},
                },
                {
                    "LEFT_ID": "op_val",
                    "REL_OP": ">",
                    "RIGHT_ID": "anchor_be",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]},
                                    "DEP": {"IN": ["aux", "auxpass"]}},
                },
            ],
        ]
        self.add_pattern('dep', rules)

    def _match(self):
        res = set()
        for token in self.doc:
            if token.tag_ in ["JJ", "VBD", "VBN"] or token.text in ["no argument"]:
                if_id = token.i - 1
                if if_id >= 0 and self.doc[if_id].lemma_ == 'if':
                    # find the nearest noun phrase
                    cur = if_id - 1
                    while cur >= 0 and (self.doc[cur].pos_ not in self.NP_POS or self.doc[cur].lemma_ in ["that", "which"]):
                        cur = cur - 1
                    # missed data
                    if max(0, cur) == if_id:
                        continue
                    start = max(0, cur)
                    end = token.i + 1
                    res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                             fragment=self.doc[start: end].text,
                                             operands=[self.doc[cur].text.replace(" that", "").replace(" which", ""), token.text],
                                             text=self.text,
                                             doc=self.doc,
                                             start=start,
                                             end=end))
        return res

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

    def match(self):
        res = set()
        self.doc = nlps['clean'](self.text)
        res.update(self._match())
        self.doc = self.nlp(clean_text(self.prev_text))
        self._merge_noun_phrase()
        res.update(self._match())
        return res
