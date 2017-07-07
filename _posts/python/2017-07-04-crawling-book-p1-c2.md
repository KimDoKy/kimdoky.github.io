---
layout: post
section-type: post
title: crawling - P1.스크레이퍼 제작 _ cahp 2. 고급 HTML 분석
category: python
tags: [ 'python' ]
---

복잡한 HTML 페이지를 분석해서 원하는 정보만 추출하는 방법을 다룹니다.

## 2.1 닭 잡는 데 소 잡는 칼을 끌 필요는 없습니다.

복잡한 태그를 써서라도 필요한 정보를 추출하고 싶을 수 있습니다. 하지만 부주의하게 사용한다면 코드는 디버그하기 어려워지거나 취약해질 수 있습니다. 우선 고급 HTML 분석을 쓰지 않아도 필요한 결과를 얻을 수 있는 방법에 대해 다룹니다.

원하는 콘텐츠가 있습니다. 그 콘텐트는 20단계나 되는 HTML 덩어리 속에, 단서가 될 만한 태그나 속성이 하나 없이 파묻혀 있을 수 있습니다.

```python
bsObj.findAll("table")[4].findAll("tr")[2].find("td").findAll("div")[1].find("a")
```
그냥 봐도 좋아보이지 않습니다. 간결함이나 우아함은 찾아볼 수 없고, 사이트 관리자가 조금만 수정하면 웹 스크레이퍼의 동작은 멈출 것입니다.

- '페이지 인쇄'같은 링크를 찾아보거나, 더 나은 HTML 구조를 갖춘 모바일 버전 사이트를 찾아보세요.
- 자바스크립트 파일에 숨겨진 정보를 찾아보세요. 물론 이렇게 하려면 자바스크립트 파일을 불러와서 분석해야 합니다.
- 중요한 정보는 페이지 타이틀에 있을 때가 대부분이지만, 원하는 정보가 페이지 URL에 들어 있을 때도 있습니다.
- 원하는 정보가 오직 이 웹사이트에만 있다면 할 수 있는 일이 더는 없을 수 있습니다. 그렇지 않다면, 이 정보를 다른 소스에서 가져올 수 없는지 생각해봅니다.

데이터가 깊숙이 파묻혀 있거나 정형화되지 않았을수록, 곧바로 코드부터 짜서는 안 됩니다.

## 2.2 다시 BeautifulSoup

이 섹션에서는 속성을 통해 태그를 검색하고, 태그 목록을 다루는 방법, 트리 내비게이션을 분석하는 방법을 다룹니다.

거의 모든 웹사이트에는 스타일시트가 존재합니다. 웹 사이트의 스타일 계층은 육안으로 해석하는 것을 위해 만들어진 것이라 웹 스크레이핑에는 별 도움이 되지 않을 것 같지만, CSS의 등장은 웹 스크레이퍼에도 큰 도움이 되었습니다. CSS는 HTML 요소를 구분해서 서로 다른 스타일을 적용합니다.  
예를 들어 다음과 같은 태그가 있습니다.
```HTML
<span class="green"></span>
<span class="red"></span>
```
이 경우 웹 스크레이퍼는 클래스를 이용해 쉽게 이 태그들을 구별할 수 있습니다. CSS는 이런 속성을 통해 사이트에 스타일을 적용하며, 웹사이트 대부분은 이런 클래스(class)와 ID(id)속성이 가득합니다.

http://www.pythonscraping.com/pages/warandpeace.html 페이지를 스크랩하는 예제 웹 스크레이퍼를 만들어봅니다.

![]({{site.url}}/img/post/python/crawling/p1c2_1.png)

이 페이지에서 등장인물이 말하는 대사는 빨간색으로, 등장인물의 이름은 녹색으로 표시되어 있습니다. 다음 소스 코드 샘플을 보면 span 태그에 적절한 CSS 클래스가 붙어 있습니다.

```HTML
"<span class="red">Heavens! what a virulent attck!</span>" replied <span class="green">the prince</span>, not in the least disconcerted by this reception.
```

페이지 전체를 가져온 다음, BeautifulSoup 객체로 프로그램을 만들 수 있습니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = BeautifulSoup(html, "html.parser")
```
BeautifulSoup 객체에 `findAll` 함수를 쓰면 `<span class="green"></span>"` 태그에 들어있는 텍스트만 선택해서 고유명사로 이루어진 파이썬 리스트를 추출할 수 있습니다.

```python
nameList = bsObj.findAll("span", {"class":"green"})
for name in nameList:
    print(name.get_text())
```
이 코드는 [전쟁과 평화]에 등장하는 모든 고유명사를 순서대로 출력합니다.

```python
~/Git/Study/crawling/web_scraping(master*) » python 2_2.py
Anna
Pavlovna Scherer
Empress Marya
Fedorovna
Prince Vasili Kuragin
Anna Pavlovna
St. Petersburg
the prince
Anna Pavlovna
.
.

```
bsObj.tagName을 호출해서 페이지에 처음 나타난 태그를 찾아냈습니다. 이번에는 bsObj.findAll(tagName, tagAttributes)을 호출해서 첫 번째 태그만이 아니라 페이지의 태그 전체를 찾은 겁니다.

이름 리스트를 만든 뒤에는 리스트의 모든 이름을 순회하며 `name.get_text()`를 호출해 태그를 제외하고 콘텐츠만 출력합니다.

> `get_text()`를 쓸 때와 태그를 보존할 떼  
`.get_text()`는 현재 문서에서 모든 태그를 제거하고 텍스트만 들어 있는 문자열을 반환합니다. 예를 들어 하이퍼링크, 문단, 기타 태그가 여럿 들어 있는 텍스트 블록에 사용하면 태그 없는 텍스트만 남습니다.  
텍스트 블록보다는 BeautifulSoup 객체를 사용하는게 원하는 결과를 얻기가 훨씬 쉽습니다. `.get_text()`는 항상 마지막, 즉 최종 데이터를 출력하거나 저장, 조직하기 직전에만 써야 합니다. 일반적으로는 문서의 태그 구조를 가능한 유지해야 합니다.

### 2.2.1 `find()`와 `findAll()`

`find()`와 `findAll()`은 BeautifulSoup에서 가장 자주 쓰는 함수입니다. 이 함수를 쓰면 HTML 페이지에서 원하는 태그를 다양한 속성에 따라 쉽게 필터링할 수 있습니다.  

두 함수는 거의 비슷한데, BeautifulSoup 문서의 함수 정의만 봐도 알 수 있습니다.

```python
findAll(tag, attributes, recusive, text, limit, keywords)
find(tag, attributes, text, keywords)
```
실제로 이 함수를 쓸 때는 거의 항상 처음 두 매개변수인 tag와 attributes만 쓰게 될 것입니다.  

- tag
태그 이름인 문자열을 넘기거나, 태그 이름으로 이루어진 파이썬 리스트를 넘길 수도 있습니다. 예를 들어 다음 코드는 문서의 모든 헤더 태그 리스트를 반환합니다.
```python
.findAll({"h1","h2","h3","h4"})
```

- attributes
속성으로 이루어진 파이썬 딕셔너리를 받고, 그중 하나에 일치하는 태그를 찾습니다. 예를 들어 다음 함수는 HTML 문서에서 녹색과 빨간색 span 태그를 **모두** 반환합니다.

```python
.findAll("span", {"class":{"green", "red"}})
```

- recusive
Booleans입니다. 문서에서 얼마나 깊이 찾아 들어가고 싶은지를 지정합니다. recusive가 True이면 findAll 함수는 매개변수에 일치하는 태그를 찾아 자식, 자식의 자식을 검색합니다. false이면 문서의 최상위 태그만 찾습니다. findAll은 True가 기본값입니다. 일반적으로 이 옵션은 그대로 두는 것이 좋습니다.(원하는 것이 정확히 무엇인지 알고 있으며 성능이 중요한 상황이 아니라면..)

- text
태그의 속성이 아니라 텍스트 콘텐츠에 일치한다는 점이 좀 다릅니다. 예를 들어 예제 페이지에서 태그에 둘러싸인 'the prince'가 몇 번 나타났는지 보려면 이전 예제의 `.findAll()` 함수를 다음과 같이 수정하면 됩니다.

```python
nameList = bsObj.findAll(text="the prince")
print(len(nameList))
```

출력 결과는 7입니다.

- limit
findAll에서만 쓰입니다. find는 findAll을 호출하면서 limit을 1로 지정한 것과 같습니다. 이 매개변수는 페이지의 항목 **처음 몇 개** 에만 관심이 있을때 사용합니다. 이 매개변수는 페이지에 나타난 순서대로 찾으며 그 순서가 원하는 바와 일치한다는 보장은 없으므로 주의해야합니다.

- keyword
특정 속성이 포함된 태그를 선택할 때 사용합니다.

```python
allText = bsObj.findAll(id="text")
print(allText[0].get_text))
```

> keyword 매개변수를 쓸 때 주의할 점  
keyword 매개변수는 특정 상황에서 매우 유용할 수 있습니다. 하지만 기술적으로는 BeautifulSoup 자체의 기능과 중복되기도 합니다.  
```python
bsObj.findAll(id="text")
bsOdj.findAll("", {"id":"text"})
```
또한 keyword는 가끔 문제를 일으키는데, 가장 흔한 경우는 class 속성으로 요소를 검색할 때 일어나며 이는 class가 파이썬에서 보호된 키워드이기 때문입니다. 즉 class는 파이썬 예약어이므로 변수나 매개변수 이름으로 쓸 수 없습니다.(BeautifulSoup.findAll()의 keyword 매개변수와는 상관없습니다.)  
예를 들어 다음 행은 class를 비표준적인 방법으로 사용하므로 문법 에러를 일으킵니다.  
```python
bsObj.findAll(class="green")
```
대신 어설프지만, 밑줄을 추가하는 해결책을 쓸 수 있습니다.
```python
bsObj.findAll(class_="green")
```
혹은 class를 따옴표 안에 쓰는 방법도 있습니다.
```python
bsObj.findAll("", {"class":"green"})
```

"원하는 속성을 딕셔너리 리스트에 담아서 함수에 전달하면 되지 않을까?"

태그 목록을 `.findAll()`에 속성 목록으로 넘기면 `or` 필터처럼 동작한다는 점, 즉 tag1, tag2, tag3 등이 들어간 모든 태그 목록을 선택하게 됩니다. 태그 목록이 길다면 필요 없는 것들도 잔뜩 선택될 것입니다. keyword 매개변수는 `and` 필터처럼 동작하므로 그런 문제가 없습니다.

### 2.2.2 기타 BeautifulSoup 객체

- BeautifulSoup 객체
이전 코드 예제에서 bsObj와 같은 형태로 사용했습니다.

- Tag 객체
리스트 호출 또는 BeautifulSoup 객체에 find와 findAll을 호출해서 또는 다음과 같이 탐색해 들어가서 얻습니다.
```python
bsObj.div.h1
```

- NavigableString 객체
태그 자체가 아니라 태그 안에 들어 있는 텍스트를 나타냅니다. 일부 함수는 NavigableString를 다루거나 반환합니다.

- Comment 객체
주석 태그 안에 들어 있는 HTML 주석 (<!- like this one -->)을 찾는데 사용합니다.

### 2.2.3 트리 이동

findAll 함수는 이름과 속성에 따라 태그를 찾습니다. 하지만 문서 안에서의 위치를 기준으로 태그를 찾을 때는 어떻게 할까요? 이럴 때 트리 내비게이션이 필요합니다. 앞에서는 트리를 단방향으로 이동했었습니다.
```python
bsObj.tag.subTag.anotherSubTag
```
http://www.pythonscraping.com/pages/page3.html 에 있는 온라인 쇼핑 사이트 스크레이핑 예제 페이지를 이용하여 HTML 트리를 이동하는 방법을 다룹니다.

![]({{site.url}}/img/post/python/crawling/p1c2_2.png)

이 페이지의 HTML은 다음과 같은 트리 구조로 나타낼 수 있습니다.

```
-html
  - body
    - div.wrapper
      - h1
      - div.content
      - table#giftList
        - tr
        - th
        - th
        - th
        - th
      - tr.gift#gift1
        - td
        - td
          - span.excitingNote
        - td
        - td
          - img
      - ..더 많은 테이블 행
  - div.footer
```

#### 자식과 자손
여러 다른 라이브러리와 마찬가지로 BeautifulSoup 라이브러리도 **자식** 과 **자손** 을 구별합니다. 예를 들어 tr 태그는 table 태그의 자식이며 tr과 th, td, img, span은 모두 table 태그의 자손입니다. 모든 자식은 자손이지만, 모든 자손이 자식인 것은 아닙니다.

일반적으로 BeautifulSoup 함수는 항상 현재 선택된 태그의 자손을 다룹니다. 예를 들어 bsObj.body.h1은 body의 자손인 첫 번째 h1 태그를 선택합니다. body 바깥에 있는 태그에 대해서는 동작하지 않습니다.

마찬가지로 bsObj.div.findAll("img")는 문서의 첫 번째 div 테그를 찾고, 그 div 태그의 자손인 모든 img 태그의 목록을 가져옵니다.

자식만 찾을 때는 `.children`을 사용합니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html.parser")

for child in bsObj.find("table", {"id":"giftList"}).children:
    print(child)
```

이 코드는 giftList 테이블에 들어 있는 제품 행 목록을 출력합니다. `children()` 대신 `descendants()`함수를 썼다면 테이블에 포함된 태그가 20개 이상 출력됐을 것이고, 거기에는 img, span, td 태그 등이 모두 포함됐을 겁니다. 자신과 자손의 구별은 중요합니다.

#### 형제 다루기
BeautifulSoup의 `next_siblings()`함수는 테이블에서 데이터를 쉽게 수집할 수 있으며, 특히 테이블에 타이블 행이 있을 때 유용합니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html.parser")

for sibling in bsObj.find("table", {"id":"giftList"}).tr.next_siblings:
    print(sibling)
```
이 코드의 출력 결과는 제품 테이블에서 첫 번째 타이틀 행을 제외한 모든 제품 행입니다. 타이틀 행은 왜 건너뛰었을까요?
1. 객체는 자기 자신의 형제(sibling)가 될 수 없습니다. 객체의 형제를 가져올 때, 객체 자체는 항상 그 목록에서 제외됩니다.
2. 이 함수가 **다음** 형제만 가져옵니다. 예를 들어 목록 중간에 있는 임의의 행을 선택하고 `next_siblings`을 호출했다면 그 다음에 있는 형제들만 반환됩니다. 즉, 타이틀 행을 선택하고 `next_siblings`을 호출하면 타이틀 행 자체를 제외한 모든 테이블 행을 선택하게 됩니다.

> 선택은 명확하게 하십시오.  
이전 코드 bsObj.table.tr 심지어 bsObj.tr을 써서 테이블의 첫 번째 행을 선택했더라도 마찬가지로 잘 동작했을 겁니다. 하지만 번거로움을 무릅쓰고 위 코드를 길고 명확하게 작성했습니다.
```python
bsObj.find("table",{"id":"giftList"}).tr
```
설령 페이지에 테이블(또는 다른 타겟 태그)이 하나뿐인 것처럼 보일 때에도 실수를 하기 쉽습니다. 또한 페이지 레이아웃은 시시때때로 변합니다. 코드를 작성할 때는 페이지 처음에 있던 테이블이, 어느 날 보니 두 번째 또는 세 번째 테이블이 되어 있을 수도 있습니다. 스크레이퍼를 더 견고하게 만들려면 항상 태그를 가능한한 명확하게 선택하는 것이 최선입니다. 가능하다면 태그 속성을 활용하십시오.

`next_siblings`를 보완하는 `previous_siblings`함수도 있습니다. 이 함수는 원하는 형제 태그 목록의 마지막에 있는 태그를 쉽게 선택할 수 있을 때 사용합니다.  

물론 `next_siblings, previous_siblings`와 거의 같은 `next_sibling, previous_sibling` 함수도 있습니다.이들 함수는 리스트가 아니라 태그 하나만 반환한다는 점을 빼면 똑같이 동작합니다.

#### 부모 다루기

일반적으로 HTML 페이지에서 데이터를 수집할 목적으로 살펴볼 때는 보통 맨 위 계층에서 시작해 원하는 데이터까지 찾아들어가지만, 가끔 BeautifulSoup의 부모 검색함수 `.parent`와 `.parents`가 필요할 때가 있습니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html.parser")
print(bsObj.find("img", {"src":"../img/gifts/img1.jpg"}).parent.previous_sibling.get_text())
```
이 코드는 `../img/gifts/img1.jpg` 이미지가 나타내는 객체의 가격($15,00)을 출력합니다.  

HTML 페이지의 구조를 보면

```
<tr>
  - <td>
  - <td>
  - <td> # 3
    - "$15.00" # 4
  - <td> # 2
    - <img src="../img/gifts/img1.jpg"> # 1
```
1. 먼저 `src="../img/gifts/img1.jpg"`에 해당하는 이미지를 선택합니다.
2. 부모 태그(이 경우는 <td> 태그)를 선택합니다.
3. 2에서 선택한 <td>의 `previous_sibling`(이 경우 제품 가격이 들어있는 <td> 태그)를 선택합니다.
4. 태그에 들어있는 텍스트인 %15.00를 선택합니다.

### 2.3 정규 표현식

[정규표현식 (REGULAR EXPRESSIONS)]({{site.url}}/tech/2017/06/11/regular-2.html)  

정규 표현식이라는 이름은 정규 문자열을 식별하는 데 쓰이는데서 유래했습니다. 즉, 정규 표현식은 문자열이 주어진 규칙에 일치하는지, 일치하지 않는지 판단 할 수 있습니다. 정규 표현식은 긴 문서에서 전화번호나 이메일 주소 같은 문자열을 빠르게 찾아보려 할 때 무척 유용합니다.  

1. 글자 a를 최소한 한 번 쓰시오.
2. 그 뒤에 b를 정확히 다섯 개 쓰시오.
3. 그 뒤에 c를 짝수 번 쓰시오.
4. 마지막에 d가 있어도 되고 없어도 됩니다.

이 규칙을 따르는 문자열은 aaaabbbbbccccd, aabbbbbcc 등이 있습니다.(조합은 무한)

정규 표현식은 위에 나열한 규칙을 짧게 줄여 쓴 것에 불과합니다. 예를 들어 다음 정규 표현식은 위에 나열한 규칙을 네 개를 하나로 합친 겁니다.

> `aa*bbbb(cc)*(d | )`

이 문자열은 처음에는 좀 복잡해 보일 수 있지만, 쪼개서 보면 명확해집니다.  

`aa*`  
먼저 a를 쓰고 그 다음에 a*를 썻습니다. a*는 a가 몇 개든 상관없고 0개여도 된다는 뜻입니다. 이렇게 하면 a가 최소한 한 번은 있다는 뜻입니다.  

`bbbbb`  
특별한 것은 없습니다. b 다섯 개를 연이어 썻습니다.  

`(cc)*`  
c 짝수 개에 관한 규칙을 충족하려면 c 두 개를 괄호 안에 쓰고 그 뒤에 아스테리스크를 붙여, c의 **쌍** 이 임의의 숫자만큼 있음을 나타냅니다.(0쌍이어도 규칙에는 맞습니다)

`(d | )`  
표현식 중간에 있는 막대는 '이거 **아니면** 저거'라는 뜻입니다. 여기서는 'd 다음에 공백을 쓰거나, **아니면** d 없이 공백만 쓴다'는 뜻이 됩니다. 이렇게 하면 d가 최대 하나만 있고, 그 뒤에 공백이 이어지면서 문자열을 끝내게 됩니다.

> <http://regexr.com/>{:target="`_`blank"} 에서 테스트 해 볼 수 있습니다.

고전적인 정규 표현식 예제는 이메일 주소를 식별하는 문제입니다. 이메일 주소의 정확한 규칙은 메일 서버에 따라 미세하게 다를 수 있지만, 일반적인 규칙은 만들 수 있습니다. 다음 표의 첫 번째 열은 이메일 주소에 해당하는 규칙이고, 두 번째 열은 그에 대응하는 정규 표현식입니다.

규칙 1 | `[A-Za-z0-9\._+]+`
---|---
이메일 주소의 첫 번째 부분에는<br> 다음 중 최소한 하나가 포함되어야 합니다.<br> 대문자, 소문자, 숫자 0-9, 마침표(.),<br> 플러스 기호(+), 밑줄 기호(`_`)| A-Z, a-z, 0-9는 각각 A부터 Z까지의 대문자 중 하나, a부터 z까지의 소문자 중 하나, 0부터 9까지의 숫자 중 하나를 뜻합니다. 이렇게 가능한 경우를 모두 대괄호([])안에 넣으면 '대괄호에 들어 있는 것들 중 아무거나 하나'라는 뜻입니다. 마지막의 + 기호는 바로 앞에 있는 것이 최소한 한 번은 나타나야하며 최대 몇 개인지는 제한하지 않는다는 뜻입니다.

규칙 2 | @
---|---
그 다음에 @ 가 나타나야 합니다. | 매우 단순한 규칙입니다. 이메일 주소에는 @ 가 반드시 있어야 하며, 정확히 한개만 있어야 합니다.

규칙 3 | `[A-Za-z]+`
---|---
그 다음에는 반드시 대문자나 소문자가 최소한 하나 있어야 합니다. | @ 다음에 오는 도메인 이름의 첫 부분은 영문 대문자 또는 소문자여야 하고 최소한 글자 하나는 있어야 합니다.

규칙 4 | \.
---|---
그 다음에는 마침표가 옵니다. | 도메인 이름 다음에는 반드시 마침표가 있어야 합니다.

규칙 5 | `(com|org|edu|net)`
---|---
마디막으로, 이메일 주소는 com, org, edu, net 중 하나로 끝납니다. | 이 규칙은 이메일 주소의 두 번째 부분에서 마침표 다음에 나타날 수 있는 글자들을 나열한 것입니다.

이 규칙들을 합치면 정규 표현식이 만들어집니다.

`[A-Za-z0-9\._+]+@[A-Za-z]+\.(com|org|edu|net)`  

아무것도 없는 상태에서 정규 표현식을 만들 때는 목표하는 문자열이 어떤 형태인지 정확하게 나타내는 단계의 목록을 만드는 것으로 시작하는 것이 좋습니다. 맨 앞과 맨 뒤에는 특히 중의를 기울여야 합니다. 예를 들어 전화번호를 식별하는 정규 표현식을 만든다면 국가 코드와 기타 확장을 고려할지 정해야 합니다.

다음은 파이썬에서 가장 널리 쓰이는 정규 표현식 기호이며, 대부분의 문자열 타입에 대응할 수 있습니다.

기호 | 의미 | 예제 | 일치하는 문자열 예제
---|---|---|---
* | 바로 앞에 있는 문자, 하위 표현식, 대괄호로 묶인 문자들이 0번 이상 나타납니다. | a*b* | aaaaaa, aaabbbbb, bbbbb
+ | 바로 앞에 있는 문자, 하위 표현식, 대괄호로 묶인 문자들이 1번 이상 나타납니다. | a+b+ | aaaaaaab, aaabbbbb, aaabbbbb
[] | 대괄호 안에 있는 문자 중 하나가 나타납니다. | [A-Z]* | APPLE, CAPITALS, QWERTY
() | 그룹으로 묶인 하위 표현식입니다. 정규 표현식을 평가할 때에는 하위 표현식이 가장 먼저 평가됩니다. | (a*b)* | aaabaab, abaaab, ababaaaaab
{m, n} | 바로 앞에 있는 문자, 하위 표현식, 대괄호로 묶인 문자들이 m번 이상, n번 이하 나타납니다. | a{2,3}b{2,3} | aabbb, aaabbb, aabb
[^] | 대괄호 안에 있는 문자를 제외한 문자가 나타납니다. | [^A-Z]* | apple, lowercase, qwerty
`|` | `|`로 분리된 문자, 문자열, 하위 표현식 중 하나가 나타납니다. `|`는 '파이프'입니다. | `b(a|i|e)d` | bad, bid, bed
. | 문자 하나(글자, 숫자, 기호, 공백 등)가 나타닙니다. | b.d | bad, bzd, b$d, b d
^ | 바로 뒤에 있는 문자 혹은 하위 표현식이 문자열의 맨 앞에 나타납니다. | ^a | apple, asdf, a
\ | 특수 문자를 원래 의미대로 쓰게 하는 이스케이프 문자입니다. | `\.` `\|` `\\` | `. | \`
`$` | 정규 표현식 마지막에 종종 쓰이며, 바로 앞에 있는 문자 또는 하위 표현식이 문자열의 마지막이라는 뜻입니다. 이 기호를 쓰지 않는 정규 표현식은 사실상 `.*`가 마지막에 있는 것이나 마찬가지여서 그 뒤에 무엇이 있든 전부 일치합니다. ^ 기호의 반대라고 생각해도 됩니다. | `[A-Z]*[a-z]*$` | ABCabc, zzzyx, Bob
?! | '포함하지 않는다'는 뜻입니다. 이 기호 쌍 바로 다음에 있는 문자(또는 하위 표현식)는 해당 위치에 나타나지 않습니다. 이 기호는 조금 혼란스러울 수 있습니다. 배제한 문자가 문자열의 다른 부분에는 나타나도 되니까요. 특정 문자를 완벽히 배제하려면 ^과 $ 를 앞뒤에 쓰세요. | `^((?![A-Z]).)*$` | no-caps-here, $ymb0ls a4e f!ne

> 정규 표현식은 언어마다 다릅니다.

### 2.4 정규 표현식과 BeautifulSoup

웹 스크레이핑에서도 BeautifulSoup와 정규 표현식을 함께 쓸 수 있습니다. 사실 문자열 매개변수를 받는 대부분의 함수(예를 들면 `find(id="aTagIdHere")`는 정규 표현식도 매개변수로 받을 수 있습니다.

http://www.pythonscraping.com/pages/page3.html 페이지를 스크랩하며 예제를 봅니다. 이 사이트에는 다음과 같은 형태의 제품 이미지가 여러개 있습니다.

> `<img src="../img/gifts/img3.jpg">`

제품 이미지 URL을 모두 수집하는 건 매우 단순해 보입니다. `.find_all("img")`로 모든 이미지 태그를 가져오면, 로고 등 불필요한 이미지가 있을뿐 아니라, 최신 웹사이트에는 종종 숨은 이미지, 공백 유지와 요소 정렬에 쓰이는 빈 이미지, 기타 알아채지 못하는 이미지 태그가 여럿 있습니다. 페이지에 있는 이미지가 모두 제품 이미지라고 확신할 수는 없습니다.

페이지 레이아웃이 바뀔 수도 있고, 어떤 이유로든 페이지에서 이미지가 차지하는 **위치** 를 토대로 태그를 찾고 싶지 않을 수도 있습니다. 웹사이트 전체에 무작위로 퍼져 있는 특정 요소나 데이터를 수집하려 할 때 이렁 일이 일어날 수 있습니다. 예를 들어 세일 상품 이미지는 일부 페이지에서는 특별한 레이아웃을 통해 상단에 노출되지만, 다른 페이지에서는 노출되지 않을 수도 있습니다.  

해결책은 태그 자체를 식별하는 무언가를 찾는 것입니다. 여기서는 제품 이미지의 파일 경로로 확인할 수 있습니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html.parser")
images = bsObj.find_all("img", {"src":re.compile("\.\.\/img\/gifts/img.*\.jpg")})
for image in images:
    print(image["src"])
```
import re 로 정규 표현식을 임포트했습니다. 이 코드틑 `../img/gifts/img`로 시작해서 `.jpg`로 끝나는 이미지의 상대 경로만 출력합니다.

```
../img/gifts/img1.jpg
../img/gifts/img2.jpg
../img/gifts/img3.jpg
../img/gifts/img4.jpg
../img/gifts/img6.jpg
```
정규 표현식은 BeautifulSoup 표현식 어디에든 매개변수로 삽입할 수 있어서, 매우 유연하게 원하는 요소를 찾을 수 있습니다.
