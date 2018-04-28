---
layout: post
section-type: post
title: EFFECTIVE PYTHON - 사용 중인 파이썬의 버전을 알자
category: python
tags: [ 'python' ]
---

```
# 2 버전은 python, 3 이상은 python3 으로 실행한다.
# bash 옵션으로 변경이 가능하다.
$ python --version
Python 3.6.0
```

파이썬 내장 모듈 sys를 통해 알아낼 수도 있다.

```python
>>> import sys
>>> print(sys.version_info)
sys.version_info(major=3, minor=6, micro=0, releaselevel='final', serial=0)
>>> print(sys.version)
3.6.0 (default, May 23 2017, 19:05:55)
[GCC 4.2.1 Compatible Apple LLVM 8.1.0 (clang-802.0.42)]
```

## 핵심 정리

- 파이썬의 주요 버전인 파이썬 2, 파이썬 3 모두 여전히 활발히 사용된다.
- 파이썬의 CPython, Jython, IronPython, PyPy 같은 런타임이 있다.
- 시스템에서 파이썬을 실행하는 명령이 사용하고자 하는 파이썬 버전인지 확인해야 한다.
- 파이썬 커뮤니티에서 주로 다루는 버전은 파이썬 3이므로 새 파이썬 프로젝트를 시작할 때는 파이썬 3를 사용하는 편이 좋다.
