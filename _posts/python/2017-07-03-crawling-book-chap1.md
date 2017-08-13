---
layout: post
section-type: post
title: crawling - P1.스크레이퍼 제작 _ chap 1. 첫 번째 웹 스크레이퍼
category: python
tags: [ 'python' ]
---

![]({{site.url}}/img/post/python/crawling/animal.jpg)

오늘부터 배워볼 동물은 '사바나천산갑'입니다.  
(파이썬으로 웹 크롤러 만들기(Web Scraping with Python))  

아직 갈 길은 멀지만, 한 걸음 한 걸음 가다보면 내공이 쌓이겠죠.

---

# Part 1. 스크레이퍼 제작

Part 1에서는 웹 스크레이핑의 기본에 대해 다룹니다. 파이썬으로 웹 서버에 정보를 요청하는 법, 서버 응답을 처리하는 기본적인 방법, 웹 사이트와 자동적으로 통신하는 법이 주된 내용입니다.

- 도메인 이름을 받고 HTML 데이터를 가져옴
- 데이테를 파싱해 원하는 정보를 얻음
- 원하는 정보를 저장함
- 필요하다면 다른 페이지에서 이 과정을 반복함

## Chapter 1 - 첫 번째 웹 스크레이퍼

브라우저의 도움 없이 데이터 구조를 파악하고 해석하는 법을 다룹니다.  
웹 서버에 특정 페이지를 요청하는 GET 요청을 보내고, 그 페이지의 HTML 결과를 얻고, 원하는 콘텐츠를 뽑아내는 데이터 추출의 기본을 다룹니다.  

### 1.1 연결

컴퓨터가 다른 컴퓨터에 연결할 때 일어나는 일들입니다. (ex.밥이 앨리스의 서버에 연결합니다.)

1. 밥의 컴퓨터는 1, 0 으로 된 비트 스트림을 보냅니다. 각 비트는 전압으로 구별됩니다. 이들 비트는 정보를 구성하며, 헤더와 바디도 그런 정보에 포함됩니다. 헤더에는 바로 다음 목표인 밥의 라우터 MAC 주소와 최종 목표인 앨리스의 IP 주소가 들어 있습니다. 바디에는 밥이 앨리스의 서버 애플리케이션에 요청하는 내용이 들어 있습니다.

2. 밥의 라우터는 이들 비트를 받아 밥의 MAC 주소에서 앨리스의 IP 주소로 가는 패킷으로 해석합니다. 밥의 라우터의 고유 IP 주소를 패킷에 '발신자(from)' 주소로 기록한 다음 밥의 라우터는 이 패킷을 인터넷에 보냅니다.

3. 밥의 패킷은 여러 중간 서버를 거치며 이동합니다. 중간 서버들은 정확한 물리적 경로 또는 유선 경로를 거쳐 앨리스의 서버를 향해 패킷을 보냅니다.

4. 앨리스의 서버는 자신의 IP 주소에서 그 패킷을 받습니다.

5. 앨리스의 서버는 패킷 헤더에서 포트 번호(웹 애플리케이션에서는 거의 항상 80입니다. IP 주소가 거리 주소라면 포트 번호는 패킷 데이터의 아파트 동수라 생각하면 됩니다.)를 찾고 적절한 애플리케이션, 즉 웹 서버 애플리케이션에 보냅니다.

6. 웹 서버 애플리케이션은 서버 프로세서에서 데이터 스트림을 받습니다. 이 데이터에는 다음과 같은 정보가 들어있습니다.

- 이 요청은 GET 요청임
- 요청하는 파일은 index.html임

7. 웹 서버는 해당하는 HTML 파일을 찾고 새 패킷으로 묶어서 자신의 라우터를 통해 밥의 컴퓨터로 전송합니다. 웹 서버가 보낸 패킷은 밥이 보낸 패킷과 같은 과정을 거쳐 밥의 컴퓨터에 도달합니다.

이 과정에서는 웹 브라우저는 개입하지 않습니다. 웹 브라우저는 이들 패킷을 만들고, 보내고, 돌아온 데이터를 해석해 사진, 소리, 비디오, 텍스트 등으로 표현하는 유용한 애플리케이션입니다. 하지만 웹 브라우저 역시 코드일 뿐, 코드는 떼어내서 기본 구성 요소로 나누고, 다시 만들고, 재사용하고, 원하는 무엇이든 바꿀 수 있습니다. 웹 브라우저는 프로세서에 명령을 내려 데이터를 애플리케이션에 보내서 유/무선 인터페이스로 처리할 수 있습니다. 그러한 일을 하는 라이브러리는 파이썬에서도 존재합니다.



```python
from  urllib.request import urlopen
html = urlopen("http://pythonscraping.com/pages/page1.html")
print(html.read())
```

```
python scrapetest.py
```

```
~/Git/Study/crawling/web_scraping(master*) » python scrapetest.py
b'<html>\n<head>\n<title>A Useful Page</title>\n</head>\n<body>\n<h1>An Interesting Title</h1>\n<div>\nLorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n</div>\n</body>\n</html>\n'
```

웹 페이지에는 여러 가지 지원 파일이 연결되어 있습니다. 이미지 파일, 자바 스크립트, CSS, 기타 요청한 페이지에 연결된 다른 컨텐츠입니다. 웹 브라우저는 웹 페이지를 해석하다 `<img src="cuteKitten.jpg">` 같은 테그를 만나면, 페이지를 완전히 렌더링하기 위해 서버에 다시 요청을 보내 cuteKitten.jpg 파일의 데이터를 받습니다.

```
from urllib.request import urlopen
```
`urllib` 라이브러리에서 파이썬 모듈 `request`를 읽고 `urllib` 함수 하나만 임포트합니다.

`urllib`은 표준 파이썬 라이브러리이므로 따로 설치할 필요는 없습니다. `urllib`에는 웹을 통해 데이터를 요청하는 함수, 쿠키를 처리하는 함수, 헤더나 유저 에이전트 같은 메타데이터를 바꾸는 함수 등이 있습니다. [urllib Doc](https://docs.python.org/3/library/urllib.html){:target="`_`blank"}

`urlopen`는 네트워크를 통해 원격 객체를 읽습니다. `urlopen`은 HTML 파일이나 이미지 파일, 기타 파일 스트림을 쉽게 열 수 있는 범용적인 라이브러리입니다.

### 1.2 BeautifulSoup 소개

BeautifulSoup는 잘못된 HTML을 수정하여 쉽게 탐색할 수 있는 XML 형식의 파이썬 객체이므로 변환이 골치 아픈 웹을 탐색할 때 유용합니다.

### 1.2.1 BeautifulSoup 설치

```
pip install beautifulsoup4
```

#### 설치 확인

```
python
>>> from bs4 import BeautifulSoup
```
임포트시 에러가 없어야 정상적으로 설치가 된 것입니다.

> 가상 환경으로 라이브러리 분리하세요.
```
pyenv virtualenv 파이썬버전 가상환경이름
pyenv local 가상환경이름
```

### 1.2.2 BeautifulSoup 실행

```python
from  urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://pythonscraping.com/pages/page1.html")
bsObj = BeautifulSoup(html.read(), "html.parser")
print(bsObj.h1)
```

출력 결과입니다.

```
~/Git/Study/crawling/web_scraping(master*) » python scrapetest.py
<h1>An Interesting Title</h1>
```

`urlopen` 라이브러리를 임포트하고 `html.read()`를 호출해서 페이지의 HTML 콘텐츠를 얻었습니다.

페이지에서 추출한 `<h1>` 태그는 BeautifulSoup 객체 구조(html-> body -> h1)에서 두 단계만큼 중첩되어 있습니다. 하지만 객체에서 가져올 때는 h1 태그를 직접 가져옵니다.

```
bsObj.h1
bsObj.html.body.h1
bsObj.body.h1
bsObj.html.h1
# 모든 결과는 같습니다.
```

BeautifulSoup 라이브러리는 단순하고 강력한 도구입니다. 원하는 정보를 둘러싼, 혹은 그 주변에 태그가 있기만 하면 HTML(XML) 파일에서 어떤 정보든 추출할 수 있습니다.

### 1.2.3 신뢰할 수 있는 연결

웹은 엉망입니다. 웹 스크레이핑에서 가장 좌절스러운 것은 스크레이퍼를 실행하고 모든 데이터가 DB에 저장될 것을 기대하였지만, 예상치 못한 데이터 형식에 부딪혀 에러를 일으키고 멈추는 것입니다.
예외 처리를 다룹니다.

```
html = urlopen("http://pythonscraping.com/pages/page1.html")
```
이 코드에서 두 가지 문제가 생길 수 있습니다.

- 페이지를 찾을 수 없거나, URL 해석에서 에러가 생긴 경우
- 서버를 찾을 수 없는 경우

첫 번째 상황에서는 HTTP 에러가 반환될 것입니다. ("404 Page Not Found", "500 Internal Server Error" 등)

```
from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup

try:
    html = urlopen("http://pythonscraping.com/pages/page1.html")
except HTTPError as e:
    print(e)
    # null을 반환하거나, break 문을 실행하거나, 다른 방법을 사용
else:
    # 프로그램을 계속 실행합니다. except 절에서 break나 return를 사용했다면
    # else 절은 필요 없습니다.
```
이제 HTTP 에러 코드가 반환되면 프로그램은 에러를 출력하고 else 문은 실행하지 않습니다.  
BeautifulSoup 객체에 들어 있는 태그에 접근할 때마다 그 태그가 실제 존재하는지 체크하는 것이 좋습니다. 존재하지 않는 태그에 접근을 시도하면 BeautifulSoup는 None 객체를 반환합니다. 문제는 None 객체 자체에 태그가 있다고 가정하고 그 태그에 접근하려 하면 AttributeError 가 일어납니다.

다음 코드에서는 nonExistentTag는 존재한다고 가정합니다.
```python
print(bsObj.nonExistentTag.someTag)
```
위 코드는 다음과 같은 예외를 일으킵니다.

```
AttributeError: 'NoneType' object has no attribute 'someTag'
```

가장 쉬운 대응 방법은 명시적으로 체크하는 것입니다.

```python
try:
    badContent = bsObj.nonExistentTag.anotherTag
except AttributeError as e:
    print("Tag was not found")
else:
    if badContent == None:
        print("Tag was not found")
    else:
        print(badContent)
```

이렇게 가능한 에러를 모두 체크하고 처리하는게 처음에는 지겨워보이지만, 코드를 조금만 수정하면 더 쉽게 읽을 수 있게 만들 수 있습니다.

```python
from urllib.request import urlopen
from urllib.request import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), "html.parser")
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title

title = getTitle("http://pythonscraping.com/pages/page1.html")
if title == None:
    print("Title could not be found")
else:
    print(title)
```

위 코드는 페이지 타이틀을 반환하거나, 어떤 문제가 있으면 None 객체를 반환하는 getTitle 함수를 만듭니다. getTitle 내부에서는 HTTPError를 체크하고 BeautifulSoup 행 두 개를 try 문으로 캡슐화합니다. 이 두 행중 어느 행이라도 AttributeError를 일으킬 수 있습니다.

> 서버가 존재하지 않으면 html은 None 객체이고 `html.read()`가 AttributeError를 일으킵니다. try 문 하나에 원하는 만큼 여러 행을 넣을 수도 있고, AttributeError를 일으킬 수 있는 별도의 함수도 어느 시점에서든지 호출할 수 있습니다.

스크레이퍼를 만들 때는 코드의 전반적 패턴에 대해 생각해야 예외도 처리하고 읽기도 쉽게 만들 수 있습니다. 코드를 많이 재사용하고 싶을때는 getSiteHTML이나 getTitle 같은 범용 함수를 만들고 여기에 예외처리를 철저히 만들어두면 믿을 수 있는 웹 스크레이퍼를 쉽게 만들 수 있습니다.
