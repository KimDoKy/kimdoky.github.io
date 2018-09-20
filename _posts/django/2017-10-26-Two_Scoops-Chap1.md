---
layout: post
section-type: post
title: Two Scoops of Django - chap1. 코딩 스타일
category: django
tags: [ 'django' ]
published: false
---

## 1.1 읽기 쉬운 코드를 만드는 것이 왜 중요한가

- 축약적이거나 함축적인 변수명은 피한다.
- 함수 인자의 이름들은 꼭 써 준다.
- 클래스와 메서드를 문서화한다.
- 코드에 주석은 꼭 달도록 한다.
- 재사용 가능한 함수 또는 메서드 안에서 반복되는 코드들은 리펙터링을 해둔다.
- 함수와 메서드는 가능한 한 작은 크기를 유지한다. 어림잡아 스크롤 없이 읽을 수 있는 길이가 적합하다.

이러한 절차들의 궁극적인 목적은 한동안 잊고 지낸 코드라도 어느 순간 다시 봤을때 바로 얼마 전에 작업했던 것처럼 쉽고 빠르게 그 내용을 이해하기 위한 것이다.  

함축적이고 난해한 함수명은 피해야 한다. balance_sheet_decrease처럼 그 의미가 설명이 되는 함수 이름이 bal_s_d와 같이 함축적이고 난해하게 쓴 이름보다 이해하기 더 쉽다. 짧게 씀으로 몇 초 정도 타자 시간을 아낄 수 있을수도 있지만 결국 몇 시간 또는 몇 일을 허비하게 되늰 기술적 부채로 다가오게 될 것이다. 그런 기술적 부채를 미리 막을 수 있다면 변수명을 길게 풀어 쓰는 편이 충분히 가치 있는 일입니다.

## 1.2 PEP 8
PEP 8은 파이썬 공식 스타일 가이드다. <https://www.python.org/dev/peps/pep-0008/>  
PEP 8에선 다음과 같은 코딩 관례들을 다루고 있습니다.

- 들여쓰기에는 스페이스를 4칸 이용한다.
- 최상위 함수와 클래스 선언 사이를 구분 짓기 위해 두 줄을 띄운다.
- 클래스 안에서 메서드들을 나누기 위해 한 줄을 띄운다.

> **현재 프로젝트의 기존 관례를 함부로 바꾸지 않도록 한다.**  
PEP8 스타일은 새로운 프로젝트에서만 적용하기로 한다. 이미 PEP8이 아닌 다른 관례를 따르고 있는 기존 장고 프로젝트에 참여 중이라면 그냥 기존 관례를 따르도록 한다.  

### 1.2.1 79칼럼의 제약

"농담이 아니라 정말로 난 여전히 화면에 80칼럼 제약이 있는 콘솔에서 작업을 한다." - 베리 모리슨(Berry Morrison)

---
PEP8에 따르면 한 줄당 텍스트는 79글자를 넘어서는 안 된다. 이는 텍스트 줄바꿈 기능을 지원하는 텍스트 편집기나 많은 개발 팀에서 코드의 이해도를 떨어뜨리지 않는 수준의 줄 길이이기 때문이다.  

- 오픈 소스 프로젝트에서는 79칼럼 제약을 반드시 지킨다. 경험상 프로젝트의 기여자나 방문자들은 이 줄 길이 제약에 대해 끊임없이 불평할 것이다.
- 프라이빗 프로젝트에 한해서는 99칼럼까지 제약을 확장함으로써 요즘 나오는 모니터들의 장점을 좀 더 누릴 수 있다.

> **코드 줄 길이에 대한 애머릭 어거스틴의 견해**  
애머릭 어거스틴(장고 코어 개발자)는 다음과 같이 말했다. "79칼럼에 맞추려고 변수나 함수 또는 클래스 이름을 줄여서 짓는 것은 허용될 수 없다. 수십 년 전 하드웨어를 기준으로 만들어진 말도 안되는 숫자를 지키기보다는 읽기 쉽고 의미있는 변수명을 만드는 것이 더 중요한 일이다."

## 1.3 임포트에 대해
PEP8은 임포트(import)를 할 때 다음과 같은 순서로 그룹을 지을 것을 제안하고 있다.

1. 표준 라이브러리 임포트
2. 연관 외부 라이브러리 임포트
3. 로컬 애플리케이션 또는 라이브러리에 한정된 임포트

장고 프로젝트를 작성할 때 다음과 같은 순서로 임포트 문들을 구성한다.

```python
# 예제 1.1
# 표준 라이브러리 임포트
from __future__ import absolute_import
from math import sqrt
from os.path import abspath
# 코어 장고 임포트
from django.db import models
from django.utils.tranclation import ugettext_lazy as _
# 서드 파티 앱 임포트
from django_extensions.db.models import TimeStampeModel
# 프로젝트 앱 임포트
from splits.models import BananaSplit
# 임포트 문에 대해 주석을 달 필요는 없다.
```

장고 프로젝트에서 임포트 순서는 다음과 같다.

1. 표준 라이브러리 임포트
2. 코어 장고 임포트
3. 장고와 무관한 외부 앱 임포트
4. 프로젝트 앱 임포트

## 1.4 명시적 성격의 상대 임포트 이용하기
코드를 작성할 때 코드들을 다른 곳으로 이동시키거나 이름을 변경하거나 버전을 나누는 등의 재구성을 손쉽게 할 수 있도록 구성하는 것은 매우 중요한 일이다. 파이썬에서는 명시적 성격의 상대 임포트(explicit relative import)를 통해 모듈의 패키지를 하드 코딩하거나 구조적으로 종속된 모듈을 어렵게 분리해야 하는 경우들을 피해 갈 수 있다.  

#### 명시적 성격의 상대 임포트에 대한 쉬운 예
얼마나 많은 아이스크림을 먹었는지(와플콘, 슈가콘, 케이크콘 등 다양한 콘이 있다고 가정) 기록하는 장고 앱을 만들었다고 가정하고 그중 한 부분을 인용한다.  

불행히 다음 코드를 보면 하드 코딩된 임포트 문을 포함하고 있다. 물론 그다지 권하지 않는 방법이다.

```python
# 나쁜 예제 1.1
# cones/views.py
from django.views.generic import CreateViews
# 절대 따라 하지 말라!
# 'cones' 패키지에 하드 코딩된 암묵적 상대 임포트가 이용되었다.
from cones.models import WaffleCone
from cones.forms import WaffleConeForm
from core.views import FoodMixin
class WaffleConeCreateView(FoodMixin, CreateViews):
    model = WaffleCone
    form_class = WaffleConeForm
```

물론 '콘' 앱 자체는 아이스크림 프로젝트에서 문제 없이 잘 작동한다. 하지만 하드 코딩된 임포트 문들은 이식성 면에서 재사용성 면에서 문제가 된다.

- 얼마나 디저트를 먹었는지 기록하는 새로운 앱에서 '콘' 앱을 재사용하려 한다면 어떻게 해야겠는가? 이럴 경우 이름이 서로 충돌되어 이름을 변경해야하는 경우가 생긴다.(예를 들어 장고 앱에 'snow cone'이라는 이름의 디저트가 있을 경우가 되겠다.)
- 어떤 이유에서 앱의 이름을 바꾸어야 할 상황이 생겼을 때는 어떻게 해야 할까?

하드 코딩된 임포트 문을 이용했을 때 단지 앱의 이름을 바꿈으로써 모든 것이 해결되지 않는다. 단순히 이름을 바꾸는 것 이외에도 모든 임포트 문을 일일이 확인해서 해당 임포트 문을 수정해야 하는 번거로운 작업이 요구된다. 게다가 실제 프로젝트에서는 추가적인 유틸리티 모듈까지 잔뜩 딸려 오게 된다. 따라서 명시적 성격의 상대 임포트를 무심히 스쳐 보내서는 안되는 것이다.  

앞의 예를 명시적 성격의 상대 임포트를 이용한 예로 바꾼다.

```python
# 예제 1.2
# cones/views.py
from __future__ import absolute_import
from django.views.generic import CreateViews
# 'cones' 패키지 상대 임포트
from .models import WaffleCone
from .forms import WaffleConeForm
from core.views import FoodMixin
class WaffleConeCreateView(FoodMixin, CreateViews):
    model = WaffleCone
    form_class = WaffleConeForm
```

전역/외부 임포트에 대해 로컬/내부 임포트가 지니는 또 하나의 장점은 파이썬 패키지를 하나의 코드 유닛화할 수 있다는 것이다.

> #### 'from __future__ import absolute_import'를 이용하자.  
rom __future__ import absolute_import 문을 통해 이전 버전으로도 호환이 가능하다. 이를 통해 상대적인 임포트 문의 이용이 가능해지게 된다.

다음 표에서 각기 다른 파이썬 임포트 유형과 장고 프로젝트에서 언제 어떤 임포트를 이용할지 요약되어 있다.

코드 | 임포트 타입 | 용도
---|---|---
from core.views import FoodMixin | 절대 임포트 | 외부에서 임포트해서 현재 앱에서 이용할 때
from .models import WaffleCone | 명시적 상대 | 다른 모듈에서 임포트해서 현재 앱에서 이용할 때
from models import WaffleCone | 암묵적 상대 | 종종 다른 모듈에서 임포트해서 현재 앱에서 이용할 때 쓰지만 좋은 방법은 아니다.

표 1.1 임포트 : 절대 vs. 명시적 상대 vs. 암묵적 상대  

명시적 성격의 임포트를 이용하는 습관은 모든 개발자에게 좋은 습관이다.

## 1.5 import \*는 피하자.

```python
# 예제 1.3
from django import froms
from django.db import models
```

```python
# 나쁜 예제 1.2
# 안티 패턴: 절대 따라하지 말 것!
from django.forms import *
from django.db.models import *
```

위의 나쁜 예를 하면 안되는 이유는 다른 파이썬 모듈의 이름 공간들이 현재 작업하는 모듈의 이름공간에 추가로 로딩되거나 기존 것 위에 덮여 로딩되는 일을 막기 위해서이다. 이럴 경우 전혀 예상치 못한 상황이 발생하거나 심각할 경우 큰 재앙이 야기되기도 한다.  

앞의 나쁜 예를 보면, 장고 폼 라이브러리와 장고 모델 라이브러리 둘다 CharField를 가지고 있다. 이 두 라이브러리를 암묵적으로 로딩함으로써 모델 라이브러리가 폼 버전의 클래스를 덮어써 버린다. 이러한 현상은 파이썬 내장 라이브러리와 다른 서드 파티 라이브러리들의 중요한 기능들을 덮어쓰는 원인이 되기도 한다.

> #### 파이썬 이름 충돌  
같은 이름으로 두 개의 모듈을 임포트한다면 다음과 같은 문제에 봉착하게 된다.
```python
# 나쁜 예제 1.3
# 안티 패턴: 절대 따라하지 말 것!
from django.forms import CharField
from django.db.models import CharField
```

import \* 구문은 마치 아이스크림 가게에 아이스크림 콘 하나를 사러 와서 서른한가지 맛 전부를 무료로 맛보게 해달라는 염치없는 손님과 같다고 볼 수 있다. 한두 개 정도의 모듈만 이용하기 위해 전부 임포트 할 필요 없다.

![]({{site.url}}/img/post/django/two_scoops/1.1.png)
그림 1.1 아이스크림 가게에서 import * 으로 구매한다는 것

## 1.6 장고 코딩 스타일
장고 공식 가이드는 아니지만 일반적으로 널리 통용되는 코딩 스타일을 다룬다.

### 1.6.1 장고 코딩 스타일
장고는 내부적으로 PEP8을 확장한 장고만의 스타일 가이드라인을 가지고 있다.

- <https://docs.djangoproject.com/en/1.8/internals/contributing/writing-code/coding-style/>

이 내용응ㄴ 공식 표준에서는 논의되지 않았더라도 프로젝트를 진행하면서 마주치는 장고 커뮤니티의 여러 코드에서 일반적으로 통용되는 사항들이다.

### 1.6.2 URL 패턴 이름에는 대시(-) 대신 밑줄(\_)을 이용한다.
파이썬다울 뿐 아니라 통합 개발 환경과 텍스트 편집기에 최적화된 스타일입니다. 여기서 말하는 URL은 웹 브라우저에서 쓰는 URL 주속가 아니라 url() 인자로 쓰이는 이름을 이야기 한다.  

```python
# 나쁜 예제 1.4
patterns = [
    url(regex='^add/$', view=views.add_topping, name='add-topping')
]
```

url 이름을 밑줄이 이용된 바람직한 경우는 다음과 같다.

```python
# 예제 1.4
patterns = [
    url(regex='^add/$', view=views.add_topping, name='add_topping')
]
```

### 1.6.3 템플릿 블록 이름에 대시 대신 밑줄을 이용한다.
URL 패턴 이름에서 밑줄을 이용하는 것과 같은 이유로 템플릿 블록을 정의하는 이름을 만들 때도 밑줄을 사용한다. 좀 더 파이썬답고 좀 더 편집기에 최적화된 방법이다.

## 1.7 자바스크립트, HTML, CSS 스타일 선택하기

### 1.7.1 자바스크립트 스타일 가이드
파이썬과 달리 자바스크립트는 공식 스타일 가이드가 없다. 대신 개인과 회사 등에서 만들어 놓은 비공식 스타일이 다양하게 존재한다. 따라서 자신이 선호하는 것을 선택한 후에 이용하면 된다.  

- <https://github.com/rwaldron/idiomatic.js>
- <https://github.com/madrobby/pragmatic.js>
- <https://github.com/airbnb/javascript>
- <https://github.com/felixge/node-style-guide>
- <http://crockford.com/javascript/>

하지만 특정 스타일 가이드를 포함한 프레임워크를 이용한다면 그 해당 스타일 가이드를 따르도록 한다.

> #### JSCS 코드 스타일 린터(linter)  
JSCS(http://jscs.info)는 자바스크립트의 코드 스타일을 점검해주는 도구다. 몇몇 스타일 가이드를 포함하여 여러 자바스크립트 스타일 규칙을 포함하고 있다.
또한 여러 텍스트 편집기용 JSCS 플러그인도 존재하며 걸프(Gulp)와 그런트(Grunt) 태스크 러너를 위한 JSCS 태스트도 있다.

### 1.7.3 HTML과 CSS 스타일 가이드

- <http://codeguide.co>
- <https://github.com/necolas/idiomatic-css>

> #### CSScomb  
CSScomb(http://csscomb.com)은 CSS용 코딩 스타일 포맷 도구다. 사용자가 미리 정해 놓은 설정에 따라 CSS의 일관성과 CSS 프로퍼티들의 순서를 검사한다. JSCS와 마찬가지로 CSScomb도 텍스트 편집기와 브런치(Brunch)를 포함한 태스트.빌드 도구의 플러그인이 존재한다.

## 1.8 통합 개발 환경이나 텍스트 편집기에 종속되는 스타일의 코딩은 지양한다.
통합 개발 환경의 기능에 기반을 두고 프로젝트의 기본 뼈대와 구현을 결정하는 종종 있다. 이런 경우 원래 개발을 시작한 개발자와 다른 개발 도구를 이용하는 개발자들이 프로젝트 코드를 서로 이해하는데 큰 어려움을 격게 된다.  
메모장이나 나노(Nano) 같은 매우 기본적인 기능의 텍스트 편집기를 이용하는 사람도 작업 내용과 코드 위치를 금방 찾을 수 있게 프로젝트 구조를 투명하고 명료하게 해야 한다.  
일례로 이렇게 통합 개발 환경에 종속적으로 개발된 코드의 경우, 통합 개발 환경 이용에 매우 제약이 있는 개발자가 템플릿 태그를 살피거나 소스 코드를 찾는 데 매우 많은 시간을 소요하게 된다. 이런 경우를 대비해 널리 통용될 수 있는 작명법인 `<앱_이름>_tag.py`를 따른다.

## 1.9 요약
코딩 스타일을 따르지 않더라도 일단 일관된 코딩 스타일을 정한 후 일관성 있게 따르는 것이 매우 중요하다. 여러 스타일을 섞여 있는 프로젝트의 경우 개발자가 실수할 확률이 더 높아지고, 개발이 더뎌지고 유지보수에 상당히 힘을 쏟아야 한다.
