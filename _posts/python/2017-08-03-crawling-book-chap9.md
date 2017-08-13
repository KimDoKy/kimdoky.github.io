---
layout: post
section-type: post
title: crawling - P2. 고급 스크레이핑 _ chap 9. 폼과 로그인 뚫기
category: python
tags: [ 'python' ]
---

웹 스크레이핑을 하면 로그인해야만 얻을 수 있는 정보들이 있습니다. 웹은 점점 더 상호작용과 소셜 미디어, 사용자가 만든 콘텐츠 쪽으로 이동하고 있습니다. 폼과 로그인은 이런 타입의 사이트에서 필수적인 부분이고, 이것 없이 사이트를 유지하기는 거의 불가능합니다. 하지만 비교적 쉽게 대응할 수 있습니다.  

이전 섹션들에서는 대부분 HTTP GET을 써서 정보를 요청했습니다. 이번 섹션에서는 웹 서버에서 저장하고 분석할 정보를 보내는 POST 메서드에 집중합니다.  

폼은 기본적으로 웹 서버가 이해하고 사용할 수 있는 POST 요청을 사용자가 보낼 수 있게 하는 수단입니다. 웹사이트에 있는 링크 태그는 사용자가 GET 요청을 형식에 맞게 보낼 수 있도록 돕습니다. 마찬가지로, HTML 폼은 POST 요청을 형식에 맞게 보낼 수 있도록 돕습니다. 따라서 코딩을 조금만 하면 POST 요청을 직접 만들어 스크레이퍼가 전송하게 할 수 있습니다.

## 9.1 파이썬 requests 라이브러리

urllib과 기본적으로 GET 요청을 할 수 있는 것 이상을 해야 할 때가 오면 파이썬 내장 라이브러리 말소 다른 것을 찾아보는게 낫습니다.  

requests 라이브러리는 복잡한 HTTP 요청과 쿠키, 헤더를 잘 처리하며 그외에도 많은 기능이 있습니다.  

라이브러리를 만든 케네스 라이츠는 파이써의 내장 라이브러리에 대해 이렇게 말했습니다.

> 파이썬의 표준 urllib2 모듈은 필요한 HTTP 기능을 거의 제공하지만, 이제 너무 뒤떨어졌습니다. 이 API는 과거에, 과거의 웹을 위해 만들어졌습니다. urllib2를 사용하려면 정말 단순한 일 하나만 하려 해도 할 일이 너무 많고, 심지어 메서드 오버라이드까지 필요할 때도 있습니다.  
API를 이렇게 만들면 안됩니다. 파이썬과 어울리지 않습니다.

requests 라이브러리 역시 pip 로 설치하면 됩니다.

## 9.2 기본적인 폼 전송

대부분의 웹 폼은 HTML 필드와 전송 버튼, 폼을 실제 처리하는 '액션' 페이지로 구성됩니다. HTML 필드는 보통 텍스트 필드이지만, 파일 업로드같은 텍스트가 아닌 필드도 있습니다.  

유명 사이트 대부분 robots.txt 파일에서 로그인 폼에 접근하는 걸 거부하므로, 웹 스크레이퍼 교재는 http://pythonscraping.com/files/form.html 에 테스트할 수 있는 몇가지 폼과 로그인페이지를 준비해두었습니다.

이 폼은 다음과 같이 구성되어 있습니다.

```HTML
<form method="post" action="processing.php">
First name: <input type="text" name="firstname"><br>
Last name: <input type="text" name="lastname"><br>
<input type="submit" value="Submit">
</form>
```

여기서 두 가지를 눈여겨 봐야합니다.  

먼저, 입력 필드 두 개의 이름이 각각 firstname과 lastname입니다. 이들 필드 이름은 폼을 전송할 때 POST로 서버에 전달될 변수 이름입니다. 폼의 동작을 흉내 내려 한다면 변수 이름을 정확히 맞춰야 합니다.  

둘째, 폼이 실제로 동작하는 곳은 http://pythonscraping.com/files/processing.php 입니다. 폼에 post 요청을 보낼 때는 폼 자체가 있는 페이지가 아니라, processing.php에 보내야 합니다. HTML 폼의 목적은 웹사이트 방문자가 실제 동작을 수행하는 페이지에 올바른 형식을 요청을 보내도록 돕는 것입니다. 요청 형식 자체를 연구하려는 것이 아니라면 폼이 존재하는 페이지에는 구애받을 필요 없습니다.  

requests 라이브러리로 폼을 보내는 건 임포트 문과 콘텐츠 출력을 포함해 단 4 줄이면 됩니다.  

```python
import requests
params = {'firstname': 'Doky', 'lastname': 'Kim'}
r = requests.post("http://pythonscraping.com/files/processing.php", data=params)
print(r.text)
```

폼을 전송하면 페이지 콘텐츠가 반환됩니다.

```
Hello there, Doky Kim!
```

이 코드는 인터넷에 존재하는 단순한 폼 상당수에 적용할 수 있습니다. 예를 들어 오라일리의 미디어 소식지 구독 폼은 다음과 같습니다.

```HTML
<form action="http://post.oreilly.com/client/o/oreilly/forms/quicksignup.cgi" id="example_form2" method="POST">
  <input name="client_token" type="hidden" value="oreilly" />
  <input name="subscribe" type="hidden" value="optin" />
  <input name="success_url" type="hidden" value="http://oreilly.com/store/newsletter-thankyou.html" />
  <input name="error_url" type="hidden" value="http://oreilly.com/store/newsletter-signup-error.html" />
  <input name="topic-or-dod" type="hidden" value="1" />
  <input name="source" type="hidden" value="orm-home-t1-dotd" />
  <fieldset>
    <input class="email_address long" maxlength="200" name="email_addr" size="25" type="text" value="Enter your email here" />
    <button alt="Join" class="skinny" name="submit" onclick="return addClickTracking('orm', 'ebook', 'rightrail', 'dod');" value="submit">Join</button>
  </fieldset>
</form>
```

여기서 두 가지만 기억하면 됩니다.

- 데이터를 전송할 필드 이름(여기서는 email_address)
- 폼 자체의 action 속성, 즉 폼을 실제 처리하는 페이지(여기서는 http://post.oreilly.com/client/o/oreilly/forms/quicksignup.cgi)

```python
import requests

params = {'email_addr' : 'makingfunk0@gmail.com'}
url = "http://post.oreilly.com/client/o/oreilly/forms/quicksignup.cgi"
r = requests.post(url, data=params)
print(r.text)
```

오레일리의 메일링 리스트에 실제로 가입하려면 이 코드가 반환하는 폼을 다시 작성해야 하지만, 그 폼에도 같은 개념이 적용됩니다.

## 9.3 라디오 버튼, 체크박스, 기타 필드

HTML 표준에는 폼에 쓸 수 있는 입력 필드가 여러가지 있습니다. 라디오 버튼, 체크박스, 셀렉트 박스 등입니다. HTML5에서는 범위 입력 필드인 슬라이더, 이메일, 날짜 등이 더 추가 됐습니다. 자바스크립트를 사용하면 쓸 수 있는 필드가 무한히 늘어납니다. 달력, 색깔 선택기 등 개발자가 만들기 나름입니다.  

폼 필드가 다양하고 복잡하더라도 신경 쓸 것은 필드 이름과 값 뿐입니다. 필드 이름은 소스 코드에서 name 속성을 보면 됩니다. 값은 조금 복잡하데, 폼을 전송하기 직전에 자바스크립트를 써서 만들 수도 있기 때문입니다. 예를 들어 고급 폼 필드에 속하는 색깔 선택기는 #F03030 같은 값을 가질 수 있습니다.  

입력 필드의 값 형식을 확신할 수 없다면 브라우저가 사이트와 주고받는 GET과 POST 요청을 추척하는 여러 도구를 쓸 수 있습니다. GET 요청을 추적하는 가장 좋은 방법은 그냥 사이트의 URL을 읽는 것입니다.

```
http://domainname.com?thing1=foo?thing2=bar
```
위와 같은 형식의 URL이 있다면 이에 대응하는 폼은 아래와 같을 겁니다.

```html
<form method="GET" action="someProcessor.php">
  <input type="someCrazyInputType" name="thing1" value="foo" />
  <input type="anotherCrazyInputType" name="thing2" value="bar" />
  <input type="submit" value="submit" />
</form>
```

이때 파이썬 매개변수 객체는 이렇게 만들면 됩니다.

```
{'thing1':'foo', 'thing2':'bar'}
```

POST 폼은 브라우저의 개발자 도구를 보는 겁니다.

![]({{site.url}}/img/post/python/crawling/c9_3.png)

크롬 개발자는 F12를 눌러 접근할 수 있습니다.
> (맥은 opt+cmd+i)

## 9.4 파일과 이미지 전송

인터넷에서는 파일 업로드는 자주 사용하지만, 웹 스크레이핑에서는 자주 사용하지는 않습니다. 하지만 알아둬서 나쁠건 없으니까요.

http://pythonscraping.com/files/form2.html 에 파일 업로드를 연습하는 폼이 준비되어 있습니다.

마크업은 아래와 같습니다.

```html
<form action="processing2.php" method="post" enctype="multipart/form-data">
Submit a jpg, png, or gif: <input type="file" name="image"><br>
<input type="submit" value="Upload File">
</form>
```

`<input>` 태그의 type 속성이 file 인 것을 제외하면 텍스트 기반 폼과 같습니다. requests 라이브러리를 사용하는 방법도 비슷합니다.

```python
import requests

files = {'uploadFile': open('../files/docker-logo.png', 'rb')}
r = requests.post("http://pythonscraping.com/pages/processing2.php", files=files)
print(r.text)
```

이번에는 문자열이 아니라 open 함수가 반환한 파이썬 File 객체를 보냈습니다.(필드이름은 uploadFile 입니다.) 이 예제에서 보낸 파일은 이 코드를 기준으로 상대 경로(../files/Python-logo.png)에 있는 이미지입니다.

실행결과입니다.

```
The file docker-logo.png has been uploaded. <a href="/pages/uploads/docker-logo.png">Link</a>
```

## 9.5 로그인과 쿠키처리

지금까지는 사이트에 정보를 전송하는 걸 허용하거나, 폼을 넘어가면 바로 필요한 정보를 제공하는 폼을 다루었습니다. 하지만 '로그인 상태를 유지합니다' 같은 기능을 제공하는 로그인 폼과는 다릅니다.  

최신 웹사이트는 대부분 쿠키를 사용해서 누가 로그인 했는지 추적합니다. 일단 사이트에서 로그인을 요청을 인증하면, 사이트는 브라우저에 쿠키를 저장합니다. 이런 쿠키에는 보통 서버에서 생성한 토큰, 만료일, 추적(tracking) 정보가 들어 있습니다. 사이트는 나중에 이 쿠키를 사이트에 머물러 방문하는 각 페이지에서 일종의 인증 증거로 사용합니다.

쿠키는 웹 개발자들에게는 환영할 만한 것이지만, 웹 스크레이퍼에는 문제가 됩니다. 웹 스크레이퍼로 언제든 로그인할 수 있지만, 서버가 반환하는 쿠키를 활용하지 못하면 웹사이트는 로그인하지 않았다고 판단할 것입니다.  

스크레이퍼 교재에서는 http://pythonscraping.com/pages/cookies/login.html 에 단순한 로그인 폼을 만들어두었습니다. 사용자 이름은 아무거나 써도 되지만, 비밀번호는 password 이어야 합니다.  

이 폼을 처리하는 페이지는 http://pythonscraping.com/pages/cookies/welcome.php 이고, 이 페이지에는 '메인 사이트' 페이지인 http://pythonscraping.com/pages/cookies/profile.php 를 가리키는 링크가 있습니다.  

로그인하지 않고 환영 페이지나 프로필 페이지에 접근하려 하면 에러 메시지와 함께 로그인하라는 안내가 표시됩니다. 프로필 페이지에서는 로그인 페이지에서 브라우저 쿠키를 만들었는지 체크합니다.

requests 라이브러리를 사용하면 쿠키 추적도 쉽습니다.


```python
import requests

params = {'username': 'Doky', 'password': 'password'}
r = requests.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print("Cookie is set to:")
print(r.cookies.get_dict())
print("---------")
print("Going to profile page_")
r = requests.get("http://pythonscraping.com/pages/cookies/profile.php", cookies=r.cookies)
print(r.text)
```

실행 결과입니다.

```
Cookie is set to:
{'username': 'Doky', 'loggedin': '1'}
---------
Going to profile page_
Hey Doky! Looks like you're still logged into the site!
```

이 코드에서는 로그인 폼을 처리하는 환영 페이지에 로그인 매개변수를 보냅니다. 마지막 요청 결과에서 쿠키를 가져와서 출력으로 확인하고, cookies 매개변수를 통해 그 쿠키를 프로필 페이지에 보냅니다.  

이런 방법은 단순한 상황에는 잘 동작하지만, 일부 복잡한 사이트는 경고 없이 자주 쿠키를 수정하기도 하며, 때로는 쿠키에 대해 생각하지 못하고 코드를 작성할 수도 있습니다. requests 라이브러리의 sessino 함수로 이런 문제를 해결할 수 있습니다.


```python
import requests

session = requests.Session()

params = {'username': 'Doky', 'password': 'password'}
s = session.post("http://pythonscraping.com/pages/cookies/welcome.php", params)
print("Cookie is set to:")
print(s.cookies.get_dict())
print("----------")
print("Going to profile page_")
s = session.get("http://pythonscraping.com/pages/cookies/profile.php")
print(s.text)
```

여기서는 requests.Session() 로 가져온 세션 객체나 쿠키나 헤더, 심지어
HTTPAdapters 같은 HTTP 에서 동작하는 프로토콜에 관한 정보까지 세션 정보를 관리합니다.  

requests 라이브러리는 프로그래머가 이거저거 생각하거나 코드를 작성할 필요 없이 모든 일을 매끄럽게 처리하는 완성도 면에서는 셀레니움(Selenium)외에는 비교할 만한 대상이 없을 정도입니다. requests 라이브러리가 모든 일을 처리하도록 내버려두고 싶겠지만, 웹 스크레이퍼를 만들 때는 항상 쿠키가 어떤 모양이고 무슨 일을 하는지 파악해야 합니다. 이걸 잘 파악하면 디버깅 시간이나, 사이트가 이상하게 동작하는 이유를 파악하는 시간이 훨씬 짧아집니다.

### 9.5.1 HTTP 기본 접근 인증

쿠키가 등장하기 전에 널리 쓰이던 로그인 처리 방법은 **HTTP 기본 접근 인증(basic access authentication)** 입니다. 가끔, 특히 높은 보안이 중요한 사이트나 기업 사이트 중에는 API와 함께 이 방식을 쓰는 곳도 있습니다. http://pythonscraping.com/pages/auth/login.php 페이지는 이런 타입의 인증을 사용합니다.

![]({{site.url}}/img/post/python/crawling/c9_5.png)
> 기본 접근 인증을 사용하는 페이지에 접근하려면 반드시 사용자 이름과 비밀번호를 입력해야 합니다.

이 예제는 사용자 이름은 무엇이든 상관없지만 비밀번호는 password 이어야 합니다.  

requests 라이브러리에는 HTTP 인증을 처리하도록 특별히 설계된 auth 모듈이 있습니다.

```python
import requests
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('doky', 'password')
r = requests.post(url="http://pythonscraping.com/pages/auth/login.php", auth=auth)
print(r.text)
```

일반적인 POST 요청처럼 보이겠지만 이번에는 HTTPBasicAuth 객체를 auth 매개변수로 요청을 넣었습니다. 결과 텍스트는 사용자 이름과 비밀번호로 보호된 페이지입니다.(요청이 실패하면 접근 거부 페이지나 나타납니다.)

## 9.6 기타 폼 문제

웹 폼은 온갖 악의적인 봇들이 넘쳐납니다. 봇이 사용자 계정을 만들고, 귀중한 서버 시간을 낭비하고, 블로그에 스팸을 뿌려댑니다. 따라서 최신 웹사이트의 HTML 폼에는 즉시 드러나지 않는 보안 기능이 포함될 때가 많습니다.  

자동 가입 방지 문자(CAPTCHA)는 챕터 11에서 다룹니다.  
허니팟과 숨긴 필드, 기타 웹사이트에서 폼을 보호하기 위해 채용하는 보안 수단은 챕터 12에서 다룹니다.
