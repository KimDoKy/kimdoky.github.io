---
layout: post
section-type: post
title: crawling - P2. 고급 스크레이핑 _ cahp 9. 폼과 로그인 뚫기
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

### 9.5.1 HTTP 기본 접근 인증

## 9.6 기타 폼 문제
