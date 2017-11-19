---
layout: post
section-type: post
title: Python Library - chap 10. HTML과 XML 다루기 - 1. XML 해석하기
category: python
tags: [ 'python' ]
---

Python에서 HTML과 XML을 다루는 라이브러리와 서드파티 패키지를 다룹니다. 또한 Web 스크래핑 및 HTML의 가공 방법도 소개합니다. 각종 라이브러리와 서드파티 패키지의 차이점에 대해 다룹니다.

# XML 해석하기

xml.etree.ElementTree는 XML을 해석하는 기능을 제공합니다. XML은 XHTML이나 RSS에서 이용하고, 오픈 데이터를 XML 포맷으로 제공하는 기상청도 있을 정도로 많은 분야에서 사용하고 있습니다.  
xml.etree.ElementTree를 이용하면 XML을 해석하고 생성할 수 있습니다.  

다음 XML 파일 sample.xml을 해석 대상으로 합니다.

### sample.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<weather>
  <local_weather name="Seoul">
    <condition>Sunny</condition>
    <temperature>25</temperature>
    <humidity>47</humidity>
  </local_weather>
  <local_weather name="Buchun">
    <condition>Cloudy</condition>
    <temperature>26</temperature>
    <humidity>38</humidity>
  </local_weather>
</weather>
```

### XML을 해석하여 정보 얻기

```python
>>> import xml.etree.ElementTree as et

>>> tree = et.parse('sample.xml')
>>> seoul = tree.find('./local_weather')  # 요소 local_weather를 검색하여 맨 처음 하나를 얻음
>>> seoul.tag  # 요소 이름 얻기
'local_weather'

>>> seoul.attrib  # 속성 리스트 얻기
{'name': 'Seoul'}

>>> seoul.get('name')  # 짖어한 속성값 얻기
'Seoul'

>>> seoul_condition = seoul.find('./condition')  # local_weather 탐색
>>> seoul_condition.tag
'condition'

>>> seoul_condition.text
'Sunny'
```
트리 구조를 따라가서 목적 정보에 도달하는 것이 기본적인 사용법입니다. 앞에선 'Sunny'를 구하기 위해 find()를 두 번 사용했으나, 한 번에 도달할 수도 있습니다.

### 한 번에 더 깊은 경로 탐색하기

```python
>>> buchun_condition = tree.find('./local_weather[@name="Buchun"]/condition')
>>> buchun_condition.text
'Cloudy'
```
find() 메서드는 맨 처음 하나가 발견된 시점에서 탐색을 종료합니다. 모두 찾을 때까지 계속 탐색하려면 findall() 메서드를 사용합니다.

### findall()을 사용한 탐색

```python
>>> elements = tree.findall('./local_weather')
>>> for element in elements:
...     element.attrib  # 요소의 속성을 dict으로 얻음
...
{'name': 'Seoul'}
{'name': 'Buchun'}
```

### xml.etree.ElementTree.parse()

형식 | xml.etree.ElementTree.parse(source, parse=None)
---|---
설명 | XML을 해석하여 트리를 작성한다.
인수 | source - 해석 대상 파일 이름 또는 파일 객체를 지정한다.
반환값 | ElementTree 객체

### xml.etree.ElementTree.find()

형식 | xml.etree.ElementTree.find(match, namespaces=None)
---|---
설명 | 요소를 트리에서 탐색하고 발견되면 Element 인스턴스를 반환한다. 맨 처음 하나가 발견된 시점에서 탐색을 종료한다.
인수 | match - 트리를 탐색하는 경로를 지정한다.
반환값 | Element 객체

match에는 XPath의 일부 표현을 사용하여 탐색 요소를 지정합니다.

### xml.etree.ElementTree.findall()

형식 | xml.etree.ElementTree.findall(match, namespaces=None)
---|---
설명 | 요소를 트리에서 탐색하고 발견되면 Element 인스턴스를 리스트로 반환한다.
인수 | match - 트리를 탐색하는 경로를 지정한다.
반환값 | Element 객체의 리스트
