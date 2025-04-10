---
layout: post
section-type: post
title: ServiceMesh - Istio - Week1
category: devops
tags: ["k8s", "istio", "servicemesh"]
---

Book for Istio study : ['Istio in action'](https://product.kyobobook.co.kr/detail/S000031741439)

![]({{ site.url }}/img/post/devops/study/istio/1/book.jpg)

> 표지는 그라셋 드 생소보르 컬렉션 중 아이슬란드 여인(Icelandic woman)이다.

## 1. 서비스 메시 소개하기

### 서비스 메시란?

분산 애플리케이션 네트워크 인프라  
애플리케이션 간의 통신을 안전하고 복원력 있게 만들며 관찰 가능성과 제어 능력을 제공  
Data Plane과 Control Plane으로 구성된 아키텍처를 통해 네트워크 트래픽을 관리하고 정책을 구현  
 특정 프로그래밍 언어나 프레임워크에 의존하지 않고도 중요한 네트워킹 기능을 애플리케이션 외부에서 구축할 수 있다.

![]({{ site.url }}/img/post/devops/study/istio/1/1.png)

### 서비스 메시는 왜 필요한가?

#### 클라우드 네이티브 환경의 문제들

- 불규칙한 요청 처리 시간
  - 서비스 간 통신에서 성능 저하가 발생하면 연쇄 장애를 일으킬 수 있다.
- 배포 자동화의 위험성
  - 테스트 자동화로 잡히지 않는 버그가 배포되거나, 블루-그린 배포 접근법이 오히려 '빅뱅' 릴리스로 이어질 수 있다.
- 보안의 일관성 부족
  - 팀마다 다른 보안 접근법을 사용해 혼란이 야기된다.

서비스메시는 복원력, 보안, 메트릭 수집 등의 기능을 애플리케이션 외부에서 해결  
효율성을 높이고(비싼 자원 == 개발자) 운영을 단순화

이스티오는 서비스 메시의 오픈소스 구현체이다.

### 주요 특징

- Data Plane
  - Envoy 프록시를 기반으로 한 서비스 프록시를 사용해 트래픽 관리, 보안 강화, 메트릭 및 트레이싱 생성 등의 기능을 제공한다.
- Control Plane
  - 운영자가 Data Plane의 동작을 제어할 수 있도록 API를 노출하며, 정책 설정과 보안 관리를 지원한다.

이스티오는 애플리케이션 코드 변경 없이도 복원력있는 시스템 구축을 가능하게 하며, 다양한 플랫폼(K8S, VM 등)에서 사용할 수 있다.

> [DoKy's Blog - DataPlane](https://kimdoky.github.io/devops/2024/11/30/devops-dataplane/https://kimdoky.github.io/devops/2024/11/30/devops-dataplane/)

### 주요 기능

- 복원력 강화
  - 재시도, 타임아웃, 서킷 브레이커 등을 통해 장애에 대한 대응력을 높임
- 관찰 가능성
  - 메트릭과 트레이싱 데이터를 통해 시스템 상태를 실시간으로 파악
- 트래픽 제어
  - 카나리 릴리즈, 단계적 롤아웃 등 세밀한 릴리스 전략 구현 지원
- 보안 강화
  - mTLS를 통해 전송 계층 암호화를 적용하며, 정책 강제와 접근 제어를 지원

![]({{ site.url }}/img/post/devops/study/istio/1/2.png)

### 서비스 메시와 다른 기술 비교

과거의 서비스 메시와 유사한 서비스들

- ESB
  - 중앙집중식 구조로 인해 병목 현상 발생 가능
  - 비즈니스 로직과 네트워킹 문제 혼합
    ![]({{ site.url }}/img/post/devops/study/istio/1/5.png)
- API 게이트웨이
  - 공개 API 관리에 초점
  - 내부 트래픽 처리시 병목 현상 유발 가능
    ![]({{ site.url }}/img/post/devops/study/istio/1/6.png)
- 서비스 메시
  - 분산형 구조로 병목 지점 제거
  - 복원력, 보안, 관찰 가능성 등 네트워킹 문제에만 집중
    ![]({{ site.url }}/img/post/devops/study/istio/1/7.png)

### 서비스 메시 도입시 고려사항

- 복잡성 증가
  - 요청 경로에 프록시라는 레이어가 추가되어 디버깅이 어려워짐
  - 프록시에 익숙치 않은 이들에게는 블랙박스가 되어 디버깅이 어려워질 수 있음
- 테넌시 관리
  - 적절한 격리 모델 및 정책 없이는 여러 서비스 간 충돌 가능성이 존재함
- 운영 부담
  - 새로운 계층으로 인해 조직 내 절차와 거버넌스를 재정비해야 할 필요가 있음

![]({{ site.url }}/img/post/devops/study/istio/1/3.png)

모든 기술에는 트레이드 오프가 존재  
서비스 메시도 마찮가지다.  
도입 전에 조직의 요구 사항과 제약 조건을 충분히 평가하고 계획적으로 실행해야 한다.

## 2. 이스티오 첫 걸음

1장에서는 서비스 메시에 대해 다루었다면, 2장에서부터 이스티오에서 다룬다.  
자세한 부분은 스터디가 진행되면서 깊이 다루겠지만, 우선 핸즈온 형식으로 이스티오가 어떤 구조로 무엇을 할 수 있는지 전체적인 청사진을 제공한다.

이 책의 아쉬운 점은 최신 버전과 차이가 많이 난다는 것이다.  
스터디에서는 kind를 통해 클러스터를 구성하고 실습을 진행한다.

### 1. [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/) 설치

책에서는 최소 vCPU 4, Memory 8GB 할당 권고(그 이상이면 됨)

![]({{ site.url }}/img/post/devops/study/istio/1/4.png)

> 그냥 넉넉히...

### 2. kind 및 utils 설치

#### 필수

- kind
- kubectl
- helm

```bash
# Install Kind
brew install kind
kind --version

# Install kubectl
brew install kubernetes-cli
kubectl version --client=true

## kubectl -> k 단축키 설정
echo "alias k=kubectl" >> ~/.zshrc

# Install Helm
brew install helm
helm version
```

#### 유틸

- krew
- kube-ps1
- kubectx
- kubecolor
- neat
- stern

```bash
# Utils 설치
brew install krew
brew install kube-ps1
brew install kubectx

# kubectl 출력 시 하이라이트 처리
brew install kubecolor
echo "alias kubectl=kubecolor" >> ~/.zshrc
echo "compdef kubecolor=kubectl" >> ~/.zshrc

# krew 플러그인 설치
kubectl krew install neat stern
```

#### kind 기본 사용

```bash
# Create a cluster with kind
kind create cluster

# 클러스터 배포 확인
kind get clusters
kind get nodes
kubectl cluster-info

# 노드 정보 확인
kubectl get node -o wide

# 파드 정보 확인
kubectl get pod -A
kubectl get componentstatuses
```

### kind로 k8s 배포

```bash
# 클러스터 배포 전 확인
docker ps

# 방안1 : 환경변수 지정
export KUBECONFIG=$PWD/kubeconfig

# Create a cluster with kind : 1.29.14 , 1.30.10 , 1.31.6 , 1.32.2
kind create cluster --name myk8s --image kindest/node:v1.32.2 --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30000
    hostPort: 30000
  - containerPort: 30001
    hostPort: 30001
  - containerPort: 30002
    hostPort: 30002
  - containerPort: 30003
    hostPort: 30003
  kubeadmConfigPatches:
  - |
    kind: ClusterConfiguration
    controllerManager:
      extraArgs:
        bind-address: "0.0.0.0"
    etcd:
      local:
        extraArgs:
          listen-metrics-urls: "http://0.0.0.0:2381"
    scheduler:
      extraArgs:
        bind-address: "0.0.0.0"
  - |
    kind: KubeProxyConfiguration
    metricsBindAddress: "0.0.0.0"
EOF

# 확인
$ kind get nodes --name myk8s
myk8s-control-plane

$ kubens default
Context "kind-myk8s" modified.
Active namespace is "default".

# kind 는 별도 도커 네트워크 생성 후 사용 : 기본값 172.18.0.0/16
$ docker network ls
NETWORK ID     NAME                DRIVER    SCOPE
4b5fa1fad600   bridge              bridge    local
a98f566148c0   host                host      local
03a59a7c78a8   kind                bridge    local
840dfd9b7e86   minikube            bridge    local
1eef9e15a3b9   multinode-cluster   bridge    local
ff5e4368dd44   none                null      local

$ docker inspect kind | jq
[
  {
    "Name": "kind",
    "Id": "03a59a7c78a86b83709bdf17ac47d6ebb7df2203917bc9fa0542481c80da6b86",
    "Created": "2025-04-06T11:59:24.607331927Z",
    "Scope": "local",
    "Driver": "bridge",
    "EnableIPv4": true,
    "EnableIPv6": true,
    "IPAM": {
      "Driver": "default",
      "Options": {},
      "Config": [
        {
          "Subnet": "172.18.0.0/16",
          "Gateway": "172.18.0.1"
        },
        {
          "Subnet": "fc00:f853:ccd:e793::/64",
          "Gateway": "fc00:f853:ccd:e793::1"
        }
      ]
    },
    "Internal": false,
    "Attachable": false,
    "Ingress": false,
    "ConfigFrom": {
      "Network": ""
    },
    "ConfigOnly": false,
    "Containers": {
      "b20ffea7929859a4b608d875a61656fd0192acb30288be9d07e54f95c21bbe60": {
        "Name": "myk8s-control-plane",
        "EndpointID": "f3e6da308de04ef87206ddb53575c9bc74f15e64bddd32a749fa9d7c044b35c0",
        "MacAddress": "3e:ea:44:2e:d6:d2",
        "IPv4Address": "172.18.0.2/16",
        "IPv6Address": "fc00:f853:ccd:e793::2/64"
      }
    },
    "Options": {
      "com.docker.network.bridge.enable_ip_masquerade": "true",
      "com.docker.network.driver.mtu": "65535"
    },
    "Labels": {}
  }
]

# k8s api 주소 확인 : 어떻게 로컬에서 접속이 되는 걸까?
$ kubectl cluster-info
Kubernetes control plane is running at https://127.0.0.1:50593
CoreDNS is running at https://127.0.0.1:50593/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

# 노드 정보 확인 : CRI 는 containerd 사용
$ kubectl get node -o wide
NAME                  STATUS   ROLES           AGE     VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE                         KERNEL-VERSION     CONTAINER-RUNTIME
myk8s-control-plane   Ready    control-plane   2m29s   v1.32.2   172.18.0.2    <none>        Debian GNU/Linux 12 (bookworm)   6.10.14-linuxkit   containerd://2.0.3

# 파드 정보 확인 : CNI 는 kindnet 사용
$ kubectl get pod -A -o wide
NAMESPACE            NAME                                          READY   STATUS    RESTARTS   AGE     IP           NODE                  NOMINATED NODE   READINESS GATES
kube-system          coredns-668d6bf9bc-892kl                      1/1     Running   0          2m48s   10.244.0.2   myk8s-control-plane   <none>           <none>
kube-system          coredns-668d6bf9bc-fb48v                      1/1     Running   0          2m48s   10.244.0.4   myk8s-control-plane   <none>           <none>
kube-system          etcd-myk8s-control-plane                      1/1     Running   0          2m55s   172.18.0.2   myk8s-control-plane   <none>           <none>
kube-system          kindnet-z64s9                                 1/1     Running   0          2m48s   172.18.0.2   myk8s-control-plane   <none>           <none>
kube-system          kube-apiserver-myk8s-control-plane            1/1     Running   0          2m55s   172.18.0.2   myk8s-control-plane   <none>           <none>
kube-system          kube-controller-manager-myk8s-control-plane   1/1     Running   0          2m53s   172.18.0.2   myk8s-control-plane   <none>           <none>
kube-system          kube-proxy-7rzjh                              1/1     Running   0          2m48s   172.18.0.2   myk8s-control-plane   <none>           <none>
kube-system          kube-scheduler-myk8s-control-plane            1/1     Running   0          2m55s   172.18.0.2   myk8s-control-plane   <none>           <none>
local-path-storage   local-path-provisioner-7dc846544d-7q5l6       1/1     Running   0          2m48s   10.244.0.3   myk8s-control-plane   <none>           <none>

# 네임스페이스 확인 >> 도커 컨테이너에서 배운 네임스페이스와 다릅니다!
$ kubectl get namespaces
NAME                 STATUS   AGE
default              Active   3m19s
kube-node-lease      Active   3m18s
kube-public          Active   3m19s
kube-system          Active   3m19s
local-path-storage   Active   3m15s

# 컨트롤플레인노드(컨테이너) 확인 : 도커 컨테이너 이름은 myk8s-control-plane
$ docker ps
CONTAINER ID   IMAGE                  COMMAND                   CREATED         STATUS         PORTS                                                             NAMES
b20ffea79298   kindest/node:v1.32.2   "/usr/local/bin/entr…"   3 minutes ago   Up 3 minutes   0.0.0.0:30000-30003->30000-30003/tcp, 127.0.0.1:50593->6443/tcp   myk8s-control-plane

$ docker images
REPOSITORY                    TAG        IMAGE ID       CREATED         SIZE
kindest/node                  v1.32.2    142f543559cc   4 weeks ago     1.5GB
kindest/node                  <none>     f226345927d7   7 weeks ago     1.5GB
gcr.io/k8s-minikube/kicbase   v0.0.45    7c93b02056db   7 months ago    1.67GB
gcr.io/k8s-minikube/kicbase   <none>     81df28859520   7 months ago    1.67GB
kindest/node                  v1.23.17   14d0a9a892b9   13 months ago   1.31GB

$ docker exec -it myk8s-control-plane ss -tnlp
State                Recv-Q               Send-Q                             Local Address:Port                              Peer Address:Port              Process
LISTEN               0                    4096                                   127.0.0.1:10248                                  0.0.0.0:*                  users:(("kubelet",pid=673,fd=22))
LISTEN               0                    4096                                  127.0.0.11:35265                                  0.0.0.0:*
LISTEN               0                    4096                                   127.0.0.1:2379                                   0.0.0.0:*                  users:(("etcd",pid=615,fd=9))
LISTEN               0                    4096                                  172.18.0.2:2380                                   0.0.0.0:*                  users:(("etcd",pid=615,fd=7))
LISTEN               0                    4096                                  172.18.0.2:2379                                   0.0.0.0:*                  users:(("etcd",pid=615,fd=8))
LISTEN               0                    4096                                   127.0.0.1:36009                                  0.0.0.0:*                  users:(("containerd",pid=105,fd=11))
LISTEN               0                    4096                                           *:2381                                         *:*                  users:(("etcd",pid=615,fd=13))
LISTEN               0                    4096                                           *:10250                                        *:*                  users:(("kubelet",pid=673,fd=19))
LISTEN               0                    4096                                           *:10249                                        *:*                  users:(("kube-proxy",pid=898,fd=21))
LISTEN               0                    4096                                           *:10259                                        *:*                  users:(("kube-scheduler",pid=503,fd=3))
LISTEN               0                    4096                                           *:10257                                        *:*                  users:(("kube-controller",pid=539,fd=3))
LISTEN               0                    4096                                           *:10256                                        *:*                  users:(("kube-proxy",pid=898,fd=9))
LISTEN               0                    4096                                           *:6443                                         *:*                  users:(("kube-apiserver",pid=533,fd=3))

# 디버그용 내용 출력에 ~/.kube/config 권한 인증 로드
$ kubectl get pod -v6
I0408 20:25:47.930544   72014 loader.go:395] Config loaded from file:  /Users/******/.kube/config
I0408 20:25:47.949372   72014 round_trippers.go:553] GET https://127.0.0.1:50593/api/v1/namespaces/default/pods?limit=500 200 OK in 12 milliseconds
No resources found in default namespace.

# kube config 파일 확인
cat $KUBECONFIG
ls -l $KUBECONFIG
```

### kube-ops-view

```bash
# kube-ops-view
# helm show values geek-cookbook/kube-ops-view
$ helm repo add geek-cookbook https://geek-cookbook.github.io/charts/
helm install kube-ops-view geek-cookbook/kube-ops-view --version 1.2.2 --set service.main.type=NodePort,service.main.ports.http.nodePort=30000 --set env.TZ="Asia/Seoul" --namespace kube-system
"geek-cookbook" already exists with the same configuration, skipping
NAME: kube-ops-view
LAST DEPLOYED: Tue Apr  8 20:26:32 2025
NAMESPACE: kube-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
1. Get the application URL by running these commands:
  export NODE_PORT=$(kubectl get --namespace kube-system -o jsonpath="{.spec.ports[0].nodePort}" services kube-ops-view)
  export NODE_IP=$(kubectl get nodes --namespace kube-system -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT

# 설치 확인
$ kubectl get deploy,pod,svc,ep -n kube-system -l app.kubernetes.io/instance=kube-ops-view
NAME                            READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kube-ops-view   1/1     1            1           59s

NAME                                 READY   STATUS    RESTARTS   AGE
pod/kube-ops-view-6658c477d4-krv4n   1/1     Running   0          59s

NAME                    TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
service/kube-ops-view   NodePort   10.96.47.104   <none>        8080:30000/TCP   59s

NAME                      ENDPOINTS         AGE
endpoints/kube-ops-view   10.244.0.5:8080   59s

# kube-ops-view 접속 URL 확인 (2 배율)
$ open "http://127.0.0.1:30000/#scale=2"
```

![]({{ site.url }}/img/post/devops/study/istio/1/8.png)

#### 클러스터 삭제

```bash
# 클러스터 삭제
kind delete cluster --name myk8s
docker ps
cat $KUBECONFIG
unset KUBECONFIG
```

## 실습!!

### 실습 환경 준비

```bash
#
git clone https://github.com/AcornPublishing/istio-in-action
cd istio-in-action/book-source-code-master

#
kind create cluster --name myk8s --image kindest/node:v1.23.17 --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30000 # Sample Application (istio-ingrssgateway)
    hostPort: 30000
  - containerPort: 30001 # Prometheus
    hostPort: 30001
  - containerPort: 30002 # Grafana
    hostPort: 30002
  - containerPort: 30003 # Kiali
    hostPort: 30003
  - containerPort: 30004 # Tracing
    hostPort: 30004
  - containerPort: 30005 # kube-ops-view
    hostPort: 30005
  extraMounts:
  - hostPath: /... # 각자 자신의 pwd 경로로 설정
    containerPath: /istiobook
networking:
  podSubnet: 10.10.0.0/16
  serviceSubnet: 10.200.1.0/24
EOF

# 설치 확인
docker ps

# 노드에 기본 툴 설치
docker exec -it myk8s-control-plane sh -c 'apt update && apt install tree psmisc lsof wget bridge-utils net-tools dnsutils tcpdump ngrep iputils-ping git vim -y'


# (옵션) kube-ops-view
helm repo add geek-cookbook https://geek-cookbook.github.io/charts/
helm install kube-ops-view geek-cookbook/kube-ops-view --version 1.2.2 --set service.main.type=NodePort,service.main.ports.http.nodePort=30005 --set env.TZ="Asia/Seoul" --namespace kube-system
kubectl get deploy,pod,svc,ep -n kube-system -l app.kubernetes.io/instance=kube-ops-view

## kube-ops-view 접속 URL 확인
open "http://localhost:30005/#scale=1.5"
open "http://localhost:30005/#scale=1.3"

# (옵션) metrics-server
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm install metrics-server metrics-server/metrics-server --set 'args[0]=--kubelet-insecure-tls' -n kube-system
kubectl get all -n kube-system -l app.kubernetes.io/instance=metrics-server
```

### 2.2 이스티오 컨트롤 플레인 알아보기

- ref
  - [Docs](https://istio.io/v1.17/docs/)
  - [Install](https://istio.io/v1.17/docs/setup/install/istioctl/)
  - [profile](https://istio.io/v1.17/docs/setup/additional-setup/config-profiles/)

```bash
# myk8s-control-plane 진입 후 설치 진행
docker exec -it myk8s-control-plane bash
-----------------------------------
# 코드 파일들 마운트 확인
$ tree /istiobook/ -L 1
/istiobook/
|-- README.md
|-- appendices
|-- bin
|-- ch10
|-- ch11
|-- ch12
|-- ch13
|-- ch14
|-- ch2
|-- ch3
|-- ch4
|-- ch5
|-- ch6
|-- ch7
|-- ch8
|-- ch9
`-- services

# istioctl 설치
$ export ISTIOV=1.17.8
$ echo 'export ISTIOV=1.17.8' >> /root/.bashrc

$ curl -s -L https://istio.io/downloadIstio | ISTIO_VERSION=$ISTIOV sh -
$ tree istio-$ISTIOV -L 2 # sample yaml 포함
istio-1.17.8
|-- LICENSE
|-- README.md
|-- bin
|   `-- istioctl
|-- manifest.yaml
|-- manifests
|   |-- charts
|   |-- examples
|   `-- profiles
|-- samples
|   |-- README.md
|   |-- addons
|   |-- bookinfo
|   |-- certs
|   |-- cicd
|   |-- custom-bootstrap
|   |-- extauthz
|   |-- external
|   |-- grpc-echo
|   |-- health-check
|   |-- helloworld
|   |-- httpbin
|   |-- jwt-server
|   |-- kind-lb
|   |-- multicluster
|   |-- open-telemetry
|   |-- operator
|   |-- ratelimit
|   |-- security
|   |-- sleep
|   |-- tcp-echo
|   |-- wasm_modules
|   `-- websockets
`-- tools
    |-- _istioctl
    |-- certs
    `-- istioctl.bash

$ cp istio-$ISTIOV/bin/istioctl /usr/local/bin/istioctl
$ istioctl version --remote=false
1.17.8

# default 프로파일 컨트롤 플레인 배포
$ istioctl x precheck # 설치 전 k8s 조건 충족 검사
✔ No issues found when checking the cluster. Istio is safe to install or upgrade!
  To get started, check out https://istio.io/latest/docs/setup/getting-started/

$ istioctl profile list
Istio configuration profiles:
    ambient
    default
    demo
    empty
    external
    minimal
    openshift
    preview
    remote

$ istioctl install --set profile=default -y
✔ Istio core installed
✔ Istiod installed
✔ Ingress gateways installed
✔ Installation complete

# 설치 확인 : istiod, istio-ingressgateway, crd 등
$ kubectl get all,svc,ep,sa,cm,secret,pdb -n istio-system
...
NAME                                    READY   STATUS              RESTARTS   AGE
istio-ingressgateway-58888b4f9b-gv7r9   1/1     Running             0          2m43s
istiod-78c465d86b-tsd8l                 1/1     Running             0          3m
...

$ kubectl get crd | grep istio.io | sort
authorizationpolicies.security.istio.io    2025-04-08T11:35:47Z
destinationrules.networking.istio.io       2025-04-08T11:35:47Z
envoyfilters.networking.istio.io           2025-04-08T11:35:47Z
gateways.networking.istio.io               2025-04-08T11:35:47Z
istiooperators.install.istio.io            2025-04-08T11:35:47Z
peerauthentications.security.istio.io      2025-04-08T11:35:47Z
proxyconfigs.networking.istio.io           2025-04-08T11:35:47Z
requestauthentications.security.istio.io   2025-04-08T11:35:47Z
serviceentries.networking.istio.io         2025-04-08T11:35:47Z
sidecars.networking.istio.io               2025-04-08T11:35:47Z
telemetries.telemetry.istio.io             2025-04-08T11:35:47Z
virtualservices.networking.istio.io        2025-04-08T11:35:47Z
wasmplugins.extensions.istio.io            2025-04-08T11:35:47Z
workloadentries.networking.istio.io        2025-04-08T11:35:47Z
workloadgroups.networking.istio.io         2025-04-08T11:35:47Z

$ istioctl verify-install # 설치 확인
...
Checked 15 custom resource definitions
Checked 2 Istio Deployments
✔ Istio is installed and verified successfully

# 보조 도구 설치
$ kubectl apply -f istio-$ISTIOV/samples/addons

#
kubectl get pod -n istio-system
NAME                                    READY   STATUS    RESTARTS   AGE
grafana-b854c6c8-hmg6f                 1/1     Running   0          72s
istio-ingressgateway-996bc6bb6-hgfzp   1/1     Running   0          2m34s
istiod-7df6ffc78d-4r28x                1/1     Running   0          2m48s
jaeger-5556cd8fcf-pkbdf                1/1     Running   0          72s
kiali-648847c8c4-zf9lx                 1/1     Running   0          72s
prometheus-7b8b9dd44c-mmn8p            2/2     Running   0          72s

# 빠져나오기
exit
-----------------------------------

#
$ kubectl get cm -n istio-system istio -o yaml
apiVersion: v1
data:
  mesh: |-
    defaultConfig:
      discoveryAddress: istiod.istio-system.svc:15012
      proxyMetadata: {}
      tracing:
        zipkin:
          address: zipkin.istio-system:9411
    enablePrometheusMerge: true
    rootNamespace: istio-system
    trustDomain: cluster.local
  meshNetworks: 'networks: {}'
kind: ConfigMap
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","data":{"mesh":"defaultConfig:\n  discoveryAddress: istiod.istio-system.svc:15012\n  proxyMetadata: {}\n  tracing:\n    zipkin:\n      address: zipkin.istio-system:9411\nenablePrometheusMerge: true\nrootNamespace: istio-system\ntrustDomain: cluster.local","meshNetworks":"networks: {}"},"kind":"ConfigMap","metadata":{"annotations":{},"labels":{"install.operator.istio.io/owning-resource":"unknown","install.operator.istio.io/owning-resource-namespace":"istio-system","istio.io/rev":"default","operator.istio.io/component":"Pilot","operator.istio.io/managed":"Reconcile","operator.istio.io/version":"1.17.8","release":"istio"},"name":"istio","namespace":"istio-system"}}
  creationTimestamp: "2025-04-08T11:35:47Z"
  labels:
    install.operator.istio.io/owning-resource: unknown
    install.operator.istio.io/owning-resource-namespace: istio-system
    istio.io/rev: default
    operator.istio.io/component: Pilot
    operator.istio.io/managed: Reconcile
    operator.istio.io/version: 1.17.8
    release: istio
  name: istio
  namespace: istio-system
  resourceVersion: "1056"
  uid: c316f813-0e90-44c4-bdd8-871141f93e64

## install neast
$ kubectl krew install neat
$ export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"

$ kubectl get cm -n istio-system istio -o yaml | kubectl neat
apiVersion: v1
data:
  mesh: |-
    defaultConfig:
      discoveryAddress: istiod.istio-system.svc:15012
      proxyMetadata: {}
      tracing:
        zipkin:
          address: zipkin.istio-system:9411
    enablePrometheusMerge: true
    rootNamespace: istio-system
    trustDomain: cluster.local
  meshNetworks: 'networks: {}'
kind: ConfigMap
metadata:
  labels:
    install.operator.istio.io/owning-resource: unknown
    install.operator.istio.io/owning-resource-namespace: istio-system
    istio.io/rev: default
    operator.istio.io/component: Pilot
    operator.istio.io/managed: Reconcile
    operator.istio.io/version: 1.17.8
    release: istio
  name: istio
  namespace: istio-system
```

![]({{ site.url }}/img/post/devops/study/istio/1/9.png)
![]({{ site.url }}/img/post/devops/study/istio/1/10.png)

![]({{ site.url }}/img/post/devops/study/istio/1/11.png)

### 2.3 서비스 메시에 첫 애플리케이션 배포해보기

```bash
#
$ kubectl create ns istioinaction
namespace/istioinaction created

# 방법1 : yaml에 sidecar 설정을 추가
cat services/catalog/kubernetes/catalog.yaml
docker exec -it myk8s-control-plane istioctl kube-inject -f /istiobook/services/catalog/kubernetes/catalog.yaml
...
  - args:
        - proxy
        - sidecar
        - --domain
        - $(POD_NAMESPACE).svc.cluster.local
        - --proxyLogLevel=warning
        - --proxyComponentLogLevel=misc:error
        - --log_output_level=default:info
        - --concurrency
        - "2"
        env:
        - name: JWT_POLICY
          value: third-party-jwt
        - name: PILOT_CERT_PROVIDER
          value: istiod
        - name: CA_ADDR
          value: istiod.istio-system.svc:15012
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
  ...
        image: docker.io/istio/proxyv2:1.13.0
        name: istio-proxy


# 방법2 : namespace에 레이블을 추가하면 istiod (오퍼레이터)가 해당 namepsace의 pod spec에 자동으로 sidecar 설정을 주입
$ kubectl label namespace istioinaction istio-injection=enabled
namespace/istioinaction labeled

$ kubectl get ns --show-labels
NAME                 STATUS   AGE     LABELS
default              Active   12m     kubernetes.io/metadata.name=default
...
istioinaction        Active   67s     istio-injection=enabled,kubernetes.io/metadata.name=istioinaction
...

#
$ kubectl get mutatingwebhookconfiguration
NAME                         WEBHOOKS   AGE
istio-revision-tag-default   4          7m59s # 특정 revision의 사이드카 주입 설정 관리
istio-sidecar-injector       4          8m25s # Istio는 각 애플리케이션 Pod에 Envoy 사이드카 프록시를 자동으로 주입
                                              ## 네임스페이스나 Pod에 istio-injection=enabled 라벨이 있어야 작동

$ kubectl get mutatingwebhookconfiguration istio-sidecar-injector -o yaml

#
$ kubectl get cm -n istio-system istio-sidecar-injector -o yaml | kubectl neat

```

![]({{ site.url }}/img/post/devops/study/istio/1/12.png)

```bash
#
$ cat services/catalog/kubernetes/catalog.yaml
$ kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction
serviceaccount/catalog created
service/catalog created
deployment.apps/catalog created

$ cat services/webapp/kubernetes/webapp.yaml
$ kubectl apply -f services/webapp/kubernetes/webapp.yaml -n istioinaction
serviceaccount/webapp created
service/webapp created
deployment.apps/webapp created

#
$ kubectl get pod -n istioinaction
NAME                     READY   STATUS    RESTARTS   AGE
catalog-6cf4b97d-qx8ln   2/2     Running   0          38s
webapp-7685bcb84-jkf25   2/2     Running   0          17s

# 접속 테스트용 netshoot 파드 생성
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: netshoot
spec:
  containers:
  - name: netshoot
    image: nicolaka/netshoot
    command: ["tail"]
    args: ["-f", "/dev/null"]
  terminationGracePeriodSeconds: 0
EOF

# catalog 접속 확인
kubectl exec -it netshoot -- curl -s http://catalog.istioinaction/items/1 | jq
{
  "id": 1,
  "color": "amber",
  "department": "Eyewear",
  "name": "Elinor Glasses",
  "price": "282.00"
}

# webapp 접속 확인
kubectl exec -it netshoot -- curl -s http://webapp.istioinaction/api/catalog/items/1 | jq
{
  "id": 1,
  "color": "amber",
  "department": "Eyewear",
  "name": "Elinor Glasses",
  "price": "282.00"
}

```

![]({{ site.url }}/img/post/devops/study/istio/1/13.png)

```bash
# 아래 방법 대신 임시 사용
kubectl port-forward -n istioinaction deploy/webapp 8080:8080
확인 후 CTRL+C 로 종료

#
open http://localhost:8080
```

![]({{ site.url }}/img/post/devops/study/istio/1/14.png)

![]({{ site.url }}/img/post/devops/study/istio/1/15.png)

### 2.4 복원력, 관찰 가능성, 트래픽 제어 기능을 갖춘 이스티오의 능력 살펴보기

![]({{ site.url }}/img/post/devops/study/istio/1/16.png)

```bash
# istioctl proxy-status : 단축어 ps
$ docker exec -it myk8s-control-plane istioctl proxy-status
NAME                                                  CLUSTER        CDS        LDS        EDS        RDS          ECDS         ISTIOD                      VERSION
catalog-6cf4b97d-qx8ln.istioinaction                  Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED       NOT SENT     istiod-7df6ffc78d-4r28x     1.17.8
istio-ingressgateway-996bc6bb6-hgfzp.istio-system     Kubernetes     SYNCED     SYNCED     SYNCED     NOT SENT     NOT SENT     istiod-7df6ffc78d-4r28x     1.17.8
webapp-7685bcb84-jkf25.istioinaction                  Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED       NOT SENT     istiod-7df6ffc78d-4r28x     1.17.8

$ docker exec -it myk8s-control-plane istioctl ps
NAME                                                  CLUSTER        CDS        LDS        EDS        RDS          ECDS         ISTIOD                      VERSION
catalog-6cf4b97d-qx8ln.istioinaction                  Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED       NOT SENT     istiod-7df6ffc78d-4r28x     1.17.8
istio-ingressgateway-996bc6bb6-hgfzp.istio-system     Kubernetes     SYNCED     SYNCED     SYNCED     NOT SENT     NOT SENT     istiod-7df6ffc78d-4r28x     1.17.8
webapp-7685bcb84-jkf25.istioinaction                  Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED       NOT SENT     istiod-7df6ffc78d-4r28x     1.17.8

#
$ cat ch2/ingress-gateway.yaml
$ cat <<EOF | kubectl -n istioinaction apply -f -
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: outfitters-gateway
  namespace: istioinaction
spec:
  selector:
    istio: ingressgateway # use istio default controller
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "*"
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: webapp-virtualservice
  namespace: istioinaction
spec:
  hosts:
  - "*"
  gateways:
  - outfitters-gateway
  http:
  - route:
    - destination:
        host: webapp
        port:
          number: 80
EOF

#
$ kubectl get gw,vs -n istioinaction
NAME                                             AGE
gateway.networking.istio.io/outfitters-gateway   17s

NAME                                                       GATEWAYS                 HOSTS   AGE
virtualservice.networking.istio.io/webapp-virtualservice   ["outfitters-gateway"]   ["*"]   17s


# istioctl proxy-status : 단축어 ps
$ docker exec -it myk8s-control-plane istioctl proxy-status
NAME                                                  CLUSTER        CDS        LDS        EDS        RDS        ECDS         ISTIOD                      VERSION
catalog-6cf4b97d-qx8ln.istioinaction                  Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-4r28x     1.17.8
istio-ingressgateway-996bc6bb6-hgfzp.istio-system     Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-4r28x     1.17.8
webapp-7685bcb84-jkf25.istioinaction                  Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-4r28x     1.17.8

ISTIOIGW=istio-ingressgateway-996bc6bb6-hgfzp.istio-system
WEBAPP=webapp-7685bcb84-jkf25.istioinaction

# istioctl proxy-config : 단축어 pc
docker exec -it myk8s-control-plane istioctl proxy-config all $ISTIOIGW
docker exec -it myk8s-control-plane istioctl proxy-config all $WEBAPP

docker exec -it myk8s-control-plane istioctl proxy-config listener $ISTIOIGW
docker exec -it myk8s-control-plane istioctl proxy-config route $ISTIOIGW
docker exec -it myk8s-control-plane istioctl proxy-config cluster $ISTIOIGW
docker exec -it myk8s-control-plane istioctl proxy-config endpoint $ISTIOIGW
docker exec -it myk8s-control-plane istioctl proxy-config log $ISTIOIGW

docker exec -it myk8s-control-plane istioctl proxy-config listener $WEBAPP
docker exec -it myk8s-control-plane istioctl proxy-config route $WEBAPP
docker exec -it myk8s-control-plane istioctl proxy-config cluster $WEBAPP
docker exec -it myk8s-control-plane istioctl proxy-config endpoint $WEBAPP
docker exec -it myk8s-control-plane istioctl proxy-config log $WEBAPP

# envoy 가 사용하고 있는 인증서 정보 확인
docker exec -it myk8s-control-plane istioctl proxy-config secret $ISTIOIGW
docker exec -it myk8s-control-plane istioctl proxy-config secret $WEBAPP


#
$ docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system
NAME          DOMAINS     MATCH                  VIRTUAL SERVICE
http.8080     *           /*                     webapp-virtualservice.istioinaction
              *           /healthz/ready*
              *           /stats/prometheus*


# istio-ingressgateway 서비스 NodePort 변경 및 nodeport 30000로 지정 변경
$ kubectl get svc,ep -n istio-system istio-ingressgateway
NAME                           TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                                      AGE
service/istio-ingressgateway   LoadBalancer   10.200.1.232   <pending>     15021:30243/TCP,80:31244/TCP,443:30816/TCP   24m

NAME                             ENDPOINTS                                       AGE
endpoints/istio-ingressgateway   10.10.0.8:15021,10.10.0.8:8080,10.10.0.8:8443   24m

$ kubectl patch svc -n istio-system istio-ingressgateway -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 8080, "nodePort": 30000}]}}'
service/istio-ingressgateway patched

$ kubectl get svc -n istio-system istio-ingressgateway
NAME                   TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)                                      AGE
istio-ingressgateway   NodePort   10.200.1.232   <none>        15021:30243/TCP,80:30000/TCP,443:30816/TCP   24m

# istio-ingressgateway 서비스 externalTrafficPolicy 설정 : ClientIP 수집 확인
$ kubectl patch svc -n istio-system istio-ingressgateway -p '{"spec":{"externalTrafficPolicy": "Local"}}'
service/istio-ingressgateway patched

$ kubectl describe svc -n istio-system istio-ingressgateway
...
External Traffic Policy:  Local

#
$ kubectl stern -l app=webapp -n istioinaction
$ kubectl stern -l app=catalog -n istioinaction

#
$ curl -s http://127.0.0.1:30000/api/catalog | jq
[
  {
    "id": 1,
    "color": "amber",
    "department": "Eyewear",
    "name": "Elinor Glasses",
    "price": "282.00"
  },
  {
    "id": 2,
    "color": "cyan",
    "department": "Clothing",
    "name": "Atlas Shirt",
    "price": "127.00"
  },
  {
    "id": 3,
    "color": "teal",
    "department": "Clothing",
    "name": "Small Metal Shoes",
    "price": "232.00"
  },
  {
    "id": 4,
    "color": "red",
    "department": "Watches",
    "name": "Red Dragon Watch",
    "price": "232.00"
  }
]

$ curl -s http://127.0.0.1:30000/api/catalog/items/1 | jq
{
  "id": 1,
  "color": "amber",
  "department": "Eyewear",
  "name": "Elinor Glasses",
  "price": "282.00"
}

$ curl -s http://127.0.0.1:30000/api/catalog -I | head -n 1
HTTP/1.1 200 OK

# webapp 반복 호출
while true; do curl -s http://127.0.0.1:30000/api/catalog/items/1 ; sleep 1; echo; done
while true; do curl -s http://127.0.0.1:30000/api/catalog -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done
while true; do curl -s http://127.0.0.1:30000/api/catalog -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 0.5; echo; done

```

#### 2.4.1 이스티오 관찰 가능성

```bash
# NodePort 변경 및 nodeport 30001~30003으로 변경 : prometheus(30001), grafana(30002), kiali(30003), tracing(30004)
$ kubectl patch svc -n istio-system prometheus -p '{"spec": {"type": "NodePort", "ports": [{"port": 9090, "targetPort": 9090, "nodePort": 30001}]}}'
$ kubectl patch svc -n istio-system grafana -p '{"spec": {"type": "NodePort", "ports": [{"port": 3000, "targetPort": 3000, "nodePort": 30002}]}}'
$ kubectl patch svc -n istio-system kiali -p '{"spec": {"type": "NodePort", "ports": [{"port": 20001, "targetPort": 20001, "nodePort": 30003}]}}'
$ kubectl patch svc -n istio-system tracing -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 16686, "nodePort": 30004}]}}'
service/prometheus patched
service/grafana patched
service/kiali patched
service/tracing patched

# Prometheus 접속 : envoy, istio 메트릭 확인
open http://127.0.0.1:30001

# Grafana 접속
open http://127.0.0.1:30002

# Kiali 접속 1 : NodePort
open http://127.0.0.1:30003

# (옵션) Kiali 접속 2 : Port forward
kubectl port-forward deployment/kiali -n istio-system 20001:20001 &
open http://127.0.0.1:20001

# tracing 접속 : 예거 트레이싱 대시보드
open http://127.0.0.1:30004
```

그라파나 확인: 대시보드 - Istio Service Dashboard -> 상단 Service(webapp 선택)
트래픽 반복 접속 해둥 상태
![]({{ site.url }}/img/post/devops/study/istio/1/17.png)

오픈 트레이싱을 통한 분산 트레이싱: Jaeger 트레이싱 대시보드 확인
![]({{ site.url }}/img/post/devops/study/istio/1/18.png)

Kiali 확인

- Namespace를 istioinaction으로 선택 후 Graph(Traffic, Versioned app graph)에서 Display 옵션 중 'Traffic Distribution', 'Traffic Animation' 활성화!
- Service nodes, Security 체크(last 1m, Evety 10s)
  ![]({{ site.url }}/img/post/devops/study/istio/1/19.png)

#### 2.4.2 복원력을 위한 이스티오

catalog에 의도적으로 500 에러를 재현하고 retry로 복원력 높이기
먄약 '간혈적/일시전 네트워크 오류'가 발생하여 webapp은 catalog 요청이 실패하는 경우, 애플리케이션 코드 수정 없이 복원력을 높여보자!

```bash
# bin/chaos.sh {error code} {frequency}
#!/usr/bin/env bash

if [ $1 == "500" ]; then

    POD=$(kubectl get pod | grep catalog | awk '{ print $1 }')
    echo $POD

    for p in $POD; do
        if [ ${2:-"false"} == "delete" ]; then
            echo "Deleting 500 rule from $p"
            kubectl exec -c catalog -it $p -- curl  -X POST -H "Content-Type: application/json" -d '{"active":
        false,  "type": "500"}' localhost:3000/blowup
        else
            PERCENTAGE=${2:-100}
            kubectl exec -c catalog -it $p -- curl  -X POST -H "Content-Type: application/json" -d '{"active":
            true,  "type": "500",  "percentage": '"${PERCENTAGE}"'}' localhost:3000/blowup
            echo ""
        fi
    done


fi
```

```bash
#
$ docker exec -it myk8s-control-plane bash
----------------------------------------
# istioinaction 로 네임스페이스 변경
$ cat /etc/kubernetes/admin.conf
$ kubectl config set-context $(kubectl config current-context) --namespace=istioinaction
Context "kubernetes-admin@myk8s" modified.
$ cat /etc/kubernetes/admin.conf

$ cd /istiobook/bin/
$ chmod +x chaos.sh
$ ./chaos.sh 500 100 # 모니터링 : kiali, grafana, tracing
catalog-6cf4b97d-qx8ln
blowups=[object Object]

$ ./chaos.sh 500 50 # 모니터링 : kiali, grafana, tracing
catalog-6cf4b97d-qx8ln
blowups=[object Object]

kubectl config set-context $(kubectl config current-context) --namespace=default
cat /etc/kubernetes/admin.conf
----------------------------------------

```

`./chaos.sh 500 100`
![]({{ site.url }}/img/post/devops/study/istio/1/20.png)
![]({{ site.url }}/img/post/devops/study/istio/1/21.png)
![]({{ site.url }}/img/post/devops/study/istio/1/22.png)

`./chaos.sh 500 50`
![]({{ site.url }}/img/post/devops/study/istio/1/23.png)
![]({{ site.url }}/img/post/devops/study/istio/1/24.png)

![]({{ site.url }}/img/post/devops/study/istio/1/25.png)

![]({{ site.url }}/img/post/devops/study/istio/1/26.png)
![]({{ site.url }}/img/post/devops/study/istio/1/27.png)

에러 발생 시 reslience 하게 retry 하도록 애플리케이션 코드 수정 없이 해보기!
Resiliency하게 해보자 -> Proxy(envoy)에 endpoint(catalog) 5xx 에러시 retry 적용

```bash
(on myk8s-control-plane)
# catalog 3번까지 요청 재시도 할 수 있고, 각 시도에는 2초의 제한 시간이 있음.
$ cat <<EOF | kubectl -n istioinaction apply -f -
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog
spec:
  hosts:
  - catalog
  http:
  - route:
    - destination:
        host: catalog
    retries:
      attempts: 3
      retryOn: 5xx
      perTryTimeout: 2s
EOF

$ kubectl get vs -n istioinaction
NAME                    GATEWAYS                 HOSTS         AGE
catalog                                          ["catalog"]   55s
webapp-virtualservice   ["outfitters-gateway"]   ["*"]         43m
```

결과적으로 client에 응답 성공률이 높아졌다!

그라파나(Istio Mesh Dashboard): retry 적용 후 Success Rate은 증가하고, 5xx 에러는 감소하는 것을 확인
![]({{ site.url }}/img/post/devops/study/istio/1/28.png)
![]({{ site.url }}/img/post/devops/study/istio/1/29.png)
![]({{ site.url }}/img/post/devops/study/istio/1/30.png)

#### 2.4.3 트래픽 라우팅을 위한 이스티오

특정 사용자 그룹만 타겟으로 새 버전을 라우팅하고, 릴리즈에 단계적 접근: catalog v2에 imageUrl 핃드 추가

```bash
(x myk8s-control-plane)
# catalog v2 배포
$ cat <<EOF | kubectl -n istioinaction apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: catalog
    version: v2
  name: catalog-v2
spec:
  replicas: 1
  selector:
    matchLabels:
      app: catalog
      version: v2
  template:
    metadata:
      labels:
        app: catalog
        version: v2
    spec:
      containers:
      - env:
        - name: KUBERNETES_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        - name: SHOW_IMAGE
          value: "true"
        image: istioinaction/catalog:latest
        imagePullPolicy: IfNotPresent
        name: catalog
        ports:
        - containerPort: 3000
          name: http
          protocol: TCP
        securityContext:
          privileged: false
EOF

# (옵션) 500 에러 발생 꺼두기
$ docker exec -it myk8s-control-plane bash
----------------------------------------
$ cd /istiobook/bin/
$ ./chaos.sh 500 delete
catalog-6cf4b97d-qx8ln catalog-v2-6df885b555-kqgrx
Deleting 500 rule from catalog-6cf4b97d-qx8ln
blowups=[object Object]Deleting 500 rule from catalog-v2-6df885b555-kqgrx
blowups=[object Object]root@myk8s-control-plane:/istiobook/bin# exit
$ exit
----------------------------------------

#
$ kubectl get deploy,pod,svc,ep -n istioinaction
NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/catalog      1/1     1            1           59m
deployment.apps/catalog-v2   1/1     1            1           2m42s
deployment.apps/webapp       1/1     1            1           59m

NAME                              READY   STATUS    RESTARTS   AGE
pod/catalog-6cf4b97d-qx8ln        2/2     Running   0          59m
pod/catalog-v2-6df885b555-kqgrx   2/2     Running   0          2m42s
pod/webapp-7685bcb84-jkf25        2/2     Running   0          59m

NAME              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/catalog   ClusterIP   10.200.1.181   <none>        80/TCP    59m
service/webapp    ClusterIP   10.200.1.190   <none>        80/TCP    59m

NAME                ENDPOINTS                         AGE
endpoints/catalog   10.10.0.13:3000,10.10.0.16:3000   59m
endpoints/webapp    10.10.0.14:8080                   59m

$ kubectl get gw,vs -n istioinaction
NAME                                             AGE
gateway.networking.istio.io/outfitters-gateway   54m

NAME                                                       GATEWAYS                 HOSTS         AGE
virtualservice.networking.istio.io/catalog                                          ["catalog"]   12m
virtualservice.networking.istio.io/webapp-virtualservice   ["outfitters-gateway"]   ["*"]         54m

# 반복 접속 종료해두기
```

![]({{ site.url }}/img/post/devops/study/istio/1/31.png)
![]({{ site.url }}/img/post/devops/study/istio/1/32.png)
![]({{ site.url }}/img/post/devops/study/istio/1/33.png)

![]({{ site.url }}/img/post/devops/study/istio/1/34.png)

v1만 접속 설정

```bash
#
$ cat <<EOF | kubectl -n istioinaction apply -f -
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: catalog
spec:
  host: catalog
  subsets:
  - name: version-v1
    labels:
      version: v1
  - name: version-v2
    labels:
      version: v2
EOF

#
$ kubectl get gw,vs,dr -n istioinaction
NAME                                             AGE
gateway.networking.istio.io/outfitters-gateway   60m

NAME                                                       GATEWAYS                 HOSTS         AGE
virtualservice.networking.istio.io/catalog                                          ["catalog"]   18m
virtualservice.networking.istio.io/webapp-virtualservice   ["outfitters-gateway"]   ["*"]         60m

NAME                                          HOST      AGE
destinationrule.networking.istio.io/catalog   catalog   9s

# 반복 접속 : v1,v2 분산 접속 확인
while true; do curl -s http://127.0.0.1:30000/api/catalog | jq; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done


# v1 라우팅 VS 수정(업데이트)
$ cat <<EOF | kubectl -n istioinaction apply -f -
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog
spec:
  hosts:
  - catalog
  http:
  - route:
    - destination:
        host: catalog
        subset: version-v1
EOF

# 반복 접속 : v1 접속 확인
while true; do curl -s http://127.0.0.1:30000/api/catalog | jq; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

```

헤더에 따라 라우팅
특정 헤더는 v2, 나머지는 v1 접속 설정

```bash
# 라우팅 VS 수정(업데이트)
cat <<EOF | kubectl -n istioinaction apply -f -
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog
spec:
  hosts:
  - catalog
  http:
  - match:
    - headers:
        x-dark-launch:
          exact: "v2"
    route:
    - destination:
        host: catalog
        subset: version-v2
  - route:
    - destination:
        host: catalog
        subset: version-v1
EOF

#
$ kubectl get gw,vs,dr -n istioinaction
NAME                                             AGE
gateway.networking.istio.io/outfitters-gateway   62m

NAME                                                       GATEWAYS                 HOSTS         AGE
virtualservice.networking.istio.io/catalog                                          ["catalog"]   20m
virtualservice.networking.istio.io/webapp-virtualservice   ["outfitters-gateway"]   ["*"]         62m

NAME                                          HOST      AGE
destinationrule.networking.istio.io/catalog   catalog   99s

# 반복 접속 : v1 접속 확인
$ while true; do curl -s http://127.0.0.1:30000/api/catalog | jq; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done
[
  {
    "id": 1,
    "color": "amber",
    "department": "Eyewear",
    "name": "Elinor Glasses",
    "price": "282.00"
  },
  {
    "id": 2,
    "color": "cyan",
    "department": "Clothing",
    "name": "Atlas Shirt",
    "price": "127.00"
  },
  {
    "id": 3,
    "color": "teal",
    "department": "Clothing",
    "name": "Small Metal Shoes",
    "price": "232.00"
  },
  {
    "id": 4,
    "color": "red",
    "department": "Watches",
    "name": "Red Dragon Watch",
    "price": "232.00"
  }
]

# 반복 접속 : v2 접속 확인
$ while true; do curl -s http://127.0.0.1:30000/api/catalog -H "x-dark-launch: v2" | jq; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done
[
  {
    "id": 1,
    "color": "amber",
    "department": "Eyewear",
    "name": "Elinor Glasses",
    "price": "282.00",
    "imageUrl": "http://lorempixel.com/640/480"
  },
  {
    "id": 2,
    "color": "cyan",
    "department": "Clothing",
    "name": "Atlas Shirt",
    "price": "127.00",
    "imageUrl": "http://lorempixel.com/640/480"
  },
  {
    "id": 3,
    "color": "teal",
    "department": "Clothing",
    "name": "Small Metal Shoes",
    "price": "232.00",
    "imageUrl": "http://lorempixel.com/640/480"
  },
  {
    "id": 4,
    "color": "red",
    "department": "Watches",
    "name": "Red Dragon Watch",
    "price": "232.00",
    "imageUrl": "http://lorempixel.com/640/480"
  }
]

```

#### 실습 완료 후 자원 정리하기

```bash
kubectl delete deploy,svc,gw,vs,dr --all -n istioinaction && kind delete cluster --name myk8s
```

---

시간이 지난만큼 앞으로의 실습은 현시점(25.4.6 기준) 최신 버전으로 진행한다.

- 실습 환경: docker (kind - k8s 1.32.2), istio 1.25.1
- kind

```bash
#
kind create cluster --name myk8s --image kindest/node:v1.32.2 --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  extraPortMappings:
  - containerPort: 30000 # Sample Application
    hostPort: 30000
  - containerPort: 30001 # Prometheus
    hostPort: 30001
  - containerPort: 30002 # Grafana
    hostPort: 30002
  - containerPort: 30003 # Kiali
    hostPort: 30003
  - containerPort: 30004 # Tracing
    hostPort: 30004
  - containerPort: 30005 # kube-ops-view
    hostPort: 30005
networking:
  podSubnet: 10.10.0.0/16
  serviceSubnet: 10.200.1.0/24
EOF

# 설치 확인
docker ps

# 노드에 기본 툴 설치
docker exec -it myk8s-control-plane sh -c 'apt update && apt install tree psmisc lsof wget bridge-utils net-tools dnsutils tcpdump ngrep iputils-ping git vim -y'


# (옵션) kube-ops-view
helm repo add geek-cookbook https://geek-cookbook.github.io/charts/
helm install kube-ops-view geek-cookbook/kube-ops-view --version 1.2.2 --set service.main.type=NodePort,service.main.ports.http.nodePort=30005 --set env.TZ="Asia/Seoul" --namespace kube-system
kubectl get deploy,pod,svc,ep -n kube-system -l app.kubernetes.io/instance=kube-ops-view

## kube-ops-view 접속 URL 확인
open "http://localhost:30005/#scale=1.5"
open "http://localhost:30005/#scale=1.3"

# (옵션) metrics-server
helm repo add metrics-server https://kubernetes-sigs.github.io/metrics-server/
helm install metrics-server metrics-server/metrics-server --set 'args[0]=--kubelet-insecure-tls' -n kube-system
kubectl get all -n kube-system -l app.kubernetes.io/instance=metrics-server
```

```bash
export ISTIOV=1.25.1
curl -s -L https://istio.io/downloadIstio | ISTIO_VERSION=$ISTIOV sh -
cd istio-$ISTIOV

# default 프로파일 배포
cat <<EOF | istioctl install -y -f -
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: demo
  components:
    ingressGateways:
    - name: istio-ingressgateway
      enabled: true
    egressGateways:
    - name: istio-egressgateway
      enabled: false
EOF
```

- addon 설치

```bash
# 설치 확인 : istiod(데몬, 컨트롤플레인), istio-ingressgateway, crd 등
kubectl get all,svc,ep,sa,cm,secret,pdb -n istio-system
kubectl get crd | grep istio.io | sort

# istio-ingressgateway 서비스 NodePort 변경 및 nodeport 30000로 지정 변경
kubectl patch svc -n istio-system istio-ingressgateway -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 8080, "nodePort": 30000}]}}'
kubectl get svc -n istio-system istio-ingressgateway

# istio-ingressgateway 서비스 externalTrafficPolicy 설정 : ClientIP 수집 확인 용도
kubectl patch svc -n istio-system istio-ingressgateway -p '{"spec":{"externalTrafficPolicy": "Local"}}'
kubectl describe svc -n istio-system istio-ingressgateway


# default 네임스페이스에 istio-proxy sidecar 주입 설정 - Docs
kubectl label namespace default istio-injection=enabled
kubectl get ns --show-labels


# addon 설치
kubectl apply -f samples/addons
kubectl rollout status deployment/kiali -n istio-system

#
kubectl get pod,svc -n istio-system

# NodePort 변경 및 nodeport 30001~30003으로 변경 : prometheus(30001), grafana(30002), kiali(30003), tracing(30004)
kubectl patch svc -n istio-system prometheus -p '{"spec": {"type": "NodePort", "ports": [{"port": 9090, "targetPort": 9090, "nodePort": 30001}]}}'
kubectl patch svc -n istio-system grafana -p '{"spec": {"type": "NodePort", "ports": [{"port": 3000, "targetPort": 3000, "nodePort": 30002}]}}'
kubectl patch svc -n istio-system kiali -p '{"spec": {"type": "NodePort", "ports": [{"port": 20001, "targetPort": 20001, "nodePort": 30003}]}}'
kubectl patch svc -n istio-system tracing -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 16686, "nodePort": 30004}]}}'

# Prometheus 접속 : envoy, istio 메트릭 확인
open http://127.0.0.1:30001

# Grafana 접속
open http://127.0.0.1:30002

# Kiali 접속 1 : NodePort
open http://127.0.0.1:30003

# (옵션) Kiali 접속 2 : Port forward
kubectl port-forward deployment/kiali -n istio-system 20001:20001 &
open http://127.0.0.1:20001

# tracing 접속 : 예거 트레이싱 대시보드
open http://127.0.0.1:30004

```

- Bookinfo sample application 배포 - [Docs](https://istio.io/latest/docs/setup/getting-started/#bookinfo)
  ![]({{ site.url }}/img/post/devops/study/istio/1/35.png)

```bash
# Bookinfo Application 배포
kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml

# 확인 : 서비스 어카운트(sa)는 spiffe 에 svid 에 사용됨
kubectl get all,sa

# product 웹 접속 확인
kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"

# productpage 파드 로그
kubectl logs -l app=productpage -c istio-proxy --tail=-1
kubectl logs -l app=productpage -c productpage -f
```

- Open the application to outside traffic

```bash
# Istio Gateway/VirtualService 설정
cat samples/bookinfo/networking/bookinfo-gateway.yaml
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: bookinfo-gateway
spec:
  selector:
    istio: ingressgateway # use istio default controller
  servers:
  - port:
      number: 8080
      name: http
      protocol: HTTP
    hosts:
    - "*"
---
apiVersion: networking.istio.io/v1
kind: VirtualService
metadata:
  name: bookinfo
spec:
  hosts:
  - "*"
  gateways:
  - bookinfo-gateway
  http:
  - match:
    - uri:
        exact: /productpage
    - uri:
        prefix: /static
    - uri:
        exact: /login
    - uri:
        exact: /logout
    - uri:
        prefix: /api/v1/products
    route:
    - destination:
        host: productpage
        port:
          number: 9080

kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml

# Istio Gateway/VirtualService 설정 확인
kubectl get gw,vs
istioctl proxy-status

# productpage 파드의 istio-proxy 로그 확인 Access log 가 출력 - Default access log format : 링크
kubectl logs -l app=productpage -c istio-proxy -f
kubectl stern -l app=productpage

# productpage 웹 접속 : 새로고침
open http://127.0.0.1:30000/productpage
curl -v -s http://127.0.0.1:30000/productpage | grep -o "<title>.*</title>"

# 반복 접속
for i in {1..100}; do curl -s http://127.0.0.1:30000/productpage | grep -o "<title>.*</title>" ; done

while true; do curl -s http://127.0.0.1:30000/productpage | grep -o "<title>.*</title>" ; echo "--------------" ; sleep 0.5; done
```

새로 고침할 때마다 트래픽이 다른 버전으로 라우팅된다.

- v1
  ![]({{ site.url }}/img/post/devops/study/istio/1/36.png)
- v2
  ![]({{ site.url }}/img/post/devops/study/istio/1/37.png)
- v3
  ![]({{ site.url }}/img/post/devops/study/istio/1/38.png)

![]({{ site.url }}/img/post/devops/study/istio/1/39.png)
(트래픽 흐름을 istio를 통해 사각화하여 볼 수 있다.)
![]({{ site.url }}/img/post/devops/study/istio/1/40.png)
(istio에 Service Mesh를 시각화하여 한 눈에 확인할 수 있다.)

- istio-ingress gateway에 istio-proxy에도 로깅 변경 해보자.

```bash
kubectl exec -it deploy/istio-ingressgateway -n istio-system -- curl -X POST http://localhost:15000/logging
kubectl exec -it deploy/istio-ingressgateway -n istio-system -- curl -X POST http://localhost:15000/logging?http=debug
kubectl exec -it deploy/istio-ingressgateway -n istio-system -- curl -X POST http://localhost:15000/logging?http=info
```

- istio-proxy 파드에 envoy 컨테이너 admin 페이지 접속

```bash
# istio-proxy 파드에 envoy 컨테이너 admin 접속 포트 포워딩 설정
kubectl port-forward deployment/deploy-websrv 15000:15000 &

# envoy 컨테이너 admin 페이지 접속
open http://localhost:15000
```

---

## 도전해보자!

- 과제 1. Istio 관리(설정, 업그레이드 등)에 편리성을 제공하는 Sail Operator 설치 및 사용
  - Sail Operator 1.0.0 released: manage Istio with an operator - [Blog](https://istio.io/latest/blog/2025/sail-operator-ga/)
  - Introducing the Sail Operator: a new way to manage Istio - [Blog](https://istio.io/latest/blog/2024/introducing-sail-operator/)
  - Istio has deprecated its In-Cluster Operator - [Blog](https://istio.io/latest/blog/2024/in-cluster-operator-deprecation-announcement/)
- 과제 2. Istio IngressGW를 Gateway API(구현체는 무엇이든 상관X)를 통한 실습 환경 구성 및 사용 - [Docs](https://istio.io/latest/docs/tasks/traffic-management/ingress/gateway-api/)
  - Gateway API Mesh Support Promoted To Stable - [Blog](https://istio.io/latest/blog/2024/gateway-mesh-ga/)
  - Getting started with Kubernetes Gateway API - [Blog](https://istio.io/latest/blog/2022/getting-started-gtwapi/)
  - Extending Gateway API support in Istio - [Blog](https://istio.io/latest/blog/2022/gateway-api-beta/)
- 과제 3. Istio Proxy를 K8S Native Sidecars로 구성 및 사용 - [blog](https://istio.io/latest/blog/2023/native-sidecars/), [k8s-docs](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/), [k8s-blog](https://kubernetes.io/blog/2023/08/25/native-sidecar-containers/) - 쿠버네티스 네이티브 사이드카 컨테이너(Sidecar Containers) - [Youtube](https://www.youtube.com/watch?v=r3CezY82EJY)

> 도전과제까지 진행하기에는 너무나도 빠듯한 일정이다... 하지만 너무나도 차고 넘치도록 유익한 스터디인 것은 분명하다.
