from model.detector import Detector
from model.discourse_pattern import DiscoursePattern

# special case of NP_COMP_NP
class NP_SAME_AS_NP(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, doc=doc)
        rules = [
            [
                {
                    "RIGHT_ID": "anchor_be",
                    "RIGHT_ATTRS": {"LEMMA": "be"}
                },
                {
                    "LEFT_ID": "anchor_be",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "nsubj"},
                },
                {
                    "LEFT_ID": "anchor_be",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_the",
                    "RIGHT_ATTRS": {"LEMMA": "the"}
                },
                {
                    "LEFT_ID": "anchor_the",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_same",
                    "RIGHT_ATTRS": {"LEMMA": "same"}
                },
                {
                    "LEFT_ID": "anchor_same",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_as",
                    "RIGHT_ATTRS": {"LEMMA": "as"}
                },
                {
                    "LEFT_ID": "anchor_as",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"DEP": "pobj"}
                },
            ],
            # be identical to
            [
                {
                    "RIGHT_ID": "anchor_be",
                    "RIGHT_ATTRS": {"LEMMA": "be"}
                },
                {
                    "LEFT_ID": "anchor_be",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "nsubj"},
                },
                {
                    "LEFT_ID": "anchor_be",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_identical",
                    "RIGHT_ATTRS": {"LEMMA": "identical"}
                },
                {
                    "LEFT_ID": "anchor_identical",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": "to"}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"DEP": "pobj"}
                }
            ],
            [
                {
                    "RIGHT_ID": "anchor_match",
                    "RIGHT_ATTRS": {"LEMMA": "match"}
                },
                {
                    "LEFT_ID": "anchor_match",
                    "REL_OP": ">",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"DEP": "nsubj"}
                },
                {
                    "LEFT_ID": "anchor_match",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}}
                }
            ],
            [
                {
                    "RIGHT_ID": "anchor_word",
                    "RIGHT_ATTRS": {"LEMMA": {"IN": ["in", "within", "from"]}}
                },
                {
                    "LEFT_ID": "anchor_word",
                    "REL_OP": "<",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": Detector.NP_POS}}
                },
                {
                    "LEFT_ID": "anchor_word",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val",
                    "RIGHT_ATTRS": {"POS": "NOUN"}
                },
            ]
        ]
        self.add_pattern('dep', rules)

    def match(self):
        res = set()
        matches = self.dep_matcher(self.doc)
        for match in matches:
            match_id, token_ids = match
            start = min(token_ids)
            end = max(token_ids)
            operands = self._extract_operands_dep(match)
            if id != self.dep_matcher.__len__() - 1:
                res.add(DiscoursePattern(pattern_name="NP_COMP_NP",
                                         fragment=self.doc[start: end+1].text,
                                         operands=operands,
                                         text=self.text,
                                         doc=self.doc,
                                         start=start,
                                         end=end + 1))
            elif "the same " in operands[-1]:
                operands[-1] = operands[-1].replace("the same ", "")
                operands = self._extract_operands_dep(match)
                if id != self.dep_matcher.__len__() - 1:
                    res.add(DiscoursePattern(pattern_name="NP_COMP_NP",
                                             fragment=self.doc[start: end + 1].text,
                                             operands=operands,
                                             text=self.text,
                                             doc=self.doc,
                                             start=start,
                                             end=end + 1))
        return res

