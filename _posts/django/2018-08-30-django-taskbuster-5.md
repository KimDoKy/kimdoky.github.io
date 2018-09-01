---
layout: post
section-type: post
title: TaskBuster Django Tutorial – Part 5
category: django
tags: [ 'django' ]
---

# [Internationalization and Localization. Languages and Time zones](http://www.marinamele.com/taskbuster-django-tutorial/internationalization-localization-languages-time-zones)

이번 파트에서는 국제화(Internationalization), 현지화(Localization), 표준 시간대(Time Zones)에 대해 다룹니다.

우리 웹 사이트는 두 가지 다른 언어를 정의하고 각 언어에 맞는 URL을 만들고, 두 언어를 지원하는 웹 사이트를 만듭니다.

또한 표준 시간대와 템플리셍 현지 시간을 표시하는 방법을 설명합니다.

이 파트의 개요는 다음과 같습니다.

 - Internationalization – Settings
 - Internationalization – Urls
 - Internationalization – Templates
 - Internationalization – Translation
 - Localization
 - Time Zones

 시작해봅시다!

## Internationalization – Settings

국제화를 구현하는 방법, 즉 우리 페이지가 여러 언어를 지원할 수 있는 방법에 대해 작업합니다.

먼저 모든 번역 파일을 저장할 폴더를 만듭니다. 이 파일들은 Django에 의해 자동으로 생성되어 우리가 번역하고자하는 문자열을 작성합니다. Django에게 어떤 문자열을 후자로 번역할지를 알려주는 방법을 설명하겠지만, 파일을 편집하고 각 문자열에 대한 번역을 수동으로 넣는 것이 아이디어입니다. 이렇게하면 장고는 사용자 환경 설저엥 따라 하나의 언어 또는 다른 언어를 선택하게 됩니다.  

번역의 폴더는 taskbuster 폴더 안에 있습니다.

```
$ mkdir taskbuster/locale
```

다음으로 'settings/base.py' 파일을 열고 다음 코드가 있는지 확인하세요.

```
USE_I18N = True
```

탬플릿 컨텍스트 프로세서 `django.templates.context_processors.i18n`은 `TEMPLATES['OPTION']['context_processors']` 설정 안에 있습니다.

```
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'django.template.context_processors.i18n',
            ],
        },
    },
]
```

Note: Django 쉡을 사용하여 특정 설정의 값을 찾을 수도 있습니다.

```python
$ python manage.py shell
>>> from django.conf import settings
>>> settings.TEMPLATES
```

해당 변수의 현재 값을 출력합니다.  

그 후, 다음 요청 컨텍스트를 통해 사용자의 언어 기본 설정을 결정할 수 있도록 올바른 위치에 Locale middleware를 추가하세요.

```
MIDDLEWARE_CLASSES = (
    ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
)
```

다음으로 사용할 언어를 지정하세요.

```
from django.utils.translation import ugettext_lazy as _
LANGUAGES = (
    ('en', _('English')),
    ('ca', _('Catalan')),
)
```
우리는 영어와 카탈로이나어를 사용할 것입니다. 원하는 언어를 자유롭게 입력해도 됩니다. `ugettext_lazy` 함수는 번역 할 언어 이름을 표시하는데 사용되며 일반적으로 함수의 바로가기를 사용합니다.

Note: 다른 함수인 `ugettext`가 번역에 사용됩니다. 두 함수의 차이점은 `ugettext`가 문자열을 즉시 반환하는 반면, `ugettext_lazy`는 템플릿을 렌더링 할 때 문자열을 반환합니다.  

'settings.py'의 경우 다른 함수로 인해 import 루프가 발생할 수 있기 때문에  `ugettext_lazy`를 사용해야 합니다. 일반적으로 `ugettext_lazy`는 models.py과 forms.py 파일에도 사용해야 합니다.

또한 `LANGUAGE_CODE` 설정은 번역이 없을 경우 Django가 사용할 기본 언어를 정의합니다. 기본값을 그대로 둡니다.

```
LANGUAGE_CODE = 'en-us'
```

마지막으로 이전에 생성한 locale 폴더를 지정하세요.

```python
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
```

콤마 잊지 마세요.

## Internationalization – Urls

이제 설정을 구성했으니 앱을 다른 언어로 작동시키는 방법에 대해 생각해봐야 합니다. 여기서는 다음과 같은 방식을 취할 것입니다: 각 URL에 Django에게 사용할 언어를 알려주는 언어 접두어를 포함시킵니다. 홈페이지의 경우 다음과 같습니다.

 - mysite.com/en
 - mysite.com/ca

'mysite.com/myapp'와 같은 나머지 URL은 다음과 같습니다.

 - mysite.com/en/myapp
 - mysite.com/ca/myapp

이 방법으로 사용자는 한 언어에서 다른 언어로 쉽게 변경할 수 있습니다. 하지만, 우리는 어떤 robots.txt를 원하지 않습니다. humans.txt도 이 구조를 따릅니다. (검색 엔진은 구조에 따라 'mysite.com/robots.txt'와 'mysite.com/humans.txt'를 찾을 것입니다.)

이를 구현하는 방법은 'urls.py'을 사용하는 것입니다.

```python
# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from .views import home, home_files

urlpatterns = [
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        home_files, name='home-files'),
]

urlpatterns += i18n_patterns(
    url(r'^$', home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
```

robots.txt와 humans.txt 파일을 같은 URL로 남겨두었고, 우리가 번역하고 싶은 것들은 `i18n_patterns` 함수를 사용합니다.

로컬 서버를 실행하고 홈페이지를 방문하면 `/en` 또는 `/ca`로 리다이렉션되어야 합니다. DJango의 공식 언어 문서에서 [how Django discovers language preference](https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#how-django-discovers-language-preference)에 대해 더 배울 수 있습니다.

사용자가 언어 환경 설정을 어떻게 변경할까요? DJango는 이것을 하는 뷰를 가지고 있습니다.

이 뷰에는 언어 매개변수가 포함된 POST 요청이 예상됩니다. 하지만 상단 검색바를 customizing 할 때 본 튜토리얼의 다른 시간대에 해당 뷰를 처리합니다. 사용 가능한 모든 언어를 가진 드롭다운 메뉴를 선택한 후 변경할 언어를 선택하는 것이 좋습니다.

계속하기 전에 테스트를 실행해봅니다.

```
$ python mange.py test taskbuster.test
```

하나는 실패합니다! 실제로 'taskbuster/test.py'에서 가장 작은 항목이 모두 실패합니다. `reverse('home')`을 사용할 때 렌더링되는 탬플릿을 찾을 수 없기 때문입니다. 우리는 reverse가 제대로 작동하게 하기 위해 active language를 설정해야 합니다. 먼저 파일 맨 위애 다음을 임포트합니다.

```python
from django.utils.translation import activate
```

그 다음은 테스트 선언 직후에 선택할 언어를 활성화하세요.

```python
def test_uses_index_template(self):
    activate('en')
    response = self.client.get(reverse("home"))
    self.assertTemplateUsed(response, "taskbuster/index.html")
```

다른 테스트에도 동일하게 적용하세요. (test_uses_base_template)

이제 테스트는 통과합니다. 'functional_tests/test_all_users.py'에도 동일한 작업을 해야 합니다.(`activate`를 임포트하고, setUp 메소드의 마지막에 `activate('en')`을 추가해야 합니다.)

## Internationalization – Templates

이제 홈페이지의 title(h1 Hello World)를 번역하는데 집중합니다. index.html을 열고 `<h1>Hello, world!</h1>`를 찾습니다.

두 가지 템플릿 태그를 사용합니다.
 - `trans`는 한 줄을 번역하는데 사용됩니다. 제목에 사용합니다.
 - `blocktrans`는 확정 된 콘텐츠에 사용됩니다. 단락에 사용합니다.

`jumbotron` 컨테이너의 h1과 p 내용을 다음 코드와 같이 변경하세요.

```html
<div class="jumbotron">
    <div class="container">
        <h1>{% trans "Welcome to TaskBuster!"%}</h1>
        <p>{% blocktrans %}TaskBuster is a simple Task manager that helps you organize your daylife. </br> You can create todo lists, periodic tasks and more! </br></br> If you want to learn how it was created, or create it yourself!, check www.django-tutorial.com{% endblocktrans %}</p>
        <p><a class="btn btn-primary btn-lg" role="button">Learn more &raquo;</a></p>
      </div>
    </div>
</div>
```

또한 이전 템플릿 태그를 엑세스하려면 템플릿 맨 위에 `{% load i18n %}`를 써야 합니다. 이 경우 base.html 태그에서 확장됩니다.

## Internationalization – Translation

마지막으로 문자열을 번역합니다.

'taskbuster_project' 폴더(manage.py파일과 동등 레벨)의 터미널로 이동하고 다음을 실행하세요.

```
$ python manage.py makemessages -l ca
```
이렇게 하면 번역하려는 언어에 대한 메시지 파일이 생성됩니다. 모든 코드를 영어로 작성하므로 해당 언어에 대한 메시지 파일을 만들 필요가 없습니다.

그러나 GNU gettext가 설치되어 있지 않다는 오류가 발생합니다. [GNU gettext 홈페이지](https://www.gnu.org/software/gettext/)에 접속해서 최신버전을 설치하세요.

기본적으로 패키지 폴더(압축을 푼 경우) 안에 들어가서 다음을 입력해야 합니다.

```
$ ./configure
```

시스템에 맞게 설치를 구성하세요. 그 다음은

```
$ make
```

패키지를 컴파일 합니다. 터미널에서 설치할때 끔찍한 코드들을 출력하는지 궁금해집니다.

원한다면

```
$ make check
```

설치하기 전에 패키지 테스트를 실행하여 모든 것이 잘 작동하는지 확인하세요. 마지막으로 실행합니다.

```
$ make install
```
패키지를 설치하세요.

이제 개발 환경으로 돌아가서 메시지 파일을 생성해 봅니다.

```
$ python manage.py makemessages -l ca
```

이제 'taskbuster/locale' 폴더로 가서 안에 있는 내용을 확인하세요.

```
$ cd taskbuster/locale
$ ls
```

'ca'(또는 번역을 위해 선택된 언어)라는 폴더가 있고 'LC_MESSAGES'라는 폴더가 내부에 있습니다. 그 안에 들어가면 'django.po'라는 파일을 찾을 수 있습니다. 에디터로 해당 파일을 열어봅세요.

파일의 시작 부분에 메타 데이터가 있지만 그 후에는 변환을 위해 표시 한 문자열을 볼 수 있습니다.

 - 'base.py' 설정 파일의 언어 이름은 'English'와 'Catalan'입니다.
 - 'index.html'파일의 title은 'Welcome to TaskBuster!'입니다.
 - 'index.html' 파일의 제목 뒤 단락

 각 문장은 msgid로 시작하는 줄에 나타납니다. 다음 행에 msgstr로 시작하는 번역을 넣어야 합니다.

 title 번역은 간단합니다.

```
msgid "Welcome to TaskBuster!"
msgstr "Benvingut a TaskBuster!"
```
단락을 사용하면 각 줄을 `""`으로 시작하고 끝내야 합니다.

```
msgid ""
"TaskBuster is a simple Task manager that helps you organize your daylife. </"
"br> You can create todo lists, periodic tasks and more! </br></br> If you "
"want to learn how it was created, or create it yourself!, check www.django-"
"tutorial.com"
msgstr ""
"TaskBuster és un administrador senzill de tasques que t'ajuda a administrar "
"el teu dia a dia. </br> Pots crear llistes de coses pendents, tasques "
"periòdiques i molt més! </br></br> Si vols apendre com s'ha creat, o"
"crear-lo tu mateix!, visita la pàgina <a href='http://www.marinamele.com/taskbuster-django-tutorial' target=_'blank'>Taskbuster Django Tutorial</a>."
```

또한 줄 끝 부분의 최종 공간을 기록하세요. 해당 공백을 포함하지 않으면 줄 끝의 단어와 다음 줄의 시작 부분에 있는 단어가 연결됩니다.

모든 번역이 설정되면 다음과 같이 컴파일해야 합니다.

```
$ python manage.py compilemessages -l ca
```

로컬 서버를 실행하고 홈페이지로 이동하여 효과를 볼 수 있지만 먼저 테스트를 작성하는 것이 좋습니다.

'functional_tests/test_all_users.py'에 다음의 테스트를 추가하세요.

```python
def test_internationalization(self):
    for lang, h1_text in [('en', 'Welcome to TaskBuster!'),
                                ('ca', 'Benvingut a TaskBuster!')]:
        activate(lang)
        self.browser.get(self.get_full_url("home"))
        h1 = self.browser.find_element_by_tag_name("h1")
        self.assertEqual(h1.text, h1_text)
```

다른 언어를 사용하는 경우 'Benvingut a TaskBuster'으로 변경되었다는 것과 `activate('ca')`을 변경하는 것을 기억하세요.

모든 테스트가 통과되기를 바랍니다. :)

## Localization

Django는 현재 **locale** 에 지정된 형식을 사용하여 템플릿의 시간과 날짜를 렌더링할 수 있습니다. 즉, 서로 다른 지역의 두 사람이 템플릿에서 서로 다른 날짜 포맷을 볼 수 있습니다.

Localization을 사용하려면 base.py 설정 파일에서 다음 코드를 확인하세요.

```
USE_L10N = True
```

이렇게 하면 템플릿에 값을 포함할 때 Django는 locale 포맷을 사용하여 값을 렌더링합니다. 자동 포맷팅을 비활성화하는 방법도 필요합니다. 예를 들어, javascript를 사용할 때는 모든 지역에 대해 동일한 포맷을 사용해야 합니다.

그걸 위한 테스트를 작성합니다. 홈페이지에서 로컬 날짜 포맷과 비 로컬 포맷을 모두 사용하여 오늘 날짜와 시간을 표시합니다.

'functional_tests/test_all_users.py'을 열어서 다음 코드를 임포트합니다.

```python
from datetime import date
from django.utils import formats
```

그 후 `HomeNewVisitorTest`클래스에 테스트 메서드를 추가하세요.

```python
def test_localization(self):
    today = date.today()
    for lang in ['en', 'ca']:
        activate(lang)
        self.browser.get(self.get_full_url("home"))
        local_date = self.browser.find_element_by_id("local-date")
        non_local_date = self.browser.find_element_by_id("non-local-date")
        self.assertEqual(formats.date_format(today, use_l10n=True),
                              local_date.text)
        self.assertEqual(today.strftime('%Y-%m-%d'), non_local_date.text)
```

그런 다음 테스트를 먼저 실행하여 무엇을 먼저 구현해야 하는지 확인하세요. 다음 명령으로 테스트를 실행할 수 있습니다.

```
$ python manage.py test functional_tests.test_all_users.HomeNewVisitorTest.test_localization
```

**local-date** id가 있는 요소를 찾을 수 없어서 테스트가 실패합니다. 그걸 만들어 봅니다.

'taskbuster/index.html' 템플릿을 열어서 파일의 시작부분에 locale 템플릿 태그를 로드합니다.

```
{% load l10n %}
```

그 후 `div` 컨테이너를 찾습니다. 처음 두 열을 편집하여 h2 헤더에 날짜를 표시합니다.

```html
<div class="col-md-4">
      <h2 id="local-date">{{today}}</h2>
      <p>This is the time using your local information </p>
      <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
</div>
<div class="col-md-4">
      <h2 id="non-local-date">{{today|unlocalize}}</h2>
      <p>This is the default time format.</p>
      <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
</div>
```

두 번째 헤더의 필터가 locale 해제됨을 유의하세요. 이렇게 하면 **today** 변수를 렌더링하는 동안 localization 포맷을 사용할 수 없게 됩니다. 또한 대형 block을 비활성하는 또 다른 템플릿 태그가 있습니다.

```
{% localize off %} code without localization {% endlocalize %}
```

[Django docs](https://docs.djangoproject.com/en/1.8/topics/i18n/formatting/#template-tags)에서 더 자세히 알 수 있습니다.

테스트를 저장하고 다시 실행하세요. **today** 변수를 home 뷰에 전달하지 않았기 때문에 다시 실패합니다.

views.py에 home 뷰를 수정합니다.

```python
import datetime

def home(request):
    today = datetime.date.today()
    return render(request, "taskbuster/index.html", {'today': today})
```

테스트를 재실행합니다. 이제 모든 테스트가 통과합니다.

> 날짜 표기법이 달라서 테스트가 통과하지 못한다면 base.py 셋팅파일에 `DATE_FORMAT = 'Y-m-d'`를 추가하세요.

## Time Zones

프로젝트가 전 세계의 날짜와 시간을 처리해야하는 경우 UTC(조정된 세계 시간)로 작업하는 것이 좋습니다. 이렇게 하면 모든 날짜와 시간에 데이터베이스의 규칙이 균일해져서 사용자의 시간대와 상관없이 비교할 수 있습니다.  

Django는 폼과 템플릿에서 원하는 시간대로 자동으로 변환하므로 걱정하지 않아도 됩니다.

time zones을 사용하려면 base.py 설정 파일을 열어서 다음 내용을 확인합니다.

```
USE_TZ = True
```

Django는 시간대 계산을 허용하는 Python 패키지인 [pytz](http://pytz.sourceforge.net/)도 설치하도록 권장합니다. 이 또한 튜토리얼 후반에 사용할 테스크 큐 관리자인 [Celery]를 사용하는데 필요한 패키지입니다. 설치하죠.

개발 환경을 활성화하고 다음을 입력합니다.

```
$ pip install pytz
```

requirement base.txt에 추가하세요.(pip freeze로 설치된 버전을 확인할 수 있습니다.) 테스트 환경에도 설치해야 합니다.

두 가지 종류의 datetime 객체가 있는데, 표준 시간대 객체와 그렇지 않은 객체를 인식합니다. 어떤 날짜 인지를 결정하기 위해 datetime 메서드 `is_aware()`와 `is_naive()`를 사용할 수 있습니다.

표준 시간대 지원을 활성화하면 모든 datetime 인스턴스가 인식됩니다. 따라서 저장된 datetime과 상호 작용하려면 aware datetime 인스턴스를 만들어야 합니다.

얘를 들어:

```python
import datetime
from django.utils.timezone import utc

now_naive = datetime.datetime.now()
now_aware = datetime.datetime.utcnow().replace(tzinfo=utc)
```

또한 `USE_TZ=True`과 같이 time zone이 활성화 된 경우 현재 aware 시간을 가져오는 바로가기가 있습니다.

```python
from django.utils.timezone import now
now_aware = now()
```

그러나 Django 문서에서 설명한 것처럼 HTTP 헤더를 통해 사용자 time zone 기본 설정을 결정할 수 있는 방법은 없습니다. 우리가 할 일은 선호하는 time zone를 사용자에게 묻고 사용자 프로필에 저장하는 것입니다. 하지만 튜토리얼의 후반에 하게 됩니다.

한편, 우리는 설정 변수로 기본 time zone을 정의할 것입니다.

```
TIME_ZONE = 'Europe/Madrid'
```

이 코드는 바르셀로나의 time zone입니다. [time zone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)에서 선택할 수 있습니다.

이제 바르셀로나에서 현재 시간(기본 time zone을 사용), UTC 시간과 뉴욕 시간을 표시하는 방법을 살펴봅니다.

'functional_tests/test_all_users.py'을 열고 다음 테스트를 작성하세요.

```python
def test_time_zone(self):
    self.browser.get(self.get_full_url("home"))
    tz = self.browser.find_element_by_id("time-tz").text
    utc = self.browser.find_element_by_id("time-utc").text
    ny = self.browser.find_element_by_id("time-ny").text
    self.assertNotEqual(tz, utc)
    self.assertNotIn(ny, [tz, utc])
```
바르셀로나, UTC, 뉴욕시간이 다른지 확인합니다.

이 테스트를 실행하면 id가 **time-tz** 인 요소가 없기 때문에 실패합니다. index.html 템플릿을 열고 세 번째 열을 편집하세요.

```html
<div class="col-md-4">
    <h2>Time Zones</h2>
    <p> Barcelona: <span id="time-tz">{{now|time:"H:i"}}</span></p>
    <p> UTC: <span id="time-utc">{{now|utc|time:"H:i"}}</span></p>
    <p> New York: <span id="time-ny">
           {{now|timezone:"America/New_York"|time:"H:i"}}</span></p>
    <p><a class="btn btn-default" href="#" role="button">View details &raquo;</a></p>
</div>
```

time filter만 사용하여 시간만 표시했습니다. 테스트를 다시 실행하면 **utc** 필터를 찾을 수 없어서 실패합니다. 'index.html' 파일 상단에 다음 코드를 추가합니다.

```
{% load tz %}
```

테스트를 다시 실행하면 뷰가 현재 변수를 전달하지 않았기 때문에 이번에는 실패합니다. 'views.py'을 열고 파일 시작 부분에 임포트를 추가합니다.

```python
from django.utils.timezone import now
```

`now` 변수를 home 뷰에 추가합니다.

```python
def home(request):
    today = datetime.date.today()
    return render(request, "taskbuster/index.html",
                       {'today': today, 'now': now()})
```

테스트를 다시 실행하면 통과해야 합니다!

이제 튜토리얼의 마지막 부분입니다. 변경 사항을 커밋하는 것을 잊지 마세요.

```
$ git add .
$ git status
$ git commit -m "Internationalization and localization"
$ git push origin master
```

GitHub와 같은 클라우드 저장소에 푸시하려는 경우에만 마지막 명령을 실행하세요.
