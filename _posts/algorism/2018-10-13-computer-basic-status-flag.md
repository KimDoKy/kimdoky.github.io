---
layout: post
section-type: post
title: 컴퓨터 공학 - Basic Status Flag
category: algorism
tags: [ 'algorism' ]
---

# Basic Status Flag

###  제로 플래그( Z 플래그)
연산 결과를 제로로 나타낸다.  
비교를 위한 연산기가 없을 경우 비교 결과가 같은( EQ 플래그) 것으로 보는 기능도 있다.

### 사인(부호) 플래그( S 플래그) / 네거티브 플래그(N 플래그)
연산 결과가 음수

### 캐리 플래그(C 플래그) / 오버플로 플래그(OV 플래그)
산술 가산 연산 결과가 캐리(자리올림)이나 오버플로(자리넘침) 발생을 나타낸다.  
시프트 연산에서 자리 넘침이 있을 때도 세트된다.

### 보조 플래그
뺄셈을 할 때 발생한다. ‘캐리 플래그가 세트되지 않았다’로 대용할 수 있다.

### GT(Greater than) 플래그
`>`. ~초과

### LT(Less than) 플래그
`<`. ~미만

### ODD 플래그
1이 홀수개

### 인터랩트 마스크
인터랩트를 받아들일지 여부를 나타냄

### 인터트랩 플래그
인터랩트가 발생한 것을 나타냄