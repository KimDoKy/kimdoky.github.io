---
layout: post
section-type: post
title: new TDD-Chapter 4. What Are We Doing with All These Tests? (And, Refactoring)
category: tdd
tags: [ 'tdd' ]
---

## 4.1. Programming Is like Pulling a Bucket of Water up from a Well

## 4.2. Using Selenium to Test User Interactions

```
$ python functional_tests.py
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 19, in
test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

 ---------------------------------------------------------------------
Ran 1 test in 1.609s

FAILED (failures=1)
```

functional_tests.py

```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text  
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')  
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')  

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)  
        time.sleep(1)  

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')  
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        # There is still a text box inviting her to add another item. She
        # enters "Use peacock feathers to make a fly" (Edith is very
        # methodical)
        self.fail('Finish the test!')

        # The page updates again, and now shows both items on her list
        [...]
```

```
$ python functional_tests.py
[...]
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: h1
```

```
$ git diff  # should show changes to functional_tests.py
$ git commit -am "Functional test now checks we can input a to-do item"
```

## 4.3. The “Don’t Test Constants” Rule, and Templates to the Rescue

### Refactoring to Use a Template

```
$ python manage.py test
[...]
OK
```

lists/templates/home.html

```
<html>
    <title>To-Do lists</title>
</html>
```

lists/views.py

```
from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')
```

```
$ python manage.py test
[...]
======================================================================
ERROR: test_home_page_returns_correct_html (lists.tests.HomePageTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/lists/tests.py", line 17, in
test_home_page_returns_correct_html
    response = home_page(request)
  File "/.../superlists/lists/views.py", line 5, in home_page
    return render(request, 'home.html')
  File "/usr/local/lib/python3.6/dist-packages/django/shortcuts.py", line 48,
in render
    return HttpResponse(loader.render_to_string(*args, **kwargs),
  File "/usr/local/lib/python3.6/dist-packages/django/template/loader.py", line
170, in render_to_string
    t = get_template(template_name, dirs)
  File "/usr/local/lib/python3.6/dist-packages/django/template/loader.py", line
144, in get_template
    template, origin = find_template(template_name, dirs)
  File "/usr/local/lib/python3.6/dist-packages/django/template/loader.py", line
136, in find_template
    raise TemplateDoesNotExist(name)
django.template.base.TemplateDoesNotExist: home.html

 ---------------------------------------------------------------------
Ran 2 tests in 0.004s
```

superlists/settings.py

```
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'lists',
]
```

```
$ python manage.py test
    [...]
    self.assertTrue(html.endswith('</html>'))
AssertionError: False is not true
```

lists/tests.py

```
self.assertTrue(html.strip().endswith('</html>'))
```

```
$ python manage.py test
[...]
OK
```

### The Django Test Client

lists/tests.py

```
from django.template.loader import render_to_string
[...]

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')
        expected_html = render_to_string('home.html')
        self.assertEqual(html, expected_html)
```

lists/tests.py

```
def test_home_page_returns_correct_html(self):
    response = self.client.get('/')  

    html = response.content.decode('utf8')  
    self.assertTrue(html.startswith('<html>'))
    self.assertIn('<title>To-Do lists</title>', html)
    self.assertTrue(html.strip().endswith('</html>'))

    self.assertTemplateUsed(response, 'home.html')
```

```
Ran 2 tests in 0.016s

OK
```

lists/tests.py

```
self.assertTemplateUsed(response, 'wrong.html')
```

```
AssertionError: False is not true : Template 'wrong.html' was not a template
used to render the response. Actual template(s) used: home.html
```

lists/tests.py (ch04l010)

```
from django.test import TestCase

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
```

## 4.4. On Refactoring

```
$ git status # see tests.py, views.py, settings.py, + new templates folder
$ git add .  # will also add the untracked templates folder
$ git diff --staged # review the changes we're about to commit
$ git commit -m "Refactor home page view to use a template"
```

## 4.5. A Little More of Our Front Page

lists/templates/home.html

```
[...]
    <h1>Your To-Do list</h1>
    <input id="id_new_item" />
</body>
[...]
```

FT

```
AssertionError: '' != 'Enter a to-do item'
```

lists/templates/home.html

```
<input id="id_new_item" placeholder="Enter a to-do item" />
```

```
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_list_table"]
```

lists/templates/home.html

```
<input id="id_new_item" placeholder="Enter a to-do item" />
<table id="id_list_table">
</table>
</body>
```

```
File "functional_tests.py", line 43, in
test_can_start_a_list_and_retrieve_it_later
  any(row.text == '1: Buy peacock feathers' for row in rows)
AssertionError: False is not true
```

functional_tests.py

```
self.assertTrue(
    any(row.text == '1: Buy peacock feathers' for row in rows),
    "New to-do item did not appear in table"
)
```

```
AssertionError: False is not true : New to-do item did not appear in table
```

```
$ git diff
$ git commit -am "Front page HTML now generated from a template"
```

## 4.6. Recap: The TDD Process
