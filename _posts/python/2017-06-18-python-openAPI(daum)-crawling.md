---
layout: post
section-type: post
title: crawling - open API (Daum) 를 활용한 텍스트 크롤러 만들기
category: python
tags: [ 'python' ]
---

## Daum Open API를 사용한 검색 크롤러 생성하기
다음(Daum) 사이트에서 제공하는 Open API를 활용해서 특정 검색어를 주고 기사를 검색하는 크롤러를 만듭니다. 이 크롤러 역시 특정 검색어의 뉴스 전체를 요약한 정보를 크롤링합니다.

### 다음 API Key 발급받기
다음 검색창에 "다음 api"라고 검색하고 접속합니다.
![]({{ site.url }}/img/post/python/daum_api.png)

맨위의 콘솔을 클릭합니다.  
가입하기 창에서 동의하고 완료 버튼을 누릅니다.  
좌측 메뉴 리스트에서 앱만들기 버튼을 누릅니다.  
![]({{ site.url }}/img/post/python/daum_api2.png)

적당한 이름을 입력하고 완료를 누릅니다.  
좌측 아래에 API 키를 선택합니다.
![]({{ site.url }}/img/post/python/daum_api3.png)

REST/JS API 오른쪽에 + 를 누릅니다.
![]({{ site.url }}/img/post/python/daum_api4.png)

모든 플랫폼을 선택하고 완료를 누릅니다.
![]({{ site.url }}/img/post/python/daum_api5.png)

완료하면 api 키가 나타납니다. API 키가 나타나면 복사해줍니다.
![]({{ site.url }}/img/post/python/daum_api6.png)

서비스 - 검색 으로 이동합니다. 화면을 아래로 내려오면 검색 api의 종류가 나타납니다. 그 중에서 웹 검색을 이용합니다.
![]({{ site.url }}/img/post/python/daum_api7.png)

웹 검색 링크를 선택하면 검색 api 를 이용하는 방법이 나옵니다.  
<https://developers.daum.net/services/apis/search/web>  

`https://apis.daum.net/search/web`  

위의 url에서 요청을 위한 파라미터를 추가해서 보내주기만 하면 됩니다.  
제일 기본적으로 api키와 검색어 파라미터, 결과 출력 형태를 지정해서 데이터를 저장해 봅니다.  

### Daum Open API 크롤러 소스 코드 작성

```python
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import os

apikey = "다음 Open API Key"
default_url = "https://apis.daum.net/search/web?output=xml&apikey="

def get_save_path():
    save_path = str(input("저장할 위치와 파일명을 적어주세요. : "))
    # 저장경로가 저장된 변수에서 '\'문자를 '/'문자열로 교체해줍니다
    save_path = save_path.replace("\\", "/")
    # 사용자가 입력한 경로에 폴더가 존재하는지 판단하고 존재하지 않으면 경로에 폴더를 생성합니다.
    if not os.path.isdir(os.path.split(save_path)[0]):
        os.mkdir(os.path.split(save_path)[0])
    return save_path

def get_result_xml():
    search = str(input("검색할 문장을 입력하세요. : "))
    # search변수에 저장된 문자열을 url에 넣을 수 있도록 utf-8포맷으로 변경시켜줍니다.
    search = urllib.parse.quote(search)
    full_url = default_url + apikey + '&q=' + search
    res = urllib.request.urlopen(full_url).read()
    return res

def fetch_result_xml():
    result_xml = get_result_xml()
    # 반환된 xml데이터를 뷰티풀수프 객체에 넣어서 데이터를 뽑아낼 준비를 합니다.
    bs = BeautifulSoup(result_xml, 'html.parser')
    items = bs.find_all("item")
    # get_save_path()함수를 실행시켜서 파일을 쓰기모드로 엽니다. 이때 encoding인수의 역할은 파이렝 내용을 쓸 때 utf-8형식으로 내용을 쓰겠다는 의미입니다.
    f = open(get_save_path(), 'w', encoding='utf-8')

    for item in items:
        date = item.find("pubdate").get_text(strip=True)
        title = item.find("title").get_text(strip=True)
        desc = item.find("description").get_text(strip=True)
        link = item.find("link").get_text(strip=True)
        url = item.find("url").get_text(strip=True)
        f.write("==" * 30 + '\n')
        f.write("게시물 날짜 : " + date + '\n')
        f.write("제목 : " + title + '\n')
        f.write("설명 : " + desc + '\n')
        f.write("링크 : " + link + '\n')
        f.write("URL : " + url + '\n')

        f.write("==" * 30 + '\n')

fetch_result_xml()
```

위의 크롤러는 daum api를 사용하여 만든 가장 기본적인 크롤러입니다. Daum Developers Api 홈페이지에 접속하면 더 다양하고 기본적인 크롤러를 응용할 수 있는 방법이 소개되어 있습니다.

---
[출처]왕초보!파이썬 배워 크롤러 DIY 하다!
