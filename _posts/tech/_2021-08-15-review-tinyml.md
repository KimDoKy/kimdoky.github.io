---
layout: post
section-type: post
title: review - 초소형 머신러닝 TinyML
category: tech
tags: [ 'tech' ]
---

머신러닝은 항상 핫하지만, 입문 허들이 높아서 쉽게 도전하지 못하고 있는 분야입니다.  

저도 라이트 버전인 '생활코딩 - 머신러닝야학' 정도만 겨우 진행해 보았습니다.

![]({{ site.url }}/img/post/book/openML.png)

그러던 중 8원 리뷰어로 '초소형 머신러닝 TinyML'을 진행하게 되었습니다.

![]({{ site.url }}/img/post/book/tinyml_1.jpg)

사실 저는 ML을 거의 모르기 때문에 겁이 났습니다.  

하지만, 이 책은 초보자들도 시작할 수 있도록 용기를 주고 있습니다 ㅎ

![]({{ site.url }}/img/post/book/tinyml_2.jpg)

---

TinyML은 저전력의 임베디드 기기에서 사용하는 ML입니다. 그래서 이 책을 100% 활용하기 위해선 노트북 뿐만 아니라 스파크펀 에지, 아두이노, ST마이크로 STM32F 746G 디스커버리 키트와 같은 일부 장비가 필요합니다. (저는 집에 아이들이 있어서 장비 마련이 어려워서.. ML만 진행했습니다.)

Chater3 에서 머신러닝의 기본적인 부분들을 설명합니다. 머신러닝을 잘 모르는 입문자도 이해하기 수월했습니다. 저는 생활코딩의 머신러닝야학을 수강한 후에 봐서 그런지 잘 이해가 되었는데, 이 부분이 어렵게 느껴지는 입문자는 머신러닝야학을 수강하신 후에 보시면 도움이 많이 됩니다.(강추)

개인적으로 이 파트에서는 인상적인 부분은 ML이 "잘" 동작하기 위해 고민하는 부분들이였습니다. 만약 이 부분을 아무 도움 없이 진행했다면 많은 삽집이 선행되어야만 하는 부분이 아닌가 싶습니다.  

이제 진짜 시작은 Chapter4부터 진행이 되는데, 예제들을 실행할 수 있는 주피터 노트북을 colab을 통해 제공해주고 있기 때문에, 막혀도 큰 걱정없이 진행할 수 있습니다.   

예전에 현재 테스트 서버로 사용하고 있는 미니 PC에서 Tensorflow를 원격에서 주피터로 실행하려고 했을때 실패 했던 기억이 있어서 걱정했는데, Tensorflow Lite를 사용하는 점과, Colab을 통해 구글의 컴퓨터를 사용하여 컴퓨터 사양 때문에 막힐까 하는 걱정은 접어두게 되었습니다.  

이 책에서는 여러 예제들을 다루는데, 해당 예제들은 Tensorflow Lite의 공식 예제라고 합니다.

- Hello World (사인파 예측하는 모델)
- 호출어 감지(음성 인식 모델) 
- 인체 감지
- 마술 지팡이(제스처 인식)

---

아두이노와 같은 보드들이 저렴한 가격으로 IOT가 활발해지고 있는데, 거기에 ML을 적용한다면 세상은 지금도 빠르게 발전하고 있지만, 거기에 더욱 가속을 할 수 있을 것 같습니다. IOT, 임베디드에 관심이 있는 사람과 ML에 익숙하신 분들에게 큰 도움이 될 수 있을 것 같습니다. 다른 입문서는 아직 보지 않아서 모르겠지만, ML 입문서로도 괜찮을 것 같습니다.

단, 아무래도 임베디드를 다루기 때문에 ML을 다루기 위해 Python 뿐만 아니라, 기본적으로 C/C++ 도 다룰 줄 아셔야 합니다.

> [저자의 Git](https://github.com/yunho0130/tensorflow-lite) 을 통해 모든 부분을 공유하고 있는데, 잘 만들어 두시기도 했고, 계속 발전하는 Git이라 계속 지켜보며 ML을 공부하시는걸 추천

> 한빛미디어 "나는 리뷰어다" 활동을 위해서 책을 제공받아 작성된 서평입니다.
