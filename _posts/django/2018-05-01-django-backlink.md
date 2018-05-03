---
layout: post
section-type: post
title: Django templtes - back link
category: django
tags: [ 'django' ]
---

링크를 연결하다보면 명시적으로 URL을 맵핑해줄 수 없는 경우가 있다.  
바로 이전 페이지로 링크하는 것이다.

역시나 [stack overflow](https://stackoverflow.com/questions/524992/django-templates-create-a-back-link?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)에 친절히 답변이 달려있다.

답변에 따르면


템플릿에서는 아래처럼 링크를 걸어준다.
```html
<a href="{{ request.META.HTTP_REFERER }}">Go back</a>
```

링크를 걸기전에 `TEMPLATE_CONTEXT_PROCESSORS` 설정을 `django.core.context_processors.request` 를 지정해주어야 한다.  

장고 2.0에서는 기본으로 설정되어있다.
