---
layout: post
section-type: post
title: EFFECTIVE PYTHON - 한 슬라이스에 start, end, stride 를 함께 쓰디 말자
category: python
tags: [ 'python' ]
---




## 핵심 정리

- 한 슬라이스에 start, end, stride를 지정하면 매우 혼란스러울 수 있다.
- 슬라이스에 start와 end 인덱스 없이 양수 stride 값을 사용하자. 음수 stride 값은 가능하면 피하는게 좋다.
- 한 슬라이스에 start, end, stride를 함께 사용하는 상황은 피하자. 파라미터 3개를 사용해야 한다면 할당 2개(하나는 슬라이스, 다른 하나는 스트라이드)를 사용하거나 내장 모듈 `itertools`의 `islice`를 사용하자.
