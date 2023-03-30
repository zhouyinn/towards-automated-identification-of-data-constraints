from model.detector import Detector
from model.discourse_pattern import DiscoursePattern
import re
from model.detector import extract_merge_range

class NP_IN_VALUESET(Detector):
    def __init__(self, text, doc=None):
        super().__init__(text, doc=doc)

    def _label_value(self, res):
        pattern = [
            {
                "POS": {"IN": Detector.NP_POS + ["ADJ", "PART", "INTJ"]},
                "LEMMA": {"NOT_IN": ["there", "that", "which"]}
            },
            {
                "TEXT": ",", "OP": "?"
            },
            {
                "TEXT": {"IN": ["and", "or"]}, "OP": "?"
            }
        ]
        self.matcher.add("VALUE", [pattern])
        matches = self.matcher(self.doc)
        matches.sort(key=lambda x: x[2], reverse=True)
        for m in matches:
            match_id, start, end = m
            with self.doc.retokenize() as retokenizer:
                attrs = {"LEMMA": "VALUE"}
                text = self.doc[start:end].text
                if '(' in text:
                    res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                             fragment=self.doc[start: end].text.replace("one of ", ""),
                                             operands=[op.strip() for op in text.split('(') if op.strip() not in ['default']],
                                             text=self.text,
                                             doc=self.doc,
                                             start=start,
                                             end=end))
                retokenizer.merge(self.doc[start:end], attrs=attrs)

    def match(self):
        res = set()
        self._label_value(res)
        super_pattern = [
            {
                "POS": {"IN": Detector.NP_POS}, "LEMMA": {"NOT_IN": ["there"]}
            },
            {
                "LEMMA": "be", "OP": "?"
            },
            {
                "TEXT": "either", "OP": "?"
            },
            {
                "LEMMA": {"IN": [":", "in", "(", ",", "-", "include"]}, "OP": "?"
            },
            {
                "LEMMA": "VALUE", "OP": "+"
            },
        ]

        self.matcher.add("NP_IN_VALUESET", [super_pattern])
        matches = self.matcher(self.doc)
        matches = [m for m in matches if self.nlp.vocab.strings[m[0]] == 'NP_IN_VALUESET']
        for end, start in extract_merge_range(matches).items():
            tokens = [token.text for token in self.doc[start: end] if token.lemma_ == 'VALUE']
            operands = []
            for t in tokens:
                operands += [s.strip().replace("one of ", "") for s in re.split(r"\bor\b|,|\band\b|:", t) if len(s.strip()) > 0 and s.strip() not in ["either", "default"]]
            if len(operands) < 2: continue
            pattern_name = 'NP_BE_VALUE' if len(operands) == 2 else self.__class__.__name__
            res.add(DiscoursePattern(pattern_name=pattern_name,
                                     fragment=self.doc[start: end].text.replace("one of ", ""),
                                     operands=operands,
                                     text=self.text,
                                     doc=self.doc,
                                     start=start,
                                     end=end))
        return res
