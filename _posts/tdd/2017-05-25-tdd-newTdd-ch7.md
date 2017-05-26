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
## 7.10. Each List Should Have Its Own URL
## 7.11. The functional tests detect another regression
## 7.12. One More View to Handle Adding Items to an Existing List
## 7.13. A Final Refactor Using URL includes
