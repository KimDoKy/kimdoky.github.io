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
# BeautifulSoup Document

[공식 문서](https://www.crummy.com/software/BeautifulSoup/bs4/doc/){:target="`_`blank"}  

[한글 문서](http://cryptosan.github.io/pythondocuments/documents/beautifulsoup4/#getting-help){:target="`_`blank"}

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

### (3) 문장 가져오기

`find()` 함수와 `find_all()` 함수를 이용해서 태그를 찾았습니다.  
하지만 우리에게 필요한 것은 화면에 보여지는 내용입니다.  

```python
>>>
>>> body_tag = bs.find('body')
>>> p_tag = body_tag.find('p')
>>>
>>> p_tag.string
' text contents 1 '
>>>
```
위 코드를 보면 먼저 body 태그에서 p 태그를 찾았습니다. p 태그가 실제로 존재하지만 `find_all`이 아니라 `find` 함수를 사용하면 제일 먼저 나오는 p 태그를 가져옵니다.  
그래서 1개만 가져와서 `p_tag`에 담았습니다. 그리고 p 태그를 찾은 후에 객체에서 string을 가져왔습니다. string은 태그의 문장을 가지고 있습니다.  
태그에 포함된 문장만을 가지고 올 때 자주 사용되는 방법입니다.  
그런데 위의 string을 사용하면 한번에 한 문장 밖에 가져오지 못합니다.  
태그 안에 존재하는 여러 개의 문장을 한꺼번에 가져오려면 어떻게 해야 할까요?

```python
>>> strings = body_tag.strings
>>> for  string in strings:
...     print(string)
...


 text contents 1


 text contents 2


 text contents 3




>>>
```
head 태그를 제외하고 body 태그안의 모든 문장을 가져오기 위해서 body 태그의 strings를 사용했습니다. strings에는 태그 안에 있는 모든 문장들이 저장되어 있습니다. 그래서 위의 코드처럼 출력해주니까 body 태그의 모든 문장들이 출력되었습니다.  

이번에는 태그에서의 여러 문자열을 하나의 문자열로 출력해주는 함수를 다뤄보겠습니다.
```python
>>> body_tag = bs.find('body')
>>> body_tag.get_text()
'\n text contents 1 \n text contents 2 \n text contents 3 \n\n'
>>>
```
위처럼 `get_text()` 함수를 사용하면 태그 아래의 모든 문자열을 하나의 문자열로 돌려줍니다. 그런데 보면 각 문장의 시작과 끝에 줄바꿈 기호가 삽입되어있습니다.  
이것은 html 태그를 Beautiful Soup로 넣어줄 때 들어간 줄 바꿈 기호들입니다.  
이것들을 다 지우고 깔끔하게 연결해 보겠습니다.  
```python
>>> body_tag.get_text(strip=True)
'text contents 1text contents 2text contents 3'
>>>
```
중간에 들어가 있던 줄 바꿈 기호가 전부 사라졌습니다.  
그런데 뽑아낸 문장들이 다닥다닥 붙어있어서 구분하기가 힘듭니다.  
문장끼리 구분을 쉽게 할 수 있도록 각 문장의 끝에 기호를 넣어줍니다.

```python
>>> body_tag.get_text('-', strip=True)
'text contents 1-text contents 2-text contents 3'
>>>
```
위의 코드를 보면 뽑아낸 문장들의 끝에 '-' 기호가 삽입되었습니다.  

### (4) 태그의 속성

Beautiful Soup에는 마치 HTML의 속성과 비슷한 부분이 있습니다.  
Beautiful Soup를 사용하여 이러한 속성들을 가져올 수 있고 속성으로 태그를 가져올 수도 있습니다.  

HTML의 태그 속성에서 class라는 속성이 있습니다.  
Beautiful Soup에서는 HTML의 class 속성을 가져올 수 있을 뿐만 아니라 태그의 속성을 추가 할 수도 있고, 제거, 변경 모두 가능합니다.

```python
>>>
>>> html="""
... <html>
...     <head>
...         <title> test web </title>
...     </head>
...     <body>
...         <p class="ptag black" align="center"> text content 1 </p>
...         <p class="ptag yellow" align="center"> text content 2 </p>
...         <p class="ptag red" align="center"> text content 3 </p>
...         <img src="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" width="500" height="300">
...     </body>
... </html>"""
>>> bs = BeautifulSoup(html)
>>> p_tag = bs.find('p')
>>> p_tag['class']
['ptag', 'black']
>>>
```
위의 코드는 첫 번째 p 태그의 class 속성을 조회하였습니다.  
class 속성을 변경해보겠습니다.  
```python
>>>
>>> p_tag['class'][1] = 'white'
>>> p_tag['class']
['ptag', 'white'] # black에서 white으로 변경 됨
>>>
```
p 태그의 클래그를 변경했습니다.  
이번에는 속성을 추가합니다.  

```python
>>>
>>> p_tag['id'] = 'P-TAG'
>>> p_tag['id']
'P-TAG'
>>> p_tag
<p align="center" class="ptag white" id="P-TAG"> text content 1 </p>
```
p 태그에 id라는 속성이 추가되었습니다. 이번에는 속성을 지워보겠습니다.  

```python
>>>
>>> p_tag['align']
'center'
>>> del p_tag['align']
>>> p_tag['align']
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/local/var/pyenv/versions/crawling_diy/lib/python3.5/site-packages/bs4/element.py", line 1011, in __getitem__
    return self.attrs[key]
KeyError: 'align'
>>> p_tag
<p class="ptag white" id="P-TAG"> text content 1 </p>
>>>
```
원래 있었던 align이라는 속성을 삭제했습니다. 속성을 삭제하고 조회하니 에러가 발생하였습니다. 오류 메시지를 보면 태그의 속성은 딕셔너리 형태라는 것을 알 수 있습니다. 속성이 key가 되고 속성값이 value가 되는 것입니다.   
```python
>>> p_tag.attrs
{'id': 'P-TAG', 'class': ['ptag', 'white']}
>>>
```
태그의 속성들을 한꺼번에 보고 싶으면 `attrs`를 이용하면 바로 접근이 가능합니다. 역시 예상한 대로 딕셔너리 형태로 나왔습니다.

### (5) 태그의 관계

HTML 코드의 태그들 사이에는 관계라는 것이 존재합니다. 이 말은 쉽게 말하면 자신을 포함하고 있는 태그를 부모 태그라고 하고, 자신이 포함하고 있는 태그를 자식태그라고 합니다. 그리고 부모도 자식도 아닌 같은 수준이 있는 태그도 있습니다.  

`find`나 `find_all` 함수는 자식 태그를 대상으로 검색을 합니다. 쉽게 말하면 자기 자신이 포함한 태그들이 검색 대상이 된다는 것입니다.
```python
>>> html="""
... <html>
...     <head>
...         <title> test web </title>
...     </head>
...     <body>
...         <p class="ptag black" align="center"> text content 1 </p>
...         <p class="ptag yellow" align="center"> text content 2 </p>
...         <p class="ptag red" align="center"> text content 3 </p>
...         <img src="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" width="500" height="300">
...     </body>
... </html>"""
>>> bs = BeautifulSoup(html)
>>> body_tag = bs.find('body') # find_all은 리스트 형태로 저장합니다
>>> body_tag
<body>
<p align="center"> text contents 1 </p>
<p align="center"> text contents 2 </p>
<p align="center"> text contents 3 </p>
<img arc="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" height='300"' width="500"/>
</body>
```
위의 HTML 코드를 사용했을 때 body 태그의 자식들은 body 태그의 시작태그와 끝 태그 사이에 존재하는 모든 태그들입니다. 여기서 body태그에 `find()` 함수나 `find_all()` 함수를 사용했을 때 찾을 수 있는 태그들은 p 태그와 img 태그뿐입니다.  
즉, `find()`나 `find_all()`함수는 자식을 검색 대상으로 한다는 것을 알 수 있습니다.  
```python
>>> for child in body_tag.children:
...     print(child)
...


<p align="center"> text contents 1 </p>


<p align="center"> text contents 2 </p>


<p align="center"> text contents 3 </p>


<img arc="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" height='300"' width="500"/>


>>>
```
위의 코드에서처럼 `children`은 해당 태그의 자식들을 리스트로 가지고 있습니다.  
이렇게 하면 `body_tag`의 자식들이 무엇인지 보기 쉬워졌습니다.  

부모는 자식의 개념을 반대로 생각하면 됩니다. body 태그의 자식들은 p와 img태그라고 한다면, p와 img태그의 부모는 body태그가 됩니다.

```python
>>> img_tag = bs.find('img')
>>> img_tag.parent
<body>
<p class="ptag white" id="P-TAG"> text content 1 </p>
<p align="center" class="ptag yellow"> text content 2 </p>
<p align="center" class="ptag red"> text content 3 </p>
<img height="300" src="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" width="500"/>
</body>
>>>
```
위의 코드에서 `parent`를 조회하니까 img 태그의 부모인 body 태그가 나왔습니다.  

그러면 자신이 포함하지도, 자신을 포함하고 있는 것도 아닌 태그는 무엇일까요? 위의 코드에서 보이는 p와 img 태그 같은 경우입니다.  
부모가 같으니까 p 태그들과 img 태그는 형제라고 볼 수 있습니다.  
Python에서는 이렇게 태그의 부모와 자식, 형제를 쉽게 찾을 수 있도록 도와줍니다.

### (6) `find_parent()` 함수와 `find_parents()`함수
`find_parent()` 함수는 쉽게 말하면 부모를 찾는 `find()` 함수라고 생각하면 됩니다.
```python
>>>
>>> p_tag = bs.find('p')
>>> p_tag
<p class="ptag white" id="P-TAG"> text content 1 </p>
>>> p_tag.find_parent('body')
<body>
<p class="ptag white" id="P-TAG"> text content 1 </p>
<p align="center" class="ptag yellow"> text content 2 </p>
<p align="center" class="ptag red"> text content 3 </p>
<img height="300" src="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" width="500"/>
</body>
>>>
```
위의 코드는 p 태그에서 자기의 부모 중에 body를 찾았습니다.

```python
>>> p_tag.find_parent('html')
<html>
<head>
<title> test web </title>
</head>
<body>
<p class="ptag white" id="P-TAG"> text content 1 </p>
<p align="center" class="ptag yellow"> text content 2 </p>
<p align="center" class="ptag red"> text content 3 </p>
<img height="300" src="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" width="500"/>
</body>
</html>
>>>
```
위의 코드는 부모 중에 html 태그를 찾아냈습니다.  
그럼 p 태그에게는 부모가 body와 html태그입니다.  

이번에는 title태그의 부모를 찾아봅니다.
``` python
>>> title_tag = bs.find('title')
>>> title_tag.find_parent('head')
<head>
<title> test web </title>
</head>
>>>
```
title 태그의 부모에서 head라는 태그를 찾았습니다. `find` 함수와 큰 차이가 없습니다.  

이번에는 `find_all()`와 비슷한  `find_parents()`함수를 보겠습니다.  
`find_parents()`함수는 자신이 포함하고 있는 모든 부모를 찾아서 리스트로 돌려줍니다.  

먼저 HTML코드를 수정합니다.

```python
>>> html="""
...  <html>
...      <head>
...          <title> test web </title>
...      </head>
...      <body>
...          <p class="ptag black" align="center"> text contents 1 </p>
...          <p class="ptag yellow" align="center"> text contents 2 </p>
...          <p class="ptag red" align="center"> text contents 3 </p>
...          <img arc="/Users/dokyungkim/Git/Study/crawling_diy/docker.png" width="500" height=300">
...
...          <div class="container">
...              <p class="text"> </p>
...          </div>
...      </body>
...  </html>"""
>>> bs = BeautifulSoup(html)
>>>
```
기존 HTML코드에 p태그를 자식으로 가진 div태그를 추가했습니다.  
새로 추가된 p 태그의 부모를 모두 찾아봅니다.
```python
>>> p_tag = bs.find('p', class_="text")
>>> parents = p_tag.find_parents()
>>> for parent in parents:
...     print(parent.name)
...
div
body
html
[document]
>>>
```
위의 코드를 보면 `find_parents` 함수를 사용하니까 자신의 바로 위 부모태그인 div태그부터 최상위의 `[document]`까지 출력되었습니다.

---
[출처]왕초보! 파이썬 배워 크롤러 DIY 하다
