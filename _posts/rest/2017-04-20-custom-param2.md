---
layout: post
section-type: post
title: custom params 해결
category: rest
tags: [ 'rest' ]
---

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'SEARCH_PARAM': 'q',
}
```

파라미터명 변경건은 셋팅에 전역으로 선언해주면 해결된다.


```
class CustomFilter(SearchFilter):
    parameter_name = 'q'
```
커스텀으로 따로 처리하려고 만들었지만 정확히 어떤걸 오버라이드 해야하는지 모르겠다.

일단 전역으로 선언하여 해결하였다.

---

Comment 개선사항

1. 로그인 구분(토큰?)  
분업으로 인해서 담당 업무자에게 물어봐야함.

2. 추가, 수정, 삭제 조건
