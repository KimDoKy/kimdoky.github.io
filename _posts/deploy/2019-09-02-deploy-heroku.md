---
layout: post
section-type: post
title: Deploy Django to Heroku
category: deploy
tags: [ 'deploy' ]
---

Heroku로 배포하는 내용은 Heroku의 홈페이지나 많은 블로그에서 다루고 있기 때문에 큰 어려움 없이 쉽게 배포할 수 있습니다....만.

일반적으로 개발하는 Django의 구조는 [헤로쿠 배포 튜토리얼](https://tutorial-extensions.djangogirls.org/ko/heroku/)(사랑해요 장고걸스..)에서 나오는 구조와는 차이가 나기도 하고, 여러 문제점들이 있어서 생각보다 배포에 시간을 사용하게 되었습니다.

그래서 까먹지 않기 위해 기록합니다.

---

### Django 구조

우선 django의 구조입니다.

```
# my app

django_app
  ├── conf
  ├── boards
  ├── manage.py
  ...

# tutorial

├── conf
├── boards
├── manage.py
...
```

tutorial의 django 구조는 root가 manage.py 파일이 있는 디렉토리입니다.

그래서 heroku 배포에 필요한 파일(Procfile, runtime.txt)은 manage.py와 동일한 레벨에 위치해야 합니다.  

---

## 1. Heroku 배포에 필요한 파이썬 패키지

```
$ pip install dj-database-url gunicorn whitenoise
```

pip로 설치후 requirements.txt 작업을 해줍니다.

```
$ pip freeze > requirements.txt
```

---

## 2. Procfile

settings.py의 경우 dev.py, prod.py 처럼 환경별로 나누었기 때문에 gunicorn에서 wsgi를 해당 셋팅으로 지정해주어야 합니다.

```
# procfile
web: gunicorn conf.wsgi.prod --log-file -
```

## 3. runtime.txt

실행할 환경의 파이썬 버전을 지정해줍니다.

```
python-3.7.0
```

---

### PostgreSQL 연결하기

```python
# settings/prod.py

import dj_database_url

DATABASES = {
    ... Postgresql 셋팅
    }

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
```

---

### Heroku 로그인

```
$ heroku login
```

(heroku cli 설치되었다고 가정합니다.)

---

### Heroku App 생성하기

```
$ heroku create app_name (소문자, 숫자, 대시(-)만 사용가능. 언더바 금지)
```

---

### 다른 브랜치를 heroku git으로 push 하기

우선 수정 및 셋팅 한 파일들을 커밋합니다.

그리고 heroku에 push 합니다. (github에는 푸시 되지 않습니다.)

```
# 기본
$ git push heroku master

# 브랜치 지정(예로 deploy라는 브랜치를 지정)
$ git push heroku deploy:master
```

파일을 변경하였다면, 꼭 다시 커밋, 푸시하고 확인해야 합니다.  
절대 기존 커밋에 덮어씌우면 안됩니다. 새로 커밋하는게 정신 건강에 좋습니다.

---

### app 확인하기

```
$ heroku open
```

브라우저에 자동 실해되어 확인이 가능하며, migrate를 하기 전이라서 에러화면을 띄웁니다.

---

### migrate 하기

```
$ heroku run python manage.py migrate --settings=conf.settings.prod
```

heroku cli는 자동완성을 지원하지 않습니다. 주의!!

---

### error 잡기

```
$ heroku logs --tail
```

위 명령으로 로그를 확인하여 에러를 잡지만, 불편합니다.  

```
$ heroku local web
```

`localhost:5000`으로 접속하면 바로 확인이 가능합니다.

위 명령으로 로컬에서 실행하여 에러를 잡는게 속 편합니다.

---

### 잡다한 에러들

에러 발생 중 로그를 살펴보니

`Your WhiteNoise configuration is incompatible with WhiteNoise v4.0` 라는 로그를 발견하였고, whitenoise 4버전부터 일부 사용하지 않는 django 설정 삭제 등 변화가 있다는 내용을 확인하였습니다.

```python
# settings/base.py

MIDDLEWARE = [
    ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

..

# Static root를 지정하지 않으면 에러 발생
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# whitenoise 4 버전부터 설정이 바뀌었기 때문에 이 부분을 꼭 기존의 내용들에서 업데이트 해야 함
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesSto
```

---

Heroku 배포는 한 번 해봐야지 하면서 미루고 있었는데, 미뤄둔 숙제 하나를 끝냈습니다.
