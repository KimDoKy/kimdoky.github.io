---
layout: post
section-type: post
title: Django - This field is required
category: django
tags: [ 'django' ]
---

### "This field is required”

위 오류는 DB에 새로운 내용을 넣을 때 발생하는 빈번히 볼 수 있다.  
당연히 필수 필드를 입력하지 않아서 그렇다고 생각하겠지만,  
메소드를 잘못 설정하거나 템플릿에서 설정이 잘못된 경우에도 발생한다.

딱히 오류가 아니기 때문에(설정이 잘못되었을뿐) 로그도 찍히지 않아서 생각보다 잘못된 부분을 찾기 힘들다.

"This field is required” 의 상황을 정리하여 다음 부분들을 확인해보면 된다.

1. 모델의 필수값 설정 : `blank=True` 를 지정했는지 확인.
2. 템플릿 폼 타입 확인 : `form` 태그에서 `enctype=multipart/form-data`이 설정되었는지 확인.
3. 뷰에서 메소드가 잘 지정되었는지 확인 : `request.POST`으로 메소드 지정이 올바르게 되었는지 확인

로그에도 찍히지 않고, 너무나 기본적인 것이라서 눈에 잘 안띈다. 이런 경우 위의 경우를 체크해 보자.
