---
layout: post
section-type: post
title: crawling - FaceBook 페이지 크롤러 만들기
category: python
tags: [ 'python' ]
---

## FaceBook 페이지 크롤러 만들기

SNS 중에 아주 많이 사용하고 있는 facebook의 데이터를 Open API를 활용해서 가져오는 크롤러를 만듭니다.  

먼저 facebook SDK를 설치합니다.

```
pip install facebook-sdk
```

Facebook 개발자 페이지 접속하기
<https://developers.facebook.com/>

도구 및 지원 - 그래프 API 탐색기


### 나의 게시물 가져오기

```python
# -*- coding: utf-8 -*-  // 해당 파일은 utf-8형식으로 인코딩을 명시해주는 역할입니다.
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

이렇게 하면 에러가 발생합니다. 파이썬 버전이 업그레이드 되면서 유니코드 관련된 것들이 많이 변경되었기 때문입니다. (파이썬3.5.2 기준)

```python
import facebook
# 생성된 액세스 토큰을 인수로 전달해 사용할 수 있는 객체를 만들어 obj에 저장합니다.
obj = facebook.GraphAPI(access_token="각자의 token")
limit = int(input("몇건의 게시물을 검색할까요? "))
# facebook객체에서 obj.get_connections함수를 실행시킵니다. get_connections함수는 해당 아이디에서 connection_name으로 전달된 데이터를 가져오는 역할을 합니다. 세 번째 인수로 전달된 limit은 한번에 가져올 게시물의 개수를 정해주는 역할을 합니다. 이 프로그램에서는 id에는 me가 전달되었고 connection_name에는 posts가 전달되었습니다. 결과물은 json으로 반환됩니다.
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
일단 response를 출력해보면 데이터가 출력이 되었기 때문에 토큰까지는 정상적으로 넘어가는 것을 확인할 수 있었고, u"---" 방식은 Python 2.x 에서 유니코드를 다룰때 사용하는 것을 알고 있었기 때문에, Python 3.X 버전에 맞게 수정하였습니다. (`enconde("utf-8")`)을 그대로 사용하면 데이터들이 유니코드로 저장됩니다.)

### 특정인이 단 댓글 찾아내기

```python
# -*- coding: cp949 -*-
# 특정 포스트에서 특정인이 쓴 댓글 찾기
import facebook
# 생성한 액세스 토큰을 인수로 전달하고 객체를 돌려 받습니다.
obj = facebook.GraphAPI(access_token="각자의 token")
postid = str(input("포스트 아이디를 입력하세요 : "))
userid = input("찾으실 유저의 이름을 입력하세요 : ")
response = obj.get_connections(id=postid, connection_name="comments", limit=25)
_find = []
while response["data"]:
    for data in response["data"]:
        try:
            if userid == data["from"]["name"].encode("cp949"):
                _data = {}
                _data["id"] = data["from"]["id"]
                _data["name"] = data["from"]["name"]
                _data["created_time"] = data["created_time"]
                _data["message"] = data["message"]
                _find.append(_data)
        except UnicodeEncodeError as e:
            if userid.decode("cp949") == data["from"]["name"]:
              _data = {}
              _data["id"] = data["from"]["id"]
              _data["name"] = data["from"]["name"]
              _data["created_time"] = data["created_time"]
              _data["message"] = data["message"]
              _find.append(_data)
    # 입력받은 이름을 가진 사용자의 댓글을 찾기 위해서는 처음부터 끝까지의 댓글을 모두 검색해야만 합니다. 그러기 위해서 다음 페이지의 존재유무를 판단하고, 다음 페이지가 존재할 경우 response에 다시 get_connections함수를 실행시켜 결과를 저장합니다. 이때 중요한 것은 after인수에 response["paging"]["cursors"]["after"]의 값을 넣어주어야 다음 페이지로 이동합니다.
    if "paging" in response and "after" in response["paging"]["cursors"]:
        after = response["paging"]["cursors"]["after"]
        response = obj.get_connections(id=postid, connection_name="comments", limit=25, after=after)
    else:
        break
f = open("/Users/dokyungkim/Git/Study/crawling_diy/facebook_comment.txt", "w")
for data in _find:
    f.write("==" * 30 + "\n")
    f.write(str(data["created_time"]) + "\n")
    f.write(str(data["message"]) + "\n")
    f.write(str(data["id"]) + "\n")
    f.write(str(data["name"]) + "\n")
    f.write("==" * 30 + "\n")
f.close()
```
위 코드는 기존 파이썬 2.x 버전의 코드를 파이썬 3.x 의 코드로 수정을 한 것입니다. 하지만..

실행하면 파일에 아무런 내용이 저장되지 않습니다.  

일단 에러가 일어 나지 않는다면 데이터쪽의 문제라고 판단을 했습니다.

그러려면 우선 API 에서 데이터를 제대로 받는지, json 구조가 바뀐것은 아닌지 확인해 볼 필요가 있다고 판단하였습니다.

`_find` 는 댓글을 저장하는 변수로, 다음 라인의 while 문에서 댓글을 저장하고 있습니다.

`_find`를 print 해보니 아무런 내용이 없었습니다. 즉, json 구조가 바뀌었다고 판단하게 되었다.

그러면 페이스북의 '그래프 API 탐색기'으로 가서 json이 어떤 구조로 데이터를 반환하는지 살펴봅니다.

![]({{ site.url }}/img/post/python/facebook_json.png)

..............

구조는 다 맞습니다. 뭐지........뭘까............

뜨든!!!

encode("cp949") 을 하면 데이터가 저장되지 않는다...

> cp949는 EUC-KR 인코딩의 확장 버전. 코드페이지 949  
[위키리스크인가 먼가....ㅋㅋㅋㅋ 위키피디아](https://ko.m.wikipedia.org/wiki/%EC%BD%94%EB%93%9C_%ED%8E%98%EC%9D%B4%EC%A7%80_949) 참조


encode 부분을 삭제하면 정상적으로 동작합니다.

![]({{ site.url }}/img/post/python/facebook_results.png)

파이썬의 업데이트로 인해 가장 큰 변화는 인코딩인 것 같습니다.

최종 코딩 소스입니다.

```python
import facebook
# 생성한 액세스 토큰을 인수로 전달하고 객체를 돌려 받습니다.
obj = facebook.GraphAPI(access_token="  각자의 token ")
postid = str(input("포스트 아이디를 입력하세요 : "))
userid = input("찾으실 유저의 이름을 입력하세요 : ")
response = obj.get_connections(id=postid, connection_name="comments", limit=25)
_find = []
while response["data"]:
    for data in response["data"]:
        try:
            if userid == data["from"]["name"]:
                _data = {}
                _data["id"] = data["from"]["id"]
                _data["name"] = data["from"]["name"]
                _data["created_time"] = data["created_time"]
                _data["message"] = data["message"]
                _find.append(_data)
        except UnicodeEncodeError as e:
            if userid == data["from"]["name"]:
              _data = {}
              _data["id"] = data["from"]["id"]
              _data["name"] = data["from"]["name"]
              _data["created_time"] = data["created_time"]
              _data["message"] = data["message"]
              _find.append(_data)
    if "paging" in response and "after" in response["paging"]["cursors"]:
        after = response["paging"]["cursors"]["after"]
        response = obj.get_connections(id=postid, connection_name="comments", limit=25, after=after)
    else:
        break
f = open("/Users/dokyungkim/Git/Study/crawling_diy/facebook_comment.txt", "w")
for data in _find:
    f.write("==" * 30 + "\n")
    f.write(str(data["created_time"]) + "\n")
    f.write(str(data["message"]) + "\n")
    f.write(str(data["id"]) + "\n")
    f.write(str(data["name"]) + "\n")
    f.write("==" * 30 + "\n")
f.close()
```

---
[출처]왕초보!파이썬 배워 크롤러 DIY 하다!....하지만 파이썬 버전이 달라서 고생 좀 했습니다.
