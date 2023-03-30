from model.detector import Detector


class NP_EXIST(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, doc=doc)
        rules = [
            [
                {
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"LEMMA": "exist"}
                },
                {
                    "LEFT_ID": "op_val",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}, "DEP": "nsubj"},
                },
            ]
        ]
        self.add_pattern('dep', rules)
