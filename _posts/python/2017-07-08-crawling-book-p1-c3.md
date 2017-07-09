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

이전 섹션에서는 링크에서 링크로 움직이며 웹사이트를 무작위로 이동했습니다. 하지만 사이트의 모든 페이지를 어떤 시스템에 따라 분류하거나 검색해야 한다면 이런 방식은 적합하지 않습니다. 사이트 전체 크롤링, 특히 거대한 사이트의 크롤링은 메모리를 많이 요구하며 크롤링 결과를 바로 저장할 데이터베이스가 준비된 어플리케이션에 적합합니다. 하지만 이런 애플리케이션을 실제 규모로 실행하지 않아도, 어떻게 움직이는지 알아보는건 가능합니다.

> ### 다크 웹과 딥 웹  
딥 웹(deep web), 다크 웹(dark web), 히든 웹(hidden web)같은 용어들이 최근 많이 생겼습니다.  
딥 웹은 간단히 말해 **표면 웹(surface web)** , 즉 검색 엔진에서 저장하는 부분을 제외한 나머지 웹을 일컫습니다. 정확하지는 않지만, 딥 웹은 인터넷의 9할 정도를 차지합니다. 구글도 폼을 전송하거나, 최상위 도메인에서 링크되지 않은 페이지를 찾아내거나, robots.txt 로 막혀있는 사이트를 조사할 수는 없으므로, 표면 웹은 비교적 작은 비욜을 차지합니다.  
다크 웹은 다크넷, 다크 인터넷이라고도 부르며 완벽히 다른 종류입니다. 다크 웹은 기존 네트워크 기반 구조에서 동작하기는 하지만, Tor 클라이언트와 HTTP 위에서 동작하며 보안 채널로 정보를 교환하는 애플리케이션 프로토콜을 사용합니다. 다크 웹도 다른 사이트와 마찬가지로 스크랩할 수는 있습니다.  
다크 웹과 달리 딥 웹은 비교적 쉽게 스크랩할 수 있습니다.

사이트 전체를 이동하는 웹 스크레이퍼에는 여러 장점이 있습니다.

#### 사이트맵 생성

예를 들어 중요한 클라이언트가 웹사이트 재설계 비용을 문의했지만, 현재 사용중인 콘텐츠 관리 시스템 내부에 접근 권한을 주기 꺼리고 사이트맵도 없는 상황입니다. 이런 경우 사이트 전체를 이동하는 크롤러를 이용해 내부 링크를 모두 수집하고, 그 페이지들을 사이트의 실제 폴더 구조와 똑같이 정리 할 수 있습니다. 이를 통해 존재하는지조차 몰랐던 부분들을 빨리 발견할 수 있고, 다시 설계해야 하는 페이지가 얼마나 되고 이동해야 할 컨텐츠가 얼마나 되는지 정확히 산출 할 수 있습니다.

#### 데이터 수집

어떤 클라이언트는 글(이야기, 블로그 포스트, 뉴스 기사 등)을 수집해서 전문화 검색 플랫폼의 프로토타입을 만들고 싶다고 의뢰했습니다. 이들 웹사이트는 철저히 탐색할 필요는 없지만, 광범위하게 진행해야 했습니다.(데이터를 가져올 사이트가 많지는 않았습니다.) 각 사이트를 재귀적으로 이동하는 크롤러를 만들어 기사 페이지에서만 데이터를 수집할 수 있었습니다.

사이트를 철저히 크롤링하려면 보통 홈페이지 같은 경우 최상위 페이지에서 시작해, 그 페이지에 있는 내부 링크를 모두 검색합니다. 검색한 링크를 모두 탐색하고, 거기서 다시 링크가 발견되면 크롤링 다음 라운드가 시작됩니다.

당연히 일은 엄청나게 커집니다. 모든 페이지에 내부 링크가 10개씩 있고 사이트가 다섯 단계로 구성되어 있다면(중간 규모 사이트에서는 매우 일반적인 깊이입니다), 최소 105 페이지, 최대 100,000페이지를 찾아야 사이트를 철저히 탐색했다고 할 수 있습니다. (최대 100,000페이지가 되는 이유는 내부 링크 중 상당수가 중복이기 때문입니다)

같은 페이지를 두 번 크롤링하지 않으려면 발견되는 내부 링크가 모두 일정한 형식을 취하고, 프로그램이 동작하는 동안 계속 유지되는 리스트에 보관하여야 합니다. 새로운 링크만 탐색하고 거기서 다른 링크를 검색해야 합니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+ pageUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    for link in bsObj.find_all("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # 새 페이지를 발견
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("")
```
웹 크롤링이 어떻게 동작하는지 충분히 보기위해, 이전에 사용한 내부 링크 기준을 완화했습니다. 이번에는 스크레이퍼가 항목 페이지만 찾는게 아니라, /wiki/로 시작하는 모든 링크를 찾으며, div의 id아 콜론이 있는지 없는지도 검사하지 않습니다.(항목 페이지에는 콜론이 들어 있지 않지만 파일 업로드 페이지나 토론 페이지, 또는 비슷한 링크들은 URL에 콜론이 있을 수도 있습니다.)  

먼저 getLinks에 빈 URL을 넘겨 호출합니다. 함수 내부에서는 빈 URL의 앞에 http://en.wikipedia.org 을 붙여 위키백과 첫 페이지 URL로 바꿉니다. 다음에는 첫 번째 페이지의 각 링크를 순회하며 전역 변수인 pages에 들어 있는지 아닌지를 검사합니다. pages는 스크립트가 이미 발견한 페이지의 세트입니다. pages에 들어 있지 않은 링크라면 리스트에 추가하고, 화면에 출력한 다음, getLinks 함수를 재귀적으로 호출합니다.

> ### 재귀에 관한 경고  
파이썬은 기본적으로 재귀 호출을 1,000회로 제한합니다. 위키백과의 링크 네트워크는 대단히 넓으므로 이 프로그램은 결국 재귀 제한에 걸려서 멈추게 됩니다. 멈추는 일을 막으려면 재귀 카운터를 삽입하거나 다른 방법을 강구해야 합니다.  
링크 깊이가 1,000단계까지 들어가지 않는 사이트에서는 이 방법도 보통 잘 동작하지만, 가끔 예외가 있습니다. 예를 들어 블로그 포스트를 가리키는 내부 링크를 일정한 규칙에 따라 생성하는 웹사이트가 있습니다. 그 규칙은 '현재 보고 있는 페이지 URL을 취해 /blog/title_of_blog.php를 덧붙인다'는 규칙이었습니다.  
문제는 URL에 이미 /blog/가 들어 있는 페이지에도 /blog/title_of_blog.php를 붙인다는 것입니다. 그러면 /blog/가 또 추가되죠. 결국 /blog/blog/blog.../blog/title_of_blog.php 같은 URL 까지 방문해야 합니다.  
결국 URL이 너무 우스꽝스럽지 않은지, 무한 루프로 보이는 조각이 있는지 체크하는 코드를 삽입해야 합니다. 그렇게 하지 않으면 제한에 걸려 금새 정지되었을 것입니다.

### 3.2.1 전체 사이트에서 데이터 수집

웹 크롤러가 페이지와 페이지 사이를 옮겨 다니기만 한다면 쓸모가 없을 것입니다. 페이지 제목, 첫 번째 문단, 편집 페이지를 가리키는 링크를 수집하는 스크레이퍼를 만들어봅니다.  

가장 먼저 해야할 일은, 사이트의 페이지 몇 개를 살펴보며 패턴을 찾는 것입니다. 위키백과에서 항목 페이지와 개인정보 정책 페이지 같은 항목 외 페이지를 살펴봤다면 다음과 같은 패턴이 있음을 알 수 있습니다.

- 항목 페이지든 편집 내역 페이지든 상관없이 항상 h1 태그 안에 있으며 h1 태그킄 페이지당 하나만 존재합니다.
- 모든 바디 텍스트는 `div#bodyContent` 태그에 들어 있습니다. 더 정확하게 첫 번째 문단의 텍스트만 선택하려 한다면 `div#mv-content-text` -> p로 첫 번째 문단 태그만 선택하는 편이 나을 것입니다. 이 방법은 콘텐츠 텍스트 섹션이 없는 파일 페이지를 제외한 모든 콘텐츠 페이지에 적용됩니다.
- 편집 링크는 항목 페이지에만 존재합니다. 존재한다면 `li#ca-edit -> span -> a`로 찾을 수 있습니다.

기본 크롤링 코드를 수정해서 크롤러와 데이터 수집(최소한 출력은 가능한) 기능이 있는 프로그램을 만들 수 있습니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("http://en.wikipedia.org"+ pageUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id="mw-content-text").find_all("p")[0])
        print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
    except AttributeError:
        print("This page is missing something! No worries though!")
    for link in bsObj.find_all("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print("-----------\n"+newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks("")
```
이 프로그램의 for 루프는 이전의 클롤링 프로그램과 거의 같습니다. 출력되는 콘텐츠를 더 졍확히 구분하기 위해 대시를 추가했습니다.  
원하는 데이터가 모두 페이지에 있다고 확신할 수는 없으므로, 각 print문은 페이지에 존대할 확률이 높은 순서대로 정렬했습니다. <h1> 타이틀 태그는 모든 페이지에 존재하므로 이 데이터를 가장 먼저 가져옵니다. 파일 페이지를 제외하면, 대부분의 페이지에 텍스트 콘텐츠가 존재하므로 이것이 두 번째로 가져올 데이터입니다. 편집 버튼은 제목과 텍스트 콘텐츠가 모두 존재하는 페이지에만 있지만, 그렇다고 100%는 아닙니다.

> ### 패턴에 따라 필요한 작업이 다릅니다.
예외 핸들러 안에 여러 행을 넣는 것은 위험합니다. 우선 어떤 행에서 예외가 일어날지 모릅니다. 또한 어떤 이유로든 페이지에 편집 버튼만 있고 제목이 없다면 편집 버튼도 가져오지 않게 됩니다. 하지만 원하는 데이터가 사이트에 있을 확률에 순서가 있고, 일부 데이터를 잃어도 되거나 자세한 로그를 유지할 필요가 없는 경우에는 별문제 없습니다.

지금까지는 데이터를 출력하기만 했지, '수집'을 하지는 않았습니다. 물론 터미널에서 데이터를 가공하기는 쉽지 않습니다.

## 3.3 인터넷 크롤링

"구글 같은 기업은 어떻게 만들어지나요?"  
"첫째, 수십억 달러를 모아 세계에서 가장 훌륭한 데이터 센터를 만들고 세계 곳곳에 배치합니다. 두 번째로, 웹 크롤러를 만듭니다."  

구글이 1994년 처음 시작되었을 때는 단 두명의 스탠퍼드 대학원생뿐이었고, 그들이 가진 건 낡은 서버와 파이썬 웹 크롤러뿐이었습니다.  

웹 크롤러는 여러 가지 최신 웹 기술의 핵심에 있고, 웹 크롤러를 사용하기 위해 반드시 거대한 데이터센터가 필요하지는 않습니다. 도메인 간 데이터 분석을 위해서는 인터넷의 무수히 많은 페이지에서 데이터를 가져오고 해석할 수 있는 크롤러가 필요합니다.  

이전과 마찬가지로 지금부터 만들 웹 크롤러도 링크를 따라 페이지와 페이지를 이동합니다. 하지만 이번에는 외부 링크를 무시하지 않고 따라갑니다. 각 페이지에 관한 정보를 기록 할 수 있는지 알아봅니다. 여태까지 했던 것처럼 도메인 하나만 다루는 것보다는 어려울 것입니다. 웹 사이트마다 레이아웃이 완전히 다르기 때문입니다. 따라서 어떤 정보를 찾을지, 어떻게 찾을지 매우 유연한 사고방식을 가져야 합니다.

> ### 지금부터 일어날 일은 아무도 모릅니다.  
다음 섹션에서 사용할 코드는 인터넷 **어디든지** 갈 수 있음을 염두해 두어야 합니다. 위키백과의 여섯 다리를 이해했다면 http://www.sesamestreet.org/ 에서 단 몇 번의 이동으로도 이상한 사이트에 도달할 수 있다는 것을 이해할 것입니다.  
즉, 법 규정이나 성적인 사이트의 텍스트를 읽어올 수도 있기 때문에, 실행 할 때는 주의를 기울여야 합니다.(미성년자는 부모와 상의하세요.)

단순히 외부 링크를 단치는 대로 따라가는 크롤러를 만들기 전에 먼저 자신에게 질문을 합니다.

- 내가 수집하려 하는 데이터는 어떤 것인가? 정해진 사이트 몇 개만 수집하면 되나? (이런 경우, 거의 틀림 없이 더 쉬운 방법이 있습니다.) 아니면 그런 사이트가 있는지조차 몰랐던 사이트에도 방문하는 크롤러가 필요할까?
- 크롤러가 특정 웹사이트에 도달하면, 즉시 새 웹사이트를 가리키는 링크를 따라가야 할까? 아니면 한동안 현재 웹사이트에 머물면서 파고들어야 할까?
- 특정 사이트를 스트랩에서 제외할 필요는 없나? 비 영어권 콘텐츠도 수집해야 할까?
- 만약 크롤러가 방문한 사이트의 웹마스터가 크롤러의 방문을 알아차렸다면 나 자신을 법적으로 보호할 수 있을까?

파이썬 함수를 결합하면 다양한 웹 스크레이핑을 실행하는 코드를 쉽게 만들 수 있고, 이는 50줄도 안되는 코드로도 충분히 가능합니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

# 페이지에서 발견된 내부 링크를 모두 목록으로 만듭니다.
def getInternalLinks(bsObj, icludeUrl):
    iternalLinks = []
    # / 로 시작하는 링크를 모두 찾습니다.
    for link in bsObj.find_all("a", href=re.compile("^(/|.*" + includeUrl + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

# 페이지에서 발견된 외부 링크를 모두 목록으로 만듭니다.
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    # 현재 URL을 포함하지 않으면서 http나 www로 시작하는 링크를 모두 찾습니다.
    for link in bsObj.find_all("a", href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html, "html.parser")
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(startingPage)
        return getNextExternalLink(internalLinks[random.randint(0, len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink("http://oreilly.com")
    print("Random external link is: " + externalLink)
    followExternalOnly(externalLink)

followExternalOnly("http://oreilly.com")
```

위 프로그램은 http://oreilly.com 에서 시작해 외부 링크에서 외부 링크로 무작위로 이동합니다.

```
~/Git/Study/crawling/web_scraping/chap3(master*) » python part1_chap3_3.py
Random external link is: https://www.linkedin.com/company/oreilly-media
Random external link is: http://fb.co/OReilly
Random external link is: https://www.youtube.com/user/OreillyMedia
Random external link is: http://twitter.com/oreillymedia
...
```

웹 사이트의 첫 번째 페이지에 항상 외부 링크가 있다는 보장은 없습니다. 여기서는 외부 링크를 찾기 위해 이전 크롤링 코드와 비슷한 방법, 즉 외부 링크를 찾을 때까지 웹 사이트를 재귀적으로 파고드는 방법을 사용하였습니다.

![]({{site.url}}/img/post/python/crawling/p1c3_1.png)
> 인터넷 사이트를 탐색하는 스크립트 순서도

작업을 '이 페이지에 있는 모든 외부 링크를 찾는다'같은 단순한 함수로 나누면, 나중에 코드를 다른 크롤링 작업에 쓸 수 있도록 리팩토링하기 쉽습니다. 예를 들어 사이트 전체에서 외부 링크를 검색하고 각 링크마다 메모를 남기고 싶다면 다음과 같은 함수를 추가하면 됩니다.

```python
# 사이트에서 찾은 외부 URL을 모두 리스트로 수집
allExtLinks = set()
allIntLinks = set()

def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    internalLinks = getInternalLinks(bsObj, splitAddress(domain)[0])
    externalLinks = getExternalLinks(bsObj, splitAddress(domain)[0])

    for link in externalLinks:
        if link not in allExtLinks:
            allExtLinks.add(link)
            print(link)
    for link in internalLinks:
        if link == "/":
            link = domain
        elif link[0:2] == "//":
            link = "http:" + link
        elif link[0:1] == "/":
            link = domain + link

        if link not in allIntLinks:
            print("About to get link: " + link)
            allIntLinks.add(link)
            getAllExternalLinks(link)

domain = "http://oreilly.com"
getAllExternalLinks(domain)
```
이 코드는 크게 루프 두 개로 생각할 수 있습니다. 하나는 내부 링크를 수집하고, 다른 하나는 외부 링크를 수집하면서 서로 연관되게 동작합니다.

![]({{site.url}}/img/post/python/crawling/p1c3_2.png)
> 웹 사이트의 외부 링크를 모두 수집하는 크롤러의 순서도

실제 코드를 작성하기 전에 그 코드가 무슨 일을 하는지 다이어그램을 그려보거나 메모해보는 습관을 들이는 게 좋습니다. 크롤러가 복잡해지면 이런 습관이 시간을 매우 많이 절약해주고, 좌절하는 일도 훨씬 줄어들 것입니다.

> ### 리다이렉트 처리  
리다이렉트를 사용하면 같은 웹 페이지를 다른 도메인 이름 아래에서 볼 수 있습니다. 리다이렉트는 크게 두 가지입니다.
- 서버 쪽 리다이렉트. 페이지를 불러오기 전에 URL이 바뀝니다.
- 클라이언트 쪽 리다이렉트. 이따금 페이지를 리다이렉트하기 전에 'You will be directed in 10 seconds..' 같은 메시지가 나올 때로 있습니다.
>
이 섹션에서는 서버 쪽 리다이렉트를 다룹니다.  
서버 쪽 리다이렉트에 대해서는 보통 신경 쓸 일이 없습니다. 파이썬 3.x애서 제공하는 urllib 라이브러리가 리다이렉트를 자동으로 처리해줍니다. 그저 이따금 크롤링하는 페이지 URL이 입력한 URL과 정확히 일치하지 않을 수 있다는 것만 기억하면 됩니다.

## 3.4 스크래파이를 사용한 크롤링
