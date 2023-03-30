from model.detector import Detector
from utils.nlp_factory import nlps
import re
from model.detector import clean_text, extract_merge_range


class NP_SET_TO_BINARY_VALUE(Detector):
    def _merge_attribute(self):
        rule = [
            [
                {"LEMMA": "the", "OP": "?"},
                {"POS": {"IN": self.NP_POS + ["ADJ"]}, "OP": "*"},
                {"LEMMA": {"IN": ["attribute", "property"]}}
            ],
        ]
        self.matcher.add("THE_ATTR", rule)
        matches = self.matcher(self.doc)
        for end, start in extract_merge_range(matches).items():
            with self.doc.retokenize() as retokenizer:
                retokenizer.merge(self.doc[start:end], attrs={"POS": "NOUN"})

    def __init__(self, text:str, doc):
        text = re.sub(r'\s*,?\s*(-|,|which)\s*if\s*', ' is ', text, flags=re.IGNORECASE)
        for word in ['true', 'false', 'on', 'off']:
            text = text.replace('the default of {}'.format(word), word)
        text = text.replace(' and ', ', and ')
        self.doc = nlps['all'](clean_text(text))
        super().__init__(text, doc=self.doc)
        self._merge_attribute()
        rules = [
            # general data be [set to / marked as] value
            [
                {
                    "RIGHT_ID": "anchor_set",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["set", "mark"]}}
                },
                {
                    "LEFT_ID": "anchor_set",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": {"IN": ["nsubjpass", "advmod"]}},
                },
                {
                    "LEFT_ID": "anchor_set",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["to", "as"]}}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["true", "false"]}}
                },

            ],
            [
                {
                    "RIGHT_ID": "anchor_set",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["set", "mark"]}}
                },
                {
                    "LEFT_ID": "anchor_set",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "nsubjpass"},
                },
                {
                    "LEFT_ID": "anchor_set",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["to", "as"]}}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ".",
                    "RIGHT_ID": "sub",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["true", "false"]}}
                },
                {
                    "LEFT_ID": "sub",
                    "REL_OP": ">>",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["true", "false"]}}
                },
            ],
            [
                {
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": self.NP_POS}}
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ">",
                    "RIGHT_ID": "anchor_set",
                    "RIGHT_ATTRS": {"LEMMA": "set"},
                },
                {
                    "LEFT_ID": "anchor_set",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": "to"}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"DEP": "pobj"}
                },
            ],
            # all the options are boolean,, and be set to true
            [
                {
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": self.NP_POS}}
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": "<",
                    "RIGHT_ID": "anchor_be",
                    "RIGHT_ATTRS": {"LEMMA": "be"},
                },
                {
                    "LEFT_ID": "anchor_be",
                    "REL_OP": ">",
                    "RIGHT_ID": "anchor_set",
                    "RIGHT_ATTRS": {"LEMMA": "set"},
                },
                {
                    "LEFT_ID": "anchor_set",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": "to"}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": {"IN":["true", "yes", "false", "no"] }}
                },
            ]
        ]
        self.add_pattern('dep', rules)
