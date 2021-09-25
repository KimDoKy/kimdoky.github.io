---
layout: post
section-type: post
title: Two Scoops of django 3.x - Chap6. Model Best Practices
category: django
tags: [ 'django' ]
---

> [Two Scoops of Django 3.x](https://www.feldroy.com/books/two-scoops-of-django-3-x)

---

모델은 장고 프로젝트의 토대가 되는 부분이기 때문에, 새 모델을 추가하거나 기존 모델을 수정해야 할 때는, 한 번 더 깊이 생각하고 프로젝트의 토대를 탄탄하고 안전하게 다질 수 있는 방향의 디자인을 고려해야 합니다.

### 유용한 모델 관련 패키지들

- `django-model-utils`: TimeStampedModel 같은 일반적인 패턴들 처리하는데 유용
- `django-extensions`: 모든 앱에 모델 클래스를 자동으로 로드해 주는 `shell_plus`라는 명령을 제공. 너무 많은 기능이 있다는 것이 단점

## 6.1 Basics

### 6.1.1 Break Up Apps with Too Many Models

하나의 앱에 모델이 20+ 이라면 작은 앱으로 나눠야 합니다.
5개 이하를 추천합니다.

### 6.1.2 Be Careful With Model Inheritance

Django는 3가지 모델 상속 방법을 제공합니다.

1. 추상화 기초 클래스(abstract base classes)
2. 멀티테이블 상속(multi-table inheritance)
3. 프락시 모델(proxy-model)

모델 상속 스타일 | 장점 | 단점
---|---|---
상속X<br/>공통 필드가 있다면 모두 해당 필드를 선언 | Django 모델을 이해하기 쉬움 | 중복되는 테이블이 많아지면 관리하기 어려움
추상화 기초 클래스<br/>상속받은 모델만 테이블이 생성 | 추가 테이블 생성 없음<br/>테이블 조인으로 인한 성능 저하 없음 | 부모 클래스를 독립적으로 이용 불가
멀티테이블 상속<br/>OneToOneField | 부모 or 자식 모델 어디든 쿼리를 할 수 있음 | 자식 테이블에 대한 각 쿼리에 대해 부모 테이블과 조인이 필요하여 부하가 발생<br/>비추
프락시 모델<br/>원래 모델에 대해서만 테이블 생성 | 각기 다른 파이썬 작용을 하는 모델들의 별칭을 가질 수 있음 | 모델의 필드 변경 불가

- 모델들 사이에 중복되는 필드가 최소(1~2개)라면, 모델 상속보다는 각각 구현하면 된다.
- 모델들 사이에 중복된 필드가 많다면, 추상화 기초 모델로 리팩터링할 수 있다.
- 프락시 모델은 편리하지만, 다른 2가지 모델 상속 방식과는 다르게 동작하므로 주의해야 한다.
- 멀티테이블 상속은 혼란과 상단한 부하를 일으키므로 반드시 피해야 한다. 대신 `OneToOneField`이나 `ForeignKeys`를 이용하여 조인을 좀 더 수월하게 컨트롤할 수 있다.

### 6.1.3 Model Inheritance in Practice: The TimeStampedModel

Django의 모든 모델은 `created`와 `modified` 타임스탬프 필드를 생성해 두는 것이 일반적이지만, 매번 작업하기엔 비효율적입니다. 이를 위해 `TimeStampedModel`을 만들어 자동으로 필드를 추가하게 할 수 있습니다.

```python
# core/models.py
form django.db import models

class TimeStampedModel(Models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
```

```python
# flavors/models.py
from django.db import models
from core.models import TimeStampedModel

class Flavor(TimeStampedModel):
    title = models.CharField(max_length=200)
```

`TimeStampedModel`을 상속 받음으로써 자동으로 두 필드를 추가 할 수 있습니다.(추상화 기초 클래스 상속 패턴)

## 6.2 Database Migrations

### 6.2.1 Tips for Creating Migrations

- 새로운 앱이나 모델이 생성되면 `django.db.migrations`를 실행한다. (`$ python manage.py makemigrations`)
- 생성된 마이그레이션을 실행하기 전에 꼼꼼히 체크해야 한다. `sqlmigrate`를 통해 SQL 문을 확인할 수 있다.
- `django.db.migrations` 스타일로 이루어 지지 않은 외부 앱에 대한 마이그레이션은 `MIGRATION_MODULES` 세팅을 이용한다.
- 생성되는 마이그레이션 개수는 상관없지만, 신경쓰인다면 `squashmigrations`를 이용한다.
- 마이그레이션 실행 전에는 반드시 백업해라.

### 6.2.2 Adding Python Functions and Custom SQL to Migrations

- [RunPython](https://docs.djangoproject.com/en/3.2/ref/migration-operations/#runpython)
- [RunSQL](https://docs.djangoproject.com/en/3.2/ref/migration-operations/#runsql)

## 6.3 Overcoming Common Obstracles of RunPython

### 6.3.1 Getting Access to a Custom Model Manager's Methods

- 모델 매니저 메서드로 filter, exclude, create, modify를 동작해야 할 경우
- django.db.migrations는 이러한 구성 요소를 제외함
- `use_in_migrations = True` 플래그를 지정하여 기본 구성 요소를 무시할 수 있습니다.
- [django doc](https://docs.djangoproject.com/en/3.2/topics/migrations/#model-managers)

```python
class MyManager(models.Manager):
    use_in_migrations = True

class MyModel(models.Model):
    objects = MyManager()
```

### 6.3.2 Getting Access to a Custom Model Method

- django.db.migrations가 모델을 직렬화하는 방법때문에 이 제한을 우회할 수 없습니다.
- 마이그레이션 중에는 커스텀 메서드를 호출할 수 없습니다.
- [django doc](https://docs.djangoproject.com/en/3.2/topics/migrations/#historical-models)

### 6.3.3 Use RunPython.noop to Do Nothing

- 역마이그레이션이 작동하려면 `reserse_code` 호출이 가능해야 합니다.
- ex) 기존 데이터를 새로 추가된 필드와 결합하는 경우

```python
from django.db import migrations, models

def add_cones(apps, schema_editor):
    Scoop = apps.get_model('scoop', 'Scoop')
    Cone = apps.get_model('cone', 'Cone')

    for scoop in Scoop.objects.all():
        Cone.objects.create(
            scoop=scoop,
            style='sugar'
        )

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('scoop', '0051_auto_20670724'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cone',
            fields=[
                ('id', models.AutoField(auto_created=True,
                    primary_key=True,
                    serialize=False, verbose_name='ID')),
                ('style', models.CharField(max_length=10),
                    choices=[('sugar', 'Sugar'), ('waffle', 'Waffle')]),
                ('scoop', models.OneToOneField(
                    null=True, to='scoop.Scoop', 
                    on_delete=django.db.models.deletion.SET_NULL)),
                ], 
            ),

        # RunPython.noop는 역마이그레이션 발생만 허용
        migrations.RunPython(add_cones, migrations.RunPython.noop)
    ]
```

### 6.3.4 Deployment and Management of Migrations

- 배포 전에 rollback 할 수 있는지 확인하자.
- 테이블의 수가 많다면 스테이징 서버에 비슷한 크기의 데이터로 충분히 테스트하자.
- MySQL을 이용한다면
  - 스키마 변환 전에 반드시 데이터베이스를 백업하자. MySQL은 스키마 변경에 대한 트랜잭션을 지원하지 않는다(롤백 불가)
  - 가능하다면 데이터베이스 변환 전에 프로젝트를 '읽기 전용 모드'로 변경한다.
  - 테이블의 크기가 크다면 오랜 시간이 걸릴 수도 있다.

  > '읽기 전용 모드'에 대해 추가 학습 필요

## 6.4 Django Model Design

### 6.4.1 Start Normalized

- [Database normalization](https://en.wikipedia.org/wiki/Database_normalization)
- [Relational Database Design/Normalization](https://en.wikibooks.org/wiki/Relational_Database_Design/Normalization)

### 6.4.2 Cache Before Denormalizing

적절한 위치에 캐시를 세팅하면, 모델을 비정구화할 때 발생하는 문제점을 상단 부붕 해소시켜주기도 합니다. [Chapter 26: Finding and Reducing Bottlenecks]()에서 자세히 다룰 예정

### 6.4.3 Denormalize Only if Absolutely Needed

비정규화는 반드시 필요할 때만 사용해야 합니다. 정규화에 익숙해져야 합니다.
비정규화를 하기 전에 캐시에 대해 더 고민해봐야 합니다.
캐시로 해결할 수 없을 때 비정규화 도입을 생각해 볼 수 있습니다.

### 6.4.4 When to Use Null and Blank

- 기본값은 False

필드 타입 | null=True | blank=True
---|---|---
CharField,<br/>TextField,<br/>SlugField,<br/>EmailField,<br/>CommaSeparatedIntegerField,<br/>UUIDField | `unique=True`, `blank=True`인 경우에는 okay | 위젯이 빈 값을 허용하도록 하려면 Okay.<br/>DB에는 빈 문자열로 저장됨
FileField,<br/>ImageField | X<br/>`MEDIA_ROOT`의 경로를 CharField에 파일 or 이미지를 저장함 | Okay.<br/>CharField에 적용된 것과 같은 규칙 적용
BooleanField | Okey | 기본값 `True`
IntegerField,<br/>FloatField,<br/>DecimalField,<br/>DurationField,<br/>etc | 해당 값이 DB에 NULL로 들어가도 문제가 없다면 Okay | 위젯에서 해당값이 빈값을 받아도 된다면 Okay<br/>`null=True`도 같이 사용해야 함
DateTimeField,<br/>DateField,<br/>TimeField,<br/>etc | DB에 해당 값들을 NULL로 설정할 수 있다면 Okay | 위젯에 빈 값을 받아도 상관 없거나, `auto_now`나 `auto_now_add`를 사용한다면 Okay<br/>`null=True`도 같이 사용해야 함
ForeignKey,<br/>OneToOneField | DB에 해당 값들을 NULL로 설정할 수 있다면 Okay | 위젯에서 해당값(ex.셀렉트박스)이 빈 값이어도 되면 Okay
ManyToManyField | X | 위젯에 해당값(ex.셀렉트박스)이 빈 값이어도 되면 Okay
GenericIPAddressField | DB에 해당값들을 NULL로 설정할 수 있다면 Okay | 위젯에 해당값이 빈 값이어도 괜찮다면 Okay
JSONField | Okay | Okay

### 6.4.5 When to Use BinaryField

- raw binary data 나 byte를 저장하는 필드입니다.
- filter, exclude, other SQL action이 적용되지 않습니다.

다음과 같은 경우에 사용할 수 있습니다.

- 메시지팩 형식의 콘텐츠
- 원본 센서 데이터
- 압축된 데이터

사용하기 나름이지만, 바이너리 데이터는 크기가 방대할 수도 있기 때문에 DB가 느려질 수 있습니다.
이런 경우 바이너리 데이터 저장이 병목 지점이 된다면 해당 데이터를 파일 형태로 저장하고 FileField에 레퍼런스하는 방식으로 해결할 수 있습니다.

#### BinaryField으로부터 파일을 직접 서비스는 금지!

- 데이터베이스의 '읽기/쓰기' 속도는 파일 시스템의 '읽기/쓰기' 속도보다 느리다.
- 데이터베이스 백업에 드는 공간과 시간이 점점 증가한다.
- 파일 자체에 접근하는 앱(장고) 레이어와 데이터베이스 레이어 둘다 거쳐야 한다.
- 자세한 내용은 [Three things you should never put in your database](https://www.revsys.com/tidbits/three-things-you-should-never-put-your-database/) 참고

### 6.4.6 Try to Avoid Using Generic Relations

- 범용 관계(generic relations): 한 테이블로부터 다른 테이블을 서로 제약 조건이 없는 외부 키(unconstrained foreign key, GenericForeignKey)로 바인딩하는 것이다.

#### 문제점

- 모델 간의 인덱싱이 존재하지 않으면 쿼리 속도에 손해를 가져오게 된다.
- 다른 테이블에 존재하지 않는 레코드를 참조할 수 있는 데이터 충돌의 위험성이 존재한다.

#### 장점

- 기존에 만들어 놓은 여러 모델 타입과 상호 작업하는 앱을 새로 제작시 수월함

#### 범용 관계 정리

- 범용관게와 GenericForeignKey 이용은 피하자.
- 범용관계가 필요하다면, 모델 디자인을 바꾸거나 새로운 PostgreSQL 필드로 해결할 수 있는지 확인하자.
- 이용해야만 한다면 서드파티 앱을 고려하자.
- [Avoid Django's GenericForeignKey](https://lukeplant.me.uk/blog/posts/avoid-django-genericforeignkey/) 참고

### 6.4.7 Make Choices and Sub-Choices Model Constants

- 선택 항목을 튜플로 정의된 구조로 모델에 속성을 추가
- [django doc](https://docs.djangoproject.com/en/3.2/ref/models/fields/#django.db.models.Field.choices)

### 6.4.8 Using Enumeration Types for Choices

- django 3.0 부터 기본 내장

```python
from django.db import models

class IceCreamOrder(models.Model): 
    class Flavors(models.TextChoices):
           CHOCOLATE = 'ch', 'Chocolate'
           VANILLA = 'vn', 'Vanilla'
           STRAWBERRY = 'st', 'Strawberry'
           CHUNKY_MUNKY = 'cm', 'Chunky Munky'

   flavor = models.CharField(
       max_length=2,
       choices=Flavors.choices
   )
```

- 단점
  - Named group은 열겨형으루 사용 불가
  - str, int 이외의 유형은 직접 정의 필요

### 6.4.9 PostgreSQL-Specific Fields: When to Use Null and Blank

필드 타입 | null=True | blank=True
---|---|---
ArrayField | Okay | Okay
HStoreField | Okay | Okay
IntegerRangeField,<br/>BigIntegerRangeField,<br/>FloatRangeField | DB에 해당 값들을 NULL로 설정할 수 있다면 Okay | 위젯에서 해당 값이 빈값을 허용하기 원한다면 `null=True`와 함께 사용
DatetimeRangeField,<br/>DateRangeField | DB에 해당 값들을 NULL로 설정할 수 있다면 Okay | 위젯에서 해당 값에 빈값을 허용하길 원하거나 `auto_now`나 `auto_now_add`를 이용한다면 `null=True`와 함께 사용

## 6.5 The Model `_meta` API

- `_meta`의 본 목적: 모델에 대한 부가적인 정보를 장고 내부적으로 이용
  - 모델 필드의 리스트를 가져올 때
  - 모델의 특정 필드의 클래스를 가져올 때(또는 상속 관계나 상속 등을 통해 생성된 정보를 가져올 때)
  - 추후 장고 버전들에서 이러한 정보를 어떻게 가져오게 되었는지 확실하게 상수로 남기기 원할 때
  - 장고 모델의 자체 검사 도구
  - 라이브러리를 이용해서 특별하게 커스터마이징된 자신만의 장고를 만들 때
  - 장고의 모델 데이터를 조정하거나 변경할 수 있는 일종의 관리 도구를 제작할 때
  - 시각화 또는 분석 라이브러리를 제작할 때
  - [django doc](https://docs.djangoproject.com/en/3.2/ref/models/meta/)

## 6.6 Model Managers

- [django doc](https://docs.djangoproject.com/en/3.2/topics/db/managers/)

모델에 질의를 하면 장고 ORM은 **모델 매니저**(데이터베이스와 연동되는 인터페이스)를 호출합니다. 모델 매니저는 모든 클래스(테이블 안의 모든 데이터)의 모든 인스턴스 세트로 작동합니다.

#### 사용 예

```python
from django.db import models
from django.utils import timezone

class PublishedManager(models.Manager):

	use_for_related_fields = True

	def published(self, **kwargs):
		return self.filter(pub_date__lte=timezone.now(), **kwargs)


class FlavorReview(models.Model):
	review = models.CharField(max_length=255)
	pub_date = models.DateTimeField()

	# 커스텀 모델 매니저를 추가
	objects = PublishedManager()
```

```python
>>> from reviews.models import FlavorReview
>>> FlavorReview.objects.count()
35
>>> FlavorReview.objects.published().count()
31
```

#### 주의점

- 모델을 상속받아 이용시 추상화 기초 클래스들의 자식들은 부모 모델의 모델 매니저를 받고, 접합 기반 클래스는 그렇지 않다.
- 모델 클래스에 적용되는 첫 번째 매니저는 장고가 기본값으로 취급하는 매니저이다. 이것은 파이썬의 일반적인 패턴을 무시하는 것으로 QuerySet의 결과를 예상할 수 없게 한다.

## 6.7 Understanding Fat Models

- Fat Model: 데이터 관련 코드를 뷰나 템플릿이 아닌 모델 메서드, 클래스 메서드, 프로퍼티, 매니저 메서드 안에 넣어 캡슐화하는 것
- 단점
  - 모델 코드의 크기가 **신의 객체**(god object) 수준으로 증가됨
  - 어마어마한 코드의 크기와 복잡성으로 이해하기 어렵고, 테스트나 유지보수 난이도 대폭 상승
- 객체 지향 언어의 아이디어를 염두해두고 로직들을 이전해야 합니다.
  - 메서드들과 클래스 메서드, 프로퍼티는 유지하고, 그 안의 로직들을 모델 행동(model behavior)이나 헬퍼 함수(stateless helper function)으로 이전한다.

### 6.7.1 Model Behaviors a.k.a Mixins

- 모델 행동은 믹스인을 통한 캡슐화와 구성화의 개념으로 이루어졌습니다.  
- 모델을 추상화 모델로부터 로직들을 상속받습니다.  
- [Kevin Stone Blog](https://blog.kevinastone.com/django-model-behaviors)
- [Section 10.2: Using Mixins With CBVs]()

### 6.7.2 Stateless Helper Functions

- 유틸리티 함수로 모델의 로직을 분리
- 장점: 로직에 대한 테스트가 수월해짐
- 단점: 상태가 없기 때문에 함수에 더 많은 인자가 필요하다.
- [Chapter 31: What About Those Random Utilities?]()

### 6.7.3 Model Behaviors vs Helper Functions

위 두 방법은 완벽하진 않지만, 충분히 도움이 되는 방법들입니다.

## 6.8 Additional Resources

- 모델은 장고 프로젝트의 기초로써, 신중히 디자인해야 합니다.
- 정규화 및 다른 방법을 고려하고, 최후 수단으로 비정규화를 도입해야 합니다.
- raw Query로 느리고 복잡한 쿼리를 해결할 수도 있습니다.
- 적절한 장소에 캐시를 사용하여 성능 이슈를 해결할 수도 있습니다.
- 인덱스를 사용하세요.
- 모델 간의 상속은 '추상화 기초 클래스'를 사용하세요.
- `null=True`, `blank=True` 옵션 사용시 주의하세요.
- `django-model-utils`, `django-extensions`를 활용해도 좋습니다.
- 거대 모델의 단점을 주의하세요.
