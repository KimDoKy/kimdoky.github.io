---
layout: post
section-type: post
title: Two Scoops of Django - chap7. 쿼리와 데이터베이스 레이어
category: django
tags: [ 'django' ]
---

다른 ORM과 마찬가지로 장고도 여러 종류의 다른 데이터를 데이터베이스 종류와는 독립적인 형태로 객체화한다. 그리고 생성된 객체에 상호 작용할 수 있는 메서드 세트를 제공한다. 대부분 원래 의도대로 역할을 수행하지만 그렇지 않은 경우들도 존재한다.

## 7.1 단일 객체에서 get_object_or_404() 이용하기
단일 객체를 가져와서 작업을 하는 세부 페이지 같은 뷰에서는 get() 대신에 get_object_or_404()를 이용하도록 한다.

> #### get_object_or_404()는 뷰에서만 이용하자.  
- 뷰에서만 이용한다.
- 헬퍼 함수, 폼, 모델 메서드, 뷰를 제외한 다른 곳 그리고 뷰와 직접적으로 관련된 곳이 아닌 곳에서는 이용하지 말자.  
어떤 프로그래머는 장고의 get_object_or_404()의 편리함에 반해 뷰, 모델, 폼 등의 모든 코드에 get_object_or_404()를 이용했다. 개발환경이나 테스트에서는 문제가 없었지만 불행히 관리자가 특정 데이터를 지우면 모든 사이트가 망가져보리는 결과를 초래했다. get_object_or_404()는 뷰에서만 이용해야 한다!

## 7.2 예외를 일으킬 수 있는 쿼리를 주의하자
단일 모델 인스턴스에서 get_object_or_404()를 이용할 때는 try-except 블로으로 예외 처리를 할 필요가 없다. get_object_or_404()가 처리하기 때문이다. 하지만 이를 제외한 경우에는 try-except를 이용한 예외처리를 해야 한다.

### 7.2.1 ObjectDoseNotExist와 DoesNotExist
ObjectDoseNotExist는 어떤 모델 객체에도 이용할 수 있지만 DoesNotExist는 특정 모델에서만 이용할 수 있다.

```python
from django.core.exceptions import ObjectDoseNotExist

from flavors.models import Flavor
from store.exceptions import OutOfStock

def list_flavor_line_item(sku):
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0)
    except Flavor.DoesNotExist:
        msg = "We are out of {0}".format(sku)
        raise OutOfStock(msg)

def list_any_line_item(model, sku):
    try:
        return model.objects.get(sku=sku, quantity__gt=0)
    except ObjectDoseNotExist:
        msg = "We are out of {0}".format(sku)
        raise OutOfStock(msg)
```

### 7.2.2 여러 개의 객체가 반환되었을 때
쿼리가 하나 이상의 객체를 반환할 수도 있다면 MultipleObjectsReturned 예외를 참고한다.이 예외 구문은 우리가 원하는 방향으로 처리하면 된다. 예를 들면 특별한 예외 경우를 발생시키거나 에러 로그를 남길 수 있다.

```python
from flavors.models import Flavor
from store.exceptions import OutOfStock, CorruptedDatabase

def list_flavor_line_item(sku):
    try:
        return Flavor.objects.get(sku=sku, quantity__gt=0)
    except Flavor.DoesNotExist:
        msg = "We are ouot of {}".format(sku)
        raise OutOfStock(msg)
    except Flavor.MultipleObjectsReturned:
        msg = "Multiple items have SKU {}. Plaese fix!".format(sku)
        raise CorruptedDatabase(msg)
```

## 7.3 쿼리를 좀 더 명확하게 하기 위해 지연 연산 이용하기
장고의 ORM은 매우 강력하기 때문에 코드를 명확하게 해야하는 책임도 따른다(유지보수가 한결 수월해짐). 복잡한 쿼리의 경우 몇 줄 안되는 코드에 너무 많은 기능을 넣는 것을 피해야 한다.

```python
# 나쁜 예
from django.models import Q

from promos.models import Promo

def fun_funtion(**kwargs):
    """유효한 아이스크림 프로모션 찾기"""
    # 너무 길게 작성된 쿼리 체인이 화면이나 페이지를 넘겨 버리게
    # 되므로 좋지 않다.
    return Promo.objects.active().filter(Q(name__startwith=name)|Q(description__icontains=name))
```

이런 달갑지 않은 과정을 피하기 위해 지연 연산(lazy evaluation)을 이용하여 장고 코드를 좀 더 깔끔하게 만들 수 있다.  
지연 연산은 데이터가 정말로 필요하기 전까지는 장고가 SQL을 호출하지 않는 특징을 가리킨다. 따라서 ORM 메서드와 함수를 얼마든지 원하는 만큼 연결해서 코드를 써내려 갈 수 있다. 결과를 실행하기 전까지는 장고는 데이터베이스에 연동되지 않는다. 한 줄에 여러 메서드와 데이터베이스의 각종 기능을 엮어 넣는 대신에, 이를 여러 줄에 걸쳐 나눠 쓸 수 있다. 이는 가독성을 엄청나게 향상시켜주며 유지보수가 한결 쉬워지게 한다.  
위의 나쁜 예를 여러 줄로 나누어 좀 더 간결하고 명확하게 구성한 코드이다.

```python
# 절대 따라하지 말것!
from django.models import Q

from promos.models import Promo

def fun_funtion(**kwargs):
   """유효한 아이스크림 프로모션 찾기"""
   results = Promo.objects.active()
   retults = results.filter(
               Q(name__startwith=name) |
               Q(description__icontains=name)
       )
   results = results.exclude(status='melted')
   retults = results.select_related('flavors')
   return results
```
수정된 코드에서 최종 결과가 어떤건지 보기 쉬워졌다. 또한 이렇게 코드를 여러 줄로 분리함으로써 코드에 주석을 좀 더 쉽게 달 수도 있다.

## 7.4 고급 쿼리 도구 이용하기
장고의 ORM은 다양한 경우를 처리할 수 있지만 모든 경우를 다 완벽히 처리할 수 있는 것은 아니다. 따라서 쿼리 요청 세트가 반환된 후 파이썬을 이용하여 이 데이터들을 다듬을 필요가 있다. 하지만 데이터베이스는 데이터 관리와 가공에서 파이썬(루비, 자바, 고 등)보다 월등히 빠르기 때문에 한 번 더 파이썬을 이용하는 것이 최선인지에 대한 문제가 발생한다.  
파이썬을 이용한 데이터를 가공하기 이전에 장고의 고급 쿼리 도구들을 이용하면 성능이 향상될 뿐 아니라 파이썬 기반 데이터 가공보다 더 잘 태스트되어 나온 코드를 이용하는 장점이 생긴다.(고급 쿼리 도구는 장고와 대부분의 데이터베이스 사이에서 지속적인 테스트를 실행해준다.)

### 7.4.1 쿼리 표현식(query expression)
데이터베이스에서 읽기 작업이 수행될 때 쿼리 표현식은 해당 읽기가 실행되는 동안 값을 산출해 내거나 연산을 수행하는 데 이용될 수 있다. 예를 들어 아이스크림 상점을 방문한 모든 고객 둥 한 번 방문할 때마다 평균 한 주걱 이상의 아이스크림을 주문한 모든 고객 목록을 가져오는 샘플을 작성해 보자.  

좀 위험하더라도 쿼리 표현식을 이용하지 않고 처리하는 방법이다.

```python
# 나쁜 예
from models.customers import Customer

customers = []
for customer in Customer.objects.iterate():
    if customer.scoops_ordered > customer.store_visits:
        customers.append(customer)
```

- 데이터베이스 안의 모든 고객 레코드에 해대 하나하나 파이썬을 이용한 루프가 돌고 있다. 이는 매우 느리며 메모리도 많이 이용하게 된다.
- 코드가 얼마나 이용되는지에 상관없이, 코드 자체가 경합 상황(race condition: 공유 자원에 대해 여러 개의 프로세스가 동시에 접근을 시도하는 상태)에 직면하게 된다. 이 코드는 사용자가 데이터와 상호 교류하는 동시에 실행되는 코드다. 여기서 단순 'READ' 역할만을 하는 상황에서는 문제가 없을지 몰라도, 실행 중에 'UPDATE'가 처리되는 환경에서라면 테이블 분실이 생길 여지가 있다.

쿼리 표현식을 통해 장고는 코드들이 서로 경합하는 상황을 피할 방법을 제시한다.

```python
from django.db.models import F
from models.customers import Customer
customers = Customer.objects.filter(scoops_ordered__gt=F('store_visits'))
```

이 코드는 데이터베이스 자체 내에서 해당 조건을 비교하는 기능을 가지고 있다. 내부적으로 장고는 다음과 같은 코드를 실행한다.

```python
SELECT * from customers_customer where scoops_ordered > store_visits
```
쿼리 표현식은 프로젝트의 안전성과 성능을 향상시켜주기 때문에 꼭 익혀두어야 한다.

<https://docs.djangoproject.com/en/1.8/ref/models/expressions/>

### 7.4.2 데이터베이스 함수들
장고 1.8에서는 UPPER(), LOWER(), COALESCE(), CONCAT(), LENGTH(), SUBSRT() 등의 일반적인 데이터베이스 함수를 이용할 수 있다.

1. 이용이 매우 쉽고 간결하다. 새 프로젝트든 기존 프로젝트든 상관없다.
2. 데이터베이스 함수들은 (비즈니스) 로직을 파이썬 코드에서 데이터베이스로 더 많이 이전할 수 있게 해 준다. 파이썬으로 데이터를 처리하는 것이 데이터베이스 내에서 처리하는 것보다 빠를 수 없기 때문에 성능이 굉장히 향상된다.. 데이터베이스 함수들은 데이터베이스별로 다르게 구현되어 있지만 장고의 ORM은 이를 하나로 통합했다. 따라서 PostgreSQL에서 쓰인 코드는 MySQL이나 SQLite3에서도 잘 동작한다.
4. 데이터베이스 함수들은 쿼리 표현식이기도 하다. 장고 ORM에서 구현해 놓은 또 다른 종류의 일반적인 패턴을 가진 쿼리 표현식이 되는 것이다.

<https://docs.djangoproject.com/en/1.8/ref/models/database-functions>

## 7.5 필수불가결한 상황이 아니라면 로우 SQL을 지향하자
ORM(Object-Relational Model)이라는 관계형 매핑은 매우 높은 생산성을 제공하는데, 우리가 처리하는 다양한 환경에서의 단순한 쿼리 작성뿐만아니라 모델에 대한 접근과 업데이트를 할 때 유효성 검사와 보안을 제공하기 때문이다. 따라서 이용하려는 쿼리를 ORM으로 표현할 수 있다면 반드시 ORM을 이용하는 것이 좋다.  
또한 개발하는 장고 앱이 서드 파티 패키지로 릴리스된다로 할 때, 로우 SQL을 이용하는 것은 앱의 이식성(portability)이 떨어질 수 있다.  

다른 환경의 데이터베이스로 데이터를 마이그레이션해야 하는 경우, 특정 데이터베이스에 종속된 기능을 SQL 쿼리를 가지고 작성했다면, 이는 데이터베이스 마이그레이션 과정에서 매우 복잡한 문제가 될 것이다.  

로우 SQL을 사용해야 하는 상황은? 로우 SQL을 직접 이용함으로써 파이썬 코드나 ORM을 통해 생성된 코드가 월등히 간결해지고 단축되는 경우에만 사용해야 한다. 예를 들어 큰 데이터 세트에 적용되는 다수의 쿼리세트가 연동되는 경우라면, 로우 SQL을 이용함으로써 더욱 효과적으로 처리하게 된다.

> #### 장고의 SQL을 이용하는 것에 대한 조언  
"ORM이 많은 일을 대신 해 준다는 말은 사실이다. 하지만 때때로 SQL이 정답일 때도 있다. 장고의 ORM에 대한 대략적인 개념을 이야기해 보자면 SQL을 기능적으로 이용하기 위해 만들어 놓은 저장소라는 것이다. 복잡한 SQL이 필요하다면 복잡한 SQL을 이용해야 한다. 단지 raw()와 extra() 메서드들을 과용하지 않는 범위에서 균형을 맞추어 가면서 말이다."  
"SQL로 쿼리를 짜는게 더 쉽다면 이용하라. 단 extra()는 끔찍하니 자제하도록 하자. 대신 raw()가 더 나으니 필요하다면 ras()를 이용하도록 하자."

![]({{site.url}}/img/post/django/two_scoops/7.1.png)
>  이 아이스크림은 로우 SQL 맛을 포함하고 있다. 약간 끈적이므로 주의하자

## 필요에 따라 인덱스를 이용하자
db_index=True를 추가하는 것은 쉽지만 언제 추가해야 하는지 판단이 필요하다. 우선 처음에는 인덱스 없이 시작한다. 그런 다음 필요에 따라 하나하나 추가해 나간다.

#### 인덱스를 추가해야 하는 경우

- 인덱스가 빈번하게(모든 쿼리의 10~25% 사이에서) 이용될 때
- 실제 데이터 또는 실제와 비슷한 데이터가 존재해서 인덱싱 결과에 대한 분석이 가능할 때
- 인덱싱을 통해 성능이 향상되는지 테스트할 수 있을 때

PostgreSQL을 이용할 때 pg_stat_activity는 실제로 어떤 인덱스들이 이용되는지 알려준다.

## 7.7 트랜잭션
장고 1.8부터는 기본적으로 ORM이 모든 쿼리를 호출할 때마다 자동으로 커밋을 하게 되었다. 즉 매번 `.create()`나 `.update()`가 호출될 때마다 SQL 데이터베이스 안의 값들이 실제로 변한다는 뜻이다. 이로 인해 뷰(혹은 다른 처리 과정에서)에서 둘 이상의 데이터베이스 수정이 요구될 때 첫 번째 수정은 문제가 없지만 두 번째 수정에서 문제가 발생해 데이터베이스상의 충돌이 일어날 위험이 존재한다는 것이다.  

이러한 데이터베이스 충돌을 해결하기 위해 데이터베이스 트랜잭션을 이용하는 방법이 있다. 데이터베이스 트랜잭션이란 둘 또는 그 이상의 데이터베이스 업데이트를 **단일화된 작업** 으로 처리하는 기법을 말한다. 이 경우 하나의 수정 작업(update)이 실패하면 트랜잭션상의 모든 업데이트가 실패 이전 상태로 복구된다. 이를 제대로 이용하려면 데이터베이스 트랜잭션이 **원자성(atomic)**, **일관성(consistent)**, **독립성(isolated)**, **지속성(durable)** 을 가져야 한다. 이런 특성을 ACID라고 한다.  

장도 1.8부터는 강력하면서도 상대적으로 이용하기 쉬운 트랜잭션 매커니즘을 제공한다. 덕분에 프로젝트의 직관적인 패턴의 데코레이터와 콘텍스트 매니저를 이용해 데이터베이스의 일관성 관리가 매우 쉬워졌다.

### 7.7.1 각각의 HTTP 요청을 트랜잭션으로 처리하라

```python
# settings/base.py

DATABASE = {
    'default': {
        # ...
        'ATOMIC_REQUESTS': True.
    },
}
```

장고에서는 ATOMIC_REQUESTS을 True로 설정함으로 모든 웹 요청을 트랜잭션으로 쉽게 처리할 수 있다. 이러한 구조는 뷰에서의 모든 데이터베이스 쿼리가 보호되는 안전성을 얻을 수 있고 초기 구성에서 데이터베이스의 무결성을 유지하는데 큰 효과적인 구성이지만, 성능 저하를 가져올 수 있다. 데이터베이스틔 디자인이나 데이터베이스가 얼마나 잠금(locking)을 잘 처리하는지에 따라 성능 저하량도 다르다.  

ATOMIC_REQUESTS를 이용할 때 주의할 점은, 오직 에러가 발생하고 나서야 데이터베이스 상태가 롤백된다는 것이다. 이러한 문제는 데이터베이스 이외의 장소(이메일이나 SMS를 보내거나, 서드 파티 API를 이용할때, 파일 시스템에 무언가를 쓸 때 등)에서 먼가를 '쓰는' 절차에서 언제든지 일어날 수 있다. 따라서 데이터베이스가 아닌 아이템에 대해 데이터를 생성, 변경, 삭제(create, update, delete)하는 뷰를 만들 때는 해당 뷰를 `transaction.non_atomic_requests()`로 데코레이팅하는 것을 고려해야 한다.  

> #### non_atomic_requests()에 대한 의견  
"이 데코레이터는 뷰와 모델 사이의 강한 커플링을 요구하는데 이 때문에 코드의 유지 보수가 어려워지게 된다. 우리하 하위 호환을 고려하지 않아고 되었다면 아마 더 나은 다른 디자인을 구상했을 것이다."

다음은 좀 더 명시적 선언을 통한 매우 간단한 API 스타일의 함수 기반 뷰다.

```python
# flavors/views.py

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Flavor

@transaction.non_atomic_requests
def posting_flavor_status(request, pk, status):
    flavor = get_object_or_404(Flavor, pk=pk)

    # 여기서 오토커밋 모드가 실행된다(장고의 기본 설정)
    flavor.latest_status_change_attempt = timezone.now()
    flavor.save()

    with transaction.atomic():
        # 이 코드는 트랜잭션 안에서 실행된다.
        flavor.status = status
        flavor.latest_status_change_success timezone.now()
        flavor.save()
        return HttpResponse("Hooray")

    # 트랜잭션이 실패하면 해당 상태 코드를 반환하다.
    return HttpResponse("Sadness", status_code=400)
```

> #### 의료 정보나 금융 정보를 다루는 프로젝트들에 대해  
의료 정보나 금융 정보를 다루는 프로젝트들의 경우 트랜잭션 무결성(transactional integrity)보다는 이벤트 일관성(eventual consistency)에 초첨을 맞추어 구성하게 된다. 다른 말로 하면 트랜잭션이 실패해 롤백될 상황이 늘 준비되어 있다는 것이다. 다행히 트랜잭션 덕분에 롤백되어도 데이터는 안전하고 깔끔하게 유지될 수 있다.

### 7.7.2 명시적인 트랜잭션 선언
명시적 트랜잭션 선언(explicit transaction declaration)은 사이트 성능을 개선하는 방법 중 하나다. 트랜잭션에서 어떤 뷰와 비즈니스 로직이 하나로 엮여있고, 어떤 것이 그렇지 않은지 명시해 주는 것이다. 개발할 때 더 많은 시간을 요구하는 것이 단점이다.

> #### ATOMIC_REQUESTS와 명시적인 트랜잭션 선언에 대한 의견  
"성능 문제가 정말 심각하지 않는 한 ATOMIC_REQUESTS를 이용하라. 대부분의 사이트에서는 그것만으로 충분할 것이다."

#### 트랜잭션 관련 가이드라인

- 데이터베이스에 변경이 생기지 않는 데이터베이스 작업은 트랜잭션으로 처리하지 않는다.
- 데이터베이스에 변경이 생기는 데이터베이스 작업은 반드시 트랜잭션으로 처리한다.
- 데이터베이스 읽기 작업을 수반하는 데이터베이스 변경 작업 또는 데이터베이스 성능에 관련된 특별한 경우에는 앞의 두 가이드라인을 모두 고려한다.

목적 | ORM 메서드 | 트랜잭션을 이용할 것인가?
---|---|---
데이터 생성 | `.create()`, `bulk_create()`, `get_or_create()` | y
데이터 가져오기 | `.get()`, `.filter()`, `count()`, `iterate()`, `exists()`, `.exclude()`, `.in_bulk` 등 |
데이터 수정하기 | `.update()` | y
데이터 지우기 | `.delete()` | y

![]({{site.url}}/img/post/django/two_scoops/7.2.png)
> 데이터베이스는 정말 아이스크림을 좋아한다.

> #### 독립적인 ORM 메서드 호출을 트랜잭션 처리하지 말자  
장고의 ORM은 데이터의 일관성을 위해 내부적으로 트랜잭션을 이용하고 있다. 예를 들어 접합 상속(concrete inheritance)으로 인해 업데이트(update)가 여러 테이블에 걸쳐 영향을 준다고 할 때 장고는 이를 트랜잭션으로 처리한다.  
따라서 독립적인 ORM 메서드 [.create(), .update(), .delete()]를 트랜잭션으로 처리하는 것은 그다지 유용하지 않다. 대신 여러 ORM 메서드들을 뷰나 함수 또는 메서드 내에서 호출할 때 트랜잭션을 이용하면 된다.

### 7.7.3 django.http.StreamingHttpResponse와 트랜잭션
뷰가 django.http.StreamingHttpResponse를 반환한다면 일단 응답(response)이 시작된 이상 트랜잭션 에러를 중간에 처리하기는 불가능하다. 프로젝트에서 이 응답 메서드가 쓰이고 있다면 ATOMIC_REQUESTS가 다음 중 하나를 따라야 한다.

1. ATOMIC_REQUESTS의 장고 기본값을 False로 설정한다. 그리고 나서 7.7.2 에 있는 기술들을 고려한다.
2. 뷰를 django.db.transaction.non_atomic_requests 데코레이터로 감싸 본다.

ATOMIC_REQUESTS를 스트리밍 응답과 같이 사용할 수 있지만, 트랜잭션은 뷰에서만 적용할 수 있다. 스트림 응답이 추가적인 SQL 쿼리를 생성했다면 오토커밋 모드일 것이다. 생성된 응답이 데이터베이스에 무언가 쓰는 일은 할 수 없다.

### 7.7.4 MySQL에서의 트랜잭션
MySQL 데이터베이스를 이용한다면 데이터베이스 타입이 InnoDB 혹은 MyISAM 이냐에 따라 트랜잭션이 지원될 수도 있고 안 될 수도 있다. 트랜잭션이 지원되지 않는다면 ATOMIC_REQUESTS나 트랜잭션을 지원하도록 쓰인 코드에 상관없이 늘 오토커밋 모드로 작동하게 된다.  
참고 정보  
<http://2scoops.co/1.8-transactions-in-mysql>  
<http://dev.mysql.com/doc/refman/5.0/en/sql-syntax-transactions.html>

### 7.7.5 장고 ORM 트랜잭션 관련 자료

- 장고 문서의 트랜잭션 부분 : <https://docs.djangoproject.com/en/1.8/topics/db/transactions/>  
- Real Python에서 트랜잭션에 대한 주제로 좋은 튜토리얼을 제공하고 있다. : <https://realpython.com/blog/python/transaction-management-with-django-1-6/>

## 7.8 요약
프로젝트 데이터를 쿼리하는 여러 방법을 다루었다. 어떻게 데이터를 저장하는지 알았으니 이 데이터를 어떻게 나타내 보이는지 알아야 한다.
