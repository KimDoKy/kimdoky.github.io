---
layout: post
section-type: post
title: Django Admin에서 related(ForeignKey) 컨트롤 하기
category: django
tags: [ 'django' ]
---

하나의 앨범은 여러 사진을 갖게 되고, 하나의 사진은 하나의 앨범에 귀속되는 모델을 구현하였습니다.

```python
from django.db import models
from django.conf import settings

class Photo(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    photo = models.ImageField()
    create_at = models.DateTimeField(auto_now_add=True)
    # GPS 정보를 저장하기 위한 필드
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    # Album 외래키
    album = models.ForeignKey('Album', on_delete=models.PROTECT)


class Album(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCA
```

 Django Admin에서 확인하기 위해 admin.py 에 등록 합니다.

```python
from django.contrib import admin
from .models import Photo, Album

admin.site.register(Photo)
admin.site.register(Album)
```

이렇게 등록하면 각 해당 모델을 어드민에서 확인이 가능합니다.  

하지만 문제는 각 사진 모델에서는 자신이 포함된 앨범을 확인 및 수정이 가능하지만,  
앨범에서는 모델에 선언된 필드 외에는 외래키 관계를 확인 할 수 없습니다.(shell 에서는 `Album.objects.get(id=1).photo_set.all()`이런식으로 불러올 수 있습니다.)

이와 같이 앨범에서 자신에게 포함된 사진들을 어드민에서 확인 및 수정을 하려면 약간의 작업이 필요합니다.  

```python
class PhotoInline(admin.TabularInline):
    model = Photo

class AlbumAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline,
    ]

admin.site.register(Album, AlbumAdmin)
```

`Inline` 작업을 해주면 앨범 모델에서도 자신에게 귀속된 사진들을 확인 및 편집이 가능합니다.

더 자세한 내용은 [django document](https://docs.djangoproject.com/en/1.9/ref/contrib/admin/#django.contrib.admin.TabularInline)을 읽어보세요.
