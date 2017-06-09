---
layout: post
section-type: post
title: ForeignKey limit?
category: diary
tags: [ 'diary' ]
---

http://asc-ind.com/ 이 사이트의 검색기능을 만들고 싶어서 모델을 짜던중에 이해가 안가는 에러가 발생했습니다.

models.py

```python
class Product(models.Model):
parts = models.CharField(max_length=10, unique=True)
engine = models.ForeignKey(Engine)
make = models.ForeignKey(Maker)
other_make = models.ForeignKey(Maker, related_name="other")
model = models.ForeignKey(Model)
models = models.ForeignKey(Model, related_name="models")
type = models.ForeignKey(Type)
```

```
...
AttributeError: 'ForeignKey' object has no attribute 'ForeignKey'
```
분명 ForeignKey는 models의 오브젝트인데 에러는 ForeignKey의 오브젝트라고... 구글링 해도 안나오네요...ㅠ
아 그리고. 모델의 하나의 클래스에 ForeignKey를 사용할 수 있는 갯수 한계가 있을까요?? 저 위에 있는 구성으로 하면 다른 필드를 추가해도 models 가 안먹는것 같아요...

삽질은 언제쯤 끝날까...
