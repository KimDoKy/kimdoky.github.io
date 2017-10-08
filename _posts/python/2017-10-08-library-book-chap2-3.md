---
layout: post
section-type: post
title: Python Library - chap 2. 수치 처리하기 - 2.3 의사 난수 다루기
category: python
tags: [ 'python' ]
---
random 모듈은 난수를 얻는 기능과 리스트나 튜플 등의 시퀀스 요소를 무작위로 얻는 기능을 가지고 있습니다.  

random의 난수 생성기는 Mersenne Twister 알고리즘을 채택해고 있습니다. C 언어의 rand() 함수나 Visual Basic의 Rad() 함수는 주기가 짧고 편차가 크거나 하는 문제가 있는 알고리즘을 채택하고 있는 것으로 알려졌으나, Mersenne Twister는 난수 생성기로서 높은 평가를 받는 알고리즘입니다.

## 난수 생성하기

### 난수 생성 함수

함수 이름 | 설명 | 반환값
---|---|---
random() | 0.0~1.0사이의 float형을 얻는다. | float
randint(x,y) | x~y 사이의 수치를 얻는다. x 또는 y에 float형을 지정하면 ValueError가 된다. | int
uniform(x,y) | x~y 사이의 수치를 얻는다. x 또는 y에 int형을 지정하더라도 float형으로 취급된다. | float

### 난수 생성

```python
>>> import random
>>> random.random()
0.48197776395679015

>>> random.randint(1,5)
5

>>> random.uniform(1,5)
3.7659256295187147
```

실험이나 기능 테스트를 수행할 때 수치는 난수로 취득하고 싶으나 재현성이 필요하다면, 난수 생성기의 초기화 함수 seed()를 사용해 시드를 고정하여 난수를 생성합니다.

### 시드 고정

```python
>>> random.seed(10) # 시드를 10으로 설정
>>> random.random()
0.5714025946899135

>>> random.seed(10) # 다시 시드를 10으로 설정
>>> random.random() # 앞과 같은 결과를 얻음
0.5714025946899135

>>> random.random() # 시드를 지정하지 않으면 다른 난수를 얻음
0.4288890546751146
```
seed()의 인수를 생략하면 시스템 시각이 사용됩니다.

## 특정 분포를 따르는 난수 생성기
단순히 난수를 생성하는 것뿐만 아니라 특정 분포에 따르는 난수도 생성할 수 있습니다.

### 특정 분포를 따르는 난수 생성 함수

함수 이름 | 설명 | 반환값
---|---|---
normalvariate(mu, sigma) | 평균 mu, 표준편차 sigma의 정규분포를 따르는 난수를 생성한다. | float
gammavariate(k, theta) | 형상모수 k, 척도모수 theta의 감마분포를 따르는 난수를 생성한다. | float

이 외에도 감마붙포나 로그 정규분포 등을 지원하는 함수가 있습니다.

### 특정 분포를 따르는 난수 생성

```python
>>> import random
>>> normal_variate = []
>>> gamma = []
>>> for i in range(10000):
...     normal_variate.append(random.normalvariate(0,1))
...     gamma.append(random.gammavariate(3,1))
```
생성된 난수 분포를 확인하고자 normalvariate() 함수와 gammavariate() 함수가 생성한 값 10,000개를 히스토그램으로 시각화한 그래프입니다.

![]({{site.url}}/img/post/python/library/2_3.png)

##### 위 히스토그램으로 시각화한 그래프 생성 코드

```python
import random
import matplotlib.pyplot as plt

normal_variate = []
gamma = []

for i in range(10000):
    normal_variate.append(random.normalvariate(0,1))
    gamma.append(random.gammavariate(3,1))

plt.hist(normal_variate, bins=350)
plt.show()

plt.hist(gamma, bins=350)
plt.show()
```

## 무작위로 선택하기
리스트나 집합 등의 시퀀스 내 요소를 무작위로 얻는 함수입니다.

### 무작위로 선택하는 함수

함수 이름 | 설명 | 반환값
---|---|---
choice(seq) | 시퀀스 seq의 요소를 하나 반환한다. | 시퀀스 내 요소
sample(population, k) | 모집단 population의 샘플 k개를 구하여 새롭게 리스트를 작성한다. | 샘플링된 리스트
shuffle(seq[, random]) | 시퀀스 seq의 요소 순서를 shuffle한다. | 없음

### 무작위 선택

```python
>>> l = [1,2,3,4,5]
>>> random.choice(l) # 시퀀스의 요소를 무작위로 하나 선택한다.
4

>>> random.sample(l,2) # 시퀀스의 요소로부터 2 번째 인수 개수로 된 리스트를 새로 생성한다.
[4, 2]

>>> random.shuffle(l) # shuffle() 은 원래 시퀀스의 요소 순서를 변경한다.
>>> l
[3, 1, 2, 4, 5]
```

sample() 함수는 한 번 추출한 요소는 다시 추출하지 않는 비복원 추출을 수행합니다. 어떤 시퀀스의 요소를 빠짐없이 무작위로 추출하고 싶다면 random.sample(l, len(l)) 과 같이 인수 k에 원래 시퀀스의 길이와 같은 수치를 작성합니다. 원본 시퀀스의 순서가 변경되어도 문제가 없다면 shuffle() 함수를 써도 괜찮습니다.
