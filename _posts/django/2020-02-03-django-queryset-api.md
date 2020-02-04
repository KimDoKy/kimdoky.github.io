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

- `annotate()`: `annotate()`의 각 인수는 QuerySet의 각 객체에 추가 될 주석이다. 각 주석은 단순한 값, 모델의 필드에 대한 참조, QuerySet의 각 객체와 관련된 집계(averages, sums 등)이다.

```python
>>> from django.db.models import Count
>>> q =  Blog.objects.annotate(Count('entry'))
>>> q[0].name    # 첫 블로그의 이름
'Blogasaurus'
>>> q[0].entry__count  # 첫 블로그의 항목 수
42

# 키워드 인수를 사용하여 집계 함수를 지정함으로 주석의 이름을 제어할 수 있다.
>>> q = Blog.objects.annotate(number_or_entries=Count('entry'))
>>> p[0].number_or_entries
42
```

- `order_by()`: 정렬 기준을 재정의한다.

```python
Entry.objects.filter(pub_date__year=2005).order_by('-pub_date', 'headline')
```
무작위로 정렬하려면 '?'를 지정하면 된다.

```python
Entry.objects.order_by('?')
# 사용 중인 DB 백엔드에 따라 비싸고 느릴수 있다.
```

다른 모델의 필드를 기준으로 정렬하려면, 이중 언더바(`__`)를 사용한다.

```python
Entry.objects.order_by('blog__name', 'headline')
```

다른 모델과의 관계인 필드를 기준으로 주문하려 하면, Django는 관련 모델의 기본 순을 정렬하거나, Meta.ordering이 지정되지 않으면 모델의 기본 키를 기준으로 한다.

```python
# 순서가 지정되지 않은 경우
Entry.objects.order_by('blog')


# 위 코드는 아래와 같아
Entry.objects.order_by('blog__id')

# name 순으로 정렬할 경우
Entry.objects.order_by('blog__name')

# asc()나 desc()를 사용해 순서를 지정할 수 있다.
Entry.objects.order_by(Coalesce('summary', 'headline').desc())

# asc(), desc()는 null 값이 정렬되는 방법을 제어하는 인수(nulls_first, nulls_last)를 가지고 있다.
```

다중값 필드를 지정하여 정렬할 수 있다(MTM, ForeignKey의 역관계)

```python
class Event(Model):
  parent = models.ForeignKey(
      'self',
      on_delete=models.CASCADE,
      related_name='children'
  )
  date = models.DateField()

Event.objects.order_by('children__date')
```
각 이벤트에 잠재적으로 여러 주문 데이터가 있을 경우 새 QuerySet이 여러번 반환된다. 그렇기 때문에 다중값 필드를 사용하여 결과를 정렬할 때는 주의해야 한다.

`Lower`으로 대소문자를 구분하여 정렬할 수 있다.

```python
Entry.objects.order_by(Lower('headline').desc())
```

`QuerySet.ordered`를 사용하면 QeurySet이 어떤 방식이든 정렬된 경우에는 True를 반환한다.

`order_by()`가 여러 번 선언되어 있다면, 맨마지막꺼만 유효하다.

```python
# headline은 무시되고, pub_date 기준으로 정렬된다.
Entry.objects.order_by('headline').order_by('pub_date')
```

> 정렬에 추가한 각 필드는 DB 비용이 발생한다. 외래키도 암시적으로 포함된다.

- `reverse()`: 역순으로 반환한다.

```python
# 마지막 5개 항목
my_queryset.reverse()[:5]
```

파이썬의 `seq[-5:]`와 같은 기능이지만, SQL에서는 효율적으로 할 수 없기 때문에(끝에서 슬라이싱하는) Django는 엑세스 모드를 지원하지 않는다.

`reverse()`는 QuerySet이 순서가 정의되어 있을 때만 효과가 있다(기본 순서를 정의하는 모델에 대해 쿼리할때, 또는 `order_by()`를 사용할때). 정의된 순서가 없는 경우 효과가 없다.

- `distinct()`: `SELECT DISTINCT`를 사용하는 QuerySet을 반환한다. 쿼리 결과에 중복행을 제거한다.

QuerySet은 기본적으로 중복 행을 제거하지 않지만, 쿼리가 여러 테이블에 걸쳐 있는 경우 중복된 결과를 얻을 수 있다. 그런 경우 `distinct()`를 사용한다.

> `order_by()`에서 사용된 필드는 SQL `SELECT`열에 포함되어 있기 때문에, `distinct()`과 함께 사용될 경우 예상치 못한 결과를 초래할 수 있다.  
관련 모델의 필드별로 정렬하면 해당 필드는 SELECT 열에 추가되지 않아서 중복 행이 구별된 것처럼 보일 수 있다. 추가 행은 반환된 결과에는 나타나지 않기 때문에, 뚜렷하지 않은 결과가 반환되는 것처럼 보인다.  
선택한 열을 제한하기 위해서 `values()`를 사용할 경우, `order_by()`안에 사용된 열이나 기본 모델 순서에서 사용되는 열이 여전히 연관되어 있어, 결과의 고유성에 영향을 미친다.  
`distinct()`을 사용하려면 **관련 모델에 의한 정렬**에 주의해야 한다. `distinct()`와 `values()`를 한께 사용할 때는 `values()` 호출에 없는 필드도 주의해야 한다.

PostgreSQL을 사용할때는 DISTINCT를 적용할 필드를 지정하기 위해 위치 인수(*fields)를 전달할 수 있다.  
일반적으로 `distinct()`를 사용하면 DB는 각 행의 각 필드를 비교하지만, 지정된 필드가 있다면, DB는 지정된 필드만 비교한다.  

필드를 지정할 때 QuerySet에 `order_by()`를 사용해야 하며, `order_by()`의 필드는 같은 순서로 필드를 시작해야 한다.

예를 들어 `SELECT DISTINCT ON(a)`은 a열의 각 값에 대한 첫번째 행을 제공한다. 순서를 지정하지 않으면 임의의 행이 제공된다.  

```python
>>> Author.objects.distinct()
[...]

# 여기부터는 PostgreSQL에서만 동작한다.
>>> Entry.objects.order_by('pub_date').distinct('pub_date')
[...]

>>> Entry.objects.order_by('blog').distinct('blog')
[...]

>>> Entry.objects.order_by('author', 'pub_date').distinct('author', 'pub_date')
[...]

>>> Entry.objects.order_by('blog__name', 'mod_date').distinct('blog__name', 'mod_date')
[...]

>>> Entry.objects.order_by('author', 'pub_date').distinct('author')
[...]
```

> DISTINCT ON 식이 ORDER BY 구문의 시작 부분과 일치하는지 확인하려면 `__id`나 참조 필드를 기준으로 명시적으로 정렬해야 한다.  

```python
# Blog 모델이 name 기준으로 정렬할 경우
Entry.objects.order_by('blog').distinct('blog')
```

쿼리가 `blog__name`으로 정렬되어 DISTINCT ON 식과 일치하지 않기 때문에 작동하지 않을 것이다.

`관계_id`(blog_id)나 참조된 필드(blog_pk)를 명시하여 두 식이 일치하는지 확인해야 한다.

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
