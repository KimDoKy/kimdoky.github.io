---
layout: post
section-type: post
title: ServiceMesh - Istio - Week9-3
category: devops
tags: ["k8s", "istio", "servicemesh"]
---

# Ambient Mode 실습
### 실습 준비

- kind로 cluster 셋팅

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
- role: worker
- role: worker
networking:
  podSubnet: 10.10.0.0/16
  serviceSubnet: 10.200.1.0/24
EOF

# 설치 확인
docker ps

# 노드에 기본 툴 설치
for node in control-plane worker worker2; do echo "node : myk8s-$node" ; docker exec -it myk8s-$node sh -c 'apt update && apt install tree psmisc lsof ipset wget bridge-utils net-tools dnsutils tcpdump ngrep iputils-ping git vim -y'; echo; done
for node in control-plane worker worker2; do echo "node : myk8s-$node" ; docker exec -it myk8s-$node sh -c 'DEBIAN_FRONTEND=noninteractive apt install termshark -y'; echo; done

# (옵션) kube-ops-view
helm repo add geek-cookbook https://geek-cookbook.github.io/charts/
helm install kube-ops-view geek-cookbook/kube-ops-view --version 1.2.2 --set service.main.type=NodePort,service.main.ports.http.nodePort=30005 --set env.TZ="Asia/Seoul" --namespace kube-system
kubectl get deploy,pod,svc,ep -n kube-system -l app.kubernetes.io/instance=kube-ops-view

## kube-ops-view 접속 URL 확인
open "http://127.0.0.1:30005/#scale=1.5"
open "http://127.0.0.1:30005/#scale=1.3"
```
- kind docker network에 테스트용 PC(container) 배포

{% raw %}
```bash
# kind 설치 시 kind 이름의 도커 브리지가 생성된다 : 172.18.0.0/16 대역
docker network ls
docker inspect kind

# 테스트용 PC(mypc) 컨테이너 기동 : kind 도커 브리지를 사용하고, 컨테이너 IP를 지정 혹은 지정 없이 배포
docker run -d --rm --name mypc --network kind --ip 172.18.0.100 nicolaka/netshoot sleep infinity # IP 지정 실행 시
# 혹은 IP 지정 실행 시 에러 발생 시 아래 처럼 IP 지정 없이 실행
docker run -d --rm --name mypc --network kind nicolaka/netshoot sleep infinity # IP 지정 없이 실행 시
docker ps

# kind network 중 컨테이너(노드) IP(대역) 확인
docker ps -q | xargs docker inspect --format '{{.Name}} {{.NetworkSettings.Networks.kind.IPAddress}}'
/myk8s-worker 172.18.0.2
/myk8s-worker2 172.18.0.4
/myk8s-control-plane 172.18.0.3
/mypc 172.18.0.100
```
{% endraw %}

- MetalLB 배포

```bash
# MetalLB 배포
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.9/config/manifests/metallb-native.yaml


# 확인
kubectl get crd
kubectl get pod -n metallb-system


# IPAddressPool, L2Advertisement 설정
cat << EOF | kubectl apply -f -
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: default
  namespace: metallb-system
spec:
  addresses:
  - 172.18.255.201-172.18.255.220
---
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: default
  namespace: metallb-system
spec:
  ipAddressPools:
  - default
EOF

# 확인
kubectl get IPAddressPool,L2Advertisement -A
```

- Istio 1.26.0 설치: Ambient profile

```bash
# myk8s-control-plane 진입 후 설치 진행
docker exec -it myk8s-control-plane bash
-----------------------------------
# istioctl 설치
export ISTIOV=1.26.0
echo 'export ISTIOV=1.26.0' >> /root/.bashrc

curl -s -L https://istio.io/downloadIstio | ISTIO_VERSION=$ISTIOV sh -
cp istio-$ISTIOV/bin/istioctl /usr/local/bin/istioctl
istioctl version --remote=false
client version: 1.26.0

# ambient 프로파일 컨트롤 플레인 배포
istioctl install --set profile=ambient --set meshConfig.accessLogFile=/dev/stdout --skip-confirmation

# Install the Kubernetes Gateway API CRDs
kubectl get crd gateways.gateway.networking.k8s.io &> /dev/null || \
  kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml

# 보조 도구 설치
kubectl apply -f istio-$ISTIOV/samples/addons
kubectl apply -f istio-$ISTIOV/samples/addons # nodePort 충돌 시 한번 더 입력

# 빠져나오기
exit
-----------------------------------

# 설치 확인 : istiod, istio-ingressgateway, crd 등
kubectl get all,svc,ep,sa,cm,secret,pdb -n istio-system
kubectl get crd | grep istio.io
kubectl get crd | grep -v istio | grep -v metallb
kubectl get crd  | grep gateways
gateways.gateway.networking.k8s.io          2025-06-06T13:06:36Z
gateways.networking.istio.io                2025-06-06T13:05:39Z

kubectl api-resources | grep Gateway
gatewayclasses                    gc           gateway.networking.k8s.io/v1           false        GatewayClass
gateways                          gtw          gateway.networking.k8s.io/v1           true         Gateway
gateways                          gw           networking.istio.io/v1                 true         Gateway

kubectl describe cm -n istio-system istio
...
Data
====
mesh:
----
accessLogFile: /dev/stdout
defaultConfig:
  discoveryAddress: istiod.istio-system.svc:15012
defaultProviders:
  metrics:
  - prometheus
enablePrometheusMerge: true
...

docker exec -it myk8s-control-plane istioctl proxy-status
NAME                           CLUSTER        CDS         LDS         EDS         RDS         ECDS        ISTIOD                      VERSION
ztunnel-df5dn.istio-system     Kubernetes     IGNORED     IGNORED     IGNORED     IGNORED     IGNORED     istiod-86b6b7ff7-q8gr9     1.26.0
ztunnel-hjzcb.istio-system     Kubernetes     IGNORED     IGNORED     IGNORED     IGNORED     IGNORED     istiod-86b6b7ff7-q8gr9     1.26.0
ztunnel-nn6z9.istio-system     Kubernetes     IGNORED     IGNORED     IGNORED     IGNORED     IGNORED     istiod-86b6b7ff7-q8gr9     1.26.0

docker exec -it myk8s-control-plane istioctl ztunnel-config workload
docker exec -it myk8s-control-plane istioctl ztunnel-config service

# iptables 규칙 확인
for node in control-plane worker worker2; do echo "node : myk8s-$node" ; docker exec -it myk8s-$node sh -c 'iptables-save'; echo; done


# NodePort 변경 및 nodeport 30001~30003으로 변경 : prometheus(30001), grafana(30002), kiali(30003), tracing(30004)
kubectl patch svc -n istio-system prometheus -p '{"spec": {"type": "NodePort", "ports": [{"port": 9090, "targetPort": 9090, "nodePort": 30001}]}}'
kubectl patch svc -n istio-system grafana -p '{"spec": {"type": "NodePort", "ports": [{"port": 3000, "targetPort": 3000, "nodePort": 30002}]}}'
kubectl patch svc -n istio-system kiali -p '{"spec": {"type": "NodePort", "ports": [{"port": 20001, "targetPort": 20001, "nodePort": 30003}]}}'
kubectl patch svc -n istio-system tracing -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 16686, "nodePort": 30004}]}}'

# Prometheus 접속 : envoy, istio 메트릭 확인
open http://127.0.0.1:30001

# Grafana 접속
open http://127.0.0.1:30002

# Kiali 접속 : NodePort
open http://127.0.0.1:30003

# tracing 접속 : 예거 트레이싱 대시보드
open http://127.0.0.1:30004
```

- istio-cni-node 확인

```bash
#
kubectl get ds -n istio-system
NAME             DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
istio-cni-node   3         3         3       3            3           kubernetes.io/os=linux   115s
ztunnel          3         3         3       3            3           kubernetes.io/os=linux   105s

#
kubectl get pod -n istio-system -l k8s-app=istio-cni-node -owide
kubectl describe pod -n istio-system -l k8s-app=istio-cni-node
...
Containers:
  install-cni:
    Container ID:  containerd://b09a6898cdb1d82b4f077d24d8eca0b761caa2ac3cdc5ae0b64765da614ee984
    Image:         docker.io/istio/install-cni:1.26.0-distroless
    Image ID:      docker.io/istio/install-cni@sha256:e69cea606f6fe75907602349081f78ddb0a94417199f9022f7323510abef65cb
    Port:          15014/TCP
    Host Port:     0/TCP
    Command:
      install-cni
    Args:
      --log_output_level=info
    State:          Running
      Started:      Fri, 06 Jun 2025 22:05:56 +0900
    Ready:          True
    Restart Count:  0
    Requests:
      cpu:      100m
      memory:   100Mi
    Readiness:  http-get http://:8000/readyz delay=0s timeout=1s period=10s #success=1 #failure=3
    Environment Variables from:
      istio-cni-config  ConfigMap  Optional: false
    Environment:
      REPAIR_NODE_NAME:            (v1:spec.nodeName)
      REPAIR_RUN_AS_DAEMON:       true
      REPAIR_SIDECAR_ANNOTATION:  sidecar.istio.io/status
      ALLOW_SWITCH_TO_HOST_NS:    true
      NODE_NAME:                   (v1:spec.nodeName)
      GOMEMLIMIT:                 node allocatable (limits.memory)
      GOMAXPROCS:                 node allocatable (limits.cpu)
      POD_NAME:                   istio-cni-node-xj4x2 (v1:metadata.name)
      POD_NAMESPACE:              istio-system (v1:metadata.namespace)
    Mounts:
      /host/etc/cni/net.d from cni-net-dir (rw)
      /host/opt/cni/bin from cni-bin-dir (rw)
      /host/proc from cni-host-procfs (ro)
      /host/var/run/netns from cni-netns-dir (rw)
      /var/run/istio-cni from cni-socket-dir (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-srxzl (ro)
      /var/run/ztunnel from cni-ztunnel-sock-dir (rw)
...
Volumes:
  cni-bin-dir:
    Type:          HostPath (bare host directory volume)
    Path:          /opt/cni/bin
    HostPathType:  
  cni-host-procfs:
    Type:          HostPath (bare host directory volume)
    Path:          /proc
    HostPathType:  Directory
  cni-ztunnel-sock-dir:
    Type:          HostPath (bare host directory volume)
    Path:          /var/run/ztunnel
    HostPathType:  DirectoryOrCreate
  cni-net-dir:
    Type:          HostPath (bare host directory volume)
    Path:          /etc/cni/net.d
    HostPathType:  
  cni-socket-dir:
    Type:          HostPath (bare host directory volume)
    Path:          /var/run/istio-cni
    HostPathType:  
  cni-netns-dir:
    Type:          HostPath (bare host directory volume)
    Path:          /var/run/netns
    HostPathType:  DirectoryOrCreate
...


# 노드에서 기본 정보 확인
for node in control-plane worker worker2; do echo "node : myk8s-$node" ; docker exec -it myk8s-$node sh -c 'ls -l /opt/cni/bin'; echo; done
-rwxr-xr-x 1 root root 52428984 Jun  1 05:42 istio-cni
...

for node in control-plane worker worker2; do echo "node : myk8s-$node" ; docker exec -it myk8s-$node sh -c 'ls -l /etc/cni/net.d'; echo; done
-rw-r--r-- 1 root root 862 Jun  1 04:54 10-kindnet.conflist


for node in control-plane worker worker2; do echo "node : myk8s-$node" ; docker exec -it myk8s-$node sh -c 'ls -l /var/run/istio-cni'; echo; done
-rw------- 1 root root 2990 Jun  1 05:42 istio-cni-kubeconfig
-rw------- 1 root root  171 Jun  1 04:54 istio-cni.log
srw-rw-rw- 1 root root    0 Jun  1 04:54 log.sock
srw-rw-rw- 1 root root    0 Jun  1 04:54 pluginevent.sock

for node in control-plane worker worker2; do echo "node : myk8s-$node" ; docker exec -it myk8s-$node sh -c 'ls -l /var/run/netns'; echo; done
...

for node in control-plane worker worker2; do echo "node : myk8s-$node" ; docker exec -it myk8s-$node sh -c 'lsns -t net'; echo; done


# istio-cni-node 데몬셋 파드 로그 확인
kubectl logs  -n istio-system -l k8s-app=istio-cni-node -f
...
```

- ztunnel 데몬셋 파드 정보 확인

```bash
# ztunnel 파드 확인 : 파드 이름 변수 지정
kubectl get pod -n istio-system -l app=ztunnel -owide
kubectl get pod -n istio-system -l app=ztunnel
ZPOD1NAME=$(kubectl get pod -n istio-system -l app=ztunnel -o jsonpath="{.items[0].metadata.name}")
ZPOD2NAME=$(kubectl get pod -n istio-system -l app=ztunnel -o jsonpath="{.items[1].metadata.name}")
ZPOD3NAME=$(kubectl get pod -n istio-system -l app=ztunnel -o jsonpath="{.items[2].metadata.name}")
echo $ZPOD1NAME $ZPOD2NAME $ZPOD3NAME

#
kubectl describe pod -n istio-system -l app=ztunnel
...
Containers:
  istio-proxy:
    Container ID:  containerd://d81ca867bfd0c505f062ea181a070a8ab313df3591e599a22706a7f4f537ffc5
    Image:         docker.io/istio/ztunnel:1.26.0-distroless
    Image ID:      docker.io/istio/ztunnel@sha256:d711b5891822f4061c0849b886b4786f96b1728055333cbe42a99d0aeff36dbe
    Port:          15020/TCP
    ...
    Requests:
      cpu:      200m
      memory:   512Mi
    Readiness:  http-get http://:15021/healthz/ready delay=0s timeout=1s period=10s #success=1 #failure=3
    Environment:
      CA_ADDRESS:                        istiod.istio-system.svc:15012
      XDS_ADDRESS:                       istiod.istio-system.svc:15012
      RUST_LOG:                          info
      RUST_BACKTRACE:                    1
      ISTIO_META_CLUSTER_ID:             Kubernetes
      INPOD_ENABLED:                     true
      TERMINATION_GRACE_PERIOD_SECONDS:  30
      POD_NAME:                          ztunnel-9rzzt (v1:metadata.name)
      POD_NAMESPACE:                     istio-system (v1:metadata.namespace)
      NODE_NAME:                          (v1:spec.nodeName)
      INSTANCE_IP:                        (v1:status.podIP)
      SERVICE_ACCOUNT:                    (v1:spec.serviceAccountName)
      ISTIO_META_ENABLE_HBONE:           true
    Mounts:
      /tmp from tmp (rw)
      /var/run/secrets/istio from istiod-ca-cert (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-42r88 (ro)
      /var/run/secrets/tokens from istio-token (rw)
      /var/run/ztunnel from cni-ztunnel-sock-dir (rw)
    ...
Volumes:
  istio-token:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  43200
  istiod-ca-cert:
    Type:      ConfigMap (a volume populated by a ConfigMap)
    Name:      istio-ca-root-cert
    Optional:  false
  cni-ztunnel-sock-dir:
    Type:          HostPath (bare host directory volume)
    Path:          /var/run/ztunnel
    HostPathType:  DirectoryOrCreate
...


#
kubectl krew install pexec
kubectl pexec $ZPOD1NAME -it -T -n istio-system -- bash
-------------------------------------------------------
whoami

ip -c addr
ifconfig

iptables -t mangle -S
iptables -t nat -S

ss -tnlp
ss -tnp

ss -xnp
Netid     State     Recv-Q     Send-Q                           Local Address:Port             Peer Address:Port       Process
u_seq     ESTAB     0          0                /var/run/ztunnel/ztunnel.sock 384472                      * 382521
u_seq     ESTAB     0          0                                            * 382521                      * 384472      users:(("ztunnel",pid=1,fd=19))
u_str     ESTAB     0          0                                            * 385352                      * 385353      users:(("ztunnel",pid=1,fd=13),("ztunnel",pid=1,fd=8),("ztunnel",pid=1,fd=6))
u_str     ESTAB     0          0                                            * 385353                      * 385352      users:(("ztunnel",pid=1,fd=7))

ls -l  /var/run/ztunnel
total 0
srwxr-xr-x    1 root     root             0 Jun  1 04:54 ztunnel.sock

# 메트릭 정보 확인
curl -s http://localhost:15020/metrics

# Viewing Istiod state for ztunnel xDS resources
curl -s http://localhost:15000/config_dump

exit
-------------------------------------------------------

# 아래 ztunnel 파드도 확인해보자
kubectl pexec $ZPOD2NAME -it -T -n istio-system -- bash
kubectl pexec $ZPOD3NAME -it -T -n istio-system -- bash


# 노드에서 기본 정보 확인
for node in control-plane worker worker2; do echo "node : myk8s-$node" ; docker exec -it myk8s-$node sh -c 'ls -l /var/run/ztunnel'; echo; done


# ztunnel 데몬셋 파드 로그 확인
kubectl logs -n istio-system -l app=ztunnel -f
...
```

---
## Deploy the sample application
```bash
#
docker exec -it myk8s-control-plane ls -l istio-1.26.0
total 40
-rw-r--r--  1 root root 11357 May  7 11:05 LICENSE
-rw-r--r--  1 root root  6927 May  7 11:05 README.md
drwxr-x---  2 root root  4096 May  7 11:05 bin
-rw-r-----  1 root root   983 May  7 11:05 manifest.yaml
drwxr-xr-x  4 root root  4096 May  7 11:05 manifests
drwxr-xr-x 27 root root  4096 May  7 11:05 samples
drwxr-xr-x  3 root root  4096 May  7 11:05 tools

# Deploy the Bookinfo sample application:
docker exec -it myk8s-control-plane kubectl apply -f istio-1.26.0/samples/bookinfo/platform/kube/bookinfo.yaml

# 확인
kubectl get deploy,pod,svc,ep
docker exec -it myk8s-control-plane istioctl ztunnel-config service
docker exec -it myk8s-control-plane istioctl ztunnel-config workload
docker exec -it myk8s-control-plane istioctl proxy-status


# 통신 확인 : ratings 에서 productpage 페이지
kubectl exec "$(kubectl get pod -l app=ratings -o jsonpath='{.items[0].metadata.name}')" -c ratings -- curl -sS productpage:9080/productpage | grep -o "<title>.*</title>"


# 요청 테스트용 파드 생성 : netshoot
kubectl create sa netshoot

cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: netshoot
spec:
  serviceAccountName: netshoot
  nodeName: myk8s-control-plane
  containers:
  - name: netshoot
    image: nicolaka/netshoot
    command: ["tail"]
    args: ["-f", "/dev/null"]
  terminationGracePeriodSeconds: 0
EOF

# 요청 확인
kubectl exec -it netshoot -- curl -sS productpage:9080/productpage | grep -i title

# 반복 요청
while true; do kubectl exec -it netshoot -- curl -sS productpage:9080/productpage | grep -i title ; date "+%Y-%m-%d %H:%M:%S"; sleep 1; done

```
## Open the application to outside traffic
```bash
#
docker exec -it myk8s-control-plane cat istio-1.26.0/samples/bookinfo/gateway-api/bookinfo-gateway.yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: bookinfo-gateway
spec:
  gatewayClassName: istio
  listeners:
  - name: http
    port: 80
    protocol: HTTP
    allowedRoutes:
      namespaces:
        from: Same
---
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: bookinfo
spec:
  parentRefs:
  - name: bookinfo-gateway
  rules:
  - matches:
    - path:
        type: Exact
        value: /productpage
    - path:
        type: PathPrefix
        value: /static
    - path:
        type: Exact
        value: /login
    - path:
        type: Exact
        value: /logout
    - path:
        type: PathPrefix
        value: /api/v1/products
    backendRefs:
    - name: productpage
      port: 9080

docker exec -it myk8s-control-plane kubectl apply -f istio-1.26.0/samples/bookinfo/gateway-api/bookinfo-gateway.yaml

# 확인
kubectl get gateway
NAME               CLASS   ADDRESS          PROGRAMMED   AGE
bookinfo-gateway   istio   172.18.255.201   True         14s

kubectl get HTTPRoute
NAME       HOSTNAMES   AGE
bookinfo               24s

kubectl get svc,ep bookinfo-gateway-istio
NAME                             TYPE           CLUSTER-IP     EXTERNAL-IP      PORT(S)                        AGE
service/bookinfo-gateway-istio   LoadBalancer   10.200.1.232   172.18.255.201   15021:31254/TCP,80:31414/TCP   42s

NAME                               ENDPOINTS                      AGE
endpoints/bookinfo-gateway-istio   10.10.1.7:15021,10.10.1.7:80   42s

kubectl get pod -l gateway.istio.io/managed=istio.io-gateway-controller -owide
NAME                                      READY   STATUS    RESTARTS   AGE   IP          NODE            NOMINATED NODE   READINESS GATES
bookinfo-gateway-istio-6cbd9bcd49-rvkss   1/1     Running   0          59s   10.10.1.7   myk8s-worker2   <none>           <none>

# 접속 확인
docker ps

kubectl get svc bookinfo-gateway-istio -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
GWLB=$(kubectl get svc bookinfo-gateway-istio -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
docker exec -it mypc curl $GWLB/productpage -v
docker exec -it mypc curl $GWLB/productpage -I

# 반복 요청 : 아래 mypc 컨테이너에서 반복 요청 계속 해두기!
GWLB=$(kubectl get svc bookinfo-gateway-istio -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
while true; do docker exec -it mypc curl $GWLB/productpage | grep -i title ; date "+%Y-%m-%d %H:%M:%S"; sleep 1; done


# 자신의 로컬 PC에서 접속 시도
kubectl patch svc bookinfo-gateway-istio -p '{"spec": {"type": "LoadBalancer", "ports": [{"port": 80, "targetPort": 80, "nodePort": 30000}]}}'
kubectl get svc bookinfo-gateway-istio

open "http://127.0.0.1:30000/productpage"

# 반복 요청
while true; do curl -s http://127.0.0.1:30000/productpage | grep -i title ; date "+%Y-%m-%d %H:%M:%S"; sleep 1; done

```
![]({{ site.url }}/img/post/devops/study/istio/9/20250606230012.png)

![]({{ site.url }}/img/post/devops/study/istio/9/20250606230028.png)

## Adding your application to ambient
- NS or Pod label: `istio.io/dataplane-mode=ambient`
- pod does not have pot-out label: `istio.io/dataplane-mode=none`

![]({{ site.url }}/img/post/devops/study/istio/9/20250606231315.png)
```bash
# 디폴트 네임스페이서 모든 파드들에 ambient mesh 통신 적용 설정
# You can enable all pods in a given namespace to be part of the ambient mesh by simply labeling the namespace:
kubectl label namespace default istio.io/dataplane-mode=ambient

# 파드 정보 확인 : 사이트카가 없다! , 파드 수명 주기에 영향도 없다! -> mTLS 암호 통신 제공, L4 텔레메트리(메트릭) 제공
docker exec -it myk8s-control-plane istioctl proxy-status
kubectl get pod

#
docker exec -it myk8s-control-plane istioctl ztunnel-config workload
NAMESPACE          POD NAME                                    ADDRESS    NODE                WAYPOINT PROTOCOL
...
default            productpage-v1-54bb874995-8flvt             10.10.2.17 myk8s-worker        None     HBONE
...

docker exec -it myk8s-control-plane istioctl ztunnel-config workload --address 10.10.2.17

docker exec -it myk8s-control-plane istioctl ztunnel-config workload --address 10.10.2.17 -o json
```
![]({{ site.url }}/img/post/devops/study/istio/9/20250606230842.png)

```
#
PPOD=$(kubectl get pod -l app=productpage -o jsonpath='{.items[0].metadata.name}')

kubectl pexec $PPOD -it -T -- bash
-------------------------------------------------------
iptables-save
iptables -t mangle -S
iptables -t nat -S
ss -tnlp
ss -tnp
ss -xnp
ls -l  /var/run/ztunnel

exit
-------------------------------------------------------
```

![]({{ site.url }}/img/post/devops/study/istio/9/20250606231821.png)

```
# 노드에서 ipset 확인 : 파드들의 ip를 멤버로 관리 확인
for node in control-plane worker worker2; do echo "node : myk8s-$node" ; docker exec -it myk8s-$node ipset list; echo; done
```
![]({{ site.url }}/img/post/devops/study/istio/9/20250606232044.png)
```
# istio-cni-node 로그 확인
kubectl -n istio-system logs -l k8s-app=istio-cni-node -f
...

# ztunnel 파드 로그 모니터링 : IN/OUT 트래픽 정보
kubectl -n istio-system logs -l app=ztunnel -f | egrep "inbound|outbound"
```
![]({{ site.url }}/img/post/devops/study/istio/9/20250606232722.png)
```
# ztunnel 파드 확인 : 파드 이름 변수 지정
kubectl get pod -n istio-system -l app=ztunnel -owide
kubectl get pod -n istio-system -l app=ztunnel
ZPOD1NAME=$(kubectl get pod -n istio-system -l app=ztunnel -o jsonpath="{.items[0].metadata.name}")
ZPOD2NAME=$(kubectl get pod -n istio-system -l app=ztunnel -o jsonpath="{.items[1].metadata.name}")
ZPOD3NAME=$(kubectl get pod -n istio-system -l app=ztunnel -o jsonpath="{.items[2].metadata.name}")
echo $ZPOD1NAME $ZPOD2NAME $ZPOD3NAME

#
kubectl pexec $ZPOD1NAME -it -T -n istio-system -- bash
-------------------------------------------------------
iptables -t mangle -S
iptables -t nat -S
ss -tnlp
ss -tnp
ss -xnp
ls -l  /var/run/ztunnel

# 메트릭 정보 확인
curl -s http://localhost:15020/metrics | grep '^[^#]'
...

# Viewing Istiod state for ztunnel xDS resources
curl -s http://localhost:15000/config_dump

exit
-------------------------------------------------------

# netshoot 파드만 ambient mode 에서 제외해보자
docker exec -it myk8s-control-plane istioctl ztunnel-config workload
kubectl label pod netshoot istio.io/dataplane-mode=none
docker exec -it myk8s-control-plane istioctl ztunnel-config workload
NAMESPACE          POD NAME                                    ADDRESS    NODE                WAYPOINT PROTOCOL
default            netshoot                                    10.10.0.7  myk8s-control-plane None     TCP

```
![]({{ site.url }}/img/post/devops/study/istio/9/20250606233142.png)
![]({{ site.url }}/img/post/devops/study/istio/9/20250606233312.png)
## 상세 정보 분석
### istio-proxy 정보 확인
```bash
#
docker exec -it myk8s-control-plane istioctl proxy-status
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/bookinfo-gateway-istio
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/bookinfo-gateway-istio --waypoint
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/bookinfo-gateway-istio --port 80
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/bookinfo-gateway-istio --port 80 -o json

docker exec -it myk8s-control-plane istioctl proxy-config route deploy/bookinfo-gateway-istio
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/bookinfo-gateway-istio --name http.80
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/bookinfo-gateway-istio --name http.80 -o json

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/bookinfo-gateway-istio
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/bookinfo-gateway-istio --fqdn productpage.default.svc.cluster.local -o json

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/bookinfo-gateway-istio --status healthy
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/bookinfo-gateway-istio --cluster 'outbound|9080||productpage.default.svc.cluster.local' -o json

docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/bookinfo-gateway-istio
docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/bookinfo-gateway-istio -o json

docker exec -it myk8s-control-plane istioctl proxy-config bootstrap deploy/bookinfo-gateway-istio
```
### ztunnel-config
```bash
# A group of commands used to update or retrieve Ztunnel configuration from a Ztunnel instance.
docker exec -it myk8s-control-plane istioctl ztunnel-config

docker exec -it myk8s-control-plane istioctl ztunnel-config service

docker exec -it myk8s-control-plane istioctl ztunnel-config service --service-namespace default --node myk8s-worker
docker exec -it myk8s-control-plane istioctl ztunnel-config service --service-namespace default --node myk8s-worker2
docker exec -it myk8s-control-plane istioctl ztunnel-config service --service-namespace default --node myk8s-worker2 -o json

docker exec -it myk8s-control-plane istioctl ztunnel-config workload
docker exec -it myk8s-control-plane istioctl ztunnel-config workload --workload-namespace default
docker exec -it myk8s-control-plane istioctl ztunnel-config workload --workload-namespace default --node myk8s-worker2
docker exec -it myk8s-control-plane istioctl ztunnel-config workload --workload-namespace default --node myk8s-worker -o json
```
![]({{ site.url }}/img/post/devops/study/istio/9/20250606234934.png)
```
docker exec -it myk8s-control-plane istioctl ztunnel-config certificate --node myk8s-worker

docker exec -it myk8s-control-plane istioctl ztunnel-config certificate --node myk8s-worker -o json
...

docker exec -it myk8s-control-plane istioctl ztunnel-config connections --node myk8s-worker

docker exec -it myk8s-control-plane istioctl ztunnel-config connections --node myk8s-worker --raw 

docker exec -it myk8s-control-plane istioctl ztunnel-config connections --node myk8s-worker -o json
```
![]({{ site.url }}/img/post/devops/study/istio/9/20250607000847.png)
```
docker exec -it myk8s-control-plane istioctl ztunnel-config policy   
NAMESPACE POLICY NAME ACTION SCOPE

docker exec -it myk8s-control-plane istioctl ztunnel-config log   
ztunnel-25hpt.istio-system:
current log level is hickory_server::server::server_future=off,info
...
```
### productpage 확인

```bash
PPOD=$(kubectl get pod -l app=productpage -o jsonpath='{.items[0].metadata.name}')

kubectl pexec $PPOD -it -T -- bash
-------------------------------------------------------
iptables-save
...

# DNS 트래픽에 대해 연결 추적을 설정, 이후 마크 기반으로 리디렉션 여부를 제어
iptables -t raw -S
...
-A PREROUTING -j ISTIO_PRERT
-A OUTPUT -j ISTIO_OUTPUT
-A ISTIO_OUTPUT -p udp -m mark --mark 0x539/0xfff -m udp --dport 53 -j CT --zone 1
-A ISTIO_PRERT -p udp -m mark ! --mark 0x539/0xfff -m udp --sport 53 -j CT --zone 1


# 특정 마크가 붙은 트래픽을 식별해서 추후 NAT에서 건너뛰게 함
iptables -t mangle -S
...
## 들어오는 패킷을 ISTIO_PRERT 체인으로 전달
-A PREROUTING -j ISTIO_PRERT

## 로컬 생성 트래픽도 마찬가지로 처리
-A OUTPUT -j ISTIO_OUTPUT

## 연결 추적에 저장된 마크를 복원
-A ISTIO_OUTPUT -m connmark --mark 0x111/0xfff -j CONNMARK --restore-mark --nfmask 0xffffffff --ctmask 0xffffffff

## 마크가 특정 값일 경우 새로운 마크로 설정
-A ISTIO_PRERT -m mark --mark 0x539/0xfff -j CONNMARK --set-xmark 0x111/0xfff


# 트래픽 리디렉션 실행
iptables -t nat -S
...
## 특정 IP 예외 처리 (프록시 자체나 메타데이터 주소 등)
-A ISTIO_OUTPUT -d 169.254.7.127/32 -p tcp -m tcp -j ACCEPT

## DNS 요청(udp/53) 을 15053 포트로 리디렉션
-A ISTIO_OUTPUT ! -o lo -p udp -m mark ! --mark 0x539/0xfff -m udp --dport 53 -j REDIRECT --to-ports 15053

## TCP 기반 DNS 요청 도 15053으로 리디렉션
-A ISTIO_OUTPUT ! -d 127.0.0.1/32 -p tcp -m tcp --dport 53 -m mark ! --mark 0x539/0xfff -j REDIRECT --to-ports 15053

## 특정 마크가 붙은 트래픽은 리디렉션에서 제외
-A ISTIO_OUTPUT -p tcp -m mark --mark 0x111/0xfff -j ACCEPT

## 루프백 인터페이스로 향하는 트래픽은 건너뜀
-A ISTIO_OUTPUT ! -d 127.0.0.1/32 -o lo -j ACCEPT

## 나머지 TCP 트래픽은 15001 로 리디렉션
-A ISTIO_OUTPUT ! -d 127.0.0.1/32 -p tcp -m mark ! --mark 0x539/0xfff -j REDIRECT --to-ports 15001

## 특정 메타데이터 IP에서 온 트래픽은 리디렉션 예외
-A ISTIO_PRERT -s 169.254.7.127/32 -p tcp -m tcp -j ACCEPT

## 들어오는 외부 TCP 트래픽을 inbound 포트(15006) 로 리디렉션
-A ISTIO_PRERT ! -d 127.0.0.1/32 -p tcp -m tcp ! --dport 15008 -m mark ! --mark 0x539/0xfff -j REDIRECT --to-ports 15006

# 요약
## DNS 트래픽 → 15053 포트로 리디렉션 (Envoy가 DNS를 프록시)
## TCP 트래픽 (출발지/도착지에 따라) → 15001 또는 15006 포트로 리디렉션
## 특정 마크 (0x539, 0x111)나 주소는 리디렉션 제외
## conntrack 및 mark 시스템으로 트래픽 상태 관리 및 리디렉션 조건 제어


# 15001,15006,15008 확인
ss -tnp
ss -tnlp
State             Recv-Q            Send-Q                       Local Address:Port                          Peer Address:Port            Process            
LISTEN            0                 128                              127.0.0.1:15053                              0.0.0.0:*                                  
LISTEN            0                 128                                  [::1]:15053                                 [::]:*                                  
LISTEN            0                 128                                      *:15001                                    *:*                                  
LISTEN            0                 128                                      *:15006                                    *:*                                  
LISTEN            0                 128                                      *:15008                                    *:*                                  
LISTEN            0                 2048                                     *:9080                                     *:*                users:(("gunicorn",pid=18,fd=5),("gunicorn",pid=17,fd=5),("gunicorn",pid=16,fd=5),("gunicorn",pid=15,fd=5),("gunicorn",pid=14,fd=5),("gunicorn",pid=13,fd=5),("gunicorn",pid=12,fd=5),("gunicorn",pid=11,fd=5),("gunicorn",pid=1,fd=5))

# 암호화 확인
tcpdump -i eth0 -A -s 0 -nn 'tcp port 15008'

apk update && apk add ngrep
ngrep -tW byline -d eth0 '' 'tcp port 15008'

#
ngrep -tW byline -d eth0 '' 'tcp port 15001'
ngrep -tW byline -d eth0 '' 'tcp port 15006'

# 
ls -l /var/run/ztunnel

exit
-------------------------------------------------------
```
## Verify mTLS is enabled
### workload의 ztunnel config를 사용하여 mTLS 검증
```bash
docker exec -it myk8s-control-plane istioctl ztunnel-config workload
```
![]({{ site.url }}/img/post/devops/study/istio/9/20250607003910.png)

### metrics에서 mTLS 검증
```
istio_tcp_connections_opened_total
```
![]({{ site.url }}/img/post/devops/study/istio/9/20250607004047.png)
### logs에서 mTLS 검증
- 소스 또는 대상 ztunnel 로그를 피어 ID와 함께 확인
- SPIFFE ID가 있다는 것은 mTLS가 수행되었음을 의미

```bash
kubectl -n istio-system logs -l app=ztunnel | grep -E "inbound|outbound"
```
![]({{ site.url }}/img/post/devops/study/istio/9/20250607004820.png)

### Kiali에서 검증
![]({{ site.url }}/img/post/devops/study/istio/9/20250607005139.png)

### tcpdump로 검증

```bash
DPOD=$(kubectl get pods -l app=details -o jsonpath="{.items[0].metadata.name}")

kubectl pexec $DPOD -it -T -- sh -c 'tcpdump -nAi eth0 port 9080 or port 15008'
```

![]({{ site.url }}/img/post/devops/study/istio/9/20250607010527.png)
## Secure Application Access: L4 Authorization Policy
### 두 계층(L4/L7)의 보안 정책
**1. L4 정책 (ztunnel)**
- 모든 ambient 워크로드에 **자동 적용**
- IP/포트 기반 접근 제어
- Kubernetes Network Policy와 **함께 사용** 가능 (심층 방어)

**2. L7 정책 (Waypoint)**
- **선택적 배포** - 필요한 워크로드만
- HTTP 메서드, 경로, 헤더 기반 고급 제어
- 트래픽 라우팅 기능 포함

**핵심**: 기본 L4 보안 + 필요시 선택적 L7 고급 기능으로 **유연한 보안 모델** 제공
```bash
# netshoot 파드만 ambient mode 다시 참여
docker exec -it myk8s-control-plane istioctl ztunnel-config workload
kubectl label pod netshoot istio.io/dataplane-mode=ambient --overwrite
docker exec -it myk8s-control-plane istioctl ztunnel-config workload

# L4 Authorization Policy 신규 생성
# Explicitly allow the netshoot and gateway service accounts to call the productpage service:
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-viewer
  namespace: default
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/netshoot
EOF

# L4 Authorization Policy 생성 확인
kubectl get authorizationpolicy

# ztunnel 파드 로그 모니터링
kubectl logs ds/ztunnel -n istio-system -f | grep -E RBAC

# L4 Authorization Policy 동작 확인
## 차단 확인!
GWLB=$(kubectl get svc bookinfo-gateway-istio -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
while true; do docker exec -it mypc curl $GWLB/productpage | grep -i title ; date "+%Y-%m-%d %H:%M:%S"; sleep 1; done

## 허용 확인!
kubectl exec -it netshoot -- curl -sS productpage:9080/productpage | grep -i title
while true; do kubectl exec -it netshoot -- curl -sS productpage:9080/productpage | grep -i title ; date "+%Y-%m-%d %H:%M:%S"; sleep 1; done


# L4 Authorization Policy 업데이트
kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1
kind: AuthorizationPolicy
metadata:
  name: productpage-viewer
  namespace: default
spec:
  selector:
    matchLabels:
      app: productpage
  action: ALLOW
  rules:
  - from:
    - source:
        principals:
        - cluster.local/ns/default/sa/netshoot
        - cluster.local/ns/default/sa/bookinfo-gateway-istio
EOF

kubectl logs ds/ztunnel -n istio-system -f | grep -E RBAC


# 허용 확인!
GWLB=$(kubectl get svc bookinfo-gateway-istio -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
while true; do docker exec -it mypc curl $GWLB/productpage | grep -i title ; date "+%Y-%m-%d %H:%M:%S"; sleep 1; done

```
![]({{ site.url }}/img/post/devops/study/istio/9/20250607012654.png)

- 허용된 정책 속성
	- 정책이 L4 전용인지 여부를 결정


|Type|Attribute|Positive match|Negative match|
---|---|---|---
|Source|Peer identity|`principals`|`notPrincipals`|
|Source|Namespace|`namespaces`|`notNamespaces`|
|Source|IP block|`ipBlocks`|`notIpBlocks`|
|Operation|Destination port|`ports`|`notPorts`|
|Condition|Source IP|`source.ip`|n/a|
|Condition|Source namespace|`source.namespace`|n/a|
|Condition|Source identity|`source.principal`|n/a|
|Condition|Remote IP|`destination.ip`|n/a|
|Condition|Remote port|`destination.port`|n/a|

## Configure waypoint proxies
- **Envoy 기반 프록시**를 **선택적으로 배포**
- 정의된 워크로드 집합에 **L7 처리** 추가
- 애플리케이션과 **독립적으로** 설치/업그레이드/확장
- 애플리케이션 소유자는 프록시 존재를 **인식하지 않음**
- 사이드카 대비 **필요한 프록시 수 대폭 감소**
- **보안 경계가 비슷한 애플리케이션 간 공유** 가능
- 특정 워크로드의 모든 인스턴스 또는 네임스페이스의 모든 워크로드 대상
- **목적지 waypoint에서 정책 시행** (사이드카와 차이점)
- 리소스(네임스페이스/서비스/포드)로 가는 **관문 역할**
- 해당 리소스로 들어오는 **모든 트래픽이 waypoint 통과 강제**
- **No mesh** → **보안 L4 오버레이** → **전체 L7 처리**로 원활한 전환
- Istio의 **점진적 채택** 가능
- ztunnel vs Waypoint
	- **ztunnel**: L4에서만 트래픽 처리, 공유 구성 요소로 안전 작동
	- **Waypoint**: ztunnel을 통해 트래픽 전달받아 L7 처리

### Waypoint 필요한 경우
- Traffic Management
    - HTTP routing & load balancing
    - Circuit breaking
    - Rate limiting
    - Fault injection
    - Retries
    - Timeouts
- Security
    - L7 기반 풍부한 인가 정책
    - 요청 타입 또는 HTTP 헤더 기반 제어
- Observability
    - HTTP metrics
    - Access logging
    - Tracing

```bash
# istioctl can generate a Kubernetes Gateway resource for a waypoint proxy. 
# For example, to generate a waypoint proxy named waypoint for the default namespace that can process traffic for services in the namespace:
kubectl describe pod bookinfo-gateway-istio-6cbd9bcd49-rvkss | grep 'Service Account'
Service Account:  bookinfo-gateway-istio

# Generate a waypoint configuration as YAML
docker exec -it myk8s-control-plane istioctl waypoint generate -h

# --for string        Specify the traffic type [all none service workload] for the waypoint
istioctl waypoint generate --for service -n default
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  labels:
    istio.io/waypoint-for: service
  name: waypoint
  namespace: default
spec:
  gatewayClassName: istio-waypoint
  listeners:
  - name: mesh
    port: 15008
    protocol: HBONE

#
docker exec -it myk8s-control-plane istioctl waypoint apply -n default
✅ waypoint default/waypoint applied

kubectl get gateway 
kubectl get gateway waypoint -o yaml
...

#
kubectl get pod -l service.istio.io/canonical-name=waypoint -owide
NAME                      READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
waypoint-66b59898-lx4tc   1/1     Running   0          14s   10.10.2.24   myk8s-worker   <none>           <none>

#
docker exec -it myk8s-control-plane istioctl waypoint list  
NAME         REVISION     PROGRAMMED
waypoint     default      True

docker exec -it myk8s-control-plane istioctl waypoint status
NAMESPACE     NAME         STATUS     TYPE           REASON         MESSAGE
default       waypoint     True       Programmed     Programmed     Resource programmed, assigned to service(s) waypoint.default.svc.cluster.local:15008

docker exec -it myk8s-control-plane istioctl proxy-status   
NAME                                                CLUSTER        CDS              LDS              EDS              RDS              ECDS        ISTIOD                     VERSION
bookinfo-gateway-istio-6cbd9bcd49-rvkss.default     Kubernetes     SYNCED (18s)     SYNCED (18s)     SYNCED (17s)     SYNCED (18s)     IGNORED     istiod-86b6b7ff7-q8gr9     1.26.0
waypoint-66b59898-lx4tc.default                     Kubernetes     SYNCED (17s)     SYNCED (17s)     IGNORED          IGNORED          IGNORED     istiod-86b6b7ff7-q8gr9     1.26.0
ztunnel-df5dn.istio-system                          Kubernetes     IGNORED          IGNORED          IGNORED          IGNORED          IGNORED     istiod-86b6b7ff7-q8gr9     1.26.0
ztunnel-hjzcb.istio-system                          Kubernetes     IGNORED          IGNORED          IGNORED          IGNORED          IGNORED     istiod-86b6b7ff7-q8gr9     1.26.0
ztunnel-nn6z9.istio-system                          Kubernetes     IGNORED          IGNORED          IGNORED          IGNORED          IGNORED     istiod-86b6b7ff7-q8gr9     1.26.0

docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/waypoint                              
RESOURCE NAME     TYPE           STATUS     VALID CERT     SERIAL NUMBER                        NOT AFTER                NOT BEFORE
default           Cert Chain     ACTIVE     true           aec0be95d5bbccfe102f63fcef4e3412     2025-06-07T16:30:42Z     2025-06-06T16:28:42Z
ROOTCA            CA             ACTIVE     true           f73948790621512973e90ca2a2b7e673     2035-06-04T13:34:53Z     2025-06-06T13:34:53Z

#
kubectl pexec waypoint-66b59898-lx4tc -it -T -- bash
----------------------------------------------
ip -c a

curl -s http://localhost:15020/stats/prometheus

ss -tnlp
State                Recv-Q               Send-Q                             Local Address:Port                              Peer Address:Port              Process
LISTEN               0                    4096                                   127.0.0.1:15000                                  0.0.0.0:*                  users:(("envoy",pid=17,fd=18))
LISTEN               0                    4096                                     0.0.0.0:15090                                  0.0.0.0:*                  users:(("envoy",pid=17,fd=21))
LISTEN               0                    4096                                     0.0.0.0:15090                                  0.0.0.0:*                  users:(("envoy",pid=17,fd=20))
LISTEN               0                    4096                                     0.0.0.0:15021                                  0.0.0.0:*                  users:(("envoy",pid=17,fd=23))
LISTEN               0                    4096                                     0.0.0.0:15021                                  0.0.0.0:*                  users:(("envoy",pid=17,fd=22))
LISTEN               0                    4096                                     0.0.0.0:15008                                  0.0.0.0:*                  users:(("envoy",pid=17,fd=35))
LISTEN               0                    4096                                     0.0.0.0:15008                                  0.0.0.0:*                  users:(("envoy",pid=17,fd=34))
LISTEN               0                    4096                                           *:15020                                        *:*                  users:(("pilot-agent",pid=1,fd=11)) 

ss -tnp

ss -xnlp
ss -xnp

exit
----------------------------------------------
```

---
# Kmesh

- ref
	- https://github.com/kmesh-net/kmesh
	- https://jimmysong.io/en/blog/introducing-kmesh-kernel-native-service-mesh/

- **eBPF + 프로그래머블 커널** 기반 고성능 서비스 메시 데이터 플레인
- **Sidecarless 아키텍처** - 애플리케이션 코드 변경 없이 투명한 트래픽 관리
- **Zero Intrusion** - 애플리케이션 컨테이너에 리소스 비용 없음

- 성능 개선
	- **Istio Envoy 대비 5배** 성능 향상 (서비스 간 통신)
	- **Kernel-Native 모드**: 전통적 사이드카 대비 **60% 이상** 지연시간 감소
	- **Dual Engine 모드**: Istio Ambient Mesh 대비 **30%** 지연시간 감소
	- **리소스 사용량 70% 감소** - 사이드카 프록시 제거

- 아키텍처 모드
	- Kernel-Native 모드
		- L4 및 Simple L7(HTTP) 트래픽 거버넌스를 커널로 sink
		- 데이터 경로에서 프록시 레이어 통과 없이 투명한 사이드카리스 서비스 메시 구축
	- Dual-Engine 모드
		- eBPF와 waypoint를 사용하여 L4와 L7 트래픽을 분리 처리
		- 점진적 채택 가능: no mesh → 보안 L4 → 전체 L7 처리

- 주요 구성요소
	- Kmesh Daemon
		- eBPF 프로그램 관리
		- 컨트롤 플레인(Istiod)에서 xDS 구성 구독
		- 관찰 가능성 및 메트릭 수집 처리
	- eBPF Orchestration
		- 커널 레벨에서 트래픽 인터셉션 및 관리
		- L4 로드 밸런싱, 트래픽 암호화/복호화, 모니터링
	- Waypoint Proxy (선택적)
		- 고급 L7 트래픽 거버넌스 처리
		- 네임스페이스 또는 서비스별 배포

## Kmesh Architecture
![]({{ site.url }}/img/post/devops/study/istio/9/20250607014152.png)

https://kmesh.net/docs/setup/quick-start/#deploy-the-sample-applications

> mac M2 docker(kind)에서 NIC eth0이 xdp 미지원으로 샘플 애플리케이션 배포 실패
