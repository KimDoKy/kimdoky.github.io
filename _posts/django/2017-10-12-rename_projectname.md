---
layout: post
section-type: post
title: Django - 프로젝트 이름을 바꾸었을 때 수정해야 하는 파일들
category: django
tags: [ 'django' ]
---

Django 프로젝트를 시작하면 최상위 디렉터리와 프로젝트 이름이 같기 때문에 서로 구분하기 위해서 프로젝트 이름을 변경합니다.

하지만 프로젝트의 이름을 바꾸면 프로젝트 이름으로 된 셋팅된 path들을 모두 변경해주어야 합니다.

> 변경할때 프로젝트 이름이 아니라 최상위 디렉터리 이름을 변경하면 이런 경우가 발생하지 않겠지만, 추후에 프로젝트 이름을 변경한다면 언젠가는 필요한 작업들입니다.


## 수정해야 하는 작업들

- renameproject/manage.py

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "renameproject.settings")
```

- renameproject/settings.py

```python
ROOT_URLCONF = 'renameproject.urls'
WSGI_APPLICATION = 'renameproject.wsgi.application'
```

- renameproject/wsgi.py

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "renameproject.settings")
```

해당 사례가 있어서 git에 올려 두었으니 참고하세요.

<https://github.com/KimDoKy/study/commit/6b33c3c4d47899636a819397056882affd067240>
