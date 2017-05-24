---
layout: post
section-type: post
title: TDD collectstatic
category: tdd
tags: [ 'tdd' ]
---

Chapter 7. collectstatic과 다른 정적 디렉터리

Django 개발 서버가 앱 폴더 내의 모든 정적 파일을 마법처럼 찾아내서 제공한다. 이것은 개발 단계에선 괜찮지만, 실제 운영 중인 웹 서버에서 Django가 정적 콘텐츠를 제공하도록 하는것은 매우 느리고 비효율적이다.  

아파치(Apache)나 Nginx 같은 웹서버도 같은 역할을 할 수 있다. 또는 직접 정적 파일을 호스팅하는 대신 모두 CDN(Content Delivery Network)에 업로드해서 호스팅하는 방법도 있다.  

이런 이유로 여러 앱에 존재하는 모든 정적 파일은 한곳에 모아서 배포용으로 만들어 둘 필요가 있다. 이 작업을 해 주는 것이 **collectstatic** 명령이다.

수집된 정적 파일이 모이는 위치는 settings.py의 STATIC_ROOT 항목을 통해 설정한다.
해당 항목 값을 레포지토리 밖에 있는 폴더로 지정한다.

```
workspace
│    ├── superlists
│    │    ├── lists
│    │    │     ├── models.py
│    │    │
│    │    ├── manage.py
│    │    ├── superlists
│    │
│    ├── static
│    │    ├── base.css
│    │    ├── etc...
```
정적 파일이 레포지토리 밖에 있어야 하는 것이 중요하다.  
왜냐하면 list/static 폴더 내에 있는 파일과 동일하기 때문에 굳이 코드 관리를 해줄 필요가 없다.

이 폴더를 설정하기 위해 프로젝트의 base 디렉터리를 기준으로 상대 경로를 지정해준다.

```
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../static'))
```
준비 되었다면 collectstatic를 실행한다.

```
$ python3 manage.py collectstatic

You have requested to collect static files at the destination
location as specified in your settings:

/workspace/static

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel:
yes

[...]
Copying '/workspace/superlists/lists/static/bootstrap/js/bootstrap.js'
Copying '/workspace/superlists/lists/static/bootstrap/js/bootstrap.min.js'
Copying '/workspace/superlists/lists/static/bootstrap/js/npm.js'

77 static files copied to '/workspace/static'.
```

생성된 ../static 폴더를 보면 모든 CSS 파일이 복사된 것을 알 수 있다.

```
$ tree ../static/
../static/
├── admin
│   ├── css
│   │   ├── base.css

[...]

│       └── urlify.js
├── base.css
└── bootstrap
    ├── css
    │   ├── bootstrap.css
    │   ├── bootstrap.min.css
    │   ├── bootstrap-theme.css
    │   └── bootstrap-theme.min.css
    ├── fonts
    │   ├── glyphicons-halflings-regular.eot
    │   ├── glyphicons-halflings-regular.svg
    │   ├── glyphicons-halflings-regular.ttf
    │   ├── glyphicons-halflings-regular.woff
    │   └── glyphicons-halflings-regular.woff2
    └── js
        ├── bootstrap.js
        ├── bootstrap.min.js
        └── npm.js

10 directories, 77 files
```

이렇게 흩어져 있는 정적 파일을 한 폴더에 옮길 수 있다.
