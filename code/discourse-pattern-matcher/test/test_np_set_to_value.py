import unittest
from detect.np_set_to_value import NP_SET_TO_VALUE
from utils.nlp_factory import nlps
from extractor import merge_np_for_text


def print_detail(text, doc=None):
    if doc is None:
        doc = nlps['all'](text)
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.dep_, '#',token.tag_, '#',token.pos_)


class TestNP_SET_TO_VALUE(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = NP_SET_TO_VALUE(text, doc)
        print_detail(text, detector.doc)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = '''If the margin is set to 0, then the width of the text area window is used to determine where to wrap lines.'''
        self.assertNotEmpty(text)

    def test01(self):
        text = '''By default the ElementStyleOption is set to COMPACT_NO_ARRAY,
  the TrailingArrayCommaOption is set to NEVER,
  and the ClosingParensOption is set to NEVER.'''
        self.assertNotEmpty(text)

    def test02(self):
        text = '''An entry may be marked as relevant.'''
        self.assertNotEmpty(text)

    def test03(self):
        text = '''when the fileIndex attribute is set to "min" but all the other settings are the
  same the "fixed window" strategy will be performed.'''
        self.assertNotEmpty(text)

    def test04(self):
        text = '''Note that although BSD Syslog records are required to be
  1024 bytes or shorter the SyslogLayout does not truncate them.'''
        self.assertNotEmpty(text)

    def test05(self):
        text = '''The flushInterval can be set to any positive integer and should represent a reasonable amount of
  time specified in milliseconds.'''
        self.assertNotEmpty(text)

    def test06(self):
        text = '''Since Ant 1.8.0, all zip, jar and similar archives written by Ant will set this flag, if the encoding has been set to UTF-8.'''
        self.assertNotEmpty(text)

    def test07(self):
        text = '''If the longfile attribute is set to fail, any long paths will cause the tar task to fail.'''
        self.assertNotEmpty(text)

    def test08(self):
        text = '''If a <srcfiles> element is used, without also specifying a <mapper> element, the default behavior is to use a merge_mapper, with the to attribute set to the value of the targetfile attribute.'''
        self.assertNotEmpty(text)

    def test09(self):
        text = '''[[Warning]] Warning
  The V0.20 version of ArgoUML provides a single design goal, Unspecified, with its
  slider set by default to priority 1.'''
        self.assertNotEmpty(text)

    def test10(self):
        text = '''when the fileIndex attribute is set to "min" but all the other settings are the
  same the "fixed window" strategy will be performed.'''
        self.assertNotEmpty(text)

    def test11(self):
        text = '''The only required attribute DELEGATE must be set to the name of a ruleset.'''
        self.assertNotEmpty(text)

    def test12(self):
        text = '''[[Warning]] Warning
    The V0.20 version of ArgoUML provides a single design goal, Unspecified, with its
    slider set by default to priority 1.'''
        self.assertNotEmpty(text)


if __name__ == '__main__':
    unittest.main()