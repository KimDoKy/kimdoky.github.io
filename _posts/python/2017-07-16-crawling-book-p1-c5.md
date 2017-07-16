---
layout: post
section-type: post
title: crawling - P1.스크레이퍼 제작 _ cahp 5. 데이터 저장
category: python
tags: [ 'python' ]
---

터미널로 출력하는 것도 흥미롭지만, 웹 스크레이퍼를 유용하게 활용하려면 스크랩한 정보를 저장할 수 있어야 합니다.  

이번 챕터에서는 3 가지 데이터 관리 방법을 다룹니다.

1. 스크랩한 데이터를 웹사이트에 사용하거나, 직접 API를 만들 생각인가요?
- 데이터베이스가 필요합니다.

2. 인터넷에서 문서를 수집해 하드디스크에 저장할 쉽고 빠른 방법을 찾고 있습니까?
- 파일 스트림이 해결책입니다.

3. 주기적 알림을 받거나, 하루에 한 번 데이터를 집계하려 하나요?
- 스스로에게 이메일을 보내세요.

꼭 웹 스크레이핑이 아니더라도, 최신 애플리케이션에는 대량의 데이터를 저장하고 조작하는 능력이 반드시 필요합니다.

## 5.1 미디어 파일

미디어 파일을 저장하는 방법은 크게 두 가지입니다. 하나는 참조를 저장하는 것이고, 다른 하나는 파일 자체를 내려받는 것입니다. 파일 참조 저장을 간단합니다. 파일이 위치한 URL을 저장하기만 하면 됩니다. 이 방법에는 여러 장점이 있습니다.

- 스크레이퍼가 파일을 내려받을 필요가 없으므로 훨씬 빨리 동작하고, 대역폭도 적게 요구합니다.
- URL만 저장하므로 컴퓨터의 공간도 확보할 수 있습니다.
- URL만 저장하고 파일을 내려받지 않는 코드는 만들기 쉽습니다.
- 큰 파일을 내려받지 않으므로 호스트 서버의 부하도 적습니다.

물론 단점도 있습니다.

- 이들 URL을 당신의 웹사이트나 애플리케이션에 포함시키는 것을 **핫링크** 라 부르는데, 말썽이 생길 소지가 많습니다.
- 애플리케이션에 사용할 미디어 파일을 다른 사람의 서버에 맡기고 싶지 않을 수 있습니다.
- 외부에 있는 파일은 바뀔 수 있습니다. 공개된 블로그 같은 곳에 핫링크 이미지를 쓰면 난처한 일이 생길 수 있습니다. 파일을 더 연구할 목적으로 나중에 저장하려고 했는데, 막상 그 나중이 되니 파일이 사라졌거나 완전히 다른 것으로 바뀌었을 수도 있습니다.
- 실제 웹 브라우저는 페이지의 HTML만 요청하지 않고, 거기 포함된 파일도 내려받습니다. 스크레이퍼에서 파일을 내려받으면 실제 사람이 사이트를 보는 것처럼 보일 수 있고, 이것이 장점이 될 때가 있습니다.

파일을 저장할지 아니면 URL만 저장할지 결정해야 한다면, 그 파일을 한두 번 이상 실제로 보거나 읽을지, 아니면 데이터베이스를 유지하면서 수집하기만 할지 생각해봐야 합니다. 답이 후자라면 그냥 URL만 저장해도 충분합니다.  

만약 전자의 경우라면, 파이썬 3.x에서는 `urllib.request.urlretrieve`을 사용해 원격 URL의 파일을 내려받을 수 있습니다.

```python
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com")
bsObj = BeautifulSoup(html, "html.parser")
imageLocation = bsObj.find("a", {"id": "logo"}).find("img")["src"]
urlretrieve(imageLocation, "logo.jpg")
```

이 코드는 http://pythonscraping.com 에서 로고를 내려받아, 스크랩트를 실행한 디렉터리에 logo.jpg라는 이름으로 저장합니다.  
이 코드는 내려받을 파일이 하나뿐이고, 파일 이름과 확장자를 어떻게 정할지 알고 있다면 잘 동작합니다. 하지만 대부분의 스크레이퍼는 파일 하나만 내려받고 끝나지 않습니다. 다음 코드에서와 같이 http://pythonscraping.com 홈페이지에서 src 속성이 있는 태그에 연결된 내부 파일을 모두 내려받습니다.

```python
import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

downloadDirectory = "downloaded"
baseUrl = "http://pythonscraping.com"

def getAbsoluteURL(baseUrl, source):
    if source.startswith("http://www."):
        url = "http://" + source[11:]
    elif source.startswith("http://"):
        url = source
    elif source.startswith("www."):
        url = source[4:]
        url = "http://"+source
    else:
        url = baseUrl + "/" + source
    if baseUrl not in url:
        return None
    return url

def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace("www.", "")
    path = path.replace(baseUrl, "")
    path = downloadDirectory + path
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    return path

html = urlopen("http://www.pythonscraping.com")
bsObj = BeautifulSoup(html, "html.parser")
downloadList = bsObj.find_all(src=True)

for download in downloadList:
    fileUrl = getAbsoluteURL(baseUrl, download["src"])
    if fileUrl is not None:
        print(fileUrl)

urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))
```
> ### 실행 전에 주의합니다.  
인터넷에서 불확실한 파일을 내려받는 건 위험합니다. 이 스크립트는 만나는 모든 것을 컴퓨터의 하드 디스크에 내려받습니다. 여기에는 스크립트, `.exe`파일, 기타 잠재적 멀웨어가 포함됩니다.  
이 프로그램을 관리자 권한으로 실행한다면 골칫거리를 자초하게 됩니다. 웹사이트에서 발견한 파일이 그 자신을 `../../../../usr/bin/python`으로 이동하는 파일이라면? 다음에 명령줄에서 파이썬 스크립트를 실행하는 순간, 컴퓨터에 멀웨어를 초청하게 되는겁니다.  
이 프로그램은 오직 예시 목적으로 만들어졌습니다. 더 광범위하게 파일 이름을 체크하는 코드 없이 무작위로 배포해서는 안되며, 권한이 제한된 계정에서만 실행해야 합니다. 항상 그렇지만, 파일을 백업하고 예민한 정보는 하드디스크에 저장하지 않으며 상식을 따르면 안전할 수 있습니다.

다음은 실행 결과입니다.

```
http://pythonscraping.com/misc/jquery.js?v=1.4.4
http://pythonscraping.com/misc/jquery.once.js?v=1.2
http://pythonscraping.com/misc/drupal.js?os2esm
http://pythonscraping.com/sites/all/themes/skeletontheme/js/jquery.mobilemenu.js?os2esm
http://pythonscraping.com/sites/all/modules/google_analytics/googleanalytics.js?os2esm
http://pythonscraping.com/sites/default/files/lrg_0.jpg
http://pythonscraping.com/img/lrg%20(1).jpg
```

이 스크립트는 람다 함수를 써서 첫 페이지의 src 속성이 있는 태그를 모두 선택한 후, URL을 손질하고 절대 경로로 바꿔 내려받을 준비를 합니다.(외부링크는 내려받지 않습니다.) 그리고 각 파일을 컴퓨터의 downloaded 폴더 안에 경로를 유지하며 내려받습니다.  

파이썬 os 모듈은 각 파일이 저장될 디렉터리가 있는지 확인하고 없으면 만들기 위해 사용했습니다. os 모듈은 파이썬과 운영체제 사이의 인터페이스 구실을 합니다. 파일 경로를 조작하고, 디렉터리를 만들고, 실행 중인 프로세스와 환경 변수에 관한 정보를 얻고, 그 외에도 여러가지 유용한 일을 할 수 있습니다.

## 5.2 데이터를 CSV로 저장

**CSV(comma-separated values)** 는 스프레드시트 데이터를 저장할 때 가장 널리 쓰이는 파일 형식입니다. 이 파일은 매우 단순하므로 마이크로소프트 엑셀을 비롯해 여러 애플리케이션에서 지원합니다. 다음은 유효한 CSV 파일 예제입니다.

```
fruit,cost
apple,1,00
banana,0.30
pear,1.25
```

파이썬과 마찬가지로 CSV에서도 공백이 중요합니다. 각 행은 줄바꿈 문자로 구분하고, 각 열은 (이름대로) 쉼표로 구분합니다. 탭이나 기타 문자로 행을 구분하는 CSV 파일도 있지만, 이런 형식은 널리 쓰이지 않고 지원하는 프로그램도 많지 않습니다.  
웹에서 CSV 파일을 내려받아, 파싱하거나 수정하지 않고 그대로 저장만 할 것이라면 다른 파일과 마찬가지로 내려받아 CSV 파일로 저장하면 됩니다.  

파이썬 csv 라이브러리를 사용하면 CSV 파일을 쉽게 수정하거나 만들 수 있습니다.

```python
import csv

csvFile = open("./files/test.csv", 'wt')
try:
    writer = csv.writer(csvFile)
    writer.writerow(('number', 'number plus 2', 'number times 2'))
    for i in range(10):
        writer.writerow((i, i+2, i*2))
finally:
    csvFile.close()
```
먼저 염두에 두고 조심할 것이 있습니다. 파이썬을 파일을 만들 때 에러를 거의 일으키지 않습니다. `./files/test.csv`가 존재하지 않으면 파이썬이 파일을 자동으로 만듭니다.(디렉터리를 자동으로 만듭니다.) 파일이 이미 존재하면 파이썬은 test.csv 를 경고 없이 새 데이터로 덮어씁니다.

코드를 실행하면 다음과 같은 CSV 파일이 생깁니다.

```csv
number,number plus 2,number times 2
0,2,0
1,3,2
2,4,4
...
```
웹 스크레이핑에서 자주 하는 일 중 하나는 HTML 테이블을 가져와서 CSV 파일을 만드는 겁니다. 위키백과의 텍스트 에디터 비교(https://en.wikipedia.org/wiki/Comparison_of_text_editors) 항목에는 매우 복잡한 HTML 테이블이 있습니다. 이 테이블에는 색깔도 들어있고, 링크와 정렬 기능, 기타 HTML 코드들이 있는데 CSV 파일로 만들기 전에 이것들을 제거해야 합니다. `BeautifulSoup`와 `get_text()` 함수를 써서 20줄도 안되는 코드로 그 일을 할 수 있습니다.

```python
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://en.wikipedia.org/wiki/Comparison_of_text_editors")
bsObj = BeautifulSoup(html, "html.parser")
# 비교 테이블은 현재 태이블은 현재 페이지의 첫 번째 테이블입니다.
table = bsObj.find_all("table", {"class":"wikitable"})[0]
rows = table.find_all("tr")

csvFile = open("./files/editors.csv", 'wt')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
        for cell in row.find_all(['td', 'th']):
            csvRow.append(cell.get_text())
            writer.writerow(csvRow)
finally:
    csvFile.close()
```
> ### 실무에 쓰기 전에, 잠깐  
HTML 테이블을 CSV 파일로 바꿔야 하는 일이 자주 있다면 이 스크립트를 스크레이퍼에 통합하는 것이 좋습니다. 하지만 딱 한 번만 바꾼다면 더 좋은 방법이 있습니다. 복사해서 붙여 넣기만 하면 됩니다. HTML 테이블의 콘텐츠를 선택해서 복사하고 엑셀에 붙여 넣으면 스크립트를 실행하지 않아도 CSV 파일을 얻을 수 있습니다.

코드를 실행하면 잘 정리된 CSV 파일 `./files/editors.csv`가 만들어 집니다.

## 5.3 MySQL

### 5.3.1 MySQL 설치

### 5.3.2 기본 명령어

### 5.3.3 파이썬과의 통합

### 5.3.4 데이터베이스 테크닉과 모범 사례

### 5.3.5 여섯 다리와 MySQL

## 5.4 이메일
