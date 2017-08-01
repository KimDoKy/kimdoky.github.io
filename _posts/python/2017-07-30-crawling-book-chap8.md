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

## 8.3 자연어 툴킷

### 8.3.1 설치

### 8.3.2 NLTK 를 사용한 통계적 분석

### 8.3.3 NLTK 를 사용한 사전적 분석

## 8.4 추가 자료
