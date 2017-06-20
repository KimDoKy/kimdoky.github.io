---
layout: post
section-type: post
title: crawling - 서울시 응답소 페이지 크롤러 만들기
category: python
tags: [ 'python' ]
---

## 서울시 응답소 페이지 크롤러 만들기

```python
import urllib.request
from bs4 import BeautifulSoup
import re
import os
# 응답소의 민원 리스트와 민원 페이지를 url 변수에 저장합니다
list_url = "http://eungdapso.seoul.go.kr/Shr/Shr01/Shr01_lis.jsp"
detail_url = "http://eungdapso.seoul.go.kr/Shr/Shr01/Shr01_vie.jsp"

def get_save_path():
    save_path = str(input("저장할 위치와 파일명을 적어주세요. : "))
    save_path = save_path.replace("\\", "/")

    if not os.path.isdir(os.path.split(save_path)[0]):
        os.mkdir(os.path.split(save_path)[0])

    return save_path

def fetch_list_url():
    # urlencode함수를 이용해서 딕셔너리의 형태의 데이터를 인코딩된 문자열의 형태로 변환해서 변수에 저장합니다
    request_header = urllib.parse.urlencode({"page" : "1"})
    # 변수에 저장된 파라미터를 utf-8 형식으로 변환합니다
    request_header = request_header.encode("utf-8")
    # 응답소의 민원 리스트 페이지에 파라미터를 전달합니다
    url = urllib.request.Request(list_url, request_header)
    # 리스트 페이지를 불러와서 utf-8형식으로 변환합니다.
    res = urllib.request.urlopen(url).read().decode("utf-8")

    bs = BeautifulSoup(res, "html.parser")
    listbox = bs.find_all("li", class_="pclist_list_tit2")
    params = []
    for i in listbox:
        params.append(re.search("[0-9]{14}", i.find("a")["href"]).group())

    return params

def fetch_detail_url():
    params = fetch_list_url()
    # get_save_path함수를 실행시켜서 파일을 쓰기모드로 엽니다. 이때 encoding인수의 역할은 파일에 내용을 쓸 때 utf-8형식으로 내용을 쓰겠다는 의미입니다
    f = open(get_save_path(), 'w', encoding="utf-8")

    for p in params:
        # 민원 페이지를 얻기 위한 파라미터를 인코딩시켜 저장합니다
        request_header = urllib.parse.urlencode({"RCEPT_NO" : str(p)})
        # 헤더를 utf-8로 변환하여 저장합니다
        request_header = request_header.encode("utf-8")
        # 민원 내용이 있는 페이지에 파라미터를 전달합니다
        url = urllib.request.Request(detail_url, request_header)
        res = urllib.request.urlopen(url).read().decode("utf-8")

        bs = BeautifulSoup(res, "html.parser")
        div = bs.find("div", class_="form_table")

        tables = div.find_all("table")

        info = tables[0].find_all("td")
        # .get_text(strip=True)는 공백을 제거합니다
        title = info[0].get_text(strip=True)
        date = info[1].get_text(strip=True)

        question = tables[1].find("div", class_="table_inner_desc").get_text(strip=True)
        answer = tables[2].find("div", class_="table_inner_desc").get_text(strip=True)

        f.write("==" * 30 + "\n")

        f.write(title + "\n")
        f.write(date + "\n")
        f.write(question + "\n")
        f.write(answer + "\n")

        f.write("==" * 30 + "\n")

fetch_detail_url()
```

---
[출처]왕초보!파이썬 배워 크롤러 DIY 하다!
