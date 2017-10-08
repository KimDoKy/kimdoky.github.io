---
layout: post
section-type: post
title: Python Library - chap 2. 수치 처리하기 - 2.4 통계 계산
category: python
tags: [ 'python' ]
---
통계 계산 기능을 제공하는 statistics 모듈에 대해 살펴봅니다. 통계 계산은 보통 NumPy나 SciPy가 잘 알려졌지만, statistics 모듈로도 간단한 통계 계산을 할 수 있습니다.

## 평균값과 중앙값 구하기
평균값, 중앙값, 최빈값 등은 데이터의 개요를 파악하는 중요한 지표가 됩니다.

### 평균값과 중앙값을 구하는 함수

함수 이름 | 설명 | 반환값
---|---|---
mean(data) | 데이터의 평균값을 구한다. | float
median(data) | 데이터의 중앙값을 구한다. | float
mode(data) | 데이터의 최빈값을 구한다. | float

### 평균값과 중앙값 구하기

```python
>>> import statistics
>>> data = [1,2,2,3,4,5,6]

>>> statistics.mean(data)
3.2857142857142856

>>> statistics.median(data)
3

>>> statistics.mode(data)
2
```

## 표준편차와 분산 구하기
표준편차와 분산은 데이터의 산포도를 파악하는 중요한 지표입니다.

### 표준편차와 분산을 구하는 함수

함수 이름 | 설명 | 반환값
---|---|---
pstdev(data) | 데이터의 모표준편차를 구한다. | float
stdev(data) |데이터의 표본표준편차를 구한다. | float
pvariance(data) | 데이터의 모분산을 구한다. | float
variance(data) | 데이터의 표본분산을 구한다. | float

### 표본편차와 분산 구하기

```python
>>> data = [1,2,2,3,4,5,6]
>>> statistics.pstdev(data)
1.6659862556700857

>>> statistics.stdev(data)
1.7994708216848747

>>> statistics.pvariance(data)
2.7755102040816326

>>> statistics.variance(data)
3.238095238095238
```

#### pvariance()와 variance()의 차이  
pvariance()와  variance()함수는 모두 분산 함수입니다. pvariance의 맨 앞 p는 population의 앞 문자로, 통계학에서 "모집단"을 의미합니다. pvariance()는 모분산, variance()는 표본분산을 구하는 함수입니다. 다루는 대상이 모집단이면 모분산을, 대상이 표본(샘플)이면 표본분산을 이용합니다. 모분산과 표본분산에 대해서 깊이 이해하려면 통계학 영역으로 넘어가기 때문에, 여기서는 차이점만 확인합니다.  

##### variance()의 구현

```python
if iter(data) is data:
        data = list(data)
    n = len(data)
    if n < 2:
        raise StatisticsError('variance requires at least two data points')
    T, ss = _ss(data, xbar)
    return _convert(ss/(n-1), T)
```
\_ss(data, xbar)에서는 "편차 제곱의 합"을 구하고 있습니다. 여기서 얻은 편차 제곱의 합을 "데이터의 개수(n)-1"로 나누는 것을 알 수 있습니다.

##### pvariance()의 구현

```python
if iter(data) is data:
        data = list(data)
    n = len(data)
    if n < 1:
        raise StatisticsError('pvariance requires at least one data point')
    T, ss = _ss(data, mu)
    return _convert(ss/n, T)
```
variance()와 거의 비슷하나, 편차 제곱의 합을 데이터 개수(n)로 나누고 있습니다. pstdev()와 stdev()는 pvariance()와 variance()의 결과에 대하여, 각각 math 모듈함수인 sqrt()를 이용하여 제곱근을 계산하게 되어 있습니다.

[statistics.py](https://github.com/python/cpython/blob/master/Lib/statistics.py){:target="\_blank"}에서 자세한 코드를 살펴볼 수 있습니다.
