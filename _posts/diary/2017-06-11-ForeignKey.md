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


---
[askdjango](https://www.facebook.com/groups/askdjango/){:target="_blank"}의 이진석님께서 도움을 주셨습니다.  

```
외래키 갯수 제한은 없습니다.

아래 코드에서 모델명이 models 라서
models = models.ForeignKey(Model, related_name="models")

다음 줄에서 참조 오류가 뜬 것입니다.
type = models.ForeignKey(Type)

그런데, 다음 정의는 중복같습니다.
model = models.ForeignKey(Model)
models = models.ForeignKey(Model, related_name="models")

model 만 있어도 충분할 듯 합니다.
```

ForeignKey의 갯수 제한은 없다는 것과 네이밍의 중요성을 다시 한번 깨닫게 되었습니다.
