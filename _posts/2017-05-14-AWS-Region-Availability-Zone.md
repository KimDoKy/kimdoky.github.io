---
layout: post
section-type: post
title: AWS Region와 Availability Zone
category: deploy
tags: [ 'deploy' ]
---

AWS Global Infrastructure는 현재 전 세계 16개 region과 2017년에 온라인으로 예정된 2개의 추가 region이 있는 42개의 Availability Zone으로 구성됩니다.

![]({{ site.url }}/img/post/global_infrastructure.png)

## Amazon Web Services Region

Region은 해당 region의 물리적 데이터 센터에 매핑 된 사용 가능한 지리적 위치입니다. 모든 region은 독립적입니다.  
이러한 격리 수준은 사용자 데이터가 특정 region을 벗어나지 않도록 보장합니다. 
각 region 내에는 2개 이상의 Availability Zone이 있으며 각 region은 다른 region의 개별 데이터 센터에서 호스팅됩니다. 
가장 큰 AWS region us-east-1에는 5개의 Availability Zone이 있습니다. 새로운 AWS region의 현재 표준은 가능한 3개이상의 Availability Zone을 갖는 것입니다. region에서 특정 리소스를 만들 때 해당 리소스를 호스트 할 Availability Zone을 선택하라는 메세지가 표시됩니다.

![]({{ site.url }}/img/post/aws_regions.png)

각 region은 다른 모든 region과 물리적으로 격리되어있지만 Amazon 글로벌 네트워크를 통해 서로 통신 할 수 있습니다. 이 글로벌 네트워크는 중복된  100GBE 사설 네트워크로서 지구를 가로 지르며 각 AWS region을 통과합니다. region 연결성을 통해 사용자가 도달 할 수 있는 전역에 애플리케이션을 구축할 수 있고 실패에도 견딜 수 있습니다. 또한 AWS는 region 간의 연결을 활용하여 S3 객체 저장 데이터나 Elastic Block Storage 스냅샷과 같은 데이터를 사용자의 재량에 따라 복제할 수 있습니다. 

![]({{ site.url }}/img/post/pinterest-ha.jpg)

region간의 데이터를 복제하고 Amazon의 Route 53 관리형 DNS를 사용하여 어떤 region의 장애가 발생해도 최소화되어야하므로, 전체 region의 장애에서 생존하거나 복구 할 수 있고 다른 region에는 영향을 주지 않습니다.

## Amazon Web Services Availability Zone(AZ)

Availability Zone은 모든 AWS 고객이 사용할 수 있는 region의 논리적 데이터 센터입니다. 한 region의 각 AZ는 이중화 된 별도의 전원, 네트워킹 및 연결을 통해 두 개의 AZ가 동시에 작동하지 않을 가능성을 줄입니다. 일반적인 오해는 **단일 AZ = 단일 데이터 센터**라는 것입니다. 실제로 각 **AZ는 1개 이상의 물리적 데이터 센터에 의해 지원되며 최대 5개의 데이터 센터**에 의해 지원됩니다. 단일 AZ는 여러 데이터 센터로 확장 될 수 있지만 AZ에서는 데이터 센터를 공유하지 못합니다. 특정 region의 AZ에 리소스를 고르게 분산시키기 위해 Amazon은 각 계쩡의 식별자에 AZ를 독립적으로 매핑합니다. 즉, 하나의 계정에 대한 us-east-1a AZ는 다른 계정의 us-east-1a와 동일한 데이터 센터 또는 물리적 하드웨어에 의해 백업 될 수 없습니다.

각 AZ에서 참여하는 데이터 센터는 중복 대기 시간이 낮은 사설 네트워크 링크를 통해 서로 연결됩니다. 마찬가지로 한 region의 모든 AZ는 이중화 개인 네트워크 링크를 통해 서로 통신합니다. 이러한 Intra-AZ 및 Intra-AZ 링크는 스토리지 및 관리 데이터베이스를 비롯한 여러 AWS 서비스의 데이터 복제에 많이 사용됩니다.

AZ가 AWS에서 중요한 기본 개념입니까? 아래 다이어 그램은 AZ 중 하나만 사용중인 2개의 AZ가 있는 region을 보여줍니다. 이 아키텍처는 사용자의 단일 구내 데이터 센터에서 실행되는 일반적인 3계층 애플리케이션의 모습을 나타냅니다. 각 계층에서 중복 서버가 실행되는 동안 데이터 센터 자체는 단일 실패 지점입니다. 

![]({{ site.url }}/img/post/single-az.png)

이 아키텍처와 달리 아래 다이어그램은 여러 AZ에 걸쳐 애플리케이션을 확장하는 권장 사례를 보여줍니다. 각 AZ에 각 계층의 클라우드 인스턴스 / 가상 서버를 배치함으로써 사용자는 단일 실패 지점으로 AZ를 제거할 수 있습니다. 서로 다른 애플리케이션 계층에 있는 Amazon Elastic Load Balancer(ELB)는 전체 AZ가 오프라인이 되어도 트래픽이 해당 AZ로 전달되도록 합니다. ELB가 AZ 외부에 "live"을  지적하고 있기에 특정 AZ의 실패로 영향을 받지 않습니다. ELB는 region 범위가 있고 주어진 region의 AZ에 걸쳐있을 수 있는 많은 AWS 서비스중 하나입니다. Route 53 과 같은 다른 서비스는 아래에 표시된 것처럼 범위가 전 세계적이며 여러 region에 서비스를 제공합니다.

![]({{ site.url }}/img/post/multi-az.png)

여러 AZ을 활용 할 수 있는 이 기능은 AWS를 사용하여 가용성이 높고 고장 방지성이 뛰어난 애플리케이션을 빌드하는데 있어 기본입니다.

[The Learning AWS Blog](https://learningawsblog.com/2017/02/06/aws-101-understanding-regions-and-availability-zones/)