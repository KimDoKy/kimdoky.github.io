---
layout: post
section-type: post
title: VPN with Azure
category: deploy
tags: [ 'network' ]
---


### VPN 연결 솔루션

- S2S(Site-to-Site)
	- 클라우드 가상 네트워크와 온프레미스 네트워크를 연결하는 '사이트 간 연결'
	- (Azure Virtual Network Gateway, Local Gateway in Azure / Virtual Private Gateway, Customer Gateway in AWS)가 필요

- P2S(Point-to-Site)
	- 클라우드 가상 네트워크와 개별 디바이스를 연결하는 '지점 및 사이트 간(사용자 VPN) 연결'
	- Azure Virtual Network Gateway와 AWS Customer Gateway의 VPN 클라이언트 구성이 필요

---

### VPN

VPN(Virtual Private Network. 가상 사설 네트워크): 인터넷상에서 안전한 사설 네트워크 연결을 제공하기 위한 기술

- VPN 서버는 최소 2개 이상의 네트워크 인터페이스 제공
	- 공용 IP 주소를 할당받아 인터넷에 액세스하는 역할
	- 사설 IP를 할당받아 내부 네트워크에 액세스하는 역할
- VPN 서버는 일반적으로 2개의 방화벽이 있는 DMZ에 설치한다.
	- 외부 방화벽은 잠재적인 인터넷 공격자에게서 DMZ 내부 호스트를 보호하는 계층을 제공
	- 내부 방화벽은 내부 호스트를 위한 보호 계층을 제공

VPN의 목적은 '보안'이기에 터널링 프로토콜을 사용해 연결 구간의 트래픽을 암호화한다.
- 주요 터널링 프로토콜 3가지
	- L2TP(Layer 2 Tunneling Protocol)
	- SSTP(Secure Socket Tunneling Protocol)
	- IKEv2(Internet Key Exchange v2)

**S2S VPN**은 클라우드와 온프레미스를 하이브리드 연결하는 복잡성이 높은 네트워크 구성 작업
Azure Virtual Network의 Gateway Subnet에 Virtual Network Gateway를 배포하고
온프레미스에는 로컬 네트워크의 VPN 디바이스를 나타내는 Local Network Gateway를 배포하고 구성한다.
IPSec/IKE VPN 터널을 통해 연결한다.(in Azure)

**IPSec(IP Security)**
IETF(국제 인터넷 기술 위원회)에서 개방형 구조로 설계한 표준
네트워크 계층에서 보안을 제공하는 서비스와 프로토콜 모음

- AH(Authentication Header): 출발지 인증, 데이터 무결성 보장
- ESP(Encapsulation Security Protocol): 출발지 인증, 데이터 무결성, 기밀성 보장
ESP가 더 많이 사용됨
- 전송 모드
	- 컴퓨터끼리 연결하기 위한 모드
	- 상위 프로토콜을 보호하지만 원본 IP 헤더는 보호하지 못함
- 터널 모드
	- 라우터 간(방화벽 간) 통신을 위해 만들어진 모드
	- 새로운 헤더를 만들어 통신하는 호스트를 파악하지 못하도록 전체 패킷을 보호함

**P2S VPN**은 개별 클라이언트에서 시작해 Azure Virtual Network와 안전하게 연결
가상 네트워크에 연결하는 클라이언트가 소수일 경우 사용

- P2S VPN 연결에 사용하는 3가지 프로토콜
	- Openvpn 프로토콜
		- 오픈소스로 개발
		- SSLv3/TLSv1 기반으로 TCP 포트 443을 사용
	- SSTP
		- MS가 개발한 TLS 기반 VPN 프로토콜
		- TCP 포트 443 사용
	- IKEv2
		- Cisco, MS가 공동 개발한 표준  IPSec 기반 터널링 프로토콜
		- 네트워크 변경이나 일시적 단절 후 안정적인 재연결을 제공

---
> ref : [처음 배우는 애저 : Azure Portal로 배우는 애저 도입부터 활용까지](https://www.hanbit.co.kr/store/books/look.php?p_code=B1481913277)
