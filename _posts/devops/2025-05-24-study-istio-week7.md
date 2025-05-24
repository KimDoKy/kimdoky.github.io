---
layout: post
section-type: post
title: ServiceMesh - Istio - Week7
category: devops
tags: ["k8s", "istio", "servicemesh"]
---

# chap12. 조직 내에서 이스티오 스케일링하기
- 여러 클러스터에서 서비스 메시 스케일링하기
- 두 클러스터를 합치기 위한 전체 조건 해결하기
- 여러 클러스터의 워크로드 간에 공통 신뢰(common trust) 설정하기
- 클러스터 간 워크로드 찾기
- east-west 트래픽을 위한 이스티오 인그레스 게이트웨이 설정하기

## 다중 클러스터 서비스 메시의 이점
- 이점
	- 격리성 강화: 팀 간 문제 전파 방지
	- 장애 경계: 클러스터 장애 시 전체 시스템 영향 최소화
	- 규정 준수: 민감 데이터 접근 제한 기능
	- 가용성 및 성능 향상: 다중 리전 운영으로 가용성 증가 및 지연 시간 감소
	- 다중/하이브리드 클라우드 지원: 다양한 클라우드 환경에서 워크로드 실행 가능

- 다중 클러스터 접근법 요약
	- 다중 클러스터 서비스 메시
	    - 여러 클러스터에 걸친 단일 메시 구성
	    - 이스티오 설정(VirtualService, DestinationRule, Sidecar)으로 클러스터 간 트래픽 관리
	- 메시 연합(다중 메시)
	    - 개별 서비스 메시 간 통신 활성화
	    - 수동 설정 필요성 증가
	    - 다른 팀 관리 또는 높은 보안 격리 필요 시 적합

## 다중 클러스터 서비스 메시 개요
- 클러스터들을 하나의 메시로 결합을 위한 전제 조건
    - 클러스터 간 워크로드 디스커버리: 컨트롤 플레인이 서비스 프록시 설정을 위해 타 클러스터 워크로드를 식별하고 접근할 수 있어야 함
    - 클러스터 간 워크로드 연결성: 워크로드 간 실제 네트워크 연결이 가능해야 하며, 단순한 엔드포인트 인식만으로는 불충분함
    - 클러스터 간 공통 신뢰: 이스티오 보안 기능 활용을 위해 클러스터 간 워크로드 상호 인증 메커니즘 필요

![]({{ site.url }}/img/post/devops/study/istio/7/20250521205321.png)

### 이스티오 다중 클러스터 배포 모델
- 클러스터 유형    
    - primary cluster: 이스티오 컨트롤 플레인이 설치된 클러스터
    - remote cluster: 컨트롤 플레인과 분리된 클러스터
- 가용성 수준에 따른 배포 모델
    - primary-remote 모델
        - 단일 컨트롤 플레인 관리 방식
        - 리소스 사용 효율성 높음
        - 기본 클러스터 장애 시 메시 전체 영향
        - 가용성 상대적으로 낮음
        - ![]({{ site.url }}/img/post/devops/study/istio/7/20250521205538.png)

    - primary-primary 모델
        - 복수의 컨트롤 플레인 사용
        - 더 많은 리소스 소비
        - 장애 영향 범위가 해당 클러스터로 제한됨
        - 가용성 향상
        - '복제된 컨트롤 플레인 배포 모델'로 불림
        - ![]({{ site.url }}/img/post/devops/study/istio/7/20250521205719.png)

    - external control plane 모델
        - 모든 클러스터가 외부 컨트롤 플레인과 연결
        - 클라우드 프로바이더의 관리형 서비스 제공 가능
        - ![]({{ site.url }}/img/post/devops/study/istio/7/20250521205853.png)

### 다중 클러스터 배포에서 워크로드는 어떻게 찾는가?
- 쿠버네티스 API 접근 보안
	- 이스티오 컨트롤 플레인은 서비스 프록시 설정을 위해 쿠버네티스 API 서버와 통신 필요
	- API 서버 접근은 강력한 권한으로, 민감 정보 조회 및 클러스터 상태 변경 가능성 내포
	- 쿠버네티스는 RBAC(Role-Based Access Control)을 통해 API 서버 접근 보호
- 클러스터 간 디스커버리에 사용되는 핵심 개념:
    - Service Account: 기계나 서비스에 ID 제공
    - Service Account Token: 자동 생성되어 ID 클레임 표현, JWT 형식으로 파드에 주입
    - Role and ClusterRole: ID에 대한 권한 집합 정의
- 토큰과 RBAC으로 원격 API 접근 보안이 가능하나 트레이드오프 존재
- 메시 연합이 이러한 위험성 완화에 도움 가능

![]({{ site.url }}/img/post/devops/study/istio/7/20250521211012.png)

- 클러스터 간 워크로드 디스커버리
	- 클러스터 간 워크로드 디스커버리는 기술적으로 동일한 방식으로 작동
	- istiod에 원격 클러스터의 서비스 어카운트 토큰 제공 필요
	- API 서버와의 보안 통신을 위한 인증서도 함께 제공
	- istiod는 이 토큰을 사용하여 원격 클러스터에 인증 후 워크로드 탐색 수행

![]({{ site.url }}/img/post/devops/study/istio/7/20250521211743.png)

### 클러스터 간 워크로드 연결
- 다중 클러스터 환경에서는 워크로드가 클러스터 간 연결 가능해야 함
- 플랫 네트워크(단일 네트워크 공유 또는 네트워크 피어링) 환경에서는 IP 주소로 직접 연결 가능하여 조건 자동 충족
- 서로 다른 네트워크에 클러스터가 있는 경우:
    - 네트워크 에지에 위치한 특수 이스티오 인그레스 게이트웨이 필요
    - 이 게이트웨이가 클러스터 간 트래픽 프록시 역할 수행
    - 다중 네트워크 메시에서는 이런 게이트웨이를 "east-west 게이트웨이"라고 부름

![]({{ site.url }}/img/post/devops/study/istio/7/20250521212603.png)

### 클러스터 간 공통 신뢰
#### 플러그인 CA 인증서
- 플러그인 중간 CA 인증서 방식은 구현이 간단함
- 이스티오가 자동 생성하는 대신 사용자가 인증서를 지정하여 시크릿으로 제공
- 두 클러스터 모두 동일한 루트 CA가 서명한 중간 CA 사용
- 장점: 간단한 구현 방식
- 단점: 중간 CA 노출 시 보안 위험 존재
    - 노출 시 공격자가 취소 전까지 신뢰받는 인증서 서명 가능
    - 이러한 위험으로 인해 조직들이 중간 CA 사용을 꺼리는 경향
- 위험 완화 방법:
    - 중간 CA를 메모리에만 로드하고 etcd에 시크릿으로 저장하지 않음
    - 더 안전한 대안으로 외부 CA 통합 방식 사용 가능

![]({{ site.url }}/img/post/devops/study/istio/7/20250521213639.png)

#### 외부 인증 기간 통합
- istiod가 인증서 서명 요청(CSRs)을 검증하고 승인하는 등록 기관 역할 수행
- 승인된 쿠버네티스 CSR은 다음 두 가지 방법으로 외부 CA에 제출:    
    1. cert-manager 사용
        - 외부 CA가 cert-manager에서 지원될 경우에만 가능
        - cert-manager의 istio-csr이 쿠버네티스 CSR을 모니터링하고 외부 CA에 서명 요청
    2. 맞춤 개발
        - 승인된 쿠버네티스 CSR을 모니터링하여 외부 CA에 제출하는 쿠버네티스 컨트롤러 개발
        - 자체 서명 대신 외부 CA 사용하도록 솔루션 조정 필요
- 외부 CA가 서명한 인증서는 쿠버네티스 CSR에 저장되며, istiod가 SDS(Secret Discovery Service)를 통해 워크로드에 전달

## 다중 클러스터, 다중 네트워크, 다중 컨트롤 플레인 서비스 메시 개요
### 다중 클러스터 배포 모델 선택하기
- 다중 네트워크 인프라에서는 클러스터 간 연결을 위한 east-west 게이트웨이 필수
- 컨트롤 플레인 배포 모델은 비즈니스 요구사항에 따라 결정:
    - 복제된 컨트롤 플레인 모델 vs 단일 컨트롤 플레인 모델
- ACME 사례 분석:
    - 온라인 상점의 서비스 중단 시 매분 수백만 달러 손실 발생
    - 고가용성이 최우선 과제
- 최종 선택된 배포 모델:
    - 다중 클러스터, 다중 네트워크, 다중 컨트롤 플레인 서비스 메시
    - 네트워크 연결을 위한 east-west 게이트웨이 사용
    - 각 클러스터에 이스티오 컨트롤 플레인이 배포되는 기본-기본(primary-primary) 배포 모델 채택

### 플러그인 CA 인증서 설정하기
- 이스티오는 설치 시 워크로드 인증서에 서명할 CA를 자동 생성
    - 생성된 CA는 'istio-ca-secret'이라는 시크릿으로 이스티오 설치 네임스페이스에 저장
    - istiod 복제본들이 이 시크릿을 공유하여 사용
- 기본 동작은 사용자 정의 CA로 대체 가능
    - 이스티오가 새 CA를 생성하는 대신 제공된 CA 사용
- 설정 방법:
    - CA 인증서를 'istio-system' 네임스페이스에 'cacerts'라는 시크릿으로 저장
    - 필요한 데이터 포함 항목:
        - ca.cert.pem: 중간 CA 인증서
        - ca-key.pem: 중간 CA 개인 키
        - root-cert.pem: 루트 CA 인증서(중간 CA 발급 기관)
        - cert-chain.pem: 중간 CA와 루트 CA를 연결한 신뢰 체인
- 인증서 구조:
    - 루트 CA: 모든 클러스터가 신뢰하는 최상위 인증서
    - 중간 CA: 각 클러스터별 발급, 워크로드 인증서 서명에 사용
    - 인증서 체인: 클라이언트의 인증서 검증을 위한 신뢰 체인 구성

#### 플러그인 CA 인증서 적용하기
인증서 확인
```bash
tree ch12/certs
ch12/certs
├── east-cluster
│   ├── ca-cert.pem
│   ├── ca-key.pem
│   └── cert-chain.pem
├── root-ca.key
├── root-cert.pem
└── west-cluster
    ├── ca-cert.pem
    ├── ca-key.pem
    └── cert-chain.pem

openssl x509 -in ch12/certs/root-cert.pem -noout -text
openssl x509 -in ch12/certs/east-cluster/ca-cert.pem -noout -text
openssl x509 -in ch12/certs/east-cluster/cert-chain.pem -noout -text
openssl x509 -in ch12/certs/west-cluster/ca-cert.pem -noout -text openssl x509 -in ch12/certs/west-cluster/cert-chain.pem -noout -text
```
![]({{ site.url }}/img/post/devops/study/istio/7/20250522215426.png)

![]({{ site.url }}/img/post/devops/study/istio/7/20250522215256.png)

- istio-system 네임스페이스를 생성후 인증서를 cacerts라는 시크릿으로 적용해 각 클러스터에 intermediate CA를 설정

```bash
# west-cluster 용 인증서 설정하기
kwest create namespace istio-system
kwest create secret generic cacerts -n istio-system \
--from-file=ch12/certs/west-cluster/ca-cert.pem \
--from-file=ch12/certs/west-cluster/ca-key.pem \
--from-file=ch12/certs/root-cert.pem \
--from-file=ch12/certs/west-cluster/cert-chain.pem

# east-cluster 용 인증서 설정하기
keast create namespace istio-system
keast create secret generic cacerts -n istio-system \
--from-file=ch12/certs/east-cluster/ca-cert.pem \
--from-file=ch12/certs/east-cluster/ca-key.pem \
--from-file=ch12/certs/root-cert.pem \
--from-file=ch12/certs/east-cluster/cert-chain.pem

# 확인
for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get ns istio-system --kubeconfig=./$i-kubeconfig; echo; done
for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get secret cacerts  -n istio-system --kubeconfig=./$i-kubeconfig; echo; done
for i in west east; do echo ">> k8s cluster : $i <<"; kubectl view-secret cacerts -n istio-system --all --kubeconfig=./$i-kubeconfig; echo; done
```
- 플러그인 인증서가 설정되면 이스티오 컨트롤 플레인을 설치할 수 있음
	- 컨트롤 플레인은 플러그인 CA 인증서를 갖고 워크로드 인증서에 서명함

### 각 클러스터에 컨트롤 플레인 설치하기
- **네트워크 메타데이터 추가 필요성**
    - 이스티오 컨트롤 플레인 설치 전에 각 클러스터에 네트워크 메타데이터를 추가해야 함
- **토폴로지 정보 활용**
    - 네트워크 메타데이터를 통해 이스티오가 토폴로지 정보를 사용할 수 있음
    - 해당 정보를 기반으로 워크로드 설정 가능
- **지역성 기반 트래픽 라우팅 최적화**
    - 워크로드가 지역 정보를 활용하여 가까운 워크로드를 우선적으로 선택
    - 트래픽 라우팅 시 근접성을 고려한 최적화 구현
- **East-West 게이트웨이 활용**
    - 다른 네트워크에 있는 원격 클러스터의 워크로드로 트래픽 라우팅 시
    - 이스티오가 자동으로 east-west 게이트웨이를 사용하도록 설정

#### 클러스터 간 연결을 위해 네트워크에 레이블 붙이기
- MeshNetwork vs 레이블 방식
    - MeshNetwork 설정: 드문 고급 사용 사례나 레거시 설정에서 사용
    - 레이블 방식: 더 간단한 방법으로 권장됨

- 레이블 설정 방법
    - 이스티오가 설치된 네임스페이스(istio-system)에 네트워크 토폴로지 정보를 레이블로 추가
    - 레이블 형식: `topology.istio.io/network=[네트워크명]`

- 실제 설정 예시
    - west-cluster: `topology.istio.io/network=west-network` 레이블 적용
    - east-cluster: `topology.istio.io/network=east-network` 레이블 적용

- 설정 명령어

```bash
kwest label namespace istio-system topology.istio.io/network=west-network
keast label namespace istio-system topology.istio.io/network=east-network
```

- 설정 효과
    - 이스티오가 이 레이블들을 통해 네트워크 토폴로지를 이해함
    - 토폴로지 정보를 바탕으로 워크로드 설정 방법을 결정함

#### IstioOperator 리소스를 사용해 컨트롤 플레인 설치하기
- IstioOperator 리소스 정의

```bash
# cat ./ch12/controlplanes/cluster-west.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-controlplane
  namespace: istio-system
spec:
  profile: demo
  components:
    egressGateways: # 이그레스 게이트웨이 비활성화
    - name: istio-egressgateway
      enabled: false
  values:
    global:
      meshID: usmesh # 메시 이름
      multiCluster:
        clusterName: west-cluster # 멀티 클러스터 메시 내부의 클러스터 식별자
      network: west-network # 이 설치가 이뤄지는 네트워크

# cat ./ch12/controlplanes/cluster-east.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-controlplane
  namespace: istio-system
spec:
  profile: demo
  components:
    egressGateways: # 이그레스 게이트웨이 비활성화
    - name: istio-egressgateway
      enabled: false
  values:
    global:
      meshID: usmesh # 메시 이름
      multiCluster:
        clusterName: east-cluster
      network: east-network
```
• **west-cluster 설치 과정**

```bash
# west-control-plane 진입 후 설치 진행
docker exec -it west-control-plane bash
-----------------------------------
# istioctl 설치
export ISTIOV=1.17.8
echo 'export ISTIOV=1.17.8' >> /root/.bashrc

curl -s -L https://istio.io/downloadIstio | ISTIO_VERSION=$ISTIOV sh -
cp istio-$ISTIOV/bin/istioctl /usr/local/bin/istioctl

# IstioOperator 파일 작성
cat << EOF > west-istio.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-controlplane
  namespace: istio-system
spec:
  profile: demo
  components:
    egressGateways:
    - name: istio-egressgateway
      enabled: false
  values:
    global:
      meshID: usmesh
      multiCluster:
        clusterName: west-cluster
      network: west-network
EOF

# 컨트롤 플레인 배포
istioctl install -f west-istio.yaml --set values.global.proxy.privileged=true -y

# 보조 도구 설치
kubectl apply -f istio-$ISTIOV/samples/addons

# 빠져나오기
exit
-----------------------------------

# 설치 확인 : istiod, istio-ingressgateway, crd 등
kwest get istiooperators -n istio-system -o yaml
...
        meshID: usmesh
        meshNetworks: {}
        mountMtlsCerts: false
        multiCluster:
          clusterName: west-cluster
          enabled: false
        network: west-network
...

kwest get all,svc,ep,sa,cm,secret,pdb -n istio-system
kwest get secret -n istio-system cacerts -o json # 미리 만들어둔 인증서/키 확인

# istio-ingressgateway 서비스 : NodePort 변경 및 nodeport 지정 변경 , externalTrafficPolicy 설정 (ClientIP 수집)
kwest patch svc -n istio-system istio-ingressgateway -p '{"spec": {"type": "LoadBalancer", "ports": [{"port": 80, "targetPort": 8080, "nodePort": 30000}]}}'
kwest patch svc -n istio-system istio-ingressgateway -p '{"spec":{"externalTrafficPolicy": "Local"}}'
kwest describe svc -n istio-system istio-ingressgateway

# NodePort 변경 및 nodeport 30001~30003으로 변경 : prometheus(30001), grafana(30002), kiali(30003), tracing(30004)
kwest patch svc -n istio-system prometheus -p '{"spec": {"type": "NodePort", "ports": [{"port": 9090, "targetPort": 9090, "nodePort": 30001}]}}'
kwest patch svc -n istio-system grafana -p '{"spec": {"type": "NodePort", "ports": [{"port": 3000, "targetPort": 3000, "nodePort": 30002}]}}'
kwest patch svc -n istio-system kiali -p '{"spec": {"type": "NodePort", "ports": [{"port": 20001, "targetPort": 20001, "nodePort": 30003}]}}'
kwest patch svc -n istio-system tracing -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 16686, "nodePort": 30004}]}}'

# Prometheus 접속 : envoy, istio 메트릭 확인
open http://127.0.0.1:30001

# Grafana 접속
open http://127.0.0.1:30002

# Kiali 접속 : NodePort
open http://127.0.0.1:30003

# tracing 접속 : 예거 트레이싱 대시보드
open http://127.0.0.1:30004

```

• **east-cluster 설치 과정**

```bash
# west-control-plane 진입 후 설치 진행
docker exec -it east-control-plane bash
-----------------------------------
# istioctl 설치
export ISTIOV=1.17.8
echo 'export ISTIOV=1.17.8' >> /root/.bashrc

curl -s -L https://istio.io/downloadIstio | ISTIO_VERSION=$ISTIOV sh -
cp istio-$ISTIOV/bin/istioctl /usr/local/bin/istioctl

# IstioOperator 파일 작성
cat << EOF > east-istio.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-controlplane
  namespace: istio-system
spec:
  profile: demo
  components:
    egressGateways:
    - name: istio-egressgateway
      enabled: false
  values:
    global:
      meshID: usmesh
      multiCluster:
        clusterName: east-cluster
      network: east-network
EOF

# 컨트롤 플레인 배포
istioctl install -f east-istio.yaml --set values.global.proxy.privileged=true -y

# 보조 도구 설치
kubectl apply -f istio-$ISTIOV/samples/addons

# 빠져나오기
exit
-----------------------------------

# 설치 확인 : istiod, istio-ingressgateway, crd 등
keast get istiooperators -n istio-system -o yaml
...
        meshID: usmesh
        meshNetworks: {}
        mountMtlsCerts: false
        multiCluster:
          clusterName: east-cluster
          enabled: false
        network: east-network
...

keast get all,svc,ep,sa,cm,secret,pdb -n istio-system
keast get secret -n istio-system cacerts -o json # 미리 만들어둔 인증서/키 확인


# NodePort 변경 및 nodeport 31001~31003으로 변경 : prometheus(31001), grafana(31002), kiali(31003), tracing(31004)
keast patch svc -n istio-system prometheus -p '{"spec": {"type": "NodePort", "ports": [{"port": 9090, "targetPort": 9090, "nodePort": 31001}]}}'
keast patch svc -n istio-system grafana -p '{"spec": {"type": "NodePort", "ports": [{"port": 3000, "targetPort": 3000, "nodePort": 31002}]}}'
keast patch svc -n istio-system kiali -p '{"spec": {"type": "NodePort", "ports": [{"port": 20001, "targetPort": 20001, "nodePort": 31003}]}}'
keast patch svc -n istio-system tracing -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 16686, "nodePort": 31004}]}}'

# Prometheus 접속 : envoy, istio 메트릭 확인
open http://127.0.0.1:31001

# Grafana 접속
open http://127.0.0.1:31002

# Kiali 접속
open http://127.0.0.1:31003

# tracing 접속 : 예거 트레이싱 대시보드
open http://127.0.0.1:31004
```

• **istioctl alias 설정**

```bash
alias iwest='docker exec -it west-control-plane istioctl'
alias ieast='docker exec -it east-control-plane istioctl'

iwest proxy-status
NAME                                                   CLUSTER          CDS        LDS        EDS        RDS          ECDS         ISTIOD                      VERSION
istio-ingressgateway-5db74c978c-wlm9q.istio-system     west-cluster     SYNCED     SYNCED     SYNCED     NOT SENT     NOT SENT     istiod-5585445f4c-b66zb     1.17.8

ieast proxy-status
NAME                                                   CLUSTER          CDS        LDS        EDS        RDS          ECDS         ISTIOD                     VERSION
istio-ingressgateway-7f6f8f8d99-vb7c8.istio-system     east-cluster     SYNCED     SYNCED     SYNCED     NOT SENT     NOT SENT     istiod-85976468f-5bsrk     1.17.8

iwest proxy-config secret deploy/istio-ingressgateway.istio-system
RESOURCE NAME     TYPE           STATUS     VALID CERT     SERIAL NUMBER                               NOT AFTER                NOT BEFORE
default           Cert Chain     ACTIVE     true           80349990876331570640723939723244297816      2025-05-17T08:47:28Z     2025-05-16T08:45:28Z
ROOTCA            CA             ACTIVE     true           100900981840825465297757884708490534092     2032-06-25T14:11:35Z     2022-06-28T14:11:35Z

# 인증서 확인
# - 미리 준비된 인증서가 적용되었는지 확인
# - 사용자 인증서, 중간 CA 인증서, 최상위 루트 인증서 체인 확인
iwest proxy-config secret deploy/istio-ingressgateway.istio-system -o json
...

# 아래는 default 에 inlineBytes 값을 decode64 -d 시 3개의 인증서 정보 출력 후 각 개별 인증서를 openssl x509 -in Y.pem -noout -text 로 출력 확인 
## (1) 사용자 인증서
-----BEGIN CERTIFICATE-----
MIIDdjCCAl6gAwIBAgIQPHLYaJhiIjAwJkg6cAVeWDANBgkqhkiG9w0BAQsFADAs
...
5xYNi7u0APTzE1swNbx2TF5eeTsFvYcbFh56ahLp0izGkahOv97bEgnZdeTsLRyH
K+5+1ZdJ2n8CuxoSY+FXUlMDwGjdvCXAKBM=
-----END CERTIFICATE-----

        Issuer: CN=west.intermediate.istio.in.action
        Validity
            Not Before: May 16 08:45:28 2025 GMT
            Not After : May 17 08:47:28 2025 GMT
        Subject: 
        ...
        X509v3 extensions:
            X509v3 Key Usage: critical
                Digital Signature, Key Encipherment
            X509v3 Extended Key Usage: 
                TLS Web Server Authentication, TLS Web Client Authentication
            X509v3 Basic Constraints: critical
                CA:FALSE
            X509v3 Authority Key Identifier: 
                D3:83:9A:3A:51:D9:03:62:35:8F:6A:A4:DA:99:88:BB:74:70:4F:33
            X509v3 Subject Alternative Name: critical
                URI:spiffe://cluster.local/ns/istio-system/sa/istio-ingressgateway-service-account


## (2) 중간 CA 루트 인증서
-----BEGIN CERTIFICATE-----
MIIDPDCCAiSgAwIBAgIRAMkJ23sotpqiiWps+38Df/YwDQYJKoZIhvcNAQELBQAw
...
usSjiM6KR77xogslodbQw4QQG+w5HQOwMa1k8WTCNrplxdsnaQJjdqUwCdixicq2
DeHuSkz4cykAI/NWc2cZIw==
-----END CERTIFICATE-----

        Issuer: CN=root.istio.in.action
        Validity
            Not Before: Jun 28 14:11:35 2022 GMT
            Not After : Jun 25 14:11:35 2032 GMT
        Subject: CN=west.intermediate.istio.in.action
        ...
        X509v3 extensions:
            X509v3 Key Usage: critical
                Certificate Sign, CRL Sign
            X509v3 Basic Constraints: critical
                CA:TRUE, pathlen:0

## (3) 최상위 루트 인증서
-----BEGIN CERTIFICATE-----
MIIDDTCCAfWgAwIBAgIQS+jSffZX7itohjyrautczDANBgkqhkiG9w0BAQsFADAf
...
3fRtDApNHbbmi7WXrM+pG4D+Buk2FUEHJVpu16Ch2K2vpRzpkliqes+T/5E92uY9
ob7MBgt61g4VZ/p8+RMJWYw=
-----END CERTIFICATE-----

        Issuer: CN=root.istio.in.action
        Validity
            Not Before: Jun 28 14:11:35 2022 GMT
            Not After : Jun 25 14:11:35 2032 GMT
        Subject: CN=root.istio.in.action
        ...
        X509v3 extensions:
            X509v3 Key Usage: critical
                Certificate Sign, CRL Sign
            X509v3 Basic Constraints: critical
                CA:TRUE, pathlen:1

#
iwest proxy-config listener deploy/istio-ingressgateway.istio-system
iwest proxy-config route deploy/istio-ingressgateway.istio-system
iwest proxy-config cluster deploy/istio-ingressgateway.istio-system
iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system
iwest proxy-config secret deploy/istio-ingressgateway.istio-system
iwest proxy-config bootstrap deploy/istio-ingressgateway.istio-system
iwest proxy-config ecds deploy/istio-ingressgateway.istio-system

#
ieast proxy-config listener deploy/istio-ingressgateway.istio-system
ieast proxy-config route deploy/istio-ingressgateway.istio-system
ieast proxy-config cluster deploy/istio-ingressgateway.istio-system
ieast proxy-config endpoint deploy/istio-ingressgateway.istio-system
ieast proxy-config secret deploy/istio-ingressgateway.istio-system
ieast proxy-config bootstrap deploy/istio-ingressgateway.istio-system
ieast proxy-config ecds deploy/istio-ingressgateway.istio-system
```
![]({{ site.url }}/img/post/devops/study/istio/7/20250522223532.png)

#### 두 클러스터 모두에 워크로드 실행하기
```bash
#
kwest create ns istioinaction
kwest label namespace istioinaction istio-injection=enabled
kwest -n istioinaction apply -f ch12/webapp-deployment-svc.yaml
kwest -n istioinaction apply -f ch12/webapp-gw-vs.yaml
kwest -n istioinaction apply -f ch12/catalog-svc.yaml # Stub catalog service to which webapp makes request
cat ch12/catalog-svc.yaml
piVersion: v1
kind: Service
metadata:
  labels:
    app: catalog
  name: catalog
spec:
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 3000
  selector:
    app: catalog


# 확인
kwest get deploy,pod,svc,ep -n istioinaction
kwest get svc,ep catalog -n istioinaction
NAME              TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
service/catalog   ClusterIP   10.100.2.43   <none>        80/TCP    2m

NAME                ENDPOINTS   AGE
endpoints/catalog   <none>      2m

kwest get gw,vs,dr -A
NAMESPACE       NAME                                            AGE
istioinaction   gateway.networking.istio.io/coolstore-gateway   16s

NAMESPACE       NAME                                                       GATEWAYS                HOSTS                         AGE
istioinaction   virtualservice.networking.istio.io/webapp-virtualservice   ["coolstore-gateway"]   ["webapp.istioinaction.io"]   16s

#
iwest proxy-status
NAME                                                   CLUSTER          CDS        LDS        EDS        RDS        ECDS         ISTIOD                      VERSION
istio-ingressgateway-5db74c978c-wlm9q.istio-system     west-cluster     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-5585445f4c-b66zb     1.17.8
webapp-5c8b4fff64-t2rh8.istioinaction                  west-cluster     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-5585445f4c-b66zb     1.17.8

# endpoint 에 IP 는 10.10.0.0/16 대역들 다수 확인
for i in listener route cluster endpoint; do echo ">> k8s cluster : west - istio-config $i <<"; docker exec -it west-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done
iwest proxy-config cluster deploy/istio-ingressgateway.istio-system | grep catalog
catalog.istioinaction.svc.cluster.local                      80        -          outbound      EDS 

iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system | grep catalog
```



```bash
#
keast create ns istioinaction
keast label namespace istioinaction istio-injection=enabled
keast -n istioinaction apply -f ch12/catalog.yaml
cat ch12/catalog.yaml


# 확인
keast get deploy,pod,svc,ep -n istioinaction
keast get svc,ep catalog -n istioinaction
keast get gw,vs,dr -A # 없음

#
ieast proxy-status
NAME                                                   CLUSTER          CDS        LDS        EDS        RDS          ECDS         ISTIOD                     VERSION
catalog-6cf4b97d-2qzhj.istioinaction                   east-cluster     SYNCED     SYNCED     SYNCED     SYNCED       NOT SENT     istiod-85976468f-5bsrk     1.17.8
istio-ingressgateway-7f6f8f8d99-vb7c8.istio-system     east-cluster     SYNCED     SYNCED     SYNCED     NOT SENT     NOT SENT     istiod-85976468f-5bsrk     1.17.8

# endpoint 에 IP 는 10.20.0.0/16 대역들 다수 확인
for i in listener route cluster endpoint; do echo ">> k8s cluster : east - istio-config $i <<"; docker exec -it east-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done
ieast proxy-config cluster deploy/istio-ingressgateway.istio-system | grep catalog
catalog.istioinaction.svc.cluster.local                      80        -          outbound      EDS

ieast proxy-config endpoint deploy/istio-ingressgateway.istio-system | grep catalog
10.20.0.15:3000                                         HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local
```

- 스텁 catalog 서비스가 필요한 이유
    - webapp 컨테이너가 FQDN을 IP 주소로 해석할 수 없으면 요청이 실패함
    - 트래픽이 애플리케이션을 떠나 프록시로 리다이렉트되기 전에 요청이 중단됨

- 스텁 서비스의 역할
    - FQDN을 서비스 클러스터 IP로 해석 가능하게 함
    - 애플리케이션이 트래픽을 시작할 수 있도록 지원
    - 엔보이 프록시로 리다이렉트되어 실제 엔보이 설정이 클러스터 간 라우팅을 처리

- 현재 상황의 한계
    - 이는 DNS 프록시의 에지 케이스로 인한 문제
    - 이스티오 커뮤니티가 향후 버전에서 DNS 프록시 개선을 통해 해결 예정

- 현재 상태와 다음 단계
    - 각 클러스터에 연결해야 하는 워크로드가 존재
    - 클러스터 간 워크로드 디스커버리가 없으면 사이드카 프록시에 반대 클러스터의 워크로드가 설정되지 않음
    - 다음 단계: 클러스터 간 디스커버리 활성화 필요

### 클러스터 간 워크로드 디스커버리 활성화하기

- 원격 클러스터 인증 요구사항
    - 이스티오가 원격 클러스터에서 정보를 쿼리하려면 인증이 필요
    - ID를 정의하는 서비스 어카운트와 권한에 대한 롤 바인딩이 필수

- istio-reader-service-account
    - 이스티오 설치 시 자동으로 생성되는 서비스 어카운트
    - 최소 권한으로 설정됨
    - 다른 컨트롤 플레인이 자신을 인증하는 데 사용
    - 서비스나 엔드포인트 같은 워크로드 관련 정보 조회에 활용

- 보안 연결을 위한 추가 요구사항
    - 서비스 어카운트 토큰이 필요
    - 원격 클러스터로 보안 커넥션을 시작할 인증서가 필요
    - 상대 클러스터가 이들을 사용할 수 있도록 설정해야 함

#### 원격 클러스터 접근용 시크릿 만들기
- create-remote-secret 명령어
    - istioctl에서 제공하는 원격 클러스터 접근용 시크릿 생성 명령어
    - 기본 istio-reader-service-account 서비스 어카운트를 사용
    - 시크릿 생성 시 IstioOperator에서 사용한 클러스터 이름을 지정하는 것이 중요 (east-cluster, west-cluster)

```bash
#
for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get sa -n istio-system --kubeconfig=./$i-kubeconfig; echo; done

# east
keast describe sa -n istio-system istio-reader-service-account      
keast get sa -n istio-system istio-reader-service-account -o yaml
keast get sa -n istio-system istio-reader-service-account -o jsonpath='{.secrets[0].name}'
eirsa=$(keast get sa -n istio-system istio-reader-service-account -o jsonpath='{.secrets[0].name}')
keast get secret -n istio-system $eirsa
keast get secret -n istio-system $eirsa -o json

kubectl rolesum istio-reader-service-account -n istio-system --kubeconfig=./east-kubeconfig

keast auth can-i --list
keast auth can-i --as=system:serviceaccount:istio-system:istio-reader-service-account --list

ieast x create-remote-secret --name="east-cluster"
# This file is autogenerated, do not edit.
apiVersion: v1
kind: Secret
metadata:
  annotations:
    networking.istio.io/cluster: east-cluster
  creationTimestamp: null
  labels:
    istio/multiCluster: "true" # 이 레이블이 true로 설정된 시크릿은 이스티오의 컨트롤 플레인이 새 클러스터를 등록하기 위해 감시한다
  name: istio-remote-secret-east-cluster
  namespace: istio-system
stringData:
  east-cluster: |
    apiVersion: v1
    clusters:
    - cluster: # 아래 'certificate-authority-data'는 이 클러스터에 보안 커넥션을 시작하는 데 사용하는 CA
        certificate-authority-data: LS0tLS1CR....
        server: https://east-control-plane:6443
      name: east-cluster
    contexts:
    - context:
        cluster: east-cluster
        user: east-cluster
      name: east-cluster
    current-context: east-cluster
    kind: Config
    preferences: {}
    users:
    - name: east-cluster
      user: # 아래 'token'은 서비스 어카운트의 ID를 나타내는 토큰
        token: eyJhb...

## certificate-authority-data 정보 : k8s 루트 인증서
openssl x509 -in YYY -noout -text

## user.token 정보 : 
jwt decode YYY
---------------------------------------------------------------
# west 에 시크릿 생성
ieast x create-remote-secret --name="east-cluster" | kwest apply -f -

# istiod 로그 확인 : 시크릿이 생성되면, 바로 istiod가 이 시크릿을 가지고 새로 추가된 원격 클러스터(east)에 워크로드를 쿼리한다.
kwest logs deploy/istiod -n istio-system | grep 'Adding cluster'

for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get secret -n istio-system --kubeconfig=./$i-kubeconfig; echo; done
kwest get secret -n istio-system istio-remote-secret-east-cluster
kwest get secret -n istio-system istio-remote-secret-east-cluster -o yaml

# west 확인 : east 의 모든 CDS/EDS 정보를 west 에서도 확인 가능!
for i in listener route cluster endpoint; do echo ">> k8s cluster : west - istio-config $i <<"; docker exec -it west-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done
iwest proxy-config cluster deploy/istio-ingressgateway.istio-system | grep catalog
iwest proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local -o json
iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system | grep catalog

# west 에서 10.20.0.15(10.20.0.0/16)로 라우팅이 가능한 상태인가?
iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||catalog.istioinaction.svc.cluster.local' -o json

# east 확인 : west 의 CDS/EDS 정보를 아직 모름!
for i in listener route cluster endpoint; do echo ">> k8s cluster : east - istio-config $i <<"; docker exec -it east-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done
ieast proxy-config cluster deploy/istio-ingressgateway.istio-system | grep catalog
ieast proxy-config endpoint deploy/istio-ingressgateway.istio-system | grep catalog
---------------------------------------------------------------
# east 에 시크릿 생성
iwest x create-remote-secret --name="west-cluster" | keast apply -f -

# istiod 로그 확인 : 시크릿이 생성되면, 바로 istiod가 이 시크릿을 가지고 새로 추가된 원격 클러스터(east)에 워크로드를 쿼리한다.
keast logs deploy/istiod -n istio-system | grep 'Adding cluster'

for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get secret -n istio-system --kubeconfig=./$i-kubeconfig; echo; done
keast get secret -n istio-system istio-remote-secret-west-cluster
keast get secret -n istio-system istio-remote-secret-west-cluster -o yaml

# east 확인 : west 의 모든 CDS/EDS 정보를 east 에서도 확인 가능!
for i in listener route cluster endpoint; do echo ">> k8s cluster : east - istio-config $i <<"; docker exec -it east-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done
ieast proxy-config cluster deploy/istio-ingressgateway.istio-system | grep webapp

# east 에서 10.10.0.15(10.10.0.0/16)로 라우팅이 가능한 상태인가?
ieast proxy-config endpoint deploy/istio-ingressgateway.istio-system | grep webapp
---------------------------------------------------------------
# catalog stub service 정보 확인 : endpoints 는 아직도 none.
kwest get svc,ep -n istioinaction
NAME              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/catalog   ClusterIP   10.100.2.43    <none>        80/TCP    14h
service/webapp    ClusterIP   10.100.2.172   <none>        80/TCP    14h

NAME                ENDPOINTS        AGE
endpoints/catalog   <none>           14h
endpoints/webapp    10.10.0.8:8080   14h

# webapp stub service 생성하지 않았으므로 별도 west 의 webapp service 정보가 없다
keast get svc,ep -n istioinaction
NAME              TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/catalog   ClusterIP   10.200.3.0   <none>        80/TCP    14h

NAME                ENDPOINTS        AGE
endpoints/catalog   10.20.0.8:3000   14h
```
### 클러스터 간 연결 설정하기
- **트래픽 유형 구분**
    - North-South 트래픽: 퍼블릭 네트워크에서 내부 네트워크로 진입하는 트래픽
    - East-West 트래픽: 서로 다른 내부 네트워크(클러스터) 간의 트래픽

![]({{ site.url }}/img/post/devops/study/istio/7/20250523000454.png)

- **네트워크 피어링의 한계**
    - 클라우드 프로바이더는 가상 네트워크 피어링으로 East-West 트래픽을 단순화
    - 네트워크 피어링은 클라우드 전용 기능으로 온프레미스나 다른 클라우드 간 연결 불가
    - 이때 이스티오의 East-West 게이트웨이가 대안 제공

#### 이스티오의 east-west 게이트웨이
- **East-West 게이트웨이의 목적**
    - 클러스터 간 East-West 트래픽의 진입점 역할
    - 서비스 운영 팀에게 투명한 프로세스 제공
    - 추가 이스티오 리소스 구성 없이 동작
- **East-West 게이트웨이의 요구사항**
    - 클러스터 사이의 정밀한 트래픽 관리 가능
    - 암호화된 트래픽 라우팅으로 워크로드 간 상호 인증 지원
    - 클러스터 내 라우팅과 클러스터 간 라우팅의 차이 최소화

#### SNI 클러스터로 east-west 게이트웨이 설정하기
- **SNI 클러스터의 개념**
    - East-West 게이트웨이는 SNI 클러스터를 모든 서비스에 추가 설정한 인그레스 게이트웨이
    - 일반 엔보이 클러스터와 유사하지만 모든 정보를 SNI에 인코딩하는 것이 핵심 차이점
    - 방향, 부분집합, 포트, FQDN 속성을 포함
- **SNI 클러스터의 동작 방식**
    - 클라이언트가 원격 클러스터의 워크로드로 연결 시 겨냥하는 클러스터를 SNI에 인코딩
    - SNI에 라우팅 결정을 위한 방향, 포트, 버전, 서비스 이름 포함
    - 게이트웨이가 SNI 헤더에서 클러스터 정보를 읽어 의도한 워크로드로 트래픽 프록시
    - 안전하고 상호 인증된 커넥션을 워크로드 간에 유지

![]({{ site.url }}/img/post/devops/study/istio/7/20250523214327.png)

#### SNI 클러스터가 있는 east-west 게이트웨이 설치하기
- SNI 클러스터 활성화 방법
    - 옵트인 기능으로 기본적으로 비활성화되어 있음
    - 환경 변수 `ISTIO_META_ROUTER_MODE`를 `sni-dnat`으로 설정하여 활성화
    - IstioOperator 정의에서 게이트웨이 라우터 모드 설정을 통해 구성
- IstioOperator 리소스 이름 주의사항
    - 컨트롤 플레인 설치에 사용한 IstioOperator 리소스와 같은 이름 사용 금지
    - 같은 이름 사용 시 기존 설치를 덮어쓰게 됨
- `ISTIO_META_ROUTER_MODE` 설정
    - `sni-dnat` 설정 시: SNI 클러스터를 자동으로 구성
    - 미설정 또는 다른 값 설정 시: `standard` 모드로 동작하며 SNI 클러스터 미설정
- `ISTIO_META_REQUESTED_NETWORK_VIEW`
    - 네트워크 트래픽이 프록시되는 위치를 정의하는 설정

```yaml
# cat ch12/gateways/cluster-east-eastwest-gateway.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: istio-eastwestgateway # IstioOperator 이름은 앞 선 이스티오 설정 이름과 겹치지 않아야 한다
  namespace: istio-system
spec:
  profile: empty # empty 프로필은 추가 이스티오 구성 요소를 설치하지 않는다
  components:
    ingressGateways:
    - name: istio-eastwestgateway # 게이트웨이 이름
      label:
        istio: eastwestgateway
        app: istio-eastwestgateway
        topology.istio.io/network: east-network
      enabled: true
      k8s:
        env:
        - name: ISTIO_META_ROUTER_MODE # sni-dnat 모드는 트래픽을 프록시하는 데 필요한 SNI 클러스터를 추가한다
          value: "sni-dnat"
        # The network to which traffic is routed
        - name: ISTIO_META_REQUESTED_NETWORK_VIEW # 게이트웨이가 트래픽을 라우팅하는 네트워크
          value: east-network
        service:
          ports:
          ... (생략) ...
  values:
    global:
      meshID: usmesh # 메시, 클러스터, 네트워크 식별 정보
      multiCluster:
        clusterName: east-cluster
      network: east-network
```

```bash
# 설치 전 확인
for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get pod -n istio-system -l istio.io/rev=default --kubeconfig=./$i-kubeconfig; echo; done
for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get IstioOperator -n istio-system --kubeconfig=./$i-kubeconfig; echo; done
kwest get IstioOperator -n istio-system installed-state-istio-controlplane -o yaml
keast get IstioOperator -n istio-system installed-state-istio-controlplane -o yaml

# 설치 전 확인 : west 에서 catalog endpoint 에 IP 확인
for i in listener route cluster endpoint; do echo ">> k8s cluster : west - istio-config $i <<"; docker exec -it west-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done
iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system | grep catalog

# IstioOperator 로 east 클러스터에 east-west 게이트웨이를 설치
cat ch12/gateways/cluster-east-eastwest-gateway.yaml
docker cp ./ch12/gateways/cluster-east-eastwest-gateway.yaml east-control-plane:/cluster-east-eastwest-gateway.yaml
ieast install -f /cluster-east-eastwest-gateway.yaml --set values.global.proxy.privileged=true -y

# east 클러스터에 east-west 게이트웨이를 설치 확인
for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get IstioOperator -n istio-system --kubeconfig=./$i-kubeconfig; echo; done
for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get pod -n istio-system -l istio.io/rev=default --kubeconfig=./$i-kubeconfig; echo; done

keast get IstioOperator -n istio-system installed-state-istio-eastwestgateway -o yaml

# east 정보 확인
ieast proxy-status

# east 에 istio-ingressgateway  에 istio-config 정보 확인 : west 의 CDS/EDS 모두 알고 있음!
for i in listener route cluster endpoint; do echo ">> east k8s cluster : ingressgateway - istio-config $i <<"; docker exec -it east-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done

# east 에 istio-eastwestgateway 에 istio-config 정보 확인 : webapp(CDS) OK, west 에 EDS 아직 모름!
for i in listener route cluster endpoint; do echo ">> east k8s cluster : eastwestgateway - istio-config $i <<"; docker exec -it east-control-plane istioctl proxy-config $i deploy/istio-eastwestgateway.istio-system; echo; done

ieast proxy-config cluster deploy/istio-eastwestgateway.istio-system | grep istioinaction

ieast proxy-config cluster deploy/istio-eastwestgateway.istio-system --fqdn webapp.istioinaction.svc.cluster.local -o json
ieast proxy-config cluster deploy/istio-eastwestgateway.istio-system --fqdn webapp.istioinaction.svc.cluster.local -o json | grep sni

ieast proxy-config endpoint deploy/istio-eastwestgateway.istio-system | grep istioinaction
ieast proxy-config endpoint deploy/istio-eastwestgateway.istio-system --cluster 'outbound|80||catalog.istioinaction.svc.cluster.local' -o json

# west 정보 확인
iwest proxy-status

# west 에 istio-ingressgateway 에 istio-config 정보 확인
for i in listener route cluster endpoint; do echo ">> west k8s cluster : ingressgateway - istio-config $i <<"; docker exec -it west-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done
iwest proxy-config cluster deploy/istio-ingressgateway.istio-system | grep istioinaction
iwest proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local -o json
iwest proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local -o json | grep sni

# west 에 istio-ingressgateway : east EDS 모든 정보에서 east의 eastwestgateway에 mtls 정보로 변경!
iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system | grep istioinaction

# 출력되는 172.18.X.Y에 IP 확인 : east 에 eastwestgateway 의 Service(LoadBalancer)의 External-IP.
keast get svc,ep -n istio-system istio-eastwestgateway

# west 에 webapp 에 istio-config 정보 확인
for i in listener route cluster endpoint; do echo ">> west k8s cluster : webapp - istio-config $i <<"; docker exec -it west-control-plane istioctl proxy-config $i deploy/webapp.istioinaction; echo; done
iwest proxy-config endpoint deploy/webapp.istioinaction | grep istioinaction

# west 에서 호출 시도
kwest get svc,ep -n istioinaction

kwest exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl catalog.istioinaction.svc.cluster.local -v
```
- **다음 설정 단계**
    - East-west 게이트웨이 설치 및 라우터 모드를 sni-dnat으로 설정 완료 후 진행
    - SNI 자동 통과 모드(SNI auto passthrough mode)를 사용하여 설정
    - East-west 게이트웨이를 통해 다중 클러스터 상호 TLS 포트를 노출
- **이스티오의 지능적 설정**
    - 이스티오가 필요한 시점에만 게이트웨이에 SNI 클러스터를 설정
    - 자동으로 최적화된 구성을 제공하는 스마트한 동작 방식
#### SNI 자동 통과로 클러스터 간 트래픽 라우팅하기
- **수동 SNI 통과와의 차이점**
    - 수동 SNI 통과: SNI 헤더 기반으로 트래픽 허용하지만 VirtualService 리소스를 수작업으로 정의해야 함
    - SNI 자동 통과: 허용된 트래픽 라우팅을 위해 VirtualService를 수작업으로 만들 필요 없음
- **SNI 자동 통과의 동작 방식**
    - SNI 클러스터를 사용하여 라우팅 수행
    - 라우터 모드가 sni-dnat일 때 east-west 게이트웨이에서 자동으로 설정됨
    - 이스티오 Gateway 리소스로 설정 가능

```yaml
# cat ch12/gateways/expose-services.yaml              
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: cross-network-gateway
  namespace: istio-system
spec:
  selector:
    istio: eastwestgateway # 셀렉터와 일치하는 게이트웨이에만 설정이 적용된다.
  servers:
    - port:
        number: 15443 # 이스티오에서 15443 포트는 멀티 클러스터 상호 TLS 트래픽 용도로 지정된 특수 포트다
        name: tls
        protocol: TLS
      tls:
        mode: AUTO_PASSTHROUGH # SNI 헤더를 사용해 목적지를 해석하고 SNI 클러스터를 사용한다.
      hosts:
        - "*.local" # 정규식 *.local 과 일치하는 SNI에 대해서만 트래픽을 허용한다.
```

- east 클러스터에 적용 시, east-cluster의 워크로드를 west-cluster에 노출한다.

```bash
# east 클러스터에 적용하자. east-cluster의 워크로드를 west-cluster 에 노출한다.
cat ch12/gateways/expose-services.yaml
keast apply -n istio-system -f ch12/gateways/expose-services.yaml

# 확인
keast get gw,vs,dr -A

# west 에서 호출 시도
kwest get svc,ep -n istioinaction

kwest exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl catalog.istioinaction.svc.cluster.local -v

# east 에 istio-ingressgateway  에 istio-config 정보 확인 : 이전 내용과 동일하게 west 의 CDS/EDS 모두 알고 있음!
for i in listener route cluster endpoint; do echo ">> east k8s cluster : ingressgateway - istio-config $i <<"; docker exec -it east-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done

# east 에 istio-eastwestgateway 에 istio-config 정보 확인 : SNI 자동 통과를 위한 listener 추가 확인!
for i in listener route cluster endpoint; do echo ">> east k8s cluster : eastwestgateway - istio-config $i <<"; docker exec -it east-control-plane istioctl proxy-config $i deploy/istio-eastwestgateway.istio-system; echo; done

ieast proxy-config listener deploy/istio-eastwestgateway.istio-system
ieast proxy-config listener deploy/istio-eastwestgateway.istio-system | grep istioinaction

ieast proxy-config listener deploy/istio-eastwestgateway.istio-system --port 15443  -o json

# west 정보 확인
iwest proxy-status

# west 에 istio-ingressgateway 에 istio-config 정보 확인
for i in listener route cluster endpoint; do echo ">> west k8s cluster : ingressgateway - istio-config $i <<"; docker exec -it west-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done

# west 에 webapp 에 istio-config 정보 확인
for i in listener route cluster endpoint; do echo ">> west k8s cluster : webapp - istio-config $i <<"; docker exec -it west-control-plane istioctl proxy-config $i deploy/webapp.istioinaction; echo; done


# IstioOperator 로 west 클러스터에 east-west 게이트웨이를 설치
cat ch12/gateways/cluster-west-eastwest-gateway.yaml
docker cp ./ch12/gateways/cluster-west-eastwest-gateway.yaml west-control-plane:/cluster-west-eastwest-gateway.yaml
iwest install -f /cluster-west-eastwest-gateway.yaml --set values.global.proxy.privileged=true -y

# west 클러스터에 east-west 게이트웨이를 설치 확인
for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get IstioOperator -n istio-system --kubeconfig=./$i-kubeconfig; echo; done
for i in west east; do echo ">> k8s cluster : $i <<"; kubectl get pod -n istio-system -l istio.io/rev=default --kubeconfig=./$i-kubeconfig; echo; done
kwest get IstioOperator -n istio-system installed-state-istio-eastwestgateway -o yaml
iwest proxy-status


# west 클러스터에 적용하자. east-cluster의 워크로드를 west-cluster 에 노출한다.
cat ch12/gateways/expose-services.yaml
kwest apply -n istio-system -f ch12/gateways/expose-services.yaml

# 확인
kwest get gw,vs,dr -A

kwest get svc,ep -n istioinaction

ieast pc clusters deploy/istio-eastwestgateway.istio-system | grep catalog

# sni 클러스터 확인
ieast pc clusters deploy/istio-eastwestgateway.istio-system | grep catalog | awk '{printf "CLUSTER: %s\n", $1}'
CLUSTER: catalog.istioinaction.svc.cluster.local
CLUSTER: outbound_.80_._.catalog.istioinaction.svc.cluster.local # catalog 서비스용 SNI 클러스터
```

- **SNI 클러스터 정의 확인**
    - catalog 워크로드에 SNI 클러스터가 성공적으로 정의됨
    - 출력을 통해 SNI 클러스터 설정이 완료되었음을 확인 가능
- **SNI 자동 통과를 통한 라우팅**
    - 게이트웨이가 SNI 자동 통과로 설정되어 있음
    - 게이트웨이에 들어오는 트래픽이 SNI 클러스터를 사용하여 의도한 워크로드로 라우팅됨
- **이스티오 컨트롤 플레인의 감지**
    - 컨트롤 플레인이 리소스 생성을 모니터링함
    - 클러스터 간 트래픽을 라우팅할 수 있는 경로가 존재함을 발견
- **워크로드 업데이트**
    - 컨트롤 플레인이 원격 클러스터에서 새로 발견한 엔드포인트로 모든 워크로드를 업데이트
    - 클러스터 간 통신을 위한 설정이 자동으로 완료됨

#### 클러스터 간 워크로드 디스커버리 검증하기
- east-cluster의 워크로드가 west-cluster에 노출되었는지 확인
- 예상 동작
	- webapp 엔보이 클러스터가 catalog 워크로드로 향하는 엔드포인트 보유 예상
	- 엔드포인트는 east-west 게이트웨이 주소를 가리켜야 함
	- east-west 게이트웨이가 catalog 요청을 프록시하는 역할

```bash
# east-cluster의 east-west 게이트웨이 주소(Service) 확인
keast -n istio-system get svc istio-eastwestgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# 이 주소를 west-cluster의 워크로드가 클러스터 간 트래픽을 라우팅할 때 사용하는 주소와 비교
iwest pc endpoints deploy/webapp.istioinaction | grep catalog
```
![]({{ site.url }}/img/post/devops/study/istio/7/20250524161858.png)

```bash
# 직접 요청을 트리거해 확인
kwest get svc -n istio-system istio-ingressgateway

EXT_IP=$(kwest -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}') echo $EXT_IP

docker exec -it mypc curl -s -H "Host: webapp.istioinaction.io" http://$EXT_IP/api/catalog | jq

alias kwest='kubectl --kubeconfig=./west-kubeconfig' EXT_IP=$(kwest -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}') while true; do docker exec -it mypc curl -s -H "Host: webapp.istioinaction.io" http://$EXT_IP/api/catalog ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done
```
![]({{ site.url }}/img/post/devops/study/istio/7/20250524163226.png)

- kiali: east-cluster 확인

![]({{ site.url }}/img/post/devops/study/istio/7/20250524164213.png)

- kiali: west-cluster 확인

![]({{ site.url }}/img/post/devops/study/istio/7/20250524164346.png)

- jaeger: west-cluster 확인

![]({{ site.url }}/img/post/devops/study/istio/7/20250524164539.png)

- jaeger: east-cluster 확인

![]({{ site.url }}/img/post/devops/study/istio/7/20250524164719.png)

- istio-proxy 로그

```bash
# west 에 istio-ingressgateway 로그
kwest logs -n istio-system -l app=istio-ingressgateway -f

# west 에 webapp 로그
kwest logs -n istioinaction -l app=webapp -c istio-proxy -f

kwest logs -n istioinaction -l app=webapp -c webapp -f

# east 에 istio-eastwestgateway 로그
keast exec -it -n istio-system deploy/istio-eastwestgateway -- curl -X POST http://localhost:15000/logging?level=debug
keast logs -n istio-system -l app=istio-eastwestgateway -f

# east 에 catalog 로그
keast logs -n istioinaction -l app=catalog -c istio-proxy -f

keast logs -n istioinaction -l app=catalog -c catalog -f
```

- west: webapp

```bash
kwest exec -it -n istioinaction deploy/webapp -c istio-proxy -- sudo tcpdump -i any tcp -nn
kwest exec -it -n istioinaction deploy/webapp -c istio-proxy -- sudo tcpdump -i lo tcp -nn
kwest exec -it -n istioinaction deploy/webapp -c istio-proxy -- sudo tcpdump -i eth0 tcp -nn

keast get svc -n istio-system istio-eastwestgateway
```

- east: webapp

```bash
# istio-proxy 에 tcp port 3000 에서 패킷 덤프에 출력 결과를 파일로 저장 
keast exec -it -n istioinaction deploy/catalog -c istio-proxy -- sudo tcpdump -i any tcp port 3000 -w /var/lib/istio/data/dump.pcap
keast exec -it -n istioinaction deploy/catalog -c istio-proxy -- ls -l /var/lib/istio/data/

# 출력 결과 파일을 로컬로 다운로드
keast get pod -n istioinaction -l app=catalog -oname
pod/catalog-6cf4b97d-sv9gj

keast cp -n istioinaction -c istio-proxy catalog-6cf4b97d-sv9gj:var/lib/istio/data/dump.pcap ./dump.pcap

# 로컬로 다운 받은 파일을 wireshark 로 불러오기 : XFF 로 요청 Client IP 확인
wireshark dump.pcap
```
![]({{ site.url }}/img/post/devops/study/istio/7/20250524182020.png)

- 다중 클러스터 트래픽 흐름
	- 트래픽 라우팅 순서
		1. west 인그레스 게이트웨이로 요청 수신
		2. west-cluster의 webapp으로 라우팅
		3. east-cluster의 catalog 워크로드로 요청 처리
	- 검증 결과
		- 다중 클러스터, 다중 네트워크, 다중 컨트롤 플레인 서비스 메시 설정 완료
		- 두 클러스터가 서로의 워크로드 발견 가능
		- east-west 게이트웨이를 통과 지점으로 상호 인증 커넥션 구현

- 다중 클러스터 서비스 메시 설정 요구사항
	1. 클러스터 간 워크로드 디스커버리
		- 서비스 어카운트 토큰과 인증서 포함된 kubeconfig 사용
		- 각 컨트롤 플레인에 동료 클러스터 접근 권한 제공
		- istioctl로 east-cluster에만 적용
	2. 클러스터 간 워크로드 연결
		- east-west 게이트웨이 설정으로 다른 클러스터 워크로드 간 트래픽 라우팅
		- 각 클러스터에 네트워크 정보 레이블 지정
	3. 클러스터 간 신뢰 설정
		- 동일한 루트 신뢰로 중간 인증서 발급
	- 몇 단계로 간단하게 구성
	- 대부분 자동화된 설정 과정
### 클러스터 간 로드 밸런싱
- 다중 클러스터 서비스 메시가 준비되어서, 클러스터 지역 인식 로드 밸런싱을 살펴본다.
	- 이를 위해 2개의 샘플 서비스를 배포
	- 이 서비스들은 워크로드가 실행 중인 클러스터의 이름을 반환하도록 설정됨
	- 즉, 요청을 처리하는 워크로드의 위치 확인 가능

```bash
# west-cluster에 첫 번째 서비스 배포
tree ch12/locality-aware/west
ch12/locality-aware/west
├── simple-backend-deployment.yaml
├── simple-backend-dr.yaml
├── simple-backend-gw.yaml
├── simple-backend-svc.yaml
└── simple-backend-vs.yaml

# west-cluster 에 간단한 백엔드 디플로이먼트/서비스를 배포
cat ch12/locality-aware/west/simple-backend-deployment.yaml
cat ch12/locality-aware/west/simple-backend-svc.yaml

kwest apply -f ch12/locality-aware/west/simple-backend-deployment.yaml
kwest apply -f ch12/locality-aware/west/simple-backend-svc.yaml
kwest get deploy -n istioinaction simple-backend-west
kwest get svc,ep -n istioinaction simple-backend

# 트래픽을 허용하기 위해 Gateway, 게이트웨이에서 백엔드 워크로드로 트래픽을 라우팅하기 위해 VirtualService 적용
cat ch12/locality-aware/west/simple-backend-gw.yaml
cat ch12/locality-aware/west/simple-backend-vs.yaml
kwest apply -f ch12/locality-aware/west/simple-backend-gw.yaml
kwest apply -f ch12/locality-aware/west/simple-backend-vs.yaml
kwest get gw,vs,dr -n istioinaction

# west-cluster의 서비스로 요청하고 클러스터 이름을 반환 확인
EXT_IP=$(kwest -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
docker exec -it mypc curl -s -H "Host: simple-backend.istioinaction.io" http://$EXT_IP | jq ".body"
docker exec -it mypc curl -s -H "Host: simple-backend.istioinaction.io" http://$EXT_IP

# 신규 터미널 : 반복 접속
alias kwest='kubectl --kubeconfig=./west-kubeconfig'
EXT_IP=$(kwest -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
while true; do docker exec -it mypc curl -s -H "Host: simple-backend.istioinaction.io" http://$EXT_IP | jq ".body" ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

# east-cluster에 서비스 배포
tree ch12/locality-aware/east
ch12/locality-aware/east
├── simple-backend-deployment.yaml
└── simple-backend-svc.yaml

# east-cluster 에 서비스를 배포
cat ch12/locality-aware/east/simple-backend-deployment.yaml

cat ch12/locality-aware/east/simple-backend-svc.yaml
keast apply -f ch12/locality-aware/east/simple-backend-deployment.yaml
keast apply -f ch12/locality-aware/east/simple-backend-svc.yaml
keast get deploy -n istioinaction simple-backend-east
keast get svc,ep -n istioinaction simple-backend
```

- kiali: west, east

![]({{ site.url }}/img/post/devops/study/istio/7/20250524184247.png)


- 이스티오의 로드밸런싱 기본 값은 라운드 로빈이다.

```bash
# 10회 요청 후 확인
for i in {1..10}; do docker exec -it mypc curl -s -H "Host: simple-backend.istioinaction.io" http://$EXT_IP | jq ".body" ; echo ; done
for i in {1..10}; do docker exec -it mypc curl -s -H "Host: simple-backend.istioinaction.io" http://$EXT_IP | jq ".body" ; echo ; done | sort | uniq -c

# 정보 확인
kwest get svc,ep -n istioinaction simple-backend

for i in listener route cluster endpoint; do echo ">> k8s cluster : west - istio-config $i <<"; docker exec -it west-control-plane istioctl proxy-config $i deploy/istio-ingressgateway.istio-system; echo; done
```
![]({{ site.url }}/img/post/devops/study/istio/7/20250524191113.png)

```
iwest proxy-config listener deploy/istio-ingressgateway.istio-system
iwest proxy-config listener deploy/istio-ingressgateway.istio-system --port 8080 -o json

iwest proxy-config route deploy/istio-ingressgateway.istio-system
iwest proxy-config route deploy/istio-ingressgateway.istio-system --name http.8080
iwest proxy-config route deploy/istio-ingressgateway.istio-system --name http.8080 -o json

iwest proxy-config cluster deploy/istio-ingressgateway.istio-system
iwest proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn simple-backend.istioinaction.svc.cluster.local -o json

iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system
iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system | grep simple

iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' -o json
```
- 이스티오는 레이블을 추출한 정보를 사용해 워크로드의 지역을 설정함

#### 클러스터 간 지역 인식 라우팅 검증하기
```bash
# 실습을 위해 노드에 지역성 정보 레이블 설정
kwest label node west-control-plane 'topology.kubernetes.io/region=westus'
kwest label node west-control-plane 'topology.kubernetes.io/zone=0'
kwest get node -o yaml

keast label node east-control-plane 'topology.kubernetes.io/region=eastus'
keast label node east-control-plane 'topology.kubernetes.io/zone=0'
keast get node -o yaml

# istio eds 에 정보 반영을 위해 파드 재기동하자 : isiotd 가 노드의 지역성 정보 레이블을 엔드포인트 설정할 때 워크로드로 전파.
iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' -o json

kwest rollout restart -n istio-system deploy/istio-ingressgateway
kwest rollout restart -n istio-system deploy/istio-eastwestgateway
kwest rollout restart -n istioinaction deploy/simple-backend-west
keast rollout restart -n istio-system deploy/istio-ingressgateway
keast rollout restart -n istio-system deploy/istio-eastwestgateway
keast rollout restart -n istioinaction deploy/simple-backend-east

iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' -o json

# 지역성 정보를 사용하려면 수동적 passive 헬스 체크가 필수이다.

# 엔드포인트 상태를 수동적으로 확인
# 이상값 감지를 사용하는 DestinationRole 적용
cat ch12/locality-aware/west/simple-backend-dr.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: simple-backend-dr
  namespace: istioinaction
spec:
  host: simple-backend.istioinaction.svc.cluster.local
  trafficPolicy:
    connectionPool:
      http:
        http2MaxRequests: 10
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 1
      interval: 20s
      baseEjectionTime: 30s

kwest apply -f ch12/locality-aware/west/simple-backend-dr.yaml
kwest get gw,vs,dr -n istioinaction

# 확인
iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' -o json
iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local'

# (전파 대기(몇 초 후)) / 요청이 지역 정보를 사용해 동일 클러스터 안에서 라우팅되는 것을 확인
EXT_IP=$(kwest -n istio-system get svc istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
docker exec -it mypc curl -s -H "Host: simple-backend.istioinaction.io" http://$EXT_IP
docker exec -it mypc curl -s -H "Host: simple-backend.istioinaction.io" http://$EXT_IP | jq ".body"

# 동일 클러스터 안에서 라우팅 되는 것을 확인
for i in {1..20}; do docker exec -it mypc curl -s -H "Host: simple-backend.istioinaction.io" http://$EXT_IP | jq ".body" ; echo ; done | sort | uniq -c
 20 "Hello from WEST"

# 모든 요청은 west-cluster 내에서 라우팅됨
# 트래픽을 라우팅하는 인그레스 게이트웨이에거 가장 가깝기 때문
# 모든 라우팅 결정을 엔보이 프록시가 하므로,
# 컨트롤 플레인이 엔보이 프록시의 설정을 수정했다고 결론지을 수 있음
#
iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' -o json
...
                "weight": 1,
                "locality": { 
                    "region": "westus", # priority 가 없으면(생략 시), 0으로 우선 순위가 가장 높음
                    "zone": "0"
                }
            ...
                "weight": 1,
                "priority": 1, # priority 0 다음으로, 두 번쨰 우선순위
                "locality": {
                    "region": "eastus",
                    "zone": "0"
                }
...
# 우선순위가 가장 높은 호스트가 사용불가가 되면, 우선순위가 낮은 호스트로 라우팅됨
```
#### 클러스터 간 장애 극복 확인하기
- 백엔드 디플로이먼트가 실패하는 상황을 시뮬레이션
	- `ERROR_RATE` 값 을 1로 설정
- 시간이 지나면, 호스트가 비정상임을 감지하고 다음 우선순위(east-cluster) 워크로드로 라우팅한다.

```bash
# 신규 터미널 : 반복 접속 해두기
while true; do docker exec -it mypc curl -s -H "Host: simple-backend.istioinaction.io" http://$EXT_IP | jq ".body" ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

kwest -n istioinaction set env deploy simple-backend-west ERROR_RATE='1'
kwest exec -it -n istioinaction deploy/simple-backend-west -- env | grep ERROR
ERROR_RATE=1

iwest proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local'
ENDPOINT                 STATUS      OUTLIER CHECK     CLUSTER
10.10.0.20:8080          HEALTHY     FAILED            outbound|80||simple-backend.istioinaction.svc.cluster.local
172.18.255.202:15443     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
```

![]({{ site.url }}/img/post/devops/study/istio/7/20250524202719.png)

- 클러스터 간 트래픽은 상대 클러스터의 east-west gateway를 통과하며 SNI 통과로 처리됨
	- 원격 클러스터에 도달한 트래픽의 로드 밸런싱에 영향을 줌
	- 이 호출은 SNI/TCP 커넥션
		- 게이트웨이가 TLS 커넥션을 종료하지 않음
		- east-west gateway는 커넥션을 그대로 백엔드 서비스에 전달
		- 커넥션이 east-west gateway에서 백엔드 서비스까지 이어짐
			- 요청 단위로 로드 밸런싱 되지 않음
	- 클러스터 사이의 장애 극복 / 로드 밸런싱
		- 클라이언트 관점으로는 부하 분산이나 장애 극복이 수행됨
		- 트래픽이 원격 클러스터의 모든 인스턴스 사이에서 반드시 균등하게 분산을 보장하지 않음

#### 인가 정책을 사용해 클러스터 간 접근 제어 확인하기
- 접근 제어 요구사항:
	- 워크로드 간 트래픽 상호 인증 필요
	- 믿을 수 있는 메타데이터 생성 필요
	- 트래픽 승인 또는 거부 결정에 사용

- 시연 시나리오:
	- 인그레스 게이트웨이 출처 트래픽만 서비스 접근 허용
	- 다른 출처 트래픽은 거부

```bash
# 적용 전에 west-cluster 서비스를 제거해서 east 에서만 트래픽을 처리하게 하자 >> 이미 위에서 장애 상황이라 안해도 되긴함
kwest delete deploy simple-backend-west -n istioinaction

#
cat ch12/security/allow-only-ingress-policy.yaml
apiVersion: "security.istio.io/v1beta1"
kind: "AuthorizationPolicy"
metadata:
  name: "allow-only-ingress"
  namespace: istioinaction
spec:
  selector:
    matchLabels:
      app: simple-backend
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/istio-system/sa/istio-ingressgateway-service-account"]

keast apply -f ch12/security/allow-only-ingress-policy.yaml
keast get authorizationpolicy -A


# 업데이트가 전파되면, west-cluster의 워크로드에서 요청을 만들어 정책 검증
# 이를 위해 임시 파드 실행
# 정책이 인그레스 게이트웨이에서 들어온 트래픽을 허용할 것
# 워크로드가 클러스터 간에 mTLS하여 정책이 ID 인증서에 인코딩된 인증데이터를 접근 데어에 사용할 수 있음
kwest run netshoot -n istioinaction --rm -it --image=nicolaka/netshoot -- zsh
-----------------------------------
curl -s webapp.istioinaction/api/ca
talog

# 직접 요청하면 실패!
curl -s simple-backend.istioinaction.svc.cluster.local
RBAC: access denied

# istio-ingressgateway 로 요청하면 성공!
	curl -s -H "Host: simple-backend.istioinaction.io" http://istio-ingressgateway.istio-system

# kiali 등 확인을 위해 반복 접속 실행
watch curl -s simple-backend.istioinaction.svc.cluster.local
watch 'curl -s -H "Host: simple-backend.istioinaction.io" http://istio-ingressgateway.istio-system'

exit
-----------------------------------
```

![]({{ site.url }}/img/post/devops/study/istio/7/20250524204126.png)

- 검증된 기능들:
	- 로드 밸런싱
	- 지역 인식 라우팅
	- 클러스터 간 장애 극복
	- 상호 인증 트래픽
	- 접근 제어

- 이스티오의 확장성
	- 조직 내에서 확장 가능
	- 여러 클러스터를 단일 메시로 통합
	- 여러 조직에게 중요한 가치 제공

# chap14. 이스티오의 요청 처리 기능 확장하기
- 엔보이 프록시의 주요 강점은 확장 가능성

- 엔보이 Request Flow 처리 단계: - https://www.envoyproxy.io/docs/envoy/latest/intro/life_of_a_request
	1. 다운스트림 TCP 연결이 워커 스레드의 엔보이 리스너에 수락됨
	2. 리스너 필터 체인 생성 및 실행 (SNI, pre-TLS 정보 제공)
	3. TLS 전송 소켓이 TCP 연결 데이터를 복호화
	4. 네트워크 필터 체인 생성 및 실행 (HTTP 연결 관리자 포함)
	5. HTTP/2 코덱이 복호화된 데이터 스트림을 독립적인 스트림으로 분리
	6. 각 HTTP 스트림에 대해 다운스트림 HTTP 필터 체인 생성 및 실행
	7. 클러스터별 로드 밸런싱 수행하여 엔드포인트 선택
	8. 각 스트림에 대해 업스트림 HTTP 필터 체인 생성 및 실행
	9. 업스트림 엔드포인트의 HTTP/2 코덱이 요청 스트림을 멀티플렉싱
	10. TLS 전송 소켓이 바이트를 암호화하여 TCP 소켓에 전송
	11. 요청과 응답이 프록시되며, 응답은 HTTP 필터를 역순으로 통과
	12. 스트림 완료 후 통계 업데이트, 액세스 로그 작성, 추적 스팬 완료

### 엔보이의 필터 체인 이해하기

- 엔보이 리스너 기본 개념
    - 리스너는 네트워킹 인터페이스에 포트를 열고 들어오는 트래픽을 수신하는 방법
    - 엔보이는 네트워크 커넥션에서 바이트를 가져와 처리하는 L3/L4 프록시
    - 리스너가 네트워크 스트림에서 바이트를 읽어 다양한 필터 단계를 거쳐 처리

- 네트워크 필터
    - 엔보이의 가장 기본적인 필터
    - 바이트 스트림에서 인코딩/디코딩 작업 수행
    - 둘 이상의 필터가 순서대로 동작하는 필터 체인 구성 가능
    - 필터 체인으로 프록시 기능 구현

![]({{ site.url }}/img/post/devops/study/istio/7/20250524220517.png)

- 주요 네트워크 필터 종류
    - MongoDB, Redis, Thrift, Kafka
    - HTTP Connection Manager (HCM) - 가장 많이 사용

![]({{ site.url }}/img/post/devops/study/istio/7/20250524221312.png)

- HTTP Connection Manager (HCM)
    - 바이트 스트림을 HTTP 헤더, 바디, 트레일러로 변환
    - HTTP 1.1, HTTP 2, gRPC, HTTP 3 등 HTTP 기반 프로토콜 지원
    - 헤더, 경로 접두사 등 요청 속성 기반 라우팅 처리
    - 액세스 로깅, 헤더 조작 기능 제공

- HTTP 필터
    - HCM 내부에 필터 기반 아키텍처 존재
    - HTTP 요청에서 순서대로 동작하는 HTTP 필터 체인 구성 가능
    - 터미널 필터(라우터 필터)로 끝나야 함

- 기본 HTTP 필터 예시
    - CORS, CSRF, ExternalAuth, RateLimit
    - Fault injection, gRPC/JSON transcoding, Gzip
    - Lua, RBAC, Tap, Router, WebAssembly

- 라우터 필터
    - HTTP 필터 체인의 마지막 터미널 필터
    - 요청을 적절한 업스트림 클러스터로 전달
    - 타임아웃과 재시도 파라미터 설정 가능

![]({{ site.url }}/img/post/devops/study/istio/7/20250524223817.png)

- 커스텀 필터 개발
    - 엔보이 핵심 코드 변경 없이 자체 필터 작성 가능
    - 프록시 위에 계층화하여 추가
    - 이스티오는 엔보이 위에 필터를 추가해 커스텀 엔보이 빌드
    - 커스텀 빌드 시 유지보수 부담과 C++ 개발 필요성 존재

### 확장용 필터

- 엔보이 확장 방법
    - C++로 커스텀 필터 작성하여 프록시에 내장 가능
    - 엔보이 바이너리 컴파일 없이 HTTP 기능 확장 가능

- 바이너리 변경 없는 확장용 HTTP 필터
    - 외부 처리 (External processing)
    - 루아 (Lua)
    - 웹어셈블리 (Wasm/WebAssembly)

- 필터 활용 방법
    - 외부 서비스 호출 설정
    - 루아 스크립트 실행
    - 커스텀 코드 실행으로 HCM 기능 강화
    - HTTP 요청/응답 처리 시 기능 확장

- 주요 활용 사례
    - 속도 제한 필터를 통한 외부 서비스 호출 처리 (중점 다룰 예정)
    - 외부 인가 요청 ([9장](https://kimdoky.github.io/devops/2025/05/10/study-istio-week5/))

### 이스티오의 데이터 플레인 커스터마이징하기

- 엔보이 데이터 플레인 확장 방법
	- 엔보이 HTTP 필터를 이스티오 API의 EnvoyFilter 리소스로 설정
	- 속도 제한 서버(RLS, Rate-Limit Server) 호출
	- 루아 스크립트 구현하여 루아 HTTP 필터에 로드
	- 웹어셈블리 HTTP 필터용 Wasm 모듈 구현

- 이스티오의 EnvoyFilter 리소스 사용
- 엔보이의 필터 아키텍처에 대한 깊이 있는 이해 필요

## EnvoyFilter 리소스로 엔보이 필터 설정하기
- EnvoyFilter 리소스 기본 개념
	- 이스티오 API가 추상화하지 않는 엔보이 설정을 직접 구성할 때 사용
	- VirtualService, DestinationRule 등은 결국 엔보이 설정으로 변환됨
	- 이스티오는 엔보이의 모든 필터/설정을 노출하지 않음
	- 고급 사용 사례를 위한 비상 수단(break glass solution)

- EnvoyFilter 주의사항
	- 고급 사용자용으로 전체 데이터 플레인을 중단시킬 수 있음
	- 엔보이 API는 이스티오 버전 간 언제든 변경 가능
	- 이전 버전과의 호환성 보장 안됨
	- 배포 전 반드시 유효성 검증 필요

- EnvoyFilter 적용 규칙
	- 달리 지정하지 않으면 네임스페이스의 모든 워크로드에 적용
	- istio-system 네임스페이스에 생성 시 메시 전체에 적용
	- workloadSelector로 특정 워크로드 지정 가능
	- 다른 이스티오 리소스들이 모두 변환/설정된 후에 적용

- tap 필터 사용 목적
	- 워크로드의 데이터 플레인을 거치는 특정 요청 디버깅
	- 엔보이의 기존 tap 필터 활용
	- 메시지 샘플링하여 수신 에이전트로 스트리밍

![]({{ site.url }}/img/post/devops/study/istio/7/20250524224205.png)

- EnvoyFilter 구성 요소
	- workloadSelector: app: webapp으로 특정 워크로드 지정
	- applyTo: HTTP_FILTER로 설정 위치 지정
	- match: SIDECAR_INBOUND, 포트 8080, router 필터 지정
	- patch: INSERT_BEFORE 작업으로 router 필터 앞에 tap 필터 추가

```yaml
# cat ch14/tap-envoy-filter.yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: tap-filter
  namespace: istioinaction
spec:
  workloadSelector:
    labels:
      app: webapp # 워크로드 셀렉터
  configPatches:
  - applyTo: HTTP_FILTER # 설정할 위치
    match:
      context: SIDECAR_INBOUND
      listener:
        portNumber: 8080
        filterChain:
          filter:
            name: "envoy.filters.network.http_connection_manager"
            subFilter:
              name: "envoy.filters.http.router"
    patch: # 엔보이 설정 패치
      operation: INSERT_BEFORE
      value:
       name: envoy.filters.http.tap
       typed_config:
          "@type": "type.googleapis.com/envoy.extensions.filters.http.tap.v3.Tap"
          commonConfig:
            adminConfig:
              configId: tap_config
```

## 외부 호출로 요청 속도 제한하기
- 속도 제한
	- 기본 HTTP 필터 기능으로 이스티오 데이터 플레인 확장
	- 외부 호출 기능을 가진 기본 필터들 활용
	- 외부 서비스 호출하여 요청 계속 여부 결정

- 속도 제한 목적
	- 특정 워크로드에서 서비스 측 속도 제한 적용
	- 속도 제한 서비스 호출하도록 이스티오 데이터 플레인 설정
	- 엔보이 HTTP 필터에서 속도 제한 호출 기능 제공

![]({{ site.url }}/img/post/devops/study/istio/7/20250524225327.png)

- 엔보이 속도 제한 방식
	- 네트워크 필터, 로컬 속도 제한, 글로벌 속도 제한 등 여러 방법 존재
	- 글로벌 속도 제한 기능에 집중
	- 모든 엔보이 프록시가 동일한 속도 제한 서비스 호출
	- 백엔드 글로벌 키-값 저장소 활용

![]({{ site.url }}/img/post/devops/study/istio/7/20250524225652.png)

- 글로벌 속도 제한 아키텍처
	- 서비스 복제본 개수와 무관하게 속도 제한 적용 가능
	- 요청 속성을 속도 제한 서버로 전송하여 결정
	- 특정 요청에 속도 제한 적용 여부 판단

- 속도 제한 서버 배포
	- 엔보이 커뮤니티 제공 속도 제한 서버 사용
	- 엔보이 속도 제한 API 구현한 서버 배포 필요
	- 백엔드 레디스 캐시와 통신 설정
	- 레디스에 속도 제한 카운터 저장 (Memcached 사용 가능)

- 설정 요구사항
	- 속도 제한 서버 배포 전 기대하는 속도 제한 동작으로 설정 필요

### 엔보이 속도 제한 이해하기

- 엔보이 HTTP 전역 속도 제한 기본 개념
    - HTTP 필터로 존재하며 HCM의 HTTP 필터 체인에 설정 필요
    - 속도 제한 서버(RLS) 구성 전 작동 원리 이해 필수

- 속도 제한 필터 처리 과정
    - HTTP 요청 처리 시 요청에서 특정 속성 추출
    - 추출한 속성을 RLS로 전송하여 평가 받음
    - 디스크립터(descriptors): 속도 제한에서 속성들 또는 속성 그룹들

- 디스크립터 종류
    - 원격 주소 (remote address)
    - 요청 헤더 (request headers)
    - 목적지 (destination)
    - 요청의 기타 일반 속성들

- RLS 평가 과정
    - 전송된 요청 속성을 미리 정의한 속성 집합과 비교
    - 일치하는 속성의 카운터를 증가시킴
    - 속성들을 트리 형태로 그룹화하거나 정의하여 카운트할 속성 결정

- 속도 제한 적용 기준
    - 속성 또는 속성 집합이 RLS 정의와 일치하면 해당 제한 횟수 증가
    - 카운트가 임계값 초과 시 해당 요청에 속도 제한 적용

#### 엔보이 속도 제한 서버 설정하기
- 예제의 속도 제한 목적
    - 로열티 등급에 따라 특정 사용자 그룹 제한
    - x-loyalty 헤더를 검사하여 로열티 등급 판단

- 로열티 등급별 제한 규칙
    - 골드 등급 (x-loyalty: gold): 분당 10개 요청 허용
    - 실버 등급 (x-loyalty: silver): 분당 5개 요청 허용
    - 브론즈 등급 (x-loyalty: bronze): 분당 3개 요청 허용
    - 식별 불가능한 등급: 분당 1개 요청 허용

```yaml
# cat ch14/rate-limit/rlsconfig.yaml 
apiVersion: v1
kind: ConfigMap
metadata:
  name: catalog-ratelimit-config
  namespace: istioinaction
data:
  config.yaml: |
    domain: catalog-ratelimit
    descriptors:
      - key: header_match
        value: no_loyalty
        rate_limit:
          unit: MINUTE
          requests_per_unit: 1
      - key: header_match
        value: gold_request
        rate_limit:
          unit: MINUTE
          requests_per_unit: 10
      - key: header_match
        value: silver_request
        rate_limit:
          unit: MINUTE
          requests_per_unit: 5
      - key: header_match
        value: bronze_request
        rate_limit:
          unit: MINUTE
          requests_per_unit: 3
```
- 주요 특징
    - 실제 요청 헤더를 직접 다루지 않고 전송된 속성만 처리
    - 속성 정의 방법은 다음 절에서 다룰 예정
    - 요청 처리 시 속성이 규칙 조건과 일치하면 제한 적용

#### 요청 경로에 속도 제한 걸기
- 속도 제한 조치 설정
    - 속도 제한 서버 설정 완료 후 엔보이에 속성 전송 설정 필요
    - "특정 요청 경로에 취하는 속도 제한 조치(rate-limit action)"

- 설정 목적
    - catalog 서비스의 `/items` 경로 호출 시 `x-loyalty` 헤더 존재 여부 포착
    - 요청이 어느 그룹에 속하는지 판단

- 설정 방법
    - 특정 엔보이 루트 설정에 rate_limit 설정 지정 필요
    - 적절한 속성 action을 속도 제한 서버로 전송하도록 구성

- 이스티오에서의 구현
    - 이스티오에 전용 API가 아직 없음 (저술 시점 기준)
    - EnvoyFilter 리소스 사용 필요
    - catalog 서비스의 모든 경로에 속도 제한 조치 지정 가능

```yaml
# cat ch14/rate-limit/catalog-ratelimit-actions.yaml 
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: catalog-ratelimit-actions
  namespace: istioinaction
spec:
  workloadSelector:
    labels:
      app: catalog
  configPatches:
    - applyTo: VIRTUAL_HOST
      match:
        context: SIDECAR_INBOUND
        routeConfiguration:
          vhost:
            route:
              action: ANY
      patch:
        operation: MERGE
        # Applies the rate limit rules.
        value:
          rate_limits: # 속도 제한 조치
            - actions:
              - header_value_match:
                  descriptor_value: no_loyalty
                  expect_match: false
                  headers:
                  - name: "x-loyalty"
            - actions:
              - header_value_match:
                  descriptor_value: bronze_request
                  headers:
                  - name: "x-loyalty"
                    exact_match: bronze
            - actions:
              - header_value_match:
                  descriptor_value: silver_request
                  headers:
                  - name: "x-loyalty"
                    exact_match: silver
            - actions:
              - header_value_match:
                  descriptor_value: gold_request
                  headers:
                  - name: "x-loyalty"
                    exact_match: gold
```

```bash
# k8s cm으로 규칙을 배포하고, 속도 제한 서버를 레디스 백엔드와 함께 배포
tree ch14/rate-limit
ch14/rate-limit
├── catalog-ratelimit-actions.yaml
├── catalog-ratelimit.yaml
├── rls.yaml
└── rlsconfig.yaml

cat ch14/rate-limit/rlsconfig.yaml
cat ch14/rate-limit/rls.yaml

kubectl apply -f ch14/rate-limit/rlsconfig.yaml -n istioinaction
kubectl apply -f ch14/rate-limit/rls.yaml -n istioinaction

# 확인
kubectl get cm -n istioinaction catalog-ratelimit-config
kubectl get pod -n istioinaction

# 엔보이가 속성을 속도 제한 서버로 보내게 해야 한다.
# 그래야 속도 제한 서버가 개수를 세어 속도 제한을 처리할 수 있기 때문
# 그 역할을 하는 EnvoyFilter를 적용
cat ch14/rate-limit/catalog-ratelimit.yaml
cat ch14/rate-limit/catalog-ratelimit-actions.yaml
kubectl apply -f ch14/rate-limit/catalog-ratelimit.yaml -n istioinaction
kubectl apply -f ch14/rate-limit/catalog-ratelimit-actions.yaml -n istioinaction
kubectl get envoyfilter -A

# 속도 제한 기능 테스트
# sleep 앱에서 catalog 서비스를 호출 시도 : 대략 1분에 한 번 정도 호출 성공! >> x-loyalty 헤더가 없을 때 속도 제한 값!
kubectl exec -it deploy/sleep -n istioinaction -c sleep -- curl http://catalog/items -v

kubectl exec -it deploy/sleep -n istioinaction -c sleep -- curl http://catalog/items -v

# silver 헤더는? (반복 호출)
kubectl exec -it deploy/sleep -n istioinaction -c sleep -- curl -H "x-loyalty: silver" http://catalog/items -v

docker exec -it myk8s-control-plane istioctl proxy-config route deploy/catalog.istioinaction --name 'InboundPassthroughClusterIpv4'
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/catalog.istioinaction --name 'InboundPassthroughClusterIpv4' -o json | grep actions

docker exec -it myk8s-control-plane istioctl proxy-config route deploy/catalog.istioinaction --name 'inbound|3000||'
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/catalog.istioinaction --name 'inbound|3000||' -o json | grep actions
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/catalog.istioinaction --name 'inbound|3000||' -o json
```

![]({{ site.url }}/img/post/devops/study/istio/7/20250525001540.png)

## 루아로 이스티오의 데이터 플레인 확장하기

- 루아 확장의 필요성
    - 기존 엔보이 필터로 구현할 수 없는 기능이 필요한 경우
    - 요청 경로에 커스텀 로직 구현이 필요한 경우
    - 자체 커스텀 로직으로 데이터 플레인 동작 확장

- 루아 필터 기능
    - 엔보이의 기본 필터 중 하나
    - 루아 스크립트를 작성하여 프록시에 주입 가능
    - 요청/응답 경로의 동작을 커스터마이징

- 루아 스크립트 활용
- 요청이나 응답의 헤더 조작
- 바디 검사 및 처리
- EnvoyFilter 리소스를 통해 데이터 플레인 설정
- 요청 경로 처리 변경 가능

![]({{ site.url }}/img/post/devops/study/istio/7/20250525003015.png)

- 루아 프로그래밍 언어 특징
    - 강력하면서도 내장 가능한 스크립팅 언어
    - 시스템 기능 강화 목적으로 설계
    - 동적 타입의 인터프리터 언어
    - 루아 가상머신의 자동 메모리 관리 (엔보이에서는 LuaJIT 사용)

- 성능 고려사항
    - 요청 바디 검사 시 프록시의 스트림 처리 방식에 영향
    - 바디 전체를 메모리에 적재할 경우 성능에 영향 가능
    - 루아 필터 사용 시 엔보이 문서 참조 권장

- 구현 방법
    - EnvoyFilter 리소스를 사용하여 루아 스크립트 주입
    - 요청 경로 처리 변경을 통한 기능 확장

## 웹어셈블리로 이스티오의 데이터 플레인 확장하기
### 웹어셈블리 소개

- 웹어셈블리(Wasm) 기본 개념
    - 바이너리 명령 형식으로 설계
    - 여러 환경 간 이식 가능을 목표
    - 여러 프로그래밍 언어로 컴파일 가능
    - 가상머신에서 실행

- 개발 목적
    - 브라우저 웹 애플리케이션의 CPU 집약적 작업 실행 속도 향상
    - 브라우저 기반 애플리케이션 지원을 자바스크립트 외 언어로 확장
    - 2019년 W3C 권고사항으로 승인
    - 모든 주요 브라우저에서 지원

- 웹어셈블리 특징
    - 모듈로 패키징된 커스텀 코드
    - 격리된 가상머신에서 안전하게 실행
    - 저장 공간과 메모리를 적게 차지
    - 거의 네이티브에 가까운 속도로 실행

- 보안 특성
    - 호스트 애플리케이션에 내장되어도 안전
    - 메모리 안전(memory safe) 보장
    - 격리된(sandboxed) 실행 환경에서 동작
    - 호스트 시스템이 허용하는 메모리와 기능에만 접근 가능

- 실행 환경
    - 대상 호스트(웹 브라우저 등) 내부의 가상머신에서 실행
    - 호스트 시스템의 제어 하에 제한된 접근 권한

### 왜 엔보이에 웹어셈블리를 사용하는가?

- 네이티브 엔보이 필터 작성의 단점
    - C++ 언어 사용 필수
    - 변경 사항을 엔보이의 새 바이너리로 정적 빌드 필요
    - 사실상 '커스텀' 엔보이 빌드 필요

- 엔보이의 웹어셈블리 지원
    - 웹어셈블리 실행 엔진 내장
    - HTTP 필터 포함 엔보이의 다양한 영역 커스터마이징 가능
    - 확장 기능 제공

- 웹어셈블리 필터 장점
    - 웹어셈블리 지원 언어로 엔보이 필터 작성 가능
    - 런타임에 프록시로 동적 로드 가능
    - 기본 엔보이 프록시 사용하면서 커스텀 필터 동적 로드

- 웹어셈블리 모듈 배포 방식
    - 로컬 캐시에 Wasm 확장 설정
    - 원하는 Wasm 확장을 로컬 캐시로 풀
    - 적절한 워크로드에 wasm-cache 마운트
    - EnvoyFilter CRD로 Wasm 필터 사용하도록 엔보이 구성

- Istio의 원격 Wasm 모듈 지원
    - Istio 1.9부터 istio-agent가 원격 HTTP 소스에서 Wasm 바이너리 로드
    - xDS 프록시와 ECDS 활용한 안정적인 솔루션 제공
    - Istio 1.12에서 새로운 Wasm API 구현

- OCI 이미지 지원
    - Istio 1.12부터 Wasm OCI 이미지로 기능 확장
    - Docker Hub, GCR, ECR 등 모든 OCI 레지스트리에서 Wasm 이미지 가져오기 가능
    - Wasm 바이너리 추출, 캐시 후 Envoy 필터 체인에 삽입

- 안정적인 배포 메커니즘
    - istio-agent가 확장 구성 리소스 업데이트 가로채기
    - 원격 페치 힌트 읽어와 Wasm 모듈 다운로드
    - 다운로드 실패 시 ECDS 업데이트 거부로 잘못된 구성 방지
