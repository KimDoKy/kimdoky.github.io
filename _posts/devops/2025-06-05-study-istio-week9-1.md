---
layout: post
section-type: post
title: ServiceMesh - Istio - Week9-1
category: devops
tags: ["k8s", "istio", "servicemesh"]
---

# Ambient Mesh

- 사이드카 프록시 대신 인프라에 통합된 데이터플레인을 사용하는 새로운 Istio 데이터플레인 모드
- **핵심 기능 유지**: 제로 트러스트 보안, 원격 측정, 트래픽 관리 기능 그대로 보존
- **기본 구조**: L4 Proxy(ztunnel)와 L7 Proxy(waypoint) 기능 분리

![]({{ site.url }}/img/post/devops/study/istio/9/20250603210244.png)

## 기존 사이드카 방식의 제약사항

- **침입성(간섭)**: 포드 사양 수정 필요, 설치/업그레이드 시 애플리케이션 포드 재시작 필요
- **리소스 활용도 저하**: 개별 포드의 최악 상황 고려한 CPU/메모리 예약으로 인한 과도한 리소스 예약
- **트래픽 차단**: 트래픽 캡처 및 HTTP 처리의 높은 컴퓨팅 비용, 일부 애플리케이션 중단 가능

  ![]({{ site.url }}/img/post/devops/study/istio/9/20250603202126.png)
  ![]({{ site.url }}/img/post/devops/study/istio/9/20250603200626.png)

## Ambient Mesh 아키텍처

### 두 개 레이어 분리

- **보안 오버레이**: 라우팅과 제로 트러스트 보안 처리
  - Traffic Mgmt: TCP Routing
  - Security
    - mTLS tunneling
    - Simple authorization policies
  - Observability: TPC metrics & logging
- **L7 프로세싱 레이어**: 필요시 활성화하여 모든 Istio 기능 액세스
  - Traffic Mgnt
    - HTTP routing & load balancing
    - Circuit breaking
    - Rate limiting
    - fault injection
    - Retry
    - Timeouts, ...
  - Security: Rich authorization policies
  - Observability
    - HTTP metrics
    - Access Logging
    - Tracing

![]({{ site.url }}/img/post/devops/study/istio/9/20250603223807.png)

### 주요 구성요소

- **ztunnel**: 각 노드에서 실행되는 공유 에이전트, 제로 트러스트 터널 역할 - **기본 기능**: mTLS, 원격 분석, 인증, L4 권한 부여 제공 - **효율성**: L7 처리 없이 사이드카보다 훨씬 효율적 - **공유 인프라**: 복잡성과 리소스 비용 감소로 공유 인프라로 제공 적합

  ![]({{ site.url }}/img/post/devops/study/istio/9/20250603205259.png)
  ![]({{ site.url }}/img/post/devops/study/istio/9/20250603222552.png)

- **waypoint proxy**: L7 처리가 필요할 때 배포되는 Envoy 기반 프록시 - **역할**: 네임스페이스의 워크로드에 대한 L7 처리 담당 - **배포**: 일반 Kubernetes 포드로 자동 확장 가능 - **확장성**: 실시간 트래픽 수요에 따른 동적 확장

  ![]({{ site.url }}/img/post/devops/study/istio/9/20250603210111.png)

## HBONE 프로토콜

- **정의**: HTTP Based Overlay Network Encapsulation
- **동작**: HTTP CONNECT 메서드를 통한 표준 HTTP 터널링
- **기술 스택**: TCP 상위 HTTP/2, TLS 상호 인증 및 암호화
- **포트**: TCP 15008 포트 사용

  ![]({{ site.url }}/img/post/devops/study/istio/9/20250603220549.png)

## 통신 흐름

![]({{ site.url }}/img/post/devops/study/istio/9/20250604213757.png)

### 통신 시나리오

#### (공통) Istio CNI DaemonSet 활용

- 파드 트래픽을 ztunnel로 리디렉션
- 호스트 네트워크 네임스페이스와 ztunnel 파드 내부에 iptables 설정

#### Ambient → Sidecar

- foo NS는 ambient mode 활성화: `istio.io/dataplan-mode=ambient`
- bar NS는 sidecar mode 활성화: `istio-injection: enabled`

![]({{ site.url }}/img/post/devops/study/istio/9/20250604220744.png)

- (1,2,3): sleep 파드에서 bar NS의 httpbin 목적지로 요청 -> istio CNI DaemonSet에 의해서 설정된 iptables에 따라, 요청 트래픽이 istioout -> (Geneve Tunnel) -> pistoout 전달
- (4,5): pistoout은 iptables rule을 통해 파드 내의 eth0 인터페이스에 port 15001로 redirect
- (6): ztunnel 파드는 목적지 httpbin 정보를 기반으로 전달 -> 노드 B eth0
- (7): 요청 트래픽은 httpbin 파드 내의 iptables rule을 통해 port 15006로 redirect되고 이후 목적지 httpbin 파드에 도착

#### Sidecar → Ambient

- foo NS는 sidecar mode 활성화: `istio-injection: enabled`
- bar-1, bar-2 NS는 ambient mode 활성화: `istio.io/dataplane-mode=ambient`

  ![]({{ site.url }}/img/post/devops/study/istio/9/20250604220809.png)

- Sidecar mode sleep -> ambient mode httpbin(waypoint proxy disabled)
  - (1,2): sleep 파드는 Sidecar Proxy에 iptables rule에 의해 15001 포트로 redirect 됨
  - (3) 목적지 httpbin 파드는 waypoint proxy disabled로 목적지 파드가 있는 워커 노드 B로 전달됨
  - (4,5,6): veth httpbin <-> httpbin 파드 내 eth0과 device pair 관계이지만, iptables rule에 의해 가로채어 istioin -> pistioin device로 전달
  - (7,8): ztunnel 파드 내에 iptables rule에 의해 port 15008 redirect
  - (9): 최종적으로 httpbin파드로 전달
- Sidecar mode sleep -> ambient mode helloworld(waypoint proxy enabled)
  - (1,2): sleep 파드는 Sidecar Proxy에 iptables rule에 의해 15001 포트로 redirect 됨
  - (3): 목적지 helloworld 파드는 waypoint proxy disabled로 목적지 파드가 있는 워커 노드 C(port 15008)로 전달됨
  - (4): waypoint 파드는 control plane을 통해 받은 라우팅 정보로 helloworld 파드가 있는 워커노드 D로 전달됨
  - (5~10): httpbin 파드 내부 과정과 동일

## 설계 원칙

### 로컬 노드에서 L7 처리 분리 이유

- **보안**: Envoy의 비멀티테넌트 특성으로 인한 보안 우려
- **리소스 효율성**: L4 처리는 L7 대비 적은 CPU/메모리 사용
- **대체 가능성**: 잘 정의된 상호 운용성 계약으로 다른 구현체 대체 가능

### 추가 홉에 대한 성능 고려사항

- 네트워크 지연시간의 주원인은 L7 처리, 네트워크 자체 아님
- 사이드카의 두 단계 L7 처리를 하나로 통합
- 제로 트러스트만 필요시 L7 처리 비용 완전 절감

## 리소스 오버헤드 개선

- **예측 가능성**: 더 적고 예측 가능한 리소스 요구사항
- **공유 리소스**: ztunnel의 노드 공유로 워크로드당 예약 대폭 감소
- **동적 확장**: waypoint proxy의 실시간 트래픽 수요 기반 확장

## 보안 특성

- **격리된 보안**: 애플리케이션 손상시에도 ztunnel과 waypoint proxy의 정책 적용 유지
- **제한된 공격 표면**: ztunnel의 L4 전용 제한으로 취약점 노출 영역 감소
- **노드별 키 접근**: ztunnel은 해당 노드 워크로드 키에만 접근
- **서비스 계정 제한**: waypoint proxy를 하나의 서비스 계정으로 제한 가능

## 기존 사이드카와의 호환성

- **상호 운용성**: 단일 메시에서 사이드카와 ambient 모드 혼합 사용 가능
- **기능 제한 없음**: 혼합 사용시에도 시스템 기능이나 보안 속성 제한 없음
- **지속 지원**: 사이드카는 규정 준수나 성능 튜닝이 필요한 사용자에게 여전히 유용

## 점진적 도입 방식

- **단계별 전환**: 메시 없음 → 보안 오버레이 → 완전한 L7 처리로 네임스페이스별 전환
- **선택적 활성화**: 필요에 따라 L7 기능 선택적 활성화
- **원활한 상호 운용**: 서로 다른 레이어의 워크로드 간 원활한 통신

---

# Rust-Based Ztunnel for Istio Ambient Service Mesh

## Ztunnel

- Istio 앰비언트 메시를 위해 특별히 설계된 노드별 프록시 (제로 트러스트 터널)
- 앰비언트 메시 내에서 워크로드를 안전하게 연결하고 인증
- **핵심 기능**: mTLS, 인증, L4 권한 부여, 원격 측정 제공
- **설계 원칙**: HTTP 트래픽 종료나 HTTP 헤더 파싱 없이 동작
- **트래픽 전달**: 웨이포인트 프록시로 트래픽을 효율적이고 안전하게 전송
- **리소스 최적화**: 모든 쿠버네티스 워커 노드에서 실행되므로 작은 리소스 사용량 유지 필수
- **설계 목표**: 워크로드에 미치는 영향을 최소화하면서 서비스 메시의 보이지 않는 부분으로 동작

## Ztunnel Architecture

![]({{ site.url }}/img/post/devops/study/istio/9/20250603222552.png)

### 주요 구성요소

- **xDS Client**: Istiod 제어 평면에서 구성 정보 수신
- **CA Client**: 공동 배치된 모든 워크로드를 위한 mTLS 인증서 관리 및 제공
- **L4 Policy enforcement**: L4 레벨 정책 시행
- **L4 Telemetry**: L4 원격 측정 (메트릭 및 로그) 제공

### 동작 방식

- **시작 시**: 서비스 계정 토큰을 사용하여 Istiod 제어 평면에 안전하게 연결
- **TLS 연결 후**: xDS 클라이언트로서 ztunnel 전용 xDS 구성 수신
- **트래픽 처리**: 공동 배치된 모든 워크로드의 인바운드/아웃바운드 트래픽 처리 (메시 외부 일반 텍스트 또는 메시 내부 HBONE)
- **관리 기능**: 디버깅 정보가 포함된 관리 서버 제공

## Envoy를 재사용하지 않는 이유

### Envoy의 한계

- 초기 구현
  - **2022년 9월 발표 당시** ztunnel은 Envoy 프록시로 구현
  - Istio의 사이드카, 게이트웨이, 웨이포인트 프록시가 모두 Envoy 사용
- **사용 사례 차이**: 사이드카 프록시나 인그레스 게이트웨이와 장단점, 요구사항, 사용 사례가 크게 다름
- **불필요한 기능**: Envoy의 풍부한 L7 기능 세트와 확장성이 ztunnel에서는 필요 없음
- **구현의 어려움**: Envoy를 ztunnel 요구사항에 맞게 변형하는 것이 어려움

## 전용 Ztunnel 구축

### 설계 가설

- **단일 사용 사례 집중**: 처음부터 단일 목적으로 설계하면 더 간단하고 성능이 뛰어난 솔루션 개발 가능
- **단순성 추구**: ztunnel을 단순하게 만들기로 한 명확한 결정이 핵심
- **적용 범위**: 많은 기능과 통합을 가진 게이트웨이 재작성에는 적용되지 않는 논리

### 두 가지 주요 영역

- **구성 프로토콜**: ztunnel과 Istiod 간의 구성 프로토콜
- **런타임 구현**: ztunnel의 런타임 구현

## Configuration Protocol (설정 프로토콜)

### 기존 xDS의 문제점

- **xDS 프로토콜**: Envoy 프록시가 구성에 사용하는 핵심 프로토콜
- **확장성 문제**: 사이드카에서 1개 포드를 가진 단일 서비스가 약 350줄의 xDS 생성
- **Envoy 기반 ztunnel**: 훨씬 더 나쁜 상황, 일부 영역에서 N^2 확장 속성 사용

### 전용 구성 프로토콜

- **목표**: 필요한 정보만 효율적인 형식으로 포함
- **단일 포드 표현 예시**:

```yaml
name: helloworld-v1-55446d46d8-ntdbk
namespace: default
serviceAccount: helloworld
node: ambient-worker2
protocol: TCP
status: Healthy
waypointAddresses: []
workloadIp: 10.244.2.8
canonicalName: helloworld
canonicalRevision: v1
workloadName: helloworld-v1
workloadType: deployment
```

### 이점

- **전송 방식**: xDS 전송 API 사용하지만 커스텀 ambient 전용 타입 활용
- **로직 이동**: Envoy 구성 대신 프록시에 로직 푸시 가능
- **mTLS 예시**: Envoy에서는 각 서비스마다 대규모 TLS 설정 필요, ztunnel에서는 단일 열거형으로 선언
- **대규모 확장**: 10만 개 포드 메시에서 구성이 엄청나게 줄어 CPU, 메모리, 네트워크 비용 절감

## Runtime Implementation (런타임 구현)

### HTTPS 터널링의 제약

- **기본 동작**: ztunnel은 HTTPS 터널을 사용하여 사용자 요청 전달
- **Envoy의 한계**: 터널링 지원하지만 구성 모델이 요구사항에 제한적
- **복잡한 요구사항**:
  - 여러 계층의 요청 (터널 자체와 사용자 요청)
  - 로드 밸런싱 후 포드별 정책 적용 필요
  - 연결당 필터를 4번 반복해야 하는 문제
- **메모리 최적화**: Envoy의 "자기 자신에게 요청 전송" 최적화에도 여전히 복잡하고 비용이 높음

### 자체 구현의 이점

- **제약 조건 고려**: 처음부터 제약 조건을 고려한 설계 가능
- **설계 유연성**: 모든 설계 측면에서 더 큰 유연성 확보
- **맞춤형 요구사항**: 스레드 간 연결 공유, 서비스 계정 간 격리 등 구현 가능

## Rust 기반 Ztunnel

### 언어 선택 과정

- **목표**: 빠르고 안전하며 가벼운 ztunnel 구현
- Go 기반
  - Go 기반 버전이 성능 및 설치 공간 요구사항 미충족
- C++
  - Envoy 일부 재사용하는 C++ 구현도 검토
  - **C++ 제외 이유**: 메모리 안전성 부족, 개발자 경험 문제, 업계의 Rust 선호 추세
- Rust 선택
  - **성공 사례**: 고성능, 저리소스 애플리케이션, 특히 네트워크 애플리케이션에서 탄탄한 실적
  - **핵심 라이브러리**:
    - **Tokio**: 비동기 런타임, 생태계 표준
    - **Hyper**: HTTP 라이브러리, 생태계 표준
  - **검증된 기술**: 광범위한 실전 테스트를 거친 라이브러리들
  - **개발 용이성**: 고성능 비동기 코드 작성 용이

### Workload xDS Configuration (워크로드 xDS 구성)

- **디버깅 용이성**: 이해하고 디버깅하기 매우 쉬운 구성
- **확인 방법**:
  - ztunnel 포드에서 `localhost:15000/config_dump` 요청
  - `istioctl pc workload` 명령 사용
- 주요 구성 요소
  - **워크로드 (workloads)**: 워크로드 정보
  - **정책 (policies)**: 정책 정보

#### 메시 포함 전 워크로드 구성 예시

```json
{
  "workloads": {
    "10.244.2.8": {
      "workloadIp": "10.244.2.8",
      "protocol": "TCP", // 메시 외부 상태
      "name": "helloworld-v1-cross-node-55446d46d8-ntdbk",
      "namespace": "default",
      "serviceAccount": "helloworld",
      "workloadName": "helloworld-v1-cross-node",
      "workloadType": "deployment",
      "canonicalName": "helloworld",
      "canonicalRevision": "v1",
      "node": "ambient-worker2",
      "authorizationPolicies": [],
      "status": "Healthy"
    }
  }
}
```

#### 앰비언트 포함 후 변화

- **레이블링**: 네임스페이스에 `istio.io/dataplane-mode=ambient` 레이블 적용
- **프로토콜 변경**: `protocol` 값이 `TCP`에서 `HBONE`으로 변경
- **의미**: ztunnel이 해당 포드의 모든 통신을 HBONE으로 업그레이드

```json
{
  "workloads": {
    "10.244.2.8": {
      "workloadIp": "10.244.2.8",
      "protocol": "HBONE",
      ...
}
```

#### 정책 구성 예시

```json
{
  "policies": {
    "default/hw-viewer": {
      "name": "hw-viewer",
      "namespace": "default",
      "scope": "WorkloadSelector",
      "action": "Allow",
      "groups": [
        [
          [
            {
              "principals": [{ "Exact": "cluster.local/ns/default/sa/sleep" }]
            }
          ]
        ]
      ]
    }
  }
}
```

#### 정책 적용 후 워크로드 업데이트

- **참조 추가**: 워크로드 구성에 권한 부여 정책 참조 추가
- **예시**: `"authorizationPolicies": ["default/hw-viewer"]`

```json
{
  "workloads": {
    "10.244.2.8": {
    "workloadIp": "10.244.2.8",
    ...
    "authorizationPolicies": [
        "default/hw-viewer"
    ],
  }
  ...
}
```

## L4 Telemetry (L4 원격 측정)

### 로그 기능

- **이해 용이성**: ztunnel 로그가 매우 이해하기 쉬움
- **로그 예시**:

  ```
  2023-02-15T20:40:48.628251Z  INFO inbound{id=4399fa68cf25b8ebccd472d320ba733f peer_ip=10.244.2.5 peer_id=spiffe://cluster.local/ns/default/sa/sleep}: ztunnel::proxy::inbound: got CONNECT request to 10.244.2.8:5000
  ```

- **로그 정보**: 소스 포드 IP(`peer_ip`)와 목적지 포드 IP를 포함한 HTTP Connect 요청 표시

### 메트릭 제공

- 접근 경로: `localhost:15020/metrics` API
- 호환성: 사이드카에서 노출하는 것과 동일한 레이블 사용
- 메트릭 범위: 전체 TCP 표준 메트릭 세트 제공

#### 메트릭 예시

```
istio_tcp_connections_opened_total{
  reporter="source",
  source_workload="sleep",
  source_workload_namespace="default",
  source_principal="spiffe://cluster.local/ns/default/sa/sleep",
  destination_workload="helloworld-v1",
  destination_workload_namespace="default",
  destination_principal="spiffe://cluster.local/ns/default/sa/helloworld",
  request_protocol="tcp",
  connection_security_policy="mutual_tls"
  ...
} 1
```

### 시각화
- 도구 요구사항: Prometheus와 Kiali 설치 필요
- UI 접근: Kiali UI에서 메트릭 쉽게 확인 가능
- 대시보드: Kiali 대시보드에서 ztunnel이 제공하는 L4 원격 측정 표시

![]({{ site.url }}/img/post/devops/study/istio/9/20250605225459.png)

---

# Istio Ambient Waypoint Proxy Made Simple

## Waypoint Proxy

- 목적지 지향적인 새로운 waypoint proxy로 단순성과 확장성 제공
- 아키텍처 분리
  - Ambient는 Istio 기능을 보안 오버레이 계층과 레이어 7 처리 계층으로 분할
- Envoy 기반의 선택적 구성 요소로 관리하는 워크로드에 대한 L7 처리 담당
- 2022년 최초 Ambient 출시 이후 waypoint 구성, 디버깅, 확장성 간소화를 위한 상당한 변경 작업 수행

## Waypoint Proxy Architecture

### 기본 특성

- **기반 기술**: 사이드카와 마찬가지로 Envoy 기반
- **동적 구성**: Istio를 통해 애플리케이션 구성을 지원하도록 동적으로 구성
- **실행 범위**: 네임스페이스별(기본값) 또는 서비스 계정별로 실행
- **독립성**: 애플리케이션 포드 외부에서 실행되어 애플리케이션과 독립적으로 설치, 업그레이드, 확장 가능
- **비용 절감**: 운영 비용 절감 효과

### 배포 방법

- **선언적 배포**: Kubernetes Gateway 리소스나 `istioctl` 명령 사용
- **Gateway 리소스 예시**:

```bash
$ istioctl experimental waypoint generate
apiVersion: gateway.networking.k8s.io/v1beta1
kind: Gateway
metadata:
name: namespace
spec:
gatewayClassName: istio-waypoint
listeners:

- name: mesh
port: 15008
protocol: HBONE
```

- **자동 관리**: Istiod가 리소스를 모니터링하고 해당 waypoint 배포를 자동으로 배포 및 관리

## 소스 프록시 구성을 대상 프록시로 전환

### 기존 사이드카 아키텍처의 문제점

#### 정책 분리

- **트래픽 셰이핑**: 요청 라우팅, 트래픽 이동, 오류 주입 등은 소스(클라이언트) 프록시에서 구현
- **보안 정책**: 대부분의 보안 정책은 목적지(서버) 프록시에서 구현

#### 발생하는 문제들

1. **Scaling (스케일링)**
   - 각 소스 사이드카는 메시 내 다른 모든 목적지에 대한 정보 필요 (다항식 스케일링 문제)
   - 목적지 구성 변경 시 모든 사이드카에 동시 알림 필요
2. **Debugging (디버깅)**
   - 정책 시행이 클라이언트와 서버 사이드카로 분리되어 문제 해결 시 시스템 동작 이해 어려움
3. **Mixed environments (혼합 환경)**
   - 모든 클라이언트가 메시에 속하지 않는 시스템에서 일관되지 않은 동작
   - 메시가 아닌 클라이언트는 카나리아 롤아웃 정책을 준수하지 않아 예상치 못한 트래픽 분산 발생
4. **Ownership and attribution (소유권 및 귀속)**
   - 이상적으로는 하나의 네임스페이스에 작성된 정책이 동일한 네임스페이스에서 실행되는 프록시 작업에만 영향을 미쳐야 함
   - 현재 모델에서는 정책이 각 사이드카에 의해 분산되고 적용됨

### Ambient의 해결책

- **목적지 중심**: 모든 정책이 목적지 waypoint에 의해 적용
- **게이트웨이 역할**: waypoint는 네임스페이스(기본 범위) 또는 서비스 계정으로의 게이트웨이 역할
- **트래픽 제어**: 네임스페이스로 들어오는 모든 트래픽이 waypoint를 통과하도록 강제
- **정책 적용**: waypoint가 해당 네임스페이스에 대한 모든 정책 적용
- **구성 단순화**: 각 waypoint는 자체 네임스페이스의 구성만 알면 됨

## 확장성 개선 시각화

### 간단한 예시 (2개 네임스페이스, 각각 2개 배포)

#### 사이드카 모델

- **구성량**: 4개 워크로드 × 4개 구성 세트 = 총 16개 구성 배포
- **변경 영향**: 구성 하나 변경 시 모든 구성 업데이트 필요

![]({{ site.url }}/img/post/devops/study/istio/9/20250605234814.png)

#### Waypoint 모델

- **구성량**: 2개 waypoint 프록시만 필요 (각 네임스페이스당 1개)
- **구성 감소**: 전송되는 구성의 총량이 25%로 감소

![]({{ site.url }}/img/post/devops/study/istio/9/20250605234840.png)

### 대규모 확장 예시

- **조건**: 각 네임스페이스를 25개 배포(각각 10개 포드)로 확장, 고가용성을 위해 각 waypoint 배포를 2개 포드로 구성

| 구성 배포             | 네임스페이스 1               | 네임스페이스 2               | 총         |
| --------------------- | ---------------------------- | ---------------------------- | ---------- |
| **사이드카**          | 25가지 구성 × 250개 사이드카 | 25가지 구성 × 250개 사이드카 | **12,500** |
| **waypoint**          | 25가지 구성 × 2개 waypoint   | 25가지 구성 × 2개 waypoint   | **100**    |
| **waypoint/사이드카** | 0.8%                         | 0.8%                         | **0.8%**   |

- **리소스 절약**: 제어 플레인과 데이터 플레인 모두의 리소스 사용량(CPU, RAM, 네트워크 대역폭) 감소
- **기존 방법 비교**: 현재 사용자는 `exportTo`나 Sidecar API 신중한 사용으로 유사한 개선 가능하지만, ambient 모드에서는 이러한 작업이 불필요
- **확장 용이성**: 확장이 훨씬 수월해짐

## 목적지에 Waypoint Proxy가 없는 경우

- 설계 가정과 한계

  - **기본 가정**: 대부분의 구성이 서비스 소비자가 아닌 서비스 생산자에 의해 가장 잘 구현
  - **예외 상황**: 제어할 수 없는 대상에 대한 트래픽 관리 구성이 필요한 경우
  - **일반적 예시**: 외부 서비스(예: example.com)에 대한 향상된 복원력 연결 (시간 초과 추가 등)

- 개발 중인 해결책
  - **진행 상황**: 커뮤니티에서 활발하게 개발 중인 영역
  - **설계 방향**:
    - 트래픽이 egress gateway로 라우팅되는 방식 설계
    - 원하는 정책으로 egress gateway를 구성하는 방법 설계

## Waypoint 구성 심층 분석

### 전제 조건

- **가이드 완료**: 환경 시작 가이드와 제어 트래픽 섹션 완료 가정
- **설정 상태**: bookinfo-reviews 서비스 계정에 대한 waypoint proxy 배포, 90% 트래픽을 reviews v1로, 10%를 reviews v2로 유도

### Listener 구성 확인

```bash
$ istioctl proxy-config listener deploy/bookinfo-reviews-istio-waypoint --waypoint
LISTENER              CHAIN                                                    MATCH                                         DESTINATION
envoy://connect_originate                                                      ALL                                           Cluster: connect_originate
envoy://main_internal inbound-vip|9080||reviews.default.svc.cluster.local-http ip=10.96.104.108 -> port=9080                 Inline Route: /*
envoy://main_internal direct-tcp                                               ip=10.244.2.14 -> ANY                         Cluster: encap
... (추가 항목들)
envoy://connect_terminate default                                              ALL                                           Inline Route:
```

#### 동작 방식

- **포트 15008**: Istio의 기본 인바운드 HBONE 포트
- **HBONE 종료**: waypoint proxy가 HBONE 연결을 종료하고 main_internal listener에게 요청 전달
- **정책 적용**: AuthorizationPolicy와 같은 워크로드 정책 적용

#### Internal Listener

- **정의**: 시스템 네트워크 API를 사용하지 않고 사용자 공간 연결을 허용하는 Envoy 리스너
- **--waypoint 플래그**: main_internal listener, filter chains, chain matches, destinations의 세부 정보 표시

#### IP 주소 정보

- **10.96.104.108**: reviews의 서비스 VIP
- **10.244.x.x**: reviews의 v1/v2/v3 포드 IP
- **확인 방법**: `kubectl get svc,pod -o wide` 명령 사용

### Cluster 구성 확인

```bash
$ istioctl proxy-config clusters deploy/bookinfo-reviews-istio-waypoint
SERVICE FQDN                         PORT SUBSET  DIRECTION   TYPE         DESTINATION RULE
agent                                -    -       -           STATIC
connect_originate                    -    -       -           ORIGINAL_DST
encap                                -    -       -           STATIC
kubernetes.default.svc.cluster.local 443  tcp     inbound-vip EDS
main_internal                        -    -       -           STATIC
prometheus_stats                     -    -       -           STATIC
reviews.default.svc.cluster.local    9080 http    inbound-vip EDS
reviews.default.svc.cluster.local    9080 http/v1 inbound-vip EDS
reviews.default.svc.cluster.local    9080 http/v2 inbound-vip EDS
reviews.default.svc.cluster.local    9080 http/v3 inbound-vip EDS
sds-grpc                             -    -       -           STATIC
xds-grpc                             -    -       -           STRICT_DNS
zipkin                               -    -       -           STRICT_DNS
```

#### 특징

- **제한된 클러스터**: 인프라용 클러스터 외에는 동일한 서비스 계정에서 실행되는 서비스와 포드를 위한 클러스터만 생성
- **아웃바운드 없음**: 다른 곳에서 실행되는 서비스나 포드를 위한 클러스터는 생성되지 않음
- **자동 필터링**: exportTo 구성 없이도 불필요한 클러스터에 대해 인식하지 않음

### Route 구성 확인

```bash
$ istioctl proxy-config routes deploy/bookinfo-reviews-istio-waypoint
NAME                                                    DOMAINS MATCH              VIRTUAL SERVICE
encap                                                   *       /*
inbound-vip|9080|http|reviews.default.svc.cluster.local *       /*                 reviews.default
default
```

#### 특징

- **선택적 인식**: Sidecar 리소스나 exportTo 구성 없이도 관련 없는 라우트에 대해 인지하지 못함
- **예시**: productpage로 라우팅하기 위한 ingress gateway 구성을 배포했지만 reviews waypoint는 이를 인식하지 않음

### 상세 Route 정보

```bash
$ istioctl proxy-config routes deploy/bookinfo-reviews-istio-waypoint --name "inbound-vip|9080|http|reviews.default.svc.cluster.local" -o yaml
```

#### 주요 구성 요소

- **가중치 기반 라우팅**: 90% 트래픽을 v1 reviews로, 10%를 v2 reviews로 유도
- **기본 설정**: Istio의 기본 재시도 및 타임아웃 구성 포함
- **정책 전환 확인**: 트래픽 및 복원력 정책이 소스에서 목적지 지향 waypoint로 전환됨을 확인

### Endpoint 구성 확인

```bash
$ istioctl proxy-config endpoints deploy/bookinfo-reviews-istio-waypoint
ENDPOINT                                            STATUS  OUTLIER CHECK CLUSTER
127.0.0.1:15000                                     HEALTHY OK            prometheus_stats
127.0.0.1:15020                                     HEALTHY OK            agent
envoy://connect_originate/                          HEALTHY OK            encap
envoy://connect_originate/10.244.1.6:9080           HEALTHY OK            inbound-vip|9080|http/v2|reviews.default.svc.cluster.local
... (reviews 관련 엔드포인트들)
```

#### 특징

- **서비스 제한**: default 및 istio-system 네임스페이스에 다른 서비스들이 있음에도 reviews 외의 서비스와 관련된 엔드포인트는 없음
- **자동 격리**: 관련 없는 서비스들로부터 자동으로 격리됨

---

# Ambient Mode Security Deep Dive

- Istio의 새로운 앰비언트 모드: Istio를 위한 사이드카 없는 데이터 플레인이자 앰비언트 메시 패턴의 참조 구현
- **주요 과제 해결**: 운영 간소화, 더 광범위한 애플리케이션 호환성, 인프라 비용 절감, 성능 향상
- **설계 원칙**: 보안이나 기능을 희생하지 않으면서도 운영, 비용, 성능에 대한 우려사항들을 신중하게 균형 있게 고려
- **보안 경계 변화**: 앰비언트 메시 구성 요소가 애플리케이션 포드 외부에서 실행됨에 따라 보안 경계가 더 나은 방향으로 변화

## Ambient Mesh 아키텍처

- **계층화된 구조**: 전송 보안 및 라우팅을 담당하는 보안 오버레이, 필요한 네임스페이스에 L7 기능 추가 옵션
- **보안 오버레이**: 노드 공유 구성 요소인 ztunnel로 구성, L4 원격 측정 및 mTLS를 담당, DaemonSet으로 배포
- **L7 계층**: waypoint proxy에 의해 제공, ID/워크로드 유형별로 배포되는 전체 L7 Envoy 프록시
- **데이터 플레인에서 애플리케이션 분리**
- **보안 오버레이 계층의 구성 요소는 CNI의 구성 요소와 유사**
- **운영의 단순성이 보안에 더 좋음**
- **다중 테넌트 L7 프록시 피하기**
- **사이드카는 여전히 일류 지원 배포**

## 데이터 플레인에서 애플리케이션 분리

### 복잡성과 취약성

- **복잡성과 취약성**: 복잡성은 취약성을 야기하며, 엔터프라이즈 애플리케이션은 매우 복잡하고 취약성에 취약
- **공격 대상**: 복잡한 비즈니스 로직, OSS 라이브러리, 버그가 있는 내부 공유 라이브러리 등 사용자 애플리케이션 코드가 주요 공격 대상
- **침해 시 노출**: 애플리케이션 침해 시 메모리에 마운트되거나 저장된 자격 증명, 비밀, 키가 공격자에게 노출

### 사이드카 vs Ambient 모델

- **사이드카 모델**: 애플리케이션 침해 시 사이드카 및 관련 ID/키 자료의 점유 포함
- **Ambient 모델**: 애플리케이션과 동일한 포드에서 실행되는 데이터 플레인 구성 요소가 없으므로 애플리케이션 침해가 비밀 접근으로 이어지지 않음

### Envoy 보안 특성

- **강화된 인프라**: Envoy는 엄격한 보안 검사를 거치는 매우 강화된 인프라, 중요 환경에서 대규모 운영 (예: Google 네트워크)
- **취약점 관리**: 강력한 CVE 프로세스를 통해 취약점을 식별하고 신속하게 수정하여 광범위한 영향 전에 고객에게 배포
- **복잡성과 취약점**: Envoy 프록시의 가장 복잡한 부분은 L7 처리, 역사적으로 Envoy 취약점 대부분이 L7 처리 스택에 위치

### L4/L7 기능 분리의 이점

- **선택적 사용**: mTLS만 사용하는 경우 CVE 위험이 높은 완전한 L7 프록시 배포 위험을 감수할 필요 없음
- **제한된 노출**: 사이드카 배포에서는 기능의 일부만 사용해도 모든 프록시 채택 필요, ambient 모드에서는 안전한 오버레이 제공 후 필요에 따라 L7 레이어만 추가하여 노출 제한
- **분리된 실행**: L7 구성 요소는 애플리케이션과 완전히 분리되어 실행되므로 공격 경로를 제공하지 않음

## CNI 구성 요소와 유사한 보안 오버레이

### 공유 인프라 특성

- **DaemonSet 실행**: L4 구성 요소는 DaemonSet 또는 노드당 하나씩 실행
- **공유 인프라**: 특정 노드에서 실행 중인 모든 포드에 대한 공유 인프라
- **민감도 수준**: CNI 에이전트, kube-proxy, kubelet, Linux 커널과 같은 노드의 다른 공유 구성 요소와 동일한 수준에서 처리 필요

### Ztunnel 동작 방식

- **트래픽 리디렉션**: 워크로드에서 발생하는 트래픽이 ztunnel로 리디렉션
- **워크로드 식별**: ztunnel이 워크로드를 식별하고 mTLS 연결에서 해당 워크로드를 나타내는 올바른 인증서 선택

### 자격 증명 관리

- **고유한 자격 증명**: ztunnel은 각 포드에 대해 고유한 자격 증명 사용
- **제한된 발급**: 자격 증명은 포드가 현재 노드에서 실행 중인 경우에만 발급
- **공격 범위 제한**: 손상된 ztunnel의 공격 범위가 해당 노드에 현재 예약된 포드의 자격 증명만 유출되도록 보장
- **클러스터 자격 증명 사용 안함**: ztunnel은 클러스터 전체 또는 노드별 자격 증명을 사용하지 않음 (유출 시 클러스터의 모든 애플리케이션 트래픽 즉시 침해 가능)

### 사이드카 모델과의 비교

- **공유 특성**: ztunnel은 공유되며, 침해 시 노드에서 실행 중인 애플리케이션의 ID가 유출될 수 있음
- **CVE 가능성 감소**: 공격 표면이 크게 줄어들기 때문에 (L4 처리만) CVE 발생 가능성이 Istio 사이드카보다 낮음
- **L7 처리 없음**: ztunnel은 L7 처리를 전혀 하지 않음
- **사이드카 CVE 영향**: L7로 인해 공격 표면이 더 넓은 사이드카의 CVE는 침해된 특정 워크로드에만 국한되지 않으며, 메시의 모든 워크로드에 반복될 가능성 높음

## 운영의 단순성

### 유지 관리의 중요성

- **핵심 인프라**: Istio는 유지 관리가 필수인 핵심 인프라
- **제로 트러스트 구현**: 애플리케이션을 대신하여 제로 트러스트 네트워크 보안의 핵심 원칙 구현
- **패치 배포**: 일정에 따라 또는 필요에 따라 패치를 배포하는 것이 매우 중요

### 플랫폼 vs 애플리케이션 주기

- **플랫폼 팀**: 애플리케이션과는 상당히 다른 예측 가능한 패치 또는 유지 관리 주기
- **애플리케이션**: 새로운 기능이 필요할 때, 일반적으로 프로젝트의 일부로 업데이트
- **애플리케이션 변경 특성**: 예측이 매우 어렵고, 시간이 많이 소요되며, 안전한 보안 관행에 적합하지 않음
- **분리의 이점**: 보안 기능을 플랫폼의 일부로 유지하고 애플리케이션과 분리하는 것이 더 나은 보안 태세 구축에 도움

### 업그레이드 복잡성

- **사이드카 운영**: 사이드카의 침습적 특성으로 인해 더욱 복잡 (사이드카 주입/배포 설명자 변경, 애플리케이션 재시작, 컨테이너 간 경합 조건 등)
- **사이드카 업그레이드**: 애플리케이션이 다운되지 않도록 조정해야 하는 롤링 재시작과 계획 수립 필요
- **Ambient 업그레이드**:
  - ztunnel 업그레이드를 일반적인 노드 패치 또는 업그레이드와 동시 진행 가능
  - waypoint proxy는 네트워크의 일부이므로 필요에 따라 애플리케이션에 완전히 투명하게 업그레이드 가능

## 다중 테넌트 L7 프록시 피하기

### L7 처리의 복잡성

- **복잡성 비교**: HTTP 1/2/3, gRPC, 헤더 구문 분석, 재시도 구현, 데이터 플레인에서 Wasm 및/또는 Lua를 사용한 커스터마이징과 같은 L7 프로토콜 지원이 L4 지원보다 훨씬 더 복잡
- **더 많은 코드**: 이러한 동작을 구현하기 위한 코드(루아나 와즘과 같은 사용자 지정 코드 포함)가 훨씬 더 많음
- **취약점 잠재력**: 복잡성이 취약점의 잠재력으로 이어질 수 있음
- **CVE 가능성**: CVE는 이러한 L7 기능 영역에서 발견될 가능성이 더 높음

### Ambient 모드의 접근법

- **L7 처리 분리**: 여러 ID에 걸쳐 프록시에서 L7 처리를 공유하지 않음
- **전용 프록시**: 각 신원(쿠버네티스의 서비스 계정)은 사이드카에서 사용하는 모델과 매우 유사한 전용 L7 프록시(waypoint proxy) 보유
- **다중 테넌시 문제**: 여러 신원과 그들의 독특한 복잡한 정책 및 맞춤화를 동시에 찾으려는 시도는 공유 자원에 많은 변동성을 추가하여 기껏해야 불공정한 비용 귀속, 최악의 경우 완전한 대리 타협 초래

## 사이드카는 여전히 first-class 지원 배포

- 지속적인 지원

  - 일부 사람들은 사이드카 모델과 알려진 보안 경계에 익숙하며 그 모델을 유지하기를 원함
  - **first-class**: Istio에서 사이드카는 메시의 first-class citizen이며 플랫폼 소유자는 사이드카를 계속 사용할 수 있음
  - **혼합 지원**: 플랫폼 소유자가 사이드카 모드와 ambient 모드를 모두 지원하고자 하는 경우 지원 가능

- 상호 운용성
  - ambient 데이터 플레인이 있는 워크로드는 사이드카가 배치된 워크로드와 기본적으로 통신 가능
- 미래 전망
  - 사람들이 ambient 모드의 보안 자세를 더 잘 이해하게 되면서, 특정 최적화를 위해 사이드카가 사용되는 Istio의 선호되는 데이터 플레인 모드가 될 것으로 확신

> **first-class citizen**<br/>
> <li>완전한 지원: 시스템에서 모든 기능과 특권을 완전히 지원받는 요소<br/>
> <li>제약 없음: 다른 요소들과 동등한 수준의 기능과 권한을 가짐<br/>
> <li>차별 없는 대우: 시스템 내에서 차별받지 않고 동등하게 취급됨<br/>
> => sidecar 모드가 ambient 모드 도입 후에도 완전히 동등한 지원을 받는 정식 배포 방식<br/>
> => 사용자들이 안심하고 계속 사용할 수 있고, 지속적으로 지원받을 수 있다는 의미

---

# Maturing Istio Ambient: Compatibility Across Various Kubernetes Providers and CNIs

## 서비스 메시와 CNI의 복잡한 관계

- 서비스 메시는 모든 Kubernetes 클러스터에 사양을 준수하는 기본 CNI 구현이 있어야 하며, 그 위에 있어야 함
- 기본 CNI 구현은 클라우드 제공업체(AKS, GKE, EKS 모두 자체 배송) 또는 Calico, Cilium과 같은 타사 CNI 구현에 의해 제공 가능

### 서비스 메시 동작 전제조건

- **기능적 CNI 필요성**: 기본적으로 mTLS를 사용한 안전한 포드 트래픽과 서비스 메시 계층의 고급 인증 및 권한 부여 정책 적용 전에 기능적 CNI 구현이 가능한 Kubernetes 클러스터 필요
- **네트워킹 경로**: 기본 네트워킹 경로가 설정되어 패킷이 클러스터 내에서 한 포드에서 다른 포드(그리고 한 노드에서 다른 노드로)로 이동할 수 있어야 함

### CNI 구현의 복잡성과 충돌

- **병렬 실행**: 때로는 동일한 클러스터 내에서 두 개의 기본 CNI 구현을 병렬로 실행할 수도 있음 (클라우드 제공업체 구현 + 타사 구현)
- **호환성 문제**: 각 CNI 구현이 내부적으로 사용할 수 있는 매우 다양한 메커니즘으로 인해 호환성 문제, 이상한 동작, 축소된 특징 세트, 일부 비호환성 문제 발생

### Istio 프로젝트의 접근법

- **자체 CNI 구현 없음**: 배송을 하지 않거나 자체 기본 CNI 구현을 요구하지 않거나, 심지어 "선호되는" CNI 구현을 요구하지 않기로 결정
- **광범위한 지원**: 가능한 한 가장 넓은 CNI 구현 생태계와의 CNI 체인을 지원
- **최대 호환성**: 관리형 오퍼링과의 최대 호환성, 공급업체 간 지원, 더 넓은 CNCF 생태계와의 구성 가능성 보장

## 앰비언트 알파에서의 트래픽 리디렉션

### istio-cni 구성 요소 역할

- **사이드카 모드**: 선택적인 구성 요소로, 일반적으로 포드를 메시에 배포하는 사용자에게 `NET_ADMIN` 및 `NET_RAW` 기능의 요구 사항 제거
- **앰비언트 모드**: 필수 구성 요소
- **구성 요소 성격**: 기본 CNI 구현이 아니며, 클러스터에 이미 존재하는 기본 CNI 구현을 확장하는 노드 에이전트

### 알파 버전 트래픽 리디렉션 메커니즘

- **구성 과정**: 포드가 앰비언트 메시에 추가될 때마다 istio-CNI 구성 요소가 노드 수준의 네트워크 네임스페이스를 통해 포드 노드에서 실행되는 ztunnel과 포드 간의 모든 들어오고 나가는 트래픽에 대한 트래픽 리디렉션 구성
- **주요 차이점**: 사이드카 메커니즘과 앰비언트 알파 메커니즘의 차이는 후자의 경우 포드 트래픽이 포드 네트워크 네임스페이스에서 벗어나 공동 위치한 ztunnel 포드 네트워크 네임스페이스로 리디렉션
- **경유 경로**: 호스트 네트워크 네임스페이스를 통과하며, 이곳에서 대부분의 트래픽 리디렉션 규칙이 구현됨

### 알파 메커니즘의 한계 발견

- **테스트 결과**: 여러 실제 쿠버네티스 환경에서 자체 기본 CNI를 사용하여 더 광범위하게 테스트한 결과, 호스트 네트워크 네임스페이스에서 포드 트래픽을 캡처하고 리디렉션하는 것이 요구 사항을 충족하지 못함이 판명
- **접근법의 한계**: 다양한 환경에서 일반적인 방식으로 목표를 달성하는 것이 이 접근 방식으로는 불가능

### 근본적인 문제점

- **충돌 지점**: 호스트 네트워크 네임스페이스에서 트래픽 리디렉션하는 것이 클러스터의 기본 CNI 구현이 트래픽 라우팅/네트워킹 규칙을 구성해야 하는 바로 그 지점과 동일
- **피할 수 없는 충돌**:
  - 기본 CNI 구현의 기본 호스트 수준 네트워킹 구성이 Istio의 CNI 확장에서 호스트 수준의 주변 네트워킹 구성을 방해하여 트래픽 중단 및 기타 충돌 발생
  - 사용자가 기본 CNI 구현에 의해 네트워크 정책을 시행하도록 배포한 경우, Istio CNI 확장이 배포될 때 네트워크 정책이 시행되지 않을 수 있음

### 대안 접근법의 한계

- **사례별 설계**: 일부 주요 CNI 구현을 위해 사례별로 문제를 설계할 수는 있지만, 보편적인 CNI 지원에 지속 가능하게 접근할 수는 없음
- **eBPF 고려**: eBPF를 고려했지만, 현재로서는 임의의 eBPF 프로그램을 안전하게 체인/확장할 수 있는 표준화된 방법이 없어 동일한 기본 문제를 가질 수 있음을 깨달음
- **비 eBPF CNI**: 이 접근 방식으로는 여전히 비 eBPF CNI를 지원하는 데 어려움을 겪을 가능성

## 과제 해결: 새로운 솔루션 개발

### 새로운 접근법의 필요성

- **충돌 불가피성**: 노드의 네트워크 네임스페이스에서 임의의 종류의 리디렉션을 수행하면 호환성 요구 사항을 위반하지 않는 한 피할 수 없는 충돌 발생
- **사이드카 모델에서의 영감**: 사이드카 모드에서는 사이드카와 애플리케이션 포드 간의 트래픽 리디렉션을 구성하는 것이 간단 (둘 다 포드의 네트워크 네임스페이스 내에서 작동)
- **아이디어**: 사이드카를 모방하고 애플리케이션 포드의 네트워크 네임스페이스에서 리디렉션을 구성하는 것

### 기술적 혁신

- **Linux 소켓 API 활용**: 하나의 네트워크 네임스페이스에서 실행되는 Linux 프로세스가 다른 네트워크 네임스페이스 내에서 리스닝 소켓을 생성하고 소유할 수 있다는 Linux 소켓 API의 기본 기능 발견
- **아키텍처 변경**: 이를 작동시키고 모든 포드 라이프사이클 시나리오를 다루기 위해 ztunnel과 Istio-CNI 노드 에이전트에 아키텍처 변경 필요

### 검증과 기여

- **프로토타입 제작**: 새로운 접근 방식이 접근할 수 있는 모든 Kubernetes 플랫폼에서 작동하는지 충분히 검증
- **업스트림 기여**: 모든 주요 클라우드 제공업체 및 CNI와 호환되도록 처음부터 구축된 인팟 트래픽 리디렉션 메커니즘을 업스트림에 기여하기로 결정

### 핵심 혁신 요약

- **네트워크 네임스페이스 제공**: 포드의 네트워크 네임스페이스를 공동 위치한 ztunnel에 제공
- **포드 외부 실행**: ztunnel이 포드 네트워크 네임스페이스 내부에서 리디렉션 소켓을 시작하면서 포드 외부에서 실행
- **사이드카 유사성**: ztunnel과 애플리케이션 포드 간의 트래픽 리디렉션이 오늘날 사이드카 및 애플리케이션 포드와 매우 유사한 방식으로 이루어짐
- **CNI 투명성**: 노드 네트워크 네임스페이스에서 작동하는 모든 Kubernetes 기본 CNI에서는 엄격히 보이지 않음
- **네트워크 정책 호환**: 네트워크 정책이 CNI가 eBPF를 사용하든 iptables를 사용하든 충돌 없이 모든 Kubernetes 기본 CNI에 의해 계속 시행되고 관리 가능

## 인팟 트래픽 리디렉션

#### 패킷 흐름과 문제점

- **패킷 경로**: 앰비언트 메시에서 포드가 생성한 패킷이 소스 포드를 떠나 노드의 호스트 네트워크 네임스페이스에 들어간 다음, 인터셉트되어 해당 노드의 ztunnel로 리디렉션되어 목적지 포드로 프록시
- **근본적 문제**: 많은 CNI 구현이 존재하며, Linux에서 패킷이 한 네트워크 네임스페이스에서 다른 네트워크 네임스페이스로 이동하는 방식을 구성할 수 있는 근본적으로 다양하고 호환되지 않는 방법들이 많음

#### 다양한 CNI 구현 방식

- **터널 사용**: 터널을 사용하거나, 네트워크를 오버레이하거나, 호스트 네트워크 네임스페이스를 통과하거나, 우회
- **네트워킹 스택**: Linux 사용자 공간 네트워킹 스택을 통과하거나, 이를 건너뛰고 커널 공간 스택에서 패킷을 왕복
- **구현 다양성**: 모든 가능한 접근 방식에 대해 CNI 구현이 있을 가능성이 높음

#### 호환성 문제들

- **작동하지 않는 CNI**: 호스트 네트워크 네임스페이스 패킷 리디렉션에 의존하기 때문에, 패킷을 호스트 네트워크 네임스페이스를 통해 라우팅하지 않는 CNI는 다른 리디렉션 구현 필요
- **규칙 충돌**: 호스트 수준의 규칙이 상충되는 경우 피할 수 없고 잠재적으로 해결할 수 없는 문제 발생
- **복잡한 질문들**:
  - CNI를 가로채는 것이 먼저인가, 아니면 나중에 가로채는 것인가?
  - 어떤 CNI는 하나, 아니면 다른 CNI를 수행하면 깨질까?
  - 네트워크 정책은 호스트 네트워크 네임스페이스에서 시행되어야 하므로 어디서 언제 시행되나?
  - 모든 인기 있는 CNI를 특수하게 구분하기 위해 많은 코드가 필요한가?

## 새로운 Istio Ambient 트래픽 리디렉션 모델

### 새로운 모델의 동작 방식

#### 포드 감지 및 이벤트 처리

- **포드 감지**: istio-CNI 노드 에이전트가 네임스페이스에 `istio.io/dataplane-mode=ambient` 라벨이 붙은 Kubernetes 포드(기존 또는 새로 생성된) 감지

#### 새로운 포드 처리

- **CNI 플러그인 트리거**: 앰비언트 메시에 추가해야 하는 새로운 포드가 시작되면, CRI에 의해 CNI 플러그인(istio-cni 에이전트에 의해 설치 및 관리됨)이 트리거됨
- **포드 이벤트 푸시**: 플러그인이 노드의 istio-cni 에이전트에 새로운 포드 이벤트를 푸시하고 에이전트가 리디렉션을 성공적으로 구성할 때까지 포드 시작을 차단
- **조기 설정**: CRI가 Kubernetes 포드 생성 과정에서 CNI 플러그인을 가능한 한 빨리 호출하기 때문에, 초기 컨테이너와 같은 것에 의존하지 않고 시작 중에 트래픽이 빠져나가지 않도록 충분히 일찍 트래픽 리디렉션 설정 가능

#### 기존 포드 처리

- **동적 추가**: 이미 실행 중인 포드가 앰비언트 메시에 추가되면 새로운 포드 이벤트가 트리거됨
- **API 감시**: istio-CNI 노드 에이전트의 Kubernetes API 감시기가 이를 감지하면 리디렉션도 동일한 방식으로 구성

#### 리디렉션 구성 과정

- **네트워크 네임스페이스 진입**: istio-cni 노드 에이전트가 포드의 네트워크 네임스페이스에 들어가 포드 네트워크 네임스페이스 내부에 네트워크 리디렉션 규칙을 설정
- **패킷 가로채기**: 포드에 들어오고 나가는 패킷을 가로채서 잘 알려진 포트(15008, 15006, 15001)에서 노드 로컬 ztunnel 프록시 인스턴스로 투명하게 리디렉션

#### Ztunnel 통신 및 설정

- **Unix 도메인 소켓 통신**: istio-cni 노드 에이전트가 유닉스 도메인 소켓을 통해 노드 ztunnel에 포드의 네트워크 네임스페이스(15008, 15006, 15001) 내부에 로컬 프록시 리스닝 포트를 설정해야 한다고 알림
- **파일 설명자 제공**: ztunnel에 포드의 네트워크 네임스페이스를 나타내는 저수준 리눅스 파일 설명자를 제공

#### Linux 소켓 API 활용

- **일반적 방식**: 소켓은 리눅스 네트워크 네임스페이스 내에서 실제로 실행되는 프로세스에 의해 생성
- **혁신적 방식**: 생성 시점에 대상 네트워크 네임스페이스가 알려져 있다고 가정하면 리눅스의 저수준 소켓 API를 활용하여 한 네트워크 네임스페이스에서 실행되는 프로세스가 다른 네트워크 네임스페이스에서 리스닝 소켓을 생성할 수 있음

#### Ztunnel 내부 처리

- **전용 프록시 인스턴스**: node-local ztunnel이 내부적으로 새로운 프록시 인스턴스와 리스닝 포트 세트를 스핀업하여 새로 추가된 포드 전용으로 만듦
- **메시 추가 완료**: 인팟 리디렉션 규칙이 적용되고 ztunnel이 청취 포트를 설정하면 이전과 마찬가지로 네트워크에 포드가 추가되고 노드-로컬 ztunnel을 통해 트래픽이 흐르기 시작

### 트래픽 흐름 다이어그램

![]({{ site.url }}/img/post/devops/study/istio/9/20250606141255.png)

### 보안 특성

- **mTLS 암호화**: 포드가 앰비언트 메시에 성공적으로 추가되면, 메시의 포드 간 트래픽은 Istio와 마찬가지로 기본적으로 mTLS로 완전히 암호화
- **암호화된 트래픽**: 트래픽이 암호화된 트래픽으로 포드 네트워크 네임스페이스에 들어오고 나감
- **투명한 기능**: 주변 메시의 모든 포드가 메쉬 정책을 적용하고 트래픽을 안전하게 암호화할 수 있는 기능을 가지고 있는 것처럼 보이지만, 포드에서 실행 중인 사용자 애플리케이션은 이러한 기능을 인식하지 못함

### 혼합 트래픽 처리

- **암호화된 트래픽**: 새 모델에서 주변 메시의 포드 간 암호화된 트래픽 흐름
- **평문 트래픽**: 메쉬 외부에서 암호화되지 않은 평문 트래픽도 필요한 경우 처리하고 정책을 시행 가능

![]({{ site.url }}/img/post/devops/study/istio/9/20250606141429.png)

![]({{ site.url }}/img/post/devops/study/istio/9/20250606141445.png)

- pod의 모든 트래픽은 로컬 ztunnel을 통해 "hairpins"처럼 연결
  - hairpins
    - 패킷이 같은 인터페이스나 경로를 통해 들어왔다가 다시 나가는 현상
    - 트래픽이 마치 U자 모양의 헤어핀처럼 같은 지점을 거쳐 방향을 바꾸는 것
  - pod의 모든 네트워크 트래픽이 ztunnel을 경유하여 U턴 하듯이 처리된다는 의미
- 모든 redirectino은 pod 내에서 발생하며, 호스트 측에서는 아무것도 발생하지 않음
- 실제로 sidecar를 추가하지 않아도 CNI는 이전의 sidecar처럼 보인다.

### 최종 결과

- **포드 내부 처리**: 새로운 앰비언트 캡처 모델의 최종 결과는 모든 트래픽 캡처와 리디렉션이 포드의 네트워크 네임스페이스 내부에서 발생
- **사이드카 모방**: 노드, CNI 및 기타 모든 것에 대해 포드 내부에 사이드카 프록시가 있는 것처럼 보임 (비록 포드에서 사이드카 프록시가 전혀 실행되지 않더라도)

### CNI 관점에서의 투명성

- **CNI 임무**: CNI 구현의 임무는 패킷을 포드로 주고 받는 것
- **설계상 특성**: 설계상으로나 CNI 사양에 따라 그 이후에는 패킷이 어떻게 될지 신경 쓰지 않음

### 호환성 개선

- **충돌 자동 제거**: 이 접근 방식은 다양한 CNI 및 네트워크 정책 구현과의 충돌을 자동으로 제거
- **광범위한 호환성**: 모든 주요 CNI에서 모든 주요 관리 쿠버네티스 제품과의 Istio 앰비언트 메시 호환성을 크게 향상

---
