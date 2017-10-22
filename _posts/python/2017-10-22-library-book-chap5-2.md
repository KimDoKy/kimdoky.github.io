---
layout: post
section-type: post
title: Python Library - chap 5. 범용 OS/런타임 서비스 - 5.2 스트림 다루기
category: python
tags: [ 'python' ]
---
io 모듈은 I/O를 다루는 다양한 스트림 객체를 제공합니다. 스트림 객체 또는 file-like 객체라고 불리는 것들, 문자열, 바이트열 등의 객체를 파일과 같이 취급할 수 있습니다. 이 모듈이 제공하는 클래스는 다음과 같습니다.

- 문자열을 파일과 같은 인터페이스로 다루는 StringIO 클래스
- 바이트명을 파일과 같은 인터페이스로 다루는 BytesIO 클래스
- 기타, 스트림 객체의 추상 기반 클래스군

내장 함수 open()에 의해 생성되는 파일 객체도 데이터 조작 대상이 파일인 스트림 객체입니다. io 모듈은 파일 객체의 클래스나 이들의 기반 클래스도 제공하기 때문에, 평소에 인식하지는 못했지만 이 모듈의 덕을 본 경우가 많습니다.

## 인메모리 텍스트 스트림 다루기 - StringIO
io.StringIO 클래스로부터 생성되는 인스턴스는 문자열을 파일처럼 취급할 수 있습니다. 이는 파일 객체와는 달리 데이터를 메모리상에서 취급합니다.

### StringIO 클래스

형식 | class StringIO([initial_value=""][,newline='\n'])
---|---
설명 | 문자열을 파일처럼 취급한다.
인수 | initial_value - 초기값이 되는 문자열을 지정한다. <br> newline - 개행 문자를 지정한다.

### io.StringIO 클래스의 메서드

함수 이름 | 설명 | 반환값
---|---|---
read(size) | 스트림의 현재 오프셋으로부터 지정 크기까지의 문자열을 반환한다. | str
write(s) | 스트림에 문자열을 쓴다. | int
tell() | 현재 오프셋을 반환한다. | int
seek(offset, whence=SEEK_SET) | 오프셋을 지정 위치로 이동한다. offset은 whence로 지정한 위치에 대한 상대 위치가 된다. <br> whence에 지정할 수 있는 값은 다음과 같다. <br> SEEK_SET - 스트림의 맨 앞을 가리킨다. 오프셋에는 0 또는 양수 값을 지정할 수 있다. <br> SEEK_CUR - 현재의 스트림 위치를 가리킨다. 오프셋에는 양수나 음수 값을 지정할 수 있다. <br> SEEK_END - 스트림의 맨 끝을 가리킨다. 오프셋에는 0 또는 음수 값을 지정할 수 있다. | int
getvalue() | 스트림이 가진 모든 내용을 문자열로 반환한다. | str
close() | 스트림을 닫는다. 닫은 뒤에 스트림을 조작하면 예외가 발생한다. | None

### StringIO 의 기본적인 사용법

```python
>>> import io
>>> stream = io.StringIO("this is test\n")  #  초기값을 줄 수 있다.
>>> stream.read(10)  # 스트림으로부터 지정한 크기만큼 읽어온다.
'this is te'

>>> stream.tell()  # 현재 오프셋을 반환한다.
10

>>> stream.seek(0, io.SEEK_END)  # 오프셋을 스트림 맨 끝으로 변경한다.
13

>>> stream.write('test')  # 스트림에 문자열을 쓴다.
4

>>> print(stream.getvalue())  # 스트림이 가진 모든 내용을 반환한다.
this is test
test

>>> stream.close()  # 스트림을 닫는다.
>>> stream.write('test')  # 닫은 뒤에 쓰려고 하면 예외가 발생한다.
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: I/O operation on closed file
```

## 단위 테스트 활용 예
io 모듈을 활용하여 단위 테스트로 사용할 수 있습니다. 스트림 객체는 다음과 같은 용도로 이용할 수 있습니다.

- 파일 객체 대신 사용
- 표준 출력 등을 캡쳐할 때

### StringIO를 이용한 표준 출력 캡쳐

```python
>>> import io
>>> from unittest.mock import patch
>>> def print_hoge():
...     print('hoge')  # print()는 sys.stdout.write()와 같음
...
>>> @patch('sys.stdout', new_callable=io.StringIO)  # 표준 출력을 StringIO로 대체
... def test_print_hoge(mocked_object):  # mocked_object가 대체한 후의 스트림
...     print_hoge()
...     assert mocked_object.getvalue() == 'hoge\n'  # 스트림에 쓰인 내용을 검증함
...
>>> test_print_hoge()
```

표준 출력을 표시하는 파일 객체 sys.stdout과 file-like 객체인 io.StringIO는 거의 같은 인터페이스를 가지고 있기 때문에 대체할 수 있습니다.
