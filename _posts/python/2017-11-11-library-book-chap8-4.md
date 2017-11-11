---
layout: post
section-type: post
title: Python Library - chap 8. 특정 데이터 포맷 다루기 - 4. JSON 다루기
category: python
tags: [ 'python' ]
---

`json` 모듈은 JSON 포맷 데이터를 다루는 기능을 제공합니다. JSON(JavaScript Object Notation)은 JavaScript로 구조화된 데이터를 표현하기 위한 포맷입니다. 지금은 Web API의 입출력 포맷으로 널리 이용되고 있고, Twitter나 GitHub의 API도 JSON을 채택하고 있습니다.  

또한 데이터베이스 상에 JSON 포맷으로 자료구조를 저장하는 방법으로도 이용하고 있습니다. PostgreSQL은 9.2 버전부터 자료형에 JSON형이 추가되었습니다. MongoDB처럼 JSON으로 자료구조를 표현하는 데이터 저장소도 있습니다.

## JSON 인코딩과 디코딩

### JSON 인코딩

```python
>>> import json
>>> data = [{'id':123, 'entitied':{'url':'python.org', 'hashtags':['#python', '#pythonkor']}}]
>>> print(json.dumps(data, indent=2))
[
  {
    "entitied": {
      "url": "python.org",
      "hashtags": [
        "#python",
        "#pythonkor"
      ]
    },
    "id": 123
  }
]
```

### json.dumps()

형식 | json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, \**kw)
---|---
설명 | 데이터를 JSON 포맷으로 인코딩한다.
인수 | obj - 인코딩 대상 객체 <br> indent - indent를 위한 스페이스 수를 지정한다. <br> sort_keys - True로 지정하면 키 값으로 정렬된다.
반환값 | JSON 형식의 str 객체

### JSON 디코딩

```python
>>> from decimal import Decimal
>>> json_str = '["ham", 1.0, {"a":false, "b":null}]'
>>> json.loads(json_str)
['ham', 1.0, {'b': None, 'a': False}]

>>> json.loads(json_str, parse_float=Decimal)  # 부동소수점 수의 취급 지정
['ham', Decimal('1.0'), {'b': None, 'a': False}]
```

### json.loads()

형식 | json.loads(s, encoding=None, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_hook=None, \**kw)
---|---
설명 | 데이터를 JSON 포맷에서 디코딩한다.
인수 | s - 디코딩 대상 객체 <br> parse_float - JSON에 포함된 부동소수점 수의 취급을 지정한다. <br> parse_int - JSON에 포함된 정수의 취급을 지정한다.
반환값 | Python 객체

인코딩과 디코딩은 다음 반환표를 기반으로 이루어집니다.

### 인코딩과 디코딩 변환표

JSON | Python
---|---
객체 | 사전
배열 | 리스트
문자열 | 문자열
수치 | 수치
true | True
false | False
null | None

인코딩할 때 튜플은 리스트와 같게 취급됩니다.

## JSON 인코딩과 디코딩(파일 객체)
JSON을 포함한 파일 객체와 Python 객체의 인코딩/디코딩에 대해 다룹니다.

### 파일 읽어오기 및 저장하기

```python
>>> import json
>>> with open('./sample.json', mode='r') as f:
...     json_string = json.load(f)
...
>>> print(json.dumps(json_string, indent=2))
[
  {
    "entities": {
      "hashtags": [
        "#python",
        "#pythonkor"
      ],
      "url": "www.python.org"
    },
    "id": 123
  }
]

>>> json_string[0]['entitiese']['hashtags'].append('#pyhack')
>>> with open('dump.json', mode='w') as f:
...     json.dump(json_string, f, indent=2)
```

### dump.json

```json
[
  {
    "entities": {
      "hashtags": [
        "#python",
        "#pythonkor",
        "#pyhack"
      ],
      "url": "www.python.org"
    },
    "id": 123
  }
]
```

문자열을 다루는 함수는 loads()와 dumps()입니다. 파일 객체를 다루는 함수는 load()와 dump()입니다. (s가 차이납니다.)

### json.dump()

형식 | json.dump(obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=none, default=None, sort_keys=False, \**kw)
---|---
설명 | 데이터를 JSON 포맷으로 인코딩하여 파일에 출력한다.
인수 | obj - 인코딩 대상 객체 <br> fp - 파일 객체를 지정한다. <br> indent - indent를 위한 스페이스 수를 지정한다. <br> sort_keys - 로 지정하면 키 값으로 정렬된다.

### json.load()

형식 | json.load(fp, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, \**kw)
---|---
설명 | 파일 객체 중 JSON 데이터를 디코딩한다.
인수 | fp - 파일 객체를 지정한다. <br> parse_float - JSON에 포함된 부동소수점 수의 취급을 지정하낟. <br> parse_int - JSON에 포함된 정수의 취급을 지정한다.
반환값 | Python 객체

인수 fp 이외의 사용법은 loads()와 같습니다.
