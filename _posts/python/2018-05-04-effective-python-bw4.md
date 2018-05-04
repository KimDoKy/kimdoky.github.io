---
layout: post
section-type: post
title: EFFECTIVE PYTHON - 복잡한 표현식 대신 헬퍼 함수를 작성하자
category: python
tags: [ 'python' ]
---

**파이썬의 간결한 문법을 이용하면 많은 로직을 한 줄의 표현식으로 작성할 수 있다.**

예를 들어 URL에서 쿼리 문자열을 디코드해야하는 상황이다.

```python
# 각 쿼리 문자열 파라미터는 정수 값을 표현한다.
from urllib.parse import parse_qs
my_values = parse_qs('red=5&blue=0&green=', keep_blank_values=True)
print(repr(my_values))

>>>
{'red': ['5'], 'blue': ['0'], 'green': ['']}
```
결과 딕셔너리에 `get` 메서드를 사용하면 각 상황에 따라 다른 값을 반환할 것이다.

```python
>>> print('Red:      ', my_values.get('red'))
Red:       ['5']
>>> print('Green:    ', my_values.get('green'))
Green:     ['']
>>> print('Opacity:  ', my_values.get('opacity'))
Opacity:   None
```

파라미터가 없거나 비어 있으면 기본값으로 0을 할당하게 하면 좋다. 이 로직에 if 문이나 헬퍼 함수까지는 쓸 필요는 없고, boolean 표현식으로 처리할 수 있다.

파이썬의 문법은 boolean 표현식으로도 쉽게 처리할 수 있다. 빈 문자열, 빈 리스트, 0이 모두 암시적으로 False로 평가된다. 따라서 다음 표현식들의 결과는 첫 번째 서브 표현식이 False일 때 or 연산자 뒤에 오는 서브 표현식을 평가한 값이 된다.

```python
# 쿼리 문자열: 'red=5&blue=0&green='
>>> red = my_values.get('red', [''])[0] or 0
>>> green = my_values.get('green', [''])[0] or 0
>>> opacity = my_values.get('opacity', [''])[0] or 0

>>> print('Red:     %r' % red)
Red:     '5'

>>> print('Green:   %r' % green)
Green:   0

>>> print('Opacity: %r' % opacity)
Opacity: 0
```

이 표현식은 읽기 어려울 뿐 아니라 필요한 작업을 다 수행하지도 않는다. 모든 파라미터 값이 정수가 되게 해서 수학식에서도 값들을 사용할 수 있게 하는 것이 목표이다. 그러려면 각 표현식을 내장 함수 int로 처리해서 문자열을 정수 값으로 파싱해야 한다.

```python
red = int(my_values.get('red', [''])[0] or 0)
```
이 코드는 읽기가 어렵다. 시가적 방해 요소도 많다. 코드를 처음 읽는 사람은 어떤 동작을 하는지 알아내려고 표현식의 각 부분을 따로 떼어내는데 시간을 들여야 한다. 짧아서 좋을 수는 있지만 큰 의미는 없다.

if/else 조건식(삼항 표현식)을 이용하면 코드를 짧게, 더 명확하게 표현할 수 있다.

```python
red = my_values.get('red', [''])
red = int(red[0]) if red[0] else 0
```
if/else 조건식을 쓰면 코드를 명확하게 이해할 수 있다. 하지만 여러 줄에 걸친 if/else 문을 대체할 정도로 명확하지는 않다. 다음처럼 모든 로직을 펼치면 더 복잡해 보인다.

```python
green = my_values.get('green', [''])
if green[0]:
    green = int(green[0])
else:
    green = 0
```

이 로직을 반복 사용해야 한다면 헬퍼 함수를 만드는 것이 좋다.

```python
def get_first_int(values, key, default=0):
    found = values.get(key, [''])
    if found[0]:
        found = int(found[0])
    else:
        found = default
    return found
```

위의 헬퍼 함수를 쓰면 or를 사용한 복잡한 표현식이나 if/else 조건식을 사용한 두 줄짜리 버전을 쓸 때보다 호출 코드가 훨씩 더 명확해진다.

표현식이 복잡해지기 시작하면 최대한 빨리 표현식을 작은 조각으로 분할하고 로직을 헬퍼 함수로 옮기는 방안을 고려해야 한다. 짧은 코드보다 가독성을 선택하는 편이 낫다. 이해하기 어려운 복잡한 표현식에는 파이썬의 함축적인 문법을 사용하면 안된다.

## 핵심 정리

- 파이썬의 문법을 이용하면 한 줄짜리 표현식을 쉽게 작성할 수 있지만 코드가 복잡해지고 읽기 어려워진다.
- 복잡한 표현식은 헬퍼 함수로 옮기는 게 좋다. 특히, 같은 로직을 반복해서 사용해야 한다면 헬퍼 함수를 사용하자.
- if/else 표현식을 이용하면 or나 and 같은 bool 연산자를 사용할 때보다 읽기 수월한 코드를 작성할 수 있다.
