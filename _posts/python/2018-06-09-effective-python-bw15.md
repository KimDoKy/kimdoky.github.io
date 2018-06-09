---
layout: post
section-type: post
title: EFFECTIVE PYTHON - 클로저가 변수 스코프와 상호 작용하는 방법을 알자
category: python
tags: [ 'python' ]
---

### 선행 학습
- [closuer](https://github.com/KimDoKy/study/blob/jupyter/jupyter/python/Closure.ipynb)  

- [scope](https://github.com/KimDoKy/study/blob/jupyter/jupyter/python/scope.ipynb)

## 클로저가 변수 스코프와 상호 작용하는 방법을 알자

숫자 리스트를 정렬할 때 특정 그룹의 숫자들이 먼저오도록 우선순위를 매기는 것.  
이런 패턴은 사용자 인터페이스를 표현하거나, 다른 것보다 중요한 메시지나 예외 이벤트를 먼저 보여줘야 할 때 유용하다.  

일반적인 방법은 리스트의 `sort` 메서드에 헬퍼 함수를 key 인수로 넘기는 것이다.  
헬퍼의 반환 값은 리스트에 있는 각 아이템을 정렬하는 값으로 사용된다.  
헬퍼는 주어진 아이템이 중요한 그룹에 있는지 확인하고 그에 따라 정렬 키를 다르게 할 수 있다.

```python
def sort_priority(values, group):
  def helper(x):
    if x in group:
      return (0, x)
    return (1, x)
  values.sort(key=helper)
```

```
>>> numbers = [8, 3, 1, 2, 5,4, 7, 6]
>>> group = {2, 3, 5, 7}
>>> sort_priority(numbers, group)
>>> print(numbers)
[2, 3, 5, 7, 1, 4, 6, 8]
```

- 파이썬은 클로저(closuer)를 지원한다. 클로저는 자신이 정의된 스코프에 있는 변수를 참조하는 함수이다. 이 덕분에 `helper` 함수가 `sort_priority`의 `group` 인수에 접근할 수 있다.
- 함수는 파이썬에서 일급 객체(first-class object)다. 함수를 직접 참조하고, 변수에 할당하고, 다른 함수의 인수로 전달하고, 표현식과 if 문 등에서 비교할 수 있다는 뜻이다. 다라서 `sort` 메서드에서 클로저 함수를 key 인수로 받을 수 있다.
- 파이썬에는 튜플을 비교하는 특정한 규칙이 있다. 먼저 인덱스 0으로 아이템을 비교하고 그 후에 인덱스 1, 인덱스 2와 같이 진행하다. `helper ` 클로저의 반환 값이 정렬 순서를 분리된 두 그룹으로 나뉘게 한 건 이 규칙 때문이다.

함수에서 우선순위가 높은 아이템을 발견했는지 여부를 반환해서 사용자 인터페이스 코드가 그에 따라 동작을 추가.  
이미 각 숫자가 어느 그룹에 포함되어 있는지 판별하는 클로저 함수가 있다. 우선순위가 높은 아이템을 발견했을 때 플래그를 뒤집는 데 클로저를 사용하면, 함수는 클로저가 수정한 플래그 값을 반환할 것이다.

```python
def sort_priority2(numbers, group):
  found = False
  def helper(x):
    if x in group:
      found = True
      return (0, x)
    return (1, x)
  numbers.sort(key=helper)
  return found
```

```
>>> found = sort_priority2(numbers, group)
>>> print('Found: ', found)
Found:  False
>>> print(numbers)
[2, 3, 5, 7, 1, 4, 6, 8]
```

정렬은 잘 되었지만 found의 결과다 틀렸다. group에 속한 아이템을 numbers에서 찾을 수 있지만 함수는 False를 반환했다. 왜?

표현식에서 변수를 참조할 때 파이썬 인터프리터는 참조를 해결하려고 다음과 같은 순서로 스코프(scope: 유효범위)를 탐색한다.

1. 현재 함수의 스코프
2. (현재 스코프를 담소 있는 다른 함수 같은) 감싸고 있는 스코프
3. 코드를 포함하고 있는 모듈의 스코프(전역 스코프)
4. (`len`이나 `str`같은 함수를 잠고 있는) 내장 스코프

이 중 어느 스코프에도 참조한 이름으로 된 변수가 정의되어 있지 않으면 `NameError` 예외가 일어난다.  

변수에 값을 할당할 때는 다른 방식으로 동작한다.  
변수가 이미 현재 스코프에 정의되어 있다면 새로운 값을 얻는다. 파이썬은 변수가 현재 스코프에 존재하지 않으면 변수 정의로 취급한다. 새로 정의된 변수의 스코프는 그 할당을 포함하고 있는 함수가 된다.  

이 할당 동작이 sort_priority2의 잘못된 이유의 힌트이다.  
found 변수는 helper 클로저에서 True로 할당된다. 클로저 할당은 sort_priority2에서 일어나는 할당이 아닌 helper 안에서 일어나는 새 변수 정의로 처리된다.

```python
def sort_priority2(numbers, group):
  found = False
  def helper(x):
    if x in group:
      found = True
      return (0, x)
    return (1, x)
  numbers.sort(key=helper)
  return found
```

이 문제는 스코핑 버드(scoping bug)라고도 한다. 하지만 언어 설계자가 의도한 결과이다.  

이 동작은 함수의 지역 변수가 자신을 포함하는 모듈을 오염시키는 문제를 막아준다.  
그렇지 않았다면, 함수 안에서 일어나는 모든 할당이 전역 모듈 스코프에 쓰레기를 넣는 결과를 낳게 된다. 그렇게 되면 불필요한 할당 뿐만 아니라 결과로 만들어지는 전역 변수들의 상호 작용으로 알기 힘든 버그가 생겨버린다.

### 데이터 얻어오기
파이썬3에는 클로저에서 데이터를 얻어오는 특별한 문법이 있다.  
`nonlocal` 문은 특정 변수 이름에 할당할 때 스코프 탐색이 일어나야 함을 나타낸다. 유일한 제약은 `nonlocal`이 (전역 변수의 오염을 피하려고) 모듈 수준 스코프가지는 탐색할 수 없다는 점.

```python
def sort_priority3(numbers, group):
  found = False
  def helper(x):
    nonlocal found
    if x in group:
      found = True
      return (0, x)
    return (1, x)
  numbers.sort(key=helper)
  return found
```

`nonlocal`문은 클로저에서 데이터를 다른 스코프에 할당하는 시점을 알아보기 쉽게 해준다.  
`nonlocal`문은 변수 할당이 모듈 스코프에 직접 들어가게 하는 `global`문을 보완한다.  

하지마나 전역 변수의 안티패턴(anti-pattern)처럼 간단한 함수 이외에 `nonlocal`을 사용하지 않도록 주의해야 한다. `nonlocal`의 부작용은 알아내기가 어렵다. 특히 `nonlocal`문과 관련 변수에 대한 할당이 멀리 떨어진 긴 함수에서는 이해하기가 더욱 어렵다.  

`nonlocal`을 사용할 떄 복잡해진다면 헬퍼 클래스로 상태를 감싸는게 좋다.(`__call__` 검색 ㄱ)

```python
class Sorter(object):
  def __init__(self, group):
    self.group = group
    self.found = False

  def __call__(self, x):
    if x in self.group:
      self.found = True
      return (0, x)
    return (1, x)
```

```
>>> sorter = Sorter(group)
>>> numbers.sort(key=sorter)
>>> assert sorter.found is True
```

### 파이썬 2의 스코프
파이썬 2는 `nonlocal` 키워드를 지원하지 않는다. 하지만 파이썬2를 쓸 일은 없을 것을 판단되어, 나중에 필요하면 찾아보겠다.

## 핵심 정리

- 클로저 함수는 자신이 정의된 스코프 중 어디에 있는 변수도 참조할 수 있다.
- 기본적으로 클로저에서 변수에 할당하면 바깥쪽 스코프에는 영향을 미치지 않는다.
- 파이썬 3에서는 nonlocal 문을 사용하여 클로저를 감싸고 있는 스코프의 변수를 수정 할 수 있음을 알린다.
- 간단한 함수 이외에는 nonlocal 문을 사용하지 말자.
