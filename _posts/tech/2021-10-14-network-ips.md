---
layout: post
section-type: post
title: Network - IPS(Intrusion Prevention System)
category: tech
tags: [ 'tech' ]
---

# IPS(Intrusion Prevention System)

![](https://blog.kakaocdn.net/dn/Sw1IP/btqDebY4Vqp/xhH3sX8cJYScNXsAlvmN50/img.png)

- 방화벽(firewall), 침입탐지시스템(IDS), 바이러스 웰(Virus Wall) 및 유해사이트 차단(Contents Filtering) 시스템 등이 유기적으로 통합 연동되어 공격의 탐지 및 방어를 동시에 수행하는 시스템

###  IPS 기술요소

1. Deep contents Inspection(In-Line Mode)
- 방지능력 및 빠른 처리속도를 위해 In-Line에 위치한 제품
- Packet Header와 Payload(data) 영역까지 분석하는 DPI(Deep Packet Inspection) 기술을 적용하여 칩입/유해정보 여부를 판별 및 즉각 차단

2. Signature Detection/Prevention
  - 알려진 Virus, Worm, Dos 등의 공격 탐지
  - IDS와 같은 다양한 침입에 대한 탐지 및 차단 기능 제공
  - 기존의 침입탐지패턴 DB를 이용한 Signature 방식
  - IPS 판단 기준: 다양한 침입탐지패턴 DB 보유 / 비정상적인 트래픽 차단 기능 제공 여부
3. Anomalpy Detection/Prevention
  - 알려지지 않은  Virus, Worm, Dos 등의 공격 대비하기 위해 비정상적인 트래픽 흐름을 탐지/차단하는 기능을 제공
  - 서비스별로 트래픽을 감시 및 정상/비정상 판단
    - 각 서비스별 트래픽 기준선(Baseline) 설정
    - 트래픽이 기준선 대비 폭주 지속 시 탐지 및 자동 방어를 수행
    - 웜(Worm)이 유발하는 트래픽 폭주 방어에 유용
    - 정상적으로  Open된 포트를 통해 들어오는 해킹 공격 차단
    - 80번을 이용한 Back Door 차단
    - 80번을 이용한 트로이 목마 차단
    - 기타 비정상 HTTP 트래픽의 차단으로 내부 웹 서버에 대한 보안
4. 기타 유해 트래픽 차단 기능
   - 트래픽 및 세선 제한 기능(Traffic Shaping/Session Shaping)
   - 스캐팅(Scanning) 시도
   - 키워드 필터링 기능
   - 내부 망 IP 주소를 가지고 외부에서 들어오는 패킷 차단 기능
   - 비공인 IP 주소를 발신자 IP로 한 패킷 차단 기능
5. Traffic/Session Shaping
   - 각 호스트 또는 IP 주소 당 발생하는 세션 수를 일정 시간 단위별로 제한함으로 과자 세션 유발 호스트를 차단
   - 각 보안 정책별로 총 세션 수를 제한
   - 각 보안 정책별로 Bandwith를 제한하여 트래픽 조절
   - 비정상적으로 발생하는 세션에 대해 지정된 단위 시간당 Threshold 값을 제한하여 불필요 트래픽 차단
   - P2P 서비스 제어

- [AWS Network Firewall](https://aws.amazon.com/ko/network-firewall/?whats-new-cards.sort-by=item.additionalFields.postDateTime&whats-new-cards.sort-order=desc)

AWS Network Firewall은 일반적인 네트워크 위협에 대한 보호 기능을 포함하고 있습니다. AWS Network Firewall의 상태 기반 방화벽은 트래픽 흐름에 연결 추적 및 프로토콜 식별과 같은 컨텍스트를 통합하여 VPC가 승인되지 않은 프로토콜을 사용하여 도메인에 액세스하는 것을 방지하는 등의 정책을 적용할 수 있습니다. AWS Network Firewall의 IPS(침입 방지 시스템)는 취약성 공격을 식별 및 차단할 수 있도록 서명 기반 탐지에 기반한 능동적인 트래픽 흐름 검사를 제공합니다. 또한 AWS Network Firewall은 알려진 악성 URL에 대한 트래픽을 중지시키고 정규화된 도메인 이름을 모니터링할 수 있는 웹 필터링을 제공합니다.



> 출처:
>
> - 정보보호 전문가를 위한 네트워크 보안
> - 이미지: [해킹을 배우자!](https://h3ck.tistory.com/6)
>
> - AWS Network FireWall
