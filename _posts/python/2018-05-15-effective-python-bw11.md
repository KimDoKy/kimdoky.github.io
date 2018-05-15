---
layout: post
section-type: post
title: EFFECTIVE PYTHON - 이터레이터를 병렬로 처리하려면 zip을 사용하자
category: python
tags: [ 'python' ]
---

파이썬에서 관련 객체로 구성된 리스트를 많이 사용한다.   

리스트 컴프리헨션을 사용하면 소스 리스트에 표현식을 적용하여 파생 리스트를 쉽게 얻을 수 있다.

```python
>>> names = ['Cecilia', 'Lise', 'Marie']
>>> letters = [len(n) for n in names]
>>> letters
[7, 4, 5]
```

피생 리스트의 아이템과 소스 리스트의 아이템은 서로 인덱스로 연관되어 있다. 따라서 두 리스트를 병렬로 순회하려면 소스 리스트인 names의 길이만큼 순회하면 된다.

```python
>>> longest_name = None
>>> max_letters = 0
>>> for i in range(len(names)):
...     count = letters[i]
...     if count > max_letters:
...         longest_name = names[i]
...         max_letters = count
...
>>> print(longest_name)
Cecilia
```

하지만 names와 letters를 인덱스로 접근하면 코드를 읽기 어려워진다. 루프의 인덱스 i로 배열에 접근하는 동작이 두번 일어난다. `enumerate`를 이용하면 약간 개선할 수는 있지만, 여전히 완벽하지 못하다.

```python
>>> for i, name in enumerate(names):
...     count = letters[i]
...     if count > max_letters:
...         longest_name = name
...         max_letters = count
```

퍄이썬은 좀 더 명료하게 하는 내장 함수 `zip`을 제공한다. `zip`은 지연 제어레이터로 이터레이터 두 개 이상을 감싼다. `zip` 제너레이터는 각 이터레이터로부터 다음 값을 담은 튜플을 얻어온다. `zip` 제너레이터를 사용한 코드는 다중 리스트에서 인덱스로 접근하는 코드보다 훨씬 명료하다.

```python
>>> for name, count in zip(names, letters):
...     if count > max_letters:
...         longest_name = name
...         max_letters = count
```


`zip` 함수를 사용할 때 두 가지 문제가 있다.

- 파이썬2에서 제공하는 `zip`은 제너레이터가 아니다. 제공한 이터레이터를 완전히 순회해서 zip으로 생성한 모든 튜플을 반환한다. 이 과정에서 메모리를 많이 사용하려 프로그램이 망가질 수 있다. 매우 큰 이터레이터를 사용하려면 `itertools`애 있는 `izip`을 사용해야 한다.

- 입력 이터레이터들의 길이가 다르면 `zip`이 이상하게 동작한다.
예를 들어 name 리스트에 다른 이름을 추가했지만 letters의 카운터를 업데이트하는 것을 잊었다면, 두 입력 리스트에 zip을 실행하면 예상치 못한 결과가 나온다.

```python
>>> names.append('DoKy')
>>> for name, count in zip(names, letters):
...     print(name)
...
Cecilia
Lise
Marie
```

새 아이템 'Doky'가 없다.  

`zip`은 감싼 이터레이터가 끝날 때까지 튜플을 계속 넘겨준다. 이 방식은 이터레이터들의 길이가 같을 때는 제대로 동작한다. 리스트 컴프리헨션에서 생성된 파생 리스트의 경우가 이에 해당한다. 그 외의 많은 경우에 `zip`의 동작은 오류를 야기할 수 있다. `zip`으로 실행할 리스트의 길이가 같다고 확신 할 수 없다면 내장 모듕 `itertools`의 `zip_longest`를 사용하는 방안을 고려해볼 수 있다.

## 핵심 정리

- 내장 함수 zip은 여러 이터레이터를 병렬로 순회할 대 사용할 수 있다.
- 파이썬 3의 zip은 튜플을 생성하는 지연 제어레이터다.
- 길이가 다른 이터레이터를 사용하면 zip은 그 결과를 조용히 잘라낸다.
- 내장 모듈 itertools의 zip_longest 함수를 쓰면 여러 이터레이터를 길이에 상관없이 병렬로 순회할 수 있다.
