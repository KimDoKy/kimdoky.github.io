---
layout: post
section-type: post
title: crawling - Beautiful Soup
category: python
tags: [ 'python' ]
---
미리 인지하고 있어야 할 내용  
1. HTML
2. [정규식](https://kimdoky.github.io/tech/2017/06/11/regular-2.html){:target="`_`blank"}  
3. [모듈](){:target="`_`blank"}

> 모든 내용은 Mac을 기준으로 진행합니다. 왜냐하면... 나는 Mac User이니까요..

---
# BeautifulSoup

[공식](https://www.crummy.com/software/BeautifulSoup/bs4/doc/){:target="`_`blank"}  

[한글](http://cryptosan.github.io/pythondocuments/documents/beautifulsoup4/#getting-help){:target="`_`blank"}

---

## 1. Beautiful Soup
Beautiful Soup은 웹 크롤러에서 가장 중요한 요소 중에 하나입니다.
굳이 Beautiful Soup라는 라이브러리를 사용하지 않아도 웹 크롤러를 만드는 것은 충분히 가능하지만 웹에서 우리가 원하는 데이터를 가져오기 위해서 일일이 수작업을 거쳐야 하는 번거로운 작업들이 Beautiful Soup를 이용하면 아주 간단하게 해결이 됩니다.  

예를 들어, 웹에서 원하는 이미지를 가져온다고 했을때 HTML 코드 전체를 대상으로 정규식 등을 사용하여 원하는 이미지가 있는 태그를 찾아내야하지만, Beautiful Soup를 이용하면 단 한 줄로 이 작업을 대신할 수 있습니다.

Beautiful Soup은 Python에서 Web 관련 작업을 하려면 꼭 배워야 할 라이브러리입니다.  

## 2. Beautiful Soup 설치하기

```Python
$ pip install beautifulsoup4
```

## 3. Beautiful Soup 사용하기

### (1) `find()` 함수 - 태그를 하나만 가져옵니다.

Beautiful Soup 객체(bs)에는 find 라는 함수가 있습니다. 이 함수를 이용하면 HTML 코드 안에서 원하는 태그를 가져올 수 있습니다.

```python
>>> html="""
... <html>
...     <head>
...         <title> test web </title>
...     </head>
...     <body>
...          <p align="center"> text contents </p>
...          <img src="/Users/dokyungkim/temp/docker.png" width="500" height="300">
...     </body>
... </html>
... """
>>> from bs4 import BeautifulSoup
>>> bs=BeautifulSoup(html)
>>> print(bs.prettify())
<html>
 <head>
  <title>
   test web
  </title>
 </head>
 <body>
  <p align="center">
   text contents
  </p>
  <img height="300" src="/Users/dokyungkim/temp/docker.png" width="500"/>
 </body>
</html>

>>> bs.find('title')
<title> test web </title>
```
위의 코드는 title 태그를 가져오고 있습니다.  
HTML 코드 안에서 어떤 특정태그를 가져오고 싶다면 위와 같이 find 함수의 인수에 태그의 이름을 전달해 주면 됩니다.

p 태그를 가져와 봅시다.
```python
>>> bs.find('p')
<p align="center"> text contents </p>
```

만약 찾고 싶은 태그가 없다면 아무 내용도 나오지 않습니다.
```python
>>> bs.find('a')
>>>
```
이번에는 속성으로 조회를 해봅시다.  
먼저 html코드중 가운데 부분을 수정합니다.
```python
>>> html="""
... <html>
...     <head>
...         <title> test web </title>
...     </head>
...     <body>
...         <p align="center"> text contents 1 </p>
...         <p align="right"> text contents 2 </p>
...         <p align="left"> text contents 3 </p>
...         <img arc="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" width="500" height=300">
...     </body>
... </html>"""
>>>
```
위의 html 코드를 보면 align 속성이 각각 center, right, left인 p태크들이 있습니다.  
각각의 p 태그를 속성을 이용해 조회해 봅니다.  
```python
>>> bs.find('p', align="center")
<p align="center"> text contents 1 </p>
>>> bs.find('p', align="right")
<p align="right"> text contents 2 </p>
>>> bs.find('p', align="left")
<p align="left"> text contents 3 </p>
```
위의 코드에서 첫 번째 줄을 보면 태스의 이름을 첫 번째 인수로 전달해주는 것까지는 동일합니다. 두 번째 인수(align="center")에 태그의 속성을 이용해서 조회합니다. 속성이름="값"의 형식으로 인수를 전달해 주면 속성을 이용해서 태그를 조회할 수 있습니다.

### (2) `find_all()` 함수 - 해당 태그가 여러 개 있을 경우 한꺼번에 모두 가져옵니다.
`find_all()` 함수는 `find()` 함수와는 다르게 원하는 태그가 몇 개가 있던 한꺼번에 가져옵니다. `find_all()` 함수를 사용하기 위해서 HTML 코드를 바꾸고 테스트해 봅니다.
```python
>>> html="""
... <html>
...      <head>
...          <title> test web </title>
...      </head>
...      <body>
...          <p align="center"> text contents 1 </p>
...          <p align="center"> text contents 2 </p> # center로 변경
...          <p align="center"> text contents 3 </p>
...          <img arc="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" width="500" height=300">
...      </body>
...  </html>"""
>>>
>>> bs=BeautifulSoup(html)
```
HTML코드를 변경 후 다시 Beautiful Soup 객체를 생성했습니다.  
```python
>>> bs.find_all('p')
[<p align="center"> text contents 1 </p>, <p align="center"> text contents 2 </p>, <p align="center"> text contents 3 </p>]
```
위 코드처럼 `find_all()` 함수를 사용해서 HTML코드 안에 있는 모든 p태그를 가져왔습니다.  
앞에서 봤던 `find()` 함수는 찾는 태그가 여러 개가 있어도 첫 번째 발견되는 1개 태그만 가져오지만 `find_all()` 함수는 여러 개를 한꺼번에 다 가져올 수 있어서 편리합니다.  
그런데 주의해야 할 점은 `find()`함수나 `find_all()` 함수는 반드시 자기 안에 있는 태그만 가져 올 수 있다는 점입니다.

```python
>>> head_tag = bs.find('head')
>>> head_tag
<head>
<title> test web </title>
</head>
>>> head_tag.find('title')
<title> test web </title>
>>> head_tag.find('p')
>>>
```
head 안에 title 부분은 성공적으로 가져옵니다. 그런데 head 태그 안에 p 태그가 존재하지 않기 때문에 아무것도 출력되지 않습니다.  

하지만 코딩을 하다 보면 지금까지 했던 것과 다르게 한가지의 태그만 찾는 것이 아니라 여러 가지의 태그를 찾아야 하는 상황이 자주 있습니다.  
예를 들어 p 태그와 img 태그를 같이 찾고 싶을 때 입니다.
```python
>>> body_tag = bs.find('body')
>>> list1 = body_tag.find_all(['p', 'img'])
>>>
>>> for tag in list1:
...     print(tag)
...
<p align="center"> text contents 1 </p>
<p align="center"> text contents 2 </p>
<p align="center"> text contents 3 </p>
<img arc="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" height='300"' width="500"/>
>>>
```
body 태그를 찾아서 `body_tag`에 넣어두고 `find_all` 함수에 리스트 형식으로 찾고 싶은 태그를 넣어줍니다. `find_all` 함수 실행결과 p태그와 img태그를 모두 찾아서 리스트로 리턴 해주었습니다. 한 번에 여러 가지 태그를 조회하고 싶을 때는 위와 같은 방식으로 해주면 됩니다.  

위와 같이 `find_all`의 인수에는 리스트만 들어갈 수 있는 것이 아닙니다.  
리스트뿐만 아니라 문자열, 정규식도 들어갈 수 있습니다.  
문자열은 처음에 `find_all`을 사용할 때의 방법과 같습니다.
```python
>>> bs.find_all('p')
[<p align="center"> text contents 1 </p>, <p align="center"> text contents 2 </p>, <p align="center"> text contents 3 </p>]
>>>
```

```python
>>> import re
>>> tags = bs.find_all(re.compile("^p"))
>>> tags
[<p align="center"> text contents 1 </p>, <p align="center"> text contents 2 </p>, <p align="center"> text contents 3 </p>]
>>>
```
`find_all` 함수에 전달할 수 있는 인수에 대해 살펴봅겠습니다.  
가장 기본적인 방법은 앞서봤던 태그이름을 전달해주는 방식입니다.  
그리고 태그이름을 전달해주는 방식 말고는 속성, 문장, limit 등이 있습니다.  
여러 방법들이 있지만 크롤러에 자주 사용하는 속성, 문장, limit 등의 방식만 다룹니다.  

속성을 이용한 방법입니다.  
```python
>>> bs.find_all(align="center")
[<p align="center"> text contents 1 </p>, <p align="center"> text contents 2 </p>, <p align="center"> text contents 3 </p>]
```
앞의 코드를 보면 `find_all` 함수에 속성="속성값"의 형식으로 인수가 전달되었습니다.  
align 속성이 center인 태그들이 조회가 됩니다. 이것이 속성을 이용하여 태그를 찾는 방법입니다. 이번에는 width속성이 500인 태그를 찾아보겠습니다.  
```python
>>> bs.find_all(width="500")
[<img arc="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" height='300"' width="500"/>]
```
width속성이 500인 태그를 검색하니까 이미지 태그가 나왔습니다.  

이번에는 text인자를 이용해 봅시다.
```python
>>> bs.find_all(text=" text contents 1 ")
[' text contents 1 ']
```
> text는 안에 텍스트가 빈칸을 포함해서 모두 정확히 일치해야 합니다.

위의 코드는 string의 문장이 " text contents 1 "인 태그를 찾는 코드입니다. text 뒷부분에 찾는 패턴을 쓸 때 공백이나 대,소문자를 특히 주의해야 합니다.  
text 인수는 문자열, 정규식, 리스트 등 여러 가지를 인수로 전달할 수 있습니다.

이번엔 정규식을 사용해 봅니다.
```python
>>> import re
>>> bs.find_all(text=re.compile(" text +"))
[' text contents 1 ', ' text contents 2 ', ' text contents 3 ']
```
위의 코드는 text인수에 "text contents" 문장 이후에 임의의 한 문자가 존재하는 태그를 찾는 코드입니다.

이번엔 limit 인수입니다.  
limit 인수는 `find_all` 함수로 찾아내는 태그의 개수를 제한합니다. 예를 들어 어떤 한 문서에서 p 태그를 `find_all` 함수로 검색했는데 수 천, 수 만개가 된다면 시간이 오래 걸릴 것입니다. 이때 몇 개까지만 찾을 수 있도록 제한을 둘 수 있는 인수가 limit 함수입니다.

```python
>>> bs.find_all('p')
[<p align="center"> text contents 1 </p>, <p align="center"> text contents 2 </p>, <p align="center"> text contents 3 </p>]

>>> bs.find_all('p', limit=2)
[<p align="center"> text contents 1 </p>, <p align="center"> text contents 2 </p>]
```
현재 HTML 코드에는 3개의 p 태그가 존재하지만 limit 인수에 2를 전달했기 때문에 p 태그를 세 개 모두 찾지 못하고 두 개만 찾게 되는 것입니다.

























[출처]왕초보! 파이썬 배워 크롤러 DIY 하다
배고프다.... 지우세요
