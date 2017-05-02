---
layout: post
section-type: post
title: custom params
category: rest
tags: [ 'rest', 'diary' ]
---

REST search parameter 를 커스텀 해달라는 요청이 들어왔다.

REST search는 `filters.SearchFilter`를 명시해줌으로써 사용이 가능하지만, 기본적으로 검색 파라미터의 이름은 `search`이지만 `SEARCH_PARAM` 설정으로 재정의 될 수 있다. 자세한 내용은 [장고 문서](https://docs.djangoproject.com/en/1.11/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields)를 참조해야한다. (하지만 그닥 도움은 안되는 것 같다. 내가 못찾는건가..)

저 파라미터 설정은 (가상환경설정시) 'pyenv/versions/가상환경/lib/python3.5/site-packages/rest_framework/setting' 의 DEFAULTS - Filtering 에 명시되어 있다.

```python
# Filtering
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
```

이 값을 변경하면 원하는 파라미터명을 사용할 수 있다.

하지만 문제점이 있다. Git에는 가상환경에 설정한 부분이 포함되지 않는다. 협업에 적용이 되지 않는다.
배포 담당자가 서버에 직접 접속하여 rest_frame에 들어가서 설정값을 변경해주면 가능할 것 같지만, 위험하고 비효율적인것 같다. 다른 방법을 찾아야 한다.
>해결방법은 다음 포스트에..  
> <https://kimdoky.github.io/diary/2017/04/20/custom-param2.html>
