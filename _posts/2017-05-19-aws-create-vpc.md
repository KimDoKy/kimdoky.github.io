---
layout: post
section-type: post
title: AWS 기본 VPC를 삭제했을 경우, 다시 생성하는 방법
category: deploy
tags: [ 'deploy' ]
---

AWS를 처음 사용했을때 처음 스터디가 끝난 후 RDS를 삭제 하지 않아서

소액의 요금이 청구 되었었다.

RDS 에서 청구된 것을 몰랐기 때문에 AWS의 모든 서비스를 삭제해버렸다.

거기서부터 삽질은 시작되었다.



TDD 를 스터디할때 중간쯤부터 배포가 나오면서 AWS를 사용해야하는 경우가 발생하였다.

전에 한것처럼 EC2 인스턴스를 생성하는 과정에서 기본 VPC 가 없어서 여러 어려운 상황에 마주쳤다.

(EC2 인스턴스틑 생성하는데 문제가 없지만, 접근 권한과 같은 VPC와 Subnet 문제들이 발생한다.)

덕분에 VPC와 AWS의 기초적인 것들을 공부하는 계기가 되었다.
> [VPC 포스팅](https://kimdoky.github.io/categories/deploy.html)

기본 VPC를 다시 생성하려했지만 계속 실패하였고, 구글링과 AWS문서를 읽어본 결과 기본 VPC는 유저가 직접 생성할 수 없다는 결론을 얻었다.

그럼 어떻게 기본 VPC를 생성할 수 있을까??

AWS support에 요청하면 된다.

AWS에 로그인하면 오른쪽 상단에 support - support Center로 들어가서 기본 VPC를 생성해달라고 요청하면 된다. (당연히 영어로)

> Support plans은 Bisic으로 하면된다. 다른건 모두 유료이다. 그리고 변경하는 순간 과금된다. 서비스를 이용하던 말던간에. 물론 Basic으로 재 변경하면 과금된건 다시 환불된다. 수수료를 제외하고...(내 500원 ㅠ)

![]({{ url.site }}/img/post/aws_create_vpc.png)

이 메일로 딱딱 해결했다고 메일이 온다. 친절하셔라...

처리되는 기간은 2일 정도 걸린 것 같다.
