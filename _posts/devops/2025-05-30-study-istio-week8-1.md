---
layout: post
section-type: post
title: ServiceMesh - Istio - Week8-1
category: devops
tags: ["k8s", "istio", "servicemesh"]
---

# chap13. 가상머신 워크로드를 메시에 통합하기
- 현실적인 워크로드 환경
	- 실제 워크로드는 자주 가상머신이나 물리 머신에서 실행됨
	- 컨테이너와 쿠버네티스는 기술 스택 현대화 노력의 일환으로 사용

- 가상머신 통합의 필요성
	- 레거시 워크로드를 단순히 쿠버네티스로 현대화하는 것이 항상 가능하지 않음
	- 비용을 고려했을 때 불가능에 가까운 경우 존재

- 쿠버네티스 현대화의 제약사항
	- 규제 준수로 인해 온프레미스에서 워크로드 실행 필요
	- 쿠버네티스 클러스터 설정 및 운영 전문 지식 부족
	- 애플리케이션 컨테이너화의 복잡성

- 애플리케이션 컨테이너화의 어려움
	- 애플리케이션 재설계 필요한 경우 존재
	- 의존성 충돌 문제 (의존성 지옥)
	- 실행 중인 가상머신에 고유한 의존성 존재

- 해결 방안
	- 사이드카 프록시 설치 및 설정을 통해 어떤 워크로드든 메시의 일부로 포함 가능
	- 레거시 워크로드를 복원력 있고 안전하고 고가용성적인 방식으로 메시 통합

- 엔터프라이즈에 제공하는 가치
	- 레거시 워크로드 보유 기업에게 흥미로운 기능 제공
	- 애플리케이션 네트워크 계층에서 이스티오로 두 세계 연결
## 이스티오의 가상머신 지원
- 가상머신 지원 발전 과정
	- 이스티오 초기부터 가상머신 메시 통합 지원
	- 제어 평면 외부에서 많은 해결책과 자동화 필요했음
	- 이스티오 1.9.0에서 베타로 승격
	- 핵심 기능 구현 및 적절한 API 접근법 결정

- 핵심 기능들
	- 가상머신에서 사이드카 프록시 설치 및 설정 (istioctl로 간소화)
	- 가상머신의 고가용성 (WorkloadGroup, WorkloadEntry 리소스 도입)
	- 가상머신에서 메시 내 서비스의 DNS 해석 (로컬 DNS 프록시 사용)

- 접근 방식
	- 새 기능들을 고수준에서 다루는 것부터 시작
	- 가상머신을 메시에 통합하는 구체적인 예제로 실습 진행
### 가상머신에서의 사이드카 프록시 설치 및 설정 단순화하기
- 가상머신이 메시 일부가 되기 위한 요구사항
	- 네트워크 트래픽 관리할 사이드카 프록시 설치
	- 프록시가 istiod에 연결해 메시 설정을 받도록 설정
	- istiod 인증용 ID 토큰을 가상머신에 제공


![]({{ site.url }}/img/post/devops/study/istio/8/20250608143631.png)
- 쿠버네티스 워크로드와의 비교
	- 쿠버네티스: 웹훅이나 istioctl로 사이드카 자동 설치/설정
	- 쿠버네티스: ID 토큰을 파드에 자동 주입
	- 가상머신: 이런 편의성이 확장되지 않음

- 가상머신 설정 과정
	- VM 소유자가 직접 프록시 설치 및 설정 필요
	- 워크로드 ID용 부트스트랩 토큰 제공 필요
	- 이후에야 워크로드가 메시의 일부가 될 수 있음

- Single-network 아키텍처
	- 쿠버네티스 클러스터와 VM 워크로드가 동일한 L3 네트워크 공간 공유
	- VM이 istiod와 다른 파드들에 IP로 직접 접근 가능
	- 게이트웨이를 통한 제어 평면 트래픽 라우팅 선택 가능 (필수 아님)
	- 자동 등록 시 VM이 시작 시 istiod에 연결하여 WorkloadEntry 리소스 자동 생성

![]({{ site.url }}/img/post/devops/study/istio/8/20250608143802.png)

- Multi-network 아키텍처
	- VM 워크로드가 쿠버네티스 클러스터와 다른 네트워크에 위치
	- 파드들이 VM의 IP 주소와 직접 통신 불가능
	- Istio east-west 게이트웨이가 네트워크 간 브리지 역할
	- 제어 평면 통신과 데이터 평면 트래픽 모두 게이트웨이를 통해 흘러감
	- VM이 게이트웨이 주소로 설정되어 istiod에 안전하게 연결

![]({{ site.url }}/img/post/devops/study/istio/8/20250608143816.png)
#### 가상머신의 프로비저닝 ID 자세히 살펴보기
- 이스티오의 가상머신 ID 제공 방식
	- 쿠버네티스를 신뢰의 원천으로 사용
	- 쿠버네티스에서 토큰 생성 후 머신에 전달
	- istio-agent가 토큰을 가져가 istiod 인증에 사용

![]({{ site.url }}/img/post/devops/study/istio/8/20250608145636.png)
![]({{ site.url }}/img/post/devops/study/istio/8/20250608145651.png)

- 클러스터 워크로드 vs 가상머신 워크로드 ID 제공 차이
	- 클러스터 워크로드: 서비스 어카운트 토큰을 파드에 자동 주입 → 토큰으로 인증하여 SVID 획득
	- 가상머신: 수작업 필요 → 서비스 어카운트 생성 → 토큰을 가상머신에 전달 → 토큰으로 인증하여 SVID 획득

- 접근법의 유사점과 차이점
	- 유사점: 기본 접근법은 동일
	- 차이점: 쿠버네티스는 토큰을 자동으로 파드에 주입
	- 가상머신: 서비스 메시 운영자가 수작업으로 토큰을 안전하게 전달 필요

- 인증 과정
	- istio-agent가 토큰을 사용해 istiod에 인증
	- istiod가 SVID 형태로 ID 발급

- 솔루션의 단점
	- 서비스 메시 운영자가 쿠버네티스에서 토큰 자동 생성 필요
	- 토큰을 VM으로 안전하게 전송하는 자동화 필요
	- 다중 클라우드 전략 채택 시 작업량이 급격히 증가

- 플랫폼이 할당한 ID (개발 중)
	- 이스티오 커뮤니티에서 개발 중인 해결책
	- 가상머신의 플랫폼 부여 ID를 신뢰의 근원으로 사용
	- istio-agent가 이를 사용해 istiod 인증
	- 이스티오가 클라우드 프로바이더에 토큰 검증 API 노출 예정
	- 아직 개발되지 않았지만 ID 공급자 설계 문서 참조 가능

- 예제에서의 접근법
	- 머신 ID 프로비저닝의 신뢰 원천으로 쿠버네티스 사용
	- 간결함을 위해 토큰을 수작업으로 가상머신에 전달

### 가상머신 고가용성

- 이스티오의 가상머신 고가용성 접근법
	- 쿠버네티스가 컨테이너화된 워크로드에서 사용하는 접근법과 매우 유사하게 모방

- 쿠버네티스의 고가용성 달성 리소스
	- **디플로이먼트(Deployment)**: 고수준 리소스로 복제본 생성 방법에 대한 설정 포함
	- **파드(Pod)**: 디플로이먼트 설정으로 만든 복제본
	    - 파드에 고유한 부분이 없도록 보장
	    - 비정상 시 폐기하고 교체 가능
	    - 불필요 시 축소 가능
	    - 서비스 가용성 유지

- 이스티오의 가상머신용 리소스
	- WorkloadGroup 리소스
		- 쿠버네티스의 디플로이먼트와 유사
		- 관리하는 워크로드 설정 방법에 대한 템플릿 정의
		- 공통 속성 지정:
		    - 애플리케이션이 노출하는 포트
		    - 그룹 인스턴스에 부여하는 레이블
		    - 메시에서 워크로드 ID를 나타내는 서비스 어카운트
		    - 애플리케이션 상태 프로브 방법
	- WorkloadEntry 리소스
		- 쿠버네티스의 파드와 유사
		- 최종 사용자 트래픽을 처리하는 개별 가상머신 표현
		- WorkloadGroup의 공통 속성 + 고유 속성 보유:
		    - 인스턴스의 상태
		    - 주소 등
	- WorkloadEntry 생성 방식
		- 수동 생성 가능
		- **권장 방식**: 워크로드 자동 등록 이용
		    - 새로 뜬 워크로드가 메시에 자동으로 참가

#### 워크로드 자동 등록 이해하기
![]({{ site.url }}/img/post/devops/study/istio/8/20250608160800.png)
- 워크로드 자동 등록 과정
	- 워크로드가 제공받은 설정을 사용해 컨트롤 플레인에 연결
	- ID 토큰으로 자신이 WorkloadGroup의 일원임을 인증
	- 성공 시 컨트롤 플레인이 메시에서 가상머신을 나타내는 WorkloadEntry 생성

- WorkloadEntry 표현의 중요성
	- 쿠버네티스 서비스나 이스티오 ServiceEntry 리소스가 레이블 셀렉터로 워크로드 선택 가능
	- 트래픽을 라우팅할 백엔드로 사용 가능

- 서비스 기반 워크로드 선택의 장점
	- 실제 주소 대신 쿠버네티스 서비스(클러스터 내 FQDN) 사용
	- 클라이언트 측 지식이나 영향 없이 운영 가능:
	    - 비정상 워크로드 폐기
	    - 수요 증가에 따른 새 워크로드 생성

- 서비스의 WorkloadEntry와 파드 타겟팅
	- 서비스를 통해 WorkloadEntry와 파드 모두 대상 지정 가능

- 마이그레이션 활용 사례
	- 가상머신의 레거시 워크로드를 쿠버네티스의 현대화 워크로드로 이전 시 위험 감소
	- 워크로드 병렬 실행 후 서비스 메시의 트래픽 전환 기능 활용
	- 가상머신에서 파드로 트래픽을 점진적 이동
	- 오류 증가 시 가상머신으로 트래픽 롤백 옵션 보유

- 리소스 관계
	- Deployment와 Pod 관계에 대비되는 WorkloadGroup과 WorkloadEntry 관계

![]({{ site.url }}/img/post/devops/study/istio/8/20250608161846.png)
#### 이스티오가 수행하는 헬스 체크 이해하기

- 헬스 체크의 필요성
	- 워크로드가 서비스 메시의 일부가 된 후 트래픽 수신 준비 상태 확인
	- 헬스 체크로 검사받아야 함

- 서비스 고가용성을 위한 두 가지 헬스 체크
	- 쿠버네티스의 헬스 체크 방식과 유사

- Readiness 프로브
	- 워크로드가 시작된 후 트래픽을 수신할 준비가 됐는지 확인
	- 서비스 메시의 관심사

- Liveness 프로브
	- 애플리케이션이 실행 중일 때 정상인지 확인
	- 비정상 시 재시작 필요
	- **서비스 메시의 관심사가 아님**

- Liveness 프로브 책임
	- 워크로드가 실행되는 플랫폼의 기능
	- 플랫폼별 구현 방식:
	    - 쿠버네티스: Deployment 설정에서 정의한 프로브로 liveness 검사
	    - 클라우드 VM: 클라우드 기능을 사용해 liveness 프로브 구현

- 클라우드 프로바이더별 자동 복구
	- 프로브 실패 시 새 인스턴스 생성 등 수정 조치 필요
	- 주요 클라우드 프로바이더 지원:
	    - Azure: VM 스케일 셋에 대한 자동 인스턴스 복구 구현
	    - AWS: 오토 스케일 그룹 인스턴스에 대한 헬스 체크 구현
	    - GCP: 관리형 인스턴스 그룹에 대한 헬스 체크 및 자동 복구 구현

![]({{ site.url }}/img/post/devops/study/istio/8/20250608161923.png)
#### 이스티오가 가상머신에서 readiness 프로브를 구현하는 방법
- Readiness 프로브 구현 방식
	- istio-agent가 WorkloadGroup 정의에 따라 주기적으로 검사
	- 애플리케이션이 트래픽을 받을 준비가 됐는지 확인

- 상태 보고 과정
	- 에이전트가 애플리케이션의 상태를 istiod에 보고
	- 상태 변화 시점에 보고 (정상↔비정상)
	- 사이드카 프록시가 istiod를 애플리케이션 상태 정보로 업데이트

![]({{ site.url }}/img/post/devops/study/istio/8/20250608162508.png)
- 컨트롤 플레인의 라우팅 결정
	- 상태를 사용해 워크로드로 라우팅할지 여부 결정
	- 애플리케이션 정상 시: 데이터 플레인에 VM 엔드포인트 설정
	- 애플리케이션 비정상 시: 데이터 플레인에서 엔드포인트 제거

- 서비스 메시 운영자의 책임
	- WorkloadGroup에 애플리케이션 readiness 검사 설정
	- 클라우드 프로바이더 권장 방법에 따라 인프라 계층에 liveness 검사 생성

- Liveness vs Readiness 프로브 설정 권장사항
	- 서로 다른 설정 사용 추천

- Readiness 프로브 특성
	- istio-agent가 수행
	- 공격적으로 설정해야 함
	- 오류 반환 인스턴스로 트래픽 라우팅 방지

- Liveness 프로브 특성
	- 클라우드 프로바이더가 수행
	- 보수적으로 설정해야 함
	- 가상머신에 복구 시간 제공

- 인스턴스 종료 시 주의사항
	- 인스턴스를 너무 성급하게 종료하지 않도록 주의
	- 유예 기간 없이 진행 중인 요청 종료 시 최종 사용자에게 실패 노출
	- 경험상 좋은 방법: readiness 프로브가 liveness 프로브보다 항상 먼저 실패하도록 설정

### 메시 내 서비스의 DNS 해석
![]({{ site.url }}/img/post/devops/study/istio/8/20250608162549.png)

- DNS 해석 문제
	- 가상머신은 쿠버네티스 클러스터 외부에 위치
	- 쿠버네티스 내부 DNS 서버에 접근할 수 없음
	- 클러스터 서비스의 호스트네임을 해석할 수 없음
	- 가상머신을 서비스 메시에 통합하기 위한 마지막 단계

- DNS 해석이 필요한 이유
	- 서비스 프록시는 트래픽 라우팅 설정을 갖고 있음
	- 문제는 트래픽을 애플리케이션에서 프록시로 가져오는 과정
	- 호스트네임 해석이 전제 조건
	- DNS 해석 실패 시 트래픽이 애플리케이션을 떠나지 않아 엔보이 프록시로 리다이렉트 불가능

![]({{ site.url }}/img/post/devops/study/istio/8/20250608162630.png)

- 기존 해결 방법 (차선책)
	- 모든 쿠버네티스 서비스가 설정된 프라이빗 DNS 서버 사용
	- 가상머신을 네임서버로 프라이빗 DNS 서버 사용하도록 설정
	- 동적 워크로드 특성으로 인해 자동화 필요
	- 쿠버네티스 컨트롤러가 변경 사항 수신하여 DNS 서버 동기화
	- external-dns 오픈소스 솔루션 활용 가능
	- 통합 솔루션이 아닌 차선책

![]({{ site.url }}/img/post/devops/study/istio/8/20250608162712.png)
- 이스티오의 통합 솔루션
	- 이스티오 1.8 이상에서 istio-agent 사이드카에 로컬 DNS 프록시 도입
	- istiod가 DNS 프록시에 메시 내 모든 서비스 설정

![]({{ site.url }}/img/post/devops/study/istio/8/20250608162808.png)

- DNS 프록시 동작 방식
	- 엔보이 프록시와 함께 이스티오 사이드카로 동작
	- 애플리케이션의 DNS 쿼리 처리
	- Iptable 규칙을 사용해 DNS 쿼리를 DNS 프록시로 리다이렉트
	- istio-cni 사용 시 과정이 약간 다름

- NDS (Name Discovery Service)
	- DNS 프록시 지속적 업데이트를 위한 새 API
	- 메시에 쿠버네티스 서비스나 이스티오 ServiceEntry 추가 시 컨트롤 플레인이 데이터 플레인에 새 DNS 항목 동기화

- DNS 프록시의 추가 기능
	- 가상머신에만 국한되지 않음
	- 여러 추가 기능 제공 가능

![]({{ site.url }}/img/post/devops/study/istio/8/20250608162832.png)
## 가상머신까지 메시 확장
### istiod와 클러스터 서비스들을 가상머신에 노출하기
- 가상머신이 메시에 통합되려면 **istiod와 통신** + **클러스터 서비스 연결** 필수
- 같은 네트워크에서는 기본 동작하지만, **별도 네트워크에서는 east-west 게이트웨이 필요**

#### East-West 게이트웨이 설치
**1. 게이트웨이 구성**
```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-eastwestgateway
spec:
  profile: empty
  components:
    ingressGateways:
    - name: istio-eastwestgateway
      k8s:
        env:
        - name: ISTIO_META_ROUTER_MODE
          value: "sni-dnat"
        service:
          ports:
          - name: mtls
            port: 15443
            targetPort: 15443
          - name: tcp-istiod
            port: 15012
            targetPort: 15012
          - name: tcp-webhook
            port: 15017
            targetPort: 15017
```

**2. 설치 및 확인**
```bash
istioctl install -f cluster-east-west-gw.yaml -y
kubectl get svc -n istio-system istio-eastwestgateway
# LoadBalancer 타입으로 외부 IP 할당 확인
```

#### 필수 포트 노출
**1. 다중 클러스터 mTLS 포트 (15443) 노출**
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: cross-network-gateway
spec:
  selector:
    istio: eastwestgateway
  servers:
  - port:
      number: 15443
      protocol: TLS
    tls:
      mode: AUTO_PASSTHROUGH
    hosts:
    - "*.local"
```

**2. istiod 포트 (15012, 15017) 노출**
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: istiod-gateway
spec:
  servers:
  - port:
      number: 15012
      protocol: tls
    tls:
      mode: PASSTHROUGH
    hosts: ["*"]
  - port:
      number: 15017
      protocol: tls
    tls:
      mode: PASSTHROUGH
    hosts: ["*"]
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: istiod-vs
spec:
  tls:
  - match:
    - port: 15012
    route:
    - destination:
        host: istiod.istio-system.svc.cluster.local
        port:
          number: 15012
  - match:
    - port: 15017
    route:
    - destination:
        host: istiod.istio-system.svc.cluster.local
        port:
          number: 443
```

#### 포트 매핑

|**포트**|**용도**|**대상**|
---|---|---
**15443** |다중 클러스터 mTLS | VM → 클러스터 서비스
**15012** |istiod XDS API|VM → istiod 구성
**15017** |istiod Webhook|VM → istiod 인증서

![]({{ site.url }}/img/post/devops/study/istio/8/20250608163247.png)

#### 설정 완료 확인

```bash
kubectl get gw,vs -A
# 결과: cross-network-gateway, istiod-gateway, istiod-vs 생성 확인
```

### WorkloadGroup으로 워크로드 그룹 나타내기
- **가상머신들의 공통 속성 정의**: 노출할 포트, 헬스체크 방법 등
- **자동 등록 활성화**: 유효한 토큰을 가진 워크로드 자동 등록

#### WorkloadGroup 구성
핵심 속성
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: WorkloadGroup
metadata:
  name: forum
  namespace: forum-services
spec:
  metadata:
    labels:
      app: forum  # 서비스가 레이블로 워크로드 선택
  template:
    serviceAccount: forum-sa  # 등록 시 필요한 인증 토큰
    network: vm-network       # 트래픽 라우팅 설정용
  probe:  # 헬스체크 설정
    periodSeconds: 5
    initialDelaySeconds: 1
    httpGet:
      port: 8080
      path: /api/healthz
```

주요 속성
- **labels**: 쿠버네티스 서비스가 WorkloadEntry 선택 시 사용
- **network**: 컨트롤 플레인이 트래픽 라우팅 설정 (같은 네트워크면 IP, 다른 네트워크면 east-west 게이트웨이)
- **serviceAccount**: 워크로드 ID, 그룹 멤버 등록 시 필수

#### WorkloadGroup 생성 과정

**1. 사전 준비**

```bash
kubectl create namespace forum-services
kubectl create serviceaccount forum-sa -n forum-services
kubectl apply -f workloadgroup.yaml
```

**2. 확인**

```bash
kubectl get workloadgroup -n forum-services
# 결과: forum WorkloadGroup 생성 확인
```

#### 가상머신 사이드카 설정 생성

**1. istioctl을 통한 설정 생성**
```bash
istioctl x workload entry configure \
  -f workloadgroup.yaml \
  -o /tmp/my-workload-files/ \
  --clusterID "west-cluster" \
  --autoregister
```

**2. 생성된 파일 구성**
```
/tmp/my-workload-files/
├── cluster.env      # 클러스터 환경 설정
├── hosts           # east-west 게이트웨이 IP 매핑
├── istio-token     # 서비스 어카운트 토큰
├── mesh.yaml       # 메시 및 네트워크 설정
└── root-cert.pem   # 루트 인증서
```

#### 주요 설정 파일 내용

**1. hosts 파일**

```
192.168.10.10 istiod.istio-system.svc
```

**2. istio-token (JWT 토큰)**

```json
{
  "aud": ["istio-ca"],
  "kubernetes.io": {
    "namespace": "forum-services",
    "serviceaccount": {
      "name": "forum-sa"
    }
  },
  "sub": "system:serviceaccount:forum-services:forum-sa"
}
```

**3. mesh.yaml (주요 설정)**

```yaml
defaultConfig:
  discoveryAddress: istiod.istio-system.svc:15012
  meshId: usmesh
  proxyMetadata:
    ISTIO_META_AUTO_REGISTER_GROUP: forum
    ISTIO_META_CLUSTER_ID: west-cluster
    ISTIO_META_DNS_CAPTURE: "true"
    ISTIO_META_NETWORK: vm-network
    SERVICE_ACCOUNT: forum-sa
  readinessProbe:
    httpGet:
      path: /api/healthz
      port: 8080
```

#### 보안 파일 전송

1. 안전한 전송 (SSH 사용)
```bash
# 생성된 파일을 가상머신으로 복사
scp -i ~/.ssh/key.pem ./my-workload-files/* ubuntu@$FORUM_IP:/tmp/
```

2. 보안 고려사항
- **민감 정보 포함**: 서비스 어카운트 토큰
- **운영 환경**: 자동화된 안전한 전송 방식 필요
- **시연 목적**: SSH 복사 사용 (간단하지만 수작업)

#### 설정 완료 후 상태
- **east-west 게이트웨이 IP**: istiod 노출 경로
- **루트 인증서**: istiod 인증서 검증용
- **서비스 어카운트 토큰**: WorkloadGroup 멤버 인증
- **메시 설정**: 네트워크 및 공통 속성

### 가상머신에 istio-agent 설치 및 설정하기


#### 사전 환경 확인

**1. DNS 설정 확인**
```bash
cat /etc/resolv.conf  # nameserver 127.0.0.53
ss -tnlp             # systemd-resolve가 127.0.0.53:53에서 리스닝
resolvectl status    # resolv.conf mode: stub
```

**2. iptables 상태 확인**
```bash
iptables -t nat -L -n -v    # 기존 NAT 규칙 확인
iptables -t raw -L -n -v    # 기존 RAW 규칙 확인
```

#### istio-agent 설치
**1. 데비안 패키지 다운로드 및 설치**
```bash
curl -LO https://storage.googleapis.com/istio-release/releases/1.17.8/deb/istio-sidecar.deb
dpkg -i istio-sidecar.deb
```

**2. 설치 확인**
```bash
which pilot-agent  # /usr/local/bin/pilot-agent
pilot-agent version
which envoy        # /usr/local/bin/envoy
envoy --version
```

**3. 설치된 디렉터리 구조**
```
/etc/istio/
├── config/
├── envoy/
├── extensions/
└── proxy/

/var/lib/istio/
├── config/
├── envoy/
├── extensions/
└── proxy/
```

#### 설정 파일 배치
**1. 필수 디렉터리 생성**
```bash
mkdir -p /etc/certs
mkdir -p /var/run/secrets/tokens
```

**2. 설정 파일 복사**
```bash
cp /tmp/root-cert.pem /etc/certs/root-cert.pem
cp /tmp/istio-token /var/run/secrets/tokens/istio-token
cp /tmp/cluster.env /var/lib/istio/envoy/cluster.env
cp /tmp/mesh.yaml /etc/istio/config/mesh
```

**3. hosts 파일 설정**
```bash
echo "192.168.10.10 istiod.istio-system.svc" >> /etc/hosts
```

#### 권한 설정
**1. istio-proxy 사용자 확인**
```bash
cat /etc/passwd | grep istio-proxy
# istio-proxy:x:998:999::/var/lib/istio:/bin/sh
```

**2. 디렉터리 소유권 변경**
```bash
chown -R istio-proxy /var/lib/istio /etc/certs /etc/istio/proxy \
                     /etc/istio/config /var/run/secrets /etc/certs/root-cert.pem
```

#### istio 서비스 시작
**1. 서비스 활성화 및 시작**
```bash
systemctl start istio
systemctl enable istio
systemctl status istio
```

**2. 프로세스 확인**
```bash
ps aux | grep istio
# 결과: pilot-agent와 envoy 프로세스 실행 확인
```

**3. iptables 규칙 자동 생성 확인**
```bash
iptables -t nat -L -n -v  # ISTIO_* 체인들 생성 확인
```

#### 연결 및 등록 확인
1. 에이전트 로그 확인
```bash
cat /var/log/istio/istio.log | grep xdsproxy
# 결과: "connected to upstream XDS server: istiod.istio-system.svc:15012"
```

2. 로그 위치
- **표준 출력**: `/var/log/istio/istio.log`
- **표준 오류**: `/var/log/istio/istio.err`
- **systemd 로그**: `journalctl -u istio -f`

3. WorkloadEntry 자동 생성 확인
```bash
kubectl get workloadentries -n forum-services
# 결과: forum-192.168.10.200-vm-network 자동 생성
```

4. 프록시 상태 확인
```bash
istioctl proxy-status
# 결과: forum-vm.forum-services가 SYNCED 상태로 표시
```

#### 생성된 인증서 확인
```bash
tree /etc/certs/
├── cert-chain.pem  # 자동 생성된 인증서 체인
├── key.pem         # 자동 생성된 프라이빗 키
└── root-cert.pem   # 복사한 루트 인증서
```

#### 주요 고려사항
1. DNS 해석
- 초기에는 컨트롤 플레인 연결 전이므로 DNS 프록시 항목 없음
- `/etc/hosts`에 east-west 게이트웨이 정적 정의 필요
- 운영환경에서는 네트워크 로드 밸런서 사용 권장

2. 헬스체크 상태
```bash
kubectl get workloadentries -n forum-services -o yaml
# status.conditions에서 헬스체크 실패 시 "status: False" 표시
```

### 클러스터 서비스로 트래픽 라우팅하기
- 가상머신에서 클러스터 내 서비스로 트래픽이 정상 라우팅되는지 확인
- DNS 해석 및 프록시를 통한 연결 과정 검증

#### 기본 연결 테스트
1. DNS 해석 확인
```bash
dig +short webapp.istioinaction
# 결과: 10.10.200.48 (클러스터 서비스 IP)
```

2. HTTP 요청 테스트
```bash
curl -s webapp.istioinaction/api/catalog/items/1 | jq
watch curl -s webapp.istioinaction/api/catalog/items/1
```

#### 연결 상태 모니터링
1. 네트워크 연결 확인
```bash
watch -d 'ss -tnp | grep envoy'
ESTAB 0 0 192.168.10.200:41238 192.168.10.10:15443 users:(("envoy",pid=3203,fd=40))
ESTAB 0 0 192.168.10.200:41242 192.168.10.10:15443 users:(("envoy",pid=3203,fd=41))
```

포트 매핑
- **15053**: DNS 프록시 포트
- **15001**: Envoy 아웃바운드 리스너
- **15443**: East-west 게이트웨이 mTLS 포트

2. iptables 규칙 동작 확인
```bash
watch -d iptables -t nat -L -n -v  # NAT 규칙 카운터 변화
watch -d iptables -t raw -L -n -v  # RAW 규칙 동작
```

3. 패킷 모니터링
```bash
tcpdump -i any -w - udp port 53 | termshark  # DNS 쿼리 모니터링
```

#### 트래픽 라우팅 과정 (4단계)
1단계: DNS 해석
- 애플리케이션이 `webapp.istioinaction` 호스트네임 해석 요청
- **iptables 규칙**이 DNS 쿼리를 **DNS 프록시(15053 포트)**로 리디렉트
- DNS 프록시가 클러스터 서비스 IP 반환

2단계: 아웃바운드 요청 시작
- IP 주소 해석 완료 후 애플리케이션이 HTTP 요청 시작
- **iptables 규칙**이 아웃바운드 트래픽을 **Envoy 프록시(15001 포트)**로 리디렉트

3단계: East-West 게이트웨이 라우팅
- Envoy 프록시가 트래픽을 **east-west 게이트웨이(15443 포트)**로 라우팅
- 게이트웨이가 다른 네트워크 간 브릿지 역할 수행

4단계: 최종 서비스 전달
- East-west 게이트웨이가 요청을 **webapp 서비스**로 프록시
- webapp이 catalog 서비스에 아이템 쿼리 후 응답 반환

### **서비스 및 엔드포인트 확인**

**클러스터 내 서비스 상태**

```bash
kubectl get svc,ep -n istioinaction webapp
# 결과:
# service/webapp   ClusterIP   10.10.200.48   <none>   80/TCP
# endpoints/webapp   172.16.0.8:8080
```

### **추가 검증 (옵션)**

**외부에서 webapp 접속 테스트**

```bash
while true; do curl -s -H "Host: webapp.istioinaction.io" http://$APP_IP:30000/api/catalog/ ; echo; date; sleep 1; done
```

![]({{ site.url }}/img/post/devops/study/istio/8/20250608164814.png)

### 트래픽을 WorkloadEntry로 라우팅하기
- 클러스터 내부에서 가상머신 워크로드로의 트래픽 라우팅 검증
- 헬스체크를 통한 트래픽 제어 메커니즘 확인

#### 쿠버네티스 서비스 생성
**1. 서비스 정의 및 생성**
```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    app: forum
  name: forum
spec:
  ports:
  - name: http
    port: 80
    targetPort: 8080
  selector:
    app: forum  # WorkloadEntry의 레이블과 매칭
```

```bash
kubectl apply -f istio-in-action/book-source-code-master/services/forum/kubernetes/forum-svc.yaml -n forum-services
kubectl get svc,ep -n forum-services
NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE service/forum ClusterIP 10.10.200.72 <none> 80/TCP 20s NAME ENDPOINTS AGE endpoints/forum <none> 20s
```
#### 프록시 설정 확인
**1. 라우트 설정 확인**
```bash
istioctl proxy-config route deploy/webapp.istioinaction --name 80 -o json
{
  "name": "forum.forum-services.svc.cluster.local:80",
  "domains": [
    "forum.forum-services.svc.cluster.local",
    "forum.forum-services",
    "forum.forum-services.svc",
    "10.10.200.72"
  ],
  "routes": [{
    "route": {
      "cluster": "outbound|80||forum.forum-services.svc.cluster.local"
    }
  }]
}
```

**2. 클러스터 및 엔드포인트 확인**
```bash
istioctl proxy-config cluster deploy/webapp.istioinaction --fqdn forum.forum-services.svc.cluster.local
istioctl proxy-config endpoint deploy/webapp.istioinaction | grep forum
# 결과: 아직 엔드포인트 없음
```
#### Forum 애플리케이션 시작
**1. 애플리케이션 다운로드 및 실행**
```bash
# forum-vm에서 실행
export ISTIOV=1.17.8
echo 'export ISTIOV=1.17.8' >> /root/.bashrc

curl -s -L https://istio.io/downloadIstio | ISTIO_VERSION=$ISTIOV sh -
cp istio-$ISTIOV/bin/istioctl /usr/local/bin/istioctl

#
curl -s localhost:15000/config_dump | istioctl proxy-config listener --file -
curl -s localhost:15000/config_dump | istioctl proxy-config route --file -
curl -s localhost:15000/config_dump | istioctl proxy-config clusters --file -
curl -s localhost:15000/config_dump | istioctl proxy-config endpoint --file -
curl -s localhost:15000/config_dump | istioctl proxy-config secret --file -
RESOURCE NAME     TYPE           STATUS     VALID CERT     SERIAL NUMBER                               NOT AFTER                NOT BEFORE
default           Cert Chain     ACTIVE     true           310309461583688467984066399721764000962     2025-05-26T01:09:42Z     2025-05-25T01:07:42Z
ROOTCA            CA             ACTIVE     true           46141372426695670978289547947687101983      2035-05-23T01:04:09Z     2025-05-25T01:04:09Z

```

**2. 애플리케이션 상태 확인**

```bash
#
istioctl proxy-config cluster deploy/webapp.istioinaction --fqdn forum.forum-services.svc.cluster.local
istioctl proxy-config endpoint deploy/webapp.istioinaction | grep forum

# 로그 모니터링
kubectl logs -n istioinaction deploy/webapp -c istio-proxy -f
[2025-05-25T04:53:18.841Z] "GET /api/users HTTP/1.1" 503 UH no_healthy_upstream - "-" 0 19 0 - "" "beegoServer" "63377970-9d0f-4591-a4d4-039b4321863d" "forum.forum-services:80" "-" outbound|80||forum.forum-services.svc.cluster.local - 10.10.200.72:80 :0 - default
[2025-05-25T04:53:18.839Z] "GET /api/users HTTP/1.1" 500 - via_upstream - "-" 0 27 2 2 "" "curl/8.7.1" "63377970-9d0f-4591-a4d4-039b4321863d" "webapp.istioinaction.io" "172.16.0.8:8080" inbound|8080|| 127.0.0.6:36439 172.16.0.8:8080 :0 outbound_.80_._.webapp.istioinaction.svc.cluster.local default

# 자신의 PC
curl -s -H "Host: webapp.istioinaction.io" http://$APP_IP:30000/api/catalog/
while true; do curl -s -H "Host: webapp.istioinaction.io" http://$APP_IP:30000/api/catalog/ ; echo; date; sleep 1; done

curl -s -H "Host: webapp.istioinaction.io" http://$APP_IP:30000/api/users
curl -s -H "Host: webapp.istioinaction.io" http://$APP_IP:30000/api/users -I
HTTP/1.1 500 Internal Server Error
```

![]({{ site.url }}/img/post/devops/study/istio/8/20250608165555.png)

### **성공적인 트래픽 라우팅**

**1. 엔드포인트 자동 등록 확인**

```bash
istioctl proxy-config endpoint deploy/webapp.istioinaction --cluster 'outbound|80||forum.forum-services.svc.cluster.local'
# 결과: 192.168.10.200:8080 HEALTHY OK
```

**2. WorkloadEntry 헬스 상태 업데이트**

```yaml
status:
  conditions:
  - status: "True"  # 헬스체크 성공
    type: Healthy
```

**3. 성공적인 요청**

```bash
# 자신의 PC
curl -s -H "Host: webapp.istioinaction.io" http://$APP_IP:30000/api/users
while true; do curl -s -H "Host: webapp.istioinaction.io" http://$APP_IP:30000/api/users ; echo; date; sleep 1; done

# 로그 모니터링
kubectl logs -n istioinaction deploy/webapp -c istio-proxy -f
[2025-05-25T05:05:51.328Z] "GET /api/users HTTP/1.1" 200 - via_upstream - "-" 0 5645 28 27 "218.153.65.54" "beegoServer" "888f982d-f7f3-4232-ac0b-826cf65ef294" "forum.forum-services:80" "192.168.10.200:8080" outbound|80||forum.forum-services.svc.cluster.local 172.16.0.8:38170 10.10.200.72:80 218.153.65.54:0 - default
[2025-05-25T05:05:51.326Z] "GET /api/users HTTP/1.1" 200 - via_upstream - "-" 0 3679 30 30 "218.153.65.54" "curl/8.7.1" "888f982d-f7f3-4232-ac0b-826cf65ef294" "webapp.istioinaction.io" "172.16.0.8:8080" inbound|8080|| 127.0.0.6:36439 172.16.0.8:8080 218.153.65.54:0 outbound_.80_._.webapp.istioinaction.svc.cluster.local default

```

- **200 상태 코드**: 성공적인 응답
- **192.168.10.200:8080**: 실제 가상머신 엔드포인트로 라우팅
- **via_upstream**: 업스트림 서비스를 통한 응답

![]({{ site.url }}/img/post/devops/study/istio/8/20250608194454.png)

**Istio의 자동 트래픽 관리:**
- **헬스체크 실패 시**: 데이터 플레인에서 엔드포인트 제외
- **헬스체크 성공 시**: 엔드포인트 자동 등록 및 트래픽 라우팅
- **클라이언트 보호**: 오류 반환 인스턴스로의 트래픽 방지

### 컨트롤 플레인이 가상머신 설정: 상호 인증 강제
- 가상머신에 Istio 보안 정책 적용 검증
- PeerAuthentication을 통한 mTLS 강제로 무단 접근 차단

#### 초기 보안 상태 (취약점)
1. 현재 문제점
- 가상머신의 8080 포트가 직접 노출
- 권한 없는 사용자도 직접 접근 가능
- 메시 외부에서 암호화되지 않은 요청 처리

2. 취약점 확인
```bash
# 자신의 PC에서 직접 요청 (메시 외부)
curl -is $FORUM:8080/api/users | grep HTTP
# 결과: HTTP/1.1 200 OK (접근 성공 - 보안 문제)
```

#### PeerAuthentication 정책 적용
```bash
# Strict mTLS 정책 생성
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system  # 메시 전체 적용
spec:
  mtls:
    mode: STRICT  # 상호 인증 강제
	
# 정책 적용
kubectl apply -f strict-peer-auth.yaml
kubectl get peerauthentication -A
# 결과: default PeerAuthentication 생성 확인
```

#### **보안 정책 효과 검증**
```bash
# 메시 외부 접근 차단 확인
# 자신의 PC에서 직접 요청 (실패 예상)
curl -is $FORUM:8080/api/users -v
# 결과: 연결 실패 또는 타임아웃 (mTLS 없는 접근 차단)

# 메시 내부 트래픽 정상 동작 확인
# istio-ingressgateway 경유 요청 (성공 예상)
while true; do 
  curl -s -H "Host: webapp.istioinaction.io" http://$APP_IP:30000/api/users
  echo; date; sleep 1
done
# 결과: 계속 성공적인 응답 (mTLS로 보호된 메시 내부 통신)
```

- 이를 통해 가상머신이 단순히 메시에 연결된 것이 아니라, **클러스터 워크로드와 동일한 수준의 보안 정책과 관리를 받는 완전한 메시 멤버**임을 확인
- PeerAuthentication은 하나의 예시이며, 모든 Istio API를 가상머신 프록시 설정에 활용할 수 있음

## DNS 프록시 이해하기
### DNS 프록시가 클러스터 호스트네임을 해석하는 방법(5단계)
![]({{ site.url }}/img/post/devops/study/istio/8/20250607205529.png)

1. DNS 쿼리 생성
- 클라이언트가 `webapp.istioinaction` 해석을 위해 **DNS 쿼리** 생성

2. 운영체제 DNS 처리
- 운영체제가 DNS 해석 처리
- 먼저 **hosts 파일**에서 호스트네임 일치 항목 확인
- 일치 항목 없으면 **기본 DNS 해석기**로 전달

3. 기본 DNS 해석기 (Ubuntu)
- **systemd-resolverd**가 기본 DNS 해석기
- **루프백 주소 127.0.0.53의 53 포트**에서 리스닝
- 하지만 요청이 거기에 도달하지 않음
- **istio-agent가 설정한 iptables 규칙**이 **DNS 프록시로 리디렉트**

4. DNS 프록시 처리
- **서비스 메시 내 알려진 서비스 해석용 항목** 포함
- 호스트네임 일치 시 해석 (`webapp.istioinaction` 해당)
- **컨트롤 플레인이 NDS로 설정**

5. 외부 DNS 위임
- 클러스터 서비스가 아닌 경우 DNS 프록시가 물러남
- **resolv.conf 파일에 명시된 네임서버**로 전달
- 여기서 호스트네임 해석 성공/실패 결정

### iptables 규칙 확인
**DNS 트래픽 리디렉션**
```bash
iptables-save | grep 'to-ports 15053'
-A OUTPUT -d 127.0.0.53/32 -p udp -m udp --dport 53 -j REDIRECT --to-ports 15053
-A ISTIO_OUTPUT -d 127.0.0.53/32 -p tcp -m tcp --dport 53 -j REDIRECT --to-ports 15053
```

### DNS 프록시 포트 확인
**pilot-agent가 15053 포트에서 리스닝**
```bash
netstat -ltunp | egrep 'PID|15053'
tcp  0  0  127.0.0.1:15053  0.0.0.0:*  LISTEN  3195/pilot-agent
udp  0  0  127.0.0.1:15053  0.0.0.0:*          3195/pilot-agent
```

### DNS 쿼리 테스트
**클러스터 서비스 해석**
```bash
dig +short @localhost -p 15053 webapp.istioinaction
# 결과: 10.10.200.48

dig +short @localhost -p 15053 catalog.istioinaction
dig +short @localhost -p 15053 forum.forum-services
```

**외부 도메인 해석**
```bash
dig +short @localhost -p 15053 www.daum.net
# 결과: daum-4vdtymgd.kgslb.com. / 121.53.105.193
```

### 핵심 특징
- **proxyConfig.proxyMetadata ISTIO_META_DNS_CAPTURE="true"** 설정 시 규칙 추가
- **pilot-agent**가 TCP/UDP 모두 처리
- 애플리케이션은 **자동 리디렉션**으로 별도 설정 불필요
- **컨트롤 플레인의 NDS**가 DNS 프록시 항목 설정

### DNS 프록시가 인식하는 호스트네임은 무엇인가?
**DNS 프록시 동작 원리:**
- **istiod가 알고 있는 서비스들**로 DNS 프록시 설정
- **istio-agent가 호스트네임의 짧은 변형들 생성**
- DNS 프록시 내 레코드로 **클러스터 내 서비스 호스트네임 해석**
- **클러스터 외부 호스트네임** 쿼리는 **머신의 기본 네임서버**로 전달

**지원하는 해석 범위:**
- 클러스터 내 서비스 (다양한 변형 지원)
- 외부 퍼블릭 도메인 (기본 네임서버로 위임)

```bash
# 워크로드 목록 확인
istioctl proxy-status | awk '{print $1}'
catalog-77fdb4997c-f8qj4.istioinaction
istio-eastwestgateway-86f6cb4699-4xfsn.istio-system
istio-ingressgateway-7b7ccd6454-pv8zp.istio-system
forum-vm.forum-services
webapp-684c568c59-vrj97.istioinaction

# 특정 워크로드의 NDS 설정 조회
# NDS 설정을 가져올 때 proxyID 파라미터에 이름을 사용한다.
kubectl -n istio-system exec deploy/istiod -- curl -Ls "localhost:8080/debug/ndsz?proxyID=forum-vm.forum-services" | jq
{
  "resource": {
    "@type": "type.googleapis.com/istio.networking.nds.v1.NameTable",
    "table": {
      "catalog.istioinaction.svc.cluster.local": {
        "ips": [
          "10.10.200.138"
        ],
        "registry": "Kubernetes",
        "shortname": "catalog",
        "namespace": "istioinaction"
      },
      "forum.forum-services.svc.cluster.local": {
        "ips": [
          "10.10.200.72"
        ],
        "registry": "Kubernetes",
        "shortname": "forum",
        "namespace": "forum-services"
      },
      "webapp.istioinaction.svc.cluster.local": {
        "ips": [
          "10.10.200.48"
        ],
        "registry": "Kubernetes",
        "shortname": "webapp",
        "namespace": "istioinaction"
      },
...

```
### 호스트네임 변형 생성 과정
1. NDS에는 FQDN만 포함
- NDS 설정에는 `webapp.istioinaction.svc.cluster.local`만 존재
- 짧은 변형(`webapp.istioinaction`)은 **직접 포함되지 않음**

2. istio-agent가 변형 생성
- istio-agent가 NDS 설정 수신 시 **쿠버네티스 클러스터 경험과 일치**시키기 위해 변형 생성
- 생성되는 변형들:
    - webapp.istioinaction
    - webapp.istioinaction.svc
    - webapp.istioinaction.svc.cluster

3. 모든 변형이 동일한 IP로 해석
- 모든 변형이 **동일한 IP 목록**으로 해석 (예: 10.10.200.48)

```bash
# 라우트 설정에서 확인
#
istioctl proxy-config route deploy/webapp.istioinaction --name 80 -o json
...
                "name": "webapp.istioinaction.svc.cluster.local:80",
                "domains": [
                    "webapp.istioinaction.svc.cluster.local",
                    "webapp",
                    "webapp.istioinaction.svc",
                    "webapp.istioinaction",
                    "10.10.200.48"
...
```
## 에이전트 동작 커스터마이징하기
### 커스터마이징 가능한 설정
**주요 설정 옵션:**
- 로그 내용 및 형식
- 로그 레벨 조정
- 인증서 발급 요청 시 인증서 수명 설정
- 기타 에이전트 동작 파라미터

### 설정 파일 위치
**사이드카 설정 파일:**
- **경로**: `/var/lib/istio/envoy/sidecar.env`
- 이 파일을 수정하여 에이전트 동작 변경

```bash
# 현재 설정 확인
cat /var/lib/istio/envoy/sidecar.env
grep "^[^#]" /var/lib/istio/envoy/sidecar.env # 주석 처리

# 새로운 설정 추가
## DNS 프록시 로깅 수준: debug로 상향
echo 'ISTIO_AGENT_FLAGS="--log_output_level=dns:debug"' >> /var/lib/istio/envoy/sidecar.env
# 인증서 수명: 12시간
echo 'SECRET_TTL="12h0m0s"' >> /var/lib/istio/envoy/sidecar.env
# 설정 확인
grep "^[^#]" /var/lib/istio/envoy/sidecar.env # 주석 처리
ISTIO_AGENT_FLAGS="--log_output_level=dns:debug"
SECRET_TTL="12h0m0s"

# 변경 사항 적용
systemctl restart istio

# www.daum.net 도메인은 질의 처리를 하지 못해서, 로컬에 resolver DNS 서버를 통해 질의 로그 확인.
tail -f /var/log/istio/istio.log
2025-05-25T07:23:03.660035Z	debug	dns	response for hostname "www.daum.net." not found in dns proxy, querying upstream
2025-05-25T07:23:03.662845Z	debug	dns	upstream response for hostname "www.daum.net." : ;; opcode: QUERY, status: NOERROR, id: 30399
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version 0; flags: ; udp: 65494

;; QUESTION SECTION:
;www.daum.net.	IN	 A

;; ANSWER SECTION:
www.daum.net.	77	IN	CNAME	daum-4vdtymgd.kgslb.com.
daum-4vdtymgd.kgslb.com.	5	IN	A	121.53.105.193

# DNS 쿼리 테스트
dig +short @localhost -p 15053 www.daum.ne
```

### 로그에서 확인 가능한 정보
**DNS 처리 과정:**
- 클러스터 내 서비스가 아닌 경우 **"not found in dns proxy"** 메시지
- **"querying upstream"**으로 외부 DNS 서버로 위임
- **upstream response**로 실제 DNS 응답 내용 표시

### 인증서 확인
**인증서 로테이션 후 확인:**
- **경로**: `/etc/certs/cert-chain.pem`
- 새 인증서의 만료 시간 검사 가능
- SECRET_TTL 설정에 따라 12시간마다 갱신

**참조 문서**: [Istio pilot-agent](https://istio.io/latest/docs/reference/commands/pilot-agent/) 공식 문서

## 메시에서 WorkloadEntry 제거하기
- 가상머신을 삭제하면 WorkloadEntry는 자동 정리된다.

```bash
# 자동 정리 확인
kubectl get workloadentries -A
```
- **자동 등록만큼 자동 삭제도 중요**
- **클라우드 네이티브 워크로드의 일시성** 지원
- 메시의 일관성 및 정확성 유지

### **쿠버네티스 vs 가상머신 구현 차이**

| **기능**            | **쿠버네티스 구현**                             | **가상머신 구현**                                 |
| ----------------- | ---------------------------------------- | ------------------------------------------- |
| **프록시 설치**        | istioctl 직접 주입 또는 웹훅 자동 주입               | 직접 다운로드해 설치                                 |
| **프록시 설정**        | 사이드카 주입 중 완료                             | istioctl로 WorkloadGroup에서 설정 생성 후 가상머신으로 전송 |
| **워크로드 ID 부트스트랩** | 서비스 어카운트 토큰이 쿠버네티스 메커니즘으로 주입             | 서비스 어카운트 토큰을 가상머신으로 수작업 전송                  |
| **헬스 체크**         | 쿠버네티스가 Readiness/Liveness 프로브 수행         | WorkloadGroup에 Readiness 프로브 설정             |
| **등록**            | 쿠버네티스가 처리                                | WorkloadGroup 구성원으로 가상머신 자동 등록              |
| **DNS 해석**        | 클러스터 내 FQDN 해석에 DNS 서버 사용, DNS 프록시는 선택사항 | istiod가 DNS 프록시 설정해 FQDN 해석                 |

### 실제 프로젝트 고려사항
1. 수작업 방식의 한계
- 메시가 **매우 취약**해짐
- **새벽 3시 긴급 복구** 상황 발생 가능
- 수작업 재구성 및 메시 등록 필요

2. 자동화의 필요성
- **가상머신 구축 및 배포 자동화** 필수
- 현재 프로젝트들이 이미 좋은 관행 보유

3. 권장 자동화 도구
- **Packer** (packer.io): 이미지 빌드
- **Ansible** (ansible.com): 구성 관리
- **Terraform** (terraform.io): 인프라 프로비저닝

### 기존 자동화 활용 방안

1. 기존 자동화 스크립트 업데이트
- **Istio 사이드카 설치** 추가
- **설정과 토큰 제공** 로직 포함
- 애플리케이션 배포 과정에 통합

2. 최종 결과
- **가상머신이 메시에 자동 통합**
- 수작업 개입 최소화
- **안정적이고 확장 가능한** 메시 운영

## 요약
- 가상머신 메시 통합 현황
	- Istio 1.24(2024년 11월)에서 ambient mode가 GA 달성으로 가상머신 통합이 더욱 안정화
	- WorkloadGroup 및 WorkloadEntry를 통한 자동 등록 지원
	- 워크로드 제거 시 WorkloadEntry 자동 삭제

- 핵심 구성요소
	- **WorkloadGroup**: 가상머신 워크로드의 논리적 그룹화 (Kubernetes Deployment와 유사)
	- **WorkloadEntry**: 단일 가상머신 워크로드 인스턴스 (Kubernetes Pod와 유사)
	- **istioctl**: 가상머신을 istiod에 연결하는 설정 생성
	- **east-west 게이트웨이**: 가상머신이 연결할 수 있도록 istiod 노출

- DNS 및 네트워킹
	- **DNS 프록시**: 클러스터 내부 호스트네임 해석, istiod가 NDS API로 설정
	- **자동 호스트네임 변형 생성**: istio-agent가 쿠버네티스 경험과 일치하도록 짧은 변형 생성
	- **가상머신 사이드카**: 다른 워크로드와 동일하게 Istio 설정 준수

- 운영 고려사항
	- **자동화 필수**: 수작업 구성은 메시를 취약하게 만듦
	- **기존 도구 활용**: Packer, Ansible, Terraform 등 기존 자동화 도구에 Istio 설정 추가
	- **자동 등록과 삭제**: 클라우드 네이티브 워크로드의 일시성 지원에 모두 중요
