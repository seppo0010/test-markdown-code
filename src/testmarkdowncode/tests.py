import re
import unittest

from . import TestMarkdownCode


def multitrim(s):
    return re.sub(r'^\s+', '', s, 0, re.M)

def create_template(lang, code, result):
    return multitrim('''
    ```{lang}
    {code}
    ```
    <!-- tmc
    {result}
    -->
    ''').format(lang=lang, code=code, result=result)


class TestTestMarkdownCode(unittest.TestCase):
    def run_tests(self, code, expected_tests):
        tests = TestMarkdownCode.find_tests(code)
        for test in tests:
            TestMarkdownCode.get_test(*test)(self)
        self.assertEqual(expected_tests, len(tests))

    def test_py(self):
        self.run_tests(create_template(
            'py',
            'print(2)',
            '2',
        ), 1)

    def test_js(self):
        self.run_tests(create_template(
            'js',
            'console.log(2)',
            '2',
        ), 1)

    def test_multi(self):
        self.run_tests(multitrim(
        '''
        # My title

        My example
        {}

        My example 2
        {}
        ''').format(
            create_template(
                'py',
                'print(2)',
                '2',
            ),
            create_template(
                'js',
                'console.log(3)',
                '3',
            )
        ), 2)

    def test_fail(self):
        with self.assertRaises(AssertionError):
            self.run_tests(create_template(
                'py',
                'print(2)',
                '3',
            ), 1)
