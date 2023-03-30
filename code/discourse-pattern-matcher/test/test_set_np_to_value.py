import unittest
from detect.set_np_to_value import SET_NP_TO_VALUE
from utils.nlp_factory import nlps
from extractor import merge_np_for_text
import re

def print_detail(doc):
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.dep_, '#',token.tag_, '#',token.pos_)


class TestSET_NP_TO_VALUE(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = SET_NP_TO_VALUE(text, doc)
        print_detail(detector.doc)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = '''If `MinimumGroupingCount`=0, no grouping will be done regardless of the number of consecutive numbers.'''
        self.assertNotEmpty(text)

    def test01(self):
        text = '''• Log frequency, if checked, will set the frequency axis to log mode.'''
        self.assertNotEmpty(text)

    def test02(self):
        text = '''If the mode=OUT (or INOUT) and the
  jdbcType=CURSOR (i.e. Oracle REFCURSOR), you must specify a resultMap to map the ResultSet to the
  type of the parameter.'''
        self.assertNotEmpty(text)

    def test03(self):
        text = '''If you do not want these default excludes applied, you may disable them with the defaultexcludes=no attribute.'''
        self.assertNotEmpty(text)

    def test04(self):
        text = '''Attributes:
  useCache=true, flushCache=FlushCachePolicy.DEFAULT, resultSetType=DEFAULT,
  statementType=PREPARED, fetchSize=-1, timeout=-1,
  useGeneratedKeys=false.'''
        self.assertNotEmpty(text)

    def test05(self):
        text = '''Set the namespace of the current scope to namespace.'''
        self.assertNotEmpty(text)

    def test06(self):
        text = '''Attributes:
    useCache=true, flushCache=FlushCachePolicy.DEFAULT, resultSetType=DEFAULT,
    statementType=PREPARED, fetchSize=-1, timeout=-1,
    useGeneratedKeys=false'''
        self.assertNotEmpty(text)