import unittest
from detect.np_if_binary_value import NP_IF_BINARY_VALUE
from utils.nlp_factory import nlps
from extractor import merge_np_for_text


def print_detail(text, doc=None):
    if doc is None:
        doc = nlps['no_en'](text)
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.dep_, '#', token.head.text, '#', token.tag_, '#',token.pos_)


class TestNP_IF_BINARY_VALUE(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = NP_IF_BINARY_VALUE(text, doc)
        print_detail(text, detector.doc)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = '''log4j2.enableDirectEncoders - if "true" (the default) log events are converted to text and this
  text is converted to bytes without creating temporary objects.'''
        self.assertNotEmpty(text)

    def test01(self):
        text = '''A project can have a set of tokens that might be automatically expanded if found when a file is copied, when the filtering-copy behavior is selected in the tasks that support this.'''
        self.assertNotEmpty(text)


if __name__ == '__main__':
    unittest.main()