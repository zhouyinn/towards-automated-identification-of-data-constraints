import unittest
from detect.np_be_value import NP_BE_VALUE
from utils.nlp_factory import nlps
from extractor import merge_np_for_text
from model.detector import clean_text


def print_detail(text, doc=None):
    if doc is None:
        doc = nlps['all'](text)
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.dep_, '#',token.head.text, '#',token.tag_, '#',token.pos_)


class TestNP_BE_VALUE(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = NP_BE_VALUE(text, doc)
        print_detail(text, detector.doc)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = '''If the data source is not an RSAM data source, the RSAM
  viewer will indicate there is no RSAM data for the channel:

  
  
 

  Figure 29 If data source does not support RSAM'''
        # data source is not an RSAM data source,
        self.assertNotEmpty(text)

    def test01(self):
        text = '''The property `GroupedNumbersSeparator` \(default `-`\) determines which string separates the first and last of the grouped numbers.'''
        # The property `GroupedNumbersSeparator` \(default `-`\)
        self.assertNotEmpty(text)

    def test02(self):
        text = '''The length of the mapped region, defaults to 32 MB
  (32 * 1024 * 1024 bytes).'''
        self.assertNotEmpty(text)

    def test03(self):
        text = '''If the
  request is GET or HEAD and a prior response is cached, the proxy may use the
  cached message if it passes any restrictions in the Expires header field.'''
        self.assertNotEmpty(text)

    def test04(self):
#         longfile attribute is warn
        text = '''The default for the longfile attribute is warn which behaves just like the gnu option except that it produces a warning for each filepath encountered that does not match the limit.'''
        self.assertNotEmpty(text)

    def test05(self):
        text = '''The 16-based algorithm is the default.'''
        self.assertNotEmpty(text)

    def test06(self):
        text = '''All
  other responses must include an entity body or a Content-Length header field
  defined with a value of zero (0).'''
        self.assertNotEmpty(text)

    def test07(self):
        text = '''If the
  request is GET or HEAD and a prior response is cached, the proxy may use the
  cached message if it passes any restrictions in the Expires header field.'''
        self.assertNotEmpty(text)

    def test08(self):
        text = '''Unfortunately some ZIP implementations don't understand Zip64 extra fields or fail to parse archives with extra fields in local file headers that are not present in the central directory, one such implementation is the java.util.zip package of Java 5, that's why the jar tasks default to never.'''
        self.assertNotEmpty(text)

    def test09(self):
        text = '''Text: If the number of pattern letters is 4 or more, the full form is used; otherwise a short or abbreviated form is used if available.'''
        print(clean_text(text))
        self.assertNotEmpty(text)

    def test10(self):
        text = '''The Gregorian calendar adds two extra rules to state that years divisible by 100 are not leap, but those divisible by 400 are.'''
        self.assertNotEmpty(text)

    def test11(self):
        text = '''In addition, if you set ant.build.clonevm to true and build.sysclasspath has not been set, the bootclasspath of forked JVMs gets constructed as if build.sysclasspath had the value last.'''
        self.assertNotEmpty(text)





if __name__ == '__main__':
    unittest.main()