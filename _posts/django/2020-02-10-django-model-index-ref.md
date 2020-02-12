---
layout: post
section-type: post
title: django - Model index reference
category: django
tags: [ 'django' ]
---

> [Django Model index ref](https://docs.djangoproject.com/en/2.2/ref/models/indexes/)  

---

인덱스 클래스는 DB 인덱스를 쉽게 만들 수 있습니다. `Meta.indexes` 옵션을 사용하여 추가할 수 있습니다.

> 인덱스는 'django.db.models.indexes'에 정의되어 있지만 편의상 'django.db.models'으로 가져옵니다. 표준 규칙은 'from django.db import models'을 사용하고 인덱스를 'models.<IndexClass>'를 참조합니다.

## Index options

```python
class Index(fields=(), name=None, db_tablespace=None, opclasses=(), condition=None)
```

DB에 index(B-Tree)을 작성합니다.

### `fields`

index가 필요한 필드 이름의 리스트나 튜플.  

기본적으로 인덱스는 각 열에 대해 오름차순으로 생성됩니다. 내림차순으로 정의하려면 앞에 하이픈을 추가하세요.

### `name`

인덱스의 이름입니다. name이 제공되지 않으면 Django는 이름을 자동생성합니다.  
다른 DB의 호환성을 위해 30자 미만으로 제한되며 숫자(0-9)나 언더스코어(`_`)로 시작하면 안됩니다.

> abstract base classes의 부분 indexes
인덱스의 이름은 언제나 고유한 이름으로 지정해야 합니다. Meta.indexes 옵션은 속성(name 포함)에 대한 값이 동일한 하위 클래스에 상속되므로, 추상 기본 클래스에 부분 인덱스를 지정할 수 없습니다. 대신 각 인덱스에 고유한 이름을 지정하여 하위 클래스에 직접 인덱스 옵션을 지정할 수 있습니다.

### `db_tablespace`

인덱스에 사용할 DB 테이블 스페이스의 이름입니다. 단일 필드 인덱스의 경우 `db_tablespace`가 제공되지 않는다면 필드의 `db_tablespace`에 인덱스가 생성됩니다.  

`Field.db_tablespace`가 지정되지 않은 경우(혹은 인덱스가 여러 필드를 사용하는 경우), 모델의 메타 클래스 안에 `db_tablespace` 옵션에 지정된 테이블스페이스에 인덱스가 생성됩니다.  

테이블 스페이스가 설정되지 않은 경우, 인덱스는 테이블과 동일한 테이블 스페이스에 생성됩니다.  

### `opclasses`

인덱스에 사용할 PostgreSQL 연산자 클래스의 이름입니다. 사용자 정의 연산자 클래스가 필요한 경우 인덱스의 각 필드마다 하나씩 제공해야 합니다.  

예를 들어 `GinIndex(name='json_index', fields=['jsonfield'], opclasses=['jsonb_path_ops'])`는 `jsonb_path_ops`를 사용하여 jsonfield에 gin 인덱스를 만듭니다.  

`opclasses`는 PostgreSQL에서만 사용됩니다.  
`opclasses`를 사용할 때는 'Index.name'이 필요합니다.

### `condition`

테이블이 매우 크고, 쿼리가 주로 행의 하위 집합을 대상으로 하는 경우, 인덱스를 해당 하위 집합으로 제한하는 것이 유용합니다. 조건을 `Q`로 지정하세요.  

예를 들어, `condition=Q(pages__gt=400)`는 400 페이지가 넘는 레코드를 인덱스화합니다.  

`condition`은 'Index.name'이 필요합니다.

> PostgreSQL에 대한 제한  
PostgreSQL는 condition 안에서 참조된 함수를 IMMUTABLE로 표시하도록 요구합니다. Django는 이걸 검증하지 않지만, PostgreSQL는 오류를 발생시킵니다.  
이건 Date functions과 Concat과 같은 기능은 받아들여지지 않는다는 것을 의미합니다.  
DateTimeField에 날짜를 지정하는 경우, datetime 객체와의 비교는 tzinfo 인수를 제공해야 합니다.

> MySQL과 MariaDB
condition 인덱스를 지원하지 않기 때문에 MySQL과 MariaDB에서는 무시됩니다.
