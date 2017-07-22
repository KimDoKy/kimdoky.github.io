---
layout: post
section-type: post
title: crawling - P1.스크레이퍼 제작 _ cahp 6. 문서 읽기
category: python
tags: [ 'python' ]
---

이번 챕터에서는 문서를 다루는 방법을 다룹니다. 로컬 폴더에 내려받거나 직접 읽고 데이터를 추출하는 것 모두 해당합니다. 다양한 텍스트 인코딩에 대해 다루고, 외국어로 된 HTML 페이지도 읽을 수 있게 됩니다.

## 6.1 문서 인코딩

문서 인코딩은 애플리케이션이 그 문서를 읽는 방법을 지정합니다. 인코딩은 보통 파일 확장자에서 추론할 수 있지만, 파일 확장자가 꼭 인코딩에 따라 정해지는 것은 아닙니다. 에를 들어 myImage.jpg를 myImage.txt로 저장해도 아무 문제가 없습니다. 최소한 텍스트 에디터로 그 파일을 열어보기전까지는요. 다행히 그런 상황은 드물고, 문서의 파일 확장자만 알아도 보통은 정확히 읽을 수 있습니다.  

모든 문서는 0과 1으로 인코딩 되어 있습니다. 인코딩 알고리즘은 그 위에서 글자 하나에 몇 비트인지, 이미지 파일이라면 각 픽셀에 몇 비트를 써서 색깔을 나타내는지 정의합니다. 그 위에 다시 PNG 파일처럼 압축 같은 공간 절약 알고리즘이 있을 수 있습니다.  

알맞은 라이브러리를 쓰기만 하면 파이썬은 어떤 형식의 정보라도 제대로 다룰 수 있습니다. 텍스트 파일과 비디오, 이미지 파일의 차이는 0과 1을 어떻게 해석하느냐일 뿐입니다. 이번 챕터에서는 자주 접하는 TXT, CSV, PDF, DOCX에 대해 다룹니다.

## 6.2 텍스트

요즘 온라인에서 평범한 텍스츠 파일을 만나는 일은 드물지만, 서비스에 중점을 두지 않는 사이트나 오래된 형식을 따르는 사이트들은 아직 텍스트 파일을 대량으로 저장하고 있는 곳도 많이 있습닏. 예를 들어 국제 인터넷기술위원회(IETF)는 발행한 문서를 모두 HTML, PDF, TXT 파일로 저장하고 있습니다. (ex. https://ietf.org/rfc/rfc1149.tct) 대부분의 브라우저는 이들 텍스트 파일을 잘 표시하고, 스크랩하는 데도 아무런 문제가 없습니다.  

대부분의 기본적인 텍스트 문서, http://www.pythonscraping.com/pages/warandpeace/chapter1.txt 의 연습용 파일 같은 경우에는 다음 방법을 씁니다.

```python
from urllib.request import urlopen
textPage = urlopen("http://www.scraping.com/pages/warandpeace/chapter1.txt")
print(textPage.read())
```

일반적으로 urlopen으로 페이지를 가져오면 BeautifulSoup 객체로 바꿔서 HTML로 파싱합니다. 여기에서는 페이지를 직접 읽을 수 있습니다. BeautifulSoup 객체로 바꾸는 건 당연히 가능하지만, 파싱할 HTML이 없으므로 효율적이지 않고, 따라서 이 라이브러리를 여기서는 필요 없습니다. 일단 텍스트 파일을 문자열로 읽으면 파이썬에서 다른 문자열을 다루듯 분석할 수 있습니다. 물론 여기엔 단서로 사용할 HTML 태그가 없으므로, 필요한 텍스트와 쓸모없는 텍스트를 구분하기가 쉽지 않습니다. 이런 점이 텍스트 파일에서 정보를 추출할 때 부딪히는 여려운 문제입니다.

### 6.2.1 텍스트 인코딩과 인터넷

파일 확장자만 알면 파일을 정확히 읽을 수 있습니다만, 그 선언은 모든 문서 중에서 가장 기본적인 `.txt`파일에는 적용되지 않습니다.  

대부분은 위의 코드로 텍스트를 읽는데 아무 문제가 없지만, 인터넷의 텍스트에는 함정이 있습니다.  

다음 섹션에서는 영어와 외국어의 인코딩 기본인 ASCII와 유니코드, ISO에 대해 다룹니다.

#### 인코딩 타입 개관

1990년대 초반, 유니코드 컨소시엄이라는 비영리 제단에서 어떤 언어에서도, 어떤 텍스트 문자에서도 사용할 수 있고 모든 글자를 표현할 수 있는 인코딩을 만들려는 시도를 했습니다. 목표는 라틴 알파벳, 키릴문자, 한자, 수학, 논리기호, 이모티콘, 방사능 경고 등 모든 기호를 표현하는 것이었습니다.  
그 결과로 만들어진 인코딩은 UTF-8(Universal Character Set Transformation Format - 8-bit) 입니다. 8비트는 글자를 표시하기 위해 필요한 최소한의 크기입니다. 모든 글자를 8비트로만 저장하면 2^8, 즉 256개밖에 되지 않기 때문에 한자를 포함한 모든 글자를 담는 것은 불가능합니다.  

UTF-8의 각 글자는 '이 글자를 표현하는 데는 1바이트만 사용한다' 또는 '다음 2바이트가 한글자를 나타낸다'는 표시를 시작하며, 최대 4바이트까지 사용합니다. 한글자를 구성하는데 몇 바이트를 사용하는지 지정하는 정보는 각 바이트마다 들어 있으므로 32비트 전체를 사용하지는 못합니다. 실제로 사용하는 것은 21비트이며 총 2,097,152글자를 표현할 수 있고, 현재는 이 중에 1,114,112 글자를 사용하고 있습니다.  

여러 애플리케이션 입장에서 유니코드는 마치 하늘이 내려준 선물과도 같지만, 습관을 버리기 어렵다 보니 여전히 ASCII를 선호하는 사람도 많습니다.  

ASCII는 1960년대부터 사용된 텍스트 인코딩 표준입니다. 각 글자에 7비트를 사용하므로 총 2^7 = 128글자를 쓸 수 있습니다. 이 숫자는 알파벳 대소문자, 구두점 등 일반적인 영어권 사용자의 키보드에 있는 글자를 모두 나타내기에 충분합니다.  

1960년대에는 저장 비용이 상당히 고가였기 때문에 텍스트 파일을 저장할 때 글자당 7비트를 사용하는지 아니면 8비트를 사용하는지가 매우 중요했습니다. 당시의 컴퓨터 과학자들은 1비트를 추가해서 어림수(round number)를 쓰는 편리함과, 7비트만 써서 파일 크기를 줄이는 실용성을 놓고 대립하기도 했지만, 결국 7비트가 승리했습니다. 하지만 최근에는 각 7 비트 앞에 추가로 0을 붙이므로(추가한 비트를 '패딩 비트'라고 합니다.) 당시 논쟁의 나쁜 점만 취한 상황이 됐습니다.(파일은 14% 커졌지만 사용 가능 글자는 128개 뿐이니까요)  

UTF-8을 설계한 사람들은 이 '패딩 비트'를 활용하기로 결정하였습니다. 즉 0으로 시작하는 모든 바이트는 그 바이트 단 하나로 한 글자를 나타내게 만들어, ASCII과 UTF-8의 인코딩 스키마가 완전히 같게 한 겁니다. 다라서 다음 글자들은 UTF-8과 ASCII에서 모두 유효합니다.  

```
0100 0001 - A
0100 0010 - B
0100 0011 - C
```
그리고 다음 글자들은 UTF-8에서만 유효하며, 문서를 ASCII 문서로 해석할 떄는 표현할 수 없습니다.

```
1100 0011 1000 0000 - Å
1100 0011 1001 1111 - ß
1100 0011 1010 0111 - ç
```

UTF 표준에는 UTF-8 외에도 UTF-16,  UTF-24, UTF-32 같은 표준이 있지만, 이들 형식으로 인코드된 문서는 특정 상황이 아니면 거의 만나기 어렵습니다.  

모든 유니코드 표준에 공통인 문제는 ASCII 코드를 벗어나는 문자를 사용하는 문서가 필요 이상 커진다는 겁니다. 사용하는 언어가 100글자 내외만 사용한다 하더라도 각 글자를 나타내는데 최소한 16비트가 필요합니다. 따라서 영어가 아닌 텍스트 문서는 영어로 된 텍스트 문서에 비해 거의 두 배 크기가 됩니다.  

ISO는 각 언어에 특화된 인코딩을 만들어 이 문제를 해결하려 했습니다. ISO 인코딩은 ASCII 같은 인코딩 방식을 택하면서, 모든 글자의 첫 비트를 '패딩 비트'로 만들어 해당 언어에필요한 특수문자에 쓰려 했습니다. 이 방식은 라틴 알파벳(인코딩에서 0~127번)을 많이 사용하고 몇 가지 특수문자가 추가되는 유렵권 언어에는 잘 어울렸습니다. 이에 따라 라틴 알파벳을 위해 디자인 된 ISO-8859-1은 분수나 저작권 기호 같은 특수문자를 쓸 수 있게 됐습니다.  

다른 ISO 문자셋, 예를 들어 ISO-8859-9 (터키어)나 ISO-8859-2 (독일어), ISO-8859-15 (프랑스어) 등도 어느 정도 널리 쓰입니다.  

ISO 인코딩을 사용하는 문서는 최근 줄어들고 있지만, 웹사이트의 9% 정도는 여전히 ISO 인코딩을 사용하고 있습니다. 따라서 이런 내용을 미리 알고, 사이트 스크랩을 시작하기 전에 미리 인코딩을 체크하는 것이 중요합니다.

### 인코딩 예제

이전 섹션에서 urlopen의 기본 설정을 이용해서 텍스트 문서를 열었습니다. 이 방법은 대부분의 영어 텍스트에서는 잘 동작하지만, 러시아어나 아라비아어 등을 만나는 순간 문제가 발생합니다.  

```python
from urllib.request import urlopen
textPage = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1-ru.txt")
print(textPage.read())
```

이 코드는 러시아어와 프랑스어로 쓰인 <전쟁과 평화> 원문의 1장을 읽어 화면에 출력합니다.

```
b"\xd0\xa7\xd0\x90\xd0\xa1\xd0\xa2\xd0\xac \xd0\x9f\xd0\x95\xd0\xa0\xd0\x92\xd0\x90\xd0\xaf\n\nI\n\n\xe2\x80\x94 Eh bien, mon prince.
```
또한 대부분의 브라우저에서 이 페이지를 방문하면 이상항 화면이 보입니다.

![]({{site.url}}/img/post/python/crawling/p1c6_2.png)

러시아어를 모국어로 사용하는 사람조차 이해하기 힘들 겁니다. 문제는 파이썬이 이 문서를 ASCII 문서로 읽으려 했고, 브라우저는 ISO-8859-1 문서로 읽으려 했습니다. 둘 중 어느 하나도 이것을 UTF-8 문서로 인식하지 못했습니다.  

이 문자열이 UTF-8이라고 명시적으로 지정하면 저확히 키릴 문자를 출력할 수 있습니다.

```python
from urllib.request import urlopen
textPage = urlopen("http://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt")
print(str(textPage.read(), 'utf-8'))
```
이 개념을 BeautifulSoup와 파이썬 3.x에 적용된 코드는 다음과 같습니다.

```python
html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html, "html.parser")
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()
content = bytes(content, "UTF-8")
content = content.decode("UTF-8")
```

앞으로 모든 웹 스크레이퍼에서 UTF-8 인코딩을 사용하고 싶어질 겁니다. UTF-8은 ASCII 글자도 문제없이 처리하기 때문입니다. 하지만 웹사이트의 9%가 ISO 버전 중 일부로 인코딩되어 있음을 기억해야 합니다. 텍스트 문서가 어떤 인코딩을 가졌는지 정확하게 판단하는건 불가능합니다. '특수한 문자'나 단어가 아닐 것이다 라는 로직을 써서 문서를 검사하고 인코딩을 짐작하는 라이브러리가 몇 가지 있지만 틀릴 때가 많습니다.  

다행히 HTML 페이지의 인코딩은 보통 <head> 내부의 태그에 들어 있습니다. 대부분의 사이트, 특히 영어로 된 사이트에는 다음과 같은 태그가 들어 있습니다.

```html
<meta charset="utf-8">
```
ECMA 인터내셔널 웹사이트(http://www.ecma-international.org/)에는 이런 태그가 있습니다.
```html
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
```
웹 스크레이핑을 많이 할 계획이고 특히 국제적 사이트에 관심이 있다면, 이 메타 태그를 찾아보고 이 태그에서 지정한 인코딩 방법을 써서 페이지 콘텐츠를 읽는게 좋습니다.

## 6.3 CSV

웹 스크레이핑을 하다 보면 CSV 파일을 만날 때도 많고, 이 형식을 선호하는 동료를 만날 때도 많습니다. 다행히 파이썬엔 CSV 파일을 완벽히 다루는 라이브러리가 있습니다. 이 라이브러리는 CSV의 여러가지 변형도 처리할 수 있습니다. 변형된 CSV를 처리할 일이 생긴다면 [문서](https://docs.python.org/3.4/library/csv.html)를 읽어보세요. 여기서는 표준 형식만 다룹니다.

### 6.3.1 CSV 파일 읽기

파이썬의 csv 라이브러리는 주로 로컬 파일을 가정하고 만들어졌습니다. 하지만 파일이 항상 로컬에 있는 건 아니고, 특히 웹 스크래핑을 할때 그렇습니다. 우회할 방법은 여러 가지가 있습니다.

- 원하는 파일을 직접 내려받은 후 파이썬에 그 파일을 위치를 알려주는 방법
- 파일을 내려받는 파이썬 스크립트를 작성해서 읽고, (원한다면) 삭제하는 방법
- 파일을 문자열 형식으로 읽은 후 StringIO 객체로 바꿔서 파일처럼 다루는 방법

첫 번째와 두 번째 방법도 가능하지만, 쉽게 메모리에서 처리할 수 있는데도 하드 디스크에 파일을 저장하는 것은 좋지 않은 습관입니다. 파일을 문자열로 읽고 객체로 바꿔서 파이썬이 파일처럼 다루게 하는 방법이 더 좋습니다. 다음 스크립트는 인터넷에서 CSV 파일(http://pythonscraping.com/files/MontyPythonAlbums.csv)을 가져와서 터미널에 행 단위로 출력합니다.

```python
from urllib.request import urlopen
from io import StringIO
import csv

data =  urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode('ascii', 'ignore')
dataFile = StringIO(data)
csvReader = csv.reader(dataFile)

for row in csvReader:
    print(row)
```
출력 결과입니다.

```
['Name', 'Year']
["Monty Python's Flying Circus", '1970']
['Another Monty Python Record', '1971']
["Monty Python's Previous Record", '1972']
['The Monty Python Matching Tie and Handkerchief', '1973']
['Monty Python Live at Drury Lane', '1974']
['An Album of the Soundtrack of the Trailer of the Film of Monty Python and the Holy Grail', '1975']
['Monty Python Live at City Center', '1977']
['The Monty Python Instant Record Collection', '1977']
["Monty Python's Life of Brian", '1979']
["Monty Python's Cotractual Obligation Album", '1980']
["Monty Python's The Meaning of Life", '1983']
['The Final Rip Off', '1987']
['Monty Python Sings', '1989']
['The Ultimate Monty Python Rip Off', '1994']
['Monty Python Sings Again', '2014']
```

코드 샘플에서 csv.reader가 반환하는 reader 객체는 순환체(iterable)이며 파이썬 리스트 객체로 구성되어 있습니다. 따라서 csvReader 객체의 각 행은 다음 방법으로 접근 할 수 있습니다.

```python
for row in csvReader:
    print("The album \"" + row[0] + "\" was released in " + str(row[1]))
```
출력 결과입니다.

```
The album "Name" was released in Year
The album "Monty Python's Flying Circus" was released in 1970
The album "Another Monty Python Record" was released in 1971
The album "Monty Python's Previous Record" was released in 1972
The album "The Monty Python Matching Tie and Handkerchief" was released in 1973
The album "Monty Python Live at Drury Lane" was released in 1974
The album "An Album of the Soundtrack of the Trailer of the Film of Monty Python and the Holy Grail" was released in 1975
The album "Monty Python Live at City Center" was released in 1977
The album "The Monty Python Instant Record Collection" was released in 1977
The album "Monty Python's Life of Brian" was released in 1979
The album "Monty Python's Cotractual Obligation Album" was released in 1980
The album "Monty Python's The Meaning of Life" was released in 1983
The album "The Final Rip Off" was released in 1987
The album "Monty Python Sings" was released in 1989
The album "The Ultimate Monty Python Rip Off" was released in 1994
The album "Monty Python Sings Again" was released in 2014
```

첫 번째 행 The album "Name" was released in Year 에 문제가 있습니다. 예제 코드라면 왜 일어났는지 알고 있기 때문에 상관없지만, 실무에서 데이터에 이런 것이 포함되면 안됩니다. 경험이 적은 프로그래머라면 단순히 첫 번째 행을 무시하거나 이런 줄을 처리할 코드를 삽입할 겁니다. 다행히 csv.reader 함수 대신 이 문제를 해결해줄 대안이 있습니다. DictReader 를 사용하면 됩니다.

```python
from urllib.request import urlopen
from io import StringIO
import csv

data =  urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode('ascii', 'ignore')
dataFile = StringIO(data)
dictReader = csv.DictReader(dataFile)

print(dictReader.fieldnames)

for row in dictReader:
    print(row)
```

csv.DictReader는 CSV 파일의 각 행을 리스트 객체가 아니라 딕셔너리 객체로 반환하며, 필드 이름은 변수 dictReader.field에 저장되고 각 딕셔너리 객체의 키로도 저장됩니다.

```
['Name', 'Year']
{'Year': '1970', 'Name': "Monty Python's Flying Circus"}
{'Year': '1971', 'Name': 'Another Monty Python Record'}
{'Year': '1972', 'Name': "Monty Python's Previous Record"}
{'Year': '1973', 'Name': 'The Monty Python Matching Tie and Handkerchief'}
{'Year': '1974', 'Name': 'Monty Python Live at Drury Lane'}
{'Year': '1975', 'Name': 'An Album of the Soundtrack of the Trailer of the Film of Monty Python and the Holy Grail'}
{'Year': '1977', 'Name': 'Monty Python Live at City Center'}
{'Year': '1977', 'Name': 'The Monty Python Instant Record Collection'}
{'Year': '1979', 'Name': "Monty Python's Life of Brian"}
{'Year': '1980', 'Name': "Monty Python's Cotractual Obligation Album"}
{'Year': '1983', 'Name': "Monty Python's The Meaning of Life"}
{'Year': '1987', 'Name': 'The Final Rip Off'}
{'Year': '1989', 'Name': 'Monty Python Sings'}
{'Year': '1994', 'Name': 'The Ultimate Monty Python Rip Off'}
{'Year': '2014', 'Name': 'Monty Python Sings Again'}
```
물론 단점도 있습니다. DictReader는 csvReader에 비해 생성하고, 처리하고, 출력하는데 조금 더 오래 걸립니다. 하지만 매우 간편하고 사용하기 쉬우므로 이 정도 성능 부담은 감수할 만합니다.

## 6.4 PDF

어도비가 1993년에 PDF 문서 형식을 만든 건, 어떤 의미로는 혁명적이라고 해도 좋을 겁니다. PDF는 사용자의 운영체계가 무엇이든 상관없이 이미지와 텍스트 문서를 똑같이 보여주기 때문입니다.  

웹에서 PDF를 사용하는 건 어울리지 않지만(HTML이 있고, 그에 비해 PDF는 더 느리고 정적인 형식이라 사용할 이유가 없습니다) PDF는 아주 널리 사용되고, 특히 공식 서식에 많이 쓰입니다.  

불행히도 파이썬 2.x 용으로 설계된 PDF 파싱 라이브러리들은 대부분 파이썬 3.x 용으로 업그레이드되지 않았습니다. 하지만 PDF는 비교적 단순한 오픈 소스 문서 형식이므로 파이썬 3.x에서 쓸 수 있는 라이브러리도 많이 나와 있습니다.  

PDFMiner3K도 그런 비교적 쉬운 라이브러리 중 하나입니다. 이 라이브러리는 매우 유연해서 명령줄에서 사용할 수도 있고, 기존 코드에 통합할 수도 있습니다. 또 다양한 언어 인코딩을 처리할 수 있습니다. 웹에는 그런 능력이 필요합니다.

```
pip install pdfminer3k
```

다음은 임이의 PDF를 로컬 파일 객체로 바꿔서 문자열로 읽는 기본적인 프로그램입니다.  

```python
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()

    return content

pdfFile = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf");
outputString = readPDF(pdfFile)
print(outputString)
pdfFile.close()
```
출력 결과입니다.

```
CHAPTER I

"Well, Prince, so Genoa and Lucca are now just family estates of
theBuonapartes. But I warn you, if you don't tell me that this
means war,if you still try to defend the infamies and horrors
perpetrated bythat Antichrist- I really believe he is Antichrist- I will
havenothing more to do with you and you are no longer my friend,
no longermy 'faithful slave,' as you call yourself! But how do you
do? I seeI have frightened you- sit down and tell me all the news."
...
```

이 함수의 장점은 로컬 파일을 읽을 때는 urlopen에서 파이썬 파일 객체를 반환받지 않고 다음 행으로 대체하기만 하면 됩니다.

```
pdfFile = open("../chap6/chapter1.pdf", 'rb')
```

출력 결과가 완벽하다고 하긴 어렵습니다. 특히 이미지가 들어 있거나, 텍스트 형식이 이상하거나, 테이블이나 차트 안에 텍스트가 있는 PDF의 경우는 더 나쁩니다. 하지만 대부분의 텍스트 PDF에서는 텍스트 파일이었을 때와 다를 바 없이 출력 결과를 보입니다.

## 6.5 마이크로소프트 워드와 .docx
