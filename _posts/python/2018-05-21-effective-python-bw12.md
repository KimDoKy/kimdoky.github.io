---
layout: post
section-type: post
title: EFFECTIVE PYTHON - for와 while 루프 뒤에는 else 블록을 쓰지 말자
category: python
tags: [ 'python' ]
---

루프에서 반복되는 내부 블록 바로 다음에 else 블록을 둘 수 있는 기능이 있다.

```python
>>>
>>>
>>> for i in range(3):
...     print('Loop %d' % i)
... else:
...     print('Else block!')
...
Loop 0
Loop 1
Loop 2
Else block!
```
`if/else`문에서 else는 '이전 블록이 실행되지 않으면 이 블록이 실행된다'는 의미이다.  
`try/except` 문에서 except도 마찬가지로 '이전 블록에서 실패하면 이 블로기 실행된다'고 정의할 수 있다.  

비슷하게 `try/except/else`의 else도 '이전 블록이 실패하지 않으면 실행하라'는 뜻이므로 이 패턴을 따른다. `try/fanally`도 '이전 블록을 실행하고 항상 마지막에 실행하라'는 의미이다.

루프에서 `break` 문을 사용해야 else 블록을 건너뛸 수 있다.

```python
>>> for i in range(3):
...     print('Loop %d' % i)
...     if i == 1:
...         break
... else:
...     print('Else block!')
...
Loop 0
Loop 1
```

빈 시퀀스를 처리하는 루프문에서도 else 블록이 즉시 실행된다.

```python
>>> for x in []:
...     print('Never runs')
... else:
...     print('For Else block!')
...
For Else block!
```

else 블록은 while 루프가 처음부터 거짓인 경우에도 실행된다.

```python
>>> while False:
...     print('Never runs')
... else:
...     print('While Else block!')
...
While Else block!
```

이렇게 동작하는 이유는 루프 다음에 오는 else 블록은 루프로 뭔가를 검색할 때 유용하기 때문이다.  

예를 들어 두 숫자가 서로소(coprime:공약수가 1밖에 없는 둘 이상의 수)인지를 판별한다. 가능한 모든 공약수를 구하고 숫자를 테스트한다. 모든 옵션을 시도한 후 루프가 끝난다. else 블록은 루프가 break를 만나지 않아서 숫자가 서로소일 때 실행된다.

```python
>>> a = 4
>>> b = 9
>>> for i in range(2, min(a, b) + 1):
...     print('Testing', i)
...     if a % i == 0 and b % i == 0:
...         print('Not coprime')
...         break
... else:
...     print('coprime')
...
Testing 2
Testing 3
Testing 4
coprime
```

실제로는 이런 방식으로 코드를 작성하면 안된다. 대신 헬퍼 ㅎ마수를 작성하는 것이 좋다.
이런 헬퍼 함수는 두 가지 일반적인 스타일로 작성한다.

1. 찾으려는 조건을 찾았을 때 바로 반환하는 것.
루프가 실패로 끝나면 기본 결과(True)를 반환한다.

```python
def comprime(a, b):
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            return False
    return True
```

2. 루프에서 찾으려는 대상을 찾았는지 알려두는 결과 변수를 사용하는 것.
뭔가를 찾았으면 즉시 break로 루프를 중단한다.

```python
def comprime(a, b):
    is_coprime = True
    for i in range(2, min(a, b) + 1):
        if a % i == 0 and b % i == 0:
            is_coprime = False
            break
    return is_coprime
```

이 두가지 방법을 적용하면 낯선 코드를 접하는 개발자들이 코드를 훨씬 쉽게 이해할 수 있다. else 블록을 사용한 표현의 장점이 나중에 자신을 비롯한 코드를 이해하려는 사람들이 받을 부담감을 줄일 수 있다. 루프 다음에 오는 else 블로은 **절대로 사용하지 말아야 한다.**

## 핵심 정리

- 파이썬에는 for와 while 루프의 내부 블록 바로 뒤에 else 블록을 사용할 수 있게 하는 특별한 문법이 있다.
- 루프 본문이 break 문을 만나지 않은 경우에만 루프 다음에 오는 else 블록이 실행된다.
- 루프 뒤에 else 블록을 사용하면 직관적이지 않고 혼돈하기 쉬우니 사용하지 말아야 한다.
