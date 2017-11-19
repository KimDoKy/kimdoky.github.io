---
layout: post
section-type: post
title: Python Library - chap 10. HTML과 XML 다루기 - 2. XML/HTML을 빠르고 유연하게 해석하기
category: python
tags: [ 'python' ]
---

`lxml` 패키지는 `xml.etree.ElementTree`와 마찬가지로  XML을 해석하는 기능을 제공합니다. lxml은 처리 속도가 빠르므로 크기가 큰 파일, 많은 파일을 다룰 때 사용하기 편합니다.  
xml.etree.ElementTree와 다른 점은 parser의 동작을 제어하여 올바른 형식이 아닌 (non well-formed) XML을 다룰 수 있습니다. HTML용 parser도 이용할 수 있습니다.

## lxml 설치

```
$ pip install lxml
```

OS가 Linux일 경우, `libxml2`와 `libxslt`가 필요합니다.

### lxml 의존 라이브러리 설치 예

```
sudo apt-get install libz-dev libxml2-dev libxslt1-dev
```
### 올바른 형식이 아닌(non well-formed) XML 해석하기

lxml은 해석할 때 동작을 결정하는 parser의 사양을 세세히 제어할 수 있습니댜.


### 예로 사용할 broken.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<weather>
  <local_weather name="Seoul">
    <condition>Sunny</condition>
    <temperature>25</temperature>
    <humidity>47</humidity>
</weather>
```
위 파일은 <local_weather>를 닫지 않아 구문으로서 올바르지 못합니다.  

### broken.xml 읽어오기

```python
>>> from lxml import etree
>>> tree = etree.parse('broken.xml')  # 오류가 됨
Traceback (most recent call last):
...
lxml.etree.XMLSyntaxError: Opening and ending tag mismatch: local_weather line 3 and weather, line 7, column 11

>>> parser = etree.XMLParser(recover=True)
>>> tree = etree.parse('broken.xml', parser)  # parser를 지정하고 있음
>>> tree.find('./local_weather').attrib
{'name': 'Seoul'}
```

parse() 메서드를 기본값인 상태로 사용하면 broken.xml 해석은 실패합니다. parser의 동작을 조정하려 할 때는 XMLParser 클래스를 이용합니다. XMLParser 클래스의 인수 recover를 True로 설정하고 parse()에서 사용하면 해석에 성공합니다.

lxml.etree에 있는 많은 인터페이스는 xml.etree.ElementTree와 호환됩니다.  

### lxml.etree.XMLParser 클래스

형식 | class lxml.etree.XMLParser(self, encoding=None, attribute_defaults=False, dtd_validation=False, load_dtd=False, no_network=True, ns_clean=False, recover=False, XMLSchema schema=None, remove_blank_text=False, resolve_entities=True, remove_comments=False, remove_pis=False, strip_cdata=True, collect_ids=True, target=None, compact=True)
---|---
설명 | XML을 해석한다. 올바른 형식이 아닌(non well-formed) XML도 다룰 수 있다.
인수 | recover - True이면, 올바른 형식이 아닌 XML도 해석을 시도한다. <br> remove_blank_text - True이면, 태그 간 공백이나 줄바꿈을 제외한다. <br> remove_comments - True이면, \<!-- 주속 --> 으로 표현되는 주석을 제외한다.

## HTML 해석하기
lxml.etree.HTMLParser는 HTML 해석에 적합합니다.  

실제 웹페이지 ["The Python Standard Library"](https://docs.python.org/3.4/library/index.html)에서 제목 목록의 텍스트와 파일 경로를 구해봅니다.

### 검색 대상 HTML 예

```html
<li class="toctree-l1">
  <a class="reference internal" href="intro.html">1. Introduction</a>
</li>
<li class="toctree-l1">
  <a class="reference internal" href="functions.html">2. Built-in Functions</a>
</li>
```

### 제목 목록 얻기

```python
>>> import urllib.request
>>> source = urllib.request.urlopen('https://docs.python.org/3.4/library/index.html').read()
>>> tree = etree.fromstring(source, etree.HTMLParser())
>>> elements = tree.findall('.//li[@class="toctree-l1"]/a')
>>> for element in elements:
...     print(element.text, element.attrib['href'])
...
1. Introduction intro.html
2. Built-in Functions functions.html
3. Built-in Constants constants.html
4. Built-in Types stdtypes.html
5. Built-in Exceptions exceptions.html
...
```
제목과 해당 파일 목록을 얻었습니다.

### lxml.etree.HTMLParser 클래스

형식 | class lxml.etree.HTMLParser(self, encoding=None, remove_blank_text=False, remove_comments=False, remove_pis=False, strip_cdata=True, no_network=True, target=None, XMLSchema schema=None, recover=True, compact=True)
---|---

HTMLParser 클래스의 사용법은 XMLParser 클래스와 거의 같습니다.

## HTML 수정하기
lxml을 사용하여 HTML의 요소와 내용을 수정하는 방법입니다. html 모듈을 사용하여 HTML을 해석합니다.

### html 모듈을 사용하여 HTML 해석하기

```python
from lxml import html
import urllib.request

url = 'https://docs.python.org/3.4/library/index.html'
tree = html.parse(urllib.request.urlopen(url)).getroot()
div_toctree = tree.find('.//div[@class="toctree-wrapper compound"]/')

print(html.tostring(div_toctree, pretty_print=True, encoding='unicode'))
```

### 해석한 HTML

```html
<ul>
<li class="toctree-l1"><a class="reference internal" href="intro.html">1. Introduction</a></li>
<li class="toctree-l1"><a class="reference internal" href="functions.html">2. Built-in Functions</a></li>
...
```

### HTML 가공하기

- 각 요소의 class 속성을 삭제한다.
- a 요소의 href 속성값을 \https://로 시작하는 경로로 수정한다.

```python
from lxml import html
import urllib.request

url = 'https://docs.python.org/3.4/library/index.html'
tree = html.parse(urllib.request.urlopen(url)).getroot()
div = tree.find('.//div[@class="toctree-wrapper compound"]/')

# class 속성을 삭제한다.
for tag in div.xpath('//*[@class]'):
    tag.attrib.pop('class')

# a 요소의 href 속성값을 절대 경로로 변경한다.
absolute_url = html.make_links_absolute(div, base_url="http://docs.python.org/3.4/library/")

print(html.tostring(absolute_url, pretty_print=True, encoding='unicode'))
```

### 가공 후의 HTML

```html
<ul>
<li><a href="http://docs.python.org/3.4/library/intro.html">1. Introduction</a></li>
<li><a href="http://docs.python.org/3.4/library/functions.html">2. Built-in Functions</a></li>
<li>
<a href="http://docs.python.org/3.4/library/constants.html">3. Built-in Constants</a><ul>
```

### lxml.html.make_links_absolute()

형식 | lxml.html.make_links_absolute(html, base_href)
---|---
설명 | a 요소의 href 속성값을 절대 경로로 변경한다.
인수 | html - 대상 tree를 지정한다. <br> base_href - 기반이 되는 URL를 지정한다.
반환값 | HtmlElement 객체
