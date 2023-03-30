from spacy.matcher import DependencyMatcher, Matcher, PhraseMatcher
from model.discourse_pattern import DiscoursePattern
from utils.nlp_factory import nlps
import string
import re
import ftfy

def is_digit(token):
    try:
        float(token.text)
    except ValueError:
        if token.pos_ == 'NUM' and token.text not in string.punctuation:
            return True
        return False
    return True


def preprocess_doc(doc):
    # num processing
    for token in doc:
        isnumber = is_digit(token)
        if token.lemma_ in string.punctuation:
            token.pos_ = 'PUNCT'
        elif isnumber:
            token.pos_ = 'NUM'
        elif not isnumber and token.pos_ == 'NUM':
            token.pos_ = 'NOUN'
            # print(token.text, token.pos_)
    return doc


def clean_text(text):
    text = ftfy.fix_text(text)

    text = re.sub(r'^\W*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\W*$', '', text, flags=re.IGNORECASE)

    # remove list id
    text = '\n'.join([re.sub(r'^\s*\d+\.?\s*$', '', t) for t in text.split('\n')])
    # remove new line
    text = text.replace('\n', ' ').replace('\r', '')

    # remove noise
    exclude_words = ["always", "must", "therefore", "already", "may ", "can", "by default", "should", "also", "now",
                     "only", "whose", "will"]
    # remove punct
    text = re.sub(r'\"|\'|`|“|”', '', text)
    for word in exclude_words:
        text = re.sub(r'\b({})\b'.format(word), '', text, flags=re.IGNORECASE)
    # remove multi spaces
    text = re.sub(r'\s\s+', ' ', text)
    # replace \( with (
    text = text.replace('\(', '(').replace('\)', ')')
    return text


def clean_operands(operands):
    exclude_words = ["system property", "whether"]
    for i in range(len(operands)):
        for word in exclude_words:
            operands[i] = re.sub(r'\s*\b({})\b\s*'.format(word), '', operands[i])
    # remove multi spaces


def extract_merge_range(matches):
    range_s = {}
    # todo: simplify the filter
    for m in matches:
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
    return dict(sorted(range_e.items(), reverse=True))


class Detector:
    NOT_NUM_NP_POS = ["NOUN", "PRON", "PROPN", "X"]
    NP_POS = NOT_NUM_NP_POS + ["NUM"]

    def __init__(self, text, nlp_type='all', doc=None):
        self.text = clean_text(text)
        self.nlp = nlps[nlp_type]
        if doc is not None:
            self.doc = doc
        else:
            self.doc = self.nlp(self.text)
        self.doc = preprocess_doc(self.doc)
        self.dep_matcher = DependencyMatcher(self.nlp.vocab)
        self.matcher = Matcher(self.nlp.vocab)
        self.phrase_matcher = PhraseMatcher(self.nlp.vocab)

    def add_pattern(self, method, rules: list):
        if method == 'dep':
            for rule in rules:
                rule_name = 'PAT#{}'.format(self.dep_matcher.__len__())
                self.dep_matcher.add(rule_name, [rule])
        elif method == 'token':
            for rule in rules:
                rule_name = 'PAT#{}'.format(self.dep_matcher.__len__())
                self.matcher.add(rule_name, [rule])
        else:
            for rule in rules:
                rule_name = 'PAT#{}'.format(self.dep_matcher.__len__())
                self.phrase_matcher.add(rule_name, [rule])

    def match(self):
        res = set()
        matches = self.dep_matcher(self.doc)
        for match in matches:
            token_ids = self._remove_tokens(match)
            start = min(token_ids)
            end = max(token_ids)
            operands = self._extract_operands_dep(match)
            # replace which
            if self.doc[start].text in ['which', 'that']:
                p = start - 1
                while p >= 0 and self.doc[p].pos_ == 'PUNCT':
                    p -= 1
                if self.doc[p].pos_ in Detector.NP_POS:
                    start = p
                    op_data = self.doc[p].text
                    operands = [op for op in operands if op not in ['which', 'that']] + [op_data]
            res.add(DiscoursePattern(pattern_name=self.__class__.__name__,
                                     fragment=self.doc[start: end + 1].text,
                                     operands=operands,
                                     text=self.text,
                                     doc=self.doc,
                                     start=start,
                                     end=end + 1))
        return res

    def _extract_operands_dep(self, match):
        match_id, token_ids = match
        on_match, patterns = self.dep_matcher.get(self.nlp.vocab.strings[match_id])
        operands = [self.doc[token_ids[i]].text for i in range(len(token_ids)) if patterns[0][i]["RIGHT_ID"].startswith("op_")]
        clean_operands(operands)
        return operands

    def _remove_tokens(self, match):
        match_id, token_ids = match
        on_match, patterns = self.dep_matcher.get(self.nlp.vocab.strings[match_id])
        return [token_ids[i] for i in range(len(token_ids)) if "sub" not in patterns[0][i]["RIGHT_ID"]]
