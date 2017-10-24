---
layout: post
section-type: post
title: Python Library - chap 5. 범용 OS/런타임 서비스 - 5.4 명령줄 옵션과 인수 다루기
category: python
tags: [ 'python' ]
---

argparse 모듈은 UNIX 계열 운영체제의 관례에 따라 명령줄 옵션을 해석(parse)하는 기능을 제공합니다. argparse에는 인수를 정의하여 명령의 도움말(help) 표시를 자동으로 생성하는 기능이 있으며, 최소한의 코드로도 사용자가 쉽게 명령줄 도구를 작성할 수 있습니다.  

argparse 모듈과 마찬가지로 명령줄 옵션의 해석을 목적으로 하는 모듈로는 getopt와 optparse 모듈이 있습니다.  

getopt는 C 언어의 getopt() 함수에 익숙한 사용자를 위해 디자인된 API를 가지고 있습니다. getopt 모듈과 비교해보면 argparse 모듈은 더 적은 코드로 명령줄 옵션을 해석할 수 있습니다.  

optparse는 이미 폐지가 결정되었기 때문에 더이상 업데이트 되지 않습니다. 따라서, argparse 모듈을 사용해야 합니다.

## 명령줄 옵션 다루기
두 개의 명령줄 인수를 갖는 스크립트를 예로 argparse 모듈의 사용법을 설명합니다. 인수 하나는 문자열, 나머지 하나는 정수를 받으며 지정된 수만큼 반복하여 문자열을 표시하기만하는 단순한 스크립트입니다.  

### parser의 작성과 옵션
다음 코드는 argparse 모듈을 사용하여 명령줄 옵션을 정의하고, 주어진 인수를 해석하여 해석된 값을 가지고 간단한 처리를 실행하는 예입니다.

```python
import argparse

# parser의 인스턴스 작성
parser = argparse.ArgumentParser(description='Example command')
# 문자열을 받는 -s 옵션을 정의
parser.add_argument('-s', '--string', type=str, help='string to display', required=True)
# 수치를 받는 -n 옵션을 정의
parser.add_argument('-n', '--num', type=int, help='number of time repeatedly display the string', default=2)
# 인수를 해석(parse)하여 얻어진 값을 변수에 저장
args = parser.parse_args()

print(args.string * args.num)
```

샘플 코드에서는 parser를 작성하여 문자열을 취하는 -s와 수치를 구하는 -n이라는 두 개의 인수를 정의했습니다. 취한 인수는 parser.parse_args()가 실행된 시점에 해석되며, 정상적으로 해석되면 그 결과를 반환합니다. 샘플 코드의 인수 정의를 해석하면 --stirng 이나 --num과 같은 긴 옵션과 같은 이름으로 값이 저장되므로, args.string이나 args.num으로 값에 접근할 수 있습니다.

### ArgumentParser의 초기화 인수
전체 동작은 parser를 초기화할 때 인수로 지정할 수 있습니다.

인수 이름 | 설명 | 기본값
---|---|---
prog | 프로그램 이름을 지정한다. | sys.args[0]
usage | 프로그램의 이용 방법을 문자열로 지정한다. | parser에 주어진 인수로부터 생성
description | 인수의 help 앞에 표시되는 문자열을 지정한다. | None
epilog | 인수의 help 뒤에 표시되는 문자열을 지정한다. | None
parents | ArgumentParser 객체의 리스트를 지정한다. 이 리스트에 포함된 객체의 인수가 추가된다. | []
formatter_class | help로 표시되는 포맷을 커스터마이징하기 위한 클래스를 제공한다. | argparse.HelpFormatter
prefix_chars | 인수의 맨 앞 문자를 지정한다. 보통 -o이나, 예를 들어 +를 지정하면 +o와 같이 지정된다. | '-'
fromfile_prefix_chars | 파일에 기술된 인수를 읽어올 때 맨 앞글자를 지정한다. 예를 들어 \@를 지정하면 \@file.txt와 같이 파일을 지정할 수 있다. | None
argument_default | parser 전체에 적용되는 인수의 기본값을 지정한다. | None
conflict_handler | 1회 명령을 호출하여 어떤 옵션이 여럿 지정되었을 때의 동작을 지정한다. 기본값은 오류가 된다. | 'error'
add_help | -h 옵션을 parser에 추가할지 여부를 지정한다. | True

앞선 샘플 코드를 repeat.py로 저장하여, 어떻게 동작하는지 셸에서 실행시켜 확인합니다.

### 인수가 부족할 때

```python
인수 없이 실행함.
-s는 필수 옵션이므로 실행 오류가 됨
$ python repeat.py
usage: repeat.py [-h] -s STRING [-n NUM]
repeat.py: error: the following arguments are required: -s/--string
```

인수 -s가 필요하다는 오류가 표시되었습니다. 이것은 parser.add_argument()로 인수를 정의할 때 -s가 필수(required=True)라고 지정했기 때문입니다.
