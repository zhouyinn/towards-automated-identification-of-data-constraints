import re
from model.detector import Detector, preprocess_doc
from model.discourse_pattern import DiscoursePattern
from utils.nlp_factory import nlps


class NP_CD_TO_CD(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, 'no_en', doc)
        self.doc = preprocess_doc(self.nlp(self.text))
        rules_dep = [
            [
                {
                    "RIGHT_ID": "anchor_between",
                    "RIGHT_ATTRS": {"LEMMA": "between"}
                },
                {
                    "LEFT_ID": "anchor_between",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val1",
                    "RIGHT_ATTRS": {"POS": "NUM"}
                },
                {
                    "LEFT_ID": "op_val1",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_and",
                    "RIGHT_ATTRS": {"LEMMA": "and"}
                },
                {
                    "LEFT_ID": "anchor_and",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val2",
                    "RIGHT_ATTRS": {"POS": "NUM"}
                }
            ],
            [
                {
                    "RIGHT_ID": "op_val1",
                    "RIGHT_ATTRS": {"POS": "NUM"}
                },
                {
                    "LEFT_ID": "op_val1",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": "to"}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val2",
                    "RIGHT_ATTRS": {"POS": "NUM"}
                }
            ],
            [
                {
                    "RIGHT_ID": "op_val1",
                    "RIGHT_ATTRS": {"POS": "NUM"}
                },
                {
                    "LEFT_ID": "op_val1",
                    "REL_OP": ".",
                    "RIGHT_ID": "anchor_to",
                    "RIGHT_ATTRS": {"LEMMA": "to"}
                },
                {
                    "LEFT_ID": "anchor_to",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_val2",
                    "RIGHT_ATTRS": {"POS": "NUM"}
                },
                {
                    "LEFT_ID": "op_val2",
                    "REL_OP": ".",
                    "RIGHT_ID": "op_data",
                    "RIGHT_ATTRS": {"POS": {"IN": self.NP_POS}}
                }
            ]
        ]
        self.add_pattern('dep', rules_dep)

    def _match_from_to(self, matches, res):
        matches = [match for match in matches if self.nlp.vocab.strings[match[0]] == 'PAT#1']
        for match in matches:
            match_id, token_ids = match
            op1_i = token_ids[0]
            op2_i = token_ids[2]
            cur = op1_i - 1
            while cur >= 0 and self.doc[cur].pos_ != 'NOUN':
                cur = cur - 1
            # extend of
            prev = cur - 1
            while prev >= 0 and self.doc[prev].lemma_ == 'of':
                cur = prev - 1
                prev = cur - 1

            op_data = re.sub(r'(?:one|two|three)\sdigit\s', '', self.doc[max(0, cur): op1_i - 1].text, flags=re.IGNORECASE)
            frag1 = re.sub(r'(?:one|two|three)\sdigit\s', '', self.doc[max(0, cur): op1_i + 1].text, flags=re.IGNORECASE)
            frag2 = re.sub(r'(?:one|two|three)\sdigit\s', '', self.doc[max(0, cur): op2_i + 1].text, flags=re.IGNORECASE)

            res.add(DiscoursePattern(self.__class__.__name__,
                                     frag1,
                                     [op_data, self.doc[op1_i].text],
                                     self.doc,
                                     max(0, cur),
                                     op1_i + 1))
            res.add(DiscoursePattern(self.__class__.__name__,
                                     frag2,
                                     [op_data, self.doc[op2_i].text],
                                     self.doc,
                                     max(0, cur),
                                     op2_i + 1))

    def _match_between_and(self, matches, res):
        matches = [match for match in matches if self.nlp.vocab.strings[match[0]] == 'PAT#0']
        for match in matches:
            match_id, token_ids = match
            operands = self._extract_operands_dep(match)
            op_val1, op_val2 = operands
            frag_1 = 'between {}'.format(op_val1)

            with self.doc.retokenize() as retokenizer:
                attrs = {"LEMMA": "BETWEEN_AND_PHRASE"}
                retokenizer.merge(self.doc[min(token_ids):max(token_ids)+1], attrs=attrs)

            # extract data
            nsubj_pat = [{"POS": {"IN": Detector.NP_POS}},
                         {"LEMMA": "be", "OP": "?"},
                         {"LEMMA": "BETWEEN_AND_PHRASE"}]
            self.matcher.add("SUBJ", [nsubj_pat])
            matches = self.matcher(self.doc)
            if len(matches) == 0:
                return
            start = min([m[1] for m in matches])
            end = max([m[2] for m in matches])
            op_data = self.doc[start].text
            res.add(DiscoursePattern(self.__class__.__name__,
                                     ' '.join([self.doc[start:end - 1].text, frag_1]),
                                     [op_data, op_val1],
                                     self.doc,
                                     start,
                                     end))
            res.add(DiscoursePattern(self.__class__.__name__,
                                     self.doc[start:end].text,
                                     [op_data, op_val2],
                                     self.doc,
                                     start,
                                     end))

    def _match_cd_to_cd_np(self, res):
        self.doc = nlps['clean'](self.text)
        matches = self.dep_matcher(self.doc)
        matches = [match for match in matches if self.nlp.vocab.strings[match[0]] == 'PAT#2']
        for m in matches:
            i1, to, i2, j = m[1]
            op_val1, op_val2, op_data = self.doc[i1].text, self.doc[i2].text, self.doc[j].text
            res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                     fragment=self.doc[i1: j + 1].text,
                                     operands=[op_data, op_val1],
                                     text=self.text,
                                     doc=self.doc,
                                     start=i1,
                                     end=j + 1))
            res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                     fragment=self.doc[i2: j + 1].text,
                                     operands=[op_data, op_val2],
                                     text=self.text,
                                     doc=self.doc,
                                     start=i2,
                                     end=j + 1))

    def match(self):
        res = set()
        matches = self.dep_matcher(self.doc)
        self._match_from_to(matches, res)
        self._match_between_and(matches, res)
        self._match_cd_to_cd_np(res)
        return res
