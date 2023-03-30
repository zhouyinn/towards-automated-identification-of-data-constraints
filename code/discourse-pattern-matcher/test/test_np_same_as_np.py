import unittest
from detect.np_same_as_np import NP_SAME_AS_NP
from utils.nlp_factory import nlps
from extractor import merge_np_for_text


def print_detail(text, doc=None):
    if doc is None:
        doc = nlps['all'](text)
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.dep_, '#',token.tag_, '#',token.pos_)


class TestNP_SAME_AS_NP(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = NP_SAME_AS_NP(text, doc)
        print_detail(text, detector.doc)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = '''The target file name is identical to the source file name, with all leading directory information stripped off.'''
        self.assertNotEmpty(text)

    def test01(self):
        text = '''The target file name is identical to the source file name.'''
        self.assertNotEmpty(text)


if __name__ == '__main__':
    unittest.main()