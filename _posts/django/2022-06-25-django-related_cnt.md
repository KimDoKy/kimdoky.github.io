---
layout: post
section-type: post
title: Model의 ForeignKey Count 구하기
category: django
tags: [ 'django' ]
---

```python
class Item(models.Model):
    name = models.CharField(max_length=20, unique=True)
    price = models.IntegerField()


class User(models.Model):
    name = models.CharField(max_length=10)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
```

전체 Item에서 FK 관계인 유저의 카운트가 특정 갯수이상인 객체의 갯수를 구하려고 한다.(역참조 카운트)

```python
Item.objects.annotate(cnt=Count('user')).filter(cnt__gte=3).count()
```
