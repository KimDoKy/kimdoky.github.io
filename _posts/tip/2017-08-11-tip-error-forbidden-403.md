---
layout: post
section-type: post
title: tip - HTTP Error 403
category: tip
tags: [ 'tip' ]
---
파이썬으로 크롤링 작업 중, 구글의 이미지 검색 페이지를 쿼리문에 맞추어 url을 열려고 했을때
`HTTP Error 403: Forbidden` 에러와 마주치게 되었습니다.

![]({{site.url}}/img/post/python/tip/403.png)

원인을 검색해본 결과 구글이 `urlopen()`으로 하는 작업을 봇(bot)으로 인식하여 차단하는 것이라고 추측하고 있었습니다.  

해결 방법은 의외로 간단합니다. [스택오버플로어](https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping){:target="`_`blank"}에서 친절히 답을 알려주고 있었죠. 바로 헤더를 추가하여 봇이 아니라고 속이는 것입니다.(이 방법으로 봇을 봇이 아니라고 속이는 것 또한 쉽겠죠..)

```python
>>> from urllib.request import Request
>>> hdr = {'referer': 'http://m.naver.com', 'User-Agent': 'Mozilla/5.0'}
>>> req = Request(url, headers=hdr)
>>> print(urlopen(req).read())
b'<!doctype html><html itemscope="" itemtype="http://schema.org/SearchResultsPage" lang="ko"><head><meta content="text/html; ...
```
