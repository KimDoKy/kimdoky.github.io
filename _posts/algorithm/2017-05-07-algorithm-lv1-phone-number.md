---
layout: post
section-type: post
title: level 1. 핸드폰번호 가리기
category: algorithm
tags: [ 'algorithm' ]
---

# [level 1] 핸드폰번호 가리기

## 문제

별이는 헬로월드텔레콤에서 고지서를 보내는 일을 하고 있습니다. 개인정보 보호를 위해 고객들의 전화번호는 맨 뒷자리 4자리를 제외한 나머지를 "*"으로 바꿔야 합니다.  
전화번호를 문자열 s로 입력받는 hide_numbers함수를 완성해 별이를 도와주세요.  
예를 들어 s가 "01033334444"면 "*******4444"를 리턴하고, "027778888"인 경우는 "*****8888"을 리턴하면 됩니다.

## 내 답안

```python
def hide_numbers(s):
    #함수를 완성해 별이를 도와주세요
    r = ""
    for i in range(len(s)):
        if i < len(s) - 4:
            i = "*"
            r = r + i
        else:
            r = r + s[i]
    return r

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : " + hide_numbers('01033334444'));
```

#### 다른 사람의 답안

```python
def hide_numbers(s):
    #함수를 완성해 별이를 도와주세요
    return "*"*(len(s)-4) + s[-4:]

# 아래는 테스트로 출력해 보기 위한 코드입니다.
print("결과 : " + hide_numbers('01033334444'));
```

### 배울점, 느낀점

- 아직 초보니까... 괜찮아.

#### 출처
> <http://tryhelloworld.co.kr/challenge_codes/133>
