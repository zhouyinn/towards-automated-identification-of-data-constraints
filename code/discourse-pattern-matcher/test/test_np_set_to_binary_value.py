import unittest
from detect.np_set_to_binary_value import NP_SET_TO_BINARY_VALUE
from utils.nlp_factory import nlps
from extractor import merge_np_for_text


def print_detail(text, doc=None):
    if doc is None:
        doc = nlps['all'](text)
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.tag_, '#',token.pos_, '#',token.dep_, '#',token.head.text)


class TestNP_SET_TO_BINARY_VALUE(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = NP_SET_TO_BINARY_VALUE(text, doc)
        res = detector.match()
        print_detail(detector.doc)
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = '''No appender accumulation since the additivity flag is set to false.'''
        self.assertNotEmpty(text)

    def test01(self):
        text = '''The readOnly attribute can be set to true or false.'''
        self.assertNotEmpty(text)

    def test02(self):
        text = '''This task will not create any index entries for archives that are empty or only contain files inside the META-INF directory unless the indexmetainf attribute has been set to true.'''
        self.assertNotEmpty(text)

    def test03(self):
        text = '''The modulepath requires fork to be set to true.'''
        self.assertNotEmpty(text)

    def test04(self):
        text = '''Toplink beans can now be built with the standard weblogic element, as long as the newCMP attribute is set to true
  The TopLink element is used to handle beans which use Toplink for the CMP operations.'''
        self.assertNotEmpty(text)

    def test05(self):
        text = '''Play the bell.wav sound file if the build succeeded, or the ohno.wav sound file if the build failed, three times, if the fun property is set to true.'''
        self.assertNotEmpty(text)

    def test06(self):
        text = '''• AT_WORD_START - If set to TRUE, the sequence will only be highlighted if it occurs at the
  beginning of a word.'''
        self.assertNotEmpty(text)

    def test07(self):
        text = '''If lineUpClosingBracket is set to true, then closing brackets on the current line will
  line up with the line containing the matching opening bracket.'''
        self.assertNotEmpty(text)

    def test08(self):
        text = '''The doubleBracketIndent property, if set to the default of false, results in code indented
  like so:'''
        self.assertNotEmpty(text)

    def test09(self):
        text = '''If the HIGHLIGHT_DIGITS attribute is set to TRUE, jEdit will attempt to highlight numbers in
  this ruleset.'''
        self.assertNotEmpty(text)

    def test10(self):
        text = '''The task will fail if the file is not included, unless the needxmlfile attribute is set to false.'''
        self.assertNotEmpty(text)

    def test11(self):
        text = '''The http://xml.org/sax/features/namespaces feature is set by default to false by the JAXP implementation used by Ant.'''
        self.assertNotEmpty(text)

    def test12(self):
        text = '''If the HIGHLIGHT_DIGITS attribute is set to TRUE, jEdit will attempt to highlight numbers in
  this ruleset.'''
        self.assertNotEmpty(text)


if __name__ == '__main__':
    unittest.main()