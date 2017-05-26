---
layout: post
section-type: post
title: new TDD-Chapter 6. Improving Functional Tests: Ensuring Isolation and Removing Voodoo Sleeps
category: tdd
tags: [ 'tdd' ]
---

## 6.1. Ensuring Test Isolation in Functional Tests

```
$ mkdir functional_tests
$ touch functional_tests/__init__.py
```

```
$ git mv functional_tests.py functional_tests/tests.py
$ git status # shows the rename to functional_tests/tests.py and __init__.py
```

```
.
├── db.sqlite3
├── functional_tests
│   ├── __init__.py
│   └── tests.py
├── lists
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_item_text.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── __pycache__
│   ├── templates
│   │   └── home.html
│   ├── tests.py
│   └── views.py
├── manage.py
└── superlists
    ├── __init__.py
    ├── __pycache__
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

functional_tests/tests.py (ch06l001)

```Python
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        [...]
```

functional_tests/tests.py (ch06l002)

```Python
def test_can_start_a_list_and_retrieve_it_later(self):
    # Edith has heard about a cool new online to-do app. She goes
    # to check out its homepage
    self.browser.get(self.live_server_url)
```

```
$ python manage.py test functional_tests
Creating test database for alias 'default'...
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later
(functional_tests.tests.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/functional_tests/tests.py", line 65, in
test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

 ---------------------------------------------------------------------
Ran 1 test in 6.578s

FAILED (failures=1)
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```

```
$ git status # functional_tests.py renamed + modified, new __init__.py
$ git add functional_tests
$ git diff --staged -M
$ git commit  # msg eg "make functional_tests an app, use LiveServerTestCase"
```

### Running Just the Unit Tests

```
$ python manage.py test
Creating test database for alias 'default'...
......F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later
[...]
AssertionError: Finish the test!

 ---------------------------------------------------------------------
Ran 7 tests in 6.732s

FAILED (failures=1)
```

```
$ python manage.py test lists
Creating test database for alias 'default'...
......
 ---------------------------------------------------------------------
Ran 6 tests in 0.009s

OK
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```

## 6.2. Aside: Upgrading Selenium and Geckodriver

## 6.3. On implicit and explicit waits, and voodoo time.sleeps

functional_tests/tests.py

```python
# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list table
inputbox.send_keys(Keys.ENTER)
time.sleep(1)

self.check_for_row_in_list_table('1: Buy peacock feathers')
```

functional_tests/tests.py (ch06l004)

```python
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10  
[...]

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:  
            try:
                table = self.browser.find_element_by_id('id_list_table')  
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return  
            except (AssertionError, WebDriverException) as e:  
                if time.time() - start_time > MAX_WAIT:  
                    raise e  
                time.sleep(0.5)  
```

functional_tests/tests.py (ch06l005)

```python
[...]
# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list table
inputbox.send_keys(Keys.ENTER)
self.wait_for_row_in_list_table('1: Buy peacock feathers')

# There is still a text box inviting her to add another item. She
# enters "Use peacock feathers to make a fly" (Edith is very
# methodical)
inputbox = self.browser.find_element_by_id('id_new_item')
inputbox.send_keys('Use peacock feathers to make a fly')
inputbox.send_keys(Keys.ENTER)

# The page updates again, and now shows both items on her list
self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
self.wait_for_row_in_list_table('1: Buy peacock feathers')
```

```
$ python manage.py test
Creating test database for alias 'default'...
......F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later
(functional_tests.tests.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/functional_tests/tests.py", line 73, in
test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

 ---------------------------------------------------------------------
Ran 7 tests in 4.552s

FAILED (failures=1)
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```

functional_tests/tests.py (def wait_for_row_in_list_table)

```python
rows = table.find_elements_by_tag_name('tr')
self.assertIn('foo', [row.text for row in rows])
return
```

```
self.assertIn('foo', [row.text for row in rows])
AssertionError: 'foo' not found in ['1: Buy peacock feathers']
```

functional_tests/tests.py (ch06l007)

```python
try:
    table = self.browser.find_element_by_id('id_nothing')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])
    return
[...]
```

```
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_nothing"]
```

코드를 원래대로 되돌려 놓고 마지막 테스트를 실행합니다.

```
$ python manage.py test
[...]
AssertionError: Finish the test!
```
