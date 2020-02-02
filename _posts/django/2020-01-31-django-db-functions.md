---
layout: post
section-type: post
title: django - Database Functions
category: django
tags: [ 'django' ]
---

> [Django Database Functions](https://docs.djangoproject.com/en/2.2/ref/models/database-functions/)  

> [SQL Server Functions](https://www.w3schools.com/sql/sql_ref_sqlserver.asp)

---


```python
# 사용될 모델
class Author(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    alias = models.CharField(max_length=50, null=True, blank=True)
    goes_by = models.CharField(max_length=50, null=True, blank=True)
```

## 비교, 변환

### Cast

```python
class Cast(expression, output_field)
```

`output_field`으로 타입을 지정한다.

```python
>>> from django.db.models import FloatField
>>> from django.db.models.functions import Cast
>>> Author.objects.create(age=25, name='Margaret Smith')
>>> author = Author.objects.annotate(
...    age_as_float=Cast('age', output_field=FloatField()),
... ).get()
>>> print(author.age_as_float)
25.0
```

### Coalesce

```python
class Coalesce(*expression, **extra)
```

둘 이상의 필드나 표현식을 지정하면, null이 아닌 첫 번째 값을 리턴한다.(빈 문자열은 null이 아니다.)  
텍스트와 숫자를 혼합하면 데이터베이스 오류가 발생한다.  

```python
>>> from django.db.models import Sum, Value as V
>>> from django.db.models.functions import Coalesce
>>> Author.objects.create(name='Margaret Smith', goes_by='Maggie')
>>> author = Author.objects.annotate(
...    screen_name=Coalesce('alias', 'goes_by', 'name')).get()
>>> print(author.screen_name)
Maggie

>>> aggregated = Author.objects.aggregate(
...    combined_age=Coalesce(Sum('age'), V(0)),
...    combined_age_default=Sum('age'))
>>> print(aggregated['combined_age'])
0
>>> print(aggregated['combined_age_default'])
None
```

```
>>> print(author.query)
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       COALESCE("blog_author"."alias", "blog_author"."goes_by", "blog_author"."name") AS "screen_name"
FROM "blog_author
```

### Greatest

```python
class Greatest(*expression, **extra)
```

둘 이상의 필드나 표현식을 지정하면, 가장 큰 값을 리턴한다.

```python
class Blog(models.Model):
    body = models.TextField()
    modified = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    body = models.TextField()
    modified = models.DateTimeField(auto_now=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

>>> from django.db.models.functions import Greatest
>>> blog = Blog.objects.create(body='Greatest is the best.')
>>> comment = Comment.objects.create(body='No, Least is better.', blog=blog)
>>> comments = Comment.objects.annotate(last_updated=Greatest('modified', 'blog__modified'))
>>> annotated_comment = comments.get()
```

```
>>> print(comments.query)
SELECT "blog_comment"."id",
       "blog_comment"."body",
       "blog_comment"."modified",
       "blog_comment"."blog_id",
       MAX("blog_comment"."modified", "blog_blog"."modified") AS "last_updated"
FROM "blog_comment"
INNER JOIN "blog_blog" ON ("blog_comment"."blog_id" = "blog_blog"."id")
```

### Least

```python
class Least(*expression, *extra)
```

둘 이상의 필드나 표현식을 지정하면, 최소값을 리턴한다.

```python
Comment.objects.annotate(
    first_write=Least(
        'modified', 'blog__modified'
        )
      )
```

```
SELECT "blog_comment"."id",
       "blog_comment"."body",
       "blog_comment"."modified",
       "blog_comment"."blog_id",
       MIN("blog_comment"."modified",
           "blog_blog"."modified") AS "first_write"
FROM "blog_comment"
INNER JOIN "blog_blog" ON ("blog_comment"."blog_id" = "blog_blog"."id")
```

### NullIf

```python
class NullIf(expression1, expression2)
```

두 표현식이 일치하면 None을 리턴한다. 두 표현식이 다르면 첫 번째 표현식을 리턴한다.

```python
null_if_author = Author.objects.annotate(
    null_age=NullIf(
        'age', V(0)
        )
    )
```

```
>>> print(null_if_author.query)
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       NULLIF("blog_author"."age", 0) AS "null_age"
FROM "blog_author"
```

## 날짜

```python
# 사용될 모델
class Experiment(models.Model):å
    start_datetime = models.DateTimeField()
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
```

### Extract

```python
class Extract(expression, lookup_name=None, tzinfo=None, **extra)
```

날짜의 구성 요소를 숫자로 추출한다.

expression 인자에는 `DateField`, `DateTimeField`, `TimeField`, `DurationField`, `lookup_name`(날짜의 일부인 IntegerField)를 취한다.  
`tzinfo`는 `pytz`를 전달하여 특정 시간대의 값을 추출할 수 있다.

```python
>>> from datetime import datetime
>>> from django.db.models.functions import Extract
>>> start = datetime(2015, 6, 15)
>>> end = datetime(2015, 7, 2)
>>> Experiment.objects.create(
...    start_datetime=start, start_date=start.date(),
...    end_datetime=end, end_date=end.date())
>>> experiment = Experiment.objects.annotate(
...    start_year=Extract('start_datetime', 'year')).get()
>>> experiment.start_year
2015
>>> Experiment.objects.filter(
...    start_datetime__year=Extract('end_datetime', 'year')).count()
1
```

```
SELECT "dbfunction_experiment"."id",
       "dbfunction_experiment"."start_datetime",
       "dbfunction_experiment"."start_date",
       "dbfunction_experiment"."start_time",
       "dbfunction_experiment"."end_datetime",
       "dbfunction_experiment"."end_date",
       "dbfunction_experiment"."end_time",
       django_datetime_extract('year',"dbfunction_experiment"."start_datetime",'UTC')
           AS "start_year"
FROM "dbfunction_experiment"
```

#### DateField extracts

- `class ExtractYear(expression, tzinfo=None, **extra)` / `lookup_name='year'`
- `class ExtractIsoYear(expression, tzinfo=None, **extra)` / `lookup_name='iso_year'`
- `class ExtractMonth(expression, tzinfo=None, **extra)` / `lookup_name='month'`
- `class ExtractDay(expression, tzinfo=None, **extra)` / `lookup_name='day'`
- `class ExtractWeekDay(expression, tzinfo=None, **extra)` / `lookup_name='week_day'`
- `class ExtractWeek(expression, tzinfo=None, **extra)` / `lookup_name='week'`
- `class ExtractQuarter(expression, tzinfo=None, **extra)` / `lookup_name='quarter'`

```python
>>> from datetime import datetime
>>> from django.utils import timezone
>>> from django.db.models.functions import (
...     ExtractDay, ExtractMonth, ExtractQuarter, ExtractWeek,
...     ExtractWeekDay, ExtractIsoYear, ExtractYear,
... )
>>> start_2015 = datetime(2015, 6, 15, 23, 30, 1, tzinfo=timezone.utc)
>>> end_2015 = datetime(2015, 6, 16, 13, 11, 27, tzinfo=timezone.utc)
>>> Experiment.objects.create(
...    start_datetime=start_2015, start_date=start_2015.date(),
...    end_datetime=end_2015, end_date=end_2015.date())
>>> Experiment.objects.annotate(
...     year=ExtractYear('start_date'),
...     isoyear=ExtractIsoYear('start_date'),
...     quarter=ExtractQuarter('start_date'),
...     month=ExtractMonth('start_date'),
...     week=ExtractWeek('start_date'),
...     day=ExtractDay('start_date'),
...     weekday=ExtractWeekDay('start_date'),
... ).values('year', 'isoyear', 'quarter', 'month', 'week', 'day', 'weekday').get(
...     end_date__year=ExtractYear('start_date'),
... )
{'year': 2015, 'isoyear': 2015, 'quarter': 2, 'month': 6, 'week': 25,
 'day': 15, 'weekday': 2}
```

```
SELECT django_date_extract('year', "dbfunction_experiment"."start_date") AS "year",
       django_date_extract('iso_year', "dbfunction_experiment"."start_date") AS "isoyear",
       django_date_extract('quarter', "dbfunction_experiment"."start_date") AS "quarter",
       django_date_extract('month', "dbfunction_experiment"."start_date") AS "month",
       django_date_extract('week', "dbfunction_experiment"."start_date") AS "week",
       django_date_extract('day', "dbfunction_experiment"."start_date") AS "day",
       django_date_extract('week_day', "dbfunction_experiment"."start_date") AS "weekday"
FROM "dbfunction_experiment"
```

#### DateTimeField extracts

- `class ExtractHour(expression, tzinfo=None, **extra)` / `lookup_name='hour'`
- `class ExtractMinute(expression, tzinfo=None, **extra)` / `lookup_name='minute'`
- `class ExtractSecond(expression, tzinfo=None, **extra)` / `lookup_name='second'`

```python
>>> from datetime import datetime
>>> from django.utils import timezone
>>> from django.db.models.functions import (
...     ExtractDay, ExtractHour, ExtractMinute, ExtractMonth,
...     ExtractQuarter, ExtractSecond, ExtractWeek, ExtractWeekDay,
...     ExtractYear,
... )
>>> start_2015 = datetime(2015, 6, 15, 23, 30, 1, tzinfo=timezone.utc)
>>> end_2015 = datetime(2015, 6, 16, 13, 11, 27, tzinfo=timezone.utc)
>>> Experiment.objects.create(
...    start_datetime=start_2015, start_date=start_2015.date(),
...    end_datetime=end_2015, end_date=end_2015.date())
>>> Experiment.objects.annotate(
...     year=ExtractYear('start_datetime'),
...     isoyear=ExtractIsoYear('start_datetime'),
...     quarter=ExtractQuarter('start_datetime'),
...     month=ExtractMonth('start_datetime'),
...     week=ExtractWeek('start_datetime'),
...     day=ExtractDay('start_datetime'),
...     weekday=ExtractWeekDay('start_datetime'),
...     hour=ExtractHour('start_datetime'),
...     minute=ExtractMinute('start_datetime'),
...     second=ExtractSecond('start_datetime'),
... ).values(
...     'year', 'isoyear', 'month', 'week', 'day',
...     'weekday', 'hour', 'minute', 'second',
... ).get(end_datetime__year=ExtractYear('start_datetime'))
{'year': 2015, 'isoyear': 2015, 'quarter': 2, 'month': 6, 'week': 25,
 'day': 15, 'weekday': 2, 'hour': 23, 'minute': 30, 'second': 1}
```

`pytz`으로 다른 시간대로 변경하여 추출할 수 있고, `Extract()`에 명시적으로 전달하면 최우선시 된다.

```python
>>> import pytz
>>> kor = pytz.timezone('Asia/Seoul')
>>> Experiment.objects.annotate(
...:     day=ExtractDay('start_datetime', tzinfo=kor),
...:     weekday=ExtractWeekDay('start_datetime', tzinfo=kor),
...:     hour=ExtractHour('start_datetime', tzinfo=kor),
...:     ).values(
...:         'day', 'weekday', 'hour').query)
{'day': 16, 'weekday': 3, 'hour': 9}
```

```
SELECT django_datetime_extract(
           'day', "dbfunction_experiment"."start_datetime", 'Asia/Seoul'
          ) AS "day",
       django_datetime_extract(
           'week_day', "dbfunction_experiment"."start_datetime", 'Asia/Seoul'
          ) AS "weekday",
       django_datetime_extract(
           'hour', "dbfunction_experiment"."start_datetime", 'Asia/Seoul'
          ) AS "hour"
FROM "dbfunction_experiment"
```

### Now

```python
class Now
```

쿼리가 실행될 때 SQL을 사용하여 DB 서버의 현재 날짜와 시간을 반환한다.

```python
>>> from django.db.models.functions import Now
>>> Article.objects.filter(published__lte=Now())
<QuerySet [<Article: How to Django>]>
```

> PostgreSQL에서 `CURRENT_TIMESTAMP`는 트랜잭션이 시작된 시간을 반환한다. DB 호환성을 위해 Now()는 `CURRENT_TIMESTAMP` 대신 `STATENEBT_TIMESTAMP`를 사용해야 한다. 트랜잭션 타임스탬프가 필요하다면 `django.contrib.postgres.functions.TransactionNow`를 사용하면 된다.

### Trunc

```python
class Trunc(expression, kind, output_field=None, tzinfo=None, **extra)
```

중요한 구성 요소까지 날짜를 자른다. 정확한 초까지는 필요없는 경우 사용한다. 예를 들어 하루 판매량을 계산할 때 사용할 수 있다.

```python
>>> from datetime import datetime
>>> from django.db.models import Count, DateTimeField
>>> from django.db.models.functions import Trunc
>>> Experiment.objects.create(start_datetime=datetime(2015, 6, 15, 14, 30, 50, 321))
>>> Experiment.objects.create(start_datetime=datetime(2015, 6, 15, 14, 40, 2, 123))
>>> Experiment.objects.create(start_datetime=datetime(2015, 12, 25, 10, 5, 27, 999))
>>> experiments_per_day = Experiment.objects.annotate(
...    start_day=Trunc('start_datetime', 'day', output_field=DateTimeField())
... ).values('start_day').annotate(experiments=Count('id'))
>>> for exp in experiments_per_day:
...     print(exp['start_day'], exp['experiments'])
...
2015-06-15 00:00:00 2
2015-12-25 00:00:00 1

# Query
SELECT django_datetime_trunc(
            'day', "dbfunction_experiment"."start_datetime", 'UTC'
            ) AS "start_day",
       COUNT("dbfunction_experiment"."id") AS "experiments"
FROM "dbfunction_experiment"
GROUP BY django_datetime_trunc('day', "dbfunction_experiment"."start_datetime", 'UTC')

>>> experiments = Experiment.objects.annotate(
...    start_day=Trunc('start_datetime', 'day', output_field=DateTimeField())
... ).filter(start_day=datetime(2015, 6, 15))
>>> for exp in experiments:
...     print(exp.start_datetime)
...
2015-06-15 14:30:50.000321
2015-06-15 14:40:02.000123

# Query
SELECT "dbfunction_experiment"."id",
       "dbfunction_experiment"."start_datetime",
       "dbfunction_experiment"."start_date",
       "dbfunction_experiment"."start_time",
       "dbfunction_experiment"."end_datetime",
       "dbfunction_experiment"."end_date",
       "dbfunction_experiment"."end_time",
       django_datetime_trunc(
           'day', "dbfunction_experiment"."start_datetime", 'UTC'
           ) AS "start_day"
FROM "dbfunction_experiment"
WHERE django_datetime_trunc('day', "dbfunction_experiment"."start_datetime", 'UTC') = 2015-06-15 00:00:00
```

#### DateField truncation

- `class TruncYear(expression, output_field=None, tzinfo=None, **extra)` / `kind='year'`
- `class TruncMonth(expression, output_field=None, tzinfo=None, **extra)` / `kind='month'`
- `class TruncWeek(expression, output_field=None, tzinfo=None, **extra)` / `kind='week'`
- `class TruncQuarter(expression, output_field=None, tzinfo=None, **extra)` / `kind='quarter'`

```python
>>> from datetime import datetime
>>> from django.db.models import Count
>>> from django.db.models.functions import TruncMonth, TruncYear
>>> from django.utils import timezone
>>> start1 = datetime(2014, 6, 15, 14, 30, 50, 321, tzinfo=timezone.utc)
>>> start2 = datetime(2015, 6, 15, 14, 40, 2, 123, tzinfo=timezone.utc)
>>> start3 = datetime(2015, 12, 31, 17, 5, 27, 999, tzinfo=timezone.utc)
>>> Experiment.objects.create(start_datetime=start1, start_date=start1.date())
>>> Experiment.objects.create(start_datetime=start2, start_date=start2.date())
>>> Experiment.objects.create(start_datetime=start3, start_date=start3.date())
>>> experiments_per_year = Experiment.objects.annotate(
...    year=TruncYear('start_date')).values('year').annotate(
...    experiments=Count('id'))
>>> for exp in experiments_per_year:
...     print(exp['year'], exp['experiments'])
...
2014-01-01 1
2015-01-01 2

# Query
SELECT django_date_trunc(
        'year', "dbfunction_experiment"."start_date") AS "year",
       COUNT("dbfunction_experiment"."id") AS "experiments"
FROM "dbfunction_experiment"
GROUP BY django_date_trunc('year', "dbfunction_experiment"."start_date")

>>> import pytz
>>> kor = pytz.timezone('Asia/Seoul')
>>> experiments_per_month = Experiment.objects.annotate(
...    month=TruncMonth('start_datetime', tzinfo=kor)).values('month').annotate(
...    experiments=Count('id'))
>>> for exp in experiments_per_month:
...     print(exp['month'], exp['experiments'])
...
2015-06-01 00:00:00+10:00 1
2016-01-01 00:00:00+11:00 1
2014-06-01 00:00:00+10:00 1

# Query
SELECT django_datetime_trunc(
        'month', "dbfunction_experiment"."start_datetime", 'Asia/Seoul'
       ) AS "month",
       COUNT("dbfunction_experiment"."id") AS "experiments"
FROM "dbfunction_experiment"
GROUP BY django_datetime_trunc(
    'month', "dbfunction_experiment"."start_datetime", 'Asia/Seoul')
```

#### DateTimeField truncation

- `class TruncDate(expression, **extra)` / `lookup_name='date', ouput_field=DateField()`
- `class TruncTime(expression, **extra)` / `lookup_name='time', ouput_field=TimeField()`
- `class TruncDay(expression, output_field=None, tzinfo=None, **extra)` / `kind='day'`
- `class TruncHour(expression, output_field=None, tzinfo=None, **extra)` / `kind='hour'`
- `class TruncMinute(expression, output_field=None, tzinfo=None, **extra)` / `kind='minute'`
- `class TruncSecond(expression, output_field=None, tzinfo=None, **extra)` / `kind='second'`

```python
>>> from datetime import date, datetime
>>> from django.db.models import Count
>>> from django.db.models.functions import (
...     TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond,
... )
>>> from django.utils import timezone
>>> import pytz
>>> start1 = datetime(2014, 6, 15, 14, 30, 50, 321, tzinfo=timezone.utc)
>>> Experiment.objects.create(start_datetime=start1, start_date=start1.date())
>>> kor = pytz.timezone('Asia/Seoul')
>>> Experiment.objects.annotate(
...     date=TruncDate('start_datetime'),
...     day=TruncDay('start_datetime', tzinfo=kor),
...     hour=TruncHour('start_datetime', tzinfo=kor),
...     minute=TruncMinute('start_datetime'),
...     second=TruncSecond('start_datetime'),
... ).values('date', 'day', 'hour', 'minute', 'second').get()
{'date': datetime.date(2014, 6, 15),
 'day': datetime.datetime(2014, 6, 16, 0, 0, tzinfo=<DstTzInfo 'Asia/Seoul' AEST+9:00:00 STD>),
 'hour': datetime.datetime(2014, 6, 16, 0, 0, tzinfo=<DstTzInfo 'Asia/Seoul' AEST+9:00:00 STD>),
 'minute': 'minute': datetime.datetime(2014, 6, 15, 14, 30, tzinfo=<UTC>),
 'second': datetime.datetime(2014, 6, 15, 14, 30, 50, tzinfo=<UTC>)
}

# Query
SELECT django_datetime_cast_date(
        "dbfunction_experiment"."start_datetime", 'UTC'
        ) AS "date",
       django_datetime_trunc(
        'day', "dbfunction_experiment"."start_datetime", 'Asia/Seoul'
        ) AS "day",
       django_datetime_trunc(
        'hour', "dbfunction_experiment"."start_datetime", 'Asia/Seoul'
        ) AS "hour",
       django_datetime_trunc(
         'minute', "dbfunction_experiment"."start_datetime", 'UTC'
       ) AS "minute",
       django_datetime_trunc(
         'second', "dbfunction_experiment"."start_datetime", 'UTC'
       ) AS "second"
FROM "dbfunction_experiment"
```

#### TimeField truncation

- `class TruncHour(expression, output_field=None, tzinfo=None, **extra)` / `kind='hour'`
- `class TruncMinute(expression, output_field=None, tzinfo=None, **extra)` / `kind='minute'`
- `class TruncSecond(expression, output_field=None, tzinfo=None, **extra)` / `kind='second'`

## 수학 함수

```python
# 사용될 모델
class Vector(models.Model):
    x = models.FloatField()
    y = models.FloatField()
```

### Abs

```python
class Abs(expression, **extra)
```

숫자 필드나 표현식의 절대값을 리턴한다.

```python
>>> from django.db.models.functions import Abs
>>> Vector.objects.create(x=-0.5, y=1.1)
>>> vector = Vector.objects.annotate(x_abs=Abs('x'), y_abs=Abs('y')).get()
>>> vector.x_abs, vector.y_abs
(0.5, 1.1)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       ABS("dbfunction_vector"."x") AS "x_abs",
       ABS("dbfunction_vector"."y") AS "y_abs"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Abs)
>>> vectors = Vector.objects.filter(x__abs__lt=1, y__abs__lt=1)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y"
FROM "dbfunction_vector"
WHERE (ABS("dbfunction_vector"."x") < 1.0 AND
       ABS("dbfunction_vector"."y") < 1.0)
```

### ACos

```python
class ACos(expression, **extra)
```
> Arc cosine: 역삼각함수 중 하나로, 코사인을 분모로 내린 역함수 [참고](https://www.scienceall.com/%EC%95%84%ED%81%AC%EC%BD%94%EC%82%AC%EC%9D%B8arccosarccosine/)

숫자 필드나 표현식의 아크 코사인을 반환한다. 표현식 값은 -1 ~ 1 사이여야 한다.

```python
>>> from django.db.models.functions import ACos
>>> Vector.objects.create(x=0.5, y=-0.9)
>>> vector = Vector.objects.annotate(x_acos=ACos('x'), y_acos=ACos('y')).get()
>>> vector.x_acos, vector.y_acos
(1.0471975511965979, 2.6905658417935308)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       ACOS("dbfunction_vector"."x") AS "x_acos", ACOS("dbfunction_vector"."y") AS "y_acos"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(ACos)
>>> vectors = Vector.objects.filter(x__acos__lt=1, y__acos__lt=1)
```

### ASin

```python
class ASin(expression, **extra)
```

숫자 필드나 표현식의 아크 사인을 반환한다. 표현식은 -1 ~ 1 사이여야 한다.

```python
>>> from django.db.models.functions import ASin
>>> Vector.objects.create(x=0, y=1)
>>> vector = Vector.objects.annotate(x_asin=ASin('x'), y_asin=ASin('y')).get()
>>> vector.x_asin, vector.y_asin
(0.0, 1.5707963267948966)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       ASIN("dbfunction_vector"."x") AS "x_asin", ASIN("dbfunction_vector"."y") AS "y_sin"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(ASin)
>>> vectors = Vector.objects.filter(x__asin__lt=1, y__asin__lt=1)
```

### ATan

```python
class ATan(expression, **extra)
```
숫자 필드나 표현식을 아크 탄젠트로 반환한다.

```python
>>> from django.db.models.functions import ATan
>>> Vector.objects.create(x=3.12, y=6.987)
>>> vector = Vector.objects.annotate(x_atan=ATan('x'), y_atan=ATan('y')).get()
>>> vector.x_atan, vector.y_atan
(1.2606282660069106, 1.428638798133829)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       ATAN("dbfunction_vector"."x") AS "x_atan",
       ATAN("dbfunction_vector"."y") AS "y_atan"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(ATan)
>>> # Get vectors whose arctangent is less than 2
>>> vectors = Vector.objects.filter(x__atan__lt=2, y__atan__lt=2)
```

### ATan2

```python
class ATan2(expression1, expression2, **extra)
```

expression1 / expression2 의 아크 탄젠트를 반환한다.

```python
>>> from django.db.models.functions import ATan2
>>> Vector.objects.create(x=2.5, y=1.9)
>>> vector = Vector.objects.annotate(atan2=ATan2('x', 'y')).get()
>>> vector.atan2
0.9209258773829491

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       ATAN2("dbfunction_vector"."x", "dbfunction_vector"."y") AS "atan2"
FROM "dbfunction_vector"
```

### Ceil

```python
class Ceil(expression, **extra)
```

숫자 필드나 표현식보다 크거나 같은 가장 작은 정수를 반환한다.

```python
>>> from django.db.models.functions import Ceil
>>> Vector.objects.create(x=3.12, y=7.0)
>>> vector = Vector.objects.annotate(x_ceil=Ceil('x'), y_ceil=Ceil('y')).get()
>>> vector.x_ceil, vector.y_ceil
(4.0, 7.0)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       CEILING("dbfunction_vector"."x") AS "x_ceil",
       CEILING("dbfunction_vector"."y") AS "y_ceil"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Ceil)
>>> # Get vectors whose ceil is less than 10
>>> vectors = Vector.objects.filter(x__ceil__lt=10, y__ceil__lt=10)
```

### Cos

```python
class Cos(expression, **extra)
```

숫자 필드나 표현식의 코사인을 반환한다.

```python
>>> from django.db.models.functions import Cos
>>> Vector.objects.create(x=-8.0, y=3.1415926)
>>> vector = Vector.objects.annotate(x_cos=Cos('x'), y_cos=Cos('y')).get()
>>> vector.x_cos, vector.y_cos
(-0.14550003380861354, -0.9999999999999986)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       COS("dbfunction_vector"."x") AS "x_cos",
       COS("dbfunction_vector"."y") AS "y_cos"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Cos)
>>> # Get vectors whose cosine is less than 0.5
>>> vectors = Vector.objects.filter(x__cos__lt=0.5, y__cos__lt=0.5)
```

### Cot

```python
class Cot(expression, **extra)
```

숫자 필드나 표현식의 코탄젠트를 반환한다.

```python
>>> from django.db.models.functions import Cot
>>> Vector.objects.create(x=12.0, y=1.0)
>>> vector = Vector.objects.annotate(x_cot=Cot('x'), y_cot=Cot('y')).get()
>>> vector.x_cot, vector.y_cot
(-1.5726734063976826, 0.642092615934331)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       COT("dbfunction_vector"."x") AS "x_cot",
       COT("dbfunction_vector"."y") AS "y_cot"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Cot)
>>> # Get vectors whose cotangent is less than 1
>>> vectors = Vector.objects.filter(x__cot__lt=1, y__cot__lt=1)
```

### Degrees

```python
class Degrees(expression, **extra)
```

숫자 필드나 표현식을 리디안 단위로 변환한다.

```python
>>> from django.db.models.functions import Degrees
>>> Vector.objects.create(x=-1.57, y=3.14)
>>> vector = Vector.objects.annotate(x_d=Degrees('x'), y_d=Degrees('y')).get()
>>> vector.x_d, vector.y_d
(-89.95437383553924, 179.9087476710785)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       DEGREES("dbfunction_vector"."x") AS "x_d",
       DEGREES("dbfunction_vector"."y") AS "y_d"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Degrees)
>>> # Get vectors whose degrees are less than 360
>>> vectors = Vector.objects.filter(x__degrees__lt=360, y__degrees__lt=360)
```

### Exp

```python
class Exp(expression, **extra)
```

숫자 필드나 표현식의 거듭제곱으로 올린(자연 로그 밑) 값을 반환한다.

```python
>>> from django.db.models.functions import Exp
>>> Vector.objects.create(x=5.4, y=-2.0)
>>> vector = Vector.objects.annotate(x_exp=Exp('x'), y_exp=Exp('y')).get()
>>> vector.x_exp, vector.y_exp
(221.40641620418717, 0.1353352832366127)

# Query

SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       EXP("dbfunction_vector"."x") AS "x_exp",
       EXP("dbfunction_vector"."y") AS "y_exp"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Exp)
>>> # Get vectors whose exp() is greater than 10
>>> vectors = Vector.objects.filter(x__exp__gt=10, y__exp__gt=10)
```

### Floor

```python
class Floor(expression, **extra)
```

숫자 필드나 표현식보다 크지 않은 최대 정수값을 반환

```python
>>> from django.db.models.functions import Floor
>>> Vector.objects.create(x=5.4, y=-2.3)
>>> vector = Vector.objects.annotate(x_floor=Floor('x'), y_floor=Floor('y')).get()
>>> vector.x_floor, vector.y_floor
(5.0, -3.0)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       FLOOR("dbfunction_vector"."x") AS "x_floor",
       FLOOR("dbfunction_vector"."y") AS "y_floor"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Floor)
>>> # Get vectors whose floor() is greater than 10
>>> vectors = Vector.objects.filter(x__floor__gt=10, y__floor__gt=10)
```

### Ln

```python
class Ln(expression, **extra)
```

자연 로그에 숫자 필드나 표현식을 리턴한다.

```python
>>> from django.db.models.functions import Ln
>>> Vector.objects.create(x=5.4, y=233.0)
>>> vector = Vector.objects.annotate(x_ln=Ln('x'), y_ln=Ln('y')).get()
>>> vector.x_ln, vector.y_ln
(1.6863989535702288, 5.4510384535657)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       LN("dbfunction_vector"."x") AS "x_ln",
       LN("dbfunction_vector"."y") AS "y_ln"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Ln)
>>> # Get vectors whose value greater than e
>>> vectors = Vector.objects.filter(x__ln__gt=1, y__ln__gt=1)
```

### Log

```python
class Log(expression1, expression2, **extra)
```

두 개의 숫자 필드나 표현식을 지정하고, 첫 번째 로그를 두 번째 베이스에 리턴한다.

```python
>>> from django.db.models.functions import Log
>>> Vector.objects.create(x=2.0, y=4.0)
>>> vector = Vector.objects.annotate(log=Log('x', 'y')).get()
>>> vector.log
2.0

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       LOG("dbfunction_vector"."x", "dbfunction_vector"."y") AS "log"
FROM "dbfunction_vector"
```

### Mod

```python
class Mod(expression1, expression2, **extra)
```

두 개의 숫자 필드나 표현식을 받아서 첫 번째의 나머지를 두 번째로 나눈 값을 반환한다.

```python
>>> from django.db.models.functions import Mod
>>> Vector.objects.create(x=5.4, y=2.3)
>>> vector = Vector.objects.annotate(mod=Mod('x', 'y')).get()
>>> vector.mod
0.8

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       MOD("dbfunction_vector"."x", "dbfunction_vector"."y") AS "mod"
FROM "dbfunction_vector"
```

### Pi

```python
class Pi(**extra)
```

상수 π를 반환한다.

### Power

```python
class Power(expression1, expression2, **extra)
```

두 개의 숫자 필드나 표현식을 받아서, 첫 번째로 올린 값을 두 번째로 거든 제곱한 값을 리턴한다.

```python
>>> from django.db.models.functions import Power
>>> Vector.objects.create(x=2, y=-2)
>>> vector = Vector.objects.annotate(power=Power('x', 'y')).get()
>>> vector.power
0.25

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       POWER("dbfunction_vector"."x", "dbfunction_vector"."y") AS "power"
FROM "dbfunction_vector"
```

### Radians

```python
class Radians(expression, **extra)
```

숫자 필드나 표현식에서 도를 라디안으로 변환한다.

```python
>>> from django.db.models.functions import Radians
>>> Vector.objects.create(x=-90, y=180)
>>> vector = Vector.objects.annotate(x_r=Radians('x'), y_r=Radians('y')).get()
>>> vector.x_r, vector.y_r
(-1.5707963267948966, 3.141592653589793)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       RADIANS("dbfunction_vector"."x") AS "x_r",
       RADIANS("dbfunction_vector"."y") AS "y_r"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Radians)
>>> # Get vectors whose radians are less than 1
>>> vectors = Vector.objects.filter(x__radians__lt=1, y__radians__lt=1)
```

### Round

```python
class Round(expression, **extra)
```

숫자 필드나 표현식을 가장 가까운 정수로 반올림하여 반환한다. 반올림이나 내림 여부는 DB에 따라 다름

```python
>>> from django.db.models.functions import Round
>>> Vector.objects.create(x=5.4, y=-2.3)
>>> vector = Vector.objects.annotate(x_r=Round('x'), y_r=Round('y')).get()
>>> vector.x_r, vector.y_r
(5.0, -2.0)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       ROUND("dbfunction_vector"."x") AS "x_r",
       ROUND("dbfunction_vector"."y") AS "y_r"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Round)
>>> # Get vectors whose round() is less than 20
>>> vectors = Vector.objects.filter(x__round__lt=20, y__round__lt=20)
```

### Sin

```python
class Sin(expression, **extra)
```

숫자 필드나 표현식의 사인을 반환한다.

```python
>>> from django.db.models.functions import Sin
>>> Vector.objects.create(x=5.4, y=-2.3)
>>> vector = Vector.objects.annotate(x_sin=Sin('x'), y_sin=Sin('y')).get()
>>> vector.x_sin, vector.y_sin
(-0.7727644875559871, -0.7457052121767203)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       SIN("dbfunction_vector"."x") AS "x_sin",
       SIN("dbfunction_vector"."y") AS "y_sin"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Sin)
>>> # Get vectors whose sin() is less than 0
>>> vectors = Vector.objects.filter(x__sin__lt=0, y__sin__lt=0)
```

### Sqrt

```python
class Sqrt(expression, **extra)
```

음수가 아닌 숫자 필드나 표현식의 제곱근을 리턴한다.

```python
>>> from django.db.models.functions import Sqrt
>>> Vector.objects.create(x=4.0, y=12.0)
>>> vector = Vector.objects.annotate(x_sqrt=Sqrt('x'), y_sqrt=Sqrt('y')).get()
>>> vector.x_sqrt, vector.y_sqrt
(2.0, 3.46410)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       SQRT("dbfunction_vector"."x") AS "x_sqrt",
       SQRT("dbfunction_vector"."y") AS "y_sqrt"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Sqrt)
>>> # Get vectors whose sqrt() is less than 5
>>> vectors = Vector.objects.filter(x__sqrt__lt=5, y__sqrt__lt=5)
```

### Tan

```python
class Tan(expression, **extra)
```

숫자 필드나 표현식의 탄젠트를 반환한다.

```python
>>> from django.db.models.functions import Tan
>>> Vector.objects.create(x=0, y=12)
>>> vector = Vector.objects.annotate(x_tan=Tan('x'), y_tan=Tan('y')).get()
>>> vector.x_tan, vector.y_tan
(0.0, -0.6358599286615808)

# Query
SELECT "dbfunction_vector"."id",
       "dbfunction_vector"."x",
       "dbfunction_vector"."y",
       TAN("dbfunction_vector"."x") AS "x_tan",
       TAN("dbfunction_vector"."y") AS "y_tan"
FROM "dbfunction_vector"

>>> from django.db.models import FloatField
>>> FloatField.register_lookup(Tan)
>>> # Get vectors whose tangent is less than 0
>>> vectors = Vector.objects.filter(x__tan__lt=0, y__tan__lt=0)
```

## 텍스트 기능

### Chr

```python
class Chr(expression, **extra)
```

숫자 필드나 표현식을 받아서, 표현식의 텍스트를 단일 문자로 리턴한다.  
파이썬의 `chr()`과 같은 동작이다.
길이도 integerField에 변환으로 등록이 가능하다.

```python
>>> Author.objects.create(name='Margaret Smith')
>>> author = Author.objects.filter(name__startswith=Chr(ord('M'))).get()
>>> print(author.name)
Margaret Smith

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by"
FROM "blog_author"
WHERE "blog_author"."name"
LIKE REPLACE(REPLACE(REPLACE((CHAR(77)), '\', '\\'), '%', '\%'), '_', '\_') || '%' ESCAPE '\'
```

### Concat

```python
class Concat(*expression, **extra)
```

두 개 이상의 텍스트 필드나 표현식 목록을 받고, 연결된 텍스트를 리턴한다.
`TextField()`와 `CharField()`를 연결하려면 `output_field()`가 `TextField()`이어야 함을 Django에 지정해주어야 한다.

```python
>>> from django.db.models import CharField, Value as V
>>> from django.db.models.functions import Concat
>>> Author.objects.create(name='Margaret Smith', goes_by='Maggie')
>>> author = Author.objects.annotate(
...     screen_name=Concat(
...         'name', V(' ('), 'goes_by', V(')'),
...         output_field=CharField()
...     )
... ).get()
>>> print(author.screen_name)
Margaret Smith (Maggie)

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       COALESCE("blog_author"."name", ) ||
         COALESCE(COALESCE( (, ) ||
         COALESCE(COALESCE("blog_author"."goes_by", ) ||
         COALESCE(), ), ),
         ) AS "screen_name"
FROM "blog_author"
```

### Left

```python
class Left(expression, length, **extra)
```

텍스트 필드나 표현식에서 앞에서부터 **length**만큼의 문자열을 반환한다.

```python
>>> from django.db.models.functions import Left
>>> Author.objects.create(name='Margaret Smith')
>>> author = Author.objects.annotate(first_initial=Left('name', 2)).get()
>>> print(author.first_initial)
Ma

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       SUBSTR("blog_author"."name", 1, 2) AS "first_initial"
FROM "blog_author"
```

### Length

```python
class Length(expression, **extra)
```

단일 텍스트 필드나 표현식을 받거, 문자 길이를 리턴한다.

```python
>>> from django.db.models.functions import Length
>>> Author.objects.create(name='Margaret Smith')
>>> author = Author.objects.annotate(
...    name_length=Length('name'),
...    goes_by_length=Length('goes_by')).get()
>>> print(author.name_length, author.goes_by_length)
(14, None)

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       LENGTH("blog_author"."name") AS "name_length",
       LENGTH("blog_author"."goes_by") AS "goes_by_length"
FROM "blog_author"

>>> from django.db.models import CharField
>>> CharField.register_lookup(Length)
>>> # Get authors whose name is longer than 7 characters
>>> authors = Author.objects.filter(name__length__gt=7)
```

### Lower

```python
class Lower(expression, **extra)
```

단일 텍스트 필드나 표현식을 받아서, 소문자를 리턴한다.

```python
>>> from django.db.models.functions import Lower
>>> Author.objects.create(name='Margaret Smith')
>>> author = Author.objects.annotate(name_lower=Lower('name')).get()
>>> print(author.name_lower)
margaret smith

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       LOWER("blog_author"."name") AS "name_lower"
FROM "blog_author"
```

### LPad

```python
class LPad(expression, length, fill_text=Value(''), **extra)
```

주어진 텍스트 필드나 표현식의 값의 length 길이가 되도록 왼쪽부터 'fill_text'값을 채워서 리턴한다.

```python
>>> from django.db.models import Value
>>> from django.db.models.functions import LPad
>>> Author.objects.create(name='John', alias='j')
>>> Author.objects.update(name=LPad('name', 8, Value('abc')))
1
>>> print(Author.objects.get(alias='j').name)
abcaJohn
```

### LTrim
```python
class LTrim(expression, **extra)
```

`Trim`과 비슷하지만, 선행 공백만 제거한다.

### Ord

```python
class Ord(expression, **extra)
```

단일 텍스트 필드나 표현식을 받고, 해당 표현식의 첫 문자의 유니 코드 포인트 값을 리턴한다.  
파이썬의 `ord()`와 같은 동작이지만, 두 문자 이상이어도 예외가 발생하지 않는다.

```python
>>> from django.db.models.functions import Ord
>>> Author.objects.create(name='Margaret Smith')
>>> author = Author.objects.annotate(name_code_point=Ord('name')).get()
>>> print(author.name_code_point)
77

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       UNICODE("blog_author"."name") AS "name_code_point"
FROM "blog_author"
```

### Repeat

```python
class Repeat(expression, number, **extra)
```

주어진 텍스트 필드나 표현식을 number 횟수만큼 반환한다.

```python
>>> from django.db.models.functions import Repeat
>>> Author.objects.create(name='John', alias='j')
>>> Author.objects.update(name=Repeat('name', 3))
1
>>> print(Author.objects.get(alias='j').name)
JohnJohnJohn
```

### Replace

```python
class Replace(expression, text, replacement=Value(''), **extra)
```

'expression'의 'text'부분을 'replacement'으로 변경한다.

```python
>>> from django.db.models import Value
>>> from django.db.models.functions import Replace
>>> Author.objects.create(name='Margaret Johnson')
>>> Author.objects.create(name='Margaret Smith')
>>> Author.objects.update(name=Replace('name', Value('Margaret'), Value('Margareth')))
2
>>> Author.objects.values('name')
<QuerySet [{'name': 'Margareth Johnson'}, {'name': 'Margareth Smith'}]>
```

### Reverse

```python
class Reverse(expression, **extra)
```

해당 표현식을 역순으로 리턴한다.

```python
>>> from django.db.models.functions import Reverse
>>> Author.objects.create(name='Margaret Smith')
>>> author = Author.objects.annotate(backward=Reverse('name')).get()
>>> print(author.backward)
htimS teragraM

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       REVERSE("blog_author"."name") AS "backward"
FROM "blog_author"
```

### Right

```python
class Right(expression, length, **extra)
```

텍스트 필드나 표현식의 마지막 문자를 length 길이만큼 반환한다.

```python
>>> from django.db.models.functions import Right
>>> Author.objects.create(name='Margaret Smith')
>>> author = Author.objects.annotate(last_letter=Right('name', 1)).get()
>>> print(author.last_letter)
h

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       SUBSTR("blog_author"."name", (1 * -1)) AS "last_letter"
FROM "blog_author"
```

### RPad

```python
class RPad(expression, length, fill_text=Value(''), **extra)
```

`LPad`와 반대

### RTrim

```python
class RTrim(expression, **extra)
```

'Trim'과 비슷하지만, 후행 공백만 제거한다.

### StrIndex

```python
class StrIndex(string, substring, **extra)
```

'string'에서 'substring'이 발생한 위치의 인덱스를 반환(1부터 시작)한다.  
찾지 못하면 0을 반환한다.

```python
>>> from django.db.models import Value as V
>>> from django.db.models.functions import StrIndex
>>> Author.objects.create(name='Margaret Smith')
>>> Author.objects.create(name='Smith, Margaret')
>>> Author.objects.create(name='Margaret Jackson')
>>> Author.objects.filter(name='Margaret Jackson').annotate(
...     smith_index=StrIndex('name', V('Smith'))
... ).get().smith_index
0

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       INSTR("blog_author"."name", Smith) AS "smith_index"
FROM "blog_author"
WHERE "blog_author"."name" = Margaret Jackson

>>> Author.objects.filter(name='Smith, Margaret').annotate(
...     smith_index=StrIndex('name', V('Marga'))
... ).get().smith_index
8

>>> authors = Author.objects.annotate(
...    smith_index=StrIndex('name', V('Smith'))
... ).filter(smith_index__gt=0)
<QuerySet [<Author: Margaret Smith>, <Author: Smith, Margaret>]>

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       INSTR("blog_author"."name", Smith) AS "smith_index"
FROM "blog_author"
WHERE INSTR("blog_author"."name", Smith) > 0
```

### Substr

```python
class Substr(expression, pos, length=None, **extra)
```

'expression'의 pos에서부터 length 길이의 문자열을 리턴한다.

```python
>>> from django.db.models.functions import Lower, Substr
>>> Author.objects.create(name='Margaret Smith')
>>> Author.objects.update(alias=Lower(Substr('name', 1, 5)))
1    # 적용된 row 수
>>> print(Author.objects.get(name='Margaret Smith').alias)
marga
```

### Trim

```python
class Trim(expression, **extra)
```

선,후행 공백을 제거 한 텍스트 필드나 표현식을 리턴한다.

```python
>>> from django.db.models.functions import Trim
>>> Author.objects.create(name='  John  ', alias='j')
>>> Author.objects.update(name=Trim('name'))
1
>>> print(Author.objects.get(alias='j').name)
John
```

### Upper

```python
class Upper(expression, **extra)
```

텍스트 필드나 표현식을 받아서 대문자로 리턴한다.

```python
>>> from django.db.models.functions import Upper
>>> Author.objects.create(name='Margaret Smith')
>>> author = Author.objects.annotate(name_upper=Upper('name')).get()
>>> print(author.name_upper)
MARGARET SMITH

# Query
SELECT "blog_author"."id",
       "blog_author"."name",
       "blog_author"."age",
       "blog_author"."alias",
       "blog_author"."goes_by",
       UPPER("blog_author"."name") AS "name_upper"
FROM "blog_author"
```

## 윈도우 함수

나중에 필요할때 찾아 살펴보기
