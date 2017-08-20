---
layout: post
section-type: post
title: crawling - P2. 고급 스크레이핑 _ chap 12. 스크레이핑 함정 피하기
category: python
tags: [ 'python' ]
---

사이트를 스크랩하였으나 출력 결과가 브라우저에서 보이는 데이터가 없다거나, 폼을 완벽하게 작성해서 전송하였지만 웹 서버에서 거부 당할 수 있습니다. 우리가 알지 못하는 이유로 IP 주소가 차단당할 때도 있습니다.  

이런 것들을 해결하기 어려운 버그들입니다. 어떤 사이트에서는 완벽하게 동작하는 스크립트가, 겉보기에는 똑같아 보이는 다른 사이트에서는 전혀 동작하지 않는 등 예측하기 어려울 뿐 아니라, 의도적으로 에러 메시지나 스택 추적을 제공하지 않기 때문입니다.  

이전 섹션들에서는 폼을 전송하고, 지저분한 데이터를 추출해서 정리하고, 자바스크립트를 실행하는 등 웹사이트에서 봇으로 하기 어려운 일들 다루는 방법을 다루었습니다. 이번 섹션에서는 다양한 주제(HTTP 헤더, CSS, HTML 폼 등)에서 뻗어 나온 테크닉들을 한데 모았습니다. 이들 모두는 웹 스크레이핑을 막으려는 목적으로 설치된 걸림돌들입니다.  

이번 섹션이 지금 당장은 큰 도움이 되지 않을 수 있지만, 언젠가 매우 어려운 버그를 해결하거나 문제를 예방하는데 도움이 될 것입니다.

## 12.1 스크레이핑의 윤리에 관해

- 정상적인 사용자에게는 아무 영향도 없으면서 스크레이퍼로부터는 절대 안전한 사이트를 만들기는 거의 불가능하지만, 이 장에서 설명하는 정보가 악의적 공격으로부터 웹사이트를 보호하는데 도움이 되길 바랍니다. 이 장에서는 웹 스크레이핑 방법의 약점을 짚기 때문에 사이트를 보호할 때도 활용할 수 있습니다. 최근 웹에 있는 봇은 대부분은 단순히 광범위하게 정보와 취약점을 찾아낼 뿐이고, 이 장에서 설명하는 간단한 테크닉 한두 가지만 적용하더라도 봇의 99%는 무력화시킬수 있습니다. 물론 봇들 역시 계속 진화하고 있으니 항상 대비하는게 중요합니다.

이번 섹션을 읽는  동안 여기서 설명하는 스크립트와 테크닉을 아무 사이트에서나 실행해서는 안됩니다. 올바른 일이 아닐뿐더러, 정지 명령이나 그보다 더 심한 일을 당할 수도 있습니다.

## 12.2 사람처럼 보이기

스크랩을 막고 싶은 사이트에서 가장 먼저 해결할 숙제는 사람과 봇을 구분하는 것입니다. CAPTCHA 처럼 이미 여러 사이트에서 사용하는 방법도 뚫기가 쉽지는 않지만, 봇이 사람처럼 보이게 하는 쉬운 방법이 몇 가지 있습니다.

### 12.2.1 헤더를 수정하십시오

[chap9](https://kimdoky.github.io/python/2017/08/03/crawling-book-chap9.html){:target="`_`blank"}에서 requests 모듈을 써서 웹사이트의 폼을 처리하는 방법을 다루었습니다. 그런데 request 모듈은 헤더 설정에도 뛰어납니다. HTTP 헤더는 웹 서버에 요청을 보낼 때마다 함께 보내는 속성, 또는 선호하는 설정의 묶음입니다. HTTP 정의에는 모호한 헤더 타입이 아주 많이 있는데, 그중 상당수는 현재 거의 쓰이지 않습니다. 다음의 일곱 가지 필드는 대부분의 주요 브라우저에 서버에 연결할 때마다 사용하는 필드입니다.

Field | Value
---|---
Host | http://www.google.com/
Connection | keep-alive
Accept | text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
User-Agent | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)<br>AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95<br>Safari/537.36
Referrer | http://www.google.com/
Accept_Encoding | gzip, deflate, sdch
Accept_Language | en-US,en;q=0.8

그리고 다음은 기본 `urllib` 라이브러리를 사용하는 일반적인 파이썬 스크레이퍼에서 보내는 헤더입니다.

Field | Value
---|---
Accept_Encoding | identity
User-Agent | Python-urllib/3.4

당신이 웹사이트 관리자이고 스크레이퍼를 차단하고 싶다면, 어느 쪽을 허용하겠습니까?

`requests` 모듈을 쓰면 헤더를 원하는 대로 바꿀 수 있습니다. https://www.whatismybrowser.com 에서 브라우저가 보내는 헤더가 서버에서 어떻게 보이는지 테스트할 수 있습니다. 다음 스크립트로 이 사이트를 스크랩해서 쿠키 설정을 확인해봅니다.

```python
import requests
from bs4 import BeautifulSoup

session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
url = "https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending"
req = session.get(url, headers=headers)

bsObj = BeautifulSoup(req.text, "html.parser")
print(bsObj.find("table",{"class":"table-striped"}).get_text)
```

출력 결과의 헤더는 headers 딕셔너리 객체에 설정한 것과 같습니다.  

웹사이트에서 어떤 필드를 보고 사람인지 확인할지는 사이트 관리자의 마음이지만, 일반적으로 `User-Agent` 하나만 확인합니다. 어떤 프로젝트를 만들고 있든, `User-Agent` 필드에 `Python-urllib/3.4`보다는 덜 의심스러운 것을 사용하는게 좋습니다. 사아트 관리자가 의심이 아주 많다면, 널리 쓰이지만 체크하는 일은 드문 `Accept_Language` 같은 필드를 바꾸는 것도 사람처럼 보이는데 도움이 될 수 있습니다.

> ### 헤더는 당신이 세계를 보는 방법을 바꿉니다.  
연구 프로젝트에 사용할  머신 러닝 번역기를 만들고 있지만 테스트에 사용할 번역된 텍스트가 많지 않다고 가정합니다. 대형 사이트들은 같은 콘텐츠를 다른 언어로 번역해서 준비해두었다가 헤더에 있는 언어 설정에 따라서 보여주는 경우가 많습니다. 단순히 헤더에서 `Accept_Language:en-US`를 'Accept_Language:fr'로 바꾸기만 해도 Hello 대신 Bonjour 를 출력하는 사이트들이 있고, 여기에서 번역 사이트에 필요한 텍스트를 얻을 수도 있을 것입니다.  
헤더는 웹사이트가 보내는 콘텐츠 형식을 바꾸기도 합니다. 예를 들어 모바일 장치로 웹을 볼 때는 배너 광고나 플래시, 기타 눈을 어지럽히는 것들이 제거된 버전이 나타낼 때가 많습니다. `User-Agent`를 다음과 같이 바꾸면, 사이트를 스크랩하기가 조금 쉬워질 수 있습니다.  
```
User-Agent:Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X)
AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257
Safari/9537.53
```

### 12.2.2 쿠키 처리

쿠키를 정확히 사용하면 스크레이핑 문제를 상당히 피할 수 있지만, 쿠키는 양날의 검이기도 합니다. 쿠키를 사용해서 웹사이트 어디를 다니는지 추적하는 사이트라면, 폼을 너무 빨리 완성한다거나 너무 여러 페이지를 다니는 등 이상한 행동을 보이는 쿠키를 차단할 수도 있습니다. 연결을 끊었다가 다시 연결하거나 IP 주소를 바꿔도 이런 '이상한 행동'을 숨길 수 있지만, 쿠키에서 정체를 숨길 수 있다면 그런 트릭은 필요 없게 됩니다.  

쿠키는 사이트를 스크랩할 때도 꼭 필요합니다. 사이트에 로그인된 상태를 유지하려면 페이지 사이를 이동할 때 쿠키를 유지하고 제시할 수 있어야 합니다. 일부 웹 사이트는 매번 로그인할 필요조차 없습니다. 한 번 로그인하면 그 쿠키를 오랫동안 가지고 있으면서 사용합니다.  

스크레이핑하는 웹사이트가 많지 않다면 그 사이트가 생성하는 쿠키를 점검해보고 스크레이퍼에서 어떤 쿠키를 조작해야 할지 생각해봐야 합니다. 사이트에 방문하고 이동함에 따라 쿠키가 어떻게 바뀌는지 보여주는 브라우저 플러그인이 많이 있습니다. 많이 사용되는 플러그인들 중 하나는 크롬 확장 프로그램인 [EditThisCookie](http://www.editthiscookie.com/){:target="`_`blank"}입니다.

`requests` 모듈을 써서 쿠키를 처리하는 방법은 [chap9](https://kimdoky.github.io/python/2017/08/03/crawling-book-chap9.html){:target="`_`blank"}을 참고하면 됩니다. 물론 `requests` 모듈은 자바스크립트를 실행하지 못하므로 구글 애널리틱스 같은 최신 추적 소프트웨어에서 만나는 쿠키는 처리하지 못합니다. 이런 쿠키는 클라이언트 쪽 스크립트가 실행을 마치거나 버튼 클릭 같은 페이지 이벤트에 따라 만들어집니다. 이런 쿠키를 처리하려면 셀레니움과 펜텀JS가 필요합니다.  

아무 사이트에나 방문해서 `get_cookies()`를 호출하면 쿠키를 볼 수 있습니다.

```python
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get("http://pythonscraping.com")
driver.implicitly_wait(1)
print(driver.get_cookies())
```

이 코드를 실행하면 매우 일반적인 구글 애널리틱스 쿠키가 보입니다.

```
[{'value': '1', 'domain': '.pythonscraping.com', 'path': '/', 'expiry': 1503214202, 'secure': False, 'httponly': False, 'name': '_gat', 'expires': '일, 20 8월 2017 07:30:02 GMT'}, {'value': 'GA1.2.667061982.1503214143', 'domain': '.pythonscraping.com', 'path': '/', 'expiry': 1503300542, 'secure': False, 'httponly': False, 'name': '_gid', 'expires': '월, 21 8월 2017 07:29:02 GMT'}, {'value': 'GA1.2.1041228017.1503214143', 'domain': '.pythonscraping.com', 'path': '/', 'expiry': 1566286142, 'secure': False, 'httponly': False, 'name': '_ga', 'expires': '화, 20 8월 2019 07:29:02 GMT'}, {'value': '1', 'domain': 'pythonscraping.com', 'name': 'has_js', 'httponly': False, 'secure': False, 'path': '/'}]
```

쿠키를 조작할 때는 `delete_cookie()`, `add_cookie()`, `delete_all_cookies()` 함수를 사용합니다. 또한 쿠키를 다른 웹 스크레이퍼에서 쓸 수 있게 저장하는 것도 가능합니다.

```python
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.get("http://pythonscraping.com")
driver.implicitly_wait(1)
print(driver.get_cookies())

savedCookies = driver.get_cookies()

driver2 = webdriver.PhantomJS()
driver2.get("http://pythonscraping.com")
driver2.delete_all_cookies()
for cookie in savedCookies:
   driver2.add_cookie({
       'domain':'.pythonscraping.com',
       'name': cookie['name'],
       'value': cookie['value'],
       'path': '/',
       'expires': None
   })

driver2.get("http://pythonscraping.com")
driver.implicitly_wait(1)
print(driver2.get_cookies())
```
>
```python
for cookie in savedCookies:
    driver2.add_cookie(cookie)
```
교재의 원래 코드(위 코드)로 실행하면, driver2의 쿠키를 교체하는 부분에서 에러가 발생합니다.
```
Message: {"errorMessage":"Unable to set Cookie"
```

이 예의 첫 번째 웹드라이버는 사이트를 가져와서 쿠키를 출력한 다음 `savedCookies` 변수에 저장했습니다. 두 번째 웹드라이버는 같은 웹사이트를 다시 불러온 다음 두 번째 쿠키를 모두 지우고 첫 번째 웹드라이버에서 저장했던 쿠키로 교체합니다.(두 번째 웹드라이버에서 사이트를 다시 불러오는 것 자체에는 다른 의미가 없지만, 셀레니움이 이 쿠키가 어느 사이트에 속하는지 알게 하려면 꼭 필요한 일입니다.) 페이지를 다시 불러오면 타임스탬프와 코드, 기타 정보가 모두 쿠키와 완전히 같아야 합니다. 구글 애널리틱스로 비교해보니 두 번째 웹드라이버는 첫 번째와 완전히 같았습니다.

> 쿠키 변경 부분을 한 줄씩 실행하여 변경 상황을 체크해봤습니다. (쉽게 구분하기 위해 value 값만 적었습니다.)

```python
# driver cookie
>>> savedCookies
[{... 'name': '_gat', ... 'value': '1', ...}, {... 'name': '_gid', ... 'value': 'GA1.2.1160189992.1503215827', ...}, {... 'name': '_ga', ... 'value': 'GA1.2.1407323930.1503215827', ...}, {'name': 'has_js', ... 'value': '1', ... }]

# driver2 cookie
>>> print(driver2.get_cookies())
[{... 'name': '_gat', ... 'value': '1', ... }, {... 'name': '_gid', ... 'value': 'GA1.2.1827877731.1503215859', ...}, {... 'name': '_ga',  ... 'value': 'GA1.2.304429178.1503215859', ...}, {'name': 'has_js', ... 'value': '1', ... }]

# delete driver2 cookie
>>> driver2.delete_all_cookies()
>>> print(driver2.get_cookies())
[]

# change driver2 cookie to driver cookie
>>> print(driver2.get_cookies())
[{'name': 'has_js', ... 'value': '1', ...}, {'name': '_ga', ... 'value': 'GA1.2.1407323930.1503215827', ...}, {'name': '_gid', ... 'value': 'GA1.2.1160189992.1503215827', ...}, {'name': '_gat', ... 'value': '1', ...}]

# after refrash driver2 cookie
>>> driver2.get("http://pythonscraping.com")
>>> driver.implicitly_wait(1)
>>> print(driver2.get_cookies())
[{...'name': '_gid', ... 'value': 'GA1.2.1160189992.1503215827', ...}, {... 'name': '_ga', ... 'value': 'GA1.2.1407323930.1503215827', ...}, {'name': 'has_js', ... 'value': '1', ...}, {'name': 'has_js', ... 'value': '1', ...}, {'name': '_gat', ... 'value': '1', ...}]
```

### 12.2.3 타이밍이 가장 중요합니다

잘 보호된 일부 웹사이트는 폼을 너무 빨리 전송하거나 너무 빨리 행동한다면 막힐 수 있습니다. 이런 보호 기능이 설치되어 있지 않다고 하더라도, 보통 사람이 움직이는 속도보다 훨씬 빨리, 훨씬 많은 정보를 가져간다면 관리자의 주의를 끌어 차단당할 수 있습니다.  

따라서 한 스레드에서 데이터를 처리하는 동안 다른 스레드에서 계속 페이지를 불러오는 멀티 스레드 프로그래밍은 페이지 로드 속도를 끌어올릴지는 몰라도 스크레이퍼를 만드는 데틑 쓸 수 없습니다. 항상 데이터와 데이터 요청을 최소한으로 유지해야 합니다. 가능하면 몇 초 정도의 간격을 두는 편이 좋습니다.

```python
time.sleep(3)
```

웹 스크레이핑은 데이터를 얻기 위해 규칙을 깨고 경계를 오가는 일이 많지만, 이 규칙만은 지키는게 좋습니다. 서버 자원을 과도하게 소비하면 법적으로 불리해지고, 소규모 사이트를 느리게 만들어 심지어 다운되게 할 수도 있습니다. 웹사이트를 다운시키는 건 윤리적으로도 잘못된 일입니다. 속도에 항상 주의해야 합니다.

## 12.3 널리 쓰이는 폼 보안 기능

### 12.3.1 숨긴 필드 값

### 12.3.2 허니팟 피하기

## 12.4 사람처럼 보이기 위한 체크리스트
