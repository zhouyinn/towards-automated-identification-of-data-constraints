from model.detector import Detector

class NP_BE_BINARY_VALUE(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, doc=doc)
        rules = [
            # general binary value
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
            # other binary value
            [
                {
                    "RIGHT_ID": "anchor_action",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]}}
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
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["on", "off", "nan", "out", "inout"]}}
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
            # conj in value
            [
                {
                    "RIGHT_ID": "sub",
                    "RIGHT_ATTRS": {"TAG": {"IN": ["JJ", "VBD", "VBN"]}}
                },
                {
                    "LEFT_ID": "sub",
                    "REL_OP": ">>",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"DEP": "conj", "TAG": {"IN": ["JJ", "VBD", "VBN"]}}
                },
                {
                    "LEFT_ID": "sub",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": {"IN": ["nsubjpass", "nsubj"]}},
                },
                {
                    "LEFT_ID": "sub",
                    "REL_OP": ">",
                    "RIGHT_ID": "anchor_be",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]},
                                    "DEP": {"IN": ["aux", "auxpass"]}},
                },
            ],
            # deal with conj
            [
                {
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"TAG": {"IN": ["JJ", "VBD", "VBN"]}}
                },
                {
                    "LEFT_ID": "op_val",
                    "REL_OP": ">",
                    "RIGHT_ID": "anchor_be",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]},
                                    "DEP": {"IN": ["aux", "auxpass"]}},
                },
                {
                    "LEFT_ID": "op_val",
                    "REL_OP": ">",
                    "RIGHT_ID": "sub",
                    "RIGHT_ATTRS": {"DEP": {"IN": ["nsubjpass", "nsubj"]}},
                },
                {
                    "LEFT_ID": "sub",
                    "REL_OP": ">>",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "conj"},
                },
            ],
            # turn on
            [
                {
                    "RIGHT_ID": "turn",
                    "RIGHT_ATTRS": {"TAG": {"IN": ["JJ", "VBD", "VBN"]}}
                },
                {
                    "LEFT_ID": "turn",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": {"IN": ["nsubjpass", "nsubj"]}},
                },
                {
                    "LEFT_ID": "turn",
                    "REL_OP": ">",
                    "RIGHT_ID": "anchor_be",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]},
                                    "DEP": {"IN": ["aux", "auxpass"]}},
                },
                {
                    "LEFT_ID": "turn",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["on", "off"]}},
                },
            ],
            # fix conj
            [
                {
                    "RIGHT_ID": "anchor_be",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["be", "allow", "remain", "show"]}}
                },
                {
                    "LEFT_ID": "anchor_be",
                    "REL_OP": ";",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "conj", "POS": {"IN": self.NP_POS + ["ADJ"]}},
                },
                {
                    "LEFT_ID": "anchor_be",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"TAG": {"IN": ["JJ", "VBD", "VBN", "ADJ"]}}
                }
            ],
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
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["on", "off", "nan", "out", "inout"]}}
                }
            ],
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
                    "REL_OP": ".",
                    "RIGHT_ID": "sub",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["on", "off", "nan", "out", "inout"]}}
                },
                {
                    "LEFT_ID": "sub",
                    "REL_OP": ">>",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"DEP": "conj", "LEMMA": {"IN": ["on", "off", "nan", "out", "inout"]}}
                }
            ],
        ]
        self.add_pattern('dep', rules)
