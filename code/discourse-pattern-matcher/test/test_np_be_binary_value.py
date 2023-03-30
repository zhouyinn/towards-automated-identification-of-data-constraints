import unittest
from detect.np_be_binary_value import NP_BE_BINARY_VALUE
from utils.nlp_factory import nlps
from extractor import merge_np_for_text


def print_detail(text, doc=None):
    if doc is None:
        doc = nlps['all'](text)
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.dep_, '#',token.head.text, '#',token.tag_, '#',token.pos_)


class TestNP_BE_BINARY_VALUE(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = NP_BE_BINARY_VALUE(text, doc)
        print_detail(text, detector.doc)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = "the headers aren't available, aren't good"
        self.assertNotEmpty(text)

    def test01(self):
        text = '''If no layout is supplied the default pattern layout
  of "%m%n" will be used.'''
        # no layout is supplied
        self.assertNotEmpty(text)

    def test02(self):
        text = '''If regexp property is set, then list of packages will
  be interpreted as regular expressions.'''
        self.assertNotEmpty(text)

    def test03(self):
        text = '''Targets without such a description are deemed internal and will not be listed, unless either the -verbose or -debug option is used.'''
        self.assertNotEmpty(text)

    def test04(self):
        text = '''• The Backup on every save option is off by default, which results in a backup only being created
  the first time a buffer is saved in an editing session.'''
        self.assertNotEmpty(text)

    def test05(self):
        text = '''If the model has been altered (as indicated by the "*" in the titlebar of ArgoUML's window),
  then activating the "New" function is potentionally not the user's intention, since it will
  erase the changes.'''
        self.assertNotEmpty(text)

    def test06(self):
        text = '''Before Servlet API 2.5/Java EE 5, a WEB-INF/web.xml file was mandatory in a WAR file, so this task failed if the webxml attribute was missing.'''
        self.assertNotEmpty(text)

    def test07(self):
        text = '''If there is no configured
  suppressions file or the optional is set to true and
  suppressions file was not found the Filter accepts all audit events.'''
        self.assertNotEmpty(text)

    def test08(self):
        text = '''In addition, if you set ant.build.clonevm to true and build.sysclasspath has not been set, the bootclasspath of forked JVMs gets constructed as if build.sysclasspath had the value last.'''
        self.assertNotEmpty(text)


if __name__ == '__main__':
    unittest.main()