---
layout: post
section-type: post
title: ManyToManyField
category: django
tags: [ 'django' ]
---

ManyToManyField 로 모델간의 관계를 형성하고 migrations를 하면

ManyToManyField를 선언한 쪽에서는 해당 필드가 테이블에 생성되지 않는다.
(ManyToManyField와 같은 related 필드는 SQL문에서 CREATE가 아닌 것으로 추측된다.)

해당 정보 및 추가 내용은 중간자모델이 생성되거나 정의한 중간자모델에 필드로 생성된다.

```python

from django.contrib.auth import get_user_model
from django.db import models

__all__ = (
    'Content',
)

# User모델 가져오기
User = get_user_model()


class Content(models.Model):
    seq = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    place = models.TextField(null=True)
    realm_name = models.TextField(null=True)
    area = models.TextField(null=True)
    price = models.TextField(null=True)
    content = models.TextField(null=True)
    ticket_url = models.TextField(null=True)
    phone = models.TextField(null=True)
    thumbnail = models.TextField(null=True)
    gps_x = models.TextField(null=True)
    gps_y = models.TextField(null=True)
    place_url = models.TextField(null=True)
    place_addr = models.TextField(null=True)
    place_seq = models.TextField(null=True)

    # 중간자 모델인 Bookmark를 이용해 User와 연결
    bookmarks = models.ManyToManyField(User, through='Bookmark')

    # DRF에서 구체적인 공연명을 알기 위한 설정
    def __str__(self):
        return self.title

    # Comment는 추후에 구현
    comment_user = models.ManyToManyField(
        User,
        through='ContentComment',
        related_name='comment_relate',
    )



class ContentComment(models.Model):
    content_d = models.ForeignKey(Content, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

```

위의 코드들에서는 User, Content, ContentComment 3개의 클래스가 관계를 형성하고 있다.

Content에서 MTM을 comment_uset(ContentComment가 뒤에 정의되고 ContentComment에서도 Content를 부르고 있기 때문에 서로 선언하면 선언 시점이 서로 어긋나서 오류가 발생한다. 그렇기 때문에 다른 앱의 모델(User)을 선언하였다.)으로 선언하였다.  
> 아직 정의되지 않은 모델에서 관계를 작성해야하는 경우, 모델 오브젝트 자체가 아닌 모델 이름을 사용할 수 있습니다.

```
from django.db import models

class Car(models.Model):
    manufacturer = models.ForeignKey(
        'Manufacturer',
        on_delete=models.CASCADE,
    )
    # ...

class Manufacturer(models.Model):
    # ...
    pass
```
>[장고 문서](https://docs.djangoproject.com/en/1.11/ref/models/fields/#model-field-types)
(이 부분을 문서에서 늦게 봐서, 모델을 되돌려서 테스트하기엔 늦은것 같아 그대로 사용하였다.)

 ContentComment를 ForeignKey으로 Content와 User를 각각 연결하고 body라는 필드로 TextField를 선언하여 추가정보를 저장하는 중간자 모델로 구현하였다.

![](./images/mtm.png)

ForeignKey로 선언된 필드는 중간자 모델에서 필드명_id 으로 생성되며 관계된 모델의 id 값을 저장한다.

MTM을 사용하면 중간자 모델은 직접 생성하지 않아도 기본적으로 생성이 된다.

models.py 작성시 SQL문이 어떻게 실행되는지 더 공부해야 할 필요가 있다. ([Django Model Document](https://docs.djangoproject.com/en/1.11/topics/db/models/))
