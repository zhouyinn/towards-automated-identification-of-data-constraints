from model.detector import Detector


class NP_SET_TO_VALUE(Detector):
    def _merge_attribute(self):
        rule = [
            [
                {"LEMMA": "the"},
                {"OP": "?"},
                {"LEMMA": "attribute"}
            ],
            [
                {"LEMMA": "the"},
                {"POS": "ADJ", "OP": "?"},
                {"POS": {"IN": self.NP_POS}, "OP": "+"}
            ]
        ]
        self.matcher.add("THE_ATTR", rule)
        matches = self.matcher(self.doc)
        matches.sort(key=lambda x: x[2], reverse=True)
        for m in matches:
            with self.doc.retokenize() as retokenizer:
                retokenizer.merge(self.doc[m[1]:m[2]], attrs={"POS": "NOUN"})

    def __init__(self, text, doc=None):
        super().__init__(text, doc=doc)
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
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"DEP": {"IN": ["pobj", "amod"]}}
                },

            ],
            # general data be [set to / marked as] [fail]
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
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["to", "as"], "DEP": "aux"}}
                },
                {
                    "LEFT_ID": "anchor_set",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": "VERB", "DEP": "xcomp"}
                },

            ],
        #     require to be
            [
                {
                    "RIGHT_ID": "anchor_require",
                    "RIGHT_ATTRS": {"LEMMA": "require"}
                },
                {
                    "LEFT_ID": "anchor_require",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "nsubjpass"},
                },
                {
                    "LEFT_ID": "anchor_require",
                    "REL_OP": ">",
                    "RIGHT_ID": "anchor_be",
                    "RIGHT_ATTRS": {"LEMMA": "be", "DEP": "xcomp"}
                },
                {
                    "LEFT_ID": "anchor_be",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"DEP": "attr"}
                },

            ],
        #     with NP set to VALUE
            [
                {
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": self.NP_POS}}
                },
                {
                    "LEFT_ID": "op_data",
                    "REL_OP": ">",
                    "RIGHT_ID": "anchor_set",
                    "RIGHT_ATTRS": {"LEMMA": "set", "DEP": "dobj"},
                },
                {
                    "LEFT_ID": "anchor_set",
                    "REL_OP": ">",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": "to", "DEP": "prep"}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"DEP": "pobj"}
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
                    "RIGHT_ATTRS": {"DEP": {"IN": ["nsubjpass", "nsubj"]}},
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
                    "RIGHT_ATTRS": {"POS": {"IN": ["ADJ", "NUM"]}}
                },

            ],
        ]
        self.add_pattern('dep', rules)
