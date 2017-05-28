---
layout: post
section-type: post
title: AWS EC2 instances 생성, 그리고 VPC
category: deploy
tags: [ 'deploy' ]
---

# AWS Deploy

## Key Pairs 생성
다운 받은 후 .pem파일을 `~/.ssh`폴더에 이동

## EC2
EC2 - Instances - Launch Instance
Ubuntu Server - Free tier로 사용 가능한 것 - Security Group 지정 - Launch - KeyPairs 선택

### SSH 접속

```
ssh -i ~/.ssh/KeyPair.pem ubuntu@ec2-13-124-46-220.ap-northeast-2.compute.amazonaws.com
```
> 작성 시점이 TDD 실습중이라서 Ubuntu으로 지정한다. 아직 프리티어 기간이 남아서 프리티어로 선택했다. VPC도 미리 생성해준다.

EC2가 셋팅되는데는 몇 분이 소요된다.

하지만.... 나는... 기본 VPC를 삭제해버렸다...

VPC의 자세한 내용은 다른 포스팅에서 다시 한다.
[AWS VIRTUAL PRIVATE CLOUD(VPC)]({{ url.site }}/tdd/2017/05/14/AWS-VPC.html)

일단 삭제된 VPC는 개인이 새로 생성할 수 없다.

그래서 [AWS Support](https://console.aws.amazon.com/support){:target="_blank"}에 요청해야한다.

잘 될런지는 모르겠다. 잘 되겠지...

[EC2 인스턴스 생성후 해야할 것들](https://github.com/KimDoKy/FastCamp/blob/master/Deploy/01.Ubuntu%20Linux%20Deploy.md){:target="_blank"}
