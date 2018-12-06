---
layout: post
section-type: post
title: django - Creating model managers
category: django
tags: [ 'django' ]
---

# Creating model managers

`objects`는 모든 모델의 기본 manager이다.  
하지만 custom manager 역시 만들어서 사용할 수 있다.  
모델에 manager를 추가하는 방법은 두 가지가 있다.  

1. `Post.objects.my_manager()`
2. `Post.my_manager.all()`

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,         self).get_queryset().filter(status='published')

class Post(models.Model):
    objects = models.Manager()  # default manager
    published = PublishedManager() # custom manager
```

`get_queryset()`은 QuerySet을 리턴하는 메소드이다.

```python
Post.published.filter(title__startswith='New')
```
