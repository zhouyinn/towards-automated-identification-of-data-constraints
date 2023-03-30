from model.discourse_pattern import DiscoursePattern
from eval_type import get_start
import unittest

class TestMatchTterms(unittest.TestCase):

    def test01(self):
        text = '''If the
  request is GET or HEAD and a prior response is cached, the proxy may use the
  cached message if it passes any restrictions in the Expires header field.'''
        frag = '''the
  request is GET or HEAD'''
        dispat = DiscoursePattern(pattern_name="NP_BE_VALUE",
                                  fragment=frag,
                                  operands=[],
                                  text=text,
                                  doc=None,
                                  start=get_start(text, frag),
                                  end=-1)
        print(dispat.start)
        self.assertTrue(dispat.match_if_before(text))
        # terms = ['at least', 'up to', 'lower', 'larger', 'more', 'negative', 'positive', 'multi']
        # self.assertTrue(dispat.match_terms(terms, text))