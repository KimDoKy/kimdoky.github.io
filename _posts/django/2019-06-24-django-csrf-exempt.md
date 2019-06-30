---
layout: post
section-type: post
title: django - CSRF의 적용을 CBV에서 제외시키기
category: django
tags: [ 'django' ]
---

간단히 HTTP 메소드 관련 몇 가지 테스트를 위해 django endpoint를 만들었지만  

django는 `POST` 메소드에서는 `CSRF verification failed. Request aborted.` 에러를 발생시켰다.

`CSRF`가 무엇인지는 여기서는 건너뜁니다.

Django의 공식 문서에서는 FBV의 예만 보여주고 있고, CBV에서는 [`Decorating CBV`](https://docs.djangoproject.com/en/2.2/topics/class-based-views/intro/#id1)으로 구현하라고 한다.

csrf_exempt가 작동하도록 `dispatch` 메소드에 데코레이터를 붙여야 한다.

이건 뷰 기능 자체의 csrf_exempt 속성을 True로 설정하고, 미들웨어는 가장 바깥 쪽 뷰 기능에서 이를 확인한다.

```python
from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class ViewTest(View):
   @method_decorator(csrf_exempt)
   def dispatch(self, request, *args, **kwargs):
       return super(ViewTest, self).dispatch(request, *args, **kwargs)

   def get(self, request):
       response = "get test"
       return HttpResponse(response)

   def post(self, request, *args, **kwargs):
       response = "post test"
       return HttpResponse(response)
```
