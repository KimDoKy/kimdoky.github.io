---
layout: post
section-type: post
title: new TDD-Chapter 5. Saving User Input- Testing the Database
category: tdd
tags: [ 'tdd' ]
---

## 5.1. Wiring Up Our Form to Send a POST Request

lists/templates/home.html

```
<h1>Your To-Do list</h1>
<form method="POST">
    <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
</form>

<table id="id_list_table">
```
FT

```
$ python functional_tests.py
[...]
Traceback (most recent call last):
  File "functional_tests.py", line 40, in
test_can_start_a_list_and_retrieve_it_later
    table = self.browser.find_element_by_id('id_list_table')
[...]
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_list_table"]
```
functional_tests.py

```Python
# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list table
inputbox.send_keys(Keys.ENTER)
time.sleep(10)

table = self.browser.find_element_by_id('id_list_table')
```
lists/templates/home.html

```html
<form method="POST">
    <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
    {% raw %}{% csrf_token %}{% endraw %}
</form>
```

FT

```
AssertionError: False is not true : New to-do item did not appear in table
```

functional_tests.py

```Python
# "1: Buy peacock feathers" as an item in a to-do list table
inputbox.send_keys(Keys.ENTER)
time.sleep(1)

table = self.browser.find_element_by_id('id_list_table')
```


## 5.2. Processing a POST Request on the Server

lists/tests.py (ch05l005)

```Python
def test_uses_home_template(self):
    response = self.client.get('/')
    self.assertTemplateUsed(response, 'home.html')


def test_can_save_a_POST_request(self):
    response = self.client.post('/', data={'item_text': 'A new list item'})
    self.assertIn('A new list item', response.content.decode())
```

```
$ python manage.py test
[...]
AssertionError: 'A new list item' not found in '<html>\n    <head>\n
<title>To-Do lists</title>\n    </head>\n    <body>\n        <h1>Your To-Do
list</h1>\n        <form method="POST">\n            <input name="item_text"
[...]
</body>\n</html>\n'
```

lists/views.py

```python
from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    if request.method == 'POST':
        return HttpResponse(request.POST['item_text'])
    return render(request, 'home.html')
```

## 5.3. Passing Python Variables to Be Rendered in the Template

lists/templates/home.html

```html
<body>
    <h1>Your To-Do list</h1>
    <form method="POST">
        <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
        {% raw %}{% csrf_token %}{% endraw %}
    </form>

    <table id="id_list_table">
        <tr><td>{{ new_item_text }}</td></tr>
    </table>
</body>
```

lists/tests.py

```python
def test_can_save_a_POST_request(self):
    response = self.client.post('/', data={'item_text': 'A new list item'})
    self.assertIn('A new list item', response.content.decode())
    self.assertTemplateUsed(response, 'home.html')
```

```
AssertionError: No templates used to render the response
```

lists/views.py (ch05l009)

```python
def home_page(request):
    return render(request, 'home.html', {
        'new_item_text': request.POST['item_text'],
    })
```

```
ERROR: test_uses_home_template (lists.tests.HomePageTest)
[...]
  File "/.../superlists/lists/views.py", line 5, in home_page
    'new_item_text': request.POST['item_text'],
[...]
django.utils.datastructures.MultiValueDictKeyError: "'item_text'"
```

lists/views.py

```python
def home_page(request):
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })
```

FT

```
AssertionError: False is not true : New to-do item did not appear in table
```

functional_tests.py (ch05l011)

```python
self.assertTrue(
    any(row.text == '1: Buy peacock feathers' for row in rows),
    f"New to-do item did not appear in table. Contents were:\n{table.text}"  
)
```
> 'f-string'은 Python 3.6의 새로운 기능이다. f로 문자열을 추가하기만하면 중괄호 구문을 사용하여 로컬변수를 삽입 할 수 있다.  
> [3.6 release notes.](https://docs.python.org/3/whatsnew/3.6.html#pep-498-formatted-string-literals){:target="_blank"}

```
AssertionError: False is not true : New to-do item did not appear in table.
Contents were:
Buy peacock feathers
```

functional_tests.py (ch05l012)

```python
self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
```

```
self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
AssertionError: '1: Buy peacock feathers' not found in ['Buy peacock feathers']
```

lists/templates/home.html

```html
<tr><td>1: {{ new_item_text }}</td></tr>
```

functional_tests.py

```python
# There is still a text box inviting her to add another item. She
# enters "Use peacock feathers to make a fly" (Edith is very
# methodical)
inputbox = self.browser.find_element_by_id('id_new_item')
inputbox.send_keys('Use peacock feathers to make a fly')
inputbox.send_keys(Keys.ENTER)
time.sleep(1)

# The page updates again, and now shows both items on her list
table = self.browser.find_element_by_id('id_list_table')
rows = table.find_elements_by_tag_name('tr')
self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
self.assertIn(
    '2: Use peacock feathers to make a fly',
     [row.text for row in rows]
)

# Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some
# explanatory text to that effect.
self.fail('Finish the test!')

# She visits that URL - her to-do list is still there.
```

```
AssertionError: '1: Buy peacock feathers' not found in ['1: Use peacock
feathers to make a fly']
```

## 5.4. Three Strikes and Refactor

```
$ git diff
# should show changes to functional_tests.py, home.html,
# tests.py and views.py
$ git commit -a
```

functional_tests.py

```python
def tearDown(self):
    self.browser.quit()


def check_for_row_in_list_table(self, row_text):
    table = self.browser.find_element_by_id('id_list_table')
    rows = table.find_elements_by_tag_name('tr')
    self.assertIn(row_text, [row.text for row in rows])


def test_can_start_a_list_and_retrieve_it_later(self):
    [...]
```

functional_tests.py

```python
# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list table
inputbox.send_keys(Keys.ENTER)
time.sleep(1)
self.check_for_row_in_list_table('1: Buy peacock feathers')

# There is still a text box inviting her to add another item. She
# enters "Use peacock feathers to make a fly" (Edith is very
# methodical)
inputbox = self.browser.find_element_by_id('id_new_item')
inputbox.send_keys('Use peacock feathers to make a fly')
inputbox.send_keys(Keys.ENTER)
time.sleep(1)

# The page updates again, and now shows both items on her list
self.check_for_row_in_list_table('1: Buy peacock feathers')
self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

# Edith wonders whether the site will remember her list. Then she sees
[...]
```
FT

```
AssertionError: '1: Buy peacock feathers' not found in ['1: Use peacock
feathers to make a fly']
```

```
$ git diff # check the changes to functional_tests.py
$ git commit -a
```

## 5.5. The Django ORM and Our First Model

lists/tests.py

```python
from lists.models import Item
[...]

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')
```

UT

```
ImportError: cannot import name 'Item'
```

lists/models.py

```python
from django.db import models

class Item(object):
    pass
```

UT

```
first_item.save()
AttributeError: 'Item' object has no attribute 'save'
```

lists/models.py

```python
from django.db import models

class Item(models.Model):
    pass
```

## 5.6. Saving the POST to the Database

UT

```
django.db.utils.OperationalError: no such table: lists_item
```

```
$ python manage.py makemigrations
Migrations for 'lists':
  lists/migrations/0001_initial.py
    - Create model Item
$ ls lists/migrations
0001_initial.py  __init__.py  __pycache__
```

## 5.7. Redirect After a POST

```
$ python manage.py test lists
[...]
    self.assertEqual(first_saved_item.text, 'The first (ever) list item')
AttributeError: 'Item' object has no attribute 'text'
```

lists/models.py

```python
class Item(models.Model):
    text = models.TextField()
```

### A New Field Means a New Migration

```
django.db.utils.OperationalError: no such column: lists_item.text
```

```
$ python manage.py makemigrations
You are trying to add a non-nullable field 'text' to item without a default; we
can't do that (the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null
value for this column)
 2) Quit, and let me add a default in models.py
Select an option:2
```
메시지를 보면 알 수 있듯이 초깃값 없이 컬럼을 추가할 수 없다. 2번을 선택해서 models.py에 초기값을 설정한다.

lists/models.py

```python
class Item(models.Model):
    text = models.TextField(default='')
```

```
$ python manage.py makemigrations
Migrations for 'lists':
  lists/migrations/0002_item_text.py
    - Add field text to item
```

```
$ python manage.py test lists
[...]

Ran 3 tests in 0.010s
OK
```

```
$ git status # see tests.py, models.py, and 2 untracked migrations
$ git diff # review changes to tests.py and models.py
$ git add lists
$ git commit -m "Model for list Items and associated migration"
```

### Saving the POST to the Database

lists/tests.py

```python
def test_can_save_a_POST_request(self):
    response = self.client.post('/', data={'item_text': 'A new list item'})

    self.assertEqual(Item.objects.count(), 1)  
    new_item = Item.objects.first()  
    self.assertEqual(new_item.text, 'A new list item')  

    self.assertIn('A new list item', response.content.decode())
    self.assertTemplateUsed(response, 'home.html')
```

UT

```
self.assertEqual(Item.objects.count(), 1)
AssertionError: 0 != 1
```

lists/views.py

```python
from django.shortcuts import render
from lists.models import Item

def home_page(request):
    item = Item()
    item.text = request.POST.get('item_text', '')
    item.save()

    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', ''),
    })
```

lists/views.py

```python
return render(request, 'home.html', {
    'new_item_text': item.text
})
```

lists/tests.py

```python
class HomePageTest(TestCase):
    [...]

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
```

lists/views.py

```python
def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST['item_text']  
        Item.objects.create(text=new_item_text)  
    else:
        new_item_text = ''  

    return render(request, 'home.html', {
        'new_item_text': new_item_text,  
    })
```

UT

```
Ran 4 tests in 0.010s

OK
```

### Redirect After a POST

lists/tests.py

```python
def test_can_save_a_POST_request(self):
    response = self.client.post('/', data={'item_text': 'A new list item'})

    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'A new list item')

    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['location'], '/')
```

lists/views.py (ch05l028)

```python
from django.shortcuts import redirect, render
from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    return render(request, 'home.html')
```

UT

```
Ran 4 tests in 0.010s

OK
```

### Better Unit Testing Practice: Each Test Should Test One Thing

lists/tests.py

```python
def test_can_save_a_POST_request(self):
    self.client.post('/', data={'item_text': 'A new list item'})

    self.assertEqual(Item.objects.count(), 1)
    new_item = Item.objects.first()
    self.assertEqual(new_item.text, 'A new list item')


def test_redirects_after_POST(self):
    response = self.client.post('/', data={'item_text': 'A new list item'})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response['location'], '/')
```

UT

```
Ran 5 tests in 0.010s

OK
```

## 5.8. Rendering Items in the Template

lists/tests.py

```python
class HomePageTest(TestCase):
    [...]

    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())
```

UT

```
AssertionError: 'itemey 1' not found in '<html>\n    <head>\n [...]
```

lists/templates/home.html

```html
<table id="id_list_table">
    {% for item in items %}
        <tr><td>1: {{ item.text }}</td></tr>
    {% endfor %}
</table>
```

lists/views.py

```python
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
```

FT

```
$ python functional_tests.py
[...]
AssertionError: 'To-Do' not found in 'OperationalError at /'
```

## 5.9. Creating Our Production Database with migrate

superlists/settings.py

```python
[...]
# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

```
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, lists, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying lists.0001_initial... OK
  Applying lists.0002_item_text... OK
  Applying sessions.0001_initial... OK
```

FT

```
AssertionError: '2: Use peacock feathers to make a fly' not found in ['1: Buy
peacock feathers', '1: Use peacock feathers to make a fly']
```

lists/templates/home.html

```html
{% for item in items %}
    <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
{% endfor %}
```
FT

```
self.fail('Finish the test!')
AssertionError: Finish the test!
```

FT는 성공했지만 결과는 원하는 결과가 아니다.

이전 테스트에서 사용된 작업 아이템이 데이터베이스에 남아있기 때문이다. 테스트를 다시 실행하면 상황이 더 악화되는 것을 볼 수 있다.

```
1: Buy peacock feathers
2: Use peacock feathers to make a fly
3: Buy peacock feathers
4: Use peacock feathers to make a fly
5: Buy peacock feathers
6: Use peacock feathers to make a fly
```

이 문제를 해결하기 위해 무언가 자동화된 방법이 필요하다. 지금은 우선 `migrate` 명령을 이용해서 수작업으로 데이터베이스를 지운 후 재생성하도록 한다.

```
$ rm db.sqlite3
$ python manage.py migrate --noinput
```
FT가 성공하는지 재확인하도록 한다.

약간의 버그가 남아있긴 하지만, 어느 정도 코드가 동작하고 있으니 코드를 커밋한다.

```
$ git add lists
$ git commit -m "Redirect after POST, and show all items in template"
```

## 5.10. Recap
