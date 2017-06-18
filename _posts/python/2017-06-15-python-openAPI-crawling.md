---
layout: post
section-type: post
title: crawling - open API (Naver) 를 활용한 텍스트 크롤러 만들기
category: python
tags: [ 'python' ]
---
## Naver의 open API를 활용한 텍스트 크롤러 생성하기

Naver의 Open API 기능을 사용하려면 먼저 네이버에 가입되어 있어야 하고 두 번째로 네이버에서 Open API 키를 발급받아야 합니다.

a. 네이버 개발자센터 홈으로 들어갑니다. <https://developers.naver.com/main/>  

![]({{ site.url }}/img/post/python/naver_api.png)
하단에 API를 누릅니다.  

![]({{ site.url }}/img/post/python/naver_api1.png)

오픈 api 이용 신청을 합니다.  

사용하기 위한 절차들을 진행합니다.  

![]({{ site.url }}/img/post/python/naver_api2.png)  

성공하면 Client ID를 발급받게 됩니다. Client ID를 복사해서 소스코드의 API_Key 부분에 붙여넣기만 하면 됩니다.  

```python
import urllib.request
import urllib.parse

from bs4 import BeautifulSoup

defaultURL = 'https://openapi.naver.com/v1/search/news.xml?'
# 새로운 API에서 사용하는 요청 변수를 각각의 변수에 담아둡니다.
sort = 'sort=sim'
start = '&start=1'
display = '&display=100'
query = '&query=' + urllib.parse.quote_plus(str(input("검색어를 입력하세요: ")))  # 사용자에게 검색어를 입력받아 quote_plus 함수로 UTF-8 타입에 맞도록 변환시켜 줍니다.
fullURL = defaultURL + sort + start + display + query
print(fullURL)
file = open("/Users/dokyungkim/Git/Study/crawling_diy/naver_news.txt", "w", encoding='utf-8')
headers = {
    'Host' : 'openapi.naver.com',
    'User-Agent' : 'curl/7.43.0',
    'Accept' : '*/*',
    'Content-Type' : 'application/xml',
    'X-Naver-Client-Id' : '여기에 ID를 넣어용',
    'X-Naver-Client-Secret' : '여기에 secret을 넣어용'
 }
 # HTTP 요청을 하기 전에 헤더 정보를 이용해 request 객체를 생성합니다. urllib 모듈에서 헤더 정보를 서버에 전달할 때 사용하는 대표적인 방법입니다.
req = urllib.request.Request(fullURL, headers=headers)
# 생성된 request객체를 uplopen함수의 인수로 전달합니다. 이렇게 되면 헤더 정보를 포함하여 서버에게 HTTP 요청을 하게 됩니다.
f = urllib.request.urlopen(req)
resultXML = f.read()
xmlsoup = BeautifulSoup(resultXML, 'html.parser')
items = xmlsoup.find_all('item')
for item in items:
    file.write('--------------------------\n')
    file.write('뉴스제목 : ' + item.title.get_text(strip=True) + '\n')
    file.write('요약내용 : ' + item.description.get_text(strip=True) + '\n')
    file.write('--------------------------\n')

file.close()
```

>
API 가이드
>
요청 변수
>
요청변수 | 타입 |  필수 | 기본값 | 설명
---|---|---|---|---
query | string | Y | - | 검색을 원하는 문자열로서 UTF-8로 인코딩한다
display | int | N | 10~100 | 검색 결과 출력 건수 지정
start | int | N | 1~1000 | 검색 시작 위치로 최대 1000까지 가능
sort | str | N | sim(기본), date | 정렬 옵션: sim(유사도순), date(날짜순)
>
출력 결과
>
필드 | 타입 | 설명
---|---|---
rss |-| 디버그를 쉽게 하고 RSS 리더기만으로 이용할 수 있게 하기 위해 만든 RSS 포맷의 컨테이너이며 그 외의 특별한 의미는 없다.
channel |- |검색 결과를 포함하는 컨테이너이다. 이 안에 있는 title, link, description 등의 항목은 참고용으로 무시해도 무방하다.
lastBuildDate|datetime| 검색 결과를 생성한 시간이다.
total| int| 검색 결과 문서의 총 개수를 의미한다.
start| int| 검색 결과 문서 중, 문서의 시작점을 의미한다.
display |int |검색된 검색 결과의 개수이다.
item| -| 개별 검색 결과이며 title, originallink, link, description, pubDate 를 포함한다.
title| str| 개별 검색 결과이며, title, originallink, link, description, pubDate 를 포함한다.
originallink |str |검색 결과 문서의 제공 언론사 하이퍼텍스트 link 를 나타낸다.
link |str| 검색 결과 문서의 제공 네이버 하이퍼텍스트 link 를 나타낸다.
description |str|검색 결과 문서의 내용을 요약한 패시지 정보이다. 문서 전체의 내용은 link 를 따라가면, 읽을 수 있다. 패시지에서 검색어와 일치하는 부분은 태그로 감싸져 있다.
pubDate |datetime| 검색 결과 문서가 네이버에 제공된 시간이다.
>
에러 메시지
>
HTTP 코드 | 에러코드 |에러 메시지 |조치방안
400| SE01| Incorrect query request (잘못된 쿼리요청입니다.)|검색 API 요청에 오류가 있습니다. 요청 URL,필수 요청 변수가 정확한지 확인 바랍니다.
400| SE02| Invalid display value (부적절한 display 값입니다.)| display 요청 변수값이 허용범위(1~100)인지 확인해 보세요.
400| SE03| Invalid start value (부적절한
start 값입니다.)|start 요청 변수값이 허용벙위(1~1000)인지 확인해 보세요.
400| SE04 |Invalid sort value (부적절한 sort 값입니다.)| sort 요청 변수 값에 오타가 없는지 확인해 보세요.
404| SE05 |Invalid search api (존재하지않는 검색 api 입니다.) 검색 API 대상에 오타가 없는지 확인해 보세요.
500 |SE99| System Error (시스템 에러)| 서버 내부 에러가 발생하였습니다.
>
---
>
HTTP에서 사용하는 헤더란, 서버에게 지금 요청을 하는 사용자에 대한 정보가 담겨 있는 데이터들입니다. 예를 들어, 입국 심사처럼 나의 국적은 어디인지, 어느 나라를 통해서 왔는지, 이 나라에 무슨 목적으로 왔는지 등 이런 정보가 기재되어 있습니다. 이와 같이 헤더를 서버에 전달하여 브라우저의 종류는 무엇이고, 어떤 유형의 데이터를 받는지, 어디에서 페이지를 접속했는지 등 서버에 전당하는 역할을 합니다.  
>
그렇기 때문에 입국 심사에서 통과하지 못했을 때 입국을 거절 당하는 것처럼, 서버에서 요구하는 특정 헤더의 정보가 잘못 되었거나 존재하지 않을 경우에는 서버쪽에서 사용자의 데이터 요청을 거절할 수 있습니다.  
>
하지만 헤더의 정보를 따로 전달해주지 않았을 경우는 어떻게 될까요?  
>
예를 들어 입국 심사의 절차에서 아무것도 묻지도 않는다면 입국이 되지 않을 이유는 없을 것입니다. 이와 같이 서버 쪽에서도 반드시 필요로 하는 헤더의 정보 같은 필수 헤더 정보가 따로 존재하지 않는다면 사용자의 요청에 언제나 응답해주는 서버가 되는 것입니다.  
>
현재 네이버에서 요구하는 헤더의 정보는 애플리케이션을 등록하고 발급받는 Client ID와 Client secret입니다. 이 정보가 누락되거나 잘못된 정보가 전달 되었을 경우에는 네이버 쪽 서버에서 데이터 요청을 거부 할 수 있습니다.

위 코드가 실제 동작하는지 실행하면 순식간에 크롤링이 됩니다.

```
~/Git/Study/crawling_diy(master*) » python sample1.py
검색어를 입력하세요:  python
https://openapi.naver.com/v1/search/news.xml?sort=sim&start=1&display=100&query=python
```

소스에서 지정된 파일이 생성되고 실행해보면 아래와 같이 저장되었음을 확인 할 수 있습니다.

```
~/Git/Study/crawling_diy(master*) » cat naver_news.txt
--------------------------
뉴스제목 : 이젠아카데미컴퓨터학원, &lt;자바(Java)와 파이썬(<b>Python</b>)을 활용한 빅데이터(R...
요약내용 : 이젠아카데미컴퓨터학원이 이공계열 대학 졸업생의 취업 경쟁력을 강화하고자 &lt;자바(Java)와 파이썬(<b>Python</b>)을 활용한 빅데이터(R) 분석&gt; 무료교육과정을 시행한다고 밝혔다. &lt;자바(Java)와 파이썬(<b>Python</b>)을 활용한...
--------------------------
--------------------------
뉴스제목 : [유명환의 하드하지 않은 하드웨어 이야기] 아두이노·라즈베리파이는 완성품...
요약내용 : 또 아두이노의 스케치(Sketch)나 라즈베리 파이에서 권장하는 파이썬(<b>Python</b>)은 코드를 구현하기는 쉽지만 실제 제품 개발에서 꼼꼼하게 하나하나 레지스터들을 설정하고 제어하기에는 C 언어에 비해 다소 미흡하다....
--------------------------
--------------------------
뉴스제목 : INDONESIA <b>PYTHON</b> SWALLOWS MAN
요약내용 : A <b>python</b> swallowed a villager in Indonesia A handout photo made available by the West Sulawesi Police on 30 March 2017 shows a villager covering the body of a victim who was swallowed by a <b>python</b>...
--------------------------
```

만약 블로그를 크롤링하고 싶을 경우에는 `defaultURL`을 수정해주면 됩니다.
---
[출처]왕초보!파이썬 배워 크롤러 DIY하다
