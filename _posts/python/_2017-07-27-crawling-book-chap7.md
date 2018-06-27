---
layout: post
section-type: post
title: crawling - P2. 고급 스크레이핑 _ chap 7. 지저분한 데이터 정리하기
category: python
tags: [ 'python' ]
---

웹 스크레이핑에서는 제한된 곳에서만 데이터를 수집할 수는 없을 때가 많습니다.  

잘못된 구두점, 일관성 없는 대문자 사용, 줄바꿀, 오타 등 지저분한 데이터는 웹의 큰 문제입니다. 이번 챕터에서는 도구와 테크닉 코드 작성 방법을 바꿔서 데이터 소스에서 문제가 발생하지 않게 막는 방법, 일단 데이터베이스에 들어온 데이터를 정리하는 방법을 다룹니다.

## 7.1 코드로 정리하기

예외를 처리하는 코드도 중요하지만, 예상 못 한 상황에 대응하는 방어적인 코드도 중요합니다.  

언어학에서 **n-그램** 은 텍스트나 연설에서 연속으로 나타난 단어 n개를 말합니다. 자연으를 분석할 때는 공통적으로 나타나는 n-그램, 또는 자주 함께 쓰이는 단어 집합으로 나눠서 생각하는게 편리할 때가 많습니다.  

이 섹션에서는 n-그램의 분석보다는 우선 정확한 형태를 갖춘 n-그램을 찾는 데 초점을 둡니다.  

다음 코드는 파이썬 프로그래민 언어에 관한 위키백과 항목에서 찾은 2-그램 목록을 반환합니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup

def ngrams(input, n):
    input = input.split(' ')
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html, "html.parser")
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()
ngrams = ngrams(content, 2)
print(ngrams)
print("2-grams count is: "+str(len(ngrams)))
```

ngrams 함수는 입력 문자열을 받고, 모든 단어가 공백으로 구분되었다고 가정하여 연속된 단어로 나눈 다음 n-그램 배열(여기서는 2-그램)을 만들어 반환합니다.

```
['Python', 'programs'], ['programs', 'on'], ['on', 'the'], ['the', '.NET']
```

하지만 동시에 쓸모없는 것들고 잔뜩 반환합니다.

```
 ['DMOZ\n\n\n\n\n\n\n\nv\nt\ne\n\n\nProgramming', 'languages\n\n\n\n\n\n\nComparison\nTimeline\nHistory\n\n\n\n\n\n\n\n\nAssembly\nBASIC\nC\nC++\nC#\nCOBOL\nFortran\nGo\nHaskell\nJava\nJavaScript'], ['languages\n\n\n\n\n\n\nComparison\nTimeline\nHistory\n\n\n\n\n\n\n\n\nAssembly\nBASIC\nC\nC++\nC#\nCOBOL\nFortran\nGo\nHaskell\nJava\nJavaScript', '(JS)\nKotlin\nLisp\nLua\nObjective-C\nPascal\nPerl\nPHP\nPython\nRuby\nShell\nSmalltalk\nSwift\nVisual'], ['(JS)\nKotlin\nLisp\nLua\nObjective-C\nPascal\nPerl\nPHP\nPython\nRuby\nShell\nSmalltalk\nSwift\nVisual', 'Basic'], ['Basic', '.NET'],
 ```

 또한 마지막 단어를 제외하고 만나는 모든 단어는 8,548개의 2-그램이 만들어졌습니다. 감당하기 어려운 량입니다.  

 정규표현식을 써서 `\n` 같은 이스케이프 문자를 제거하고 유니코드 문자도 제거하면 어느 정도 정리된 출력 결과를 얻을 수 있습니다.

 ```python
def ngrams(input, n):
    input = re.sub('\n+', " ", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    print(input)
    input = input.split(' ')
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output
```

이 코드는 먼저 줄바꿈 문자를 모두 공백으로 바꾸고, 연속됨 공백을 하나로 합쳐서 모든 단어와 단어 사이에 공백이 하나만 있게 합니다. 다음에는 콘텐츠 인코딩을 UTF-8로 바꿔서 이스케이프 문자를 없앱니다.  

이런 단계를 거치면 함수의 출력 결과가 크게 개선되지만, 여전히 몇몇 문제가 남아 있습니다.

```
['Pythoneers.[43][44]', 'Syntax'], ['7', '/'], ['/', '3'], ['3', '==']
```

이제 이 데이터를 처리하는 규칙을 이상적인 데이터인 데이터에 가까워지기 위해 몇 가지 규칙을 추가해야 합니다.

- i와 a를 제외한, 단 한글자로 된 '단어'는 버려야 합니다.
- 위키백과 인용 표시인 대괄호로 감싼 숫자도 버려야 합니다.
- 구두점도 버려야 합니다.

이제 '청소 작업' 목록이 좀 길어졌으니, cleanInput 함수로 분리하는 것이 좋습니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string

def cleanInput(input):
    input = re.sub('\n', " ", input)
    input = re.sub('\[[0-9]*\]', "", input)
    input = re.sub(' +', " ", input)
    input = bytes(input, "UTF-8")
    input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

def ngrams(input, n):
    input = cleanInput(input)
    output = []
    for i in range(len(input)-n+1):
        output.append(input[i:i+n])
    return output
```
import string과 string.punctuation으로 파이썬이 구두점이라 생각하는 모든 글자의 리스트를 얻었습니다. 파이썬 콘솔에서 string.punctuation의 결과를 확인할 수 있습니다.

```python
>>> import string
>>> print(string.punctuation)
!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
```

콘텐츠의 모든 단어를 순회하는 루프 안에서 item.strip(string.punctuation)을 사용하면 단어 양 끝의 구두점을 모두 없앨 수 있습니다. 물론 하이픈이 들어간 단어는 바뀌지 않습니다.

이제 훨싼 깔끔한 2-그램을 얻을 수 있습니다.

```
['Python', 'programs'], ['programs', 'into'], ['into', 'intermediate'], ['intermediate', 'bytecode'], ['bytecode', 'which'], ['which', 'is'],
```

### 7.1.1 데이터 정규화

데이터 정규화(data normalization)란 언어학적으로 또는 논리적으로 동등한 문자열, 예를 들어 전화번호 (555) 123-4567 과 555.123.4567 같은 문자여링 똑같이 표시되도록, 최소한 비교할 때 같은 것이라고 판단하게 하는 작업니다.  

앞에서 다룬 n-그램 코드를 사용하면 데이터 정규화 기능을 사용할 수 있습니다.  

물론 이 코드에는 문제가 있습니다. 중복된 2-그램이 많다는 점입니다. 2-그램을 만나면 리스트에 추가할 뿐 그 빈도를 기록하지도 않습니다. 2-그램이 존재하는지만 보기보다는 그 빈도를 기록하면 흥미로울 뿐 아니라 데이터 정리 알고리즘이나 정규화 알고리즘을 바꿨을 때 어떤 효과가 있는지 알아보는 데도 유용합니다. 데이터를 성공적으로 정규화한다면 중복 없는 n-그램의 총 숫자는 줄어들겠지만 n-그램의 총 숫자는 줄어들지 않을 것입니다.  

하지만 파이썬 딕셔너리는 정렬되지 않습니다. 딕셔너리를 정렬한다면, 각 값을 다른 타입의 컨테이너에 복사한 후 정렬하는 방법밖에 없습니다. 파이썬의 collections 라이브러리에 들어 있는 OrderDict를 사용하면 이 문제를 쉽게 해결할 수 있습니다.

```
from collections import OrderedDict
...
ngrams = ngrams(content, 2)
ngrams = dict(ngrams) # 수동으로 형변환을 했습니다. 자세한 내용은 하단에..
ngrams = OrderedDict(sorted(ngrams.items(), key=lambda t: t[1], reverse=True))
print(ngrams)
```
> 1. 위 코드를 그대로 하면 속성 에러가 일어난다. items는 list에는 없는 속성이기 때문이다. OrderedDict를 통해 ngrams를 dict 타입으로 바꾸고 정렬을 한다는 것 같은데, 저대로 해도 에러가 일어나서, 수동으로 형변환을 하니 정상적으로 동작하였다. OrderedDict는 좀 더 살펴볼 필요가 있다. 일단 수동으로 형변환을 해서 넘어갔다.  
> 2. 수동으로 형변환을 하면 작동은 하지만 원하는 결과가 나오지 않는다. 다른 사람(Young Oh Jeong,https://www.slideshare.net/epangelia/web-scraping-withpythonchap07)의 코드를 참고하여 작성 후 동작을 확인했다. 결과값이 너무 길어서 맨 앞의 값을 확인하지 못하여 텍스트 파일로 저장하여 내용을 확인하였습니다.

여기서는 파이썬의 sorted 함수를 활용해 값을 기준으로 정렬해서 새 OrderDict 객체 넣었습니다. 결과는 다음과 같습니다.

```
OrderedDict([('Software Foundation', 37), ('Python Software', 37), ('of Python', 37), ('of the', 33), ('Foundation Retrieved', 31), ('in the', 22), ('in Python', 21), ('van Rossum', 20),  
...
```

2-그램은 총 6,756개이고, Software Foundation과 Python Software가 가장 많이 등장하였습니다. 하지만 분석해보면 Python Software는 Python software로도 2번 등장합니다. 마찬가지로 van Rossum과 Van Rossum도 리스트에 각각 존재합니다.  

다음 행을 cleanInput 함수에 추가하면, 2-그램의 총 숫자는 변함없이 6,756개이지만, 중복을 제거한 숫자가 6593개로 줄어듭니다.

```Python
input = input.upper()
```

그런데 여기서 잠시 멈추고 정규화를 확장할 때 필요한 연산 과정에 대해서 생각해보는게 좋습니다. 단어의 철자가 달라도 동등하다고 생각해야 하는 경우들이 많습니다. 하지만 이런 경우의 수를 모두 체크하려면, 만나는 모든 단어에 대해 체크해야 합니다.  

예를 들어 'Python 1st'와 'Python first'가 모두 등장합니다. 그렇다고 'first, second, third 등은 모두 '1st, 2nd, 3rd 으로 통일한다'와 같은 규칙을 만들면 단어마다 10회 내외는 체크해야합니다.  

마찬가지로 일관성 없는 하이픈 사용(co-ordinated와 coordinated), 오타, 기타 자연어의 모순은 n-그램에도 영향을 미칩니다. 그런 모순이 많을수록 출력 결과도 엉망이 됩니다.  

하이픈이 들어간 경우 하이픈을 모두 제거하면 될 수도 있습니다. 하지만 all-too-common 처럼 널리 쓰이는 하이픈이 들어간 구절들이 모두 한 단어로 뭉뚱그려질 겁니다. 다른 방식으로 하이픈을 공백으로 바꾸는게 나을 수도 있지만, 경우의 수를 생각하면 그리 좋은 생각은 아닙니다.

## 7.2 사후 정리

코드에서 할 수 있는 일은 한계가 있습니다. 많은 프로그래머들은 이런 경우 '스크립트를 만들자'라는 반응을 보입니다. 물론 뛰어난 해결책일 수 있습니다. 하지만 오픈리파인(OpenRefine)같은 프로그램도 있습니다. 이 프로그램은 데이터를 빠르고 쉽게 정리해 주고, 프로그래머가 아닌 사람도 쉽게 사용할 수 있습니다.

### 7.2.1 오픈리파인
오픈리파인(http://openrefine.org)은 메타웹이라는 회사에서 시작한 오픈소스 프로젝트입니다. 2010년에 구글이 인수하여 구글 리파인으로 바꿨습니다. 구글은 2012년에 리파인 개발을 중지하고 이름을 다시 오픈리파인으로 바꿔 원하는 사람은 누구든 프로젝트 개발에 참여할 수 있습니다.

#### 오픈리파인 설치하기

오픈 리파인의 인터페이스는 브라우저 안에서 동작하지만 데스크톱 애플리케이션이므로 반드시 설치하여야 합니다. 오픈리파인 웹사이트(http://openrefine.org/download.html)에서 자신의 os용 애플리케이션을 내려받으면 됩니다.(122MB 정도 되니까 인터넷 환경을 확인하고 받으세요. 그리고 사이트 자체가... 다운로드 속도가 지못지.... ㅠㅠ)

오픈리파인을 사용하려면 데이터를 CSV 파일로 바꿔야합니다. 데이터를 데이터베이스에 저장했다면 CSV 파일로 내보낼 수 있습니다. [참조](https://kimdoky.github.io/python/2017/07/16/crawling-book-chap5.html){:target="`_`blank"}

#### 오픈리파인 사용하기

이번 예제는 위키백과의 텍스트 에디터 비교 테이블(https://en.wikipedia.org/wiki/Comparison_of_text_editors)에서 스크랩한 데이터를 사용합니다. 이 테이블은 비교적 형식을 잘 갖추고 있지만, 오랜 시간에 걸쳐 여러번 편집되었기 때문데 조금씩 형식이 틀린 곳이 있습니다. 또한 이 데이터는 컴퓨터가 아니라 사람이 보기 위해 만들어졌기 때문에 일부 형식은 프로그램의 입력에는 맞지 않습니다.

![]({{site.url}}/img/post/python/crawling/p2c7.png)

오픈리파인에서 눈여겨봐야 할 것은 각 열 레이블 다음에 있는 화살표입니다. 이 화살표는 열 필터링, 정렬, 변형, 데이터 제거가 가능한 도구 메뉴를 엽니다.

#### 필터링

데이터 필터링에는 필터와 facet 두 가지 방법이 있습니다. 필터는 정규 표현식을 써서 데이터를 거를 때 유용합니다. 예를 들어 프로그래밍 언어 열에서 프로그래밍 언어 세 개 이상이 쉼표로 구분된 데이터만 보는 화면입니다.

![]({{site.url}}/img/post/python/crawling/p2c7_2.png)

화면 왼쪽의 상자를 통해 필터를 쉽게 조작하고, 수정하고, 추가할 수 있습니다. 필터와 facet을 함께 쓸 수도 있습니다.  

facet은 열의 콘텐츠 전체를 바탕으로 데이터를 제외하거나 포함하려 할 때 유용합니다. 예를 들어 2005년 이후에 출시됐고 GPL이나 MIT 라이선스로 운영하는 에디터만 보는 화면입니다. facet에는 필터링 도구가 내장되어 있습니다. 예를 들어 숫자형 값에 필터링을 사용하면 포함할 범위를 선택할 슬라이드바가 나타납니다.

> 숫자형 값을 필터링 했을때 범위를 선택하는 facet는 찾지 못하였습니다.. 어디 있는지 모르겠네요...

데이터를 어떤 식으로 필터링했더라도 언제라도 오픈리파인이 지원하는 형식으로 내보낼 수 있습니다. CSV, HTML, HTML 테이블, 엑셀 외에도 여러 가지 형식을 지원합니다.

#### 정리

데이터를 말끔하게 필터링하려면 그 데이터가 비교적 잘 정리되어 있어야 합니다. 예를 들어 바로 앞에서 다룬 facet를 보면, 출시일이 01-01-2006인 에디터는 'First public release' facet에 포함되지 않습니다. 이 facet은 2006이라는 값을 찾으므로 그 형태에 맞지 않는 값은 무시합니다.  

오픈리파인은 GREL(Goole Refine Expression Language)이라는 이름의 표현식을 사용합니다. 이 언어는 단순한 규칙에 따라 셀 값을 변형하는 간단한 람다 함수를 만드는데 사용합니다.

```
if(value.length() != 4, "invalid", value)
```
이 함수를 First public release 열에 적용하면 날짜가 YYY 형식인 셀 값만 사용하고, 다른 셀은 모두 'invalid'로 표시합니다.

열 제목의 화살표를 클릭하고 'edit cells - transform' 을 선택하면 원하는 GREL 문을 적용할 수 있습니다.

![]({{site.url}}/img/post/python/crawling/p2c7_3.png)

그런데 이상적이지 않은 값을 모두 배제하기는 쉽지만 그렇게 하서는 큰 의미가 없습니다. 가능하면 형식이 어긋난 정보도 살리는 것이 좋습니다. GREL의 match 함수를 쓰면 좀 더 유연하게 규칙을 적용할 수 있습니다.

```
value.match(".*([0-9]{4}).*").get(0)
```
이 함수는 문자열이 정규 표현식에 일치하는지 검사합니다. 문자열이 정규 표현식에 일치하면 배열을 반환합니다. 정규 표현식의 캡쳐 그룹에 일치하는 부분은 모두 그 배열에 포함됩니다.  

따라서 이 코드는 숫자 4개가 연달아 있는 것을 모두 찾고 그중 첫 번째 것을 반환합니다. 날짜를 텍스트로 썼거나, 형식이 맞지 않더라도 해당 연도를 추출하는 데는 충분합니다. 이 코드에는 날짜가 존재하지 않을 때 null을 반환한다는 장점도 있습니다.(GREL은 null 변수를 다루더라도 null 포인터 예외를 일으키지 않습니다.)  

셀 편집과 GREL를 사용하면 데이터를 여러 가지로 변형할 수 있습니다.
