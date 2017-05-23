---
layout: post
section-type: post
title: new TDD-Chapter 3. Testing a Simple Home Page with Unit Tests
category: tdd
tags: [ 'tdd' ]
---

## 3.1. Our First Django App, and Our First Unit Test

```
$ python manage.py startapp lists
```

```
superlists/
├── db.sqlite3
├── functional_tests.py
├── lists
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
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


## 3.2. Unit Tests, and How They Differ from Functional Tests

## 3.3. Unit Testing in Django

lists/tests.py

```python
from django.test import TestCase

class SmokeTest(TestCase):

    def test_bad_maths(self):
        self.assertEqual(1 + 1, 3)
```

```
$ python manage.py test
Creating test database for alias 'default'...
F
======================================================================
FAIL: test_bad_maths (lists.tests.SmokeTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/lists/tests.py", line 6, in test_bad_maths
    self.assertEqual(1 + 1, 3)
AssertionError: 2 != 3

 ---------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```

```
$ git status  # should show you lists/ is untracked
$ git add lists
$ git diff --staged  # will show you the diff that you're about to commit
$ git commit -m "Add app for lists, with deliberately failing unit test"
```

## 3.4. Django’s MVC, URLs, and View Functions

lists/tests.py

```python
from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page  

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')  
        self.assertEqual(found.func, home_page)  
```

```
$ python manage.py test
ImportError: cannot import name 'home_page'
```

## 3.5. At Last! We Actually Write Some Application Code!

lists/views.py

```python
from django.shortcuts import render

# Create your views here.
home_page = None
```

```
$ python manage.py test
Creating test database for alias 'default'...
E
======================================================================
ERROR: test_root_url_resolves_to_home_page_view (lists.tests.HomePageTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/lists/tests.py", line 8, in
test_root_url_resolves_to_home_page_view
    found = resolve('/')
  File ".../django/urls/base.py", line 27, in resolve
    return get_resolver(urlconf).resolve(path)
  File ".../django/urls/resolvers.py", line 392, in resolve
    raise Resolver404({'tried': tried, 'path': new_path})
django.urls.exceptions.Resolver404: {'tried': [[<RegexURLResolver
<RegexURLPattern list> (admin:admin) ^admin/>]], 'path': ''}

 ---------------------------------------------------------------------
Ran 1 test in 0.002s

FAILED (errors=1)
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```

## 3.6. urls.py

superlists/urls.py

```python
from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
]
```

```
python manage.py test

[...]
TypeError: view must be a callable or a list/tuple in the case of include().
```

lists/views.py

```python
from django.shortcuts import render

# Create your views here.
def home_page():
    pass
```

```
$ python manage.py test
Creating test database for alias 'default'...
.
 ---------------------------------------------------------------------
Ran 1 test in 0.003s

OK
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```

```
$ git diff  # should show changes to urls.py, tests.py, and views.py
$ git commit -am "First unit test and url mapping, dummy view"
```

## 3.7. Unit Testing a View

lists/tests.py

```python
from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)


    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  
        response = home_page(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.startswith('<html>'))  
        self.assertIn('<title>To-Do lists</title>', html)  
        self.assertTrue(html.endswith('</html>'))
```
FT

```
TypeError: home_page() takes 0 positional arguments but 1 was given
```

- Minimal code change:  
lists/views.py

```
def home_page(request):
    pass
```

- Tests

```
html = response.content.decode('utf8')
AttributeError: 'NoneType' object has no attribute 'content'
```

- Code—​we use django.http.HttpResponse, as predicted:

lists/views.py

```
from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return HttpResponse()
```

- Tests again:

```
self.assertTrue(html.startswith('<html>'))
AssertionError: False is not true
```

- Code again:

lists/views.py

```
def home_page(request):
    return HttpResponse('<html>')
```

- Tests:

```
AssertionError: '<title>To-Do lists</title>' not found in '<html>'
```

- Code

lists/views.py

```
def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title>')
```

- Tests—​almost there?

```
self.assertTrue(html.endswith('</html>'))
AssertionError: False is not true
```

- Come on, one last effort:

lists/views.py

```
def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title></html>')
```

- Surely?

```
$ python manage.py test
Creating test database for alias 'default'...
..
 ---------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
System check identified no issues (0 silenced).
Destroying test database for alias 'default'...
```

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

```
$ git diff  # should show our new test in tests.py, and the view in views.py
$ git commit -am "Basic view now returns minimal HTML"
```

```
$ git log --oneline
a6e6cc9 Basic view now returns minimal HTML
450c0f3 First unit test and url mapping, dummy view
ea2b037 Add app for lists, with deliberately failing unit test
[...]
```


### Useful Commands and Concepts
#### Running the Django dev server
python manage.py runserver

#### Running the functional tests
python functional_tests.py

#### Running the unit tests
python manage.py test

#### The unit-test/code cycle

1. Run the unit tests in the terminal.

2. Make a minimal code change in the editor.

3. Repeat!
