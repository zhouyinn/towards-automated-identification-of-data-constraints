import unittest
from detect.np_comp_value import NP_COMP_NP
from utils.nlp_factory import nlps
from extractor import merge_np_for_text


def print_detail(text, doc=None):
    if doc is None:
        doc = nlps['all'](text)
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.dep_, '#',token.tag_, '#',token.pos_)


class TestNP_COMP_VALUE(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = NP_COMP_NP(text, doc)
        # print_detail(text, detector.doc)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = "source file is newer than the destination file"
        self.assertNotEmpty(text)

    def test01(self):
        text = "Band pass filter removes signals above Max. frequency or lower than Min. frequency."
        self.assertNotEmpty(text)

    def test02(self):
        text = '''The usetimestamp option enables you to control downloads so that the remote file is only fetched if newer than the local copy.'''
        self.assertNotEmpty(text)

    def test03(self):
        text = '''It will be highlighted in yellow when the number of to-do items grows above 50 todo
  items, and red when above 100.'''
        self.assertNotEmpty(text)

    def test04(self):
        text = '''Expires = "Expires" ":" HTTP-date
  An example of its use is
  Expires: Thu, 01 Dec 1994 16:00:00 GMT
  If the date given is equal to or earlier than the value of the Date header, the
  recipient must not cache the enclosed entity.'''
        self.assertNotEmpty(text)

    def test05(self):
        text = '''A user agent should
  never automatically redirect a request more than 5 times, since such
  redirections usually indicate an infinite loop.'''
        self.assertNotEmpty(text)

    def test06(self):
        text = '''9.2.2 RSAM Alarm
  If the Alarm option is checked, Swarm will play an audible alarm in Value view whenever the latest RSAM
  value acquired is equal to or greater than the Event threshold specified under Event Options.'''
        self.assertNotEmpty(text)

    def test07(self):
        text = '''9.2.2 RSAM Alarm\n  If the Alarm option is checked, Swarm will play an audible alarm in Value view whenever the latest RSAM\n  value acquired is equal to or greater than the Event threshold specified under Event Options.'''
        self.assertNotEmpty(text)


if __name__ == '__main__':
    unittest.main()