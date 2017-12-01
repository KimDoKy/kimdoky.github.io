---
layout: post
section-type: post
title: Python - File Object(파일 객체)
category: python
tags: [ 'python' ]
---

## 데이터를 영속성있게 저장하려면?
기본적으로 메모리 내 데이터 프로세스가 종료되면 내용은 날라갑니다.  
데이터를 계속 사용하려면 파일에 저장해야 합니다. 파이썬에서는 `open` 함수를 통해 파일 읽기/쓰기를 지원합니다.

## 파일 모드(Read, Write, Append)

- R : 기존 파일 읽기
- W or A : 새 파일 생성해서 쓰기. 지정된 경로에 파일이 없을 경우 같은 동작을 합니다.
- W : 기존 파일 내용 제거하고, 처음부터 쓰기
- A : 기존 파일에 추가하기

## 파일의 종류

- Text : 문자열 데이터. 문자열 데이터는 유니코드로 관리하게 되고, 사용하려면 특정 인코딩/디코딩을 하여 사용해야 합니다. 파이썬3에서는 `open()` 함수가 자동으로 인코딩/디코딩을 지원합니다.
- Binary : 바이너리 데이터
 - 자동 인코딩/디코딩을 수행하지 않습니다.(raw data 그대로 사용)
 - 문자열이 아닌, 이미지PDF/XLS 포맷 등
 - TEXT 테이터도 Binary로 열수 있음

## open [#doc](https://docs.python.org/3/library/functions.html#open)

open? 으로 도움말을 확인할 수 있습니다.  

### 자주 사용하는 옵션

- file_obj = open(파일경로, mode='rt', encoding=None, 그외옵션)
- readed_data = file_obj.read() # 파일 내용 처음부터 끝까지 모두 읽기
- file_obj.close()

- file object 주요 멤버함수
 - .write() : 파일에 쓰기
 - .read() :  파일 읽기
 - .close() : 파일 닫기

#### encoding 옵션

- 자동 인코딩/디코딩 옵션
- text mode 시에만 지정 가능. binary 모드에서는 지정불가
- 미지정시에는 OS 설정에 따라, 다른 인코딩이 지정
 - locale.getpreferredencoding(False)
 - 맥/리눅스 : utf-8 / 한글 윈도우 : cp949

#### 파일을 열 때, 5가지 모드

- r(read), w(write), a(append)
- 인코딩 모드
 - t(text) : 자동 인코딩/디코딩 모드
  - read() : 반환타입은 str
  - write() : str으로 자동 변환
 - b(binary) : 바이너리 모드
  - read() : 반환타입은 bytes
  - write() : bytes으로 자동 변환
- ex: rt(read + text), rb, wt, wb, at, ab

##### r(read)
`filecontent_unicode = open('filepath.txt', 'rt', encoding='utf-8').read()`  
'rt'를 사용할때 인코딩을 꼭 지정해주면 인코딩때문에 골치아픈 일을 방지할 수 있습니다.

- 지정 경로에 파일이 없을 경우 **IOError** 예외 발생
- 파일에 대한 읽기권한이 없으면 **PermissionError** 예외 발생

read()를 처음 사용하면 정상적으로 내용이 나오지만, 다시 실행하면 빈 내용이 출력됩니다. 파일 읽기의 커서가 파일의 내용을 모두 읽은후 맨 뒤에 위치하고 있기 때문에 빈 내용이 출력됩니다. 커서의 위치를 옮기려면 `seek()`함수를 사용하여 커서의 위치를 옮긴후 다시 read()를 사용하면 내용을 다시 읽어 올 수 있습니다.

바이너리에서는 수동으로 인코딩/디코딩('obj.read().decode('utf8')')을 사용할 수 있다.
(텍스트 모드는 자동으로 인코딩/디코딩)  

##### w(write)
`open('filepath.txt', 'wt', encoding='utf8').write('가나다')` # 유니코드 문자열(str)  

- 지정 경로에 파일이 없으면, 새 파일 생성
- 지정 경로에 파일이 있으면, 기존 파일 **무시** 하고 새 파일 생성
- 지정 경로에 파일은 있지만, 쓰기 권한이 없으면 **PermissionError** 예외 발생
- 지정 경로에 디렉터리가 없으면, **FileNotFoundError** 예외 발생

##### a(append)
`open('filepath.txt', 'at', encoding='utf8').write('가나다')` # 유니코드 문자열(str)  

- w(write)와 유사
- 지정 경로 파일이 존재하면, **해당 내용에 이어서 내용 추가**

##### t(text)
```python
with open('filepath.txt', 'wt', encoding='utf8') as f:
    f.write('가나다')
```

- 지정 **encoding** 으로, 자동 인코딩/디코딩과 함께 파일 쓰기/읽기
- `with`절을 사용하면 자동으로 파일을 닫아줍니다.

##### b(binary)

```Python
with open('filepath.txt', 'wb') as f:
    f.write('가나다'.encode('utf8')) # 바이너리니까 직접 인코딩을 지정해주어야 함.
```

- encoding 옵션 지정 불가
- 문자열이 아닌 파일을 읽어들일 때에는 인코딩/디코딩을 수행하면 안되므로, 필해 binary모드를 지정

```Python
with open('abc.jpg', 'rb') as f:
    photo_data = f.read()  # bytes 타입. 문자열이 아니기 때문에 인코딩/디코딩이 필요 없음
```

### 파일에 접근하는 다양한 방법

```Python
f = open('sample.txt', 'rt', encoding='utf8')
print(f.read())
f.close()

f = open('sample.txt', 'wt', encoding='utf8')
f.write('hello ')
print('world', file=f)  # file에 넘겨진 인자는 .write 멤버함수만 지원하면 됨
f.close()
```

파일을 닫기전에 예외가 발생하면 파일을 닫을 수가 없기 때문에 반드시 예외처리를 통해 닫아주어야 합니다.

```Python
f = open('sample.txt', 'wt', encoding='utf8')
try:
    f.write('hello ')
    1/0  # ZeroDivisionError 예외 발생
finally:  # 예외 발생여부 상관없이 무조건 실행
    f.close()
```

### with 절
```Python
with open('sample.txt', 'rt') as f:
    file_content = r.read()
```

- open함수에서 with절을 지원합니다.

### file object는 순회 가능(iterable)한 객체 [#ref](https://stackoverflow.com/questions/7395542/is-explicitly-closing-files-important)
줄(line) 단위로 순회
```Python
with open('sample.txt', 'rt', encoding='utf8') as f:
    for line in f:
        print(line)
```

- 파이썬은 소스코드를 실행하기 전에, 소스파일의 내용을 먼저 디코딩합니다. 소스코드 인코딩을 파이썬에게 잘못 알려주면, SyntaxError 예외가 발생합니다. 주석이라도 예외가 발생합니다.
