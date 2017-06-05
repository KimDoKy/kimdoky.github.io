---
layout: post
section-type: post
title: new TDD-Chapter 4. What Are We Doing with All These Tests? (And, Refactoring)
category: tdd
tags: [ 'tdd' ]
---
- 너무 테스트를 과하게 하는건 아닌가?
- 어떤 것들은 중복 작업인 것이 분명하다. 기능 테스트와 단위 테스트에서 겹치는 부분이 있다.
- 왜 `django.core.urlresolver`를 단위 테스트에 사용하는거지? 이건 Django라는 외부 코드를 테스트하는 거 아닌가? 외부 코드 테스트는 의미가 없다고 생각한다.
- 선언 코드 한 줄이나 상수 하나를 반환하는 함수로 단위 테스트를 하는 것은 너무 시시하다. 이건 시간 낭비다. 더 복잡한 처리를 위한 테스트를 만들어야 하는거 아닌가?
- 단위 테스트-코드 주기 동안 해야 하는 최소 코드 변경은 정말 필요한거야? 그냥 한 번에 다 변경해서 마지막에만 테스트하면 안되는건가? `home_page = None`은 말도 안돼.
- 정말 실제 업무에서도 이렇게 코드를 작성하는 건 아니지?

이런 질문들은 의미가 있습니다. '이게 정말 가치 있는 것일까?'

## 4.1. Programming Is like Pulling a Bucket of Water up from a Well
프로그래밍은 정말 어려운 작업입니다. 종종 똑똑한 사람들이 성공하는 경우가 있습니다. TDD는 똑똑하지 못한 우리들을 도와주기 위해 존재합니다. 켄트 벡(Kent Beck,TDD를 고안한 사람)은 우물가에 있는 물 뜨는 두레박을 비유로 들어 설명합니다. 우물이 깊지 않으면 두레박도 꽉 차지 않아서 퍼 올리는 것이 쉽습니다. 가득 차 있다고 해도 처음 몇 번은 쉽게 할 수 있습니다. 하지만 시간이 지나면서 곧 지치기 시작합니다. 하지만 이때 도르래를 이용하면 직접 퍼 올리는 것보다 효율적입니다. TDD는 이런 도르래와 같아서 우리의 작업 효율을 올려주소 쉴 수 있는 시간도 줍니다. 또한 뒤로 미끄러 지는 것도 막아줍니다.

![]({{ site.url }}/img/post/tdd/4_1.png)

'이 정도까지 할 필요가 있을까?' TDD는 "훈련"입니다. 즉 자연스럽게 익힐 수 있는 것이 아닙니다. 대부분의 성과가 즉시 보여지는 것이 아니라 오랜 기간을 거쳐야 보이기 때문에, TDD에 적응할 수 있도록 노력해야 합니다. 이것이 테스팅 코드님 그림을 통해 보여주고자 한 것입니다.

>
## 시시한 함수에 대한 시시한 테스트의 이점
>
단기적 관점에선 간단한 함수나 상수를 위한 테스트 작성이 하찮게 여겨질 수도 있습니다. 물론 보다 수월한 규칙(일부만 단위 테스트를 하는)을 따라서 TDD를 "적당하게"할 수도 있습니다. 하지만 여기서는 완벽하면서도 철처한 TDD입니다. 이것은 무술의 카타(Kata)와 같습니다.(즉 정확한 동작을 배워서 기술 자체가 외 근육이 되도록 하는 것입니다.) 문제는 애플리케이션이 복잡해지면서 발생하게 되는데, 이때는 정말 테스트가 필요해집니다. 하지만 복잡성이라는 것은 우리가 모르는 사이에 조금씩 다가와서 복잡하다는 것 자체를 인지하지 못하고, 얼마 되지 않아 끓는 물 속에 개구리 꼴이 되는 것입니다.  
>
간단한 함수를 위한 간단한 테스트에 대해 언습하고 싶은 것이 두 가지 더 있습니다.  
>
첫 번째는, 테스트가 정말 시시한 테스트라면 테스트 작성 자체에 시간이 많이 걸리지 않는다는 것입니다. 그러니 불평말고 작성하도록 합니다.  
>
두 번째는, 틀을 사용하는 것이 도움이 된다는 것입니다. 쉬운 함수를 위한 테스트 틀이 있다면, 함수가 복잡해지더라도 심리적으로 부담을 줄일 수 있습니다.(단기간에 if 제어나 for 루프 처리가 늘어날 수 있습니다.) 우리가 인지하기 전에 프로그램이 다형성 트리 파서(parser) 구조가 되더니 어느새 재귀 처리로까지 번질 수 있습니다. 하지만 초반부터 틀을 갖추어 테스트를 했기 때문에 새로운 테스트를 추가하는 것이 자연스럽고 테스트도 수월합니다. 테스트를 해야 할 정도로 복잡하다고 판단한 후 테스트를 작성하기 시작한다면(복잡하다는 기준도 모호하지만), 틀이 없기 때문에 훨씬 많은 수고를 들여서 테스트를 만들고 수정해야 합니다. 즉 개구리 수프가 되고 마는 것입니다.  
>
언제 테스트를 작성하기 시작해야 하는지 결정하려고 주관적인 규칙에 얽매이는 대신에, 지금 바로 훈련하기 바랍니다. 다른 훈련들과 마찬가지로 익숙해지기 전까지 시간을 가지고 규칙에 익숙해져야 합니다.

## 4.2. Using Selenium to Test User Interactions
테스트를 다시 실행해서 어디까지 진행했는지 확인합니다.

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
> TDD가 훌륭한 이유 중 하나가 다음에 무엇을 해야 할지 잊어버릴 걱정이 없다는 것입니다. 테스트를 다시 실행하기만 하면 다음 작업이 무엇인지 가르쳐줍니다.

"Finish the test"라고 했으니 이 명령을 따르도록 합니다. 다음 작업을 진행합니다.

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
        header_text = self.browser.find_element_by_tag_name('h1').text  #1
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')  #1
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby
        # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')  #2

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)  #3
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')  #1
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
>
#1 : 셀레늄이 제공하는 다양한 메소드를 사용하고 있습니다. `find_element_by_tag_name`, `find_element_by_id`, `find_elements_by_tag_name` 등 입니다. (`element`에 `s`가 붙어 있어서 복수의 요소를 반환합니다.)  
#2 : 셀레늄의 입력 요소를 타이핑하는 방법인 `send_keys`을 사용합니다.
#3 : `Keys` 클래스는 'Enter'나 'Ctrl' 같은 특수 키 입력을 전송하는 역할을 합니다.

> `find_element_...`와 `find_elements_...` 함수의 차이점에 유의해야합니다. 전자는 하나의 요소만 반환하며 요소가 없는 경우 예외를 발생시킵니다. 반면 후자는 리스트를 반환하며 이 리스트가 비어 있어도 괜찮습니다.

이 함수들의 내부를 보면 파이썬으로 만들어진 것을 알 수 있습니다. 이 함수들은 "generator expression"으로 "list comprehension"과 비슷하지만 더 진보된 기술입니다. 더 많은 자료는 [Guido](http://python-history.blogspot.kr/2010/06/from-list-comprehensions-to-generator.html){:target="_blank"}가 설명한 자료를 볼 수 있습니다.

FT를 실행해 봅니다.

```
$ python functional_tests.py
[...]
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: h1
```
"<h1>" 요소를 찾지 못했다는 메시지입니다. 그러면 어떻게 이 문제를 해결할 수 있을까요?  

FT를 많이 수정했다면 커밋을 하는 것이 좋은 습관입니다. 커밋 시에는 가능한 작은 단위로 하는 것이 좋습니다.

```
$ git diff  # should show changes to functional_tests.py
$ git commit -am "Functional test now checks we can input a to-do item"
```

## 4.3. The “Don’t Test Constants” Rule, and Templates to the Rescue

`lists/tests.py`에 있는 단위 테스트를 다시 봅니다. 현재는 특정 HTML 문자열을 확인하고있지만, HTML을 테스트하기 위한 효율적인 방법이 아닙니다. 단위 테스트 시의 일반적인 규칙 중 하나는 "상수는 테스트하지 마라"입니다. HTML을 문자열로 테스트하는 것은 상수 테스트와 같다고 할 수 있습니다.  

단위 테스트는 로직이나 흐름 제어, 설정 등을 테스트하기 위한 것입니다. 정확히 어떤 글자들이 HTML 문자열에 배열돼 있는지 체크하는 어설션은 아무 의미가 없습니다. 이 경우는 템플릿을 이용하는 것이 훨씬 나은 접근법입니다. HTML을 .html 확장자의 파일 형태로 보관할 수 있다면, 구문 검증을 더 효율적으로 할 수 있습니다. 이를 위한 많은 종류의 파이썬 템플릿 프레임워크가 존재하며, Django도 잘 동작하는 템플릿 프레임워크를 가지고 있습니다.

### Refactoring to Use a Template
지금부터 할 작업은 뷰 함수가 이전과 같은 HTML을 반환하도록 하는 것이지만, 다른 프로세스를 적용하는 것입니다. 이것을 리패터링(Refactoring)이라고 합니다. 리팩터링이란 "기능(결과물)은 바꾸지 않고" 코드 자체를 개선하는 작업을 말합니다.  


"기능은 바꾸지 않고"라는 것이 핵심입니다. 리팩터링을 통해 기능도 동시에 변경하거나 추가하려고 한다면 곧 문제에 부딪힐 것입니다. 리팩터링은 그 자체가 하나의 기술 영역으로 메뉴얼까지 존재합니다.([Refactoring](https://refactoring.com/){:target="_blank"})

첫 번째 규칙은 테스트 없이 리팩터링할 수 없다는 것입니다. 다행히도 지금 다루는 TDD와 같은 내용입니다. 그러면 테스트를 통과하는지 확인해봅니다. 이를 통해 리팩터링 작업이 가능한지를 결정할 수 있습니다.

```
$ python manage.py test
[...]
OK
```
테슽트를 통과했습니다. 이제 HTML 문자열을 별도에 저장해봅니다. 'lists/templates'라는 폴더를 만들고 여기에 쳄플릿 파일들을 저장하도록 합니다. 이 폴더에 'home.html'이라는 새로운 파일을 만들어서 HTML 내용을 저장하도록 합니다.

lists/templates/home.html

```
<html>
    <title>To-Do lists</title>
</html>
```
태그가 구분(강조)되는 것을 볼 수 있습니다. 그러면 뷰 함수를 수정합니다.

lists/views.py

```
from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')
```
`HttpResponse`를 만드는 대신에 Django의 `render` 함수를 사용하고 있습니다. 이 함수는 첫 번째 인수로 요청(request)을 지정하고, 두 번째 인수로 렌더링할 템플릿명을 지정합니다. Django는 앱 폴더 내에 template 이라는 폴더를 자동으로 검색합니다. 그리고 템플릿 콘텐츠를 기반으로  `HttpResponse`를 만들어 줍니다.

> 템플릿은 Django의 매우 강력한 기능 중 하나입니다. 무엇보다 파이썬 변수를 HTML 텍스트로 변경해주는 기능은 큰 강점입니다. 지금은 이 기능을 사용하지 않지만 뒤에서 사용합니다. 여기서 디스크에 있는 파일을 수동으로 읽지 않고, `render`와 'render_to_string'을 사용하는 것도 이것 때문입니다.

동작하는지 확인해봅니다.

```
$ python manage.py test
[...]
======================================================================
ERROR: test_home_page_returns_correct_html (lists.tests.HomePageTest) #2
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "/.../superlists/lists/tests.py", line 17, in
test_home_page_returns_correct_html
    response = home_page(request) #3
  File "/.../superlists/lists/views.py", line 5, in home_page
    return render(request, 'home.html') #4
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
django.template.base.TemplateDoesNotExist: home.html #1

 ---------------------------------------------------------------------
Ran 2 tests in 0.004s
```

>
#1 : 먼저 에러를 확인합니다: 템플릿을 발견할 수 없어서 에러가 발생하고 있습니다.
#2 : 어떤 테스트가 실패하는지 다시 확인합니다: HTML 뷰 테스트 부분이빈다.
#3 : 테스트에서 실패의 원인이 된 부분을 확인합니다: `home_page` 함수 호출에 문제가 있습니다.
#4 : 마지막으로 애플리케이션의 어느 부분에서 에러가 발생하는지 확인합니다: `render` 호출 부분에서 에러가 발생합니다.

왜 Django가 템플릿을 못 찾을까요?

문제는 아직 이 앱을 Django에 등록하지 않았기 때문입니다. Django에게 해당 앱을 사용한다고 신고를 해야 합니다. 이를 웨해서 settings.py 파일에 앱을 추가해야 합니다. 파일을 열어서 `INSTALLED_APPS` 항목을 찾습니다.

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
쉼표(,)를 끝에 추가하는 것을 잊으면 안됩니다. 마지막에 추가할 때는 필요 없지만, 정작 있어야 할 때 추가하는 것을 잊어버려서 애를 먹을 수 있습니다. 파이썬은 다른 줄에 있는 문자열들을 합쳐버리기 때문에 주의가 필요합니다.

수정했으면 다시 테스트를 실행합니다.

```
$ python manage.py test
    [...]
    self.assertTrue(html.endswith('</html>'))
AssertionError: False is not true
```
조금 진전이 있습니다. 이제 템플릿 파일을 찾을 수 있는 듯합니다. 하지만 여전히 마지막 세 개 어설션이 실패하고 있습니다. 디버그를 위해 `print repr(response.content)`를 이용해서 응답 내용을 출력해본 결과, 파일 마지막 부분에 라인(`\n`)이 추가돼 있는 것을 확인할 수 있습니다. 다음과 같이 수정하면 해결 됩니다.

lists/tests.py

```
self.assertTrue(html.strip().endswith('</html>'))
```
작은 팁이지만, HTML 파일 마지막 부분에 있는 빈 공간 때문에 문제가 발생하는 것을 예방해 줍니다. 테스트를 다시 실행합니다.

```
$ python manage.py test
[...]
OK
```
코드 리팩터링 작업이 끝났습니다. 테스트 결과도 만족스럽습니다.
다음은 상수를 테스트하지 않고 템플릿을 이용해서 렌더링하는 것을 테스트하도록 수정해주어야 합니다.


### The Django Test Client
우리가 테스트 할 수 있는 한가지 방법은 직접 템플릿을 테스트에 렌더링 한 다음에 이를 뷰가 반환하는 것과 비교하는 것입니다. 이것은 Django의 `render_to_string` 함수를 이용하면 간단히 구현할 수 있습니다.

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
하지만 이것은 올바른 템플릿을 사용한다는 좀 부담스러운 테스트 방법입니다. `.decode()`와  `strip()`을 사용하면 산만하게 됩니다. 대신 Django는 `Django Test Client`를 제공합니다.


lists/tests.py

```
def test_home_page_returns_correct_html(self):
    response = self.client.get('/')  #1

    html = response.content.decode('utf8')  #2
    self.assertTrue(html.startswith('<html>'))
    self.assertIn('<title>To-Do lists</title>', html)
    self.assertTrue(html.strip().endswith('</html>'))

    self.assertTemplateUsed(response, 'home.html')  #3
```

>
#1 : `HttpRequest` 객체를 생성하고 뷰 함수를 호출하는 대신 `self.client.get`을 호출하여 테스트 할 URL을 전달합니다.  
#2 : 모든 테스트가 제대로 작동하는지 확인하기 위해 이전 테스트는 유지합니다.  
#3 : `.assertTemplateUsed`는 Django TestCase 클래스가 제공하는 테스트 메소드입니다. 이 메소드를 통해 응답을 렌더링하는데 사용 된 템플릿을 확인할 수 있습니다.(NB - 테스트 클라이언트가 검색한 응답에만 작동합니다.)

그리고 그 테스트는 여전히 통과할 것입니다.

```
Ran 2 tests in 0.016s

OK
```
테스트 후 실패하지 못한 것은 의심스럽기 때문에 고의적으로 테스트를 중단시킵니다.

lists/tests.py

```
self.assertTemplateUsed(response, 'wrong.html')
```
그러면 오류 메시지가 어떻게 출력되는지도 배울 수 있습니다.

```
AssertionError: False is not true : Template 'wrong.html' was not a template
used to render the response. Actual template(s) used: home.html
```
이것은 매우 도움이 됩니다. assert를 수정합니다. 오래된 assertion을 삭제할 수 있습니다. 또한 이전 `test_root_url_resolves` 테스트는 Django Test Client에 의해 암시적으로 테스트 되기 때문에 삭제할 수 있습니다. 두 번의 긴 테스트를 하나로 결합했습니다!

lists/tests.py (ch04l010)

```
from django.test import TestCase

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
```
여기서 중요한 것은 상수를 테스트하는 것이 아니라 구현 결과물을 비교하는 것입니다.

> ## Django Test Client를 사용하지 않는 이유는?  
>
'Django Test Client'를 처음부터 사용하지 않은 이유는 무엇일까요? 평소엔 그것을 사용합니다. 하지만 몇 가지 이유로 먼저 "수동적인" 방식을 먼저 다루고 싶었습니다. 첫 번째, 개념을 하나씩 소개하고 학급 곡선을 가능한 얕게 유지할 수 있기 때문입니다. 두 번째, Django를 사용하여 앱을 개발하는 것은 아니기 때문에 테스트 도구를 항상 사용할 수는 없지만, 함수를 직접 호출하고 응답을 검사하는 것은 항상 가능하기 때문입니다.  
>
Django Test Client에는 단점도 있습니다. [뒤](https://www.obeythetestinggoat.com/book/chapter_purist_unit_tests.html){:target="_blank"}에 완전히 고립된 단위 테스트와 Test Client가 우리를 향항 "통합 된"테스트의 차이점에 대해 설명할 것입니다.

## 4.4. On Refactoring
간단한 리팩터링이었습니다. 하지만 켄트 백(Kent Beck)이 "Test-Driven Development"에서 언급했듯이, "이런 식으로 해야 한다는 것이 아니라, 이런 식으로 할 수 있다는 것을 보여주기 위함입니다."  

사실 본능적으로 테스트를 먼저 수정하고 싶었습니다. `assertTemplateUsed` 함수를 바로 사용해서 필요 없는 3개의 assertion을 삭제하고 예상 렌더링과 콘텐츠를 비교하는 부분만 남겨둡니다. 그리고 나서 앱 코드를 수정하는 것입니다. 하지만 이렇게 단계를 나누어 설명함으로 쉽게 이해할 수 있었을 것입니다. <html>이나 <title> 태그 대신에, 임의로 여러 문자열들을 사용해서 템플릿을 만들 수 있었습니다.

> 리팩터링 할 때에는 코드나 테스트 중 하나만 작업해야 합니다.

리팩터링 시에는 몇 가지 처리를 수정하기 위해 단계를 건너뛰는 경향이 있습니다. 하지만 반 이상의 파일을 수정하기 시작하면서 자신이 무엇을 수정했는지 모르게 되고 결국 아무것도 동작하지 않게 됩니다. 리팩터링 캣처럼 되고 싶지 않다면 작은 단계로 나누어 착실히 작업하도록 합니다. 참고로 리팩터링과 기능 변경은 전혀 다른 개념인 것에 유의헤야 합니다.

![]({{ site.url }}/img/post/tdd/4_2.gif)

리팩터링 후에 커밋하는 것이 좋습니다.

```
$ git status # see tests.py, views.py, settings.py, + new templates folder
$ git add .  # will also add the untracked templates folder
$ git diff --staged # review the changes we're about to commit
$ git commit -m "Refactor home page view to use a template"
```

## 4.5. A Little More of Our Front Page

아직까지 기능 테스트가 실패하고 있는 상태입니다. 테스트를 통과하도록 코드를 수정해봅니다. HTML이 이젠 템플릿 형태이기 때문에 추가적인 단위 테스트 없이 바로 수정할 수 있습니다. 현재 필요한 것은 '<h1>'입니다.

lists/templates/home.html

```html
<html>
    <head>
        <title>To-Do lists</title>
    </head>
    <body>
        <h1>Your To-Do list</h1>
    </body>
</html>
```
FT가 이 방식을 좋아하는지 확인합니다.

```
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_new_item"]
```
OK...

lists/templates/home.html

```
[...]
    <h1>Your To-Do list</h1>
    <input id="id_new_item" />
</body>
[...]
```
이번엔 괜찮을까요?

```
AssertionError: '' != 'Enter a to-do item'
```
placeholder를 추가합니다.

lists/templates/home.html

```
<input id="id_new_item" placeholder="Enter a to-do item" />
```
다음과 같은 결과를 확인할 수 있습니다.

```
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate
element: [id="id_list_table"]
```
이제 페이지에 테이블을 추가 할 수 있습니다. 현재는 테이블이 비어있습니다.

lists/templates/home.html

```
<input id="id_new_item" placeholder="Enter a to-do item" />
<table id="id_list_table">
</table>
</body>
```
다시 FT를 실행합니다.

```
File "functional_tests.py", line 43, in
test_can_start_a_list_and_retrieve_it_later
  any(row.text == '1: Buy peacock feathers' for row in rows)
AssertionError: False is not true
```
원인이 분명치 않습니다. 문제를 찾기 위해 코드 넘버를 따라가보니 기능 테스트에 사용한 함수에 문제가 있다는 것을 알았습니다. 정확히는 `assertTrue`라는 함수로, 현재 자세한 실패 메시지를 출력하고 있지 않습니다. 대부분의 `assertX` 함수는 사용자 정의 메시지를 인수로 지정할 수 있습니다.

functional_tests.py

```
self.assertTrue(
    any(row.text == '1: Buy peacock feathers' for row in rows),
    "New to-do item did not appear in table"
)
```
다시 FT를 실행하면 다음고 같은 메시지를 확인할 수 있습니다.

```
AssertionError: False is not true : New to-do item did not appear in table
```
이 문제를 해결하려면 사용자 폼(form) 제출 처리를 구현해야 하는데, 이것은 다음 섹션의 주제입니다.  

일단 커밋합니다.

```
$ git diff
$ git commit -am "Front page HTML now generated from a template"
```
리팩터링으로 인해 템플릿을 렌더링하기 위한 뷰 설정을 완료했고, 상수를 더 이상 테스트하지 않아도 됩니다. 또한 사용자 입력 처리를 위한 준비가 완료되었습니다.

## 4.6. Recap: The TDD Process
TDD 프로세스의 주요 내용을 모두 살펴보았습니다.  

- Functional tests
- Unit tests
- 단위 테스트-코드 주기(The unit-test/code cycle)
- Refactoring

흐름도를 이용해서 TDD 프로세스를 정리해봅니다. 흐름도를 이용하면 반복 처리나 재귀 처리를 표현하고 이해하기 수월합니다.

![]({{ site.url }}/img/post/tdd/4_3.png)

테스트를 작성하고 실행해서 그것이 실패하는 것을 확인합니다. 그리고 문제를 해결하기 위해 최소 코드를 작성합니다. 테스트를 통과할 때가지 이 과정을 반복합니다 필요에 따라선 코드를 리팩터링합니다. 리팩터링 후에는 다시 테스트 과정을 반복해야 합니다.  

기능 테스트와 단위 테스트를 둘 다 해야 할 때는 어떻게 적용할까요? 기능 테스트를 상위 테스트 관점으로 생각하면 됩니다. "최소 코드 작성" 부분이 단위 테스트를 이용하는 작은 TDD 주기가 되는 것입니다.  

![]({{ site.url }}/img/post/tdd/4_4.png)

먼저 기능 테스트를 작성하고 실패하는지 확인합니다. "최소 코드 작성" 프로세스에선 작은 TDD 주기를 통해 테스트가 통과하도록 만듭니다. 이때 하나 또는 그 이상의 단위 테스트를 작성하고 이를 단위 테스트-코드 주기에 넣어서 통과할 때까지 주기를 반복합니다. 통과하면 다시 FT를 돌아가서 애플리케이션 코드를 수정합니다.(리팩터링) 수정 후에는 다시 단위 테스트를 실시합니다.  

기능 테스트 관점의 리팩터링은 어떻게 해야 할까요? 이것은 애플리케이션 동작을 확인하기 위해 기능 테스트를 사용하지만, 단위 테스트를 변경, 추가, 제거 할 수 있음을 의미합니다. 또한 단위 테스트 주기를 이용해서 실제 구현한 것을 변경합니다.  

기능 테스트는 애플리케이션이 동작하는지 아닌지를 판단하기 위한 궁극의 수단입니다. 반면, 단위 테스트는 이 판단을 돕기 위한 툴이라 할 수 있습니다.  

이런 식으로 TDD 를 표현한 것을 "이중 반복 TDD(Double-Loop TDD)"라고 부르는 경우도 있습니다.  

이 후 섹션에서는 이 처리 흐름의 각 요소에 대해 자세히 다룹니다.
