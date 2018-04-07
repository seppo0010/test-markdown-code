import hashlib
import re
import subprocess
import unittest


class TestMarkdownCode(unittest.TestCase):
    tests = []

    @staticmethod
    def get_test(lang, code, expected):
        def test(self):
            if lang == 'py':
                output = subprocess.check_output(('python', '-c', code)).decode('utf8')
            elif lang == 'py3':
                output = subprocess.check_output(('python3', '-c', code)).decode('utf8')
            elif lang == 'js':
                output = subprocess.check_output(('nodejs', '-e', code)).decode('utf8')
            else:
                raise ValueError('unsupported language {}'.format(lang))
            self.longMessage = True
            self.assertEqual(output.strip(), expected.strip(), 'Running\n{}'.format(code))
        return test

    @staticmethod
    def find_tests(markdown):
        return [
            (lang, code, expected)
            for (lang, code, expected)
            in re.findall(
                r'^```(.*?)?\n(.*?)?```(?:\n<\!--\s+tmc(.*?)-->)?',
                markdown, re.M|re.S
            )
            if '' not in (lang, code, expected)
        ]

    @staticmethod
    def create_tests(markdown):
        for (lang, code, expected) in TestMarkdownCode.find_tests(markdown):
            test = 'test_{}'.format(hashlib.sha1((lang+code+expected).encode('utf8')).hexdigest())
            setattr(TestMarkdownCode, test, TestMarkdownCode.get_test(lang, code, expected))
            TestMarkdownCode.tests.append(test)

    @staticmethod
    def load_tests(test_cases):
        for test in TestMarkdownCode.tests:
            test_cases.addTest(TestMarkdownCode(test))
