---
layout: post
section-type: post
title: Two Scoops of django 3.x - Chap7. Queries and the Database Layer
category: django
tags: [ 'django' ]
---

> [Two Scoops of Django 3.x](https://www.feldroy.com/books/two-scoops-of-django-3-x)

---

## 7.1 Use `get_object_or_404()` for Single Objects

단일 객체를 가져와서 작업할 경우 `get()` 보다는 `get_object_or_404()`를 이용해야 합니다.  

단 아래의 제약 사항을 따라야 합니다.

- 뷰에서만 사용한다.
- 헬퍼 함수, 폼, 모델 메서드, 뷰를 제외한 곳, 뷰와 직접적으로 관련된 곳이 아닌 곳에서는 사용 금지

## 7.2 Be Careful With Queries That Might Throw Exceptions

`get_object_or_404()`는 자체적으로 예외처리를 해주지만, 그 외에는 반드시 예외처리를 해야 합니다.

### 7.2.1 ObjectDoesNotExist vs. DoesNotExist

- `ObjectDoesNotExist`는 모든 모델 객체에서 사용 가능
- `DoesNotExist`는 특정 모델에서만 사용 가능

```python
from django.core.exceptions import ObjectDoesNotExist

from flavors.models import Flavor
from store.exceptions import OutOfStock

def list_flavor_line_item(sku):
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0)
    except Flavor.DoesNotExist:
        msg = 'We are out of {0}'.format(sku) raise OutOfStock(msg)
        
def list_any_line_item(model, sku):
    try:
        return model.objects.get(sku=sku, quantity__gt=0)
    except ObjectDoesNotExist:
        msg = 'We are out of {0}'.format(sku) raise OutOfStock(msg)
```

### 7.2.2 When You Just Want One Object but Get Three Back

객체가 2개 이상 반환되었을 때는 `MultipleObjectsReturned` 예외처리를 하면 됩니다.

```python
from flavors.models import Flavor
from store.exceptions import OutOfStock, CorruptedDatabase

def list_flavor_line_item(sku): 
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0) 
    except Flavor.DoesNotExist:
        msg = 'We are out of {}'.format(sku)
        raise OutOfStock(msg)
    except Flavor.MultipleObjectsReturned:
        msg = 'Multiple items have SKU {}. Please fix!'.format(sku) 
        raise CorruptedDatabase(msg)
```

## 7.3 Use Lazy Evaluation(지연연산) to Make Queries Legible

복잡한 쿼리의 경우 몇 줄 안되는 코드에 무리하게 줄이면 안됩니다.

```python
# 나쁜 예
from django.db.models import Q
from promos.models import Promo

def fun_function(name=None):
    return Promo.objects.active().filter(
        Q(name__startswith=name) | 
        Q(description__icontains=name))
```

django는 결과를 실행하기 전까지 DB를 호출하지 않기 때문에, 복잡한 ORM을 여러 줄로 나누어서 사용함으로써 가독성을 향상시키고, 유지보수를 보다 쉽게 해줍니다.

```python
from django.db.models import Q
from promos.models import Promo

def fun_function(name=None):
    results = Promo.objects.active()
    results = results.filter(
                   Q(name__startswith=name) |
                   Q(description__icontains=name)
               )
    results = results.exclude(status='melted') 
    results = results.select_related('flavors') 
    return results
```

### 7.3.1 Chaning Queries for Legibility

Pandas와 JS 커뮤니티에서는 지연평가 대신 아래와 같은 연결 방법을 차용합니다.

```python
from django.db.models import Q
from promos.models import Promo

def fun_function(name=None):
    qs = (Promo
         .objects
         .active()
         .filter(
             Q(name__startswith=name) |
             Q(description__icontains=name)
         )
         .exclude(status='melted')
         .select_related('flavors')
     )
    return qs
```

하지만 디버깅을 하려면 일부분을 주석처리 하는 등의 추가 처리가 필요합니다.
(개인적으로 비추천)

## 7.4 Lean on Advanced Query Tools

### 7.4.1 Query Expressions

DB에서 읽기 작업을 수행될 때 쿼리 표현식으로 해당 읽기가 실행되는 동안 값을 산출하거나 연산을 수행하는데 이용할 수 있습니다.

```python
# 나쁜 예
from models.customers import Customer

customers = []
for customer in Customer.objects.iterator():
    if customer.scoops_ordered > customer.store_visits:
        customers.append(customer)
```

- DB의 모든 Customer 레코드를 하나하나 루프 돌기 때문에 매우 느리고, 메모리도 많이 사용합니다.
- 위 코드는 'READ'만 하기 때문에 문제가 없겠지만, 'UPDATE'와 같은 값이 변경되는 처리라면 데이터가 분실 될 위험이 있습니다.(경합 상황)

```python
# 개선된 예
from django.db.models import F
from models.customers import Customer

customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
```

위 코드는 아래의 SQL을 실행하게 됩니다.

```sql
SELECT * from customers_customer where scoops_ordered > store_visits
```

### 7.4.2 Database Functions

Django에서는 `UPPER()`, `LOWER()`, `COALESCE()`, `LENGTH()`, `SUBSTR()` 등의 데이터베이스 함수를 이용 할 수 있습니다. 다음과 같은 장점들이 있습니다.

- 쉽게 간결합니다.
- 파이썬으로 작성된 로직을 DB로 이전할 수 있습니다. 파이썬은 DB 안에서 데이터를 처리하는 것보다 빠르기 때문에 성능이 많이 향상됩니다.
- ORM은 다양한 DB를 지원합니다.
- DB 함수들은 쿼리 표현식입니다.

[Django Query Expressions](docs.djangoproject.com/en/3.2/ref/models/expressions/)

## 7.5 Don't Drop Down to Raw SQL Until It's Necessary

ORM은 다양한 환경에서 단순한 쿼리 작성, 모델에 대한 접근, 업데이트의 유효성 검사, 보안을 제공합니다.  

Raw SQL을 사용한다면 다음과 같은 문제가 발생할 수 있습니다.

- 장고 서드 파티 패키지로 릴리스 될때 이식성이 떨어질 수 있음
- 마이그레이션 하는 경우, 특정 DB에 종속된 기능을 SQL 로 작성했다면,  마이그레이션 과정에서 복잡한 문제가 발생할 가능성이 높음
- ORM의 장점을 모두 포기해야 함

Raw SQL을 사용해야 할 경우

- Raw SQL을 직접 작성함으로서 ORM이나 파이썬 코드보다 월등히 단출되는 경우
 - ex) 큰 데이터 세트에 다수의 쿼리셋이 연동되는 경우

## 7.6 Add Indexes as Needed

모델에 `db_index = True`만 추가하면 사용할 수 있습니다.  

인덱스를 사용해야 하는 경우

- 인덱스가 빈번히 이용될 때(모든 쿼리의 10~25% 사이)
- 실제 데이터 혹은 실제와 비슷한 데이터가 존재하여 인덱싱 결과에 대한 분석이 가능할 때
- 인덱싱을 통해 성능이 향상되는지 테스트가 가능할 때

'Chap26. Finding and Reducting Bottlenecks'에서 추가적으로 다룰 예정

## 7.7 Transactions

트랜잭션: 둘 또는 그 이상의 데이터베이스 업데이트를 **단일화된 작업**으로 처리하는 기법

### 7.7.1 Wrapping Each HTTP Request in a Transaction

```python
# settings/base.py

DATABASES = {
    'default': {
        # ...
        'ATOMIC_REQUESTS': True,
    },
}
```

Django의 `ATOMIC_REQUESTS` 설정은 읽기 데이터를 포함한 모든 요청을 트랜잭션 처리하되 됩니다. 장점은 모든 DB 쿼리가 보호되는 안정성을 얻을 수 있다는 것입니다. 히자만 성능이 저하될 수 있다는 단점이 있습니다.
  
그리고  **에러가 발생**해야만 롤백이 됩니다.  
ex) 작업 처리 중 확인 메일을 보낸 후에 롤백이 된다면...  

DB가 아닌 아이템에 대한 데이터 생성, 변경, 삭제하는 뷰를 만들 때는 `transaction.non_atomic_request()` 데코레이팅하는 방법을 고려해 볼 수 있습니다.

```python
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Flavor

@transaction.non_atomic_requests
def posting_flavor_status(request, pk, status):
    flavor = get_object_or_404(Flavor, pk=pk)
    
    # 오토커밋 모드가 실행
    flavor.latest_status_change_attempt = timezone.now()
    flavor.save()
    
    with transaction.atomic():
        # 트랜잭션 안에서 실행
        flavor.status = status
        flavor.latest_status_change_success = timezone.now()
        flavor.save()
        return HttpResponse('Hooray')
        
    # 트랜잭션이 실패하면 400 반환
    return HttpResponse('Sadness', status_code=400)
```

### 7.7.2 Explicit Transaction Declaration

- DB에 변경이 생기지 않는 작업은 트랜잭션 처리하지 않습니다.
- DB에 변경이 생기는 작업은 반드시 트랜잭션 처리합니다.
- DB 읽기 작업을 수반하는 DB 변경 작업이나 DB 성능에 관련된 특별한 경우는 위 두 가지 모두 고려해야 합니다.

Purpose | ORM method | Use Transaction?
---|---|---
데이터 생성 | `.creaet()`, `bulk_create()`, `.get_or_create()` | O
데이터 가져오기 | `.get()`, `filter()`, `.count()`, `.iterate()`, `exists()`, `.exclude()`, etc | X
데이터 수정하기 | `.update()` | O
데이터 지우기 | `.delete()` | O

### 7.7.3 django.http.StreamingHttpResponse and Transactions

- StreamingHttpResponse 사용 예: [hong_devlog](https://hong-dev.github.io/vibe/streaming/)

뷰가 StreamingHttpResponse를 반환한다면 응답이 시작된 이상 트랜잭션 처리를 할 수 없습니다.  

- ATOMIC_REQUESTS 의 기본값을 False로 설정하고, '(7.7.2)명시적인 트랜잭션'을 선언하여 처리해야 합니다.
- 뷰를 `django.db.tracsaction.non_atomic_requests` 데코레이션으로 감쌉니다.

스트리밍 응답에 트랜잭션을 적용할 수 있지만, 스트림 응답이 추가적인 SQL 쿼릴르 생성했다면 해당 부분은 트랜잭션을 적용할 수 없습니다.

### 7.7.4 Transactions in MySQL

> 업무에 바로 쓰는 SQL 튜닝 Chap2. DB 엔진 용어 발췌. 

- Storage Engine: 사용자가 요청한 SQL 문을 토대로 DB에 저장된 디스크나 메모리에서 필요한 데이터를 가져오는 역할
- 일반적으로 트랜잭션 발생은 데이터를 처리하는 OLTP(online transaction processing) 환경이 대다수인 만큼 주로 InnoDB 엔진을 사용.  
- 대량의 쓰기 트랜잭션이 발생하면 MyISAM 엔진을 사용. 
- 메모리 데이터를 로드하여 빠르게 읽는 효과를 내려면 Memory 엔진

MySQL 설정이 트랜잭션을 지원하지 않으면 Django는 항상 자동 커밋 모드입니다.  
MYSQL 설정이 트랜잭션을 지원한다면 앞서 언급한 대로 트랜잭션을 처리합니다.

[MySQL Transaction](https://dev.mysql.com/doc/refman/8.0/en/sql-transactional-statements.html)

### 7.7.5 Django ORM Transaction Resources

[Django Transaction Doc](https://docs.djangoproject.com/en/3.2/topics/db/transactions/)

[Real Python Transaction Tutorial](https://realpython.com/transaction-management-with-django-1-6/)
