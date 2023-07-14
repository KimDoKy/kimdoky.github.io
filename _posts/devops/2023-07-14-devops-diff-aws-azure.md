---
layout: post
section-type: post
title: devops - AWS와 Azure의 네트워크 구조상 차이로 인한 주의점
category: deploy
tags: [ 'deploy', 'azure' ]
---

AWS는 인프라 구축시 Internet Gateway, NAT Gateway를 직접 생성 및 설정을 해주어야만  private subnet이 외부와 통신을 할 수 있습니다.

![]({{ site.url }}/img/post/deploy/230714/aws_nat_architecture.png)

Azure는 AWS와 달리 여러 과정을 블랙박스에서 자동으로 설정이 됩니다.

Azure에서 Container App를 사용한다면 Subnet과 연결하기 위해 Container App Environment를 생성해야 합니다.
그런데 이 과정에서 NAT Gateway가 자동으로 설정되어 Public하게 동작합니다.

![]({{ site.url }}/img/post/deploy/230714/azure_outbound_ip.png)

이러한 과정에서 생성된 자원에 대해서는 확인 및 접근이 불가능합니다.

AWS에 익숙한 사람이라면 이 부분을 놓칠 수 있는 부분입니다.

Azure에서 이러한 과정으로 설정된 public subnet을 NSG(Network Security Group)을 설정하여 private으로 설정할 수 있습니다.

NSG는 AWS의 Security Group과 NACL을 합쳐둔 개념으로 이해하면 될 것 같습니다.

- 리소스 자동 생성 시점
	- NAT Gateway : Container Apps Environment
	- Internet Gateway : Application Gateway
