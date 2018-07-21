---
layout: post
section-type: post
title: Python - 동적으로 변수 생성하기
category: python
tags: [ 'python' ]
published: false
---

## 동적으로 변수 생성하기

```python
i = 0
while i <= int(count):
    file_name = input('파일명을 입력하세요. ')
    exec("%s_path=''" % (file_name))
    i += 1
```
> 주의점. `exec()`함수는 함수 안에 선언하면 작동하지 않는다. 함수형 프로그래밍으로 진행하다가 이 점에 대해 구글링으로도 발견하지 못해서 한참 삽질을 하였다...


## 생성된 변수 확인하기

```python
def inquiry_func():
    path_category = ([v for v in globals().keys() if v.endswith('path')])
    print(path_category)
```
