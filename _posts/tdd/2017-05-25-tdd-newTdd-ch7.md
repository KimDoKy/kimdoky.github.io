---
layout: post
section-type: post
title: new TDD-Chapter 7. Working Incrementally
category: tdd
tags: [ 'tdd' ]
---

## 7.1. Small Design When Necessary

functional_tests/tests.py

```python
# Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some
# explanatory text to that effect.
self.fail('Finish the test!')

# She visits that URL - her to-do list is still there.

# Satisfied, she goes back to sleep
```
### Not Big Design Up Front
### YAGNI!
### REST (ish)

```
/lists/<list identifier>/
```

```
/lists/new
```

```
/lists/<list identifier>/add_item
```

## 7.2. Implementing the New Design Incrementally using TDD

## 7.3. Ensuring we have a regression test

functional_tests/tests.py (ch07l005)
(test_can_start_a_list_and_retrieve_it_later -> test_can_start_a_list_for_one_user)

```python
def test_can_start_a_list_for_one_user(self):
    # Edith has heard about a cool new online to-do app. She goes
    [...]
    # The page updates again, and now shows both items on her list
    self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
    self.wait_for_row_in_list_table('1: Buy peacock feathers')

    # Satisfied, she goes back to sleep


def test_multiple_users_can_start_lists_at_different_urls(self):
    # Edith start a new todo list
    self.browser.get(self.live_server_url)
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy peacock feathers')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: Buy peacock feathers')

    # She notices that her list has a unique URL
    edith_list_url = self.browser.current_url
    self.assertRegex(edith_list_url, '/lists/.+')  
```

functional_tests/tests.py (ch07l006)

```python
[...]
    self.assertRegex(edith_list_url, '/lists/.+')  

    # Now a new user, Francis, comes along to the site.

    ## We use a new browser session to make sure that no information
    ## of Edith's is coming through from cookies etc
    self.browser.quit()
    self.browser = webdriver.Firefox()

    # Francis visits the home page.  There is no sign of Edith's
    # list
    self.browser.get(self.live_server_url)
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy peacock feathers', page_text)
    self.assertNotIn('make a fly', page_text)

    # Francis starts a new list by entering a new item. He
    # is less interesting than Edith...
    inputbox = self.browser.find_element_by_id('id_new_item')
    inputbox.send_keys('Buy milk')
    inputbox.send_keys(Keys.ENTER)
    self.wait_for_row_in_list_table('1: Buy milk')

    # Francis gets his own unique URL
    francis_list_url = self.browser.current_url
    self.assertRegex(francis_list_url, '/lists/.+')
    self.assertNotEqual(francis_list_url, edith_list_url)

    # Again, there is no trace of Edith's list
    page_text = self.browser.find_element_by_tag_name('body').text
    self.assertNotIn('Buy peacock feathers', page_text)
    self.assertIn('Buy milk', page_text)

    # Satisfied, they both go back to sleep
```

```
$ python manage.py test functional_tests
[...]
.F
======================================================================
FAIL: test_multiple_users_can_start_lists_at_different_urls
(functional_tests.tests.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/functional_tests/tests.py", line 83, in
test_multiple_users_can_start_lists_at_different_urls
    self.assertRegex(edith_list_url, '/lists/.+')
AssertionError: Regex didn't match: '/lists/.+' not found in
'http://localhost:8081/'

 ---------------------------------------------------------------------
Ran 2 tests in 5.786s

FAILED (failures=1)
```

```
$ git commit -a
```

## 7.4. Iterating Towards the New Design

lists/tests.py (test_redirects_after_POST)

```python
self.assertEqual(response.status_code, 302)
self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
```

```
$ python manage.py test lists
[...]
AssertionError: '/' != '/lists/the-only-list-in-the-world/'
```

lists/views.py

```python
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
```
FT

```
File "/.../superlists/functional_tests/tests.py", line 57, in
test_can_start_a_list_for_one_user
[...]
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_list_table"]

[...]

File "/.../superlists/functional_tests/tests.py", line 79, in
test_multiple_users_can_start_lists_at_different_urls
  self.wait_for_row_in_list_table('1: Buy peacock feathers')
[...]
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_list_table"]
```
## 7.5. Taking a first, self-contained step: one new URL

lists/tests.py (ch07l009)

```python
class ListViewTest(TestCase):

    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')  
        self.assertContains(response, 'itemey 2')  
```

test list

```
self.assertContains(response, 'itemey 1')
[...]
AssertionError: 404 != 200 : Couldn't retrieve content: Response code was 404
```

### A New URL

superlists/urls.py

```python
urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/the-only-list-in-the-world/$', views.view_list, name='view_list'),
]
```

test list

```
AttributeError: module 'lists.views' has no attribute 'view_list'
```

### A New View Function

lists/views.py

```python
def view_list(request):
    pass
```

test list

```
ValueError: The view lists.views.view_list didn't return an HttpResponse
object. It returned None instead.

[...]
FAILED (errors=1)
```

lists/views.py

```python
def view_list(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
```
UT

```
Ran 7 tests in 0.016s
OK
```

FT

```
FAIL: test_can_start_a_list_for_one_user
[...]
  File "/.../superlists/functional_tests/tests.py", line 67, in
test_can_start_a_list_for_one_user
[...]
AssertionError: '2: Use peacock feathers to make a fly' not found in ['1: Buy
peacock feathers']

FAIL: test_multiple_users_can_start_lists_at_different_urls
[...]
AssertionError: 'Buy peacock feathers' unexpectedly found in 'Your To-Do
list\n1: Buy peacock feathers'
[...]
```

lists/templates/home.html

```html
        <form method="POST">
```

lists/templates/home.html

```html
        <form method="POST" action="/">
```
FT

```
FAIL: test_multiple_users_can_start_lists_at_different_urls
[...]
AssertionError: 'Buy peacock feathers' unexpectedly found in 'Your To-Do
list\n1: Buy peacock feathers'

Ran 2 tests in 8.541s
FAILED (failures=1)
```

## 7.6. Green? Refactor

```
$ grep -E "class|def" lists/tests.py
class HomePageTest(TestCase):
    def test_uses_home_template(self):
    def test_displays_all_list_items(self):
    def test_can_save_a_POST_request(self):
    def test_redirects_after_POST(self):
    def test_only_saves_items_when_necessary(self):
class ListViewTest(TestCase):
    def test_displays_all_items(self):
class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
```

> 'grep' : 파일 내부 문자열 검색  

`test_displays_all_list_items` 삭제  

test lists

```
Ran 6 tests in 0.016s
OK
```

## 7.7. Another Small Step: A Separate Template for Viewing Lists

lists/tests.py

```python
class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_all_items(self):
        [...]
```

```
AssertionError: False is not true : Template 'list.html' was not a template
used to render the response. Actual template(s) used: home.html
```

lists/views.py

```python
def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
```

```
django.template.exceptions.TemplateDoesNotExist: list.html
```

```
$ touch lists/templates/list.html
```

```
AssertionError: False is not true : Couldn't find 'itemey 1' in response
```

```
$ cp lists/templates/home.html lists/templates/list.html
```

lists/templates/home.html

```python
<body>
  <h1>Start a new To-Do list</h1>
  <form method="POST">
    <input name="item_text" id="id_new_item" placeholder="Enter a to-do item" />
    {% raw %}{% csrf_token %}{% endraw %}
  </form>
</body>
```

lists/views.py

```python
def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request, 'home.html')
```
UT, FT

```
AssertionError: '1: Buy milk' not found in ['1: Buy peacock feathers', '2: Buy
milk']
```

```
$ git status # should show 4 changed files and 1 new file, list.html
$ git add lists/templates/list.html
$ git diff # should show we've simplified home.html,
           # moved one test to a new class in lists/tests.py added a new view
           # in views.py, and simplified home_page and made one addition to
           # urls.py
$ git commit -a # add a message summarising the above, maybe something like
                # "new URL, view and template to display lists"
```

## 7.8. A Third Small Step: a URL for Adding List Items

### A Test Class for New List Creation

`test_can_save_a_POST_request`와 `test_redirects_after_POST`를 새 클래스로 이동하고 post URL을 변경하세요.

lists/tests.py (ch07l021-1)

```python
class NewListTest(TestCase):

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')


    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
```

lists/tests.py (ch07l021-2)

```python
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
```
UT

```
self.assertEqual(Item.objects.count(), 1)
AssertionError: 0 != 1
[...]
self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
[...]
AssertionError: 404 != 302 : Response didn't redirect as expected: Response
code was 404 (expected 302)
```
첫 번째 오류는 데이터베이스에 아이템을 저장할 수 없다는 메시지이고, 두 번째는 뷰가 302 상태 코드 대신에 404 코드를 반호나하고 있다는 메시지입니다. lists/new가 아직 구축되지 않아서 client.post가 404 응답을 받기 때문입니다.

### A URL and View for New List Creation

superlists/urls.py

```python
urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/new$', views.new_list, name='new_list'),
    url(r'^lists/the-only-list-in-the-world/$', views.view_list, name='view_list'),
]
```

lists/views.py (ch07l023-1)

```python
def new_list(request):
    pass
```

lists/views.py (ch07l023-2)

```python
def new_list(request):
    return redirect('/lists/the-only-list-in-the-world/')
```

UT

```
self.assertEqual(Item.objects.count(), 1)
AssertionError: 0 != 1
```
비교적 쉽게 고칠 수 있는 첫 번째 에러부터 해결합니다. `home_page`에서 다시 코드를 빌려옵니다.

lists/views.py (ch07l023-3)

```python
def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')
```

```
Ran 7 tests in 0.030s

OK
```

FT

```
[...]
AssertionError: '1: Buy milk' not found in ['1: Buy peacock feathers', '2: Buy
milk']
Ran 2 tests in 8.972s
FAILED (failures=1)
```

### Removing Now-Redundant Code and Tests

lists/views.py

```python
def home_page(request):
    return render(request, 'home.html')
```

UT

```
OK
```
문제가 없습니다. `test_only_saves_items_when_necessary` 테스트도 삭제해줍니다.

확인을 위해 테스트를 재실행합니다.

UT

```
Ran 6 tests in 0.016s
OK
```
FT는 어떨까요?

### A regression! Pointing Our Forms at the New URL

뜨든...

```
ERROR: test_can_start_a_list_for_one_user
[...]
  File "/.../superlists/functional_tests/tests.py", line 57, in
test_can_start_a_list_for_one_user
    self.wait_for_row_in_list_table('1: Buy peacock feathers')
  File "/.../superlists/functional_tests/tests.py", line 23, in
wait_for_row_in_list_table
    table = self.browser.find_element_by_id('id_list_table')
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_list_table"]

ERROR: test_multiple_users_can_start_lists_at_different_urls
[...]
  File "/.../superlists/functional_tests/tests.py", line 79, in
test_multiple_users_can_start_lists_at_different_urls
    self.wait_for_row_in_list_table('1: Buy peacock feathers')
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_list_table"]
[...]

Ran 2 tests in 11.592s
FAILED (errors=2)
```
URL이 아직 이전 URL을 가리키고 있기 때문입니다. home.html와 list.html을 다음과 같이 변경하세요.

lists/templates/home.html, lists/templates/list.html

```html
<form method="POST" action="/lists/new">
```

FT

```
AssertionError: '1: Buy milk' not found in ['1: Buy peacock feathers', '2: Buy
milk']
[...]
FAILED (failures=1)
```
이전(리팩터링 이전)과 같은 상태입니다. 이로써 URL 관련 수정을 성공적으로 마쳤고, views.py도 훨씬 깔끔해졌습니다. 또한 애플리케이션이 이전과 동일한 상태로 동작하고 있는 것도 확인했습니다. 리팩터링 작업을 무사히 마쳤습니다

```
$ git status # 5 changed files
$ git diff # URLs for forms x2, moved code in views + tests, new URL
$ git commit -a
```

## 7.9. Biting the bullet: Adjusting Our Models

URL 관련 정비는 마쳤습니다. 이제 모델을 변경해야합니다. 먼저 모델 단위 테스트를 조정합니다.  
수정 작업을 위해 변경할 곳을 diff 형식으로 표시하였습니다.

lists/tests.py

```python
@@ -1,5 +1,5 @@
 from django.test import TestCase
-from lists.models import Item
+from lists.models import Item, List


 class HomePageTest(TestCase):
@@ -44,22 +44,32 @@ class ListViewTest(TestCase):



-class ItemModelTest(TestCase):
+class ListAndItemModelsTest(TestCase):

     def test_saving_and_retrieving_items(self):
+        list_ = List()
+        list_.save()
+
         first_item = Item()
         first_item.text = 'The first (ever) list item'
+        first_item.list = list_
         first_item.save()

         second_item = Item()
         second_item.text = 'Item the second'
+        second_item.list = list_
         second_item.save()

+        saved_list = List.objects.first()
+        self.assertEqual(saved_list, list_)
+
         saved_items = Item.objects.all()
         self.assertEqual(saved_items.count(), 2)

         first_saved_item = saved_items[0]
         second_saved_item = saved_items[1]
         self.assertEqual(first_saved_item.text, 'The first (ever) list item')
+        self.assertEqual(first_saved_item.list, list_)
         self.assertEqual(second_saved_item.text, 'Item the second')
+        self.assertEqual(second_saved_item.list, list_)
```
새로운 List(목록) 객체를 생성하고, 각 아이템에 .list 속성을 부여해서 List 객체에 할당하고 있습니다. 목록이 제대로 저장됐는지와 두 개 작업 아이템이 목록에 제대로 할당됐는지 확인하도록 합니다. 코드를 보면 알다시피 목록 개체를 서로 비교하는 것이 가능합니다.(saved_list와  list 비교) 이 비교 처리는, 주 키(.id 속성)가 같은지 확인합니다.

UT  
첫 번째 에러  

```
ImportError: cannot import name 'List'
```

기본적인거니까 알아서 해결해 본다.

두 번째 에러

```
AttributeError: 'List' object has no attribute 'save'
```
세 번째 에러

```
django.db.utils.OperationalError: no such table: lists_list
```

makemigrations 한다.

```
$ python manage.py makemigrations
Migrations for 'lists':
  lists/migrations/0003_list.py
    - Create model List
```
네 번째 에러

```
self.assertEqual(first_saved_item.list, list_)
AttributeError: 'Item' object has no attribute 'list'
```

### A Foreign Key Relationship

lists/models.py

```python
from django.db import models

class List(models.Model):
    pass

class Item(models.Model):
    text = models.TextField(default='')
    list = models.TextField(default='')
```

```
$ python manage.py test lists
[...]
django.db.utils.OperationalError: no such column: lists_item.list

$ python manage.py makemigrations
Migrations for 'lists':
  lists/migrations/0004_item_list.py
    - Add field list to item
```

```
AssertionError: 'List object' != <List: List object>
```

lists/models.py

```python
from django.db import models

class List(models.Model):
    pass


class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)
```

```
$ rm lists/migrations/0004_item_list.py
$ python manage.py makemigrations
Migrations for 'lists':
  lists/migrations/0004_item_list.py
    - Add field list to item
```
> 마이그레이션을 삭제하는 것은 매우 위험합니다. 데이터베이스에 이미 적용된 마이그레이션을 삭제하면, Django가 상태를 차악하지 못하고 이후 마이그레이션을 어떻게 적용해야 할지 혼란스러워하게 됩니다. 마이그레이션이 더 이상 필요하지 않다는 확싱이 있을 때만 삭제합니다. 일반적으론 버전 관리 시스템에 커밋한 마이그레이션은 절대 삭제하지 않습니다.

### Adjusting the Rest of the World to Our New Models
테스트로 돌아와서 어떤 상태인지 확인합니다.

```
$ python manage.py test lists
[...]
ERROR: test_displays_all_items (lists.tests.ListViewTest)
django.db.utils.IntegrityError: NOT NULL constraint failed: lists_item.list_id
[...]
ERROR: test_redirects_after_POST (lists.tests.NewListTest)
django.db.utils.IntegrityError: NOT NULL constraint failed: lists_item.list_id
[...]
ERROR: test_can_save_a_POST_request (lists.tests.NewListTest)
django.db.utils.IntegrityError: NOT NULL constraint failed: lists_item.list_id

Ran 6 tests in 0.021s

FAILED (errors=3)
```
확인하기 어렵지만 모델 테스트가 성공했습니다. 세 개의 뷰 테스트가 실패하고 있지만...

각 작업 아이템이 부모 목록을 가지고 있어야 한다는 Items과 Lists 관계 때문입니다. 기존 테스트가 아직 이 관계를 인식할 준비가 돼있지 않습니다.

이것이 우리가 테스트를 해야 하는 이유입니다. 문제를 해결해봅시다. 가장 쉬운 방법은 ListViewTest를 수정해서 두 개 테스트 아이템을 위한 부모 목록을 만드는 것입니다.

lists/tests.py (ch07l031)

```python
class ListViewTest(TestCase):

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='itemey 1', list=list_)
        Item.objects.create(text='itemey 2', list=list_)
```

이제 new_list 뷰로 POST할 때 실패하는 두 개 오류가 남는다. 테스트 코드를 확인하 후 애플리케이션 코드를 확인하자.

```
File "/.../superlists/lists/views.py", line 9, in new_list
Item.objects.create(text=request.POST['item_text'])
```
부모 목록 없이 작업 아이템을 생성하려 하기 때문에 발생하는 에러입니다. 뷰에도 비슷한 작업을 합니다.

lists/views.py

```python
from lists.models import Item, List
[...]
def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
```
이것으로 테스트가 모두 성공합니다.

```
Ran 6 tests in 0.030s

OK
```
이 시점에서 무언가 석연찮은 감정이 느껴지게 됩니다. '아이템을 만들 때마다 목록도 새로 생성되고 있어. 전체를 한번에 하는게 더 좋은거 아닌가?'. 하지만 테스팅 고트님을 기억해야합니다. 산 위에 있을 때처러 한발 한발 내디뎌야 합니다. (마음 가는대로 한다면... 리택터링 캣을 만나게 될 것입니다...하)  

FT

```
AssertionError: '1: Buy milk' not found in ['1: Buy peacock feathers', '2: Buy
milk']
[...]
```

따라서 현재는 FT를 실행해서 문제 없이 동작하다는 것만으로 충분합니다. 이전 처리를 망치지 않았고 데이터베이스도 무사합니다. 커밋 ㄱㄱ.

```
$ git status # 3 changed files, plus 2 migrations
$ git add lists
$ git diff --staged
$ git commit
```
## 7.10. Each List Should Have Its Own URL

목록을 위한 고유 식별자로 어떤 것을 사용해야 할까요? 이 시점에서 가장 간단한 것은 데이터베이스가 자동으로 생성하는 id 필드입니다. `ListViewTest`를 수정해서 두 테스트가 새로운 URL을 가리키도록 합니다.

오래된 `test_displays_all_items` 테스트를 `test_displays_only_items_for_that_list`로 변경해서 특정 리스트에서만 툴력되는 아이템을 체크하도록 만듭니다.

lists/tests.py (ch07l033)

```python
class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)
        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list item 2')
```

UT

```
FAIL: test_displays_only_items_for_that_list (lists.tests.ListViewTest)
AssertionError: 404 != 200 : Couldn't retrieve content: Response code was 404
(expected 200)
[...]
FAIL: test_uses_list_template (lists.tests.ListViewTest)
AssertionError: No templates used to render the response
```

### Capturing Parameters from URLs
URL을 통해 어떻게 파라미터를 전달하는지 봅니다.

superlists/urls.py

```python
urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/new$', views.new_list, name='new_list'),
    url(r'^lists/(.+)/$', views.view_list, name='view_list'),
]
```
URL용 정규표현을 수정해서 캡쳐 그룹(capture group)(.+)을 추가합니다. 캡쳐 그룹은 `/` 뒤에 나오는 모든 문자에 일치합니다. 취득한 텍스트는 인수 형태로 뷰에 전달합니다.

즉 URL이 `/lists/1/`이면 일반 요청 인수 다음에 두 번째 인수. 즉 '1'이 `view_list`에 전달됩니다. `/lists/foo/`인 경우 `view)list(request, "foo")`가 됩니다.

아직 뷰가 인수를 받을 수 없기 때문에 테스트(UT)가 실패합니다.

```
ERROR: test_displays_only_items_for_that_list (lists.tests.ListViewTest)
[...]
TypeError: view_list() takes 1 positional argument but 2 were given
[...]
ERROR: test_uses_list_template (lists.tests.ListViewTest)
[...]
TypeError: view_list() takes 1 positional argument but 2 were given
[...]
ERROR: test_redirects_after_POST (lists.tests.NewListTest)
[...]
TypeError: view_list() takes 1 positional argument but 2 were given
FAILED (errors=3)
```
views.py에 더미(dummy) 파라미터를 적용해서 쉽게 해결할 수 있습니다.

lists/views.py

```python
def view_list(request, list_id):
    [...]
```

```
FAIL: test_displays_only_items_for_that_list (lists.tests.ListViewTest)
[...]
AssertionError: 1 != 0 : Response should not contain 'other list item 1'
```
뷰가 어떤 아이템을 템플릿을 보낼지 구분하는 처리를 추가합니다.

lists/views.py

```python
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items})
```
### Adjusting new_list to the New World
이제 다른 에러가 발생합니다.

```
ERROR: test_redirects_after_POST (lists.tests.NewListTest)
ValueError: invalid literal for int() with base 10:
'the-only-list-in-the-world'
```
에러가 발생한 코드를 살펴봅니다.

lists/tests.py

```python
class NewListTest(TestCase):
    [...]

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
```

새로운 세상에 있는 Lists와 Items를 맞이할 준비가 돼있지 않습니다. 이 뷰는 막 생성된 특정 새 목록의 URL로 리다이렉트 되는 테스트가 있어야한다.

lists/tests.py (ch07l036-1)

```python
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')
```
뷰가 올바른 위치로 리디렉션하도록 수정합니다.

lists/views.py (ch07l036-2)

```python
def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
```

이제 UT가 통과하게 됩니다.

```
$ python3 manage.py test lists
[...]
......
 ---------------------------------------------------------------------
Ran 6 tests in 0.033s

OK
```
## 7.11. The functional tests detect another regression

```
F.
======================================================================
FAIL: test_can_start_a_list_for_one_user
(functional_tests.tests.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/functional_tests/tests.py", line 67, in
test_can_start_a_list_for_one_user
    self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
[...]
AssertionError: '2: Use peacock feathers to make a fly' not found in ['1: Use
peacock feathers to make a fly']

 ---------------------------------------------------------------------
Ran 2 tests in 8.617s

FAILED (failures=1)
```
FT가 애플리케이션 퇴행이 발생했다고 경고합니다. 모든 POST 전달 시마다 새로운 목록을 만들기 때문에, 여러 아이템을 하나의 목록에 추가하는 기능이 동작하지 않습니다. 이것이 FT가 유용한 이유입니다.

## 7.12. One More View to Handle Adding Items to an Existing List

기존 목록에 신규 아이템을 추가하기 위한 URL과 뷰가 필요합니다.(`/lists/<list_id>/add_item`).

lists/tests.py

```python
class NewItemTest(TestCase):

    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)


    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )

        self.assertRedirects(response, f'/lists/{correct_list.id}/')
```
>
`other_list`에 궁금 하신가요? 특정 목록을 보는 테스트와 마찬가지로 특정 목록에 항목을 추가하는 것이 중요합니다. 이 두 번째 객체를 데이터베이스에 추가하면 구현시 List.objects.first()와 같은 해킹을 사용하지 못하게됩니다. 그것은 어리석은 일이며, 당신이하지 말아야 할 모든 어리석은 것들에 대해 테스트의 길로 너무 멀리 갈 수 있습니다 (결국 그 수는 무한합니다). 그것은 심판의 부름이지만,이 사람은 그럴 가치가 있다고 느낍니다. 더 많은 내용은  [testing-for-stupidity](https://www.obeythetestinggoat.com/book/chapter_advanced_forms.html#testing-for-stupidity)을 살펴봅니다. (해석기의 한계네요..)

```
AssertionError: 0 != 1
[...]
AssertionError: 301 != 302 : Response didn't redirect as expected: Response
code was 301 (expected 302)
```
### Beware of Greedy Regular Expressions!
아직 `lists/1/add_item` URL을 지정하지 않았으니 예상한 에러는 404 != 302 일 것입니다. 하지만 301이 ?

그 이유는 URL에 포함된 정규식 때문입니다.

superlists/urls.py

``` python
    url(r'^lists/(.+)/$', views.view_list, name='view_list'),
```
Django는 영구적 리디렉션(301)에 대한 내부적인 이슈가 있어서 슬래시가 누락되는 경우 문제가 발생합니다. 이 경우는 `/lists/1/add_item/`이 `lists/(.+)/`에 의해 매칭됩니다. `(.+)`가 `1/add_item`을 캡쳐하기 때문입니다. 결국 DJango는 마지막 꼬리 슬래시를 원한다는 것을 알 수 있습니다.

이것은 URL에서 숫자만 추출하도록 수정하면 됩니다. 이때 쓰는 정규표현은 `\d`입니다.

superlists/urls.py

```python
    url(r'^lists/(\d+)/$', views.view_list, name='view_list'),
```

```
    AssertionError: 0 != 1
    [...]
    AssertionError: 404 != 302 : Response didn't redirect as expected: Response
    code was 404 (expected 302)
```

### The Last New URL
이제 예측한 대로 404 상태입니다. 기존 목록에 신규 아이템을 추가하는 URL을 만듭니다.

superlists/urls.py

```python
urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^lists/new$', views.new_list, name='new_list'),
    url(r'^lists/(\d+)/$', views.view_list, name='view_list'),
    url(r'^lists/(\d+)/add_item$', views.add_item, name='add_item'),
]
```

매우 비슷한 세 개의 URL이 만들어졌습니다. 리팩터링이 필요하다는 의미입니다. 작업 메모장에 추가해 둡니다.

UT로 돌아가면 모듈 뷰 객체가 누락되었습니다.

```
AttributeError: module 'lists.views' has no attribute 'add_item'
```

### The Last New View
해결해 봅시다!

lists/views.py

```python
def add_item(request):
    pass
```

다음과 같은 에러가 발생합니다.

```
TypeError: add_item() takes 1 positional argument but 2 were given
```

lists/views.py

```python
def add_item(request, list_id):
    pass
```
그러면 이런 오류가 일어납니다.

```
ValueError: The view lists.views.add_item didn't return an HttpResponse object.
It returned None instead.
```
`view_list`에서 `List.objects`를 복사하고, `new_list`에서 `redirect`를 복사할 수 있습니다.

lists/views.py

```python
def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    return redirect(f'/lists/{list_.id}/')
```
결과는 다음과 같습니다.

```
self.assertEqual(Item.objects.count(), 1)
AssertionError: 0 != 1
```
마지막으로 신규 작업 아이템을 저장할 수 있도록 합니다,

lists/views.py

```python
def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
```

모든 테스트가 통과하는 것을 확인할 수 있습니다.

```
Ran 8 tests in 0.050s

OK
```

### Testing the response context objects directly
기존 목록에 신규 작업 아이템을 추가하기 위한 새로운 뷰와 URL이 있습니다. 이제 list.html 템플릿에서 사용하면 됩니다. 폼 태그를 이용해 수정합니다.

lists/templates/list.html

```html
    <form method="POST" action="but what should we put here?">
```

현재 작업 목록에 아이템을 추가하는 URL을 얻으려면, 템플릿이 어떤 목록과 아이템을 표시하고 있는지 알아야 합니다.

lists/templates/list.html

```html
    <form method="POST" action="/lists/{{ list.id }}/add_item">
```

이것이 동작하려면, 뷰가 목록을 템플릿에게 전달하도록 만들어야 합니다. `ListViewTest`에 새로운 단위 테스트를 생성합니다.

lists/tests.py (ch07l041)

```python
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)
```
response.context는 렌더링 함수에 전달할 context를 나타냅니다. Django 테스트 클라이언트는 이것을 response 객체에 넣어서 테스트할 수 있도록 돕습니다.
테스트 결과는 다음과 같습니다.

```
KeyError: 'list'
```

list를 템플릿에 전달하고 있지 않기 때문입니다. 실제로 이 처리를 더 간소화 할 기회를 줍니다.

lists/views.py

```python
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})
```
템플릿이 아이템을 기대하고 있기 때문에 이 코드는 당연히 에러를 발생시킵니다.

```
FAIL: test_displays_only_items_for_that_list (lists.tests.ListViewTest)
[...]
AssertionError: False is not true : Couldn't find 'itemey 1' in response
```
list.html에 있는 폼의 POST 처리를 수정하면 해결됩니다.

lists/templates/list.html (ch07l043)

```html
    <form method="POST" action="/lists/{{ list.id }}/add_item">  

      [...]

      {% for item in list.item_set.all %}  
        <tr><td>{{ forloop.counter }}: {{ item.text }}</td></tr>
      {% endfor %}
```
`.item_set`은 "reverse lookup"이라 불리는 것입니다. DJango가 제공하는 유용한 ORM으로, 다른 테이블에 있는 아이템과 관련된 객체를 찾아줍니다.

결과적으로 UT가 성공합니다.

```
Ran 9 tests in 0.040s

OK
```

FT는 어떨까요?

```
$ python manage.py test functional_tests
[...]
..
 ---------------------------------------------------------------------
Ran 2 tests in 9.771s

OK
```

성공입니다. 작업 메모장을 다시 확인해봅니다.

테스팅 고트님은 어중간하게 코드를 마무리하는 것을 싫어합니다. 코드를 정리하는 것이 마지막 임무입니다.

이 작업을 시작하기 전에 커밋 ㄱㄱ.  
리팩터링하기 전에는 항상 작업 상태를 커밋해두도록 합니다.

```
$ git diff
$ git commit -am "new URL + view for adding to existing lists. FT passes :-)"
```

# 7.13. A Final Refactor Using URL includes
superlists/urls.py는 전체 사이트에 적용할 URL을 설정합니다. lists 앱에만 적용할 URL이라면 lists/url.py가 적합합니다. URL을 설정하는 가장 간단한 방법은 기본 urls.py를 복사하는 것입니다.

```
$ cp superlists/urls.py lists/
```
superlists/urls.py에 있는 코드 세 줄을 include로 교체합니다. include가 URL 정규표현을 접두사로 사용할 수 있으며, 지정한 URL에 모두 적용된다는 것에 유의합니다.(이를 통해 코드 중복을 줄일 수 있습니다.)

superlists/urls.py

```python
from django.conf.urls import include, url
from lists import views as list_views  
from lists import urls as list_urls  

urlpatterns = [
    url(r'^$', list_views.home_page, name='home'),
    url(r'^lists/', include(list_urls)),  
]
```
lists/urls.py를 수정해서 세 개 URL의 뒷부분만 포함할 수 있고, 상위 urls.py에서 온 다른 내용들을 제거할 수 있습니다.

lists/urls.py (ch07l046)

```python
from django.conf.urls import url
from lists import views

urlpatterns = [
    url(r'^new$', views.new_list, name='new_list'),
    url(r'^(\d+)/$', views.view_list, name='view_list'),
    url(r'^(\d+)/add_item$', views.add_item, name='add_item'),
]
```
UT를 다시 실행하면 모든 게 정상 동작하는 것을 확인할 수 있습니다.

```
$ git status
$ git add lists/urls.py
$ git add superlists/urls.py
$ git diff --staged
$ git commit
```

테스트 격리를 비롯한 설계 방식 등 여러가지 주제를 다룬 챕터였습니다. 가장 중요한 것은 기존 사이트에 새로운 설계 내용을 반영하기 위해, 사이트를 한 단계씩 수정해서 동작 상태를 확인 후에 다음 단계로 넘어가는 과정입니다.

## 알아두면 유용한 TDD 개념과 일반적인 법칙
### 테스트 격리(test Isolation)와 전역 상태(Global State)
각각의 테스트가 다른 테스트에 영향을 끼쳐서는 안 됩니다. 이것은 각 테스트 마지막에는 영구적인 상태를 초기화해야 한다는 것을 의미합니다. Django의 테스트 실행자는 각 테스트 결과물을 제거해주는 테스트 데이터베이스를 생성함으로써 이 문제를 해결해준다.

### 동작 상태 확인 후 다음 동작 상태 확인(테스팅 고트님 VS 피팩터링 캣)
일반적으론 모든 것을 한 번에 수정하는 것이 쉽습니다. 하지만 주의하지 않으면 결국 리책터링 캣 처지가 돼서 오히려 많은 코드를 재수정해야 하거나 아무것도 동작하지 않는 상태가 됩니다. 테스팅 고트님은 우리가 한 단계씩 수정해서 동작하는지 확인 후에 다음 단계로 넘어가도록 격려하고 있습니다.

### YAGNI
'You ain't gonna need it!'(그것을 사용할 일이 없을 것이다)  
나중에 도움이 될 것이라는 생각에 코드를 작성하려는 유혹을 이겨내야합니다. 그것을 사용하지 않을 수도 있고, 무엇보다 이후에 발생한 요구사항 변경을 예측할 수 없기 때문입니다.
