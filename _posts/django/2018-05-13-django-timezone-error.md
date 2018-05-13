---
layout: post
section-type: post
title: Django - timezone errors(RuntimeWarning)
category: django
tags: [ 'django' ]
---

한국에서 django로 작업을 할때 timezone settings를 한국에 맞추어서 작업을 하게 된다.

```python
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```

하지만 모델에서 `DateTimeField`를 사용하게 되었을때 `datetime` 라이브러리의 `datetime.now()`를 사용하면 문제점이 발생한다.

```
RuntimeWarning: DateTimeField [모델명].use_date received a naive datetime (2018-05-12 00:47:52.053876) while time zone support is active.
```

timezone을 서울로 입력하였기 때문에 DB에도 같은 시간대로 입력이 되어야 하지만, 실제로는 UTC 기준으로 입력이 된다. 그래서 위과 같은 경고를 띄웁니다.

해결하기 위해서는 `USE_TZ = False`로 설정하면 된다.

그리고 `import datetime` 대신 `from django.conf import timezone`을 사용하여 `datetime.now()`를 사용하면 된다.(라이브러리를 바꾸지 않고 사용해도 크게 오류가 일어나지 않았다. 아직 개발 서버인 sqlite라서 유연하게 넘어갔을 수도 있다. 다른 db에서 테스트해볼 필요가 있다.)  

```python
# 장고 내부적으로 인식하는 시간대를 사용
USE_TZ = True

# local time을 사용
USE_TZ = False
```
