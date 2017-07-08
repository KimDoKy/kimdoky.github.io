---
layout: post
section-type: post
title: crawling - P1.스크레이퍼 제작 _ cahp 3. 크롤링 시작하기
category: python
tags: [ 'python' ]
---

여러 페이지, 여러 사이트를 이동하는 스크레이퍼를 통해 실제 문제를 다룹니다.

웹 크롤러의 핵심은 재귀입니다. 웹 크롤러는 URL에서 페이지를 가져오고, 그 페이지를 검사해 다른 URL을 찾고, 다시 그 페이지를 가져오는 작업을 무한히 반복합니다.

하지만 웹 크롤링이 가능하다는 것과 웹 크롤링을 해야 한다는 것은 다릅니다. 웹 크롤러를 사용할 때는 반드시 대역폭에 세심한 주의를 기울여야 하며, 타겟 서버의 부하를 줄일 방법을 생각해야 합니다.

## 3.1 단일 도메인 내의 이동

'위키백과의 여섯다리' 혹은 '케빈 베이컨의 여섯다리'에 대해서 알아야합니다. 두 게임 모두 목표는 관계가 없어 보이는 두 대상을 연결하는 겁니다.

> 케빈 베이컨의 여섯다리 : 어떤 배우와 케빈 베이컨까지 최단의 연결 고리를 만드는 놀이이다. 이는 케빈 케이컨이 매우 다작(多作)하는 배우라는 것이 근거가 된다. 같이 출연한 영화가 연결의 고리가 되는데, 예를 들어 케빈 베이컨과 같은 영화에 출연했던 배우는 모두 한 다리만에 베이컨까지 닿을 수 있고 그 배우들과 같이 출연했던 배우는 두 다리만에 베이컨까지 닿을 수 있다는 식이다. 이렇게 특정 배우로부터 케빈 베이컨에게까지 최소 몇 다리만에 도달 할 수 있는지를 나타내는 수를 ‘베이컨 수’라고 한다.

이 섹션에서는 위키백과의 여섯 다리를 푸는 프로젝트를 시작합니다. 에릭 아이들의 페이지(https://en.wikipedia.org/wiki/Eric_Idle)에서 시작해 케빈 베이컨의 페이지(https://en.wikipedia.org/wiki/Kevin_Bacon)에 닿는 최소한의 클릭수를 찾는 겁니다.

> 위키백과의 서버 부하에 대한 대책은?  
위키백과 재단에 따르면 위키백과 방문자는 대략 초당 2,500명이며, 그중 99퍼센트 이상이 다른 위키백과 도메인으로 이동합니다. 워낙 트래픽이 대단하니, 여기서 만들 웹 스크레이퍼 정도는 위키백과 서버에 별 영향을 끼치지 않을 겂니다. 하지만 코드 샘플을 집중적으로 사용하거나 위키백과 사이트를 스크랩하는 프로젝트를 만든다면 위키백과 재단에 기부하는 것을 권합니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html, "html.parser")
for link in bsObj.find_all("a"):
    if 'href' in link.attrs:
        print(link.attrs['href'])
```
링크 목록을 살펴보면 예상대로 'Apollo 13', 'Philadelphia'와 같은 원하지 않는 것들도 포함되어 있습니다.  

사실 위키백과의 모든 페이지에는 사이드바, 푸터, 헤더 링크가 있고 카테고리 페이지, 토론 페이지 등 그외에도 관심 없는 항목의 페이지를 가리키는 링크가 많이 있습니다.

책 저자의 친구는 이러한 스크레이퍼를 만들다가 내부 링크가 항목 페이지인지 아닌지를 판단하는 100행이 넘는 필터링 함수를 만들었다고 합니다. '항목 링크'와 '다른 링크'를 구분하는 패턴을 발견하는데 시간을 투자하였고 어떠한 규칙을 발견하였습니다.

- 이 링크들은 id 가 bodyContent인 div 안에 있습니다.
- URL에는 세미클론이 포함되어 있지 않습니다.
- URL은 /wiki/ 로 시작합니다.

이 규칙을들 활용하면 항목 페이지를 가리키는 링크만 가져오도록 수정할 수 있습니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html, "html.parser")
for link in bsObj.find("div", {"id":"bodyContent"}).find_all("a", href=re.compile("^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        print(link.attrs['href'])
```
이 코드를 실행하면 케빈 베이커의 위키백과 항목에서 다른 항목을 가리키는 모든 링크 목록을 볼 수 있습니다.

특정 위키백과 항목에서 다른 항목을 가리키는 모든 링크 목록을 가져오는 이 스크립트도 물론 흥미롭지만, 현실적으로 쓸모는 없습니다. 이 코드를 다음과 같은 형태로 바꿀 수 있어야 합니다.

- /wiki/<article_name> 형태인 위키백과 항목 URL을 받고, 링크된 항목 URL 목록 전체를 반환하는 getLinks 함수
- 시작 항목에서 getLinks를 호출하고 반환된 리스트에서 무작위로 항목 링크를 선택하여 getLinks를 다시 호출하는 작업을, 프로그램을 끝내거나 새 페이지에 항목 링크가 없을 때까지 반복하는 메인 함수

다음 코드가 그와 같은 코드입니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re
random.seed(datetime.datetime.now())

def getLinks(articleUrl):
    html = urlopen("https://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id":"bodyContent"}).find_all("a", href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks("/wiki/Kevin_Bacon")
while len(links) > 0:
    newArticle = links[random.randint(0, len(links) -1)].attrs["href"]
    print(newArticle)
    links = getLinks(newArticle)
```

이 프로그램은 필요한 라이브러리를 임포트한 후 처음 하는 일은 현재 시스템 시간을 가지고 난수 발생기를 실행합니다. 이렇게 하면 프로그램을 실행할 때마다 위키백과 항목들 속에서 새롭고 흥미로운 무작위 경로를 찾을 수 있습니다.

> ### 의사 난수와 무작위 시드  
앞의 코드에서 파이썬의 난수 발생기를 사용해 각 페이지에서 무작위로 항목을 선택해, 위키백과를 무작위로 이동했습니다. 하지만 난수는 조심해서 사용해야 합니다.  
>
컴퓨터는 정확한 답을 계산하는데 강하지만, 뭔가를 창조하는 데는 약합니다. 따라서 난수를 만드는 것도 매우 어려운 일입니다. 대부분의 알고리즘은 균등하게 분배되고 예측하기 어려운 숫자들을 만들어내기 위해 최선을 다하며, 이런 알고리즘이 기동하기 위해서는 시드 숫자가 필요합니다. 시드 숫자가 일치하면 그 결과인 난수 배열도 항상 일치합니다. 따라서 시스템 시간으로 난수 배열을 만들면 항목도 무작위로 고를 수 있습니다.  
>
파이썬의 의수 난수 발생기는 **메르센 트위스터 알고리즘** 을 사용합니다. 이 알고리즘은 예측하기 어렵고 균일하게 분산된 난수를 만들긴 하지만, 프로세서 부하가 좀 있는 편입니다. 이렇게 훌륭한 난수를 공짜로 얻을 수는 없는거죠.

그 다음 getLinks 함수를 정의합니다. 이 함수는 /wiki/...  형태로 된 URL을 받고 그 앞에 위키백과 도메인 이름인 http://en.wikipedia.org 를 붙여, 그 위치의 HTML에서 BeautifulSoup 객체를 가져옵니다. 그리고 앞에서 설명한 매개변수에 따라 항목 링크 태그 목록을 추출해서 반환합니다.  

이 프로그램은 초기 페이지인 https://en.wikipedia.org/wiki/Kevin_Bacon 의 링크 목록을 links 변수로 정의하며 시작합니다. 그리고 루프를 실행해서 항목 링크를 무작위로 선택하고, 선택한 링크에서 href 속성을 추출하고, 페이지를 출력하고, 추출한 URL에서 새 링크 목록을 가져오는 작업을 반복합니다.  

물론 단순히 페이지에서 페이지를 이동하는 스크레이퍼를 만들었다고 위키백과의 여섯다리 문제가 풀리는 것은 아닙니다. 반드시 결과 데이터를 저장하고 분석할 수 있어야 합니다.

> ### 예외 처리를 잊지 마세요!  
앞의 코드는 간결함을 위해 예외 처리를 생략했지만, 잠재적 함정이 많이 있습니다. 예를 들어 bodyContent 태그의 이름이 바뀐다면 충돌이 일어날 것입니다.  
주의 깊게 살펴보며 진행한다면 이 스크립트는 별문제 없지만, 자동으로 실행되는 실무 코드에서는 예외 처리가 훨씬 더 많이 필요할 것입니다.

## 3.2 전체 사이트 크롤링

### 3.2.1 전체 사이트에서 데이터 수집

## 3.3 인터넷 크롤링

## 3.4 스크래파이를 사용한 크롤링
