---
layout: post
section-type: post
title: crawling - FaceBook 페이지 크롤러 만들기
category: python
tags: [ 'python' ]
---

## FaceBook 페이지 크롤러 만들기

SNS 중에 아주 많이 사용하고 있는 facebook의 데이터를 Open API를 활용해서 가져오는 크롤러를 만듭니다.  

```
pip install facebook-sdk
```

Facebook 개발자 페이지 접속하기
<https://developers.facebook.com/>

도구 및 지원 - 그래프 API 탐색기


### 나의 게시물 가져오기

```python
# -*- coding: utf-8 -*-
# posts는 내가 작성한 글만을 내 타임라인에서 가져옵니다. 다른 사람이 남긴 글까지 모조리 가져오고 싶다면 feed를 사용해야 합니다.
import facebook
obj = facebook.GraphAPI(access_token="각자의 token")
limit = int(input("몇건의 게시물을 검색할까요? "))
response = obj.get_connections(id="me", connection_name="posts", limit=limit)
f = open("/Users/dokyungkim/Git/Study/crawling_diy/facebook.txt", "w")

for data in response[u"data"]:
    f.write("==" * 30 + "\n")
    f.write("게시물 작성자 : " + data[u"from"][u"name"].encode("utf-8") + "\n")
    f.write("게시물 아이디 : " + data[u"from"][u"id"].encode("utf-8") + "\n")
    f.write("최종 업데이트 시간 : " + data[u"updated_time"].encode("utf-8") + "\n")
    f.write("게시물 링크 : " + data[u"actions"][0][u"link"].encode("utf-8") + "\n")
    if u"message" in data:
        f.write("게시물 내용 : " + data[u"message"].encode("utf-8") + "\n")
    if u"picture" in data:
        f.write("게시물 사진 이름 : " + data[u"name"].encode("utf-8") + "\n")
        f.write("사진 주소 : " + data[u"picture"].encode("utf-8") + "\n")
    if u"description" in data:
        f.wrtie("사진 설명 : " + data[u"description"].encode("utf-8") + "\n")
    f.write("==" * 30 + "\n")
    f.close()
```
....

이렇게 하면 에러가 발생합니다. 파이썬 버전이 업그레이드 되면서 유니코드 관련된 것들이 많이 변경되었기 때문입니다.

```python
import facebook
obj = facebook.GraphAPI(access_token="각자의 token")
limit = int(input("몇건의 게시물을 검색할까요? "))
response = obj.get_connections(id="me", connection_name="posts", limit=limit)
f = open("/Users/dokyungkim/Git/Study/crawling_diy/facebook_post.txt", "w")

for data in response["data"]:
    f.write("==" * 30 + "\n")
    f.write("게시물 작성자 : " + str(data["from"]["name"]) + "\n")
    f.write("게시물 아이디 : " + str(data["from"]["id"]) + "\n")
    f.write("최종 업데이트 시간 : " + str(data["updated_time"]) + "\n")
    f.write("게시물 링크 : " + str(data["actions"][0]["link"]) + "\n")
    if "message" in data:
        f.write("게시물 내용 : " + str(data["message"]) + "\n")
    if "picture" in data:
        f.write("게시물 사진 이름 : " + str(data["name"]) + "\n")
        f.write("사진 주소 : " + str(data["picture"]) + "\n")
    if "description" in data:
        f.write("사진 설명 : " + str(data["description"]) + "\n")
    f.write("==" * 30 + "\n")
f.close()
```

대화식 python을 실행해서 에러가 발생하는 부분은 하나하나 찾아봤습니다.  
일단 response를 출력해보면 데이터가 출력이 되었기 때문에 토큰까지는 정상적으로 넘어가는 것을 확인할 수 있었고, u"---" 방식은 Python 2.x 에서 유니코드를 다룰때 사용하는 것을 알고 있었기 때문에, Python 3.X 버전에 맞게 수정하였습니다.

코드해석 추가 예정.

### 특정인이 단 댓글 찾아내기

```python
# -*- coding: cp949 -*-
# 특정 포스트에서 특정인이 쓴 댓글 찾기
import facebook
# 생성한 액세스 토큰을 인수로 전달하고 객체를 돌려 받습니다.
obj = facebook.GraphAPI(access_token="각자의 token")
postid = str(input("포스트 아이디를 입력하세요 : "))
userid = input(u"찾으실 유저의 이름을 입력하세요 : ")

response = obj.get_connections(id=postid, connection_name="comments", limit=25)
_find = []
while response[u"data"]:
    for data in response[u"data"]:
        try:
            if userid == data[u"from"][u"name"].encode("cp949"):
                _data = {}
                _data["id"] = data[u"from"][u"id"]
                _data["name"] = data[u"from"][u"name"]
                _data["created_time"] = data[u"created_time]
                _data["message"] = data[u"message"]
                _find.append(_data)
        except UnicodeEncodeError as e:
            if userid.decode("cp949") == data[u"from"][u"name"]:
              _data = {}
              _data["id"] = data[u"from"][u"id"]
              _data["name"] = data[u"from"][u"name"]
              _data["created_time"] = data[u"created_time]
              _data["message"] = data[u"message"]
              _find.append(_data)
if u"paging" in response and u"after" in response[u"paging"][u"cursors"]:
    after = response[u"paging"][u"cursors"][u"after"]
    response = obj.get_connections(id=postid, connection_name="comments", limit=25, after=after)
else:
    break
f = open("/Users/dokyungkim/Git/Study/crawling_diy/facebook1.txt", "w")
for data in _find:
    f.write("==" * 30 + "\n")
    f.write(data["created_time"].encode("utf-8") + "\n")
    f.write(data["message"].encode("utf-8") + "\n")
    f.write(date["id"].encode("utf-8") + "\n")
    f.write(data["name"].encode("utf-8") + "\n")
    f.write("==" * 30 + "\n")
f.close()
```

파이썬 버전에 맞게 수정 테스트 예정.

코드 분석 추가 예정.

---
[출처]왕초보!파이썬 배워 크롤러 DIY 하다!....하지만 파이썬 버전이 달라서 고생 좀 했습니다.
