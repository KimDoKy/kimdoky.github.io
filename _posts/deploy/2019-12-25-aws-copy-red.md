---
layout: post
section-type: post
title: AWS RDS DB를 다른 계정으로 복사하기
category: deploy
tags: [ 'deploy' ]
---

AWS를 사용하다보면 서로 다른 AWS 계정간의 DB를 복사해야 하는 상황이 있습니다.  

보통은 VPC로 같은 RDS에 접근하여 사용하지만, DB를 복사하고, 테스트해야 하는 상황이 발생하여, DB를 다른 계정으로 복사하는 방법을 포스팅합니다.  

AWS에 친절한 설명과 비디오로까지 설명을 해주고 있지만, 비디오를 잘안봐서..

>> 참고 [aws red db스냅샷 공유](https://aws.amazon.com/ko/premiumsupport/knowledge-center/rds-snapshots-share-account/)

'1. Amazon RDS 콘솔을 엽니다.

![]({{ site.url }}/img/post/deploy/snapshot/1.png)

'2. 복사하려는 DB를 스냅샷을 생성합니다.

![]({{ site.url }}/img/post/deploy/snapshot/2.png)

![]({{ site.url }}/img/post/deploy/snapshot/3.png)

>> 스냅샷이 생성되는데 약간의 시간이 소요됩니다.

'3. 다른 AWS 계정과 공유할 수동 스냅샷을 선택하고 [스냅샷 작업]를 선택한 후 [스냅샷 공유]을 선택합니다.

![]({{ site.url }}/img/post/deploy/snapshot/4.png)

![]({{ site.url }}/img/post/deploy/snapshot/5.png)

프라이빗으로 선택하고, 복사해갈 AWS 계정 id를 입력합니다.

AWS 계정 ID는 오른쪽 상단의 계정 - 내 계정 - 계정 설정에 있습니다.

![]({{ site.url }}/img/post/deploy/snapshot/6.png)

참고: 이 단계를 반복하여 최대 20개의 AWS 계정과 스냅샷을 공유할 수 있습니다.

'4. 스냅샷으로 DB 생성하기

공유한 스냅샷은 [나와 공유 상태]를 선택하야 뜹니다.

![]({{ site.url }}/img/post/deploy/snapshot/7.png)

이제 생성한 스냅샷으로 복구를 하던지, 마이그레이트를 하던지해서 사용하면 됩니다.


