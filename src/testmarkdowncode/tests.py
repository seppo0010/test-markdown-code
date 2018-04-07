# -*- coding: utf-8 -*-

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


def easy_py():
    return create_template(
        'py',
        'print(2)',
        '2',
    )

class TestTestMarkdownCode(unittest.TestCase):
    def run_tests(self, code, expected_tests):
        tests = TestMarkdownCode.find_tests(code)
        for test in tests:
            TestMarkdownCode.get_test(*test)(self)
        self.assertEqual(expected_tests, len(tests))

    def test_py(self):
        self.run_tests(easy_py(), 1)

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
            easy_py(),
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

    def test_unsupported_language(self):
        with self.assertRaises(ValueError):
            self.run_tests(multitrim('''
                No expected:
                ```wat
                print(1)
                ```
                <!-- tmc
                1
                -->
            '''), 0)

    def test_ignore_incomplete(self):
        self.run_tests(multitrim('''
        No expected:
        ```py
        print(1)
        ```

        Unlabeled expected:
        ```py
        print(1)
        ```
        <!--
        1
        -->
        '''), 0)

    def test_not_ascii(self):
        self.run_tests('ħ€łłø\n' + easy_py(), 1)

    def test_after_incomplete(self):
        self.run_tests(multitrim('''
        ```py
        print(1)
        ```

        ''' + easy_py()), 1)
