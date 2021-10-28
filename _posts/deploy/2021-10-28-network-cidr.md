---
layout: post
section-type: post
title: CIDR(Classless Inter-Domain Routing) with AWS VPC, Subnet
category: deploy
tags: [ 'deploy' ]
---

AWS VPC와 Subnet을 구성하게 되면 CIDR을 설정해야 합니다.

IPv4 네트워크는 A ~ E Class 체계로 구성되어 있습니다.

![network-addressing2](https://static.javatpoint.com/tutorial/computer-network/images/network-addressing2.png)

CIDR는 네트워크 클래스를 대체하는 IP 주소 할당 방식입니다. 

- IPv4 주소를 보다 효율적으로 구성
- 접두어로 계층을 나눔으로써 광역 라우팅의 부담을 줄임

IPv4 주소는 8비트씩 4개의 클래스(32비트)로 구성됨

ex. 10.0.0.0/24

`/24` 를 접두어로 계층을 표기하며, 0 ~ 32 까지 표현 가능합니다.

CIDR로 지정한 비트를 제외한 남은 비트가 주소의 범위가 됩니다.

## VPC와 Subnet을 구성해보기

VPC를 10.0.0.0/24로 구성하고, 2개의 서브넷을 구성해보겠습니다.

각 서브넷은 VPC의 CIDR에 설정한 범위 안에 포함되어야 합니다.

각 CIDR에 따른 네트워크 범위는 직접 계산해도 되지만, 아래의 계산 사이트를 활용합니다.

- [Subnet Calculator](https://mxtoolbox.com/subnetcalculator.aspx)

- [IpAddressGuide](https://www.ipaddressguide.com/cidr)

VPC CIDR을 10.0.0.0/20 로 구성하면 10.0.0.0 ~ 10.0.0.255 라는 범위를 갖게 됩니다.

![]({{ site.url }}/img/post/deploy/cidr/0.20.png)

이제 서브넷을 저 범위 안에서 구성하면 됩니다.

1번째 서브넷의 CIDR은 10.0.0.0/24로 구성합니다. 10.0.0.0 ~ 10.0.0.255 범위를 갖게 됩니다.

![]({{ site.url }}/img/post/deploy/cidr/0.24.png)

2번째 서브넷의 CIDR은 10.0.4.0/24로 구성합니다. 10.0.4.0 ~ 10.0.4.255 범위를 갖게 됩니다

![]({{ site.url }}/img/post/deploy/cidr/4.24.png)

---

참조 링크

- [CIDR이란?](https://kim-dragon.tistory.com/9)
- [stack overflow](https://stackoverflow.com/questions/51734945/cidr-address-is-not-within-cidr-address-from-vpc/56051282#56051282)
- [AWS VPC 생성하기](https://aws-builders-kr.workshop.aws/ko/30-vpc/100-create-vpc.html)
