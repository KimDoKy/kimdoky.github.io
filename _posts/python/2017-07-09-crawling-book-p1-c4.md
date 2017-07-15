---
layout: post
section-type: post
title: crawling - P1.스크레이퍼 제작 _ cahp 4. API 사용
category: python
tags: [ 'python' ]
---

대형 프로젝트를 다루다 보면 다른 사람들의 코드를 다루면서 고생을 하게 됩니다. 네임스페이스 문제, 타입 문제, 함수 반환 값에 대한 오해, A 지점에서 B 메서드로 정보를 전달하는 것 같은 단순한 문제조차 악몽처럼 복잡해 질 수 있습니다.  

그래서 애플리케이션 프로그래밍 인터페이스(API)가 필요한 것입니다. API는 본질에서 다른 여러 애플리케이션 사이에 간편한 인터페이스를 제공합니다. 애플리케이션을 어떤 프로그래머가 만들었든, 어떤 구조로 만들었든, 심지어 언어가 무엇인지도 상관없습니다. API는 서로 정보를 공유해야 하는 소프트웨어 사이에서 국제어 구실을 하도록 디자인 된 것입니다.  

소프트웨어 애플리케이션이 다양하므로 API 역시 다양하지만, 최근에 API라고 하면 보통 웹 애플리케이션 API로 이해합니다. API가 요청을 보낼 때는 HTTP를 통해 데이터를 요청하며 API는 이 데이터를 XML이나 JSON 형식으로 반환합니다. 대부분의 API가 아직 XML을 지원하지만 JSON을 인토딩 프로토콜로 선택라는 API도 빠르게 늘어나고 있습니다.  

API를 사용하는 건 웹 스크레이핑이 아니라고 생각할 수도 있지만, 거의 같은 테크닉(HTTP 요청 보내기)을 사용해 비슷한 결과(정보 얻기)를 추구합니다. 둘은 상호 보완적일 때가 많습니다.  

예를 들어 웹 스크레이퍼에서 얻은 정보와 API에서 얻은 정보를 결합해 더 유용한 것으로 바꿀 수도 있습니다. 후반부에서 위키백과 편집 내역(IP 주소가 들어 있는)과 IP 주소 해석기 API를 결합해 세계 곳곳에 있는 위키백과를 어떻게 편집하고 있는지 알아보는 프로그램을 만듭니다.  

chap4 에서는 API의 일반적인 개관과 함께 최근 널리 쓰이는 API에 대해 알아보고, 직접 만든 웹 스크레이퍼에서 어떻게 활용할 수 있는지 살펴봅니다.


## 4.1 API는 어떻게 동작하는가

API는 원래 의도만큼 사방에서 쓰이지는 않지만, 다양한 정보에 필요한 API가 존재합니다. 음악과 음악가, 앨범, 음악 스타일과 관련된 정보를 얻을 수 있는 API도 있고, ESPN에서 선수 정보, 게임 정보, 점수 등 여러정보들에 관한 API를 제공합니다. 구글 개발자 섹션(https://console.developers.google.com)에는 언어 번역과 분석, 지오로케이션 등 수십 가지 API가 있습니다.  

API는 사용하기 매우 쉽습니다. 브라우저에 다음을 입력하는 것만으로 간단한 API 요청을 해볼 수 있습니다.

```
http://freegeoip.net/json/50.78.253.58
# 이 API는 IP 주소를 지리적 위치로 변환하는 API입니다.
```
다음과 같은 응답을 얻습니다.

```
{"ip":"50.78.253.58","country_code":"US","country_name":"United States","region_code":"MA","region_name":"Massachusetts","city":"Boston","zip_code":"02116","time_zone":"America/New_York","latitude":42.3496,"longitude":-71.0746,"metro_code":506}
```

API는 HTTP를 통해 동작합니다. 웹사이트에서 데이터를 가져오고, 파일을 내려받고, 기타 인터넷에서 하는 거의 모든 일과 똑같은 프로토콜입니다. API가 일반 웹사이트와 다른 점은 완전히 정형화된 문법을 사용한다는 점, HTML이 아니라 JSON이나 XML로 데이터를 보낸다는 점뿐입니다.

## 4.2 공통 표기법

API는 상당히 표준화된 규칙으로 정보를 제공하며, 그 정보를 생성하는 방법 역시 상당히 표준화되어 있습니다. 덕분에 API가 잘 만들어져 있다면 그 API를 사용하는데 필요한 기초적인 규칙을 빨리 배울 수 있습니다.  

하지만 일부 API는 이런 규칙을 살짝 벗어나기도 하므로, 처음 사용하는 API는 문서를 반드시 읽어야 합니다.

### 4.2.1 메서드

HTTP를 통해 웹 서버에 정보를 요청하는 방법은 다음 네 가지입니다.

- **GET**
- **POST**
- **PUT**
- **DELETE**

**GET** 은 브라우저의 주소 표시줄을 통해 웹사이트에 방문할 때 쓰는 방법입니다. http://freegeoip.net/json/50.78.253.58 을 호출할 때도 GET 메서드를 씁니다. GET 은 웹서버에 정보를 요청할 때 쓰는 방법이라고 생각해도 됩니다.

**POST** 는 폼을 작성하거나, 서버에 있는 스크립트에 정보를 보낼 때 사용합니다. 웹사이트에 로그인할 때마다 사용자 이름과 암호화된 비밀번호를 보낼 때도 POST 요청을 사용합니다. API에 POST 요청을 보내는 건 그 정보를 데이터베이스에 저장하라고 요청을 하는 겁니다.

**PUT** 은 웹사이트에서는 널리 쓰이지 않지만 API에는 가끔 쓰입니다. PUT 요청은 객체나 정보를 업데이트할 때 사용합니다. 예를 들어 새 사용자를 등록할 때는 POST 요청을, 사용자의 이메일 주소를 업데이트할 떄는 PUT 요청을 쓰는 API가 있을 수 있습니다.

> 대부분의 API가 정보를 업데이트할 때도 POST 요청을 사용합니다. 새 항목을 만드는 것인지, 기존 항목을 업데이트하는 것인지 구분하는 방법은 API 요청이 어떻게 만들어졌느냐에 달려 있습니다. 하지만 그 차이를 알아둬서 나쁜 건 없고, 널리 쓰이는 API 중에는 PUT 요청을 사용하는 API도 있습니다.

**DELETE** 는 문자 그대로 어떤 객채를 삭제할 때 사용합니다. 예를 들어 http://myapi.com/user/23 에 DELETE 요청을 보낸다면 그 API는 ID가 23인 사용자를 삭제할 겁니다. 무작위 사용자가 데이터베이스에서 정보를 제거하면 안되므로, 주로 정보의 배포가 목적인 공용 API에서 DELETE 메서드를 쓰는 경우는 별로 없습니다. 하지만 PUT 메서드와 마찬가지로 알아둬서 바쁠건 없습니다.

HTTP 명세에는 다른 HTTP 메서드도 많이 정의되어 있지만, 위 4 가지만 주로 사용합니다.

### 4.2.2 인증

인증을 전혀 사용하지 않는, 즉 애플리케이션에 등록하지 않고도 자유롭게 호출할 수 있는 API도 있지만 최신 API는 어떤 형태로든 인증을 해야 사용할 수 있습니다.

호출 횟수에 따라 비용을 청구하기 위해 인증을 요구하는 API도 있고, 월간 구독 개념으로 서비스를 제공하는 API도 있습니다. 초당, 시간당, 하루당 몇 회로 호출 숫자를 제한하기 위해 인증을 사용하는 곳도 있고, 사용자에 따라 특정 정보에의 접근을 제한하거나 API 호출 타입을 제한하기 위해 인증을 사용하는 곳도 있습니다. 제한 목적이 아니라 마케팅 목적으로 사용자가 무엇을 호출하는지 기록하려고 인증을 요구하는 곳도 있습니다.  

API 인증은 일반적으로 일종의 토큰을 사용하며 API를 호출할 때마다 이 토큰이 웹 서버에 전송됩니다. 사용자가 등록할 때 토큰을 제공하고 영구적으로 쓰는 곳도 있고(보통 높은 수준의 보안이 필요하지 않은 곳), 자주 바뀌며 사용자 이름과 비밀번호 조합에 따라 서버에서 받아오게 하는 곳도 있습니다.  

예를 들어 에코 네스트(Echo Nest) API에 건스 앤 로지스의 노래 목록을 오청하려면 다음과 같이 합니다.

`http://developer/echonest.com/api/v4/artist/songs?api_key=[your api key]&name=guns%20n%27%20reses&format=json&start=0&results=10`

이 요청은 API에 등록할 때 받은 `api_key` 값을 서버에 보내서 서버가 요청자를 라이언 미첼이라고 인식하고, json 데이터를 요청자에게 보냅니다.  

토큰은 요청 자체의 URL에 넣어서 보낼 수도 있고, 요청 헤더에서 쿠키를 통해 보낼 수고 있습니다. 이전에 다룬 urllib 패키지를 통해 보낼 수도 있습니다.

```python
token = "[your api key]"
webRequest = urllib.request.Request("http://myapi.com", headers={"token":token})
html = urlopen(webRequest)
```

## 4.3 응답

API에서 중요한 부분은 그 응답이 정형화되어 있다는 겁니다. 가장 널리 쓰이는 응답 타입은  **XML(Extensible Markup Language)** 과 **JSOM(JavaScript Object Notations)** 입니다.

몇 가지 중요한 이유로 최근에는 JSON 이 XML 보다 더 널리 쓰입니다. 먼저, JSON 파일은 일반적으로 디자인된 XML 파일보다 작습니다.

XML 데이터로  

`<user><firstname>Ryan</firstname><lastname>Mitchell</lastname><username>Kludgist</username></user>`

98 글자인데, 같은 데이터를 JSON으로 나타내면 다음과 같습니다,

`{"user":{"firstname":"Ryan","lastname":"Mitchell","username":"Kludgist"}}`

73 글자이고, XML에 비해 36%만큼 작습니다.

물론 XML으로도 JSON과 같은 형식으로 만들 수도 있습니다.

`<user firstname="ryan" lastname="Mitchell" username="Kludgist"></user>`  

하지만 이런 형식은 중첩된 데이터를 깊숙이 탐색할 수 없으므로 나쁜 형식입니다. 그리고 JSON과 글자 수 차이도 많이 나지 않습니다.  

JSON이 빠르게 퍼진 이유에는 웹 기술의 발전도 있습니다. 과거에는 API를 받는 쪽에서도 PHP나 .NET 같은 서버쪽 스크립트를 쓰는 경우가 많았습니다. 요즘은 앵귤러나 백본 같은 프레임워크가 API 호출을 주고 받습니다. 서버 쪽 기술은 받는 데이터 형식에 다소 완고한 편입니다. 반면 백본 같은 자바스크립 라이브러리는 JSON을 더 선호합니다.  

### 4.3.1 API 호출

API 호출 문법은 API에 따라 크게 다르지만, 몇 가지 표준적이 부분도 존재합니다. GET 요청으로 데이터를 가져올 때, URL 경로는 데이터에 어떻게 찾아가는지를 나타내고 쿼리 매개변수는 일종의 필터 또는 검색에 사용할 추가 요청 구실을 합니다.

예를 들어 가상의 API에, ID가 1234인 사용자가 2014년 8월 한 달 동안 작성한 글을 요청한다면 다음과 비슷한 URL을 사용할 겁니다.  

`http://socialmediasite.com/user/1234/posts?from=08012014&to=08312014`

URL 경로에 API 버전, 원하는 데이터 형식, 기타 속성을 사용하는 API도 있습니다. 예를 들어 위 요청에 추가로 API 버전 4를 사용해서 JSON 형식으로 데이터를 요청한다고 합시다.

`http://socialmediasite.com/api/v4/json/user/1234/posts?from=08012014&to=08312014`  

API 버전과 데이터 형식을 매개변수로 받는 곳도 있습니다.

`http://socialmediasite.com/user/1234/posts?format=json&from=08012014&to=08312014`

## 4.4 에코 네스트

에코 네스트는 웹 스크레이퍼를 기반으로 움직이는 회사의 좋은 예입니다. 판도라처럼 음악으로 수익을 올리는 회사들은 음악을 분류하고 설명을 첨부하는 작업에 사람의 손이 필요하지만, 에코 네스트는 인공지능으로 블로그와 뉴스에서 스크랩한 정보를 음악가, 음악, 앨범으로 분류합니다.  

더 좋은 점은, 비상업적 용도로는 이 API를 무료로 사용할 수 있습니다. 물론 API 키는 필요하지만, 에코 네스트의 계정 생성 페이지(https://developer.echonest.com/account/register)에서 이름과 이메일 주소, 사용자 이름만 등록하면 키를 받을 수 있습니다.
> 현재는 대한민국은 지원하지 않습니다. 그래서 예제는 넘어갑니다.

## 4.5 트위터

트위터는 까다로운 API으로 악명 높지만, 실제 사용자 수는 2억 3천만 명이 넘고 매월 일억 달러 이상의 수익을 올리고 있기 때문에 API로 데이터를 원할 때는 조심스러운 것이 당연합니다.  

트위터의 사용 제한은 두 가지입니다. 15분 사이에 15번 호출, 또는 15분 사이에 180번 호출이며 이 구분은 호출 타입에 따라 다릅니다. 예를 들어 트위터 사용자의 기본 정보를 가져오는건 1분에 12번씩 할 수 있지만, 해당 유저를 팔로잉하는 사람 목록은 1분에 한 번밖에 요청할 수 없습니다.

### 4.5.1 시작하기

사용 제한에 더해, 트위터는 API 키를 받는 것부터 그 키를 사용하는 것까지 다른 API보다 복잡한 승인 시스템을 사용하고 있습니다. API 키를 받으려면 물론 트위터 계정이 필요합니다. 또한 트위터 개발자 사이트(https://apps.twitter.com/app/new)에 '애플리케이션'을 등록해야 합니다.  

등록을 마치면 애플리케이션 기본 정보가 있는 페이지로 이동하는데, 사용자 키도 이 페이지에 있습니다.

![]({{site.url}}/img/post/python/crawling/twitter_developer.png)
> 트위터의 애플리케이션 설정 페이지에는 새 애플리케이션에 대한 기본 정보가 들어 있습니다.

'keys and access tokens'를 누르면 더 많은 정보가 나옵니다.

![]({{site.url}}/img/post/python/crawling/twitter_developer_2.png)
> 트위터 API를 사용하려면 시크릿 키가 필요합니다.

이 페이지에는 어떤 이유로든 시크릿 키가 노출 됐을 때, 자동으로 키를 재 설정하는 버튼도 있습니다.

### 4.5.2 몇 가지 예제

트위터는 OAuth를 기반으로 한 인증 시스템을 사용하는데, 대단히 복잡합니다. 직접 하는 것보다는 이미 나와 있는 라이브러리를 사용하는 것이 좋습니다. 트위터 API를 '손으로' 다루는 건 상당히 복잡하므로, 이 섹션의 샘플은 파이썬 코드를 통해 API에 연결하는데 중점을 둡니다.  

파이썬 트위터 도구 페이지(http://mike.verdone.ca/twitter/#downloads)에서 내려 받거나 pip 등으로 설치하면 됩니다.

> ### 트위터 증명 권한
기본적으로 애플리케이션 접근 토큰에는 읽기 전용 권한이 주어집니다. 이 권한으로도 필요한 일은 대부분 할 수 있지만, 실제 트윗을 작성하는 애플리케이션은 만들 수 없습니다.  
토큰에 읽기/쓰기 권한을 주려면 트위터 애플리케이션 관리 패널의 '권한' 탭으로 이동합니다. 권한 업데이트가 적용되려면 토큰을 재생성해야 합니다.  
마찬가지로, 애플리케이션에서 필요하다면 트위터 계정에 들어오는 다이렉트 메시지에 접근할 수 있도록 토큰 권한을 업데이트할 수 있습니다. 하지만 토큰에는 정말 꼭 필요한 권한만 부여해야 합니다. 일반적으로 여러 애플리케이션에 사용할 토큰을 여러 세트 만들어 사용하는 것이 좋습니다. 지나치게 강력한 토큰을 만들어 그런 권한이 필요하지 않은 애플리케이션에 사용하는 것은 좋지 않습니다.

첫 번째 연습문제로 특정 트윗을 검색해봅니다. 다음 코드는 트위터 API에 연결해서 해시 태그 #python이 들어있는 트윗 목록을 JSON으로 출력합니다. OAuth가 들어 있는 행의 문자열을 실제 키로 교체합니다.

```python
from twitter import *

t = Twitter(aouth=OAuth('Access Token','Access Token Secret','Consumer Key','Consumer Secret'))
pythonTweets = t.search.tweets(q = "#python")
print(pythonTweets)
```
이 스크립트의 출력 결과가 좀 과해 보이는 건 트윗이 생성된 날짜와 시간, 리트윗이나 좋아요에 대한 세부사항, 사용자 계정, 프로필 이미지 등 트윗 한 개당 가져오는 정보가 많아서 그렇습니다. 이 데이터 중 일부만 필요하겠지만, 트위터 API는 API를 통해 가져온 트윗을 자신의 웹사이트에 쓰려는 웹 개발자를 위해 디자인됐으므로 부가 정보가 많이 들어 있습니다.

API를 통해 트윗 하나를 보내고 결과를 봅니다.

```python
from twitter import *

t = Twitter(aouth=OAuth('Access Token','Access Token Secret','Consumer Key','Consumer Secret'))
statusUpdate = t.statuses.update(status='Hello, world!')
print(statusUpdate)
```
> `{'message': 'Status is a duplicate.', 'code': 187}` 에러가 발생한다면, 메시지를 변경해서 다시 해보면 된다. 메시지가 중복되어서 발생하는 에러이다.

![]({{site.url}}/img/post/python/crawling/twitter_developer_3.jpeg)
> 트위터에 입력한 내용으로 트윗 된 것을 확인 할 수 있다.

다음은 결과 JSON입니다.

```
~/Git/Study/crawling/web_scraping/chap4(master*) » python part1_chap4_twitter_2.py
{'favorited': False, 'in_reply_to_screen_name': None, 'id': 885915670877057024, 'lang': 'en', 'created_at': 'Fri Jul 14 17:35:30 +0000 2017', 'truncated': False, 'text': 'Twitter Test', 'place': None, 'in_reply_to_status_id_str': None, 'id_str': '885915670877057024', 'entities': {'symbols': [], 'user_mentions': [], 'urls': [], 'hashtags': []}, 'coordinates': None, 'source': '<a href="http://czarcie.com" rel="nofollow">czarcie scraper</a>', 'is_quote_status': False, 'in_reply_to_status_id': None, 'user': {'followers_count': 25, 'contributors_enabled': False, 'profile_image_url': 'http://pbs.twimg.com/profile_images/1096219848/harpydevil_38_normal.jpg', 'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 'time_zone': None, 'lang': 'en', 'following': False, 'created_at': 'Thu Aug 05 15:36:30 +0000 2010', 'url': 'http://t.co/y1bdxvIKtm', 'profile_sidebar_border_color': 'C0DEED', 'profile_sidebar_fill_color': 'DDEEF6', 'favourites_count': 5, 'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1096219848/harpydevil_38_normal.jpg', 'profile_link_color': '1DA1F2', 'geo_enabled': False, 'profile_text_color': '333333', 'is_translation_enabled': False, 'profile_background_color': 'C0DEED', 'listed_count': 2, 'location': 'Corea. rep', 'is_translator': False, 'translator_type': 'none', 'utc_offset': None, 'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 'statuses_count': 149, 'screen_name': 'Makingfunk', 'notifications': False, 'profile_background_tile': False, 'id_str': '175075821', 'entities': {'url': {'urls': [{'display_url': 'cyworld.co.kr/makingfunk', 'url': 'http://t.co/y1bdxvIKtm', 'expanded_url': 'http://www.cyworld.co.kr/makingfunk', 'indices': [0, 22]}]}, 'description': {'urls': []}}, 'default_profile_image': False, 'profile_use_background_image': True, 'id': 175075821, 'friends_count': 43, 'default_profile': True, 'protected': False, 'has_extended_profile': False, 'follow_request_sent': False, 'verified': False, 'description': 'aLMOND wAFFLEs', 'name': 'Kim Do Kyung'}, 'contributors': None, 'geo': None, 'retweeted': False, 'favorite_count': 0, 'in_reply_to_user_id': None, 'retweet_count': 0, 'in_reply_to_user_id_str': None}
```
트윗 하나를 보낸 결과입니다. 트위터에서 API 접근을 제한하는 이유가 모든 요청에 응답하는데 필요한 대역폭 때문이 아닌가 싶을 정도입니다.  

트윗 목록을 요청할 때는 가져올 숫자를 정할 수도 있습니다.
```python
pythonStatuses = t.statuses.user_timeline(screen_name="montypython", count=5)
print(pythonStatuses)
```
여기서는 @mantypython의 타임라인에 있는 마지막 다섯 트윗(리트윗 포함)을 요청했습니다.

대부분의 사람들이 이 세 가지 예제(트윗 검색, 특정 사용자의 트윗 요청, 트윗 만들기) 정도라면 트위터 API로 하고자 한 일을 충족하겠지만, 트위터 파이썬 라이브러리의 기능은 훨씬 다양합니다 트윗 목록을 검색하거나 조작하고, 다른 사용자를 팔로우하거나 팔로우를 끊거나, 다른 사용자의 프로필 정보를 찾아보는 등 많은 기능이 있습니다. 라이브러리 문서는 깃허브(https://github.com/sixohsix/twitter)를 참고하세요.

## 4.6 구글 API

최근 웹에서 가장 상세하고 쓰기 쉬운 API 컬렉션을 갖춘 곳은 구글입니다. 구글에는 번역, 지오로케이션, 달력 같은 기본적인 것부터 유전학에 관한 API도 있습니다. G메일, 유투브, 블로거 같은 인기 있는 앱의 API도 있습니다.  

구글 API에는 레퍼런스 페이지가 두 개 있습니다. 하나는 제품 페이지(https://developers.google.com/products/)입니다. 이 페이지는 API와 소프트웨어 개발 도구, 기타 소프트웨어 개발자들이 흥미 있어 할 프로젝트의 저장소 구실을 합니다. 다른 하나는 API 콘솔(https://code.google.com/apis/console/)입니다. 이 페이지는 API를 켜거나 끄고, 사용 제한과 사용량을 일목요연하게 정리된 간편한 인터페이스를 제공하며, 원한다면 구글이 제공하는 클라우드 컴퓨팅 인스턴스도 이용할 수 있습니다.  

구글 API는 대부분 무료지만 검색 API 같은 일부 API는 사용료를 지불해야 합니다. 무료 API의 사용 제한은 매우 낮은 편이어서 기본 계정으로도 하루 250번에서 2백만 번까지 요청을 보낼 수 있는 API도 있습니다. 일부 API는 신용카드를 통해 신원 증명을 하면(무료) 제한이 완화되기도 합니다. 예를 들어 구글 플레이스(Places) API의 기본 사용 제한은 하루 1천 번이지만, 신원 증명을 하면 15만 번으로 늘어납니다. [사용 제한과 요금 페이지](https://developers.google.com/places/webservice/usage){:target="`_`blank"}를 참고하세요.

### 4.6.1 시작하기

구글 계정이 있으면 [개발자 콘솔](https://console.developers.google.com/project/){:target="`_`blank"}에서 사용 가능한 API 목록을 확인하고 키를 받을 수 있습니다.  
로그인하거나 계정을 만들면 [API 콘솔 페이지](https://code.google.com/apis/console/){:target="`_`blank"}에서 API 키를 포함한 계정 증명을 볼 수 있습니다. 왼쪽 메뉴에서 '사용자 인증 정보'를 클릭하면 보입니다.

![]({{site.url}}/img/post/python/crawling/google_developer.png)
> 구글의 사용자 인증 정보 페이지

사용자 인증 정보 페이지에서 사용자 인증 정보 만들기 버튼을 클릭해서 API 키를 만들 때 해당 키를 특정 IP 주소나 URL에서만 사용할 수 있게 제한할 수 있습니다. API 키를 제한 없이 쓸 수 있게 만들려면 '제한' 버튼을 누르지 않은 채 API 키를 생성하면 됩니다. 하지만 이렇게 IP 주소를 제한하지 않을 때는 키를 잘 보관해야 합니다. API 키를 사용해서 요청 할 때마다 허용된 사용량이 차감되며, 요청의 인증이 실패해도 사용량이 차감됩니다.  

API 키는 여러 개 만들 수 있습니다. 예를 들어 각 프로젝트에 따라 API 키를 따로 쓰거나 소유한 도메인마다 API 키를 따로 쓸 수 있습니다. 하지만 구글의 API 제한은 계정에 걸리는 것이지 키에 걸리는 것이 아닙니다. API 키를 여러 개 만들면 API 권한을 좀 더 체계적으로 관리할 수 있겠지만, 제한이 완화되지는 않습니다.

### 4.6.2 몇 가지 예제

구글의 가장 유명한 API는 구글 지도 API입니다. 여러 웹사이트에서 구글 지도를 쓰고 있기 때문에 이 기능은 친숙하게 느껴질겁니다. 하지만 구글 지도 API는 단순히 사이트에 지도를 가져다 쓰는 것에 그치지 않습니다. 거리 주소를 위도/경도로 바꾸고, 어느 곳이든 고도를 구하고, 다양한 위치 기반 시각화를 만들고, 임의의 위치에 관한 타임존 정보를 얻는 등 여러 가지 작업을 할 수 있습니다.  
이들 예제를 직접 해보려면 먼저 구글 API 콘솔에서 필요한 API를 활성화해야 합니다. 구글은 어떤 API가 얼마나 활성화되었는지를 근거로 API 사용자 통계를 내고 있으므로 API를 사용하기 전에 명시적으로 활성화해야 합니다.  

구글의 지오코드 API를 사용하면 브라우저에서 단순한 GET 요청을 보내 거리 주소(예제에선 보스턴 과학 박물관 주소)를 위도와 경도로 변환할 수 있습니다.

```json
https://maps.googleapis.com/maps/api/geocode/json?address=1+Science+Park+Boston+MA+02114&key=[API Key]

{
   "results" : [
      {
         "address_components" : [
            {
               "long_name" : "Museum Of Science Driveway",
               "short_name" : "Museum Of Science Driveway",
               "types" : [ "route" ]
            },
            {
               "long_name" : "Boston",
               "short_name" : "Boston",
               "types" : [ "locality", "political" ]
            },
            {
               "long_name" : "Massachusetts",
               "short_name" : "MA",
               "types" : [ "administrative_area_level_1", "political" ]
            },
            {
               "long_name" : "미국",
               "short_name" : "US",
               "types" : [ "country", "political" ]
            },
            {
               "long_name" : "02114",
               "short_name" : "02114",
               "types" : [ "postal_code" ]
            }
         ],
         "formatted_address" : "Museum Of Science Driveway, Boston, MA 02114 미국",
         "geometry" : {
            "bounds" : {
               "northeast" : {
                  "lat" : 42.3687854,
                  "lng" : -71.06963
               },
               "southwest" : {
                  "lat" : 42.3666775,
                  "lng" : -71.07326490000001
               }
            },
            "location" : {
               "lat" : 42.3679381,
               "lng" : -71.07111019999999
            },
            "location_type" : "GEOMETRIC_CENTER",
            "viewport" : {
               "northeast" : {
                  "lat" : 42.3690804302915,
                  "lng" : -71.06963
               },
               "southwest" : {
                  "lat" : 42.3663824697085,
                  "lng" : -71.07326490000001
               }
            }
         },
         "place_id" : "ChIJ3YE7YpZw44kRQKJTFGx_8V0",
         "types" : [ "route" ]
      }
   ],
   "status" : "OK"
}
```

API에 보내는 주소에 특별히 요구되는 형식이 있지는 않습니다. 구글은 구글이라, 지오코드 API는 우편번호 또는 주(미시건 주 등) 정보가 빠져 있거나, 설령 주소에 오타가 있더라도 정확한 주소를 추론해서 사용합니다. 예를 들어 요청 매개변수에 1+Skience+Park+Bostton+MA 처럼 오타를 내거나 우편번호를 쓰지 않아도 같은 결과를 반환합니다.  

위에서 찾은 위도와 경도를 타임존 API에 보내면 타임존 정보를 알 수 있습니다.

```
https://maps.googleapis.com/maps/api/timezone/json?location=42.3677994,-71.0708078&timestamp=1412649030&key=[Api Key]
```

응답은 다음과 같습니다.

```json
{
   "dstOffset" : 3600,
   "rawOffset" : -18000,
   "status" : "OK",
   "timeZoneId" : "America/New_York",
   "timeZoneName" : "Eastern Daylight Time"
}
```
타임존 API에 요청을 보낼 때는 유닉스 타임스탬프(Unix timestamp)가 필요합니다. 구글은 타임스탬프 정보를 이용해 타임존을 서머타임에 맞게 수정해서 제공합니다. 서머타임을 적용하지 않는 지역이라도 타임스탬프가 있어야 API에 요청을 보낼 수 있습니다.  

구글 지도 API는 더 쉽습니다. 위도와 경도를 가지고 고도를 읽어옵니다.

```
https://maps.googleapis.com/maps/api/elevation/json?locations=42.3677994,-71.0708078&key=[Api Key]
```
이 요청은 지정한 위치가 해발 몇 미터인지 반환합니다. '해상도(resolution)'를 함께 알려주는데, 이것은 이 고도를 보간할 때 사용한 데이터 포인트 중 가장 먼 것이 몇 미터 떨어졌는지 나타냅니다. 해상도가 낮을수록 고도가 정확한 겁니다.

```json
{
   "results" : [
      {
         "elevation" : 5.127755641937256,
         "location" : {
            "lat" : 42.3677994,
            "lng" : -71.0708078
         },
         "resolution" : 9.543951988220215
      }
   ],
   "status" : "OK"
}
```

## 4.7 JSON 파싱



## 4.8 모든 것을 하나로

## 4.9 마치며
