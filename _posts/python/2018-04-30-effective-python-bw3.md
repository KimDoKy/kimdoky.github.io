---
layout: post
section-type: post
title: EFFECTIVE PYTHON - bytes, str, unicode의 차이점을 알자
category: python
tags: [ 'python' ]
---

Type | 파이썬 2 | 파이썬 3
---|---|---
binary | str | bytes
unicode | unicode | str

유니코드 문자를 바이너리 데이터로 표현하는 일반적인 인코딩은 UTF-8 이다. 하지만 파이썬 3의 str 인스턴스와 파이썬 2의 unicode 인스턴스는 연관된 바이너리 인코딩이 없다.

- 유니코드 -> 바이너리 : `encode` 메서드
- 바이너리 -> 유니코드 : `decode` 메서드

파이썬 프로그래밍을 할 때 외부에 제공할 인터페이스에서는 유니코드를 인코드하고 디코드해야 한다. 프로그램의 핵심 부분에선 유니코드 문자 타입을 사용하면, 출력 텍스트 인코딩(이상적으로 UTF-8)을 엄격하게 유지하면서 다른 텍스트 인코딩(Latin-1, Big5 등)을 쉽게 수용할 수 있다.  

문자 타입이 분리되어 있어서 부딪히는 상황이 있다.

- UTF-8(혹은 다른 인코딩)으로 인코드된 문자인 8비트 값을 처리하려는 상황
- 인코딩이 없는 유니코드 문자를 처리하려는 상황

이 경우 변환하고 코드에서 원하는 타입과 입력값의 타입이 정확히 일치하게 하려면 헬퍼 함수 2개가 필요하다.

#### python 3에서는 먼저 str이나 bytes를 입력으로 받고 str을 반환하는 메서드가 필요하다.

```python
def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value # str 인스턴스
```

#### 그리고 str이나 bytes를 받고 bytes를 반환하는 메서드도 필요하다.

```python
def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return vale # bytes 인스턴스
```


파이썬에서 8 비트 값과 유니코드 문자를 처리할 때는 중대한 이슈가 있다.
파이썬 3에서 내장 함수 `open`이 반환하는 파일 핸들을 사용하는 연산은 기본으로 UTF-8 인코딩을 사용한다는 점이다. 파이썬 2에서 파일 연산은 기본으로 바이너리 인코딩을 사용한다. 이 차이점은 문제가 될 수 있다.

```python
with open('/tmp/random.bin', 'w') as f:
    f.write(os.urandom(10))
>>>
TypeError: must be str, not bytes
```

문제가 일어나는 이유 : 파이썬 3의 `open`에 새 `encoding` 인수가 추가되었기 때문이다.
이 파미터의 기본값은 'utf-8'이다. 따라서 파일 핸들을 사용하는 `read`나 `write` 연산은 바이너리 데이터를 담은 `bytes` 인스턴스가 아니라 유니코드 문자를 담은 `str` 인스턴스를 기대한다.

위 코드를 해결하려면 쓰기 모드(`w`)가 아니라 바이너리 쓰기 모드(`wb`)로 오픈해야 한다.

```python
with open('/tmp/random.bin', 'wb') as f:
    f.write(os.urandom(10))
```

파일에서 데이터를 읽어올 때도 `r`이 아니 `rb`를 사용해야 한다.

## 핵심 정리

- 파이썬 3에서 bytes는 8비트 값을 저장하고, str은 유니코드 문자를 지정한다. `>`나 `+`와 같은 연산자에 bytes와 str 인스턴스를 함께 사용할 수 없다.
- 헬퍼 함수를 사용해서 처리할 입력값이 원하는 문자 시퀀스 타입(8비트 값, UTF-8 인코딩 문자, 유니코드 문자 등)으로 되어 있게 한다.
- 바이너리 데이터를 파일에서 읽거나 쓸 때는 파일을 바이너리 모드('rb' 혹은 'wb')로 오픈한다.
