---
layout: post
section-type: post
title: ServiceMesh - Istio - Week9-2
category: devops
tags: ["k8s", "istio", "servicemesh"]
---

# Ambient Mesh - [Jimmy Song Blog](https://jimmysong.io/)

# Istio CNI Unveiled: Streamlining Service Mesh Connectivity

- **주제**: 서비스 메시 연결 간소화
- **주요 내용**:
  - Init 컨테이너의 보안 위험과 이를 해결하는 방법
  - Istio CNI의 작동 원리와 장점
  - Ambient Mode의 구현 메커니즘과 CNI와의 통합

## Istio 네트워크 요구 사항 및 솔루션 개요

### 기본 동작 방식

- **사이드카 모드**: Istio 서비스 메시가 사이드카 모드를 통해 애플리케이션 트래픽을 가로채고 관리
- **구성 요소**: 사이드카 프록시와 init 컨테이너를 애플리케이션 파드에 주입
- **트래픽 관리**: iptables 규칙을 사용하여 네트워크 트래픽 관리
- **효과성**: 대부분의 쿠버네티스 플랫폼에서 효과적
- **보안 문제**: 권한에 대한 높은 의존성으로 인해 멀티 테넌트 환경에서는 보안 문제 발생 가능

## Istio-init의 한계

### 권한 요구사항

- **istio-init 컨테이너**: 트래픽 차단 규칙을 초기화하기 위해 채택
- **고급 권한 필요**: iptables 규칙과 같은 네트워크 구성을 수정하려면 컨테이너에 고급 권한 필요
- **NET_ADMIN 권한**: 포드를 배포하는 서비스 계정에 NET_ADMIN 컨테이너 권한을 부여해야 함
- **보안 정책 충돌**: 일부 조직의 보안 정책과 상충될 수 있음

### 기본 동작

- **주입 방식**: 기본적으로 Istio 메시 내의 포드에 주입
- **트래픽 하이재킹**: Istio의 사이드카 프록시로 네트워크 트래픽을 하이재킹
- **보안 위험 증가**: 권한 요구 사항과 보안 위험을 크게 증가시킴

## Istio CNI 플러그인

- **커뮤니티 대응**: 권한 요구사항 문제에 대응하여 Istio 커뮤니티가 Istio CNI 플러그인 도입
- **init 컨테이너 제거**: init 컨테이너의 필요성을 없앰
- **직접 조작**: Kubernetes 네트워크 계층에서 직접 조작을 허용
- **권한 요구사항 감소**: 권한 요구 사항을 줄이고 배포 프로세스를 간소화
- **호환성 문제**: CNI 호환성 문제 존재

## 앰비언트 모드 소개

- **사이드카 없는 솔루션**: Istio의 Ambient Mode는 혁신적인 사이드카 없는 솔루션
- **네트워크 기술**: Geneve 터널이나 Istio CNI를 사용하여 네트워크 유연성과 보안 강화
- **범용 솔루션**: 최근 모든 CNI와 호환되는 범용 솔루션 도입
- **호환성 해결**: 모든 CNI와의 호환성 문제를 해결
- **효과적 관리**: Istio가 기존 네트워크 정책에 영향을 미치지 않고 서비스 간 트래픽을 더욱 효과적으로 관리할 수 있도록 지원

## NET_ADMIN 권한에 대한 보안 고려 사항

### 권한 범위

- **광범위한 작업**: NET_ADMIN 권한을 통해 컨테이너 내 프로세스가 다음 작업 수행 가능:
  - iptables 규칙 수정
  - 네트워크 인터페이스 구성 변경
  - IP 라우팅 테이블 관리
  - 네트워킹 관련 커널 매개변수 제어
- **보안 문제**: 과도한 권한 부여 및 잠재적인 공격 영역과 관련된 문제 발생

### 모범 사례

- **사용 범위 제한**: 필요한 경우에만 NET_ADMIN 권한을 부여하고 Kubernetes 네트워크 정책을 통해 제한
- **지속적인 모니터링 및 감사**: NET_ADMIN 권한을 사용하여 컨테이너에 대한 엄격한 로깅 및 모니터링 시행

## Istio CNI 플러그인의 작동 원리

![]({{ site.url }}/img/post/devops/study/istio/9/20250606165042.png)

### 기본 구조

- **바이너리 파일**: 각 노드의 파일 시스템에 에이전트로 설치되는 바이너리 파일
- **노드 에이전트**: Istio CNI 노드 에이전트가 각 노드에 설치된 에이전트 역할

### 주요 기능

- **플러그인 설치**: Istio CNI 플러그인을 설치하고 노드의 CNI 구성을 업데이트
- **모니터링**: 에이전트가 CNI 플러그인과 구성 경로의 변경 사항을 모니터링

### 모드별 동작

- **사이드카 모드**: 포드에 대한 iptables를 사용하여 사이드카 네트워킹 설정 처리
- **앰비언트 모드**: 포드 이벤트를 앰비언트 감시 서버와 동기화한 다음, 해당 서버가 포드 내에서 iptables 구성
- **권한 요구사항**: 노드에는 두 가지 모드에서 작동하기 위해 CAP_SYS_ADMIN, CAP_NET_ADMIN, CAP_NET_RAW와 같은 상승된 권한이 필요

## Istio Ambient Mode와 Kubernetes CNI 간 충돌 해결

### 설계 목표

- **모든 CNI 적응**: Istio의 앰비언트 모드는 모든 CNI에 적응하도록 설계
- **기존 구성 보호**: 기존 CNI 구성에 영향을 주지 않고 ztunnel을 사용하여 포드 내 트래픽 리디렉션을 투명하게 처리
- **역할 분담**:
  - 앰비언트 모드: ztunnel을 통해 Istio 서비스 메시를 통과하는 트래픽 관리
  - 표준 CNI: 포드에 표준화된 네트워크 액세스 제공

### 주요 문제점

- **CNI 역할**: IP 주소 할당 및 패킷 전달 등 쿠버네티스 파드 간의 네트워크 연결 문제 해결
- **앰비언트 요구사항**: ztunnel로 트래픽을 가져와야 하는데, 이는 CNI의 네트워크 구성과 호환되지 않을 수 있음
- **구체적 문제들**:
  - 주요 CNI 네트워크 구성이 Istio의 CNI 확장과 충돌하여 트래픽 처리 중단 가능
  - 배포된 네트워크 정책이 CNI에 따라 달라지는 경우 Istio CNI 사용시 이러한 정책 실행에 영향 가능

### 해결 방안

- **사용자 공간 실행**: 포드와 동일한 사용자 공간에서 ztunnel을 실행하여 트래픽 리디렉션 관리
- **커널 공간 충돌 방지**: CNI에 의해 수정된 커널 공간과의 충돌 방지
- **직접 연결**: 포드가 CNI의 영향을 받지 않고 ztunnel에 직접 연결 가능

### Ambient 모드 프로세스

- **UDS 이벤트**: Ambient CNI 에이전트가 포드 생성을 알리는 UDS 이벤트를 수신하여 상호작용 시작
- **iptables 수정**: Ambient Watch Server가 필요에 따라 포드 내의 iptables를 수정하여 트래픽을 ztunnel로 리디렉션
- **연결 설정**: ztunnel이 Kubernetes 클러스터 내에서 연결을 설정하고 네트워크 트래픽 리디렉션 처리

![]({{ site.url }}/img/post/devops/study/istio/9/20250606165144.png)

### 충돌 완화 방법

- **사용자 공간에서 ztunnel 실행**: ztunnel이 포드와 동일한 사용자 공간에서 실행되어 CNI와의 직접적인 충돌 회피
- **CNI 호환성 보장**: Istio CNI 구성이 기존 CNI 플러그인 구성에 영향을 미치지 않고 수행되어야 하며, 포드 간의 정상적인 통신과 트래픽 관리 보장

## Istio Ambient Mode를 통한 최적화된 트래픽 관리

### 고급 트래픽 전달 메커니즘

- **노드 로컬 Ztunnel**: 고급 트래픽 전달 메커니즘을 사용
- **수신 소켓 설정**: Pod의 네트워크 네임스페이스 내에 수신 소켓을 설정할 수 있도록 함
- **트래픽 유형**: 서비스 메시에서 발생하는 암호화된(mTLS) 트래픽과 일반 텍스트 트래픽의 효과적인 리디렉션 용이
- **장점**:
  - 트래픽 관리의 유연성 향상
  - 기존 CNI 플러그인과의 잠재적 충돌 방지

### 구현 흐름

![]({{ site.url }}/img/post/devops/study/istio/9/20250606170024.png)

1. **태그 감지**: Istio CNI 노드 에이전트가 `istio.io/dataplane-mode=ambient` 태그가 지정된 Pod를 감지
2. **CNI 플러그인 트리거**: Pod 이벤트(새로운 시작 또는 기존 Pod가 메시에 가입)를 기반으로 CNI 플러그인이 트리거되어 Istio CNI 노드 에이전트가 트래픽 리디렉션 구성
3. **리디렉션 규칙 구성**: 네트워크 리디렉션 규칙이 Pod의 네트워크 네임스페이스 내에 설정되어 트래픽을 가로채서 노드 로컬 ztunnel 프록시로 리디렉션
4. **수신 소켓 설정**: 노드 로컬 ztunnel이 트래픽 리디렉션을 활성화하기 위해 Pod의 네트워크 네임스페이스 내에 수신 소켓을 생성
5. **트래픽 처리**: 노드 로컬 ztunnel이 메시 내에서 암호화된(mTLS) 트래픽과 일반 텍스트 트래픽을 처리하여 안전하고 효율적인 데이터 전송 보장

---

# Detailed Explanation of Transparent Traffic Interception in Istio Ambient Mode

## 상세 트래픽 인터셉션 프로세스

### 기본 원칙

- **사이드카 불필요**: 앰비언트 모드에서는 애플리케이션 포드에 코드 변경이나 사이드카 주입이 필요하지 않음
- **네트워크 네임스페이스 내 처리**: 트래픽 가로채기 및 리디렉션은 포드의 네트워크 네임스페이스 내에서만 이루어짐
- **CNI 충돌 방지**: 기본 CNI와의 충돌을 방지

### 단계별 프로세스

![]({{ site.url }}/img/post/devops/study/istio/9/20250606165237.png)

#### 1. Pod 초기화 및 네트워크 구성 (Pod Initialization and Network Configuration)

- **쿠버네티스 포드 생성**: 쿠버네티스가 포드를 생성할 때 컨테이너 런타임 인터페이스(CRI)를 통해 기본 CNI 플러그인(예: Calico, Cilium)을 호출하여 포드의 네트워크를 구성
- **네트워크 네임스페이스 설정**: 이 단계에서는 포드의 네트워크 네임스페이스(netns)가 설정됨

#### 2. Istio CNI 노드 에이전트가 트래픽 리디렉션을 구성 (Istio CNI Node Agent Configures Traffic Redirection)

- **포드 감지**: Istio CNI 노드 에이전트가 새로운 포드가 주변 모드로 표시되었음을 감지 (레이블을 통해 `istio.io/dataplane-mode=ambient`)
- **iptables 규칙 설정**: 포드의 네트워크 네임스페이스에 들어가 트래픽 가로채기를 위한 iptables 규칙을 설정
- **파일 설명자 전달**: 네트워크 네임스페이스의 파일 설명자(FD)가 ztunnel에 전달됨

#### 3. Ztunnel이 Pod 네트워크 네임스페이스에서 소켓 수신을 시작 (Ztunnel Starts Listening Sockets in Pod Network Namespace)

- **네임스페이스 FD 수신**: ztunnel이 네임스페이스 FD를 수신
- **소켓 수신 시작**: 리디렉션된 트래픽을 처리하기 위해 해당 네임스페이스 내의 소켓을 수신하기 시작

#### 4. 투명한 트래픽 차단 및 처리 (Transparent Traffic Interception and Processing)

- **트래픽 가로채기**: 애플리케이션에서 발생한 트래픽이 Pod의 iptables 규칙에 의해 가로채여 투명하게 ztunnel로 리디렉션
- **트래픽 처리**: ztunnel이 트래픽을 대상 서비스로 전달하기 전에 정책 검사, 암호화 및 기타 처리를 수행
- **응답 처리**: 응답은 ztunnel에 의해 해독되어 애플리케이션으로 반환

## ztunnel 로그 분석

### 로그 검사 명령

```bash
kubectl -n istio-system logs -l app=ztunnel | grep -E "inbound|outbound"
```

### 인바운드 트래픽 예시

```bash
2024-11-16T10:33:01.410751Z	info	access	connection complete	src.addr=10.28.2.19:58000 src.workload="bookinfo-gateway-istio-64fc6d75d6-s442s" src.namespace="default" src.identity="spiffe://cluster.local/ns/default/sa/bookinfo-gateway-istio" dst.addr=10.28.2.18:15008 dst.hbone_addr=10.28.2.18:9080 dst.service="productpage.default.svc.cluster.local" dst.workload="productpage-v1-57ffb6658c-tgbjs" dst.namespace="default" dst.identity="spiffe://cluster.local/ns/default/sa/bookinfo-productpage" direction="inbound" bytes_sent=9603 bytes_recv=2052 duration="2110ms"
```

- **트래픽 방향**: bookinfo-gateway-istio에서 제품 페이지 서비스로의 인바운드 트래픽
- **암호화**: HBONE을 통해 암호화된 ztunnel의 포트 15008을 통과
- **신원 확인**: SPIFFE를 통해 신원이 확인됨

### 아웃바운드 트래픽 예시

```bash
2024-11-16T10:32:59.360677Z	info	access	connection complete	src.addr=10.28.2.18:51960 src.workload="productpage-v1-57ffb6658c-tgbjs" src.namespace="default" src.identity="spiffe://cluster.local/ns/default/sa/bookinfo-productpage" dst.addr=10.28.2.14:15008 dst.hbone_addr=34.118.226.6:9080 dst.service="details.default.svc.cluster.local" dst.workload="waypoint-7594b5b786-vgjwz" dst.namespace="default" dst.identity="spiffe://cluster.local/ns/default/sa/waypoint" direction="outbound" bytes_sent=794 bytes_recv=414 duration="40ms"
```

- **트래픽 방향**: 제품 페이지 포드에서 세부 서비스로 나가는 아웃바운드 트래픽
- **라우팅**: HBONE 터널을 사용하여 ztunnel을 통해 경유지 포드(포트 15008)로 라우팅
- **기준점**: `inbound` 및 `outbound`는 ztunnel을 기준으로 함

## 결론

- **구현 방식**: Istio CNI 노드 에이전트와 ztunnel의 협업을 통해 사이드카 없이 투명한 트래픽 차단을 구현
- **높은 호환성**: 기본 CNI와의 충돌을 방지
- **간소화된 작업**: 애플리케이션 코드를 변경할 필요가 없어 리소스 오버헤드가 줄어듦
- **강화된 보안**: HBONE을 통해 종단 간 암호화된 전송이 가능

---

# In-Pod IPtables Rule Injection in Istio Ambient Mode Explained

## Pod 내부의 iptables 규칙

### 기본 설정

- **설정 주체**: 포드의 네트워크 네임스페이스에서 Istio CNI 노드 에이전트가 투명한 트래픽 차단 및 리디렉션을 가능하게 하는 일련의 iptables 규칙을 설정
- **테이블 구성**: mangle과 nat 테이블에 규칙들이 삽입되어 Istio가 인바운드 및 아웃바운드 트래픽을 처리하는 방법을 보여줌

### mangle 테이블 규칙

```bash
*mangle
:PREROUTING ACCEPT [99138:22880045]  # mangle 테이블의 PREROUTING 체인에 대한 기본 ACCEPT 정책
:INPUT ACCEPT [0:0]                  # mangle 테이블의 INPUT 체인에 대한 기본 ACCEPT 정책
:FORWARD ACCEPT [0:0]                # mangle 테이블의 FORWARD 체인에 대한 기본 ACCEPT 정책
:OUTPUT ACCEPT [100900:34940164]     # mangle 테이블의 OUTPUT 체인에 대한 기본 ACCEPT 정책
:POSTROUTING ACCEPT [0:0]            # mangle 테이블의 POSTROUTING 체인에 대한 기본 ACCEPT 정책
:ISTIO_OUTPUT - [0:0]                # 아웃바운드 트래픽 처리를 위한 사용자 정의 ISTIO_OUTPUT 체인
:ISTIO_PRERT - [0:0]                 # 프리라우팅 트래픽 처리를 위한 사용자 정의 ISTIO_PRERT 체인
-A PREROUTING -j ISTIO_PRERT         # 모든 PREROUTING 트래픽을 ISTIO_PRERT 체인으로 전달
-A OUTPUT -j ISTIO_OUTPUT            # 모든 OUTPUT 트래픽을 ISTIO_OUTPUT 체인으로 전달
-A ISTIO_OUTPUT -m connmark --mark 0x111/0xfff -j CONNMARK --restore-mark --nfmask 0xffffffff --ctmask 0xffffffff
# 일관된 연결 추적을 위해 연결 마크 0x111/0xfff 복원

-A ISTIO_PRERT -m mark --mark 0x539/0xfff -j CONNMARK --set-xmark 0x111/0xfff
# PREROUTING에서 0x539/0xfff로 마킹된 패킷에 대해 연결 마크를 0x111/0xfff로 설정

COMMIT  # mangle 테이블 규칙 적용
```

### nat 테이블 규칙

```bash
*nat
:PREROUTING ACCEPT [2:120]           # nat 테이블의 PREROUTING 체인에 대한 기본 ACCEPT 정책
:INPUT ACCEPT [0:0]                  # nat 테이블의 INPUT 체인에 대한 기본 ACCEPT 정책
:OUTPUT ACCEPT [119:9344]            # nat 테이블의 OUTPUT 체인에 대한 기본 ACCEPT 정책
:POSTROUTING ACCEPT [0:0]            # nat 테이블의 POSTROUTING 체인에 대한 기본 ACCEPT 정책
:ISTIO_OUTPUT - [0:0]                # 아웃바운드 NAT 트래픽 처리를 위한 사용자 정의 ISTIO_OUTPUT 체인
:ISTIO_PRERT - [0:0]                 # 프리라우팅 NAT 트래픽 처리를 위한 사용자 정의 ISTIO_PRERT 체인
-A PREROUTING -j ISTIO_PRERT         # 모든 PREROUTING 트래픽을 ISTIO_PRERT 체인으로 전달
-A OUTPUT -j ISTIO_OUTPUT            # 모든 OUTPUT 트래픽을 ISTIO_OUTPUT 체인으로 전달
-A ISTIO_OUTPUT -d 169.254.7.127/32 -p tcp -m tcp -j ACCEPT
# 169.254.7.127(Istio 내부 주소로 추정)로 향하는 TCP 트래픽 허용

-A ISTIO_OUTPUT -p tcp -m mark --mark 0x111/0xfff -j ACCEPT
# 0x111/0xfff로 마킹된 TCP 트래픽 허용

-A ISTIO_OUTPUT ! -d 127.0.0.1/32 -o lo -j ACCEPT
# 127.0.0.1을 제외한 루프백 인터페이스로의 트래픽 허용

-A ISTIO_OUTPUT ! -d 127.0.0.1/32 -p tcp -m mark ! --mark 0x539/0xfff -j REDIRECT --to-ports 15001
# 127.0.0.1 외부로 향하는 아웃바운드 TCP 트래픽(0x539/0xfff로 마킹되지 않은)을 포트 15001(아웃바운드 소켓)로 리디렉션

-A ISTIO_PRERT -s 169.254.7.127/32 -p tcp -m tcp -j ACCEPT
# PREROUTING 체인에서 169.254.7.127에서 발생하는 TCP 트래픽 허용

-A ISTIO_PRERT ! -d 127.0.0.1/32 -p tcp -m tcp ! --dport 15008 -m mark ! --mark 0x539/0xfff -j REDIRECT --to-ports 15006
# 목적지 포트가 15008이 아닌 인바운드 TCP 트래픽(0x539/0xfff로 마킹되지 않은)을 포트 15006(인바운드 소켓)으로 리디렉션

COMMIT  # nat 테이블 규칙 적용
```

## 특정 포트의 역할

- **15008 (HBONE 소켓)**: HBONE 프로토콜을 사용하여 HTTP 기반 트래픽을 투명하게 처리
- **15006 (일반 텍스트 소켓)**: 포드 간 통신을 위해 메시 내의 암호화되지 않은 트래픽을 관리
- **15001 (아웃바운드 소켓)**: 아웃바운드 트래픽을 제어하고 외부 서비스 액세스에 대한 정책을 시행

### Istio의 포트 활용

- **투명한 관리**: 이러한 포트를 활용하여 인바운드, 아웃바운드 및 내부 트래픽을 투명하게 관리하고 제어
- **세분화된 제어**: 세분화된 보안 정책과 트래픽 제어를 적용

## 마킹 시스템

- 0x539 마크의 중요성
  - **트래픽 식별**: 0x539 마크는 Istio 프록시(예: ztunnel)에서 발생하는 트래픽을 식별
  - **재처리 방지**: 이 마크는 프록시에서 처리된 패킷을 구별하여 재처리되거나 잘못된 경로로 지정되지 않도록 함
- 0x111 마크의 중요성
  - **연결 수준 표시**: 0x111 마크는 Istio 메시 내의 연결 수준 표시에 사용되며, 프록시에 의해 연결이 처리되었음을 나타냄
  - **CONNMARK 활용**: iptables의 CONNMARK 모듈이 이 마크를 전체 연결로 확장하여 후속 패킷 매칭 속도를 높임

## iptables 규칙 시각화

- **소스 코드 참조**: [Istio GitHub - iptables.go](https://github.com/istio/istio/blob/master/cni/pkg/iptables/iptables.go)

![]({{ site.url }}/img/post/devops/study/istio/9/20250606170601.png)

## 트래픽 라우팅 시각화

### 노드 간 암호화된 L4 트래픽 경로

![]({{ site.url }}/img/post/devops/study/istio/9/20250606170650.png)

- iptables는 패킷을 ztunnel이 수신하는 포트로 리다이렉트
- Istio CNI는 포트 15001(outbound socket), 15006(plaintext socket), 15008(HBONE socket)에서 수신하는 각 Pod에 대해 cross-netns socket을 생성

#### 1. 애플리케이션이 요청을 보냄

- **트래픽 시작**: 트래픽이 애플리케이션 프로세스에 의해 시작되어 Pod의 네트워크 네임스페이스에 진입

#### 2. iptables 규칙 매칭

- **아웃바운드 처리**: 아웃바운드 트래픽은 OUTPUT 체인에서 일치하며, 권한 있는 트래픽(eligible traffic)은 ISTIO_OUTPUT 체인으로 리디렉션
- **체인 처리**: ISTIO_OUTPUT 체인에서는 트래픽이 표시(marked)되고 수락(accepted)됨

#### 3. REDIRECT 동작

- **트래픽 캡처**: 트래픽이 iptables에 의해 캡처되어 ztunnel의 수신 포트로 리디렉션
- **포트 구분**: 일반 텍스트 트래픽의 경우 15006, 암호화된 트래픽의 경우 15008

#### 4. ztunnel의 트래픽 처리

- **트래픽 수신**: ztunnel이 트래픽을 수신하고 정책 검사, 암호화 및 기타 작업을 수행

#### 5. 트래픽의 대상 서비스 전달

- **HBONE 터널**: ztunnel이 처리된 트래픽을 HBONE 터널을 통해 대상 노드의 ztunnel로 전송
- **최종 전달**: 대상 노드의 ztunnel이 트래픽을 복호화하여 대상 서비스로 전달

---

# Packet Lifecycle and Traffic Optimization in Istio Ambient Mode 정리

## 패킷 수명 주기 개요: 커널 공간에서 사용자 공간으로

### 기본 처리 흐름

- **시작점**: 앰비언트 모드에서 패킷 처리는 Pod의 커널 공간 네트워크 스택에서 시작
- **iptables 가로채기**: 패킷이 iptables 규칙에 의해 가로채진 후 사용자 공간의 zTunnel에 의해 처리
- **zTunnel 작업**: 투명 프록싱, 정책 적용, 암호화된 터널 생성 등의 작업을 처리
- **커널 공간 복귀**: 패킷이 대상 서비스 또는 다른 zTunnel로 전달되기 위해 커널 공간 네트워크로 다시 전송

### 최적화 핵심 아이디어

- **첫 번째 패킷 분석**: 첫 번째 패킷을 세부적으로 분석하고 태그를 지정
- **경로 확보**: 후속 패킷의 경로를 확보함으로써 중복 오버헤드를 줄임

![]({{ site.url }}/img/post/devops/study/istio/9/20250606171022.png)

## 첫 번째 패킷 경로: 가로채기에서 목적지 확인까지

### 초기 패킷 방출

- **애플리케이션 시작**: Pod 내의 애플리케이션이 패킷(예: HTTP 요청)을 방출
- **네트워크 스택 처리**: 해당 패킷이 먼저 Pod의 네트워크 네임스페이스와 커널 공간 네트워크 스택에서 처리

### Iptables를 통한 투명한 차단

- **트래픽 필터링**: iptables 규칙이 아웃바운드 트래픽을 필터링
- **리디렉션 조건**: 대상 주소가 non-local이고 패킷에 특정 태그가 없는 경우 zTunnel의 투명 프록시 포트(예: 15006 또는 15008)로 리디렉션
- **원래 목적지 추출**: IP_TRANSPARENT 및 SO_ORIGINAL_DST 옵션을 사용하여 zTunnel이 사용자 공간에서 패킷의 원래 목적지 주소를 추출 (소스 IP 보존)
- **투명 프록시**: 동일한 노드, 여러 노드 또는 메시 외부에 위치한 서비스에 대해 투명한 프록시 처리가 가능

### zTunnel 사용자 공간에서의 정책 검증 및 처리

- **정책 및 보안 검사**: zTunnel에 들어가면 첫 번째 패킷이 RBAC 검증 및 mTLS 암호화 결정과 같은 정책 및 보안 검사를 거침
- **메시 내 트래픽**: 암호화된 노드 간 통신을 위해 HTTP/2 CONNECT 터널(HBONE)이 설정
- **메시 외 트래픽**: 직접 TCP 전송이 사용됨

### 패킷 송신 및 연결 설정

- **아웃바운드 소켓 설정**: 처리 후, zTunnel이 패킷의 구문 분석된 세부 정보를 기반으로 아웃바운드 소켓(예: HTTP/2 터널 또는 평문 TCP 연결)을 설정
- **커널 공간 복귀**: 커널 공간으로 다시 보내 대상 서비스 또는 zTunnel로 라우팅
- **전체 여정 완료**: 이 시점에서 첫 번째 패킷이 커널 공간에서 사용자 공간으로 갔다가 돌아오는 전체 여정을 완료
- **정보 기록**: 연결 상태, 정책 및 터널 정보가 후속 패킷을 최적화하기 위해 기록됨

## 후속 패킷 경로: Conntrack 및 터널 재사용을 통한 빠른 전달

### 기본 메커니즘

- **연결 추적**: 첫 번째 패킷이 대상 해결 및 정책 검증을 완료하면, 리눅스 커널의 연결 추적(conntrack)이 연결 상태를 기록하고 태그를 지정
- **직접 도달**: 동일한 연결에 속하는 후속 패킷이 복잡한 iptables 리디렉션 및 대상 해상도를 우회하여 zTunnel의 인바운드 소켓에 직접 도달

### Conntrack의 역할

- **연결 추적**: 기존 연결을 추적하여 후속 패킷을 위한 빠른 경로를 제공
- **직접 전송**: iptables 규칙을 반복적으로 트리거하거나 정책 검사를 거치지 않고 패킷을 zTunnel로 직접 전송 가능

### 인바운드 소켓 및 사용자 공간 처리

- **직접 식별**: zTunnel의 인바운드 소켓에 들어오는 후속 패킷이 연결 태그에 의해 직접 식별
- **검증 생략**: 복잡한 RBAC 검증 또는 암호화 결정을 건너뛰게 됨
- **터널 재사용**: 첫 번째 패킷에 대해 암호화된 터널(HBONE)이 설정된 경우, 후속 패킷들이 이 터널을 재사용
- **기존 연결 사용**: 평문 트래픽의 경우, 기존 TCP 연결이 직접 전송에 사용됨

### 터널 및 일반 텍스트 경로 최적화

- **HBONE 터널**: 메쉬 내 암호화된 트래픽의 경우 HTTP/2 터널을 통해 멀티플렉싱이 가능해져 반복적인 연결 오버헤드가 줄어듦
- **Plaintext Socket**: 로컬 또는 외부 비암호화 트래픽의 경우, 후속 패킷이 기존 평문 연결을 사용하여 추가 캡슐화를 방지

### 성능 향상

- **경로 간소화**: 이러한 메커니즘이 후속 패킷의 처리 경로를 크게 간소화하여 성능과 처리량을 향상

## 핵심 기술 포인트 및 최적화 전략

### 1. Transparent Proxying (투명 프록싱)

- **기술 활용**: IP_TRANSPARENT와 SO_ORIGINAL_DST를 사용하여 zTunnel이 non-local 트래픽을 원활하게 캡처하고 파싱
- **진정한 투명 프록시**: 진정한 투명 프록시를 달성

### 2. Efficient Kernel-User Space Switching (효율적인 커널-사용자 공간 전환)

- **첫 번째 패킷**: 사용자 공간에서 첫 번째 패킷에 대한 상세한 구문 분석과 정책 검증을 완료
- **후속 패킷**: 후속 패킷에 대한 연결 트랙 및 인바운드 소켓 메커니즘을 활용
- **최적화 결과**: 불필요한 컨텍스트 전환을 최소화

### 3. Multiplexed Tunnels (다중화 터널)

- **HTTP/2 CONNECT 터널**: HTTP/2 CONNECT 터널(HBONE)이 암호화, 로드 밸런싱 및 다중화를 지원
- **효율성 향상**: 후속 패킷 전송의 효율성을 향상

---

# Understanding L7 Traffic Management in Istio Ambient Mode: From Ztunnel to Waypoint Proxy

## Istio Ambient Mode에서 L7 트래픽 관리 이해하기: Ztunnel에서 Waypoint Proxy까지

- **ztunnel 역할**: Istio의 앰비언트 모드에서 서비스 간 L4 트래픽 가로채기 및 암호화를 담당하는 노드 수준 보안 프록시 역할
- **ztunnel 제한사항**: HTTP 기반 라우팅이나 정책 적용과 같은 L7 작업은 처리하지 않음
- **Waypoint Proxy 역할**: L7 트래픽 관리를 위해 Envoy 기반 웨이포인트 프록시가 HTTP 요청을 처리하고 L7 정책을 적용
- **트래픽 전달**: ztunnel이 L7 처리가 필요한 트래픽을 감지하면 HBONE 프로토콜을 사용하여 해당 트래픽을 웨이포인트 프록시로 전달
- **프록시 처리**: 프록시가 정책을 적용하고, 원격 측정 데이터를 로깅하고, ztunnel을 통해 대상 Pod로 요청을 전달
- **분석 내용**: 트래픽 전달 경로를 자세히 설명하고, L7 트래픽이 ztunnel에서 웨이포인트 프록시로, 그리고 최종적으로 대상 Pod로 흐르는 방식을 분석

## 앰비언트 모드에서의 역할 및 책임

### ztunnel (L4 트래픽 관리자)

- **트래픽 가로채기**: L4(TCP) 수준에서 트래픽을 가로챔
- **보안 기능**: mTLS 암호화를 사용하여 트래픽을 보호하고 서비스 ID를 인증

### 웨이포인트 프록시 (L7 트래픽 관리자)

- **L7 정책 관리**: HTTP 라우팅, 인증, 권한 부여, 원격 측정과 같은 L7 트래픽 정책을 관리
- **애플리케이션 인식**: 애플리케이션 인식 프록시 역할을 하여 비즈니스별 정책을 적용하고 관찰 스택에 메트릭을 전송

### 협업 방식

- **L7 처리 요구**: 요청에 L7 처리(예: `productpage` 서비스 호출 `reviews-v1`)가 필요한 경우
- **HBONE 사용**: ztunnel이 HBONE을 사용하여 트래픽을 웨이포인트 프록시로 전달
- **투명한 처리**: 투명한 정책 적용 및 원격 측정 수집을 가능하게 함

## L7 Traffic Path in Ambient Mode

![]({{ site.url }}/img/post/devops/study/istio/9/20250606173937.png)

### 시나리오별 트래픽 경로

- **동일 노드**: 소스 포드와 목적지 포드가 동일 노드에 있는 L7 트래픽 경로

![]({{ site.url }}/img/post/devops/study/istio/9/20250606174003.png)

- **크로스 노드**: 다른 노드에 있는 소스 파드와 대상 파드의 L7 트래픽 경로

![]({{ site.url }}/img/post/devops/study/istio/9/20250606174029.png)

### Traffic Path Breakdown 분석

#### 1. Application Request Sent (요청 전송)

- **요청 시작**: productpage 서비스가 reviews.default.svc.cluster.local:9080에서 reviews-v1 서비스에 대한 HTTP 요청을 시작

#### 2. ztunnel L4 Traffic Interception

- **트래픽 가로채기**: 소스 노드의 Ztunnel이 Kubernetes의 iptables 규칙을 사용하여 제품 페이지에서 아웃바운드 요청을 가로챔
- **구성 검사**: Istio의 제어 평면 구성을 검사하고 L7 정책이 적용되어야 한다고 판단

#### 3. Forwarding Traffic Using HBONE Protocol (HBONE 프로토콜을 사용한 트래픽 전달)

- **프로토콜 선택**: Ztunnel이 네이티브 Envoy XDS 또는 TCP+mTLS 터널링 대신 HBONE 프로토콜을 사용
- **HBONE 정의**: HBONE(HTTP 기반 오버레이 네트워크 환경)이 HTTP/2에서 트래픽을 캡슐화하여 L7 처리를 위한 투명한 트래픽 전달을 가능하게 함
- **트래픽 전달**: ztunnel이 가로챈 트래픽을 HBONE 터널로 감싸 웨이포인트 프록시로 전달

#### 4. L7 Processing and Policy Enforcement by Waypoint Proxy (Waypoint 프록시를 통한 L7 처리 및 정책 시행)

- **인증 검증**: 웨이포인트 프록시가 Envoy을 기반으로 구축되었으며, SPIFFE ID와 컨텍스트 메타데이터를 사용하여 다운스트림 클라이언트의 mTLS 자격 증명을 검증
- **정책 적용**:
  - **HTTP 라우팅 및 부하 분산**: 호스트/경로 헤더를 기반으로 요청을 라우팅
  - **승인 정책**: 헤더와 토큰을 통해 액세스를 검증
  - **트래픽 셰이핑**: 오류 주입, 요청 속도 제한, 재시도 구현
  - **원격 측정 수집**: 메트릭, 로그, 추적 및 요청 기간을 추적
- **트래픽 전달**: 웨이포인트 프록시가 처리된 트래픽을 HBONE을 통해 대상 노드의 ztunnel로 전달

#### 5. Delivering Traffic to Target Pod (타겟 포드에 트래픽 전달)

- **트래픽 수신**: 타겟 노드의 ztunnel이 HBONE을 통해 웨이포인트 프록시로부터 트래픽을 수신
- **최종 전달**: 요청을 캡슐화 해제한 후 애플리케이션 포트의 타겟 포드(reviews-v1)로 전달

## Insights and Key Takeaways

### 1. Transparent Routing via Waypoint Proxy (Waypoint 프록시를 통한 투명한 라우팅)

- **제한된 정보**: 웨이포인트 프록시가 대상 Pod의 IP 주소와 재작성된 포트 15008만 알고 있음
- **ztunnel 관리**: ztunnel이 Kubernetes iptables를 사용하여 트래픽 리디렉션을 관리

### 2. End-to-End Security (종단간 보안)

- **mTLS 보장**: SPIFFE ID 검증을 통한 상호 TLS(mTLS)가 안전한 트래픽 전송을 보장
- **제로 트러스트**: 트래픽이 ztunnel을 우회하여 제로 트러스트 아키텍처를 적용할 수 없음

### 3. Transparent Policy Enforcement (투명한 정책 시행)

- **코드 변경 불필요**: 개발자가 애플리케이션 코드를 변경할 필요가 없음
- **자동화**: 교통 관제, 보안, 원격 측정이 데이터 플레인 수준에서 완전히 자동화됨

## How to Debug Ambient Mode?

### ztunnel Debugging

- **디버깅 도구**: `istioctl ztunnel`을 사용하여 ztunnel 구성 및 상태를 검사

### Waypoint Proxy Debugging

- **Envoy 전용 명령**: `istioctl pc` 및 `istioctl ps`와 같은 Envoy 전용 명령을 사용하여 Envoy 프록시 구성을 검사
- **Waypoint 전용 도구**: `istioctl waypoint`를 사용하여 간소화된 구성 검사

## 결론

- **ztunnel 역할**: Istio 앰비언트 모드가 투명 인터셉션, mTLS 암호화, 포워딩을 포함한 L4 트래픽 처리를 위해 ztunnel을 사용
- **Waypoint Proxy 역할**: HTTP 기반 라우팅, 정책 시행, 원격 측정 수집과 같은 L7 작업은 웨이포인트 프록시에 의해 관리
- **통신 프로토콜**: ztunnel과 웨이포인트 프록시 간의 통신은 HBONE 프로토콜에 의해 촉진
- **혁신적 디자인**: 사이드카를 제거하여 작동을 단순화하면서도 고성능, 보안, 관찰 가능성을 유지

---

# Beyond Sidecar: A Deep Dive Into Istio Ambient Mode Traffic Mechanism and Cost Efficiency

## 앰비언트 모드가 중요한 이유

### Service Mesh의 과제

- **리소스 오버헤드**: 사이드카 프록시로 인해 발생하는 리소스 오버헤드 및 운영 복잡성
- **운영 복잡성**: Envoy를 업그레이드하거나 시작하려면 다시 모든 Pod를 다시 시작해야 하는 경우가 많음
- **성능 요구**: 고성능과 낮은 비용에 대한 수요 증가

### 일반적인 서비스 메시 배포 모델

![]({{ site.url }}/img/post/devops/study/istio/9/20250606174218.png)

서비스 메시 아키텍처가 모색해 온 다양한 프록시 배포 전략:

- **Sidecar**: 각 Pod 내부에서 Envoy 프록시를 실행
- **Ambient**: 프록시를 Pod에서 노드 수준으로 이동 (이 게시물의 주요 초점)
- **Cilium Mesh**: L4의 커널 공간에서 eBPF를 사용하고 L7 기능을 위해 Envoy와 결합
- **gRPC**: 메시 기능을 애플리케이션 SDK에 직접 내장

### 각 모델의 특성 비교

![]({{ site.url }}/img/post/devops/study/istio/9/20250606175919.png)

| **방법**        | **보안**                          | **능률**           | **관리 용이성**            | **성능**                                              |
| --------------- | --------------------------------- | ------------------ | -------------------------- | ----------------------------------------------------- |
| **Sidecar**     | Pod별 프록시를 통한 높은 격리성   | 높은 리소스 사용량 | 중앙집중화되어 있지만 복잡 | 약간의 지연이 추가됨                                  |
| **Ambient**     | ztunnel을 통한 보안(계속 발전 중) | 더 효율적으로 공유 | 관리하기 쉽고 아직 성숙 중 | 좋음. AZ 간 트래픽으로 인해 오버헤드가 발생할 수 있음 |
| **Cilium mesh** | 중간, eBPF를 사용한 커널 기반     | 커널 수준 효율성   | 구성하기 복잡함            | 사용 사례에 따라 다름                                 |
| **gRPC**        | 앱 통합, 앱에 따라 다름           | 효율적임           | 복잡한 업그레이드 관리     | 낮은 지연 시간으로 실시간 사용에 이상적               |

### 앰비언트 모드의 탄생

- **구성**: ztunnel + Waypoint Proxy를 사용하여 데이터 플레인을 단순화하고 Sidecar를 제거하는 차세대 Istio 아키텍처
- **효과**: 자원을 절약하고 운영 복잡성을 줄임
- **선택적 기능**: Waypoint Proxy가 선택적으로 L7 기능을 제공하면서 mTLS 정책 시행 및 계속 지원

## Istio Ambient Mode의 핵심 개념

### Key Components of Ambient Mode

#### 1. ztunnel (L4)

- **배포**: 노드 수준 프록시로 실행
- **기능**: 투명한 트래픽 차단 및 mTLS 암호화를 담당
- **처리 범위**: L4 전달만 필요한 대부분의 트래픽을 처리

#### 2. 웨이포인트 프록시 (L7)

- **배포**: 선택적으로 배포됨 (네임스페이스, 서비스 또는 포드 세분성으로 구성 가능)
- **기능**: HTTP/gRPC 인증, 라우팅, 관찰성과 같은 고급 기능을 처리

#### 3. 이스티오 CNI

- **대체**: `istio-init` 컨테이너를 교체하고 트래픽 리디렉션을 처리
- **지원**: Sidecar와 Ambient 모드 모두 지원
- **보안**: 권한이 없는 모드에서 트래픽 리디렉션을 활성화하여 보안 강화

### Overview of Ambient Mode Architecture

![]({{ site.url }}/img/post/devops/study/istio/9/20250606180018.png)

**Ambient Mode에서는 Istio 데이터 평면이 두 개의 계층으로 분할:**

1. **Security Layer (ztunnel)**: 각 노드에 배포되는 경량 L4 프록시
2. **Optional L7 Layer (Waypoint Proxy)**: HTTP/gRPC 프록싱이 필요할 때만 배포

**제어 평면**: 여전히 Istiod에서 관리하며, Istiod가 구성과 인증서를 ztunnel과 Waypoint 프록시 모두에 배포

### Deployment Strategies for Waypoint Proxy

- **Namespace-level** (기본): 네임스페이스의 모든 워크로드에 적용
- **Service-level**: L7 처리만 필요한 서비스의 경우
- **Pod-level**: 세부적인 제어 제공
- **Cross-namespace**: 게이트웨이 리소스를 통한 공유를 활성화

### Istio CNI 기능

- **Traffic Interception**: `istio-init` 컨테이너를 대체하여 설치 간소화
- **Dual-mode Support**: Sidecar와 Ambient 모드 모두 호환
- **Unprivileged Mode Compatibility**: 권한 상승 없이 실행되는 Pod에 대한 트래픽 리디렉션 활성화
- **CNI Chaining**: 기존 CNI 구성에 Istio CNI를 추가 플러그인으로 추가
- **In-Pod Traffic Redirection (Ambient Mode)**:
  - Pod의 네트워크 네임스페이스 내부에서 `iptables REDIRECT` 규칙 사용
  - Pod 내에 로컬 소켓을 생성하여 트래픽을 가로채고 프록시

### Istio CNI 동작 방식

![]({{ site.url }}/img/post/devops/study/istio/9/20250606180132.png)
**Pod가 시작될 때 Istio CNI가 수행하는 작업:**

1. Pod의 네트워크 네임스페이스에 들어가서 ztunnel이 수신 중인 소켓으로 트래픽을 리디렉션하기 위한 iptables 규칙 세트를 생성
2. 더 이상 각 Pod에 init 컨테이너를 주입할 필요가 없으며, 권한 상승도 필요하지 않아 배포가 더욱 깔끔하고 안전해짐
3. ztunnel이 각 Pod의 네트워크 네임스페이스 내부에 소켓을 생성하고, 노드의 모든 Pod에 대해 이를 수행

## Traffic Flow and Core Mechanisms

### Transparent Traffic Interception

- **동작 방식**: 앰비언트 모드에서 Istio CNI가 각 Pod의 네트워크 네임스페이스에 iptables 규칙을 주입하여 아웃바운드 트래픽을 투명하게 가로채고 노드의 로컬 ztunnel 프로세스로 리디렉션
- **결정 과정**: zTunnel이 트래픽을 L4에서 전달할지 아니면 L7 처리를 위해 Waypoint Proxy로 보낼지 결정

### 트래픽 처리 과정

**Kubelet이 노드에서 Pod를 시작하면:**

1. Istio CNI 에이전트가 이 이벤트를 감지
2. 에이전트가 Pod의 네트워크 네임스페이스에 진입하여 트래픽을 로컬 소켓으로 리디렉션하는 iptables 규칙을 설정
3. Pod의 파일 디스크립터(FD)를 zTunnel에 전달
4. zTunnel이 FD를 수신하면 Pod의 네임스페이스 내에 소켓을 생성

**Pod가 트래픽을 전송할 때:**

- iptables 규칙 때문에 트래픽이 가로채여 로컬 zTunnel 프로세스로 리디렉션
- zTunnel이 Waypoint를 통해 트래픽에 L7 처리가 필요한지 여부를 판단:
  - **L7 기능이 불필요한 경우**: 트래픽을 암호화하여 L4에서 대상 Pod로 직접 전달
  - **L7 기능이 필요한 경우**: 트래픽을 Waypoint Proxy로 터널링

![]({{ site.url }}/img/post/devops/study/istio/9/20250606180233.png)

### Packet Lifecycle Overview

1. **Pod → ztunnel**: Pod의 트래픽이 CNI에 의해 가로채여 동일한 노드의 로컬 ztunnel로 리디렉션
2. **ztunnel**: 대상 주소를 확인하고 mTLS 암호화를 적용
3. **(L7 정책이 필요한 경우) ztunnel → Waypoint Proxy**: HTTP 인증, 라우팅 등을 처리
4. **웨이포인트 프록시**: L7 처리 후 트래픽을 ztunnel로 다시 전송
5. **ztunnel**: 트래픽을 대상 노드의 ztunnel로 캡슐화를 해제하거나 전달
6. **대상 Pod로**: 목적지 ztunnel이 최종적으로 대상 Pod로 트래픽을 전달

### The HBONE Protocol

![]({{ site.url }}/img/post/devops/study/istio/9/20250606180301.png)

- **정의**: 앰비언트 모드에서 ztunnel과 Waypoint Proxy가 HBONE(HTTP/2 + CONNECT) 프로토콜을 사용하여 보안 터널을 구축
- **장점**: mTLS 암호화 및 다중화가 가능해져 연결 오버헤드가 줄어들고 프록시 전달 로직이 간소화

#### HBONE CONNECT 요청 예시

```bash
:method: CONNECT
:scheme: https
:authority: Pod_B_IP:9080
:path: /api/v1/users?id=123
x-envoy-original-dst-host: Pod_B_IP:9080
x-forwarded-proto: hbone
x-istio-attributes: ...
```

- HBONE 동작
  - 외부 TCP 연결: ztunnel_A_IP:52368에서 Node_B_IP:15008까지 (포트 15008은 대상 노드의 HBONE 청취자)
  - HTTP/2 계층에서 CONNECT 요청 시작, 권한 필드는 Pod_B_IP:9080을 나타냄
  - 사용자 지정 헤더를 통해 라우팅 컨텍스트 및 보안 메타데이터 전달
  - HTTP/2 CONNECT 위에 구축된 "inner 터널"로 애플리케이션 계층 요청을 캡슐화

### 시나리오별 트래픽 흐름

#### Encrypted Traffic on the Same Node (동일한 노드의 암호화된 트래픽)

- **조건**: 소스 Pod와 대상 Pod가 동일한 노드에 있는 경우
- **경로**: ztunnel의 L4 암호화 경로를 통해 전송
- **처리**: ztunnel이 내부적으로 암호화 및 복호화를 수행하고 트래픽을 대상 Pod로 직접 전달
- **L7 필요시**: ztunnel이 Waypoint 프록시와 HBONE 터널을 설정하고 트래픽이 Waypoint를 통해 라우팅

![]({{ site.url }}/img/post/devops/study/istio/9/20250606180407.png)

#### Encrypted Traffic Across Nodes (L4) (노드 간 암호화된 트래픽 L4)

- **가장 일반적인 경우**: 교차 노드 시나리오
- **처리**: 소스 노드의 ztunnel이 HBONE 터널을 통해 트래픽을 암호화하여 목적지 노드의 ztunnel로 전송
- **전달**: 목적지 ztunnel이 트래픽을 압축 해제하고 이를 일반 텍스트로 목적지 Pod로 전달
- **효율성**: L7 기능이 필요하지 않은 한 Waypoint 프록시를 통한 추가 홉을 피하여 프록시 체인을 줄이고 효율성 향상

![]({{ site.url }}/img/post/devops/study/istio/9/20250606180424.png)

#### Encrypted Traffic Across Nodes (L7) (노드 간 암호화된 트래픽 L7)

**L7 처리가 필요한 경우의 흐름:**

1. source ztunnel이 트래픽을 웨이포인트 프록시로 터널링
2. 웨이포인트가 인증 및 라우팅과 같은 L7 로직을 처리
3. 웨이포인트가 HBONE을 사용하여 트래픽을 destination ztunnel로 재터널링
4. destination ztunnel이 트래픽을 압축 해제하여 목적지 포드까지 전달

**특징**: L4 전용 트래픽에 비해 하나의 프록시 홉을 추가하지만, L7 처리가 필요한 트래픽만 이 추가 단계를 거쳐 불필요한 오버헤드가 줄어듦

![]({{ site.url }}/img/post/devops/study/istio/9/20250606180436.png)

#### Catch-All Traffic (이탈 방지)

- **목적**: Istio 메시 외부에서 발생하는 트래픽이 메시를 우회하지 않도록 ztunnel에서 가로채고 관리
- **처리 방식**:
  - 애플리케이션 포트 대상 트래픽: 0x539 마크 확인, 없으면 포트 15006으로 리디렉션 후 처리하여 0x539 마크 추가 후 애플리케이션 포트로 전달
  - 포트 15008 대상: HBONE 트래픽으로 처리하여 ztunnel에서 직접 처리

![]({{ site.url }}/img/post/devops/study/istio/9/20250606180453.png)

### L4와 L7 트래픽의 차이점

| 트래픽 유형 | 처리 위치                   | 예시 시나리오                                               |
| ----------- | --------------------------- | ----------------------------------------------------------- |
| **L4**      | ztunnel (투명한 전달)       | 애플리케이션 계층 정책이 필요하지 않은 TCP 수준 트래픽      |
| **L7**      | ztunnel → 웨이포인트 프록시 | 인증, 라우팅, 관찰성 등 고급 기능이 필요한 HTTP/gRPC 트래픽 |

## Ambient Mode vs. Sidecar Mode

### Ambient Mode의 제약사항

- **세분화된 구성**: 앰비언트 모드와 사이드카 모드를 혼합할 때, 개별 포드에 세분화된 프록시 구성(예: EnvoyFilter)을 적용하는 것이 어려움
- **성숙도**: 다중 클러스터, 다중 네트워크 및 VM 워크로드에 대한 지원이 아직 성숙하지 않았으며, 운영 환경에서 주의가 필요
- **고급 사용자 지정**: WASM 플러그인과 같은 일부 고급 사용자 지정을 앰비언트 모드에서 팟 단위로 직접 적용할 수 없음

### 모드별 상세 비교

| 기준                  | Sidecar mode                                                        | Ambient mode                                                 |
| --------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------ |
| **프록시 위치**       | 각 Pod가 자체 Envoy 사이드카를 실행                                 | 노드 수준 ztunnel + 선택적 Waypoint 프록시                   |
| **리소스 오버헤드**   | 특히 대규모 환경에서 CPU/메모리 사용량이 더 높음                    | 오버헤드 감소; 프록시가 노드/네임스페이스 수준에서 공유됨    |
| **운영 복잡성**       | 사이드카 업그레이드에 영향을 받는 모든 Pod의 롤링 재시작이 필요     | 업그레이드가 몇몇 구성 요소(ztunnel/Waypoint)에 집중됨       |
| **성능**              | 강력한 Pod당 격리가 있지만 Pod당 프록시 비용이 추가됨               | 더 나은 L4 성능, L7은 Waypoint를 통해 하나 더 전달 홉을 추가 |
| **기능 완전성**       | 성숙하고 안정적이며 멀티 클러스터, VM 및 하이브리드 네트워크를 지원 | 계속 발전 중이며 다중 네트워크 및 VM 지원이 개발 중          |
| **일반적인 시나리오** | 엄격한 격리 또는 사용자 정의 EnvoyFilter/WASM이 필요한 시나리오     | 대규모 클러스터, 가벼운 관리, 대부분 L4 트래픽               |

### 권장사항

- **기존 사용자**: 이미 사이드카 모델을 사용 중이고 성숙한 기능에 크게 의존하고 있다면, 지금은 사이드카를 계속 사용
- **신규 도입**: 자원 절약과 운영 간소화가 우선이고 트래픽의 대부분이 L4인 경우 앰비언트 모드 사용
- **하이브리드**: 혼합 배포를 고려하되, 사이드카 대 앰비언트 워크로드에 대한 경계와 정책을 명확하게 계획

## Key Takeaways

- **비용 절감**: 앰비언트 모드가 사이드카를 제거하여 팟당 프록시 오버헤드를 줄여 리소스 및 운영 비용을 크게 낮춤
- **효율적 아키텍처**: ztunnel + Waypoint 아키텍처로 L7 기능은 필요할 때만 활성화되며, 다른 모든 트래픽은 L4에서 효율적으로 전달
- **성숙도**: 앰비언트 모드가 GA에 도달했지만, 멀티 클러스터/VM/멀티 네트워크 지원과 같은 기능들은 여전히 추가적인 테스트와 검증이 필요
- **권장 대상**: 대규모 클러스터, 주로 L4 트래픽, 자원 효율성과 중앙 집중식 관리에 대한 수요가 높은 팀에게 권장
