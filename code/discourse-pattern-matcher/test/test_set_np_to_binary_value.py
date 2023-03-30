import unittest
from detect.set_np_to_binary_value import SET_NP_TO_BINARY_VALUE
from utils.nlp_factory import nlps
from extractor import merge_np_for_text


def print_detail(text, doc=None):
    if doc is None:
        doc = nlps['all'](text)
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.dep_, '#',token.tag_, '#',token.pos_)


class TestSET_NP_TO_BINARY_VALUE(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = SET_NP_TO_BINARY_VALUE(text, doc)
        # print_detail(text, detector.doc)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = '''Similarly, if failonerror=false and fork=false, then <java> must return 0 otherwise the build will exit, as the class was run by the build JVM.'''
        self.assertNotEmpty(text)

    def test01(self):
        text = '''GelfLayout is garbage-free when used with compressionType="OFF",
  as long as no additional field contains '${' (variable substitution).'''
        self.assertNotEmpty(text)

    def test02(self):
        text = '''However,\n  by setting setterCanReturnItsClass property to true\n  definition of a setter is expanded, so that setter return type can also\n  be a class in which setter is declared.'''
        self.assertNotEmpty(text)

    def test03(self):
        text = '''If you set the inheritrefs attribute to true, all references will be copied, but they will not override references defined in the new project.'''
        self.assertNotEmpty(text)