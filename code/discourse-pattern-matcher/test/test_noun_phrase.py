import unittest
from detect.noun_phrase import NP_OF_VALUE, NP_CD, VALUE_FOR_NP, CD_NP
from utils.nlp_factory import nlps


def print_detail(doc):
    for token in doc:
        print(token.text, token.lemma_, token.dep_, token.tag_, token.pos_)


class TestNP_OF_NP(unittest.TestCase):
    def assertNotEmpty(self, text):
        detector = NP_OF_VALUE(text)
        res = detector.match()
        print_detail(detector.doc)
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = 'charset value of \"ISO-8859-1\"'
        self.assertNotEmpty(text)

    def test01(self):
        text = '''The only required attribute DELEGATE must be set to the name of a ruleset.'''
        self.assertNotEmpty(text)


class TestNP_CD(unittest.TestCase):
    def assertNotEmpty(self, text):
        detector = NP_CD(text)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        print(','.join([str(p) for p in res]))

    @unittest.skip('spaCy take the text as a noun phrase')
    def test01(self):
        text = "304 (not modified)"
        self.assertNotEmpty(text)


class TestNP_FOR_NP(unittest.TestCase):
    def assertNotEmpty(self, text):
        detector = VALUE_FOR_NP(text)
        res = detector.match()
        print_detail(detector.doc)
        self.assertNotEqual(0, len(res))
        print(','.join([str(p) for p in res]))

    def test01(self):
        text = "The epoch date for the calendar"
        self.assertNotEmpty(text)

    def test02(self):
        text = '''If the headers aren't available, a length of -1 will be returned, and NULL for the content
  type.'''
        self.assertNotEmpty(text)


class TestCD_NP(unittest.TestCase):
    def assertNotEmpty(self, text):
        detector = CD_NP(text)
        res = detector.match()
        print_detail(detector.doc)
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test01(self):
        text = '''If a Boolean
  tagged value does not exist or is invalid for one model element, a default value is assumed by
  the code generator.'''
        self.assertNotEmpty(text)

    def test02(self):
        text = '''Expansions can contain up to nine positional parameters.'''
        self.assertNotEmpty(text)

    def test03(self):
        text = '''If it is multi-line comment - only its first line is analyzed.'''
        self.assertNotEmpty(text)


if __name__ == '__main__':
    unittest.main()


