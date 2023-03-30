from model.detector import Detector
import re
from model.discourse_pattern import DiscoursePattern
import copy
from utils.nlp_factory import nlps


def _clean_match(m):
    range_s = {}
    for m in m:
        match_id, start, end = m
        if start not in range_s:
            range_s[start] = end
        else:
            if end > range_s[start]:
                range_s[start] = end
    range_e = {}
    for start, end in range_s.items():
        if end not in range_e:
            range_e[end] = start
        else:
            if start < range_e[end]:
                range_e[end] = start
    return range_e


class NP_COMP_NP(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, doc=doc)
        self.doc = copy.deepcopy(self.doc)

    def _tag_comp_phrase(self):
        # match comp phrase
        terms = ["<=", ">=", "above", "before", "below",
                 "greater than", "lower than", "newer than",
                 "greater than or equal to", "less than", "more than", "less than or equal to",
                 "at or before", "equal to or earlier than", "equal to or later than", "equal to or greater than",
                 "equal to or less than"]
        patterns = [self.nlp.make_doc(text) for text in terms]
        self.phrase_matcher.add("TerminologyList", patterns)
        matches = self.phrase_matcher(self.doc)
        if len(matches) == 0:
            return
        range = _clean_match(matches)
        for end, start in range.items():
            with self.doc.retokenize() as retokenizer:
                attrs = {"LEMMA": "COMP_PHRASE"}
                retokenizer.merge(self.doc[start:end], attrs=attrs)

    def _process_conj(self):
        dep_rule = [
            {
                "RIGHT_ID": "op_data",
                "RIGHT_ATTRS": {"POS": {"IN": self.NP_POS}, "LEMMA": {"NOT_IN": ["which", "that", "whether"]}}
            },
            {
                "LEFT_ID": "op_data",
                "REL_OP": ">",
                "RIGHT_ID": "anchor_comp",
                "RIGHT_ATTRS": {"DEP": "conj", "LEMMA": "COMP_PHRASE"}
            },
        ]
        self.dep_matcher.add("conj_comp_phrase", [dep_rule])
        matches = self.dep_matcher(self.doc)
        res = []
        for m in matches:
            match_id, token_ids = m
            on_match, patterns = self.dep_matcher.get(self.nlp.vocab.strings[match_id])
            op_data = " ".join(
                [self.doc[token_ids[i]].text for i in range(len(token_ids)) if "op_data" in patterns[0][i]["RIGHT_ID"]])
            res.append((m[1][0], m[1][1] + 1, op_data))
        return res

    def _extract_op_val(self, start):
        self.matcher.add("VALUE", [[{"LEMMA": "COMP_PHRASE"}, {"POS": {"IN": Detector.NP_POS}}]])
        matches = self.matcher(self.doc)
        for m in matches:
            m_id, s, e = m
            if s == start - 1: return e - 1, self.doc[e - 1].text
        return None

    def match_(self):
        res = set()
        self._tag_comp_phrase()

        # conj
        conj_match = []
        if any([x in self.text for x in ['and', 'or']]):
            conj_match = self._process_conj()
        # extract data
        rules = [{"POS": {"IN": Detector.NP_POS}},
                 {"LEMMA": "with", "OP": "?"},
                 {"POS": {"IN": Detector.NP_POS}, "OP": "?"},
                 {"LEMMA": {"IN": ["which", "that"]}, "OP": "?"},
                 {"POS": "VERB", "OP": "?"},
                 {"LEMMA": {"IN": ["have", "be"]}, "OP": "?"},
                 {"POS": "VERB", "OP": "?"},
                 {"LEMMA": "if", "OP": "?"},
                 {"LEMMA": "COMP_PHRASE"}]
        self.matcher.add("DATA", [rules])
        matches = self.matcher(self.doc)
        non_conj_match = []
        for m in matches:
            m_id, start, end = m
            start_ = min([m[1] for m in matches])
            span = self.doc[start:start_ + 1]  # The matched span
            op_data = re.sub(r'(which)?\s+(?:be|is|are|was|were)$', '', span.text)
            if op_data == '': continue
            non_conj_match.append((start, end, op_data))

        for m in conj_match + non_conj_match:
            start, end, op_data = m
            # extract value
            if self.matcher.get("DATA") is not None:
                self.matcher.remove("DATA")

            op = self._extract_op_val(end)
            if op is None: continue
            end, op_val = op

            res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                     fragment=self.doc[start: end + 1].text,
                                     operands=[op_data, op_val],
                                     text=self.text,
                                     doc=self.doc,
                                     start=start,
                                     end=end))

        return res

    def match(self):
        res = set()
        for type in ['all', 'no_en', 'no_nc', 'clean']:
            if type == 'all':
                res.update(self.match_())
            self.doc = nlps[type](self.text)
            res.update(self.match_())
        return res
