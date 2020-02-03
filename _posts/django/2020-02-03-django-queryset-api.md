---
layout: post
section-type: post
title: django - QuerySet Api reference
category: django
tags: [ 'django' ]
---

> [Django QuerySet Api reference](https://docs.djangoproject.com/en/2.2/ref/models/querysets/#django.db.models.query.QuerySet.values)  

---

한 번쯤은 쿼리셋 부분의 공식 문서를 정독해야겠다는 생각을 이제서야 실천한다..  

---

# QuerySet이 평가되는 경우

Django에서 QuerySet이 평가될 때까지 실제로 데이터베이스 활동이 발생하지 않기 때문에, 데이터베이스에 충돌하지 않고 필터링, 슬라이스 등을 할 수 있다.  

- `iteration`. QuerySet은 반복 가능하며, 처음 반복할 때 데이터베이스 쿼리를 실행한다.

```python
for e in Entry.objects.all():
  pritn(e.headline)
```

- `slicing`. QuerySet은 파이썬의 배열 슬라이싱 구문을 사용하여 자를 수 있다. Django는 슬라이스 구문의 'step' 매개 변수를 사용하면 데이터베이스 쿼리를 실행하고 목록을 반환한다. 평가된 QuerySet을 슬라이싱하면 목록도 반환된다.  

평가되지 않은 QuerySet을 자르면 또 다른 평가되지 않은 QuerySet을 반환하더라고, SQL으로 잘 변환도 안되고, 명확한 의미를 가지지 않기 떄문에 추가로 수정하는 것은 허용하지 않는다.

- `pickling/caching`. [pickling QuerySets](https://docs.djangoproject.com/en/2.2/ref/models/querysets/#pickling-querysets) 참조.

- `repr()`. QuerySet은 `repr()`를 콜할때 평가된다. 이건 파이썬 인터프리터를 위한 것이로, API를 인터프리터로 사용할 때 즉시 결과를 볼 수 있다.

- `len()`. QuerySet은 `len()`을 콜할때 평가된다. 결과 목록의 길이를 반환한다.  
레코드 갯수만 가져오는 것이라면 `SELECT COUNT(*)`이 훨씬 효율적이다.  

- `list()`. `list()`를 사용하여 QuerySet을 강제로 평가할 수 있다.

```python
entry_list = list(Entry.objects.all())
```

- `bool()`. `bool()`을 사용하여 QuerySet을 테스트하면 쿼리가 실행된다. 결과가 하나 이상이면 True, 그렇지 않으면 False를 반환한다.  

```python
if Entry.objects.filter(headline='Test'):
  print("There is at least one Entry with the headline Test")
```

# Pickling QuerySets

- Pickle은 파이썬 객체 구조를 직렬화/역직렬화 할 때 사용한다. [참조: What is Pickle in python?](https://pythontips.com/2013/08/02/what-is-pickle-in-python/)

QuerySet을 선택하면 pickle라기 전에 모든 결과를 메모리에 로드한다. Pickling은 보통 캐싱 전에 사용되며, 캐싱된 QuerySet을 다시 로드하면 결과가 이미 존재하여 사용할 수 있도록 준비하길 원한다.(데이터베이스에서 읽는 것은 캐싱의 목적에 어긋나소 다소 시간이 소요된다.) 즉 QuerySet을 풀 때는 현재의 데이터베이스의 데이터가 아니라 QuerySet을 Pickling 한 순간의 결과이다.  

나중에 데이터베이스에서 QuerySet을 재생성할때 필요한 정보만 선택하려면 QuerySet의 쿼리 속성을 선택하면된다. 그후에 다음과 같은 일부 코드를 사용하여 QuerySet(결과가 로드되지 않은)을 재생성할 수 있다.

```python
import pickle
query = pickle.loads(s) # pickling된 문자열
qs = MyModel.objects.all()
qs.query = query     # 복구된 원래 쿼리
```

> pickle은 django의 버전이 다를때 호환성을 보장하지 않는다.

# QuerySet API

```python
class QuerySet(model=None, query=None, using=None, hits=None)
```

보통 QuerySet을 사용할때 `filter()`를 여려개 연결하여 새로운 QuerySet을 생성한다.  

QuerySet 클래스에는 두 가지 특성이 있다.

- **ordered**: QuerySet이 정렬되어 있다면 True를 반환. QuerySet에 `order_by()`가 되었는지를 판단한다.

- **db**: 현재 QuerySet이 사용하는 DB의 정보를 반환한다.

# 새 QuerySet을 반환하는 함수들

- `filter()`: 지정된 매개 변수와 일치하는 객체를 포함한 QuerySet을 반환한다.

- `exclude()`: 지정된 매개 변수와 일치하지 않는 객체를 포함한 QuerySet을 반환한다.

```python
# pub_date가 2005-1-3 이후이고 headline이 'Hello'인 모든 항목을 제외
Entry.objects.exclude(pub_date__gt=datetime.date(2005, 1, 3), headline='Hello')

# SQL
SELECT *
WHERE NOT (pub_date > '2005-1-3' AND headlint = 'Hello')

# pub_date가 2005-1-3이후이거나 headline이 'Hello'인 모든 항목을 제외
Entry.objects.exclude(pub_date__gt=datetime(2005, 1, 3)).exclude(headline='Hello')

# SQL
SELECT *
WHERE NOT pub_date > '2005-1-3'
AND NOT headline = 'Hello'
```

- `annotate()`

- `order_by()`

- `reverse()`

- `distinct()`

- `values()`

- `values_list()`

- `dates()`

- `datetimes()`

- `none()`

- `all()`

- `union()`

- `intersection()`

- `difference()`

- `select_related()`

- `prefetch_related()`

- `extra()`
 - `select`
 - `where / tables`
 - `order_by`
 - `params`

- `defer()`

- `only()`

- `using()`

- `select_for_update()`

- `raw()`

# 새 QuerySet을 반환하는 연산자들

- `AND(&)`

- `OR(|)`

# QuerySet을 반환하지 않는 함수들

- `get()`

- `create()`

- `get_or_create()`

- `update_or_create()`

- `bulk_create()`

- `bulk_update()`

- `count()`

- `in_bulk()`

- `iterator()`

- `latest()`

- `earliest()`

- `first()`

- `last()`

- `aggregate()`

- `exists()`

- `udpate()`

- `delete()`

- `as_manager()`

- `explain()`

# 필드 검색

- `exact`

- `iexact`

- `contains`

- `icontains`

- `in`

- `gt`

- `gte`

- `lt`

- `lte`

- `startswith`

- `istartswith`

- `endswith`

- `iendswith`

- `range`

- `date`

- `year`

- `iso_year`

- `month`

- `day`

- `week`

- `week_day`

- `quarter`

- `time`

- `hour`

- `minute`

- `second`

- `isnull`

- `regex`

- `iregex`

# 집계 기능

- `expressions`

- `output_field`

- `filter`

- `**extra`

- `Avg`

- `Count`

- `Max`

- `Min`

- `StdDev`

- `Sum`

- `Variance`

# Query-related tools

- `Q()` objects

- `Prefetch()` objects

- `prefetch_related_objects()`

- `FilteredRelation()` objects

-
