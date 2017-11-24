---
layout: post
section-type: post
title: Python Library - chap 11. 테스트와 디버깅 - 9. 로그 출력하기
category: python
tags: [ 'python' ]
---

`logging` 모듈은 로그 출력에 관한 기능을 제공합니다.

## 세 가지 로깅 설정 방법

### 로깅 기능을 이용하는 방법

이용 방법 | 적절한 용도
---|---
logging으로 루트 로거를 설정한다. | 한 모듈로만 구성되는 소규모 소프트웨어
로거와 핸들러 등을 조합한 모듈 방식으로 설정한다. | 여러 모듈로 구성되는 중-대규모 소프트웨어
dictConfig()등을 사용하여 특정 자료구조에서 일괄적으로 설정한다. | 여러 모듈로 구성되는 중-대규모 소프트웨어

> #### 모듈 방식과 dictConfig, 어느 쪽을 사용할까?  
dictConfig는 구조적으로 읽기 쉬운 로길 설정을 작성할 수 있으나 dict으로부터 일괄적으로 설정하기 때문에, 특히 대화 모드 등에서 조금씩 작성하여 동작시키는 것과 같은 방식에는 적합하지 않습니다. 반면 코드로 설정하는 모듈 방식은 다소 길게 작성해야 하지만, 짧은 모드에서도 동작을 확인할 수 있습니다.  
따라서 로거나 핸들러 등을 사용한 짧은 코드로 로깅 설정을 다양하게 테스트해보며 로깅에 익숙해지고 나서, 코드를 dictConfig로 대체하는 방법을 추천합니다.

## 표준으로 정의된 로그 레벨
Python 로깅 기능에는 표준으로 6개의 로그 레벨이 정의되어 있습니다. 또한 NOTSET을 제외하고 각각의 로그 레벨을 사용하여 메시지를 출력하는 메서드가 있습니다.

### 표준 포그 레벨과 대응 메서드

로그 레벨 | 값 | 메서드
---|---|---
CRITICAL | 50 | logging.critical()
ERROR | 40 | logging.error()
WARNING | 30 | logging.warning()
INFO | 20 | logging.info()
DEBUG | 10 | logging.debug()
NOTSET | 0 | 대응하는 메서드 없음

로그 레벨을 지정함으로써, 지정한 로그 레벨보다 낮은 값을 가진 로그 레벨 메시지의 출력을 제한할 수 있습니다.  

## logging 모듈에서 로그 다루기

### 간단한 로그 출력 예

```Python
>>> import logging
>>> logging.debug('debug message')  # 로그 레벨로 인해 출력되지 않음
>>> logging.warning('warning message')  # 출력됨
WARNING:root:warning message
```

import 직후 logging 모듈에서 로그 출력 메서드를 호출하면, 로그 출력은 다음과 같이 동작합니다.

- 메시지는 표준 오류 출력된다.
- 출력 포맷은 <로그 레벨>:<로거 이름>:<메시지>이다.
- 로그 레벨은 logging.WARNING으로 설정되어 있다.

## 로그 메시지에 변수를 출력하는 예
로그 메시지에 변숫값을 출력합니다. 두 번째 이후의 인수 값이 메시지의 포맷 문자열로 치환됩니다.

```Python
>>> import logging
>>> favorite_thing = 'bouldering'
>>> logging.error('I love %s!', favorite_thing)  # %가 변수의 값으로 치환된다.
ERROR:root:I love bouldering!
```

출력 위치나 메시지 출력 포맷, 로그 레벨 등의 로깅 동작을 변경하고 싶을 때는 logging.basicConfig()를 사용합니다. logging.basicConfig()에는 다음 인수를 전달할 수 있습니다.

### logging.basicConfig()의 인수

인수 | 내용
---|---
filename | 출력 파일 이름을 지정한다.
filemode | 파일을 열 때 모드를 지정한다.
format | 지정한 로그 포맷으로 출력한다.
datefmt | 지정한 일시 포맷을 사용한다.
style | format으로 쓸 수 있는 세 종류의 스타일 중 하나를 지정한다. <br> '%' : % 스타일 <br> '{' : str.format() 스타일 <br> '$' : string.Template 스타일
level | 로그 레벨의 임계 값을 지정한다.
stream | 지정한 스트림을 사용한다. filename과 동시에 지정할 수 없다.
handlers | 사용할 핸들러의 리스트를 지정한다. filename, stream과 동시에 지정할 수 없다.

### logging.basicConfig()로 로깅 동작 변경하기

```Python
>>> logformat = '%(asctime)s %(levelname)s %(message)s'
>>> logging.basicConfig(filename='/tmp/test.log',  # 출력 대상 변경
                        level=logging.DEBUG,  # 로그 레벨 변경
                        format=logformat)  # 출력 포맷 변경

>>> logging.debug('debug message')
>>> logging.info('info message')
>>> logging.warning('warning message')
```

### /tmp/test.log의 출력 내용
위 코드를 실행하면 출력 위치가 변경되므로 /tmp/test.log에 다음 내용이 출력됩니다.

```
$ cat /tmp/test.log
2017-11-22 00:05:58,459 DEBUG debug message
2017-11-22 00:06:10,397 INFO info message
2017-11-22 00:06:24,648 WARNING warning message
```

로깅 동작을 변경한 내용이 반영된 메시지가 출력되었습니다.

- 출력 포맷을 변경함으로써, 맨 처음에 날짜를 포함한 포맷으로 메시지가 출력되었다.
- 로그 레벨을 logging.DEBUG로 설정함으로써, DEBUG 레벨과 INFO 레벨의 로그가 출력되었다.

### 로그 포맷에 사용할 수 있는 속성

이름 | 포맷 | 설명
---|---|---
asctime | %(asctime)s | "2017-11-21 12:00:23,123" 형식의 시각
filename | %(filename)s | pathname의 파일 이름 부분
funcName | %(funcName)s | 로깅 호출을 포함한 함수 이름
levelname | %(levelname)s | 로그 레벨을 가리키는 문자열
lineno | %(lineno)s | 로깅을 호출하는 파일 내의 행 수
module | %(module)s | 모듈 이름(filename의 이름 부분)
message | %(message)s | 로그 메시지
name | %(name)s | 로깅에 사용된 로거의 이름
pathname | %(pathname)s | 로깅을 호출한 파일의 전체 경로
process | %(process)s | 프로세스 ID
thread | %(thread)s | 스레드 ID

## 모듈 방식으로 로깅 설정하기
logging 모듈은 앞의 기본적인 사용법 외에도, 몇 가지 부품을 조합하여 유연하게 로깅을 구성할 수 있습니다.

### 로깅을 구성하는 부품

이름 | 내용
---|---
로거 | 로그 출력 인터페이스를 제공한다.
핸들러 | 로그의 송신 대상을 결정한다.
필터 | 로그의 필터링 기능을 제공한다.
포메터 | 로그 출력 포맷을 결정한다.

예를 들면 다음처럼 구성할 수 있습니다.

- 하나의 로그에 여러 개의 핸들러를 설정한다.
ex) 로거에 메시지를 넘길 때, 콘솔과 파일 두 개의 대상에 로그를 출력하고 싶을 때.
- 두 개의 로거에 각각 다른 핸들러를 설정한다.
ex) 로거 A에 메시지를 넘길 때는 로그 파일에 출력하지만, 로거 B에 넘길 때는 메일을 송신하고 싶을 때.

### 부품 조합에 따른 로깅 설정

```Python
# 로거 작성
>>> logger = logging.getLogger('hoge.fuga.piyo') # hoge.fuga.piyo라는 이름을 설정함
>>> logger.setLevel(logging.INFO)  # INFO 레벨 이상의 로그는 출력하나, DEBUG 레벨 로그는 출력되지 않음

# 핸들러 작성
>>> handler = logging.FileHandler('/tmp/test.log') # 파일을 출력 대상으로 하는 핸들러를 작성
>>> handler.setLevel(logging.INFO)

# 필터 작성
>>> filter = logging.Filter('hoge.fuga')  # 로거 이름이 hoge.fuga에 일치할 때만 출력하는 필터를 생성(위 로거는 일치함)

# 포매터 작성
>>> formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 조합
>>> handler.setFormatter(formatter)  # 핸들러에 포매너를 설정
>>> handler.addFilter(filter)  # 핸들러에 필터를 설정
>>> logger.addHandler(handler)  # 로거에 핸들러를 설정
>>> logger.addFilter(filter)  # 로거에 필터를 설정

# 로그 출력
>>> logger.debug('debug message')
>>> logger.info('info message')
```

로그 레벨 필터는 로거와 핸들러에 의해 동작합니다.  INFO 레벨 로그를 출력하도록, 로거와 핸들러 양쪽에 로그 레벨을 설정하였습니다.  

출력 대상이 파일이므로 앞선 코드에서는 logging.FileHandler 클래스를 이용했습니다. 이외에도 logging 모듈과 logging.handlers 모듈에는 다양한 핸들러 클래스가 마련되어 있습니다.  

일시를 포함한 포맷으로 로그를 출력하기 위해 포맷을 작성하였습니다. 포매터는 공식문서 "[LogRecord attributes](https://docs.python.org/3/library/logging.html)"룰 첨고하세요.

### 로거의 계층 구조
로거를 생성하는 logging.getLogger()에는 인수로 로거 이름을 전달할 수 있습니다. 이로 이름의 문자열에 dot가 포함되면, 계층 구조가 만들어집니다. 앞의 예는 다음과 같은 계층이 만들어 집니다.

#### 로거의 계층 구조

![]({{site.url}}/img/post/python/library/11.3.png)

hoge.fuga.piyo의 부모 로거는 hoge.fuga이며, 그 부모는 hoge입니다. 모든 로거의 계층 구조에는 공통 부모 로거가 존재하며 이것을 "루트 로거"라고 합니다.  

### 로거의 계층 구조를 이용한 관용구

또한 로거의 계층 구조를 이용한 자주 쓰이는 관용구 입니다.

```Python
import logging
logger = logging.getLogger(__name__)
```

\__name__은 모든 패키지나 모듈의 구조가 문자열로 저장되어 있기 때문에, 로거 이름을 보면 어느 패키지/모듈에서 출력한 로그인지 알 수 있습니다. 로거 이름을 \__name__으로 하는 로거를 "모든 레벨 로거"라고 합니다.

#### 계층 구조를 이용한 로깅 일괄 설정

자식 로거는 메시지를 부모 로거의 핸들러에 전달합니다. 이를 이용하여 특정 계층 다음에 있는 특정 이름을 가진 로거에 공통 설정을 적용할 수 있습니다.

- logging.getLogger('hoge.guga')
- logging.getLogger('hoge.piyo')

앞선 로거는 메시지를 받으면 자신의  로거로 설정된 핸들러에 메시지를 남김니다. 이때 부모인 hoge 로거에 메시지를 전달하며, hoge 로거에 설정된 핸들러를 사용하여 로그 출력을 시도합니다. 따라서 hoge 로거에 대하여 핸들러를 설정해 두면 hoge.fuga와 hoge.piyo가 같은 핸들러를 사용할 수 있습니다.  

메시지가 자식 로거로부터 부모 로거로 전달되는 성질과 모듈 레벨 로거를 조합하면, 특정 패키지/모듈 다음의 로거에 대해 간단히 공통 로깅을 설정할 수 있습니다.

### 필터를 통한 로그 출력 제어

logging.Filter('hoge.fuga')와 같이 생성된 필터는 로거나 핸들러에 설정하여 로그 레벨과는 다른 기준을 적용하는 필터링 기능을 제공합니다.  

필터는 로거의 이름에 따라 필터링을 실행합니다. 샘플 코드에서는 로거 이름으로 'hoge.fuga'을 필터링 지정하였습니다. 로거 이름이 'huge.fuga' 다음의 계층일 때 출력을 허가합니다.(ex. huge.fuga, hoge.fuga.piyo 등)

## 사전이나 파일로 로깅 설정하기

Python 로깅 기능에는 로거와 핸들러, 포맷 외에도, logging.config 모듈에서 dict 객체나 파일로써 로깅 설정을 작성하는 방법도 제공합니다.  

### 사전 객체로 설정하기 - dictConfig()

logging.config.dictConfig()는 사전 형식으로 작성한 설정 정보로 로깅을 설정할 수 있습니다.

### logging.config.dict()

형식 | logging.config.dictConfig(config)
---|---
설명 | dict 형식으로 작성한 설정 정보로 로깅을 설정한다.
인수 | config - 로깅 설정을 작성한 dict를 지정한다.

### dictConfig를 사용한 로깅 설정 예

```Python
import logging
from logging.config import dictConfig
config = {
    'version' 1,  # dictConfig의 버전, 1만 지원됨
    'disable_existing_loggers': False,  # False이면 기존 로깅 설정을 무효화하지 않는다.
    'formatters': {  # 포매터 설정을 구성하는 dict
        'example': {  # 포매터 이름
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 포맷 문자열
        },
    },
    'filters': {  # 필터 설정을 구성하는 dict
        'hoge-filter': {  # 필터 이름
            'name': 'hoge.fuga',  # 필터 대상 로거 이름
        },
    },
    'handlers': {  # 핸들러를 구성하는 dict
        'file': {  # 핸들러 이름
            'level': 'INFO',  # 핸들러의 로그 레벨 지정
            'class': 'logging.FileHandler',  # 핸들러의 클래스
            'filename': '/tmp/test.log',  # 출력 파일 경로
            'formatter': 'example',  # 핸들러에 설정하는 포매터 이름
            'filters': ['hoge-filter'],  # 핸들러에 설정하는 필터 이름 리스트
        },
    },
    'loggers': {  # 로거 설정을 구성하는 dict
        'hoge': {  # 로거 이름
            'handlers': ['file'],  # 로거가 이용하는 핸들러 이름의 리스트
            'level': 'INFO',  # 로거의 로그 레벨
            'propagate': True,  # True이면 자식 로거에 설정을 전달함
        },
    },
}
dictConfig(config)
logger = logging.getLogger('hoge.fuga.piyo')
logger.debug('debug message')
logger.info('info message')
```
"부품 조합에 따른 로깅 설정"과 같은 설정을 dictConfig()에 대응하는 포맷으로 치환한 예입니다.  

disable_existing_loggers가 True이면(기본값), 그 이전의 로깅 설정은 무효화되므로 주의해야합니다.  


dictConfig의 좋은 코드 예는, Django의 설정 파일에 LOGGING의 값입니다. dictConfig()의 포매터에 근거하여 작성되어 있습니다.  <https://docs.djangoproject.com/en/1.11/topics/logging/#examples>

### 파일로부터 설정 읽어오기 - fileConfig()
fileConfig()를 사용하면 파일에 작성된 내용에 근거하여 로깅을 설정합니다. fileConfig()는 dictConfig()와 달리 필터를 설정할 수 없습니다.

#### logging.config.fileConfig()

형식 | logging.config.fileConfig(fname, defaults=None, disable_existing_loggers=True)
---|---
설명 | configparser 형식의 파일에 작성한 설정 정보로부터 로깅을 설정한다.
인수 | fname - 설정 파일 이름을 지정한다. <br> defaults - ConfigParser에 전달할 기본값을 지정한다. <br> disable_existing_loggers - True이면 이 함수를 호출하기 이전의 로깅 설정을 무효화한다.

fileConfig는 dictConfig보다 오래되었기 때문에 기능 추가는 dictConfig에만 이루어질 예정이므로, dictConfig를 사용할 것을 권장합니다.

> #### Sentry - 오류 탐지, 디버깅을 위한 강력한 아군  
서비스 환경에서 로그를 운용할 때는 '여러 개의 서버에서 출력된 로그를 어떻게 집약할 것인가?', '발생한 오류를 어떻게 탐지할 것인가?'라는 문제가 발생합니다. 이를 위한 수단으로, Sentry라는 웹 서비스가 있습니다.  
Sentry는 오류 추적(Error tracking)를 주목적으로 하는 로그 집약 서비스입니다. 로그를 출력하는 서버가 클라이언트가 됩니다. HTTP 등의 네트워크 프로토콜을 통해 Sentry 서버에 로그를 송신하면, 같은 종류의 로그 집약이나 dict에 등록되어 있던 메일 주소에 대한 통보 등을 수행합니다. Sentry 자체도 Python으로 작성된 소프트웨어입니다.  
Sentry와 비슷한 서비스로 Airbrake나 Buganag등이 있는데, Python으로 웹 서비스를 개발하는 기업에서 만든 것이기 때문에 Python과 잘 맞는 편입니다.(다양한 언어를 지원하지만 Python 클라이언트 기능이 가장 좋습니다.)  
Sentry의 Python용 클라이언트 라이브러리인 raven-python은 logging에 준거한 핸들러를 제공하거나 기존 로깅 구현을 쉽게 적용할 수 있습니다.
