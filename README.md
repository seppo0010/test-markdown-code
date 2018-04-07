# Test Markdown Code

[![Build Status](https://travis-ci.org/seppo0010/test-markdown-code.svg?branch=master)](https://travis-ci.org/seppo0010/test-markdown-code)

Test your markdown files' code

## Example

Markdown

    ```py
    a = 'hello'
    print(a)
    ```
    <!-- tmc
    hello
    -->

Would produce the following markdown code

```py
a = 'hello'
print(a)
```
<!-- tmc
hello
-->

And executing run-markdown-code would pass the tests.
