from utils.nlp_factory import nlps
from spacy.matcher import PhraseMatcher
import re


class DiscoursePattern:

    nlp = nlps['clean']

    def __init__(self, pattern_name: str, fragment: str, operands: list, text: str, doc=None, start=-1, end=-1):
        self.pattern_name = pattern_name
        self.fragment = fragment
        self.operands = operands
        self.doc = doc
        self.start = start
        self.end = end
        self.pattern_type = self.get_pattern_type(text)

    def __eq__(self, other):
        if not isinstance(other, DiscoursePattern):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.pattern_name == other.pattern_name and str(self.fragment) == str(other.fragment) and set(self.operands) == set(other.operands)

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        return 'pattern_name: %s\t fragment: %s \t operands: %s' % (self.pattern_name, self.fragment, sorted(self.operands))

    def get_pattern_type(self, text):
        if self.pattern_name in ['VALUE_FOR_NP', 'NP_CD']:
            return 'concrete-value'
        elif self.pattern_name in ['NP_CD_TO_CD', 'NP_COMP_NP', 'NP_SAME_AS_NP']:
            return 'value-comparison'
        elif self.pattern_name in ['NP_SET_TO_BINARY_VALUE', 'NP_EXIST', 'NP_BE_BINARY_VALUE', 'NP_IF_BINARY_VALUE', 'SET_NP_TO_BINARY_VALUE']:
            return 'binary-value'
        elif self.pattern_name == 'NP_IN_VALUESET':
            return 'categorical-value'
        elif self.pattern_name == 'NP_SET_TO_VALUE':
            terms = ['at least', 'up to', 'lower', 'larger', 'more', 'negative', 'positive', 'multi', 'shorter', 'longer']
            if self.match_terms(terms, text) or self.match_if_before(text) or self.match_if():
                return 'value-comparison'
            return 'concrete-value'
        elif self.pattern_name == 'NP_BE_VALUE':
            if self.match_if_before(text) or re.search(r"(\b(not|positive|negative|no)\b)|n't", self.fragment) or self.match_if():
                return 'value-comparison'
            return 'concrete-value'
        elif self.pattern_name == 'CD_NP':
            terms = ['at least', 'up to', 'lower', 'larger', 'more', 'negative', 'positive', 'multi', 'last', 'first']
            if self.match_terms(terms, text) or self.match_if_before(text) or self.match_if():
                return 'value-comparison'
            return 'concrete-value'
        elif self.pattern_name == 'NP_OF_VALUE':
            terms = ['at least', 'up to', 'lower', 'larger', 'more', 'negative', 'positive', 'multi']
            if self.match_terms(terms, text):
                return 'value-comparison'
            return 'concrete-value'
        elif self.pattern_name == 'SET_NP_TO_VALUE':
            if self.match_if_before(text) or self.match_if():
                return 'value-comparison'
            return 'concrete-value'
        return None

    def match_if(self):
        doc = self.nlp(self.fragment)
        return any([token.lemma_ in ['if', 'when'] for token in doc])

    def match_if_before(self, text):
        if self.start == 0: return False
        end = self.start
        start = end - 5 if end >= 5 else 0
        doc = self.nlp(text)
        for token in doc[start: end + int(len(text.split())/4)]:
            if token.lemma_ in ['if', 'when']:
                return True
        return False

    def match_terms(self, terms, sentence):
        patterns = [self.nlp.make_doc(text) for text in terms]
        matcher = PhraseMatcher(self.nlp.vocab)
        matcher.add("TerminologyList", patterns)
        doc = self.nlp(sentence.lower())
        matches = matcher(doc)
        return len(matches) > 0
