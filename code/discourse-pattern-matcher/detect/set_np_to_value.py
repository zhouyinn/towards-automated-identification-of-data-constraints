from model.detector import Detector
from model.discourse_pattern import DiscoursePattern
from utils.nlp_factory import nlps
import re
from model.detector import preprocess_doc, extract_merge_range

def _preprocess_text(text):
    return re.sub(r'\b=\b', ' = ', text)


class SET_NP_TO_VALUE(Detector):
    def __init__(self, text, doc=None):
        super().__init__(_preprocess_text(text), doc=doc)
        rule1 = [
                {"LEMMA": {"IN": ["set", "define"]}},
                {"POS": {"IN": Detector.NP_POS}, "OP": "+"},
                {"LEMMA": {"IN": ["to", "as"]}},
                {"POS": "VERB", "OP": "?"},
                {"POS": {"IN": Detector.NP_POS}},
             ]
        rule2 = [
                {"POS": {"IN": Detector.NP_POS}},
                {"LEMMA": "="},
                {"POS": {"IN": Detector.NP_POS + ["ADV"]}, "OP": "?"},
                {"POS": {"IN": Detector.NP_POS + ["ADP"]}},
                {"LEMMA": ".", "OP": "?"},
                {"POS": {"IN": Detector.NP_POS}, "OP": "?"},
            ]
        self.matcher.add('token1', [rule1])
        self.matcher.add('token2', [rule2])

    def _match(self):
        res = set()
        matches = self.matcher(preprocess_doc(self.doc))
        if len(matches) == 0:
            return set()
        match1 = list(extract_merge_range([m for m in matches if self.nlp.vocab.strings[m[0]] == 'token1']).items())
        match2 = list(extract_merge_range([m for m in matches if self.nlp.vocab.strings[m[0]] == 'token2']).items())
        i = 0
        for end, start in match1 + match2:
            if i < len(match1):
                operands = [self.doc[start + 1].text, self.doc[start + 3 : end].text]
            else:
                operands = [self.doc[start].text, self.doc[start + 2 : end].text]
            # include 'if' and 'when'
            if start > 0 and self.doc[start - 1].lemma_ in ['if', 'when']:
                start = start - 1
            res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                     fragment=self.doc[start: end].text,
                                     operands=operands,
                                     text=self.text,
                                     doc=self.doc,
                                     start=start,
                                     end=end))
            i += 1
        return res

    def _match_split_for_all(self):
        res = set()
        for token in self.doc:
            if '=' in token.text:
                operands = [t for t in token.text.split('=') if len(t.strip()) > 0]
                start, end = token.i, token.i
                if token.i > 0 and self.doc[token.i - 1].lemma_ in ['if', 'when']:
                    start = start - 1
                if len(operands) < 2: continue
                res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                         fragment=self.doc[start: end+1].text.replace('=', ' = '),
                                         operands=operands,
                                         text=self.text,
                                         doc=self.doc,
                                         start=start,
                                         end=end))
        return res

    def match(self):
        res = set()
        text = _preprocess_text(self.text)
        for type in ['all', 'no_en', 'no_nc', 'clean']:
            if type == 'all':
                res.update(self._match_split_for_all())
            self.doc = nlps[type](text)
            res.update(self._match())
        return res
