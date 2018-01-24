---
layout: post
section-type: post
title: python 3.6으로 exe파일 만들기
category: tip
tags: [ 'tip' ]
---

아직 windows OS가 주류이기 때문에 exe 파일로 만들 필요가 있습니다.

python 으로 코딩한 파일을 exe으로 변환하기 위해 `cx_freeze`을 설치해 줍니다.

> `cx_freeze 5.0.2` 에서 테스트 되었습니다.

```
pip install cx_freeze         # 최신 버전 설치
pip install cx_freeze==5.0.2  # 특정 버전 설치
```

아래와 같이 셋팅파일을 작성합니다.

```python
# setup.py (filename은 편할대로 하세요.)
import sys
from cx_Freeze import setup, Executable

setup(
		name="Demo",
		version="1.0",
		description = "테스트 파일",
		author = "makingfunk",
		executables = [Executable("mbcCheck.py")])
```

> 라이브러리(bs4)가 포함된 파일로 테스트 하기 위해 기존에 만들었던 크롤링 파일로 테스트 하였습니다. <https://github.com/KimDoKy/otherprogram>

```
python setup.py build  # 폴더 형식
python setup.py install  # 설치
```

>
기존의 `bdist_msi`는 `install`으로 변경된 것 같습니다.

이대로 실행하면 파일이 생성되는데 실행해보면 라이브러리가 없어 프로세스가 종료됩니다.

라이브러리를 포함시키려면 파일을 생성하는 환경을 pyenv로 가상환경을 지정해주고 pip 로 필요한 라이브러리를 설치한 후 파일을 생성해주면 됩니다.

윈도우 컴이 현재 없어서 윈도우에서 아직 테스트를 못해봤습니다. 테스트 해보고 내용 추가 하겠습니다.
