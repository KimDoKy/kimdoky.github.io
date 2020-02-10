---
layout: post
section-type: post
title: django - Model Meta options
category: django
tags: [ 'django' ]
---

> [Django Model Meta options](https://docs.djangoproject.com/en/2.2/ref/models/options/)  

---

# Meta options

### `abstract`

`abstract=True`이면 해당 모델을 추상 기본 클래스가 됩니다.

### `app_label`

모델이 `INSTALLED_APPS`에서 앱 외부에 정의된 경우, 모델이 속한 앱을 선언해야 합니다.

```python
app_label = 'myapp'
```

### `base_manager_name`

모델의 `_base_manager`에 사용할 매니저의 이름 속성을 지정합니다.(`objects`가 기본값)

기본적으로 `django.db.models`에 지정된 매니저를 재지정할때 사용합니다.  
기본 매니저가 적합하지 않은 경우에 사용합니다.

### `db_table`

Django는 모델 클래스이름과 해당 클래스가 포함된 앱이름을 기준으로 DB 테이블 이름을 자동으로 생성합니다.  

예를 들어, 'bookstore'라는 앱에 'Book' 모델이 정의되면, 'bookstore_book'으로 DB 테이블 이름을 정합니다.  

`db_table`으로 DB 테이블 이름을 지정할 수 있습니다.

```python
db_table = 'music_ablbum'
```

MySQL 백엔드의 경우 테이블 이름은 소문자로 지정해야 합니다.  
Oracle은 테이블 이름에 30자 제한이 있습니다.

### `db_tablespace`

- [테이블 스페이스?](http://www.dbguide.net/db.db?cmd=view&boardUid=26445&boardConfigUid=9&boardIdx=21&boardStep=1)

DB 테이블 스페이스명을 지정합니다. 기본값은 프로젝트의 `DEFAULT_TABLESPACE`입니다. 백엔드가 테이블 스페이스를 지원하지 않으면 무시됩니다.

### `default_manager_name`

모델의 `_default_manager`에 사용할 매니저의 이름을 지정합니다.

모델에 여러 모델 매니저가 있고, 기본 관리자를 지정해야 하는 경우에 사용합니다.  

### `default_related_name`

필드의 역관계 이름은 유일해야 합니다. 기본적으로 `<model_name>_set`으로 지정됩니다.  

### `get_latest_by`

매니저의 `latest()`, `earliest()` 메소드에서 사용할 기본 필드를 지정합니다.

```python
# Latest by ascending order_date.
get_latest_by = "order_date"

# Latest by priority descending, order_date ascending.
get_latest_by = ['-priority', 'order_date']
```

### `managed`

기본값은 True으로, Django는 마이그레이션 혹은 마이그레이션의 일부로 DB 테이블을 생성하고 flush 관리 명령으로 제거합니다. 즉, DB 테이블의 수명주기를 관리합니다.

만약 False라면, 이 모델의 DB에 대해 테이블 작석이나 삭제를 수행하지 않습니다.  
이는 모델이 다른 방법으로 작성된 테이블이나 DB 뷰를 작성할 경우에 유용합니다. 그외의 모델 처리는 기존과 동일합니다.  

- 기본 키 필드를 자동으로 선언하지 않으면, 모델링 중인 DB 테이블의 모든 열을 지정하는 것이 좋습니다.
- ManyToManyField를 사용하고 있다면 하나의 관리 모델과 하나의 비관리 모델 사이의 중간 테이블이 생성되지만, 조인이 되지는 않습니다. 이 기본 동작을 변경하려면 중간 테이블을 명시적으로 모델로 작성하고 ManyToManyField.through 속성으로 연결해야 합니다.
- 테스트의 경우 올바른 테이블을 작성해야 합니다.

### `order_with_respect_to`

주어진 필드(보통 ForeignKey)과 관련해서 객체를 정렬 할 수 있게 합니다.

```python
# Question에 둘 이상의 Answer이 있고, 답변 순서가 중요한 경우
from django.db import models

class Question(models.Model):
    text = models.TextField()
    # ...

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # ...

    class Meta:
        order_with_respect_to = 'question'
```

`order_with_respect_to`를 설정하면 두 개의 추가 메서드(`get_RELATED_order()`, `set_RELATED_order()`)가 제공됩니다. REKATED는 소문자로 된 모델 이름입니다.

```python
# Question 객체에 여러 개의 Answer 관련 객체가 있다면
# 반환된 목록에는 Answer 관련 객체의 기본 키가 포함됩니다.
>>> question = Question.objects.get(id=1)
>>> question.get_answer_order()
[1, 2, 3]

# Answer 기본 키 리스트를 전달하여 Question 객체의 Answer 관련 객체의 순서를 설정할 수 있습니다.
>>> question.set_answer_order([3, 1, 2])


# 관련 객체는 get_next_in_order(), get_previous_in_order()를 가져온다.
# 이 메서드는 적절한 순서로 객체에 액세스할 때 사용합니다.
# Answer 객체는 id로 정렬되었다고 가정
>>> answer = Answer.objects.get(id=2)
>>> answer.get_next_in_order()
<Answer: 3>
>>> answer.get_previous_in_order()
<Answer: 1>
```

`order_with_respect_to`와 `ordering`은 함께 사용할 수 없고, 이 모델의 객체 리스트를 얻을때마다 `order_with_respect_to`가 적용됩니다.  

`order_with_respect_to`는 새 DB 열을 추가하기 때문에 추가하거나 변경하려면 마이그레이션을 수행하고 적용해야 합니다.

### `ordering`

객체 리스트를 가져올때 사용하기 위한 기본 순서를 지정합니다.  

```python
# pug_date 역순으로 정렬
ordering = ['-pub_date']

# 무작위 정렬
ordering = ['?']

# pub_date를 내림차순으로 정렬한 후, author를 오름차순으로 정렬
ordering = ['-pub_date', 'author']

# 쿼리식도 사용가능
# author을 오름차순으로 정렬하고 null 값을 마지막으로 정렬
ordering = [F('author').asc(nulls_last=True)]
```

ordering은 DB 비용이 발생합니다. 추가한 외래키는 모든 기본 ordering도 암시적으로 포함됩니다.

### `permissions`

이 객체를 생성할 때 permissions 테이블에 추가 권한을 생성합니다.  

각 모델은 add, change, delete, view permissions이 자동으로 생성됩니다.

```python
# can_deliver_pizzas라는 권한을 추가합니다.
# 형식 // (permission_code, permission_name)의 리스트나 튜플
permissions = [('can_deliver_pizzas', 'Can deliver pizzas')]
```

### `default_permissions`

기본 권한('add', 'change', 'delete', 'view') 권한을 수정합니다. 기본 권한이 필요 없는 경우 빈 리스트를 설정합니다.  

이 옵션은 모델이 마이그레이션을 하기 전에 해야합니다.

### `proxy`

`proxy = True`이면 다른 모델을 서브 클래싱하는 모델이 [프록시 모델](https://himanmengit.github.io/django/2018/02/09/DjangoModels-13-Proxy.html)로 처리됩니다.


### `required_db_features`

마이그레이션 단계에서 연결에 있어야하는 DB 기능 리스트입니다.  
예를 들어 `['gis_enabled']`으로 설정하면 모델은 GIS-enabled DB에서만 동기화됩니다.  

여러 DB 백엔드로 테스트할때 일부 모델을 건너뛸때도 유용합니다.

### `required_db_vendor`

이 모델이 지원하는 DB 업체의 이름입니다. 현재는 'sqlite', 'postgresql', 'mysql' 혹은 'oracle'입니다. 이 속성이 현재 연결 업체와 일치하지 않으면 모델은 동기화되지 않습니다.

### `select_on_save`

Django 1.6 이전의 `django.db.models.Model.save()` 알고리즘의 사용 여부를 결정합니다. 기존의 알고리즘은 SELECT를 사용하여 업데이트할 기존 행이 있는지 확인합니다. 새로운 알고리즘은 UPDATE를 직접 시도합니다. 간혹 기존 행의 업데이트가 Django에 표시되지 않습니다.  

예로 NULL을 반환하는 PostgreSQL 'ON UPDATE'라는 트리거가 있는데, 새 알고리즘은 DB에 행이 존재하더라고 INSERT를 수행합니다.  

기본값은 False이고 일반적으로 이 속성은 설정할 필요가 없습니다.  

### `indexes`

모델에서 정의하려는 필드의 색인 리스트

```python
from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
            models.Index(fields=['first_name'], name='first_name_idx'),
        ]
```

### `unique_together`

함께 사용되는 필드 이름 셋은 고유해야합니다.

```python
unique_together = [['driver', 'restaurant']]

# 편의상 단일 리스트도 가능합니다.
unique_together = ['driver', 'restaurant']
```

Django admin에서 사용되며, DB 수준에서 적용됩니다. (적절한 UNIQUE 문이 CREATE TABLE 문에 포함됨)  

ManyToManyField는 `unique_together`에 포함될 수 없습니다.  
제약 조건을 위반하면 'ValidationError'가 발생합니다.

### `index_together`

함께 색인 될 필드 이름 셋

```python
index_together = [["pub_date", "deadline"]]

# 편의상 이렇게도 가능
index_together = ["pub_date", "deadline"]
```

이 필드 리스트는 함께 색인됩니다.(적절한 CREATE INDEX 문이 실행됩니다.)

### `constraints`

모델에서 정의하려는 제약 조건 리스트

```python
from django.db import models

class Customer(models.Model):
    age = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(age__gte=18), name='age_gte_18'),
        ]
```

### `verbose_name`

사람이 읽기 쉽게 이름을 지정합니다. (어드민에서)

```python
verbose_name = "pizza"
```

`verbose_name`을 지정하지 않으면 Django는 CamelCase로 이름을 지정합니다.

### `verbose_name_plural`

`verbose_name`의 복수형

```python
verbose_name_plural = "stories"
```

`verbose_name_plural`을 지정하지 않으면 Django는 `verbose_name` + 's'을 사용합니다.

## Read-only Meta attributes

### `label`

객체의 표현은 `app_label.object_name`을 반환합니다. (ex. 'polls.Question')

### `label_lower`

모델을 나타내는 `app_label.model_name`을 반환합니다.(ex. 'polls.question')
