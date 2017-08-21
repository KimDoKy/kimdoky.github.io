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

봇이 사이트에서 공개한 글과 블로그 포스트를 몇 개 내려받는 건 별 문제가 아니지만, 봇이 사용자 계정을 수천 개 만들고 사이트 사용자에게 스팸을 뿌려댄다면 큰 문제가 됩니다. 웹 폼, 특히 계정 생성과 로그인에 관련된 폼은 봇의 무분별한 사용을 차단하지 못한다면 중요한 위협 보안과 서버 자원에 심각한 위협이 됩니다. 따라서 대부분의 사이트 소유자들은 사이트 접근 제한을 중요한 문제로 판단하고 있습니다.  

폼과 로그인에서 봇을 차단하기 위해 사용하는 보안수단은 웹 스크레이퍼에게 매우 어려운 문제입니다.  

이 섹션에서 설명하는 내용은 자동화된 봇을 만들 때 고려해야 할 보안 수단의 일부일 뿐입니다.  

### 12.3.1 숨긴 필드 값

'숨긴' 필드의 값은 브라우저에게는 보이지만 사용자에게는 보이지 않습니다.(물론 사이트의 소스 코드에서는 볼 수 있습니다.) 쿠키에 변수를 저장하고 웹사이트 전체에서 사용하는 방법이 널리 퍼지면서 숨김 필드는 한동안 사용되지 않았지만, 스크레이퍼가 폼을 전송하지 못하게 막는 용도로 최근에 사용되고 있습니다.  

다음 그림은 페이스북 로그인 페이지에 사용된 숨김 필드입니다. 페이스북 로그인 페이지에서 사용자에게 보이는 것은 사용자 이름과 비밀번호 필드, 전송 버튼뿐이지만 사실 이 폼은 이면에서 아주 많은 정보를 서버에 전달합니다.

![]({{site.url}}/img/post/python/crawling/c12_3_1.png)

숨긴 필드가 웹 스크레이핑을 막는 방법은 크게 두 가지입니다. 서버에서 폼을 생성할 때 무작위로 변수를 만들어 폼을 넣고 그 값을 처리하는 페이지에서 받는 방법입니다. 이 값이 폼에 들어 있지 않다면 서버는 전송 받은 값이 폼 페이지에서 온 것이 아니라 봇이 직접 보냈다고 판단할 만한 근거를 갖게 됩니다. 이 방법에 대응하는 가장 좋은 방법은 먼저 폼 페이지를 스크랩해서 무작위로 생성된 변수를 가져온 후 처리 페이지로 보내는 것입니다.  

두 번째 방법은 일종의 허니팟(honey pot)입니다.
> #### 허니팟(honey pot)?  
컴퓨터 보안 탐지, 어떤 방식으로의 무단 사용 시도에 대항하도록 설정 메커니즘 정보 시스템  
속임술, 악성 코드 허니팟, 스팸 버전, 이메일 트랩 등이 있다.

폼에 숨긴 필드가 있고, 그 필드의 name 속성이 당연히 있을 법한, 예를 들어 username 이나 email address 같은 것이라면, 이런 상황을 고려하지 않고 만든 봇은 그 필드가 숨겨져 있는지 아닌지와 관계없이 값을 채우고 전송할 것입니다. 숨긴 필드가 실제 값으로 채워지거나, 처리하는 페이지에서 기본값으로 정해놓은 값과 다르다면 서버는 전송된 값을 무시하고, 심지어 해당 사용자를 차단하는 경우도 있습니다.  

다시 정리하자면, 이따근 서버에서 예상하고 있는 것을 놓치지는 않았는지 폼 페이지를 확인해야합니다. 숨긴 필드가 여러 개 있고 종종 무작위로 생성된 큰 문자열 변수가 들어 있다면 서버에서 폼을 전송 받을 때 그 값이 들어 있는지 체크하고 있을 가능성이 높습니다. 또한 폼 변수가 단 한 번만 사용됐는지, 최근에 생성됐는지 체크하는 서버도 있습니다. 이렇게 체크하면 그 값 자체를 스크립트에 저장하고 몇 번이고 사용하는 것을 막을 수 있습니다.

### 12.3.2 허니팟 피하기

CSS를 활용해, 즉 id와 class를 읽어서 유용한 정보와 그렇지 않은 정보를 쉽게 구분할 수 있을 때도 있지만, 가끔 웹 스크레이퍼에서 CSS 때문에 문제가 생길 때도 있습니다. CSS를 써서 폼 필드를 숨겼다면, 사이트에 방문하는 일반적인 사용자에게는 그 필드가 보이지 않으니 작성하지 않을 거라고 봐야합니다. 그 필드가 값으로 채워졌다면 봇으로 판단하는 함정입니다.  

이런 방식은 비단 폼만이 아니라 링크나 이미지, 파일, 기타 사이트에 존재하는 무엇이든, 사용자에는 보이지 않고 봇은 읽을 수 있는 모든 것에 적용할 수 있습니다. 숨겨둔 링크로만 도달할 수 있는 페이지에 방문했다면 서버 쪽 스크립트로 사용자의 IP 주소를 차단하거나, 사용자를 로그아웃 시키거나, 다른 방법으로 이후 사이트에 접근하지 못하게 막는 것은 간단합니다. 사실 여러 비즈니스 모델이 이 개념에 따라 만들어졌습니다.  

http://pythonscraping.com/pages/itsatrap.html 예제 페이지입니다. 이 페이지에는 두 개의 링크가 있는데 하나는 CSS로 숨겼고 다른 하나는 보입니다. 그리고 숨긴 필드가 두 개 있는 폼이 들어 있습니다.

```html
<html><head>
	<title>A bot-proof form</title>
<style>
body {
	overflow-x:hidden;
}
.customHidden {
	position:absolute;
	right:50000px;
}
</style></head>

<body>
	<h2>A bot-proof form</h2>
<a href="http://pythonscraping.com/dontgohere" style="display:none;">Go here!</a>
<a href="http://pythonscraping.com">Click me!</a>
<form>
<input type="hidden" name="phone" value="valueShouldNotBeModified"><p>
<input type="text" name="email" class="customHidden" value="intentionallyBlank"></p><p>
<input type="text" name="firstName"></p><p>
<input type="text" name="lastName"></p><p>
<input type="submit" value="Submit"></p><p>
</p></form>

</body></html>
```

이 세 요소는 각각 다른 방법으로 사용자에게 숨겼습니다.

- 첫 번째 링크는 CSS `display:none` 속성으로 숨겼습니다.
- 전화번호 필드는 숨긴 필드입니다.
- 이메일 필드는 화면 오른쪽으로 50,000픽셀 이동하였고, 스크롤바를 숨겨서 모니터에서 보이지도, 이동하지도 못하게 했습니다.

셀레니움은 방문한 페이지를 실제로 렌더링하므로 페이지에 보이는 요소와 보이지 않는 요소를 구별할 수 있습니다. 페이지에 요소가 존재하는지는 `is_displayed()`함수로 알 수 있습니다.  

다음 코드는 앞에서 설명한 페이지를 가져와서 숨긴 링크와 필드가 있는지 찾습니다.

```python
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.PhantomJS()
driver.get("http://pythonscraping.com/pages/itsatrap.html")
links = driver.find_elements_by_tag_name("a")
for link in links:
    if not link.is_displayed():
        print("The link "+link.get_attribute("href")+" is a trap")

fields = driver.find_elements_by_tag_name("input")
for field in fields:
    if not field.is_displayed():
        print("Do not change value of "+field.get_attribute("name"))
```

셀레니움은 숨긴 링크와 필드를 찾고 다음의 결과를 출력합니다.

```
The link http://pythonscraping.com/dontgohere is a trap
Do not change value of phone
Do not change value of email
```

숨긴 링크에는 방문하지 않겠지만, 미리 생성된 값이 들어 있는 숨긴 필드도 전송하지 말아야 합니다. 요약하면, 숨긴 필드를 단순히 무시해서는 위험하며 반드시 매우 조심스헙게 조작해야 합니다.

## 12.4 사람처럼 보이기 위한 체크리스트

이 포스트를 비롯한 크롤링 포스트에는 스크레이퍼처럼 보이지 않고 사람처럼 보이기 위한 많은 정보가 들어 있습니다. 웹사이트에서 계속 차단당한다면 다음의 체크 리스트를 참고하면 해결할 수 있을 수도 있습니다.

- 먼저, 웹 서버에서 가져온 페이지가 비어 있거나, 있어야 할 정보가 없거나, 다른 어떤 형태로든 예상과 다르다면 사이트에서 페이지를 생성할 때 사용하는 자바스크립트가 싱핼되지 않았기 때문일 수 있습니다.  
[CHAP 10. 자바스크립트 스크레이핑](https://kimdoky.github.io/python/2017/08/13/crawling-book-chap10.html)를 참고하세요.
- 폼을 전송하거나 POST 요청을 보낸다면 웹사이트에서 받을 것이라 예상하는 정보를 모두, 정확한 형식으로 보내고 있는지 확인하세요. 크롬 개발자 도구의 'Network' 탭에서 사이트에 실제 보내지는 POST 요청을 보고 확인할 수 있습니다.
- 사이트에 로그인된 상태를 유지할 수 없거나 웹사이트가 이상한 '상태'의 동작을 보인다면 쿠키를 체크하세요. 쿠키가 각 페이지에서 정확히 유지되는지, 사이트에 요청을 보낼 때마다 쿠키가 함께 전송되는지 확인하세요.
- HTTP 에러를 겪고 있다면, 특히 403 Forbidden 에러를 겪고 있다면 웹사이트에서 당신의 IP 주소를 봇으로 판단했고 요청을 더는 받으려 하지 않기 때문일 수 있습니다. IP 주소가 블랙리스트에서 제거되길 기다리거나 새 IP 주소를 얻으세요.(가까운 스타벅스를 가세요.) 다시 차단당하지 않으려면 다음 사항을 유념하세요.
  - 스크레이퍼가 사이트를 너무 빨리 이동하지 않게 하세요. 지나치게 빠른 스크레이핑은 서버에 부담을 주고, 법적인 문제를 불러오고, 스크레이퍼가 블랙리스트에 기록되게 하는 1순위 원인입니다. 스크레이퍼에 지연 시간을 추가하고 밤에 실행하세요. 기억할 것은, 프로그램 작성이든 데이터 수집이든 계획 없이 달려들면 반드시 문제가 발생한다는 것입니다. 미리 계획하고, 문제의 원인을 처음부터 피하세요.
  - 헤더를 바꾸세요. 일부 사이트는 자신이 스크레이퍼라고 광고하는 것은 무엇이든 차단합니다. 헤더에 어떤 값을 써야 할지 모르겠다면 브라우저의 헤더를 복사하세요.
  > 브라우저에서 헤더 복사하기(크롬 기준)  
  1. 개발자 도구를 열고 Network를 선택  
  2. 좌측 Name에서 확인하고 싶은 파일 선택
  3. 우측 Header 탭 선택  
  ![]({{site.url}}/img/post/python/crawling/c12_4_get_header.png)
  
  - 일반적인 사람에게는 불가능한 것을 클릭하거나 접근하지 마세요.(허니팟입니다.)
  - 접근하기 정 어렵다면 웹사이트 관리자에게 연락해서 당신이 무엇을 하려는지 알리는 것도 하나의 방법입니다. 관리자의 이메일 주소는 보통 webmaster@domain.com 혹은 admin@domain.com 입니다. 스크레이퍼를 사용할 수 있는 권한을 요청하세요. 관리자도 사람이니 이런 방법이 통할 수도 있습니다.
