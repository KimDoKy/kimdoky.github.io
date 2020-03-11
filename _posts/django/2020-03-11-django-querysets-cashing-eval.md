---
layout: post
section-type: post
title: django - QuerySets Evaluation and Caching
category: django
tags: [ 'django' ]
---

원문: [Understanding Django QuerySets Evaluation and Caching](https://medium.com/better-programming/understanding-django-database-querysets-and-its-optimizations-1765cb9c36e5)

추가로 읽어 볼 만한 포스팅  
[Django project optimization guide (part 2)](https://dizballanze.com/django-project-optimization-part-2/)  
[Django Database Optimization Tips](https://medium.com/better-programming/django-database-optimization-tips-4e11631dbc2c)
---

Django는 QuerySet을 평가될 때까지 실제로 DB 활동이 발생하지 않기 때문에, DB와 충돌하지 않고 필터링, 슬라이스 등을 할 수 있다.  

여기서 설명할 사용할 모델이다.

```python
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField(blank=True)

    class Meta:
        default_related_name = 'entries'

    def __str__(self):
        return self.headline
```


```python
q1 = Entry.objects.filter(blog=2)
q2 = q1.filter(headline__contains='food')
entry_list = list(q3)
```

위 q1, q2는 모두 데이터베이스에 실행한 것처럼 보이지만 실제론 마지막 코드(`entry_list = list(q3)`)만 데이터베이스에 실행한다.  

QuerySet을 세분화 할 때는 이전 쿼리와 상관없는 별도의 QuerySet을 가져와서 저장, 사용, 재사용을 할 수 있다.  

```python
q =Entry.objects.filter(blog=2).exclude(body_text__icontains="food")

q1 = Entry.objects.filter(blog=2)
q2 = q1.exclude(body_text__icontains="food")
```

q, q2는 데이터베이스 작업을 수행한다.  

평가(Evaluation)는 실제로 데이터베이스에 도달하는 것을 의미한다. QuerySet에서 반복을 시작하면 QuerySet과 일치하는 모든 raw가 데이터베이스에서 패치되어 Django 모델로 변환된다. 그 후 이러한 모델은 QuerySet의 내장 캐시에 저장되기 때문에 QuerySet을 반복 할 때는 데이터베이스를 다시 평가할 필요가 없다.

## Cache 활성화

QuerySet에서 캐시를 사용하려면 QuerySet을 변수에 저장하여 재사용하면 된다. Django의 QuerySet 클래스에는 쿼리 결과(Django models)를 list에 저장하는 `_result_cache` 라는 변수가 있다. QuerySet에 캐시가 없으면 `_result_cache`는 `None`을, 그렇지 않으면 모델 객체 list가 된다. 캐시된 QuerySet을 반복하는 경우 기본적으로 `_result_cache`를 반복한다.

```python
# 다음 두 개의 QuerySet을 작성하고 평가한 후 QuerySet을 저장하지 않아서 재사용을 할 수 없다.
print([e.headline for e in Entry.objects.all()])
print([e.pub_date for e in Entry.objects.all()])

# 다음 코드는 QuerySet을 변수에 저장한다.
# 평가 할 때 결과를 캐시(_result_cache)에 저장한다.
queryset = Entry.objects.all()
# 평가를 반복
for each in queryset:
    print(each.headline)

# 이전 평가의 캐시를 사용
for each in queryset:
    print(each.id)
```

반복하는 것이 평가하는 유일한 방법은 아니다.

## Iteration

QuerySet은 반복이 가능하며, 첫 번째 행을 반복하기 전에 데이터베이스 적중이 발생하고 결과는 캐시에 저장된다.

```python
# 처음 headline을 출력하기 전에 데이터베이스 적중, 캐싱이 발생한다.
queryset = Entry.objects.all()    
# 평가와 캐싱이 일어나는 시점
for each in queryset:
    print(each.headline)

# 이전 평가의 캐시를 사용
for each in queryset:
    print(each.headline)
```

## Slicing

평가되기 전의 QuerySet을 슬라이스하면 새 QuerySet이 반환된다. 반환된 QuerySet은 추가 수정(더 많은 필터나 순서 수정 등)을 허용하지 않지만, 추가 슬라이싱은 허용한다.

```python
# 더 이상 필터를 사용하여 QuerySet을 사용할 수 없다.
queryset = Entry.objects.all()[10:100]
# q1은 필터를 사용할 수 있지만, q2, q3은 필터를 사용할 수 없다.
q1 = Entry.objects.all()
q2 = q1[1:10]
q3 = q2[1:5]

# q1의 캐시에 결과를 저장한다.
lst1 = [each.blog.id for each in q1]
# q2의 캐시에 결과를 저장한다.
lst2 = [each.blog.id for each in q2]
```

이미 평가된 QuerySet을 슬라이스하면 QuerySet 객체가 아니라 객체 list를 반환한다. 평가한 후에 다시 반복하면 QuerySet은 캐시(`_result_cache`) 된 list를 사용한다.

```python
queryset = Entry.objects.all()
lst = list(queryset)
# 초기 객체의 리스트를 반환한다.
first_ten = queryset[:10]
# QuerySet을 슬라이싱하는게 아니라 first_ten을 슬라이싱한다.
first_five = first_ten[:5]
```

평가되지 않은 QuerySet에서 index를 사용하여 하나의 요소를 선택하면 데이터베이스 적중이 발생하지만, 이미 평가된 QuerySet에서 선택하면 캐시를 사용한다.

```python
queryset = Entry.objects.all()
# QuerySet이 평가되기 전이기 때문에 데이터베이스를 조회한다.
print(queryset[5])
lst = list(queryset)
# list()에서 평가가 발생했기 때문에 캐시를 사용한다.
print(queryset[5])
print(queryset[10])
```

파이썬의 슬라이스 문법에서 step 파라미터를 평가 전의 QuerySet에 사용하는 경우는 예외이다. 이 경우는 쿼리를 즉시 실행하고 QuerySet 객체가 아닌 모델 객체 리스트를 반환한다.

```python
entry_list = Entry.objects.all()[1:100:2]
```

## Pickling / Caching

QuerySet을 피클하면 평가된다. QuerySet을 캐시에 저장하면 다음에 평가할 때 캐시에서 모델 객체 리스트를 제공한다.
> [pickle](https://docs.python.org/3/library/pickle.html)

## repr()

QuerySet은 `repr()`을 호출할 때 평가되지만, 결과를 캐시에 저장하지는 않는다.  
`print()`도 마찬가지이다.

```python
# repr()는 평가는 하지만 결과를 캐시에 저장하지는 않는다.
queryset = Entry.objects.all()
str_repr = repr(queryset)
# 캐시를 사용하지 못하기 떄문에 다시 데이터베이스를 실행한다.
for each in queryset:
    print(each.headline)
```

## len()

`len()`을 호출하면 QuerySet이 평가되고 평가된 결과가 캐시에 저장된다.

```python
# len()은 평가와 함께 결과를 캐시에 저장한다.
queryset = Entry.objects.all()
ln = len(queryset)
# 이전 평가의 캐시를 사용
for each in queryset:
    print(each.headline)
```

그렇기 때문에 단지 항목의 갯수만 알아보기 위해 `len()` 대신 `count()`를 사용해야 한다.

## list()

`list()`는 QuerySet을 강제로 평가하고, 모델 객체 리스트를 반환하고 결과를 캐시에 저장한다.

```python
# queryset을 평가하고 결과를 캐시에 저장한다.
queryset = Entry.objects.all()
lst = list(queryset)
# 이전 list() 평가의 캐시를 사용
for each in queryset:
    print(each.headline)
```

## If Statement

if문은 쿼리를 실행하고 결과를 캐시에 저장한다.  
결과가 하나 이상 있으면 True, 아니면 False이다.

```python
queryset = Entry.objects.all()
if queryset:
    # if문에서 평가된 캐시를 사용
    for each in queryset:         
        print(each.headline)
```

## Related Model Attributes는 캐시되지 않는다.

Django가 QuerySet을 평가할 때 `select_related`나 `prefetch_related`를 사용하지 않으면 관계 필드가 쿼리에 포함되지 않기 떄문에 캐시에 포함되지 않는다.

```python
queryset = Entry.objects.all()
    for each in queryset:
        print(each.headline)
        # blog를 위해 데이터베이스 사용
        print(each.blog.name)

    for each in queryset:
        # 캐시 사용
        print(each.headline)
        # 캐시를 사용하지 못하여, blog를 위해 다시 데이터베이스 사용
        print(each.blog.name)

    # select_related 나 prefetch_related를 사용하여 관련 객체를 캐시한다.
    queryset = Entry.objects.select_related('blog')
    for each in queryset:
        print(each.headline)
        print(each.blog.name)

    for each in queryset:
        # 캐시 사용
        print(each.headline)
        # 캐시 사용
        print(each.blog.name)
```
