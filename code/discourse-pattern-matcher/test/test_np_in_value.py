import unittest
from detect.np_in_value import NP_IN_VALUE
from utils.nlp_factory import nlps
from extractor import merge_np_for_text


def print_detail(text, doc=None):
    if doc is None:
        doc = nlps['all'](text)
    for token in doc:
        print(token.text, '#', token.lemma_, '#',token.dep_, '#',token.tag_, '#',token.pos_)


class TestNP_IN_VALUE(unittest.TestCase):
    def assertNotEmpty(self, text):
        doc = merge_np_for_text(text)[0]
        detector = NP_IN_VALUE(text, doc)
        # print_detail(text, detector.doc)
        res = detector.match()
        self.assertNotEqual(0, len(res))
        for r in res:
            print(r)

    def test00(self):
        text = '''6.2.1 P and S
  When doing a P or S pick, users must traverse all the way down the menu tree to determine onset
  (Emergent or Impulsive), polarity, and weight (0 to 4) of the pick.'''
        self.assertNotEmpty(text)

    def test01(self):
        text = '''The standard set of fields in a period are years, months, weeks, days, hours, minutes, seconds and millis.'''
        self.assertNotEmpty(text)

    def test02(self):
        text = '''time spans: 1 hour,
  12 hours, 1 day, 2 days, 1 week, 2 weeks, 4 weeks, 6 weeks, and 8 weeks'''
        self.assertNotEmpty(text)

    def test03(self):
        text = '''Encoding considerations: only "7bit", "8bit", or "binary" are
  permitted'''
        self.assertNotEmpty(text)

    def test04(self):
        text = '''type: directory or regular'''
        self.assertNotEmpty(text)

    def test05(self):
        text = '''Classifier ( metaclass, powertype, process, thread and
  utility).'''
        self.assertNotEmpty(text)

    def test06(self):
        text = '''ArgoUML provides the standard
  stereotypes for a classifier: metaclass, powertype, process, thread and utility.'''
        self.assertNotEmpty(text)

    def test07(self):
        text = '''There are two “wrap modes”, “soft” and “hard”; they are described
  below.'''
        self.assertNotEmpty(text)

    def test08(self):
        text = '''Supported server types are Unix, NT, OS2, VMS, and OS400.'''
        self.assertNotEmpty(text)

    def test09(self):
        text = '''The standard set of fields in a period are years, months, weeks, days, hours, minutes, seconds and millis.'''
        self.assertNotEmpty(text)

    def test10(self):
        text = '''Options are Wave, Spectra, Spectrogram,
  or Particle Motion.'''
        self.assertNotEmpty(text)

    def test11(self):
        text = '''• In the current buffer for future editing sessions by placing the following in one of the first or last
  10 lines of the buffer, where mode is either “none”, “soft” or “hard”, and column is the desired
  wrap margin:'''
        self.assertNotEmpty(text)

    def test12(self):
        text = '''Supported read
  formats are SAC, SEED, miniSEED, SEISAN, Matlab-readable text file, and WIN.'''
        self.assertNotEmpty(text)

    def test13(self):
        text = '''• In the current buffer for future editing sessions by placing the following in one of the first or last
  10 lines of the buffer, where mode is either “none”, “soft” or “hard”, and column is the desired
  wrap margin:'''
        self.assertNotEmpty(text)

    def test14(self):
        text = '''A Filter
  will be called on one of its filter methods and will return a Result, which is an Enum that has
  one of 3 values - ACCEPT, DENY or NEUTRAL.'''
        self.assertNotEmpty(text)

    def test15(self):
        text = '''The set of built-in
  levels includes TRACE, DEBUG, INFO, WARN, ERROR, and FATAL.'''
        self.assertNotEmpty(text)

    def test16(self):
        text = '''Attributes: statement an array of strings which is the SQL statement to execute, keyProperty which
  is the property of the parameter object that will be updated with the new value, before which must be either
  true or false to denote if the SQL statement should be executed before or after the insert,
  resultType which is the Java type of the keyProperty, and statementType is a type of the statement that is any one of STATEMENT, PREPARED or CALLABLE that is mapped to Statement, PreparedStatement and CallableStatement respectively.'''
        self.assertNotEmpty(text)

    def test17(self):
        text = '''The facility option must be set to one of
  "KERN", "USER", "MAIL", "DAEMON", "AUTH", "SYSLOG", "LPR", "NEWS", "UUCP", "CRON", "AUTHPRIV",
  "FTP", "NTP", "AUDIT", "ALERT", "CLOCK", "LOCAL0", "LOCAL1", "LOCAL2", "LOCAL3", "LOCAL4", "LOCAL5",
  "LOCAL6", or "LOCAL7".'''
        self.assertNotEmpty(text)

    def test18(self):
        text = '''Maximum entity length: Long#MAX_VALUE.'''
        self.assertNotEmpty(text)

    def test19(self):
        text = '''Basically it says, that you have to set the manifest entry Multi-Release: true and place all additional or overwriting classes in META-INF/versions/number/package-structure, e.g. '''
        self.assertNotEmpty(text)

    def test20(self):
        text = '''Its value must be a number and is interpreted as seconds since the epoch (midnight 1970-01-01).'''
        self.assertNotEmpty(text)

    def test21(self):
        text = '''The property `GroupedNumbersSeparator` \(default `-`\) determines which string separates the first and last of the grouped numbers.'''
        self.assertNotEmpty(text
                            )

if __name__ == '__main__':
    unittest.main()