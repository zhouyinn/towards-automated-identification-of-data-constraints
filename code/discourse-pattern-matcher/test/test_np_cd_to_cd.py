import unittest
from detect.np_cd_to_cd import NP_CD_TO_CD
from utils.nlp_factory import nlps
from extractor import merge_np_for_text
from model.detector import clean_text


def print_detail(text, doc=None):
    if doc is None:
        doc = nlps['all'](text)
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.dep_, '#',token.tag_, '#',token.pos_)


class TestNP_CD_TO_CD(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = NP_CD_TO_CD(text, doc)
        print_detail(text, detector.doc)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = '''Two to four authors: First letters of last names concatenated.'''
        self.assertNotEmpty(text)

    def test01(self):
        text = '''One may prioritize entries from prio3 \(low\) to prio1 \(high\).'''
        self.assertNotEmpty(text)

    def test02(self):
        text = '''Legal values are between 0\n  and 95.'''
        # print('@@@@', clean_text(text))
        self.assertNotEmpty(text)

    def test03(self):
        text = '''Sweek of year, from 01 to 53'''
        self.assertNotEmpty(text)


if __name__ == '__main__':
    unittest.main()