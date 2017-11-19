---
layout: post
section-type: post
title: Python Library - chap 10. HTML과 XML 다루기 - 3. 간편한 HTML parser 이용하기
category: python
tags: [ 'python' ]
---

`beautifulsoup4` 패키지를 다룹니다. Web 스크래핑에 자주 사용됩니다.

## beautifulsoup4 설치

```
$ pip install beautifulsoup4
```

## HTML 내 용소 정보 구하기

```python
>>> from bs4 import BeautifulSoup
>>> from urllib import request
>>> from lxml import html
>>> html = BeautifulSoup(request.urlopen('http://www.python.org'))
>>> html.title  # title 요소 얻기
<title>Welcome to Python.org</title>

>>> html.title.text  # title 요소의 내용 얻기
'Welcome to Python.org'

>>> html.h1  # h1 요소 얻기
<h1 class="site-headline">
<a href="/"><img alt="python™" class="python-logo" src="/static/img/python-logo.png"/></a>
</h1>

>>> html.find('h1')  # html.h1과 마찬가지로 h1 요소 얻기
<h1 class="site-headline">
<a href="/"><img alt="python™" class="python-logo" src="/static/img/python-logo.png"/></a>
</h1>

>>> html.h1.img  # h1 요소의 자식 요소인 img 요소 얻기
<img alt="python™" class="python-logo" src="/static/img/python-logo.png"/>

>>> html.h1.img.attrs  # img 요소의 속성과 값 얻기
{'class': ['python-logo'], 'src': '/static/img/python-logo.png', 'alt': 'python™'}

>>> html.h1.img['src']  # img 요소의 src 속성값
'/static/img/python-logo.png'

>>> html.find(id='back-to-top-1')  # id 속성값으로 요소 검색
<a class="jump-link" href="#python-network" id="back-to-top-1"><span aria-hidden="true" class="icon-arrow-up"><span>▲</span></span> Back to Top</a>

>>> html.find('li', attrs={'class':'shop-meta'})  # 속성 이름과 값을 dict으로 지정하여 검색
<li class="shop-meta ">
<a href="/community/" title="Python Community">Community</a>
</li>
```

### bs4.BeautifulSoup 클래스

형식 | class bs4.BeautifulSoup(self, markup='', features=None, builder=None, parse_only=None, from_encoding=None, \**kwargs)
---|---
설명 | HTML을 해석한다.
인수 | markup - 해석 대상 HTML <br> features - parser를 지정한다.
반환값 | BeautifulSoup 객체

features에는 'xml', 'html5lib', 'html.parser'를 지정할 수 있습니다.(미리 해당 패키지를 설치해야 합니다.)  

BeautifulSoup 객체는 html.h1.img처럼, 요소를 거슬러 올라가 목적 정보를 탐색할 수 있습니다. find() 메서드를 사용해서 요소를 탐색할 수도 있습니다.  

요소의 내용은 `.text`로 얻습니다. 요소 속성 정보는 Tag 갹체의 dict으로 존재합니다. 속성 이름과 값, 한쌍을 attrs로 취득할 수 있습니ㅏㄷ. 속성 이름을 지정하여 그 값을 직접 취득하려면 img['src']와 같이 지정해야 합니다.

### BeautifulSoup.find()

형식 | BeautifulSoup.find(name=None, attrs={}, recursive=True, text=None, \**kwargs)
---|---
설명 | 요소를 탐색하여 맨 처음 발견된 하나를 얻는다.
인수 | name -  요소 이름을 검색 조건으로 한다. <br> attrs - 요소의 속성 이름과 값을 검색 조건으로 한다. dict형으로 작성한다. <br> recursive -  False를 지정하면 바로 아래 자식 요소만 대상이 된다. <br> text - 요소의 내용(시작 태그와 종료 태그 사이의 텍스트)을 검색 조건으로 한다.
반환값 | Tag 객체

요소 이름 이외의 정보까지 검색하려면 find() 메소드의 인수로 요소의 속성 정보를 부여합니다. id 속성값으로 요소를 특정하는 경우, find(id='ID 이름')과 같이 지정합니다. class 속성은 find(class_='class 이름')과 같이 하면 조건으로 쓸 수 있습니다. class_는 Python의 예약어와 충돌을 피하고자 밑줄이 붙어 있습니다.  

find('요소 이름', attrs={'속성 이름':'값'})과 같이 지정하면 조건을 더 좁힐 수 있습니다. 속성 이름과 값의 한 쌍을 여러 개 작성하면 AND 검색이 됩니다. name 인수는 생략이 가능합니다.

### HTML 내의 링크 URL을 모두 추출하기
여러 개의 요소를 구할 땐 `find_all()` 메서드를 이용합니다.

### URL 목록 추출하기

```python
>>> import re
>>> html = BeautifulSoup(request.urlopen('https://www.python.org'))
>>> url_list = html.find_all('a')
>>> for url in url_list:
...     print(url['href'])
...
#content
#python-network
/
/psf-landing/
https://docs.python.org
...

>>> docs_list = html.find_all(href=re.compile('^http(s)?://docs'), limit=2)
>>> for doc in docs_list:
...     print(doc['href'])
...
https://docs.python.org
https://docs.python.org/3/license.html
```

### BeautifulSoup.find_all()

형식 | BeautifulSoup.find_all(name=None, attrs={}, recursive=True, text=None, limit=None, \**kwargs)
---|---
설명 | 요소를 탐색하여 조건에 일치하는 모두를 구한다.
인수 | name -  요소 이름을 검색 조건으로 한다. <br> attrs - 요소의 속성 이름과 값을 검색 조건으로 한다. dict형으로 작성한다. <br> recursive -  False를 지정하면 바로 아래 자식 요소만 대상이 된다. <br> text - 요소의 내용(시작 태그와 종료 태그 사이의 텍스트)을 검색 조건으로 한다. <br> limit - 지정한 수만큼 요소가 발견되면 검색을 종료한다.
반환값 | Tag 객체의 리스트

## 텍스트만 추출하기

```python
>>> html = BeautifulSoup(request.urlopen('http://www.python.org'))
>>> tag = html.find('div', attrs={'id':'nojs'})
>>> tag
<div class="do-not-print" id="nojs">
<p><strong>Notice:</strong> While Javascript is not essential for this website, your interaction with the content will be limited. Please turn Javascript on for the full experience. </p>
</div>

>>> print(tag.get_text(strip=True))
Notice:While Javascript is not essential for this website, your interaction with the content will be limited. Please turn Javascript on for the full experience.

>>> print(tag.get_text(separator='-- '))

-- Notice:--  While Javascript is not essential for this website, your interaction with the content will be limited. Please turn Javascript on for the full experience. --
```

### BeautifulSoup.get_text()

형식 | BeautifulSoup.get_text(separator='', strip=False, types=(<class 'bs4.element.NavigableString'>,<class 'bs4.element.CData'>))
---|---
설명 | 트리로부터 텍스트 부분을 추출한다.
인수 | separator - 태그로 잘려 있던 위치에 지정한 문자열을 삽입한다. <br> strip - True로 지정하면 빈 행을 제외한다.
반환값 | 추출한 문자열

## HTML을 정형화하여 출력하기
prettify()를 사용하면 HTML을 다둠어 출력합니다.

```python
>>> print(html.h1)  # 일반 출력
<h1 class="site-headline">
<a href="/"><img alt="python™" class="python-logo" src="/static/img/python-logo.png"/></a>
</h1>

>>> print(html.h1.prettify())  # prettify() 사용
<h1 class="site-headline">
 <a href="/">
  <img alt="python™" class="python-logo" src="/static/img/python-logo.png"/>
 </a>
</h1>

>>> print(html.h1.a.prettify(formatter='html'))  # 특수 문자를 엔티티 참조로 출력
<a href="/">
 <img alt="python&trade;" class="python-logo" src="/static/img/python-logo.png"/>
</a>
```


## HTML 수정하기

### HTML 수정에 자주 이용하는 메서드

형식 | 설명
---|---
insert(position, new_child) | position 위치에 new_child 내용을 삽입한다.
replace_with(new_tag) | 태그를  new_tag로 대체한다.
clear() | 요소의 내용을 삭제한다. 태그는 남는다.
decompose() | 트리에서 태그를 제거한다. 태그의 자식 요소도 제거된다.
extract() | 태그를 트리에서 추출하고 제거한다. 제거한 테그가 반환된다.
wrap(wrapper_tag) | 태그를 wrapper_tag로 래핑한다.

### HTML 수정에 자주 이용하는 메서드 사용 예

```python
>>> html = BeautifulSoup(request.urlopen('https://www.python.org'))
>>> html.h1  # h1 요소를 얻음
<h1 class="site-headline">
<a href="/"><img alt="python™" class="python-logo" src="/static/img/python-logo.png"/></a>
</h1>

>>> html.h1.insert(0, 'ham')
>>> html.h1  # h1 시작 태그 바로 뒤에 문자열 ham이 삽입됨
<h1 class="site-headline">ham
<a href="/"><img alt="python™" class="python-logo" src="/static/img/python-logo.png"/></a>
</h1>

>>> html.h1.insert(3, 'egg')  # position 값에 따라 삽입 위치가 달라짐
>>> html.h1  # h1 종료 태그 직전에 문자열 egg가 삽입된
<h1 class="site-headline">ham
<a href="/"><img alt="python™" class="python-logo" src="/static/img/python-logo.png"/></a>egg
</h1>

>>> new_tag = html.new_tag('span')  # 태그 span 생성
>>> new_tag.string = 'ham egg'  # span의 내용을 설정함
>>> html.h1.img.replace_with(new_tag)  # img 태그를 대체함
<img alt="python™" class="python-logo" src="/static/img/python-logo.png"/>

>>> html.h1  # img가 span으로 대체되어 있음
<h1 class="site-headline">ham
<a href="/"><span>ham egg</span></a>egg
</h1>

>>> html.h1.span.clear()  # span 요소의 내용을 삭제함
>>> html.h1
<h1 class="site-headline">ham
<a href="/"><span></span></a>egg
</h1>

>>> html.h1.span.decompose()  # span 태그를 제거함
>>> html.h1
<h1 class="site-headline">ham
<a href="/"></a>egg
</h1>

>>> html.h1.a.extract()  # a 태그를 추출함
<a href="/"></a>

>>> html.h1  # 추출한 부분은 트리에서 제거되어 있음
<h1 class="site-headline">ham
egg
</h1>

>>> wrapper_tag = html.new_tag('div')  # 래핑용 태그 생성
>>> wrapper_tag.attrs['class'] = 'wapper'
>>> html.h1.wrap(wrapper_tag)  # 래핑
<div class="wapper"><h1 class="site-headline">ham
egg
</h1></div>
```
