---
layout: post
section-type: post
title: Python Library - chap 6. 파일과 디렉터리 접근하기 - 4. 파일 이름 매치와 경로 패턴 풀기
category: python
tags: [ 'python' ]
---
`fnmatch` 모듈은 파일 이름의 패턴 매치 기능을 제공하고, `glob` 모듈은 파일 경로의 패턴 풀기 기능을 제공합니다.  

`fnmatch` 모듈은 UNIX의 셸 형식으로 파일 이름 패턴 매치 기능을 제공합니다. `glob` 모듈은 내부에서 `fnmatch`를 이용하고 있습니다.  

`fnmatch`와 `glob`을 Windows에서 이용할 때도 매치에 사용할 수 있는 패턴은 UNIX 셸 형식입니다.

## 파일 이름 매치하기

### fnmatch 모듈의 메서드

함수 이름 | 설명 | 반환값
---|---|---
`fnmatch(filename, pattern)` | `filename`이 `pattern`과 일치하면 True, 그렇지 않으면 False를 반환한다. 운영체제가 대소문자를 구분하지 않으면 그에 따른다. | bool
`fnmatchcase(filename, pattern)` | 대소문자를 구분하여 매치한다. | bool
`filter(names, pattern)` | 파일 이름의 리스트로부터 패턴과 일치하는 요소만을 반환한다. | list
`translate(pattern)` | 패턴을 정규 표현 형식으로 변환한다. | str

같은 패턴으로 여러 번 매치할 때는 리스트를 생성해서 `filter()`를 적용하거나 `translate()`의 결과를 `re` 모듈로 컴파일하여 반복 사용하면 효율적으로 처리할 수 있습니다. `fnmatch()`가 호출될 때마다 내부에서 패턴 문자열을 셸 형식에서 정규 표현 형식으로 변환하여 매치하기 때문입니다.

### fnmatch 모듈의 샘플 코드

```python
>>> import fnmatch, re
>>> pattern = 'hoge??.py'  # ??는 임의의 두 문자와 매치
>>> fnmatch.fnmatch('Hoge01.py', pattern)
False  # 본래는 숫자는 ??에 일치하여 True가 나와야 하지만, 운영체제에 따라 다를 수 있다. 참고로 실습환경은 mac

>>> fnmatch.fnmatch('hoge01.py', pattern)
True  # 소문자로 했을때 숫자가 일치되어 True가 반환됨을 확인할 수 있다.

>>> fnmatch.fnmatchcase('Hoge01.py', pattern)
False  # 대소문자가 구분되어 일치하지 않음

>>> fnmatch.filter(['hoge.py', 'hoge00.py', 'hoge01.py', 'fuga01.py'], pattern)
['hoge00.py', 'hoge01.py']

>>> fnmatch.translate(pattern)  # 정규 표현 형식으로 변환
'hoge..\\.py\\Z(?ms)'

>>> re_pattern = re.compile(_)  # 패턴을 컴파일해서 재사용하는 예
>>> re_pattern.match('hogege.py')
<_sre.SRE_Match object; span=(0, 9), match='hogege.py'>
```

## 파일 경로의 패턴 풀기
`glob` 모듈은 UNIX의 셸 형식의 패턴으로 파일 경로를 매치하여, 일치한 모든 파일과 디렉터리의 경로를 반환합니다.

### glob 모듈의 메서드

함수 이름 | 설명 | 반환값
---|---|---
`glob(pathname)` | `pathname`에 주어진 패턴과 일치하는 파일이나 디렉터리 리스트를 반환한다. | list
`iglob(pathname)` | `glob()`과 같은 내용을 리스트가 아닌 발생자로 반환한다. | 발생자
`escape(pathname)` | ?, [, \* 등의 특수 문자를 이스케이프한다. | str

풀린 요소에 차례로 접근할 때는 발생자를 반환하는 `iglob()`을, 차례와 관계없이 접근할 때는 `glob()`을 사용하는 것이 좋습니다.  

지정하는 경로 이름에 ?나 \* 등의 특수 문자가 포함되면, 문자가 그대로 풀려버립니다. 문자열을 `escape()` 메서드를 사용하여 이스케이프하면 풀리지 않고 경로 이름으로서 처리됩니다.

### glob 모듈의 샘플 코드

```python
>>> import glob
>>> glob.glob('filesystem/*.rst')
['filesystem/fnmatch-glob.rst', 'filesystem/index.rst', 'filesystem/os-path.rst', 'filesystem/pathlib.rst', 'filesystem/tempfile.rst']
>>> glob.iglob('filesystem/*.rst')
<generator object _iglob at 0x101390a98>
>>> glob.escape('example?.txt')
'example[?].txt'
```
