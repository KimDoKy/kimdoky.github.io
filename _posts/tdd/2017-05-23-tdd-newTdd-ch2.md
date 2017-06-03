---
layout: post
section-type: post
title: new TDD-Chapter 2. Extending Our Functional Test Using the unittest Module
category: tdd
tags: [ 'tdd' ]
---
Django의 기본 페이지인 "it worked!" 페이지를 확인하는 테스트를 확장해서 실제 사이트의 메인 페이지에서 확인해야 할 사항들을 반영하도록 합니다.

TDD 스터디를 하면서 구축할 애플리케이션은 작업 목록(To-Do) 사이트(해야 할 일을 정리한 목록 사이트)입니다. 작업 목록은 예제로 사용하기에 매우 좋습니다. 매우 기본적이면서도 간단해서(테스트 리스트만 있으면 됨) "최소한의 실행 가능한" 애플리케이션을 구축하고 실행할 수 있기 때문입니다. 또한 어떤 형태로든 확장할 수 있습니다. 마감일을 추가하거나, 알림 기능, 공유 기능 등을 추가할 수 있고, 클라이언트 UI도 개선할 수 있습니다. 이 예제를 통해 웹 프로그래밍 전반과 TDD 적용 방법에 배울 수 있습니다.

### 2.1 Using a Functional Test to Scope Out a Minimum Viable App

셀레늄을 이용한 테스트에서는 실제 웹 브라우저를 실행해서 애플리케이션이 어떻게 "동작(functions)"하는지 사용자 관점에서 확인 할 수 있습니다. 이런 테스트를 *기능 테스트(Functional test,FT)** 라고 부릅니다.

또한 이것은 FT 자체가 애플리케이션 사양이 될 수 있음을 의미하기도 합니다. *사용자 스토리(User story)* 라고 하는 방식을 따르는 경향이 있는데, 특정 기능을 사용자가 어떻게 사용하며 이때 애플리케이션이 어떻게 반응해야 하는지를 확인하는 방식입니다.

> ## 용어: 기능 테스트 == 승인 테스트 == 종단간 테스트  
사람들마다 다르게 표현하길 원할 수 있습니다. 중요한 것은 이 테스트들이 전체 애플리케이션이 어떻게 동작하는지를 외부 사용자 관점에서 확인하는 테스트라는 것입니다. 블랙박스(BlackBox) 테스트라는 용어를 사용하는 경우도 있는데, 시스템 내부에 대해서 전혀 알지 못하기 때문입니다.

FT는 사람이 이해할 수 있는 스토리를 가지고 있어야 합니다. 이것을 분명하게 정의하기 위해 테스트 코드에 주석을 기록합니다. 새로운 FT를 만들 때는 사용자 스토리의 핵심을 정리하기 위해 주석을 먼저 작성할 수도 있습니다. 사람이 이해할 수 있다는 것은 FT를 프로그래머가 아니더라도 이해할 수 있어야 한다는 것으로, 애플리케이션 요구 사항과 특징을 보고 논의할 수 있을 정도가 돼야 합니다.  

TDD와 애자일(Agile) 개발 방식은 종종 함께 구현되기도 하는데, 이때 언급되는 것이 최소 기능 애플리케이션입니다. 가장 간단한 기능만으로 구성되지만 동작하는 애플리케이션을 의미합니다. 이런 애플리케이션을 구축해서 테스트해보도록 합니다.  

최소 기능의 작업 목록 애플리케이션에 필요한 것은 사용자가 작업을 입력하고 그것을 저장해두는 기능입니다.

functional_tests.py

```Python
from selenium import webdriver

browser = webdriver.Firefox()

# Edith has heard about a cool new online to-do app. She goes
# to check out its homepage
browser.get('http://localhost:8000')

# She notices the page title and header mention to-do lists
assert 'To-Do' in browser.title

# She is invited to enter a to-do item straight away

# She types "Buy peacock feathers" into a text box (Edith's hobby
# is tying fly-fishing lures)

# When she hits enter, the page updates, and now the page lists
# "1: Buy peacock feathers" as an item in a to-do list

# There is still a text box inviting her to add another item. She
# enters "Use peacock feathers to make a fly" (Edith is very methodical)

# The page updates again, and now shows both items on her list

# Edith wonders whether the site will remember her list. Then she sees
# that the site has generated a unique URL for her -- there is some
# explanatory text to that effect.

# She visits that URL - her to-do list is still there.

# Satisfied, she goes back to sleep

browser.quit()
```

> ## 주석을 한마디로 표현하면..  
주석은 분명 코드의 의도나 그 속성을 기록하기 때문에 도움이 됩니다. 하지만 코드로 작성한 것을 그대로 반복해서 글로 표현하는 것은 의미가 없습니다. 예를 들면
```
 wibble 값을 1 늘린다  
 wibble += 1
```  
의미가 없을 뿐 아니라 코드를 변경하지만 주석은 변경하지 않고 넘어갈 위험성이 있고, 이는 잘못된 결과를 토래할 수 있습니다. 가장 이상적인 방법은 이해할 수 있는 변수명이나 함수명을 사용하고, 프로그램 주소를 잘 만들어서 코드 자체만 보고도 해석이 가능하도록 하는 것입니다. 이렇게 하면 어던 코드인지 설명하는 주석을 굳이 사용하지 않아도 됩니다. 중요한 곳에만 코드 사용의 이유를 설명해두면 되는 것입니다.  
>
물론 주석이 유용하게 사용되는 경우도 있습니다. Django에서 많은 주석을 사용하는데, 이는 API 적용을 위한 유용한 정보들을 담고 있기 때문입니다. 또한 기능 테스트에선 사용자 스토리를 표현하기 위해 주석을 사용합니다. 이를 통해 늘 사용자 관점에서 테스트하는 것이 가능해집니다.

테스트 스토리를 주석으로 표현했고, 어썰션(assertion)이 "Django" 대신에 "To-Do"라는 타이틀을 찾도록 수정했습니다. 지금 시점에서는 테스트가 실패해야 하기 때문입니다. 그럼 실행해 봅니다.  

먼저 서버를 시작합니다.

```
$ python manage.py runserver
```
서버를 켜 둔 상태에서 FT 진행합니다.

```
$ python functional_tests.py
Traceback (most recent call last):
  File "functional_tests.py", line 10, in <module>
    assert 'To-Do' in browser.title
AssertionError
```
기대한 대로 테스트가 실패했습니다.

### 2.2 The Python Standard Library’s unittest Module

조금 성가시지만 다루고 넘어야 할 것이 있습니다. 먼저 "AssertionError"라는 메세지가 도움이 되지 못한다는 것입니다. 테스트가 브라우저 타이틀에서 어떤 문구를 찾았는지 알려준다면 유용할 것입니다. 또한 파이어폭스 창이 떠돌아다니는데 이것을 자동적으로 닫아 줄 수 있다면 좋을 것입니다.

브라우저 타이틀명을 표시하기 위해서 asser 명령의 두 번째 인수를 이용해서 다음과 같이 기술하면 됩니다.

```python
assert 'To-Do' in browser.title, "browser title was " + browser.title
```
열려있는 파이어폭스 창을 닫아주기 위해선 `try/finally`를 이용해도 되지만, 이런 문제는 테스트 시에 자주 발생하기 때문에 이를 위한 별도 솔루션이 이미 존재합니다. 기본 라이브러리의 `unittest` 모듈입니다. 그럼 적용해 봅니다.

functional_tests.py

```
from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):  #1

    def setUp(self):  #3
        self.browser = webdriver.Firefox()

    def tearDown(self): #3
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):  #2
        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)  #4
        self.fail('Finish the test!')  #5

        # She is invited to enter a to-do item straight away
        [...rest of comments as before]

if __name__ == '__main__':  #6
    unittest.main(warnings='ignore')  #7
```

> #1 : 'unittest.TestCase'를 상속해서 테스트를 클래스 형태로 만듭니다.  
> #2 : `test`로 시작하는 이름은 테스트 메소드이며 테스트 실행자에 의해 실행됩니다. 클래스 당 하나 이상의 테스트 메소드를 작성할 수 있습니다. 가능한 테스트 내용을 알 수 있는 테스트 메소드 명칭을 사용하는 것이 좋습니다.
> #3 : `setUP`과 `tearDown`은 특수한 메소드로, 각 테스트 시작과 후에 실행됩니다. 여기서는 브라우저를 시작하고 닫을 때 사용하고 있습니다. `try/except`와 비슷한 구조로 테스트에 에러가 발생해도 `tearDown`이 실행됩니다.(`setUP`내에 `exception`이 있는 경우는 `tearDown`이 실행되지 않습니다.) 이를 이용하면 파이어폭스 창이 쓸데없이 떠다니는 것을 막을 수 있습니다.  
> #4 : 테스트 어설션을 만들기 위해, assert 대신에 `self.assertIn`을 사용합니다. `unittest`는 테스트 어설션을 만들기 위해 이런 유용한 함수를 다수 제공합니다. 예를 들면 `assertEqual`, `assertTrue`, `assertFalse` 같은 것이 있습니다. 자세한 사항은 [unittest 문서](https://docs.python.org/3/library/unittest.html){:target="_blank"}를 확인하세요.  
> #5 : `self.fail`은 강제적으로 테스트 실패를 발생시켜서 에러 메세지를 출력합니다. 여기서는 테스트가 끝났다는 것을 알리기 위해 사용하고 있습니다.  
> #6 : 마지막은 `if __name__ == '__main__'` 부분입니다.(파이썬 스크립트가 다른 스크립트에 임포드 된 것이 아니라 커맨드라인을 통해 실행됐다는 것을 확인하는 코드입니다.) `unittest.main()`을 호출해서 `unittest` 테스트 실행자를 가동합니다. 이것은 자동으로 파일 내 테스트 클래스와 메소드를 찾아서 실행해주는 역할을 합니다.  
> #7 : `warnings='ignore'`는 테스트 작성 시에 발생하는 불필요한 리소스 경고를 제거하기 위한 것입니다. 이 부분을 진행할 때쯤이면 이미 리소스 경고 문제가 발생하디 않기 때문에 삭제해도 무관합니다.

> Django 테스트 문서를 이미 읽었다면, `LiveServerTestCase`라는 것을 보고 이걸 사용하는 것이 좋은 건지 궁금해할 수도 있습니다. 현 시점에서는 매우 복잡한 기능으로써 후반부에 다루도록 합니다.

그러면 코드를 실행해 봅니다.

```
$ python functional_tests.py
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVisitorTest)
 ---------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 18, in
test_can_start_a_list_and_retrieve_it_later
    self.assertIn('To-Do', self.browser.title)
AssertionError: 'To-Do' not found in 'Welcome to Django'

 ---------------------------------------------------------------------
Ran 1 test in 1.747s

FAILED (failures=1)
```
이전보다 조금 나아진 것을 알 수 있습니다. 테스트가 파이어폭스 창과 연동되고, 제대로 된 형태의 결과 메세지가 출력됩니다. 몇 개의 테스트가 실행됐고 그중에서 몇 개가 실패했는지 보여주며, `assertIn`은 유용한 디버깅 정보와 함께 도움이 되는 에러 메세지를 출력하고 있습니다.

### 2.3 Commit

커밋(commit)하기에 좋은 타이밍입니다. 매우 정확한 변경 내용을 반영할 수 있습니다. 기능 테스트에 설정한 스토리를 주석으로 포함시켰습니다. 또한 파이썬 `unittest` 모듈과 모듈에 포함된 다양한 테스트 함수들을 추가했습니다.  

`git status`를 실행하면 `functional_tests.py` 파일이 변경된 유일한 파일이라는 것을 확인할 수 있습니다. `git diff`를 실행하면 이전에 커밋한 내용과 현재 디스크상에 있는 파일이 어떻게 다른지 보여줍니다. 꽤 많은 부분이 수정된 것을 알 수 있습니다.

```
$ git diff
diff --git a/functional_tests.py b/functional_tests.py
index d333591..b0f22dc 100644
--- a/functional_tests.py
+++ b/functional_tests.py
@@ -1,6 +1,45 @@
 from selenium import webdriver
+import unittest

-browser = webdriver.Firefox()
-browser.get('http://localhost:8000')
+class NewVisitorTest(unittest.TestCase):

-assert 'Django' in browser.title
+    def setUp(self):
+        self.browser = webdriver.Firefox()
+
+    def tearDown(self):
+        self.browser.quit()
[...]
```
커밋을 실행합니다.

```
$ git commit -a
```

`-a`는 "모든 변경 내용을 관리 가능 파일에 자동으로 반영한다"라는 의미입니다.(관리 가능 파일이란, 이미 이전에 커밋한 이력이 있는 파일입니다.) 이 옵션은, 새로운 파일은 커밋 대상에서 제외합니다.(명시적으로 `git add`로 추가할 수 있습니다.) 특히 이번 경우느 추가 파일이 없기 때문에 유용한 단축 명령입니다.

> # 유용한 TDD 개념  
## 사용자 스토리(User Story)  
사용자 관점에서 어떻게 애플리케이션이 동작해야 하는지 기술한 것입니다. 기능 테스트 구조화를 위해 사용합니다.  
## 예측된 실패(Excepted failure)  
의도적으로 구현한 테스트 실패를 의미합니다.
