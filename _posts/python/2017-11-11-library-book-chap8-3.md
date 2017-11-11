---
layout: post
section-type: post
title: Python Library - chap 8. 특정 데이터 포맷 다루기 - 3. YAML 다루기
category: python
tags: [ 'python' ]
---
`PyYAML`패키지는 YAML 포맷의 데이터를 다루는 기능을 제공합니다. YAML포맷은 자료구조를 간소한 기술로 표현할 수 있어 일반적으로 많이 사용합니다. Python 제품에서 프로비저닝 도구인 Ansible은 YAML을 다룰때 PyYAML을 사용합니다.  

PyYAML을 사용하면 애플리케이션의 설정 파일을 YAML 모맷으로 작성하여 이용할 수 있습니다.

## PyYAML 설치

### PyYAML의 pip 설치

```
$ pip install PyYAML
```

## YAML 파일 읽어오기

sample1.yml을 대상으로 합니다.

```yml
---
database:
  host: localhost
  port: 3306
  db: test
  user: test
smtp_host: localhost
```

### YAML 파일 읽어오기

```python
>>> import yaml
>>> file = open('sample1.yml', 'r')
>>> conf = yaml.load(file)
>>> conf
{'smtp_host': 'localhost', 'database': {'db': 'test', 'port': 3306, 'user': 'test', 'host': 'localhost'}}
>>> conf['database']['port']
3306
>>> file.close()
```
해시로 표현되는 데이터를 읽어오면 Python의 dict형으로 취습할 수 있습니다. 중첩도 유지됩니다. 해시 이외에 배열로 자료구조를 표현할 수도 있습니다. 이때는 Python의 리스트형으로 취급됩니다.

### yaml.load()

형식 | yaml.load(stram, Loader=(class 'yaml.loader.Loader'))
---|---
설명 | YAML 포맷으로 작성된 파일을 읽어온다.
인수 | stram - YAML 파일을 읽어올 텍스트 스트림을 지정한다.
반환값 | YAML을 해석한 결과의 Python 객체

yaml.load()와 비슷한 기능을 가진 yaml.load_all()도 있습니다. yaml.load_all()은 "---"로 구분된 YAML 파일을 읽어오기 위해 사용합니다.

### sample2.yml

```yaml
---
order: 1
menu: ham
---
order: 2
menu: egg
```

### load_all()을 사용해 YAML 파일 읽어오기

```python
>>> with open('sample2.yml', 'r') as f:
...     for data in yaml.load_all(f):
...         print(data)
...
{'menu': 'ham', 'order': 1}
{'menu': 'egg', 'order': 2}
```

## YAML 파일 쓰기

```python
>>> hosts = {'web_server': {'192.168.0.2', '192.168.0.3'}, 'db_server':['192.168.10.7']}
>>> with open('dump.yml', 'w') as f:
...     f.write(yaml.dump(hosts, default_flow_style=False))
...
84
```

### dump.yml

```yaml
db_server:
- 192.168.10.7
web_server: !!set
  192.168.0.2: null
  192.168.0.3: null
```

### yaml.dump()

형식 | yaml.dump(data, stream=None, Dumper=Dumper, \**kwds)
---|---
설명 | YAML 포맷으로 작성된 파일을 출력하낟.
인수 | data - 출력 대상 데이터 <br> stream - 출력할 파일 객체를 지정한다.
반환값 | stream이 None이면 문자열을 반환한다.

dump()에는 YAML 포맷과 관련된 인수를 지정할 수 있습니다.

### YAML 포맷 관련 인수

인수 | 설명
---|---
indent | 리스트가 중첩되는 경우 등에 indent 스페이스 수를 수치로 지정한다.
explicit_start | True를 지정하면 맨 앞에 "---"가 포함된다. 기본값은 False
default_flow_style | 기본값 True에서는 YAML의 flow 스타일이 채택된다. False를 지정하면 블록 스타일이 된다.
