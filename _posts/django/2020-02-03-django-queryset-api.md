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

### `filter()`

지정된 매개 변수와 일치하는 객체를 포함한 QuerySet을 반환한다.

### `exclude()`

지정된 매개 변수와 일치하지 않는 객체를 포함한 QuerySet을 반환한다.

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

### `annotate()`

`annotate()`의 각 인수는 QuerySet의 각 객체에 추가 될 주석이다. 각 주석은 단순한 값, 모델의 필드에 대한 참조, QuerySet의 각 객체와 관련된 집계(averages, sums 등)이다.

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

### `order_by()`

정렬 기준을 재정의한다.

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

### `reverse()`

역순으로 반환한다.

```python
# 마지막 5개 항목
my_queryset.reverse()[:5]
```

파이썬의 `seq[-5:]`와 같은 기능이지만, SQL에서는 효율적으로 할 수 없기 때문에(끝에서 슬라이싱하는) Django는 엑세스 모드를 지원하지 않는다.

`reverse()`는 QuerySet이 순서가 정의되어 있을 때만 효과가 있다(기본 순서를 정의하는 모델에 대해 쿼리할때, 또는 `order_by()`를 사용할때). 정의된 순서가 없는 경우 효과가 없다.

### `distinct()`

`SELECT DISTINCT`를 사용하는 QuerySet을 반환한다. 쿼리 결과에 중복행을 제거한다.

QuerySet은 기본적으로 중복 행을 제거하지 않지만, 쿼리가 여러 테이블에 걸쳐 있는 경우 중복된 결과를 얻을 수 있다. 그런 경우 `distinct()`를 사용한다.

> `order_by()`에서 사용된 필드는 SQL `SELECT`열에 포함되어 있기 때문에, `distinct()`과 함께 사용될 경우 예상치 못한 결과를 초래할 수 있다.  
관련 모델의 필드별로 정렬하면 해당 필드는 SELECT 열에 추가되지 않아서 중복 행이 구별된 것처럼 보일 수 있다. 추가 행은 반환된 결과에는 나타나지 않기 때문에, 뚜렷하지 않은 결과가 반환되는 것처럼 보인다.  
선택한 열을 제한하기 위해서 `values()`를 사용할 경우, `order_by()`안에 사용된 열이나 기본 모델 순서에서 사용되는 열이 여전히 연관되어 있어, 결과의 고유성에 영향을 미친다.  
`distinct()`을 사용하려면 **관련 모델에 의한 정렬** 에 주의해야 한다. `distinct()`와 `values()`를 한께 사용할 때는 `values()` 호출에 없는 필드도 주의해야 한다.

PostgreSQL을 사용할때는 DISTINCT를 적용할 필드를 지정하기 위해 위치 인수(`*fields`)를 전달할 수 있다.  
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

### `values()`

dict를 반환하는 QuerySet을 반환한다.

```python
>>> Blog.objects.filter(name__startswith='Beatles')
<QuerySet [<Blog: Beatles Blog>]>

>>> Blog.objects.filter(name__startswith='Beatles').values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
```

`values()`는 선택적 위치 인수를 사용하며, SELECT가 제한되어야 하는 필드 이름을 지정할 수 있다. 필드를 지정하면 지정한 필드에 대한 필드의 키/값만 들어간다. 필드를 지정하지 않으면 DB 테이블의 모든 필드에 대한 키/값이 들어간다.  

```python
>>> Blog.objects.values()
<QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>

>>> Blog.objects.values('id', 'name')
<QuerySet [{'id': 1, 'name': 'Beatles Blog'}]>
```

`values()` 인자로 표현식을 넣을 수 있으며, 아래 코드는 키를 주석으로 교체한다.  

```python
>>> from django.db.models.functions import Lower
>>> Blog.objects.values(lower_name=Lower('name'))
<QuerySet [{'lower_name': 'beatles blog'}]>
```

built_in과 custom lookup을 사용할 수 있다.

```python
>>> from django.db.models import CharField
>>> from django.db.models.functions import Lower
>>> CharField.register_lookup(Lower)
>>> Blog.objects.values('name__lower')
<QuerySet [{'name__lower': 'beatles blog'}]>
```

`values()`의 aggregate는 동일한 `values()`내의 다른 인수보다 먼저 적용된다. 다른 값으로 그룹화해야 하는 경우, `values()`의 인자에 추가해야 한다.

```python
>>> from django.db.models import Count
>>> Blog.objects.values('entry__authors', entries=Count('entry'))
<QuerySet [{'entry__authors': 1, 'entries': 20}, {'entry__authors': 1, 'entries': 13}]>

>>> Blog.objects.values('entry__authors').annotate(entries=Count('entry'))
<QuerySet [{'entry__authors': 1, 'entries': 33}]>
```

'Foo'라는 필드가 ForeignKey인 경우, 'foo_id'라는 사전 키를 반환하는데, 실제 모델 속성의 이름이다.  
`value()`를 호출하고 필드 이름을 입력할때 'foo'나 'foo_id'를 입력하면 동일한 항목을 반환한다.

```python
>>> Entry.objects.values()
<QuerySet [{'blog_id': 1, 'headline': 'First Entry', ...}, ...]>

>>> Entry.objects.values('blog')
<QuerySet [{'blog': 1}, ...]>

>>> Entry.objects.values('blog_id')
<QuerySet [{'blog_id': 1}, ...]>
```

- `values()`와 `distinct()`를 값이 사용하면 순서가 결과에 영향을 미친다.
- `extra()`를 호출한 후 `values()`를 사용하면, `extra()`의 선택 인수에 의해 정의된 필드를 `values()` 호출에 명시적으로 포함해야 한다.
- `values()` 호출 후에 `extra()`를 사용하면 선택도니 추가 필드는 무시된다.
- `values()` 뒤에 `only()`, `defer()`를 호툴하는 것은 무의미하므로 **NotImplementedError를 발생시칸다.
- 변환과 집계를 겹합하려면 두 개의 `annotate()` 호출을 하거나, `values()`에 키워드 인수로 사용해야 한다. 변환이 관련 필드에 등록된 경우 첫 번째 `annotate()`는 생략할 수 있다.

```python
>>> from django.db.models import CharField, Count
>>> from django.db.models.functions import Lower
>>> CharField.register_lookup(Lower)
>>> Blog.objects.values('entry__authors__name__lower').annotate(entries=Count('entry'))
<QuerySet [{'entry__authors__name__lower': 'test author', 'entries': 33}]>
>>> Blog.objects.values(
...     entry__authors__name__lower=Lower('entry__authors__name')
... ).annotate(entries=Count('entry'))
<QuerySet [{'entry__authors__name__lower': 'test author', 'entries': 33}]>
>>> Blog.objects.annotate(
...     entry__authors__name__lower=Lower('entry__authors__name')
... ).values('entry__authors__name__lower').annotate(entries=Count('entry'))
<QuerySet [{'entry__authors__name__lower': 'test author', 'entries': 33}]>
```

`values()` 호출 후에 `filter()`, `order_by()` 등을 호출할 수 있다.

```python
# 둘은 동일하다.
Blog.objects.values().order_by('id')
Blog.objects.order_by('id').values()
```

**OneToOneField**, **ForeignKey**, **ManyToManyField** 속성을 통해 역관계가 있는 관련 모델을 참조할 수도 있다.

```python
>>> Blog.objects.values('name', 'entry__headline')
<QuerySet [{'name': 'My blog', 'entry__headline': 'An entry'},
     {'name': 'My blog', 'entry__headline': 'Another entry'}, ...]>
```

MTM 등 역관계가 있는 하나의 필드에 여러 데이터가 포함될 수 있기 때문에 `values()`를 사용하면 너무 큰 결과를 반환할 수도 있다.

### `values_list()`

Tuple를 반환하는 QuerySet을 반환한다. 그외에는 `values()`와 동일하다.

```python
>>> Entry.objects.values_list('id', 'headline')
<QuerySet [(1, 'First entry'), ...]>
>>> from django.db.models.functions import Lower
>>> Entry.objects.values_list('id', Lower('headline'))
<QuerySet [(1, 'first entry'), ...]>
```

단일 필드만 지정하는 경우, `flat` 매개 변수로 전달 할 수도 있다. True리면 반환된 결과가 튜플이 아닌 단일 값임을 의미한다.

```python
>>> Entry.objects.values_list('id').order_by('id')
<QuerySet[(1,), (2,), (3,), ...]>

>>> Entry.objects.values_list('id', flat=True).order_by('id')
<QuerySet [1, 2, 3, ...]>
```

`named=True`를 전달하면, `namedtuple()` 결과를 얻을 수 있다.

```python
>>> Entry.objects.values_list('id', 'headline', named=True)
<QuerySet [Row(id=1, headline='First entry'), ...]>
```

`values_list()`에 인자를 넣지 않으면 선언 된 순서대로 모델의 모든 필드가 반환된다.  

특정 필드의 값을 얻으려면 `get()`을 호출해야 한다.

```python
>>> Entry.objects.values_list('headline', flat=True).get(pk=1)
'First entry'
```

더블언더바로 MTM도 참조할 수 있다. 필드에 값이 없는 경우 None을 반환한다.

```python
>>> Author.objects.values_list('name', 'entry__headline')
<QuerySet [('Noam Chomsky', 'Impressions of Gaza'),
 ('George Orwell', 'Why Socialists Do Not Believe in Fun'),
 ('George Orwell', 'In Defence of English Cooking'),
 ('Don Quixote', None)]>
```

### `dates()`

날짜를 나타내는 필드를 `datetime.date` 객체 리스트로 평가되는 QuerySet을 반환한다. 각 필드는 `datetime.date` 객체 유형이어야 한다.

```
dates(field, kind, order='ASC')
```

- field: 모델의 DateField 필드 이름을 지정한다.
- kind: 'year', 'month', 'week', 'day' 중 하나를 선택한다.
- order: 기본값은 'ASC'이다.

```python
>>> Entry.objects.dates('pub_date', 'year')
[datetime.date(2005, 1, 1)]
>>> Entry.objects.dates('pub_date', 'month')
[datetime.date(2005, 2, 1), datetime.date(2005, 3, 1)]
>>> Entry.objects.dates('pub_date', 'week')
[datetime.date(2005, 2, 14), datetime.date(2005, 3, 14)]
>>> Entry.objects.dates('pub_date', 'day')
[datetime.date(2005, 2, 20), datetime.date(2005, 3, 20)]
>>> Entry.objects.dates('pub_date', 'day', order='DESC')
[datetime.date(2005, 3, 20), datetime.date(2005, 2, 20)]
>>> Entry.objects.filter(headline__contains='Lennon').dates('pub_date', 'day')
[datetime.date(2005, 3, 20)]
```

### `datetimes()`

날짜를 나타내는 필드를 `datetime.datetime` 객체 리스트로 평가되는 QuerySet을 반환한다.

```python
datetimes(field_name, kind, order='ASC', tzinfo=None)
```

- field_name: 모델의 DateTimeField의 이름을 지정해야 한다.
- kind: 'year', 'month', 'week', 'day', 'hour', 'minute', 'second' 중에 선택하여 지정한다.
- order: `dates()`와 동일하다.
- tzinfo: 시간대를 정의한다. 매개변수는 datetime.tzinfo 객체이어야 한다. 그렇지 않으면 Django의 시간대를 사용하고, `USE_TZ`가 False이면 효과가 없다.

### `none()`

객체를 반환하지 않는 QuerySet을 반환하고, 엑서스할 때 쿼리가 실행되지 않는다.  
`qs.none()`은 EmptyQuerySet의 인스턴스이다.

```python
>>> Entry.objects.none()
<QuerySet []>
>>> from django.db.models.query import EmptyQuerySet
>>> isinstance(Entry.objects.none(), EmptyQuerySet)
True
```

### `all()`

현재 QuerySet의 사본을 리턴한다. QuerySet이 평가된 후 평가 이전에 평가한 QuerySet에 `all()`을 호출하면 업데이트된 결과를 얻게 된다.

### `union()`

SQL의 UNION 연산자를 사용하여 둘 이상의 QuerySet 결과를 결합한다.

```python
>>> qs1.union(qs2, qs3)
```

UNION 연산자는 기본적으로 고유한 값만 선택하지만, 중복값을 혀용하려면 `all=True` 인수를 사용하면 된다.

`union()`, `intersection()`, `difference()`는 인자가 다른 모델의 QuerySet인 경우 첫 번째 QuerySet 타입의 모델 인스턴스를 반환한다. SELECT 리스트가 모든 QuerySet과 동일하기만 하면 다른 모델을 전달 할 수도 있다. 이런 경우 QuerySeet에 적용된 QuerySet 메소드의 첫 번째 QuerySet에서 컬럼 이름을 사용해야 한다.

```python
>>> qs1 = Author.objects.values_list('name')
>>> qs2 = Entry.objects.values_list('headline')
>>> qs1.union(qs2).order_by('name')
```

또한 LIMIT, OFFSET, COUNT(* ), ORDER_BY, 지정한 열(slicing, `count()`, `order_by()`, `values()/values_list()`만 결과 QuerySet에 지정할 수 있다.  

DB는 결합된 쿼리에서 허용되는 작업을 제한한다. 예를 들면 대부분의 DB는 결합된 쿼리에서 LIMIT나 OFFSET을 허용하지 않는다.

### `intersection()`

SQL의 INTERSECT 연산자를 사용하여 둘 이상의 QuerySet의 공유 요소를 리턴한다.

```python
>>> qs1.intersection(qs2, qs3)
```

### `difference()`

SQL의 EXCEPT 연산자를 사용하여 QuerySet(qs1)에는 있고 qs2, qs3에는 없는 요소만 유지한다.

```python
>>> qs1.difference(qs2, qs3)
```

### `select_related()`

쿼리를 실행할때 추가적인 관련 객체 데이터를 선택하여 외래키 관계를 팔로우할 QuerySet을 반환한다. 이건 더 복잡한 쿼리를 가져오도록 부추기지만 외래키 관계를 사용할 경우 DB 쿼리가 필요하지 않음을 의미한다.

```python
# 일반적인 조회와 select_related() 조회의 차이점

#일반적인 조회
# 아래 2줄은 각각 DB에 접근한다.
e = Entry.objects.get(id=5)
b = e.blog

# select_related를 사용한 조회
# select_related으로 blog 필드에 접근하여 캐싱되기 때문에 e.blog는 DB를 거치지 않아도 된다.
e = Entry.objects.select_related('blog').get(id=5)
b = e.blog

# 객체의 QuerySet과 select_related() 함께 사용
from django.utils import timezone

# 공개 예정인 항목이 있는 모든 블로그 찾기
blogs = set()

for e in Entry.objects.filter(pub_date__gt=timezone.now()).select_related('blog'):
    # select_related()가 없으면 각각에 대한 데이터베이스 쿼리를 만 항목에 대한 관련 블로그를 가져오기 위해 각 루프 반복에 대한 DB 쿼리가 된다.
    blogs.add(e.blog)
```

`filter()`나 `select_related()`의 연결 순서는 상관없다.

```python
Entry.objects.filter(pub_date__gt=timezone.now()).select_related('blog')
Entry.objects.select_related('blog').filter(pub_date__gt=timezone.now())
```

외래키를 쿼리하는 것과 비슷한 방식으로 외래키를 따를 수 있다.

```python
# models
from django.db import models

class City(models.Model):
    # ...
    pass

class Person(models.Model):
    # ...
    hometown = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

class Book(models.Model):
    # ...
    author = models.ForeignKey(Person, on_delete=models.CASCADE)
```

`Book.objects.select_related('author__hometown').get(id=4)`를 호출하면 관련 Person과 관련 City가 캐시된다.

```python
# author와 hometown 테이블에 조인하여 DB를 히트한다.
b = Book.objects.select_related('author__hometown').get(id=4)
p = b.author         # Doesn't hit the database.
c = p.hometown       # Doesn't hit the database.

# Without select_related()...
b = Book.objects.get(id=4)  # Hits the database.
p = b.author         # Hits the database.
c = p.hometown       # Hits the database.
```

`select_related()`에 ForeignKey나 OneToOneField 관계를 참조할 수 있다.  
또한 select_related을 전달된 필드 리스트에서 OneToOneField의 역방향도 참조할 수 있다. 즉 OneToOneField를 필드가 정의된 객체로 다시 이동할 수 있다.  

필드 이름을 지정하는 대신 관련 객체의 필드에 related_name을 사용하면 된다.  

관련 객체가 많은 `select_content()`를 호출하고 싶거나, 모든 관계를 모르는 상황이 있을 수 있다. 이런 경우 `select_content()`를 인수 없이 호출한다. 이러면 null 아닌 모든 외래키를 따르게 된다. 대부분의 이런 경우는 기본 쿼리를 더 복잡하게 만들고 필요한 데이터보다 많은 데이터를 반환하기 때문에 권장되지 않는다.  

QuerySet에서 select_related의 이전 호출에 의해 추가된 관련 필드 리스트를 지워야 하는 경우 매개 변수로 None을 전달한다.

```python
>>> without_relations = queryset.select_related(None)
```

```python
# select_related를 체이닝하여 콜하는 경우
# 둘은 같다.
select_related('foo', 'bar') == select_related('foo').select_related('bar')
```

### `prefetch_related()`

지정된 각 조회에 대해 단일 배치에서 관견 객체를 자동으로 검새하는 QuerySet을 반환한다. 이건 `select_related`와 비슷하다. 둘 다 관련 객체에 액세스하여 발생하는 DB 쿼리의 유출을 막기 위해 설계되었지만, 전략은 완전 다르다.

`select_related`는 SQL join을 생성하고 SELECT 문에 관련 객체의 필드를 포함시켜 작동한다. 그렇기 때문에 `select_related`는 동일한 DB 쿼리에서 관련 객체를 가져온다. 그러나 많은 관계가 조인하여 발생하는 큰 결과셋을 피하기 위해 `select_related`는 외래키와 one-to-one 관계로 제한한다.  

`prefetch_related`는 각 관계에 대해 별도로 조회하고 파이썬에서 joining을 수행한다. 이를 통해 `select_related`에서는 할 수 없는 many-to-many, many-to-one 객체도 사용이 가능하다. 또한 `GenericRelation`, `GenericForeignKey`도 지원하지만, 동일한 결과 집합으로 제한된다.

```python
# 예를 위한 모델
from django.db import models

class Topping(models.Model):
    name = models.CharField(max_length=30)

class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return "%s (%s)" % (
            self.name,
            ", ".join(topping.name for topping in self.toppings.all()),
        )
```

```python
# run
>>> Pizza.objects.all()
["Hawaiian (ham, pineapple)", "Seafood (prawns, smoked salmon)"...
```

위 코드의 문제는 `Pizza.__str__()`이 `self.toppings.all()`을 요청할때마다 DB를 쿼리해야하기 떄문에 `Pizza.objects.all()`은 Toppings 테이블에서 쿼리를 실행한다.

```python
# prefetch_related를 사용하면 두 개의 쿼리로 줄일 수 있다.
>>> Pizza.objects.all().prefetch_related('toppings')
```

이건 각 Pizza마다 `self.toppings.all()`을 의미한다. 이 `self.toppings.all()`은 호출할 때마다 DB로 이동하지 않고 단일 조회로 채워진 미리 설정된 QuerySet 캐시에서 해당 항목을 찾는다.  

즉, 모든 관련 toppings은 단일 쿼리로 가져와 관련 결과들로 미리 채워진 캐시가 있는 QuerySet을 만드는데 사용되고, 이 QuerySet은 `self.toppings.all()` 호출에 사용된다.

`prefetch_related()`의 추가 쿼리는 QuerySet의 평가가 시작되고 기본 쿼리가 실행된 후에 실행된다.  

반복 가능한 모델 인스턴스의 경우 `prefetch_related_objects()`를 사용하여 해당 인스턴스에서 관련 속성을 미리 준비할 수 있다.  

그 후에 기본 QuerySet의 결과 캐시와 지정된 모든 관련 객체를 메모리에 완전히 불러온다. 일반적으로는 DB에서 쿼리가 실행 된 후에도 필요한 모든 객체를 메모리에 로드하지 않는다.

> QuerySet에서 다른 DB 쿼리를 암시하는 후속 체인 메소드는 이전의 캐시된 결과를 무시하고 새로운 DB 쿼리를 사용하여 데이터를 검색한다.

```python
>>> pizzas = Pizza.objects.prefetch_related('toppings')
>>> [list(pizza.toppings.filter(spicy=True)) for pizza in pizzas]
```

위 코드는 `pizza.toppings.all()`가 프리패치 되었지만 아무런 도움이 되지 않는다. `prefetch_related('toppings')`는 `pizza.toppings.all()`을 암시하지만 `pizza.toppings.filter()`와는 다른 쿼리다. 그래서 위 코드에서는 사용하지 않는 DB 쿼리를 수행하기 때문에 프리패치가 도움이 되지 않을 뿐더러, 성능까지 저하된다.

또한, 관련 관리자에서 DB 변경 메소드(`add()`, `remove()`, `clear()`, `set()`을 호출하면 프리패치된 캐시가 지워진다.

일반 조인 구문을 사용하여 관련 필드의 관련 필드를 수행할 수도 있다.

```python
# 위 모델 코드에 추가 모델
class Restaurant(models.Model):
    pizzas = models.ManyToManyField(Pizza, related_name='restaurants')
    best_pizza = models.ForeignKey(Pizza, related_name='championed_by', on_delete=models.CASCADE)
```

```python
>>> Restaurant.objects.prefetch_related('pizzas__toppings')
```

Restaurant에 속한 모든 Pizza와 해당 Pizza에 속하는 모든 Topping이 프리패치되는데, 이는 총 3개의 DB 쿼리가 발생한다.(Restaurant, Pizza, Topping)

```python
>>> Restaurant.objects.prefetch_related('best_pizza__toppings')
```

이건 각 Restaurant마다 최고의 Pizze와 최고의 Pizza를 위한 모든 Topping을 가져온다. 이 역시 3개의 DB 쿼리가 발생한다.

물론, `select_related`를 사용하여 쿼리를 둘로 줄일 수도 있다.

```python
>>> Restaurant.objects.select_related('best_pizza').prefetch_related('best_pizza__toppings')
```

프리패치는 기본쿼리 후에 실행되므로 `best_pizza` 객체가 이미 패치되었음을 감지하고 다시 패치하지 않는다.  

`prefetch_related` 호출을 연결하면 프리패치된 조회가 누적된다. 이 동작을 지우려면 None을 매개변수로 전달해야 한다.

```python
>>> non_prefetched = qs.prefetch_related(None)
```

`prefetch_related`를 사용시 유의할 점은 쿼리로 생성된 객체가 의도와 상관없이 관계가 있는 다른 객체간에 공유 될 수 있다는 것이다. 이건 일반적으로 외래키 관계에서 발생하는데, 이 동작이 문제가 되지 않는다면 메모리와 CPU 시간을 모두 절약한다.  

`GenericForeignKey`는 여러 테이블의 데이터를 참조할 수 있기 때문에 모든 항목에 대해 하나의 쿼리가 아니라 참조된 테이블 당 하나의 쿼리가 필요하다. 관계된 행을 가져오지 못한 경우 ContentType 테이블에 추가 쿼리가 있을 수 있다.  

대부분 `prefetch_related`는 SQL IN 연산자를 사용한다. 이건 큰 QuerySet의 경우 DB에 따라 쿼리 구분 분석이나 실행시 큰 IN 이 생성되어 성능 이슈가 발생할 수 있음을 의미한다.  

`iterator()`를 사용하면 `prefetch_related()`는 무시된다.  

`Prefetch`를 사용하면 프리패치 객체를 추가로 제어할 수 있다.

```python
>>> from django.db.models import Prefetch
# 가장 단순한 Prefetch 사용으로, 기본 문자열 검색과 동일하다.
>>> Restaurant.objects.prefetch_related(Prefetch('pizzas__toppings'))

# 선택적 queryset 인자를 사용하여 cunstom queryset를 만들 수 있다.
# 이걸로 queryset의 기본 순서를 변경 할 수 있다.
>>> Restaurant.objects.prefetch_related(
...     Prefetch('pizzas__toppings', queryset=Toppings.objects.order_by('name')))

# select_related()를 호출하여 쿼리를 더 줄일 수 있다.
>>> Pizza.objects.prefetch_related(
...     Prefetch('restaurants', queryset=Restaurant.objects.select_related('best_pizza')))

# to_attr 인자를 사용하여 프리패치된 결과를 사용자 정의 속성에 지정할 수 있다.
# 결과는 리스트에 저장된다.

# 이를 통해 다른 QuerySet으로 동일한 관계를 여러번 프리패치 할 수 있다.
>>> vegetarian_pizzas = Pizza.objects.filter(vegetarian=True)
>>> Restaurant.objects.prefetch_related(
...     Prefetch('pizzas', to_attr='menu'),
...     Prefetch('pizzas', queryset=vegetarian_pizzas, to_attr='vegetarian_menu'))

# 사용자 정의된 to_attr으로 작성된 조회는 다른 조회에서 같이 계속 순회가 가능하다.
>>> vegetarian_pizzas = Pizza.objects.filter(vegetarian=True)
>>> Restaurant.objects.prefetch_related(
...     Prefetch('pizzas', queryset=vegetarian_pizzas, to_attr='vegetarian_menu'),
...     'vegetarian_menu__toppings')

# 프리 패치 결과를 필터링 할때는 to_attr을 사용하는 것이 좋다.
>>>
>>> # Recommended:
>>> restaurants = Restaurant.objects.prefetch_related(
...     Prefetch('pizzas', queryset=queryset, to_attr='vegetarian_pizzas'))
>>> vegetarian_pizzas = restaurants[0].vegetarian_pizzas
>>>
>>> # Not recommended:
>>> restaurants = Restaurant.objects.prefetch_related(
...     Prefetch('pizzas', queryset=queryset))
>>> vegetarian_pizzas = restaurants[0].pizzas.all()
```

사용자 지정 프리패치는 ForeignKey나 OneToOneField와 같은 단일 관계에서도 동작한다. 이런 관계는 일반적으로 `select_related()`를 사용하지만, 사용자 정의 QuerySet을 사용하여 프리패치 하는 것이 더 유용한 경우도 많다.

 - 관련 모델에서 추가 프리패치를 수행하는 QuerySet을 사용하려는 경우
 - 관련 객체의 일부만 프리패치하려는 경우
 - `deferred fields`처럼 성능 최적화된 기술을 사용하려는 경우

```python
>>> queryset = Pizza.objects.only('name')
>>>
>>> restaurants = Restaurant.objects.prefetch_related(
...     Prefetch('best_pizza', queryset=queryset))
```

### `extra()`

Django는 복잡한 WHERE 구문을 위해 `extra()`을 제공한다.(QuerySet에 의해 생성된 SQL에 특정 절을 삽입하기 위한 훅)  

`extra()`는 더이상 업데이트 되지 안는다. 다른 쿼리셋 메소드를 사용해서 쿼리를 표현할 수 없는 경우에만 사용해야 한다.

 - `select`
 여분의 필드를 삽입할 수 있다. SELECT 절에 dict를 맵핑해야 한다.

```python
# Entry에 추가속석 is_recent 이 있음
# 이 속성은 pub_date가 2006년 1월 1일보다 큰지 여부를 나타냄
Entry.objects.extra(select={'is_recent': "pub_date > '2006-01-01'"})

# SQL
SELECT blog_entry.*, (pub_date > '2006-01-01') AS is_recent
FROM blog_entry;

# Blog 객체에 entry_count속석 관련 Entry 객체의 정수 갯수를 호출
Blog.objects.extra(
    select={
        'entry_count': 'SELECT COUNT(*) FROM blog_entry WHERE blog_entry.blog_id = blog_blog.id'
    },
)

# SQL
SELECT blog_blog.*, (SELECT COUNT(*) FROM blog_entry WHERE blog_entry.blog_id = blog_blog.id) AS entry_count
FROM blog_blog;
```

 - `where / tables`
 `where`을 사용하여 명시적으로 SQL WHERE절을 정의한다.  
 `tables`를 사용하여 SQL FROM절에 테이블을 수동으로 추가할 수 있다.

 ```python
 # where의 각 요소는 AND로 해석된다.
 Entry.objects.extra(where=["foo='a' OR bar = 'a'", "baz = 'a'"])

# SQL
SELECT * FROM blog_entry WHERE (foo='a' OR bar='a') AND (baz='a')
```

 - `order_by`

`extra()`으로 생성된 새로운 필드나 테이블을 정렬할 수 있다.
 ```python
q = Entry.objects.extra(select={'is_recent': "pub_date > '2006-01-01'"})
q = q.extra(order_by = ['-is_recent'])
```
 - `params`
 where의 매개 변수를 '%s'으로 표현하는데, 매개 변수를 params에 넣어야 한다.

 ```python
 Entry.objects.extra(where=['headline=%s'], params=['Lennon'])
 ```

### `defer()`

QuerySet으로 DB에 접근할때 지연시킬 필드명을 지정한다.

```python
Entry.objects.defer("headline", "body")

# 여러번 호출할 수도 있다.
Entry.objects.defer("body").filter(rating=5).defer("headline")

# 관련 모델의 필드는 이중 언더바로 지정하여 적용할 수 있다.
Blog.objects.select_related().defer("entry__headline", "entry__body")

# defer()를 초기화하려면 None을 인자로 전달하면 된다.
my_queryset.defer(None)
```

기본 키와 같은 모델의 일부 필드는 지연시킬 수 없다.

### `only()`

`defer()`와 정반대로 동작한다. 지연되어서는 안되는 필드를 지정한다.  
거의 모든 필드를 연기해야하는 경우 `only()`을 사용하면 코드는 더 간단해진다.

```python
# Person은 name, age, biography 3개의 필드를 가지고 있다고 가정한다.
# 두 코드는 동일한 동작을 한다.
Person.objects.defer("age", "biography")
Person.objects.only("name")
```

`only()`을 중첩할 경우 마지막만 적용된다.

```python
# This will defer all fields except the headline.
Entry.objects.only("body", "rating").only("headline")
```

그렇기 때문에 `defer()`와 `only()`를 결합하여 사용할 수 있다.

```python
# headline를 제외한 모든 것이 지연된다.
Entry.objects.only("headline", "body").defer("body")


# headline, body를 호출한다.
Entry.objects.defer("body").only("headline", "body")
```

### `using()`

둘 이상의 DB를 사용하는 경우 QuerySet이 평가할 DB를 지저한다.

```python
# queries the database with the 'default' alias.
>>> Entry.objects.all()

# queries the database with the 'backup' alias
>>> Entry.objects.using('backup')
```

### `select_for_update()`

트랜잭션이 끝날때까지 행을 잠그는 'SELECT ... FOR UPDATE' SQL문을 생성하는 QuerySet을 반환한다.

```python
from django.db import transaction

entries = Entry.objects.select_for_update().filter(author=request.user)
with transaction.atomic():
    for entry in entries:
        ...
```

일반적으로 다른 트랜잭션이 선택된 행 중 하나에 잠금을 획득한 경우, 잠금이 해제 될때까지 쿼리가 차단되는데, 차단하지 않으려면 `select_for_update(nowait=True)`를 하면 된다.  
`select_for_update(skip_locked=True)`를 하면 잠긴 행을 무시할 수 있다.

부모 모델을 잠그려면 `of`에 상위 링크 필드(<parent_model_name>_ptr)를 지정해야한다.
```python
Restaurant.objects.select_for_update(of=('self', 'place_ptr'))
```

해당 필드가 null인 경우 사용이 불가하고 `NotSupportedError`가 발생한다. 이러한 제한을 피하기 위해 제외할 수 있다.

```python
>>> Person.objects.select_related('hometown').select_for_update().exclude(hometown=None)
<QuerySet [<Person: ...)>, ...]>
```

postgresql, oracle, mysql에서 `select_for_update()`를 지원하지만, MySql은 of 인수를 지원하지 않고, nowait, skip_locked는 MySQL 8.0.1 이상에서만 지원한다.  

### `raw()`

원시 SQL 쿼리를 실행하고, `django.db.models.query.RawQuerySet` 인스턴스를 반환한다.

# 새 QuerySet을 반환하는 연산자들

### `AND(&)`

SQL AND 연산자를 사용하여 결합한다.

```python
# 모두 동일하다.
Model.objects.filter(x=1) & Model.objects.filter(y=2)
Model.objects.filter(x=1, y=2)
from django.db.models import Q
Model.objects.filter(Q(x=1) & Q(y=2))

# SQL
SELECT ... WHERE x=1 AND y=2
```

### `OR(|)`

SQL OR 연산자를 사용하여 결합한다.

```python
# 모두 동일하다.
Model.objects.filter(x=1) | Model.objects.filter(y=2)
from django.db.models import Q
Model.objects.filter(Q(x=1) | Q(y=2))

# SQL
SELECT ... WHERE x=1 OR y=2
```

# QuerySet을 반환하지 않는 함수들

이 메소드들은 캐시를 사용하지 않고, 호출 될 떄마다 DB를 쿼리한다.

### `get()`

단일 객체를 반환한다.  

QuerySet이 하나의 행을 반환 될 것으로 예상되면 인수 없이 사용하면 된다.

```python
entry = Entry.objects.filter(...).exclude(...).get()
```

### `create()`

객체의 생성 및 저장을 한번에 진행한다.

```python
# 1,2는 동일하다.
## 1
p = Person.objects.create(first_name="Bruce", last_name="Springsteen")

## 2
p = Person(first_name="Bruce", last_name="Springsteen")
p.save(force_insert=True)
```

### `get_or_create()`

단일 객체(`(object, created)`)를 반환하고, 없으면 생성한다.

`get_or_create()`에 `filter()`를 사용할 수 있다.

```python
from django.db.models import Q

obj, created = Person.objects.filter(
    Q(first_name='Bob') | Q(first_name='Robert'),
).get_or_create(last_name='Marley', defaults={'first_name': 'Bob'})
```

`get_or_create()`에서 여러 객체가 발견되면 `MultipleObjectsReturned`를 발생시킨다.

### `update_or_create()`

단일 객체를 업데이트하고, 없다면 생성한다.  

튜플을 반환한다. `(object, created)`

### `bulk_create()`

객체 리스트를 DB에 삽입한다. (한번에 여러 객체를 저장)

```python
>>> Entry.objects.bulk_create([
...     Entry(headline='This is a test'),
...     Entry(headline='This is only a test'),
... ])
```

몇가지 주의 사항이 있다.

- `save()`가 호출되지 않기 때문에 `pre_save`, `post_save` 시그널이 발생하지 않는다.
- 다중 테이블 상속 시나리오에서는 하위 모델과 작동하지 않는다.
- 모델의 기본 키가 AuthField인 경우 DB 백엔드가 지원하지 않는 다면(PostgreSQL) 기본 키 속성을 검색하여 설정하지 않는다.
- many-to-many 관계는 지원하지 않는다.

### `bulk_update()`

하나의 쿼리로 모델 인스턴스에서 제공된 필드를 효율적으로 업데이트한다.

```python
>>> objs = [
...    Entry.objects.create(headline='Entry 1'),
...    Entry.objects.create(headline='Entry 2'),
... ]
>>> objs[0].headline = 'This is entry 1'
>>> objs[1].headline = 'This is entry 2'
>>> Entry.objects.bulk_update(objs, ['headline'])
```

`QuerySet.update()`와 `save()`을 사용하여 모델 리스트를 반복 업데이트하는 것보다 효율적이지만 몇가지 주의 사항이 있다.

- 모델의 기본 키를 업데이트 할 수 없다.
- 각 모델의 `save()`가 호출되지 않아서 `pre_save`, `post_save` 시그널이 발생하지 않는다.
- 많은 수의 행을 업데이트하는 경우 SQL이 매우 클 수 있다. `batch_size`를 사용하여 이런 경우를 피할 수 있다.(`batch_size`는 단일 쿼리에 저장되는 개체 수를 제어한다.)
- 다중 테이블 상속시 조상에 정의된 필드를 업데이트하면, 각 조상마다 추가 쿼리가 발생한다.
- objs에 중복이 포함된 경우 첫 항목만 업데이트 된다.

### `count()`

QuerySet과 일치하는 DB 객체의 수를 나타내는 정수를 반환한다.

```python
# Returns the total number of entries in the database.
Entry.objects.count()

# Returns the number of entries whose headline contains 'Lennon'
Entry.objects.filter(headline__contains='Lennon').count()
```

`count()`는 `SELECT COUNT(*)`를 수행하므로, 모든 레코드를 파이썬 객체에 로드하고 `len()`를 호출하는 것보다는 `count()`를 사용해야한다.(객체를 메모리에 로드하지 않을때는 `len()`이 더 빠르다.)

### `in_bulk()`

`in_bulk(id_list=None, field_name='pk')`

`{id, object}`형식으로 반환한다. `id_list`를 지정하지 않으면 QuerySet의 모든 객체를 반환한다. `field_name`은 고유 필드이어야 하고, 기본키로 설정해야 한다.

```python
>>> Blog.objects.in_bulk([1])
{1: <Blog: Beatles Blog>}
>>> Blog.objects.in_bulk([1, 2])
{1: <Blog: Beatles Blog>, 2: <Blog: Cheddar Talk>}
>>> Blog.objects.in_bulk([])
{}
>>> Blog.objects.in_bulk()
{1: <Blog: Beatles Blog>, 2: <Blog: Cheddar Talk>, 3: <Blog: Django Weblog>}
>>> Blog.objects.in_bulk(['beatles_blog'], field_name='slug')
{'beatles_blog': <Blog: Beatles Blog>}
```

### `iterator()`

QuerySet을 평가하고 결과를 iterator에 반환한다.  

QuerySet은 보통 반복적인 평가가 추가 쿼리를 생성하지 않도록 결과를 내부적으로 캐시한다. 하지만 `iterator()`는 QuerySet 수준에서 캐싱하지 않고 결과를 직접 읽는다.  

많은 수의 객체를 반환하는 QuerySet의 경우 쿼리 성능이 향상되고 메모리는 크게 감소한다.  

이미 평가한 QuerySet에 `iterator()`을 사용하면 쿼리를 반복하여 재평가하는 점은 주의해야 한다.  

`iterator()`를 사용하면 이전의 `prefetch_related()`는 무시된다.  

- server-side cursors를 사용하는 경우

Oracle과 PostgreSQL는 server-side sursors를 사용하여 전체 결과 셋을 메모리에 로드하지 않고 DB에서 결과를 스트리밍한다.  

server-side cursors의 경우, `chunk_size` 매개변수는 DB 드라이버 수준에서 캐시할 결과의 수를 지정한다. 더 많은 결과를 가져오면 메모리 소비량이 증가하지만, DB 드라이버와 DB 간의 전송 횟수가 줄어든다.  

PostgreSQL의 경우, `DISABLE_SERVER_SIDE_CURSORS`가 False로 설정되어있어야 server-side cursors를 사용할 수 있다.  

- server-side cursors가 없는 경우

MySQL은 스트리밍 결과를 지원하지 않기 때문에, Python DB 드라이버는 전체 결과셋을 메모리에 로드한다. 그후 `fetchmany()` 메소드를 사용하여 파이썬 row 객체로 변환된다.  

`chunk_size` 매개 변수는 DB 드라이버에서 Django가 검색하는 배치의 크기를 제어한다. 배치가 클수록 메모리 소비량이 약간 증가하지만, DB 드라이버와 통신하는 오버헤드가 감소한다.  

텍스트와 숫자 데이터가 혼홥된 10~20 열의 행들의 데이터의 경우, 2000은 100KB 미만의 데이터를 가져올 것이며, 루프가 일찍 종료될 경우 전송되는 행의 수와 폐기되는 데이터 사이의 좋은 절충안이 될 것이다.

### `latest()`

주어진 필드를 기준으로 최신 객체를 반환한다.  

```python
# pub_date 필드를 기준으로 최신 항목을 반환한다.
Entry.objects.latest('pub_date')

# 여러 필드를 기반으로 선택할 수도 있다.
# 두 항목의 pub_date가 동일한 경우 expire_date가 빠른 항목을 선택
Entry.objects.latest('pub_date', '-expire_date')
```

모델의 Meta가 `get_latest_by`를 지정하는 경우, `get_latest_by`에 지정된 필드가 기본값이 되어, `earliest()`,`latest()`의 인수를 생략할 수 있다.

`earliest()`, `latest()`는 오직 편의와 가독성을 위해서 존재한다.

`earliest()`와 `latest()`는 null date의 인스턴스를 반환 할 수 있다.  
순서는 DB에 위임되기 때문에, 서로 다른 DB를 사용할 경우 null 값을 허용하는 필드의 결과는 다르게 정렬될 수 있다. 예를 들어 PostgreSQL와 MySQL은 null 값이 null이 아닌 값보다 높은 것으로 정렬하고, SQLite는 반대로 처리한다.  

```python
# null 값을 필터링 할 수 있다.
Entry.objects.filter(pub_date__isnull=False).latest('pub_date')
```

### `earliest()`

방향이 변경된 경우를 제외하고 `latest()`와 다르게 작동한다.
(다르게 작동한다는게 무슨 의미인지 이해가 안된다.)

### `first()`

### `last()`

### `aggregate()`

### `exists()`

### `udpate()`

### `delete()`

### `as_manager()`

### `explain()`

# 필드 검색

### `exact`

### `iexact`

### `contains`

### `icontains`

### `in`

### `gt`

### `gte`

### `lt`

### `lte`

### `startswith`

### `istartswith`

### `endswith`

### `iendswith`

### `range`

### `date`

### `year`

### `iso_year`

### `month`

### `day`

### `week`

### `week_day`

### `quarter`

### `time`

### `hour`

### `minute`

### `second`

### `isnull`

### `regex`

### `iregex`

# 집계 기능

### `expressions`

### `output_field`

### `filter`

### `**extra`

### `Avg`

### `Count`

### `Max`

### `Min`

### `StdDev`

### `Sum`

### `Variance`

# Query-related tools

### `Q()` objects

### `Prefetch()` objects

### `prefetch_related_objects()`

### `FilteredRelation()` objects
