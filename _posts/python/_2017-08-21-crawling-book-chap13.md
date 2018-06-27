---
layout: post
section-type: post
title: crawling - P2. 고급 스크레이핑 _ chap 13. 스크레이퍼로 웹사이트 테스트하기
category: python
tags: [ 'python' ]
---

여러 기술이 복합된 웹 프로젝트를 개발하다 보면, 정기적으로 테스트하는 부분은 보통 서버쪽에 한정됩니다. 파이썬을 포함해 최근의 프로그래밍 언어는 대부분 어떤 종류든 테스트 프레임워크가 들어 있지만, 프론트엔드는 제외되곤 합니다. 방문자와 사용자가 만나는 부분은 프론트엔드밖에 없는데도 말입니다.  

웹사이트를 개발할 때 여러 가지 마크업 언어와 프로그래밍 언어를 뒤죽박죽 섞어는 쓰는 것도 이런 문제의 원인 중 하나입니다. 자바스크립트에 단위 테스트를 적용할 수 있지만, HTML이 바뀌어서 자바스크립트가 의도한 대로 동작할 수 없게 될 때도 있습니다.  

프론트엔드 테스트는 나중으로 미뤄지거나 초보 프로그래머에게 맡기게 됩니다. 그리고 초보 프로그래머는 기껏해야 체크리스트와 버그 트래커 정도 입니다. 하지만 조금만 수고를 들이면 이 체크리스트를 단위 테스트로, 사람의 눈을 웹 스크레이퍼로 대체할 수 있습니다.  

웹 인터페이스의 모든 부분이 의도한 대로 동작하는지 매일 테스트하고, 누군가 웹사이트에 새 기능을 추가하거나 요소 위치를 바꿀 때마다 테스트 슈트가 동작하는 TDD를 상상해봅니다. 이번 챕터에서는 파이썬 기반 웹 스크레이퍼로 웹사이트를 테스트하는 기본적인 방법을 다룹니다.

## 13.1 테스트 입문

코드가 예상대로 동작한다고 확신할 수 있는 (최소한 테스트를 만든 부분에서는) 테스트 슈트를 만들어 두면 시간과 걱정을 덜 수 있고, 새 업데이트를 적용하기도 쉽습니다.

### 13.1.1 단위 테스트란?

**테스트** 와 **단위 테스트** 는 종종 혼용됩니다. 프로그래머들이 테스트를 만들고 있다고 말한다면 단위 테스트를 만들고 있는 겁니다. 반면 프로그래머가 단위 테스트를 만들고 있다고 말한다면 사실은 다른 종류의 테스트를 만들고 있을 때가 많습니다.

구체적인 정의와 방법은 회사마다 다르지만, 단위 테스트에는 일반적으로 다음과 같은 특징이 있습니다.

- 각 단위 테스트는 한 구성 요소 기능의 한 가지 측면만 테스트합니다. 예를 들어 은행 계좌에서 돈을 인출할 때 액수가 음수라면 적절한 에러 메시지와 함께 에러가 일어나는지 테스트할 수 있습니다.
- 각 단위 테스트는 완벽히 독립적이어야 하며, 각 단위 테스트의 시작과 끝은 반드시 그 단위 테스트 자체에서 모두 이루어져야 합니다. 마찬가지로, 단위 테스트는 다른 테스트의 성공 여부에 영향을 받아서는 안되며, 반드시 순서에 상관없이 실행할 수 있어야 합니다.
- 각 단위 테스트에는 보통 **어서션(assertion)** 이 최소한 하나 들어갑니다. 어서션(단언)이란, 예를 들어 2 + 2는 반드시 4 라고 확정적으로 말하는 겁니다. 가끔 단위 테스트에 실패 상태만 포함될 때도 있습니다.예를 들어 예외가 발생하지 않은 상황을 실패 상태로 정하면 예외가 발생하지 않았을 때는 아무 일도 하지 않고 넘어갈 겁니다.
- 단위 테스트는 메인 코드와는 별도로 관리합니다. 테스트할 코드를 임포트해서 테스트해야 하지만, 일반적으로 다른 클래스와 디렉터리에 분리합니다.

통합 테스트와 유효성 검사 테스트 등 테스트 타입은 여러 가지 있지만, 이번 챕터는 단위 테스트에만 집중합니다. 최근 TDD가 인기를 끌면서 단위 테스트가 널리 쓰이기도 하지만, 단위 테스트는 짧고 유연해서 예제와 함께 사용하기 쉽습니다. 파이썬에는 단위 테스트 기능이 내장되어 있습니다.

## 13.2 파이썬 `unittest`

파이썬의 단위 테스트 모듈 `unittest`는 파이썬을 표준으로 설치하면 항상 설치됩니다. `unittest.TestCase` 를 임포트해서 확장해 쓰기만 하면 다음과 같은 기능을 제공합니다.

- 각 단위 테스트의 처음과 끝에서 동작하는 setUp, tearDown 함수
- 테스트가 성공 또는 실패하게 하는 여러 가지 타입의 assert 문
- `test_`로 시작하는 모든 함수를 단위 테스트로 실행하고 이 접두어가 없는 함수는 무시

다음 코드는 2 + 2 = 4 를 테스트하는 매우 단순한 단위 테스트입니다.

```python
import unittest

class TestAddition(unittest.TestCase):
    def setUp(self):
        print("Setting up the test")
    def tearDown(self):
        print("Tearing down the test")
    def test_twoPlusTwo(self):
        total = 2+2
        self.assertEqual(4, total)
if __name__ == '__name__':
    unittest.main()
```

이 코드에서 `setUp`과 `tearDown`에 별 유용한 기능은 없지만 예시 목적으로 여기 포함시켰습니다. 이들 함수는 각 테스트가 시작하고 끝날 때 실행되는 것이지, 클래스에 있는 모든 테스트보다 먼저 실행되거나 모든 테스트가 끝난 다음에 실행되는 것은 아닙니다.

```
Setting up the test
Tearing down the test
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

### 13.2.1 위키백과 테스트

웹사이트 프론트엔드 테스트는 스크레이퍼에 파이썬 `unittest` 라이브러리를 결합하기만 하면 될 정도로 매우 간단합니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest

class TestWikipedia(unittest.TestCase):
    bsObj = None
    def setUpClass():
        global bsObj
        url = "http://en.wikipedia.org/wiki/Monty_Python"
        bsObj = BeautifulSoup(urlopen(url), "html.parser")

    def test_titleText(self):
        global bsObj
        pageTitle = bsObj.find("h1").get_text()
        self.assertEqual("Monty Python", pageTitle)

    def test_contentExists(self):
        global bsObj
        content = bsObj.find("div", {"id":"mw-content-text"})
        self.assertIsNotNone(content)

if __name__ == '__main__':
    unittest.main()
```

이번에는 두 가지를 테스트합니다. 첫 번째 테스트는 페이지 타이틀이 Monty Python 인지 확인하고, 두 번째 테스트는 페이지에 콘텐츠 div가 있는지 확인합니다.  

```
..
----------------------------------------------------------------------
Ran 2 tests in 1.790s

OK
```

페이지 콘텐츠는 한 번만 불러왔고 전역 객체 bsObj를 두 테스트에서 공유합니다. 이렇게 할 수 있는 것은 `unittest`에서 사용하는 `setUpClass`함수 덕분입니다. 이 함수는 매 테스트마다 실행되는 `setUp`과는 달리 클래스를 시작할 때 단 한 번 실행됩니다. `setUp` 대신 `setUpClass`를 사용하면 불필요한 로딩을 줄이고 페이지 콘텐츠를 한 번만 불러와서 여러 테스트를 실행할 수 있습니다.  

한 번에 페이지 하나씩 테스트하는 건 그리 강력하거나 흥미로워 보이지 않지만, 웹사이트의 페이지 전체를 방문하는 웹 크롤러와 각 페이지마다 어서션을 실행하는 단위 테스트와 결합하면 어떨까요?  

테스트를 반복적으로 실행하는 방법은 여러 가지이지만, 각 테스트 세트마다 페이지를 반드시 한 번씩만 불러오도록 조심해야 하며, 메모리에 너무 많은 정보를 담고 있지 않게 해야 합니다. 다음 코드가 바로 그 작업입니다.

```python
class TestWikipedia(unittest.TestCase):
    bsObj = None
    url = None

    def test_PageProperties(self):
        global bsObj
        global url

        url = "http://en.wikipedia.org/wiki/Monty_Python"
        # 처음 100 페이지를 테스트 합니다.
        for i in range(1,100):
            bsObj = BeautifulSoup(urlopen(url), "html.parser")
            titles = self.titleMatchesURL()
            self.assertEquals(titles[0], titles[1])
            self.assertTrue(self.contentExists())
            url = self.getNextLink()
        print("Done!")

    def titleMatchesURL(self):
        global bsObj
        global url
        pageTitle = bsObj.find("h1").get_text()
        urlTitle = url[(url.index("/wiki/")+6):]
        urlTitle = urlTitle.replace("_", " ")
        urlTitle = unquote(urlTitle)
        return [pageTitle.lower(), urlTitle.lower()]

    def contentExists(self):
        global bsObj
        content = bsObj.find("div", {"id":"mw-content-text"})
        if content is not None:
            return True
        return False

    def getNextLink(self):
        # 챕터5에서 설명한 방법에 따라 페이지의 링크를 무작위로 반환합니다.
        global bsObj
        links = bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
        link = links[random.randint(0, len(links)-1)].attrs['href']
        print("Next link is: "+link)
        return "http://en.wikipedia.org"+link

if __name__ == '__main__':
    unittest.main()
```

실행 결과입니다.

```
chap13_2_1_wiki_unittest_2.py:22: DeprecationWarning: Please use assertEqual instead.
  self.assertEquals(titles[0], titles[1])
Next link is: /wiki/Twice_a_Fortnight
Next link is: /wiki/The_Philosophers%27_Football_Match
...
Next link is: /wiki/Mythic_Entertainment
Next link is: /wiki/Customization_of_avatars
F
======================================================================
FAIL: test_PageProperties (__main__.TestWikipedia)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "chap13_2_1_wiki_unittest_2.py", line 22, in test_PageProperties
    self.assertEquals(titles[0], titles[1])
AssertionError: 'avatar (computing)' != 'customization of avatars'
- avatar (computing)
+ customization of avatars


----------------------------------------------------------------------
Ran 1 test in 30.957s

FAILED (failures=1)
```

여기에는 몇 가지 눈여겨볼 것이 있습니다. 먼저, 이 클래스에 실제 테스트는 단 하나뿐입니다. 다른 함수들은 테스트가 통과했는지 판단하기 위해 복잡한 작업을 하긴 하지만, 그래도 보조 함수일 뿐입니다. 테스트 함수에서 assert 문을 실행하므로, 테스트 결과는 그 함수로 다시 돌아갑니다.  

또, contentExists는 불리언을 반환하지만 titleMatchesURL은 그 값을 평가할 수 있도록 반환합니다. 그냥 불리언을 반환하지 않고 값을 되돌린 이유는, 다음 블리언 어서션의 결과를 비교해 보면 알 수 있습니다.

```
======================================================================
FAIL: test_PageProperties (__main__.TestWikipedia)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "chap13_2_1_wiki_unittest_2.py", line 22, in test_PageProperties
    self.assertTrue(self.titleMatchesURL())
AssertionError: False is not true
```

assertEquals 문의 결과입니다.

```
======================================================================
FAIL: test_PageProperties (__main__.TestWikipedia)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "chap13_2_1_wiki_unittest_2.py", line 22, in test_PageProperties
    self.assertEquals(titles[0], titles[1])
AssertionError: 'avatar (computing)' != 'customization of avatars'
- avatar (computing)
```

디버그하기에 훨씬 수월해집니다.  

여기서 에러가 난 이유는 http://wikipedia.org/wiki/Customization_of_avatars 항목이 avatar (computing) 항목으로 리다이렉트했기 때문입니다.

## 13.3 셀레니움을 사용한 테스트

Ajax 스크레이핑도 쉽지 않지만, 자바스크립트는 웹사이트 테스트도 어렵게 할 때가 있습니다. 다행히 셀레니움은 복잡한 웹사이트도 처리할 수 있는 훌륭한 테스트 프레임워크를 갖고 있습니다. 셀레니움은 원래 웹사이트 테스트를 위해 설계되었습니다.  

셀레니움의 단위 테스트는 클래스 안에 함수로 저장하지 않아도됩니다. 셀레니움의 어서션 문에는 괄호가 필요 없고, 테스트는 조용히 수행되며 어떤 에러가 있을 때만 메시지가 표시됩니다.

```python
driver = webdriver.PhantomJS()
driver.get("http://en.wikipedia.org/wiki/Monty_Python")
assert "Monty Python" in driver.title
driver.close()
```
이 테스트를 실행해도 출력 결과는 없습니다.  

셀레니움 테스트는 이런 방식으로 파이썬 단위 테스트보다 가볍게 작성할 수 있으며, 어서션 문을 일반적인 코드에 쓸 수도 있습니다. 이런 방식은 특정 조건이 맞지 않을 때 코드 실행을 종료하고자 할 때 유용합니다.

### 13.3.1 사이트 조작

폼의 기능을 테스트하고 브라우저에서 완벽히 동작하는지 확인하려면 어떻게 해야 할까요?  

이전에 링크 이동과 폼 제출, 기타 상호작용과 비슷한 동작들을 다루었지만, 핵심은 브라우저 인터페이스를 사용하는 것이 아니라 **지나가는** 것이었습니다. 반면 셀레니움은 문자 그대로 텍스트를 입력하고, 버튼을 클릭하고, 기타 우리가 브라우저를 사용 할때 하는 일 전부를 합니다. 그리고 잘못된 폼, 코드가 엉성한 자바스크립트, HTML 오타, 그 밖에도 고객이나 방문자를 방해할 만한 요소들을 모두 찾아낼 수 있습니다.  

이런 종류의 테스트의 핵심은 셀레니움 elements 라는 개념입니다. [쳅터10](https://kimdoky.github.io/python/2017/08/13/crawling-book-chap10.html){:target="`_`blank"}에서 가볍게 다루었었습니다. 다음과 같이 호출하면 이 객체가 반환됩니다.

```python
usernameField = driver.find_element_by_name('username')
```
브라우저에서 사이트의 여러 요소에 다양한 행동을 취할 수 있는 것처럼, 셀레니움도 주어진 요소에 다양한 행동을 취할 수 있습니다. 그중에서도 다음과 같은 것들이 널리 쓰입니다.

```python
myElement.click()
myElement.click_and_hold()
myElement.release()
myElement.double_click()
myElement.send_keys_to_element("content to enter")
```

이런 행동 여러 개를 **체인** 으로 묶어서 저장하고 원하는 만큼 실행할 수도 있습니다. 액션 체인은 행동 여러 개를 하나로 묶는 간편한 방법이면서, 앞서 다룬 예제들처럼 요소에 대해 해당 행동을 명시적으로 호출하는 것과 기능적으로는 완전히 같습니다.  

http://pythonscraping.com/pages/files/form.html 에 있는 폼 페이지를 보면 어떤 차이가 있는지 볼 수 있습니다. 다음 방법으로 폼을 채우고 전송할 수 있습니다.

```python
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

driver = webdriver.PhantomJS()
driver.get("http://pythonscraping.com/pages/files/form.html")

firstnameField = driver.find_element_by_name("firstname")
lastnameField = driver.find_element_by_name("lastname")
submitButton = driver.find_element_by_id("submit")

### 방법 1 ###
firstnameField.send_keys("Doky")
lastnameField.send_keys("Kim")
submitButton.click()
#############

### 방법 2 ###
actions = ActionChains(driver).click(firstnameField).send_keys("Doky").click(lastnameField).send_keys("Kim").send_keys(Keys.RETURN)
actions.perform()
#############

print(driver.find_element_by_tag_name("body").text)

driver.close()
```

방법 1은 두 필드에서 `send_keys`를 호출한 다음 전송 버튼을 클릭합니다. 방법 2는 액션 체인으로 각 필드를 클릭한 다음 텍스트를 입력하는데, 이 동작은 `perform` 메서드를 호출했을 때 차례대로 일어납니다. 어느 방법을 써도 동일하게 동작합니다.

```
Hello there, Doky Kim!
```

두 방법에는 작은 차이가 하나 더 있습니다. 첫 번째 방법은 전송 버튼을 두번 클릭했고, 두 번째 방법은 엔터 키를 눌렀습니다. 셀레니움에서는 결과적으로는 같은 동작을 여러 가지 방법으로 할 수 있으니 다양한 방법을 생각해 낼 수 있습니다.

#### 드래그 앤 드롭

버튼을 클릭하고 텍스트를 입력하는 것도 유용하지만, 셀레니움이 정말 뛰어난 것은 웹에서 비교적 최근부터 쓰이는 상호작용도 따라 할 수 있다는 점입니다. 셀레니움은 드래그 앤 드롭 동작도 쉽게 흉내 낼 수 있습니다. 드래그 앤 드롭 기능을 사용하려면 드래그할 요소인 '소스' 요소를 지정하고, 이동할 오프셋 또는 드래그 대상 요소를 지정하면 됩니다.  

데모 페이지(http://pythonscraping.com/pages/javascript/draggableDemo.html)에서 드래그 앤 드롭 인터페이스 예제를 볼 수 있습니다.

```
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains

jquery_url = "http://code.jquery.com/jquery-1.11.2.min.js"

driver = webdriver.PhantomJS()
driver.get("http://pythonscraping.com/pages/javascript/draggableDemo.html")

print(driver.find_element_by_id("message").text)

### drag and drop ###
# load jQuery helper
with open("jquery_load_helper.js") as f:
    load_jquery_js = f.read()

# load drag and drop helper
with open("drag_and_drop_helper.js") as f:
    drag_and_drop_js = f.read()

# load jQuery
driver.execute_async_script(load_jquery_js, jquery_url)

driver.execute_script(drag_and_drop_js + "$('#draggable').simulateDragDrop({ dropTarget: '#div2'});")
########################
'''
element = driver.find_element_by_id("draggable")
target = driver.find_element_by_id("div2")
actions = ActionChains(driver)
actions.drag_and_drop(element, target).perform()
'''

print(driver.find_element_by_id("message").text)
```
> 점검 필요  
https://stackoverflow.com/questions/29381233/how-to-simulate-html5-drag-and-drop-in-selenium-webdriver/29381532#29381532

```
Prove you are not a bot, by dragging the square from the blue area to the red area!
```
그리고 작업이 왼료됨과 동시에, 다음 메시지가 표시됩니다.
```
You are definitely not a bot!
```
페이지의 메시지처럼, 요소를 드래그해서 봇이 아님을 증명하는 것은 CAPTCHA에서 널리 쓰이는 방법입니다. 물론 그저 클릭하고, 누른 채 움직이기만 하면 되니까 봇이 페이지 요소를 드래그 할 수 있게 된 건 오래된 일이지만 이걸 움직여서 사람임을 증명하라는 발상은 아직 그대로입니다.  

드래그 앤 드롭을 사용하는 CAPTCHA 라이브러리에서 '고양이 그림을 소 그림 위로 드래그하시오'같은, 봇에게는 무척 어려운(명령을 이해하고, 고양이와 소를 구분해야 하니까요) 행동을 지시하는 경우는 별로 없습니다. 대개는 숫자를 정렬한다거나 하는 쉬운 문제를 냅니다.  

물론 이런 드래그 앤 드롭 테크닉의 강점은 그 변형이 엄청나게 많다는 것인데, 사실 그런 변형들은 많이 쓰이지 않습니다. 그런 경우의 수에 모두 대응하는 봇을 만들 사람은 없으니까요.

#### 스크린샷 찍기

셀레니움에는 스크린샷 기능이 있습니다.

```python
driver = webdriver.PhantomJS()
driver.get('http://www.pythonscraping.com/')
driver.get_screenshot_as_file('tmp/pythonscraping.png')
```
이 스크립트는 http://www.pythonscraping.com 으로 이동한 후 홈페이지 스크린샷을 찍어서 tmp 폴더에 저장합니다.(폴더는 미리 만들어두어야 합니다.) 스크린샷은 다양한 이미지 형식을 사용할 수 있습니다.

## 13.4 `unittest` vs 셀레니움

unittest와 셀레니움은 각각 최적화 되어 있는 부분들이 있습니다. 셀레니움은 사이트에서 정보를 가져오는데 편리하고, unittest는 그 정보가 테스트를 통과하는 기준에 맞는지 평가할 수 있습니다. unittest에 셀레니움을 임포트해서 사용할 수도 있습니다.  

바로 앞의 드래그 예제에서 어서션을 포함한 단위 테스트를 만들 수 있습니다.

```python
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
import unittest

class TestAddition(unittest.TestCase):
    driver = None
    def setUp(self):
        global driver
        driver = webdriver.PhantomJS()
        url = 'http://pythonscraping.com/pages/javascript/draggableDemo.html'

    def tearDown(self):
        print("Tearing down the test")

    def test_drag(self):
        global driver
        element = driver.find_element_by_id("draggable")
        target = driver.find_element_by_id("div2")
        actions = ActionChains(driver)
        actions.drag_and_drop(element, target).perform()

        self.assertEqual("You are definitely not a bot!", driver.find_element_by_id("message").text)

if __name__ == '__main__':
    unittest.main()
```
> 위의 드래그 예제가 제대로 실행이 안되기 때문에 어서션 에러가 일어납니다.

파이썬 unittest와 셀레니움을 조합하면 웹사이트의 거의 모든 것을 테스트 할 수 있습니다. [이미지처리 라이브러리](https://kimdoky.github.io/python/2017/08/14/crawling-book-chap11.html){:target="`_`blank"}와 함께 사용한다면 사이트의 스크린샷을 찍어 픽셀 단위로 정교하게 테스트할 수도 있습니다.
