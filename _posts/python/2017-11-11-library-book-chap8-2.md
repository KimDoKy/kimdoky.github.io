---
layout: post
section-type: post
title: Python Library - chap 8. 특정 데이터 포맷 다루기 - 2. INI 파일 다루기
category: python
tags: [ 'python' ]
---

`configparser`는 INI파일을 다루는 기능을 제공합니다. INI파일은 Windows OS에서 설정 파일로 자주 사용됩니다. 단순한 텍스트로 표현할 수 있기 때문에 Windows 이외의 플랫폼에서도 사용하고 있습니다. 대표적으로 분산형 버전 관리 도구인 Mercurial 입니다.  

## INI 파일 읽어오기

config.ini이란 INI파일을 사용합니다.

```ini
[DEFAULT]
home_dir = /home/guest
group = viewer
limit = 200

[USER_A]
home_dir = /home/user_a
group = Developer
```

INI 파일은 []으로 감싼 "섹션", "옵션 이름과 해당 값"을 한 쌍으로 기술합니다. 옵션 이름과 값은 등호(=)로 구분하며 콜론(:)도 사용할 수 있습니다.

### INI 파일 읽어오기

```python
>>> from configparser import ConfigParser
>>> config = ConfigParser()
>>> config.read('config.ini')  # INI 읽어오기
['config.ini']

>>> config.sections()  # 섹션 리스트 얻기
['USER_A']
>>> config.options('USER_A')  # 옵션 이름 리스트 얻기
['home_dir', 'group', 'limit']

>>> 'USER_B' in config  # 섹션 존재 확인
False

>>> config.get('USER_A', 'group')  # 옵션 값 얻기
'Developer'

>>> config.get('USER_A', 'limit')  # DEFAULT 값 얻기
'200'
```

### ConfigParser.read() 메서드

형식 | ConfigParser.read(file_path)
---|---
설명 | INI 파일을 읽어온다.
인수 | file_path - INI 파일의 경로
반환값 | 해석한 파일 이름의 리스트

file_path는 여러 개의 INI파일을 리스트로 지정할 수도 있습니다.

### ConfigParser.sections() 메서드

형식 | ConfigParser.sections()
---|---
설명 | 읽어온 INI 파일 안에 존재하는 섹션 이름을 리스트로 반환한다.
반환값 | 섹션의 리스트

반환값인 리스트 안에는 DEFAULT 섹션은 포함되지 않습니다. DEFAULT라는 섹션 이름은 특별한 역할을 하며, 지정한 옵션은 기타 모든 섹션의 기본값으로 채택됩니다. 섹션 이름은 대소문자르 구별합니다.

### ConfigParser.options() 메서드

형식 | ConfigParser.options(section)
---|---
설명 | 지정한 섹션 안에 존재하는 옵션 이름을 리스트로 반환한다.
인수 | section - 섹션 이름
반환값 | 옵션 이름 리스트

섹션 이름은 대소문자를 구분하지 않습니다.

### ConfigParser.get() 메서드

형식 | ConfigParser.get(section, option)
---|---
설명 | 지정한 옵션 이름의 값을 구한다.
인수 | section - 섹션 이름 <br> option - 옵션 이름
반환값 | 옵션 이름에 대응하는 값

option에 지정하는 옵션 이름이 INI 파일 중에서 유일한 값이라 하더라도 setion 지정은 필수입니다.  

지정한 section 내에 옵션 이름 option이 존재하지 않으면, DEFAULT 섹션에 옵션 이름이 있는지를 탐색하여 발견되면 해당 값을 사용합니다. 조금 전 'config.ini'의 코드 예에서 USER_A의 섹션에 limit라는 옵션 이름은 존재하지 않았습니다. 그러나 DEFAULT 섹션에 limit의 값이 '200'으로 설정되어 있기 때문에, 결과적으로 '200'이 선택되었습니다. 이 동작을 잘 기억해서 직접 조건 분기를 구현하지 않도록 합니다.

## INI 파일의 추가 활용법

INI 파일은 단순한 구성으로 가독성도 뛰어나기 때문에 다루기 쉬운 포맷이지만, 반복해서 같은 문자열을 적다 보면 복잡해지기 쉽습니다. 이 같은 경우에는 값 삽입(interpolation) 기능을 이용합니다.  

다음 INI 파일 config_interp.ini를 이용합니다.

```ini
[USER_A]
home_dir = /home/user_a
mail_dir = %(home_dir)s/mail
group = Developer
```

### BasicInterolation 이용하기

```python
>>> config = ConfigParser()
>>> config.read('config_interp.ini')
['config_interp.ini']
>>> config.get('USER_A', 'mail_dir')
'/home/user_a/mail'
```

ConfigParser 클래스의 인스턴스를 생성할 때 아무것도 지정하지 않을 때에는 기본으로 값 삽입 기능을 이용할 수 있습니다.  

옵션 이름 mail_dir의 값에 `%(home_dir)s`라고 INI 파일에 기술하면, 같은 섹션 내(또는 DEFAULT 섹션 내)의 옵션 이름 home_dir의 값인 /home/user_a 로 치환됩니다. 그 결과, home/user_a/mail이 얻어집니다.  

ConfigParser 클래스의 인스턴스를 생성할 때 ExtendedInterpolation 클래스를 지정하면, 더 고도의 값을 삽입할 수 있게 됩니다.

다음 INI 파일 config_exinterp.ini을 이용합니다.

```ini
[USER_A]
home_dir = /home/user_a
mail_dir = ${home_dir}/mail
group = Developer

[USER_B]
group = ${USER_A:group}
```

### ExtendedInterpolation 이용하기

```python
>>> from configparser import ConfigParser, ExtendedInterpolation
>>> config = ConfigParser(interpolation=ExtendedInterpolation())
>>> config.read('config_exinterp.ini')
['config_exinterp.ini']
>>> config.get('USER_B', 'group')
'Developer'
```

섹션 [USER_B]의 옵션 group 값에 `$[USER_A:group]`이라고 기술하였습니다. 이는 `$[섹션:옵션 이름]` 구조이며, 다른 섹션의 임의의 옵션 이름 값을 삽입한 것입니다. 같은 섹션 내의 다른 옵션 값을 삽입할 때는 `$[옵션 이름]` 형식으로 기술하면 됩니다.

> #### configparser와 자료형  
configparser로 읽어온 데이터는 모두 문자열이 됩니다. 수치형으로 취급하고 싶다면 ConfigParser.getint()를 이용하는 방법이 있으나, int()를 이용해서 형변환해도 문제 없습니다.  
```python
>>> from configparser import ConfigParser
>>> config = ConfigParser()
>>> config.read('config.ini')
['config.ini']

>>> config.getint('USER_A','limit')
200

>>> int(config.get('USER_A', 'limit'))
200
```
