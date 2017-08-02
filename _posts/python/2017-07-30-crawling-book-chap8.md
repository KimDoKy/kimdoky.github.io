---
layout: post
section-type: post
title: crawling - P2. 고급 스크레이핑 _ cahp 8. 자연어 읽고 쓰기
category: python
tags: [ 'python' ]
---

구글 이미지 검색에 '귀여운 고양이(cute kitten)'라고 입력했을 때, 구글은 무엇을 검색했는지 어떻게 알 수 있을까요? 귀여운 고양이 이미지 주변에 있는 텍스트를 이용합니다. 유투브의 검색 창에 '죽은 앵무새(dead parrot)'이라고 입력했을 때 몬티 파이튼의 스케치를 찾아야 한다고 판단하는 건 어떻게 했을까요? 각 비디오를 올릴 때 함께 올리는 제목과 설명 텍스트 덕분입니다.  

사실 '죽은 새 몬티 파이튼(deceased bird monty python)'이라고 타이핑해도 똑같이 '죽은 앵무새' 스케치가 나옵니다. 그 페이지 자체는 deceased과 bird 같은 단어가 없어도 말입니다. 구글은 '핫 도그(hot dog)'가 음식을 가리키며 '강아지를 삶다(boiling puppy)'와는 완전히 다른 의미임을 알고 있습니다. 어떻게 가능할까요? 모두 **통계** 덕분입니다.  

텍스트 분석은 배경에 있는 개념을 이해하면 머신 러닝 전반에 걸쳐 대단히 큰 도움이 되며, 현실 세계의 문제를 개연성과 알고리즘의 관점에서 모델링을 하는 더 범용적인 능력을 갖게 됩니다.  

예를 들어 샤짐(shazam) 음악 서비스는 소리를 듣고 어떤 음악인지 알아내는데, 설령 그 소리에 주위의 잡음이 끼어 있거나 소리가 왜곡되어 있더라도 알아냅니다. 구글은 다른 단서는 아무것도 없이 이미지 자체만 가지고 자동으로 이미지 캡션을 만듭니다.

## 8.1 데이터 요약

챕터 7에서 텍스트 콘텐츠를 n-그램, 즉 단어 n개로 구성된 구절로 나누는 것에 대해 다루었습니다. 매우 기본적인 수준에서 말한다면, 이 방법은 어떤 단어와 구절이 텍스트에서 가장 많이 쓰이는지 판단하는 데 쓸 수 있습니다. 한 걸음 더 나가면, 원래 텍스트에서 가장 많이 쓰인 구절이 들어 있는 문장을 추출해 마치 사람이 말하는 듯 요약하는 데도 쓸 수 있습니다.  

이번에 사용할 샘플 텍스트는 미국 제9대 대통령 윌리엄 헨리 해리슨(William Henry Harrison)의 취임 연설(http://pythonscraping.com/files/inaugurationSpeech.txt)입니다. 해리슨은 두 가지 기록을 세웠습니다. 하나는 역대 대통령 중 가장 긴 취임 연설이라는 점이고, 다른 하나는 재임 기간이 가장 짧았다는(32일) 기록입니다.  

챕터 7에서 n-그램을 찾을 때 썼던 코드를 조금 수정하고, operator 모듈에 들어 있는 파이썬의 정렬 함수를 사용하면 n-그램을 찾고 정렬하는 코드를 만들 수 있습니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
import operator
import os

def cleanInput(input):
    input = re.sub('\n+', " ", input).lower()
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
    output = {}
    for i in range(len(input)-n+1):
        ngramTemp = " ".join(input[i:i+n])
        if ngramTemp not in output:
            output[ngramTemp] = 0
        output[ngramTemp] += 1
    return output

content = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')
ngrams = ngrams(content, 2)
sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True)
print(sortedNGrams)
```

출력 결과의 일부분입니다.

```
[('of the', 213), ('in the', 65), ('to the', 61), ('by the', 41), ('the constitution', 34), ('of our', 29), ('to be', 26), ('the people', 24), ('from the', 24), ('that the', 23), ('it is', 23), ('and the', 23), ('of a', 22), ('the executive', 19), ('of their', 19),
```

이들 2-그램 중에서 the constitution은 연설문에 상당히 많이 등장하는 구절이 맞지만, of the, in the, to the 등은 눈여겨 볼 필요가 없습니다. 이러한 필요없는 단어를 자동으로 걸러내는 방법이 있을까요??  

브리검영 대학교의 언어학 교수인 마크 데이비스(Mark Davies)는 최근 십여 년간 미국에서 인기 있었던 출판물에서 뽑은 4억 5천만 개 이상의 단어로 구성된 현대 미국영어자료(http://corpus.byu.edu/coca/)를 관리하고 있습니다.  

이 중에서 가장 많이 사용된 단어 5천 개의 리스트가 무료로 제공되었고, 그 분량은 가장 널리 쓰이는 2-그램을 걸러내는 기본 필터로 사용하기에 충분한 양입니다. 다음의 isCommon 함수와 함께 사용하면 처음 100단어만으로도 결과는 많이 개선됩니다.

```
def isCommon(ngram):
    commonWorks = ["the", "be", "and", "of", "a", "in", "to", "have", "it", "i", "that", "for", "you", "he", "with", "on", "do", "say", "this", "they", "is", "an", "at", "but", "we", "his", "from", "that", "not", "by", "she", "or", "as", "what", "go", "their", "can", "who", "get", "if", "would", "her", "all", "my", "make", "about", "know", "will", "as", "up", "one", "time", "has", "been", "there", "year", "so", "think", "when", "which", "them", "some", "me", "people", "take", "out", "into", "just", "see", "him", "your", "come", "could", "now", "than", "like", "other", "how", "then", "its", "our", "two", "more", "these", "want", "way", "look", "first", "also", "new", "because", "day", "more", "use", "no", "man", "find", "here", "thing", "give", "many", "well"]
    for word in ngram:
        print(word)
        if word in commonWorks:
            return True
    return False
```
> 위 함수를 적용하면서 원하는 결과가 나오지 않아서 마음대로 코드를 수정하여 결과를 얻었습니다. commonWorks안의 단어가 전부 결과에서 제외되어야 하기 때문에 각 단어를 각각 비교하였고, 단어가 들어가면 for문은 단어의 철자를 각각 비교하기 때문에 조건이 제대로 적용되지 않습니다. 그래서 for문을 삭제하고 단어 하나하나를 넣어서 함수를 적용시켰습니다.

```python
def isCommon(ngram):
    commonWorks = ["the", "be", "and", "of", "a", "in", "to", "have", "it", "i", "that", "for", "you", "he", "with", "on", "do", "say", "this", "they", "is", "an", "at", "but", "we", "his", "from", "that", "not", "by", "she", "or", "as", "what", "go", "their", "can", "who", "get", "if", "would", "her", "all", "my", "make", "about", "know", "will", "as", "up", "one", "time", "has", "been", "there", "year", "so", "think", "when", "which", "them", "some", "me", "people", "take", "out", "into", "just", "see", "him", "your", "come", "could", "now", "than", "like", "other", "how", "then", "its", "our", "two", "more", "these", "want", "way", "look", "first", "also", "new", "because", "day", "more", "use", "no", "man", "find", "here", "thing", "give", "many", "well"]
    if ngram in commonWorks:
        return True
    return False

...

def ngrams(input, n):
    input = cleanInput(input)
    output = {}
    for i in range(len(input)-n+1):
        if isCommon(input[i]) or isCommon(input[i+1]):
            pass
        else:
            ngramTemp = " ".join(input[i:i+n])
            if ngramTemp not in output:
                output[ngramTemp] = 0
            output[ngramTemp] += 1
    return output

...
```

위 코드를 적용하여 연설문 본문에서 3회 이상 발견한 2-그램은 다음과 같습니다.

```
('united states', 10), ('executive department', 4), ('general government', 4), ('chief magistrate', 3), ('government should', 3), ('legislative body', 3), ('mr jefferson', 3), ('called upon', 3), ('whole country', 3), ('same causes', 3)
```

리스트의 처음 두 항목인 united states와 executive department는 대통령의 취임 연설에 등장할 만한 단어입니다.  

널리 쓰이는 단어는 비교적 최근을 기준으로 선정했기 때문에, 이 연설문이 1841년에 작성되었다는걸 감안하면 필터링 결과는 다소 부적절할 수 있습니다. 하지만 100단어 정도만 사용했음에도 만족할 만한 결과과 나왔습니다.

이제 텍스트에서 핵심 주제는 추출했고, 텍스트 요약은 어떻게 만들어야 할까요? 한가지 방법은 자주 쓰인 n-그램 각각에 대해 그 구절이 쓰인 첫 번째 문장을 검색하는 것입니다. 첫 문장인 만큼 본문 전체에 대한 만족할 만한 개관이 될 거라고 짐작할 수 있습니다.

## 8.2 마르코프 모델

마르코프(Markov) 텍스트 생성기는 트위토프 앱(http://twitov.extrafuture.com)처럼 개그 목적으로 널리 쓰이기도 하고, 스팸 탐지 시스템을 통과하는 스팸 메일을 만드는데도 쓰입니다.  

이들  텍스트 생성기는 마르코프 모델을 기초로 만들어졌습니다. 마르코프 모델은 어떤 특정 사건이 다른 특정 사건에 뒤이어, 일정 확률로 일어나는 대규모 무작위 분포를 분석할 때 자주 쓰입니다.

예를 들어 아래 그림처럼 기상 시스템의 마르코프 모델을 만들 수 있습니다.

![]({{site.url}}/img/post/python/crawling/p2c8_1.png)

이 모델에서 'Sunny'의 다음날은 70%로 화창한 날이고, 20%는 'Cloudy'이며, 'Rainy'일 확률은 불과 10%입니다. 'Rainy'의 다음 날은 50% 확률로 'Rainy'이고, 'Cloudy'와 'Sunny'는 각각 25%입니다.

- 각 노드에서 출발하는 확률의 합은 반드시 정확히 100%이어야 합니다. 시스템이 아무리 복잡하더라도 반드시 100% 확률로 다음 단계를 넘어가야 합니다.
- 현재 이 시스템에는 세 가지 경우의 수만 있지만, 이 모델을 가지고 만들 수 있는 일기예보는 무한히 길어질 수 있습니다.
- 다음 단계에 영향을 미치는 것은 오직 현재 노드의 상태뿐입니다. 현재 'Sunny'에 있다면, 이전 100일이 무슨 날씨였든 상관없이 다음날이 화창한 확률은 항상 70%입니다.
- 특정 노드는 다른 노드에 비해 도달하기 어렵습니다. 배경이 되는 수학 이론은 상당히 복잡하지만 주어진 시점이 언제든 상관없이 'Rainy'로 이동할 확률이 가장 낮다는 건 쉽게 알 수 있습니다.

물론 이건 매우 단순한 시스템이고, 마르코프 모델은 얼마든지 크게 만들 수 있습니다. 사실 수슬의 페이지 평가 알고리즘도 웹사이트를 노드로 나타내고 들어오고/나가는 링크를 노드 사이의 연결로 나타내는 마르코프 모델을 일부 채용하고 있습니다. 특정 노드에 도달할 확률은 그 사이트의 상대적 인기를 나타냅니다. 즉 이 날씨 시스템이 작은 인터넷이라면 'Rainy'는 등급이 낮은 페이지이고, 'Sunny'는 등급이 높은 페이지가 됩니다.  

지금까지 설명한 것들을 염두에 두고, 텍스트를 분석하고 작성하는 예제를 만듭니다.  

이번에도 해리슨 대통령의 취임 연설을 사용합니다. 연설문 구조에 따라 얼마든지 긴 마르코프 체인을 만들 수 있습니다.

```python
from urllib.request import urlopen
from random import randint

def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum

def retrieveRAndomWord(wordList):
    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word

def buildWordDict(text):
    # 줄바꿈 문자와 따옴표를 제거합니다.
    text = text.replace("\n", " ")
    text = text.replace("\"", "")

    # 구두점 역시 단어로 취급해서 마르코프 체인에 들어가게 됩니다.
    punctuation = [',', '.', ';', ':']
    for symbol in punctuation:
        text = text.replace(symbol, " " + symbol + " ")

    words = text.split(" ")
    # 빈 단어를 제거합니다.

    words = [word for word in words if word != ""]

    wordDict = {}
    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
            # 이 단어에 필요한 새 딕셔너리를 만듭니다.
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]] = wordDict[words[i-1]][words[i]] + 1
    return wordDict

text = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')
wordDict = buildWordDict(text)

# 길이가 100인 마르코프 체인을 생성합니다.
length = 100
chain = ""
currentWord = "I"
for i in range(0, length):
    chain += currentWord + " "
    currentWord = retrieveRAndomWord(wordDict[currentWord])

print(chain)
```

출력 결과는 실행할 때마다 다르지만, 다음 결과는 도무지 말이 되지 않는 결과의 예입니다.

```
I sincerely believe in Chief Magistrate to make all necessary sacrifices and oppression of the remedies which we may have occurred to me in the arrangement and disbursement of the democratic every other addition of legislation, by the interests which violate that the Government would compare our aboriginal neighbors the people to its accomplishment. The latter also susceptible of the Constitution not much mischief, disputes have left to betray. The maxim which may sometimes be an impartial and to prevent the adoption or
```

이 코드는 어떻게 동작할까요?

buildWordDict 함수는 인터넷에서 가져온 텍스트 문자열을 받아서 따옴표를 제거하고, 따옴표를 제외한 다른 구두점 주위에 공백을 넣어 단어로 취급합니다. 그리고 2차원 딕셔너리, 즉 다음 형태를 가진 딕셔너리의 딕셔너리를 만듭니다.

```
{word_a : {word_b : 2, word_c : 1, word_d : 1},
 word_e : {word_b : 5, word_c : 2}, ... }
```

이 에제 딕셔너리에서  word_a는 4번 발견됐는제, 그중 둘은 word_b로 이어지고, 다른 둘은 각각 word_c와 word_d로 이어집니다. word_e는 7번 발견됐는데, 그중 다섯은 word_b로 이어지고 나머지 둘은 word_d로 이어집니다.  

이 결과를 노드 모델로 나타낸다면 word_a를 나타내는 노드에서 나오는 화살표 중 50%는 word_b로, 25%는 word_c로, 다른 25%는 word_d로 향할 겁니다.  

일단 이 딕셔너리를 만들고 나면 현재 단어가 무엇이든 간에 다음 단어로 찾아갈 수 있는 검색 테이블 구실을 할 수 있습니다.
> 예외는 텍스트의 마지막 단어입니다. 마지막 단어 뒤에는 아무것도 없기 때문입니다. 예제 텍스트의 마지막 단어는 마침표(.)인데, 마침표는 215번이나 나타나므로 막다른 길이 될 리 없으므로 편리합니다. 다만 마르코프 생성기를 직접 만든다면 텍스트의 마지막 단어는 믿을 수 있는 것이여야만 할 수도 있습니다.

샘플로 만든 2차원 딕셔너리에서 현재 word_e에 있다면, 딕셔너리 {word_b : 5, word_d: 2}를 retrieveRAndomWord 함수에 넘기게 됩니다. retrieveRAndomWord 함수는 딕셔너리를 받고, 그 딕셔너리에 있는 단어들의 빈도를 참고해서 무작위 단어를 반환합니다.  

무작위 단어를 시작해서 마르코프 체인을 이리저리 움직이며 원하는 만큼 단어를 생성할 수 있습니다.

### 8.2.1 위키백과의 여섯 다리: 결론

챕터 3에서 케빈 베이컨에 관한 위키백과 항목에서 시작해 다른 항목으로 넘어가는 링크를 수집해 데이터베이스에 저장하는 스크레이퍼를 만들었습니다. 어떤 페이지에서 시작해 목표 페이지에 도달하는 링크 체인을 찾는 문제는 첫 번째 단어와 마지막 단어가 정해진 상태에서 마르코프 체인을 찾는 것과 마찬가지입니다. 이런 종류의 문제를 **방향성 그래프(directed graph)** 문제라고 부릅니다.이런 문제이서 A -> B는 B -> A와 같지 않습니다. football이라는 단어 뒤에는 player라는 단어가 따라올 때가 많지만, player 뒤에 football이 따라오는 경우는 매우 드문것과 같습니다. 케빈 베이컨의 위키백과 항목에는 그의 고향인 필라델피아를 가리키는 링크가 있지만, 필라델피아 항목에는 케빈 베이컨을 가리키는 링크가 없습니다.  

이와는 대조적으로 원래 케빈 베이컨의 여섯 다리 게임은 **비방향성 그래프(undirected graph)** 문제입니다. 케빈 베이컨이 줄리아 로버츠와 함께 <유혹의 선>에 출연했다면, 줄리아 로버츠는 반드시 케빈 베이컨과 함께 <유혹의 선>에 출연한 겁니다. 따라서 관계를 양쪽을 모두 향합니다. 컴퓨터 과학에서 비방향성 그래프 문제는 방향성 그래프 문제보다 적기는 하지만, 둘 다 컴퓨터로 풀리에는 어려운 문제입니다.  

이러한 문제를 풀기 위해 많은 연구가 행해졌고 다양한 변형도 시도됐지만, 방향성 그래프에서 가장 짧은 경로를 찾을 때 가장 좋고 가장 널리 쓰이는 방법은 **너비 우선 탐색(breadth0first search)** 입니다.  

너비 우선 탐색에서는 우선 시작 페이지에서 출발하는 링크를 모두 검색합니다. 검색한 링크에 목표 페이지가 들어 있지 않으면 2단계 링크, 즉 시작 페이지에서 링크된 페이지에서 다시 링크된 페이지를 찾습니다. 링크 단계 제한에 걸리거나, 목표 페이지를 찾을 때까지 이 과정을 반복합니다.  

챕터 5에서 설명한 링크 테이블을 사용해 너비 우선 탐색을 푸는 코드입니다.

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='127.0.0.1', user='root', passwd=None, db='mysql', charset='utf-8')

cur = conn.cursor()
cur.execute("Use wikipedia")

class SolutionFound(RuntimeError):
    def __init__(self, message):
        self.message = message

def getLinks(fromPageId):
    cur.execute("SELECT toPageId FROM links WHERE fromPageId = %s", (fromPageId))
    if cur.rowcount == 0:
        return None
    else:
        return [x[0] for x in cur.fetchall()]

def constructDict(currentPageId):
    links = getLinks(currentPageId)
    if links:
        return dict(zip(links, [{}]*len(links)))
    return {}

# 링크 트리가 비어 있거나 링크가 여러 개 들어 있습니다.
def searchDepth(targetPageId, currentPageId, linkTree, depth):
    if depth == 0:
        # 재귀를 중지하고 함수를 끝냅니다.
        return linkTree
    if not linkTree:
        linkTree = constructDict(currentPageId)
        if not linkTree:
            # 링크가 발견되지 않았으므로 이 노드에서는 계속 할 수 없습니다.
            return {}
    if targetPageId in linkTree.keys():
        print("TARGET " + str(targetPageId) + " FOUND!")
        raise SolutionFound("PAGE: " + str(currentPageId))

    for branchKey, branchValue in linkTree.items():
        try:
            # 재귀적으로 돌아와서 링크 트리를 구축합니다.
            linkTree[branchKey] = searchDepth(targetPageId, branchKey, branchValue, depth-1)
        except SolutionFound as e:
            print(e.message)
            raise SolutionFound("PAGE: " + str(currentPageId))
    return linkTree

try:
    searchDepth(134951, 1, {}, 4)
    print("No solution found")
except:
    print(e.message)
```
> DB 연결 부분을 더 점검해야 합니다. 현재 연결에서 에러가 일어납니다.
```
File "/usr/local/var/pyenv/versions/scrapingEnv/lib/python3.5/site-packages/pymysql/__init__.py", line 90, in Connect
    return Connection(*args, **kwargs)
  File "/usr/local/var/pyenv/versions/scrapingEnv/lib/python3.5/site-packages/pymysql/connections.py", line 678, in __init__
    self.encoding = charset_by_name(self.charset).encoding
AttributeError: 'NoneType' object has no attribute 'encoding'
```
패스워드를 입력해도 인코딩 에러가 일어납니다. 현재 이슈를 해결중입니다.

>
```
AttributeError: 'NoneType' object has no attribute 'encoding'
```
위 에러는 파이썬 버젼에 따른 차이로 에러가 일어나는 것으로 추측됩니다. 인코딩방식(charset='utf-8') 부분을 삭제해주면 DB 연결은 성공합니다.


getLinks와 constructDict는 주어진 페이지에 따라 데이터베이스에서 링크를 가져오고, 가져온 링크를 딕셔너리 형식으로 바꾸는 보조 함수입니다. 메인 ㅎ마수인 searchDepth는 재귀적으로 동작하면서 한 번에 한 단계씩 링크 트리를 구축하는 동시에 검색합니다. 이 함수는 다음 규칙을 따릅니다.

- 주어진 재귀 제한에 도달하면(즉, 자기 자신을 너무 자주 호출했다면) 아무 일도 하지 않고 끝납니다.
- 주어진 링크 딕셔너리가 비어 있다면 현재 페이지의 링크로 트리를 만듭니다. 현재 페이지에 링크가 없다면 돌아갑니다.
- 현재 페이지에 목표 페이지를 가리키는 링크가 있다면 해결책을 찾았음을 알리는 예외를 일으킵니다. 그러면 각 스택에서 현재 페이지를 출력하면서 다시 예외를 일으키므로 결과적으로 해결책인 페이지 목록이 화면에 출력됩니다.
- 해결책을 찾지 못하면 링크 단계 제한을 한 단계 줄이면서 자신을 다시 호출하여 다음 단계 링크를 검색합니다.

케빈 베이컨의 페이지(id 1)와 에릭 아이들의 페이지(id 134951) 사이의 링크를 검색한 결과는 다음과 같습니다.

```
Target 134951 FOUND!
PAGE: 156224
PAGE: 155545
PAGE: 3
PAGE: 1
```

이 결과를 순서대로 보면 케빈 베이컨 -> 샌디에이고 코믹콘 -> 브라이언 프라우드 -> 테리 존스 -> 에릭 아이들 입니다.

여섯 다리 문제와 문장에서 어떤 단어가 다른 어떤 단어 뒤에 자주 나타나는지를 모델링하는 것 외에도, 다양성 그래프와 비방향성 그래프는 웹 스크레이핑을 하다가 마주칠 다양한 상황을 모델링할 때 쓸 수 있습니다. 예를 들어 어떤 웹사이트가 다른 어떤 웹사이트를 링크하고 있는지, 어떤 보고서가 다른 어떤 보고서를 인용하고 있는지, 판매 사이트에 종종 함께 노출되는 상품은 어떤 것인지, 이 링크는 얼마나 강력한지, 링크는 양방향인지 등의 다양한 상황들에서 말입니다.  

이들 관계릐 기본적인 타입을 알게 되면 스크랩한 데이터에 따라 모델을 만들거나, 시각화하거나, 뭔가 예측하려 할 때 큰 도움이 됩니다.

## 8.3 자연어 툴킷

지금까지는 주로 텍스트 본문에 있는 단어를 통계적으로 분석하는데 집중했습니다. 가장 많이 쓰인 단어, 비정상적인 단어, 어떤 단어 뒤에 어떤 단어가 주로 따로오는지, 그들을 어떻게 묶을수 있는지 말입니다. 아직 하지 못한 것은 그 단어들이 어떤 의미인지 가능한한 이해하는 겁니다.  

자연어 툴킷(NLTK. Natural Language Toolkit)은 영어 텍스트의 부분마다 식별하고 태깅하도록 설계된 파이썬 라이브러리 모음입니다. 2000년에 시작된 프로젝트로 15년간 수십명의 개발자가 참여했습니다.  

### 8.3.1 설치

```
pip install NLTK
```

모듈을 설치한 다음에는 미리 작성된 텍스트 저장소를 내려받아 몇 가지 기능을 쉽게 테스트해 볼 수 있습니다.

```
>>> import nltk
>>> nltk.download()
```
이 명려은 NLTK 다운로더를 실행합니다.

![]({{site.url}}/img/post/python/crawling/c8_3_1.png)

패키지를 다운로드 해야 뒷 내용을 따라 갈 수 있습니다.

### 8.3.2 NLTK 를 사용한 통계적 분석

NLTK는 텍스트에서 단어 숫자, 단어 빈도, 어휘 다양도 같은 통계적 정보를 생성할 때 아주 유용합니다. 필요한 것이 비교적 단순한 계산, 예를 들어 텍스트 섹션에서 고유한 단어 숫자를 세어보는 것이라면 NLTK는 좀 과할 수 있습니다. 이 모듈은 매우 크니까요. 하지만 비교적 광범위한 텍스트 분석이 필요하다면 이 모듈에서 제공하는 많은 함수를 통해 원하는 거의 모든 것을 얻을 수 있습니다.  

NLTK 분석은 항상 Text 객체로 시작합니다. 다음과 같은 방법으로 단순한 파이썬 문자열을 Text 객체로 바꿀 수 있습니다.

```python
from nltk import word_tokenize
from nltk import Text

tokens = word_tokenize("Here is some not very interesting text")
text = Text(tokens)
```

word_tokeniz 함수는 파이썬에서 문자열로 인식하는 텍스트는 무엇이든 받을 수 있습니다. 지금 당장은 테스트해볼 긴 문자열이 없지만 기능을 써보고 싶다면 NLTK에 내장된 몇 권의 책을 다음과 같이 임포트해서 사용할 수 있습니다.

```
from nltk.book import *
```

위 명령은 아홉 권의 책을 불러옵니다.

```python
>>> from nltk.book import *
*** Introductory Examples for the NLTK Book ***
Loading text1, ..., text9 and sent1, ..., sent9
Type the name of the text or sentence to view it.
Type: 'texts()' or 'sents()' to list the materials.
text1: Moby Dick by Herman Melville 1851
text2: Sense and Sensibility by Jane Austen 1811
text3: The Book of Genesis
text4: Inaugural Address Corpus
text5: Chat Corpus
text6: Monty Python and the Holy Grail
text7: Wall Street Journal
text8: Personals Corpus
text9: The Man Who Was Thursday by G . K . Chesterton 1908
```

이 장의 나머지 예제에서는 text6인 <몬티 파이튼과 성배>를 사용하겠습니다.  

Text 객체는 일반적인 파이썬 배열과 거의 비슷하게 조작할 수 있습니다. 텍스트 단어들로 구성된 배열이라고 생각하면 됩니다. 이런 특징을 이용해서 텍스트에 들어 있는 고유한 단어 숫자와 총 단어 숫자를 비교할 수 있습니다.

```
>>> len(text6)/len(text)
2423.8571428571427
```
위 코드는 대본의 각 단어가 평균 2423번 정도 사용됐음을 보여줍니다.
> 어떻게 해서 이렇게 결과가 나왔는지 아직 잘 이해가 안갑니다...

텍스트를 빈도분포(frequency distribution.통계학에서는 도수분포라고 부릅니다.) 객체에 넘기면 가장 많이 쓰인 단어는 무엇인지, 다양한 단어들의 빈도가 어느 정도인지 알 수 있습니다.

```python
>>> from nltk import FreqDist
>>> fdist = FreqDist(text6)
>>> fdist.most_common(10)
[(':', 1197), ('.', 816), ('!', 801), (',', 731), ("'", 421), ('[', 319), (']', 312), ('the', 299), ('I', 255), ('ARTHUR', 225)]
>>> fdist["Grail"]
34
```

이 텍스트는 영화 대본이므로 구조를 짐작할 수 있는 단어도 몇 가지 보입니다. 예를 들어 전부 대문자로 된 ARTHUR가 자주 등장하는데, 대본에서는 아서 왕의 대사가 있을 때마다 그 앞에 등장하기 때문입니다. 또한 모든 행에 등장하는 콜론(:)은 등장인물의 이름과 대사를 구분하는 역할을 합니다. 이걸 보면 이 영화에 대사가 1,197개가 있음을 알 수 있습니다.  

이전에 살펴본 2-그램을 바이그램(bigram)이라고도 부릅니다. 마찬가지로 3-그램을 트라이그램(trigram)이라고 합니다. 이들을 만들고, 검색하고, 목록을 만드는 것도 쉽습니다.

```python
>>> from nltk import bigrams
>>> bigrams = bigrams(text6)
>>> bigramsDist = FreqDist(bigrams)
>>> bigramsDist[("Sir", "Robin")]
18
```

2-그램 Sir Robin을 검색하면 2-그램이 빈도분포에서 표현되는 방법과 일치하도록 Sir와 Robin의 배열로 만들면 됩니다. 3-그램에 해당하는 trigrams 모듈도 똑같이 동작합니다.
일반적으로는 ngrams 모듈을 임포트하기만 하면 됩니다.

```python
>>> from nltk import ngrams
>>> fourgrams = ngrams(text6, 4)
>>> fourgramsDist = FreqDist(fourgrams)
>>> fourgramsDist[("father", "smelt", "of", "elderberries")]
1
```
여기서 ngrams 함수는 텍스트 객체를 분리해 두 번째 매개변수로 지정한 n-그램으로 나눕니다. 이 코드에서는 텍스트를 4-그램으로 나누게 했습니다. 그리고 father smelt of elderberries라는 구절이 정확히 한 번만 나온 것을 확인했습니다.
> 구절의 단어 순서도 정확히 일치해야 합니다.

빈도분포와 텍스트 객체, n-그램은 모두 루프에서 사용할 수 있습니다. 예를 들어 다음 코드는 coconut으로 시작하는 4-그램을 모두 출력합니다.

```
from nltk.book import *
from nltk import ngrams
fourgrams = ngrams(text6, 4)
for fourgram in fourgrams:
    if fourgram[0] == "coconut":
        print(fourgram)
```

결과입니다.

```
*** Introductory Examples for the NLTK Book ***
Loading text1, ..., text9 and sent1, ..., sent9
Type the name of the text or sentence to view it.
Type: 'texts()' or 'sents()' to list the materials.
text1: Moby Dick by Herman Melville 1851
text2: Sense and Sensibility by Jane Austen 1811
text3: The Book of Genesis
text4: Inaugural Address Corpus
text5: Chat Corpus
text6: Monty Python and the Holy Grail
text7: Wall Street Journal
text8: Personals Corpus
text9: The Man Who Was Thursday by G . K . Chesterton 1908
('coconut', 'and', 'you', "'")
('coconut', "'", 's', 'tropical')
('coconut', '?', 'ARTHUR', ':')
('coconut', '.', 'ARTHUR', ':')
('coconut', 'back', 'anyway', '...')
('coconut', 'on', 'a', 'line')
```

NLTK 라이브러리에는 큰 텍스트를 정리하고, 수를 세고, 정렬하고, 측정하도록 설계된 방대한 여러 도구와 객체가 있습니다. 이 도구들은 대부분 아주 잘 설계되어 있으며, 파이썬에 익숙한 사람은 직관적으로 사용할 수 있습니다.

### 8.3.3 NLTK 를 사용한 사전적 분석

지금까지 모든 단어를 곧이곧대로 비교하고 분류했습니다. 철자가 같지만 다른 단어를 구별하지도 않았고, 문맥에 따라 뜻이 다른 것도 생각하지 않았습니다.  

"He was objective in achieving his objective of writing an objective philosophy, primarily using verbs in the objective case." 사람은 이런 문장을 쉽게 이해하지만, 웹 스크레이퍼는 이 문장을 보고 같은 단어가 4번 사용됐다고 생각할 뿐 각 단어의 의미는 이해하지 못합니다. (objective는 순서대로 객관적인, 목표, 실재적, 목적격 이라는 네 가지 다른 의미로 쓰였습니다.)

연설문의 각 부분을 이해하는 것에 더해 어떤 단어가 여라 가지 의미로 사용되는 것을 구별할 수 있다면 유용할 겁니다. 예를 들어 일상적으로 쓰이는 영단어로 구성된 회사 이름을 찾아볼 수도 있고, 어떤 회사에 대한 의견인 "ACME Products is good"과 "ACME Products is not bad"가 같은 의견이라는 것도 알 수 있습니다. 한 문장에는 good이 있고 다른 문장에는 bad가 있는데도 말이죠.

---
> ### 펜 트리뱅크의 태그
NLTK는 텍스트에 태그를 붙일 때 널리 쓰이는, 펜실베니아 대학의 펜 트리뱅크(Penn Treebank) 프로젝트(https://goo.gl/1ZoxjD)를 기본적으로 사용하고 있습니다. 태그 중에는 등위 접속사를 나타내는 CC처럼 쉽게 이해되는 것도 있지만, 불변화사를 나타내는 RP처럼 혼란스러운 것도 있습니다 이 섹션에서 사용되는 태그가 궁금할 때는 다음 표를 참고하세요.
>
태그 | 원어 | 한국어
---|---|---
CC | coordinating conjunction | 등위 접속사(and, or, but 같은 접속사)
CD | cardinal number | 기수(순서의 의미가 없이 수량만 나타내는 수)
DT | determiner | 한정사(명사 앞에 붙는 the, some, my 같은 말들)
EX | existential "there" | 장소가 아니라 존재를 나타내는 there <br> (**There** is always some madness in love.)
FW | foreign word | 외래어
IN | preposition,<br> subordinating conjunction | 전치사, 종속 접속사
JJ | adjective | 형용사
JJR | adjective, comparative | 비교급 형용사 (My house is **larger** than hers.)
JJS | adjective, superlative | 최상급 형용사 (My house us the **largest** one in our neighborhood.)
LS | list item marker | 목록임을 나타내는 문자
MD | modal | 법조동사(can, must, may 등)
NN | noun, singular or mass | 명사. 단수 또는 복수
NNS | noun, plural | 복수형 명사
NNP | proper noun, singular | 단수형 고유명사
NNPS | proper noun, plural | 복수형 고유명사
PDT | predeterminer | 선행 한정사 (all, both, half 등)
POS | possessive ending | 소유격 문자 (어포스트로피 및 's)
PRP | personal pronoun | 인칭대명사 (I, you, he, she)
PRP$ | possessive pronoun | 소유격 대명사 (The dog is **mine**.)
RB | adverb | 부사
RBR | adverb, comparative | 비교급 부사 (Jim works **harder** than his brother.)
RBS | adverb, superlative | 최상급 부사 (Everyone in the race ran fest, but John ran the **festest** of all.)
RP | Particle | 불변화사 (동사와 함께 쓰이는 부사나 전치사, She tore **up** the letter.)
SYM | symbol | 기호
TO |"to" | to
UH | ilnterjection | 감탄사
VB | verb, base form | 동사 원형
VBD | verb, past tense | 과거형 동사
VBG | verb, gerund or present participle | 동명사 또는 현재진행형(~ing)
VBN | verb, past participle | 과거분사 (I have **seen** six deer.)
VBP | verb, non-third person<br>singular present | 3인칭이 아닌 현재형 동사
VBZ | verb, third person singular present | 3인칭 현재형 동사(s로 끝남)
WDT | wh-determiner | wh로 시작하는 한정사(문장 맨 앞에 등장하지 않는 what, which)
WP | wh-pronoun | wh로 시작하는 대명사 (what, which, who, whoever)
WP$ | possessive wh-pronoun | wh로 시작하는 소유격 대명사 (whom, whose)
WRB | wh-adverb | wh로 시작하는 부사 (when, where, why, how)

NLTK는 문장을 분석하는 것 외에도 단어의 문맥과 내장된 방대한 사전으로 그 의미를 찾는 것을 도울 수 있습니다. 기본적인 수준에서 NLTK는 문장의 각 부분을 분석할 수 있습니다.

```Python
>>> from nltk.book import *
*** Introductory Examples for the NLTK Book ***
Loading text1, ..., text9 and sent1, ..., sent9
Type the name of the text or sentence to view it.
Type: 'texts()' or 'sents()' to list the materials.
text1: Moby Dick by Herman Melville 1851
text2: Sense and Sensibility by Jane Austen 1811
text3: The Book of Genesis
text4: Inaugural Address Corpus
text5: Chat Corpus
text6: Monty Python and the Holy Grail
text7: Wall Street Journal
text8: Personals Corpus
text9: The Man Who Was Thursday by G . K . Chesterton 1908
>>> from nltk import word_tokenize
>>> from nltk import pos_tag

>>> text = word_tokenize("Strange women lying in ponds distributing swords is no basis for a system of government. Supreme executive power derives from a mandate from the masses, not from some farcical aquatic ceremony.")
>>> words = pos_tag(text)
>>> print(words)

[('Strange', 'JJ'), ('women', 'NNS'), ('lying', 'VBG'), ('in', 'IN'), ('ponds', 'NNS'), ('distributing', 'VBG'), ('swords', 'NNS'), ('is', 'VBZ'), ('no', 'DT'), ('basis', 'NN'), ('for', 'IN'), ('a', 'DT'), ('system', 'NN'), ('of', 'IN'), ('government', 'NN'), ('.', '.'), ('Supreme', 'NNP'), ('executive', 'NN'), ('power', 'NN'), ('derives', 'VBZ'), ('from', 'IN'), ('a', 'DT'), ('mandate', 'NN'), ('from', 'IN'), ('the', 'DT'), ('masses', 'NNS'), (',', ','), ('not', 'RB'), ('from', 'IN'), ('some', 'DT'), ('farcical', 'JJ'), ('aquatic', 'JJ'), ('ceremony', 'NN'), ('.', '.')]
```

각 단어는 **튜플** 로 나뉩니다. 튜플에는 단어와 함께 그 단어가 연설문에서 어떤 의미로 쓰였는지 나타내는 태그가 들어 있습니다. 언뜻 보기엔 매우 단순해 보일지 모르지만, 다음 예를 보면 이 작업은 매우 복잡한 알고리즘을 거치고 있음을 알 수 있습니다.

```python
>>> text = word_tokenize("The dust was thick so he had to dust")
>>> words = pos_tag(text)
>>> print(words)
[('The', 'DT'), ('dust', 'NN'), ('was', 'VBD'), ('thick', 'RB'), ('so', 'RB'), ('he', 'PRP'), ('had', 'VBD'), ('to', 'TO'), ('dust', 'VB')]
```
이 문잔에는 dust라는 단어가 한 번은 명사로, 다른 한 번은 동사로 쓰였습니다. NLTK는 두 단어의 쓰임을 문맥에 따라 정확히 판단했습니다. NLTK는 영어의 **문맥 자유 문법(context-free grammar)** 에 따라 문장의 각 부분을 판단합니다. 문맥 자유 문법은 간단히 말해서, 무엇이 다른 무엇의 다음에 올 수 있는지 정의한 순서 리스트입니다. 여기서는 연설의 각 부분이 다른 어떤의 뒤에 올 수 있는지 없는지를 정의하는데 쓰였습니다. dust처럼 모호한 단어를 만날 때마다 문맥 자유 문법을 참고해서 그 문법을 따르는 부분을 선택합니다.

> ### 머신 러닝과 머신 트레이닝
추가 예정

그렇다면 문맥에 따라 주어진 단어가 명사인지 동사인지 알 수 있는건 좋지만, 웹 스크레이핑에는 어떤 도움이 될까요?

웹 스크레이핑을 하다 보면 검색에 관련된 문제를 자주 겪게 됩니다. 예를 들어, 어떤 사이트의 텍스트를 수집한 후 거기서 google이라는 단어를 찾되, 고유명사가 아니라 동사로 사용된 것만 찾고 싶을 때가 있을 겁니다. 아니면 반대로, google을 가리키는 단어만 찾고 있는데, 작성자가 대소문자를 정확하게 쓰기만 바라기는 어려울 때도 있습니다.(문장 중간에서 단어의 첫 글자를 대문자로 쓰면 보통 고유명사입니다. 이걸 믿고 대소문자를 가려 Google만 찾으면 실수로 google이라고 쓴 부분은 모두 놓치게 됩니다.) 이럴 때 pos_tag 함수가 대단히 유용합니다.

```python
from nltk import word_tokenize, sent_tokenize, pos_tag
sentences = sent_tokenize("Google is one of the best companies in the world. I constantly google myself to see what I'm up to.")
nouns = ['NN', 'MMS', 'NNP', 'NNPS']

for sentence in sentences:
    if "google" in sentence.lower():
        taggedWords = pos_tag(word_tokenize(sentence))

        for word in taggedWords:
            if word[0].lower() == "google" and word[1] in nouns:
                print(sentence)
```
> 출력 결과입니다.  
Google is one of the best companies in the world.

이 코드는 google(또는 Google)이 동사가 아니라 명사로 사용된 문장만 출력합니다. 물론 더 명확하게 지정해서 NNP(고유명사)로 태그된 Google만 찾게 할 수도 있지만, NLTK라 할지라도 가끔은 실수하기 마련입니다. 애플리케이션에 따라서 융통성을 발휘해야 할 때가 좋을 때도 있습니다.  

자연어의 모호한 부분은 대개 NLTK의 pos_tag 함수로 해결할 수 있습니다. 찾으려는 단어나 구절을 단순히 검색하지 말고 태그와 **함께** 검색한다면 스크레이퍼가 훨씬 정확하고 효율적으로 검색하게 만들 수 있습니다.

## 8.4 추가 자료

컴퓨터로 자연어를 처리, 분석, 이해하는 것은 컴퓨터 과학에서 매우 어려운 일 중 하나이며, 이 주제에 관한 논문과 보고서는 헤아릴 수 없이 많습니다. 여기서 다운 내용을 일상적인 웹 스크레이핑을 넘어 다른 것을 생각할 영감을 얻거나, 자연어 분석이 필요한 프로젝트에 임할 때 방향을 자을 단서에 사용하면 됩니다.  

기초적인 자연어 처리와 NLTK에 관한 자료는 훌륭한 것이 많이 있습니다. 특히 스티븐 버드, 유언 클라인, 에드워드 로퍼가 쓴 <Natural Language Processing with Python> 은 이 주제에 관한 쉽고 자세한 책입니다.  

또한 제임스 푸스테요프스키와 엠버 스텁스의 <Natural Language Annotation for Machine Learning>은 좀 더 높은 수준의 이론적 가이드입니다. 이 책에서 다루는 주제들은 NLTK에서 완벽하게 동작합니다.
