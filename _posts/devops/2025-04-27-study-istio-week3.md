---
layout: post
section-type: post
title: ServiceMesh - Istio - Week3
category: devops
tags: ["k8s", "istio", "servicemesh"]
---

# 5. 트래픽 제어: 세밀한 트래픽 라우팅
Istio를 사용해 서비스 간 트래픽을 정밀하게 제어하는 방법을 다룬다. 새 소프트웨어 릴리스의 위험을 줄이고, 복잡한 배포 패턴을 지원할 수 있다.

---
## 새로운 코드 배포의 위험 줄이기

ACME사는 블루/그린 배포를 사용해 서비스 v2(그린)를 기존 v1(블루) 옆에 배포했다.


![]({{ site.url }}/img/post/devops/study/istio/3/20250417212106.png)
트래픽을 v2로 전환하거나, 문제 발생 시 v1으로 빠르게 되돌릴 수 있었다.

하지만 블루/그린 배포만으로는 여전히 '빅뱅 릴리스'의 위험이 있었다. 이를 해결하기 위해 **배포**와 **릴리스**를 분리하는 전략이 필요하다.
### 배포 vs 릴리스
catalog 서비스 v1이 운영 중일 때, 새로운 코드 변경(v1.1)을 추가하려면:
- 빌드하고 태깅한 후 스테이징 환경에 배포
- 검증과 승인을 거친 뒤 운영 환경에 배포

![]({{ site.url }}/img/post/devops/study/istio/3/20250417212755.png)

운영 환경에 새 버전을 설치해도, 트래픽을 연결하지 않으면 사용자에겐 아무 영향이 없다. 운영 환경에서 새 버전의 메트릭과 로그를 수집해 안정성을 검증할 수 있다.

검증이 완료되면 실제 트래픽을 일부 옮겨 **릴리스**를 시작한다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250417213119.png)

처음에는 내부 직원만 신버전을 사용하게 할 수 있다. 이렇게 하면 내부 피드백을 통해 안정성을 검증할 수 있다.

검증 후 무과금 고객이나 실버 등급 고객 등으로 릴리스를 확장해 전체 배포를 완료한다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250417213627.png)

---
### 실습 준비

- kind로 cluster 셋팅
    - [https://raw.githubusercontent.com/KimDoKy/istio-in-action-book-source-code/refs/heads/master/kind_2.sh](https://raw.githubusercontent.com/KimDoKy/istio-in-action-book-source-code/refs/heads/master/kind_2.sh)
- istio 설치 및 추가 설정
    - [https://raw.githubusercontent.com/KimDoKy/istio-in-action-book-source-code/refs/heads/master/install_istio_on_control_plane.sh](https://raw.githubusercontent.com/KimDoKy/istio-in-action-book-source-code/refs/heads/master/install_istio_on_control_plane.sh)
---
## 이스티오로 요청 라우팅하기

catalog 서비스 트래픽을 제어하기 위해 Istio VirtualService를 사용한다. 특정 요청만 신버전으로 보내는 **다크 런치(dark launch)** 기법을 구현할 수 있다.
#### 작업 공간 청소
```bash
k config set-context $(kubectl config current-context) --namespace=istioinaction
k delete deployment,svc,gateway,virtualservice,destinationrule --all -n istioinaction
```
### catalog 서비스 v1 배포

```bash
# Let’s deploy v1 of our catalog service. From the root of the book’s source code, run the following command
kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction

# 확인
kubectl get pod -n istioinaction -owide
NAME                     READY   STATUS    RESTARTS   AGE   IP           NODE                  NOMINATED NODE   READINESS GATES
catalog-6cf4b97d-x45bl   2/2     Running           0          16s   10.10.0.21   myk8s-control-plane   <none>           <none>

# 도메인 질의를 위한 임시 설정 : 실습 완료 후에는 삭제 해둘 것
echo "127.0.0.1       catalog.istioinaction.io" | sudo tee -a /etc/hosts
cat /etc/hosts | tail -n 3

# netshoot로 내부에서 catalog 접속 확인
kubectl exec -it netshoot -- curl -s http://catalog.istioinaction/items | jq

# 외부 노출을 위해 Gateway 설정
cat ch5/catalog-gateway.yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: catalog-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "catalog.istioinaction.io"
    
kubectl apply -f ch5/catalog-gateway.yaml -n istioinaction

# 트래픽을 catalog 서비스로 라우팅하는 VirtualService 리소스 설정
cat ch5/catalog-vs.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog-vs-from-gw
spec:
  hosts:
  - "catalog.istioinaction.io"
  gateways:
  - catalog-gateway
  http:
  - route:
    - destination:
        host: catalog

kubectl apply -f ch5/catalog-vs.yaml -n istioinaction

# 확인
kubectl get gw,vs -n istioinaction

NAME                                          AGE
gateway.networking.istio.io/catalog-gateway   21s

NAME                                                    GATEWAYS              HOSTS                          AGE
virtualservice.networking.istio.io/catalog-vs-from-gw   ["catalog-gateway"]   ["catalog.istioinaction.io"]   11s

# istio-ingressgateway Service(NodePort)에 포트 정보 확인
kubectl get svc -n istio-system istio-ingressgateway -o jsonpath="{.spec.ports}" | jq
[
  {
    "name": "status-port",
    "nodePort": 31674,
    "port": 15021,
    "protocol": "TCP",
    "targetPort": 15021
  },
  {
    "name": "http2",
    "nodePort": 30000, # 순서1
    "port": 80,        
    "protocol": "TCP",
    "targetPort": 8080 # 순서2
  },
  {
    "name": "https",
    "nodePort": 30005,
    "port": 443,
    "protocol": "TCP",
    "targetPort": 8443
  }
]

# 호스트에서 NodePort(Service)로 접속 확인
curl -v -H "Host: catalog.istioinaction.io" http://localhost:30000
kubectl stern -l app=catalog -n istioinaction

open http://localhost:30000
open http://catalog.istioinaction.io:30000
open http://catalog.istioinaction.io:30000/items


# 신규 터미널 : 반복 접속 실행 해두기
while true; do curl -s http://catalog.istioinaction.io:30000/items/ ; sleep 1; echo; done
while true; do curl -s http://catalog.istioinaction.io:30000/items/ -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done
while true; do curl -s http://catalog.istioinaction.io:30000/items/ -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 0.5; echo; done
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426102318.png)

![]({{ site.url }}/img/post/devops/study/istio/3/20250426102151.png)
![]({{ site.url }}/img/post/devops/study/istio/3/20250419225302.png)
![]({{ site.url }}/img/post/devops/study/istio/3/20250426103443.png)

```bash
docker exec -it myk8s-control-plane istioctl proxy-status
NAME                                                  CLUSTER        CDS        LDS        EDS        RDS        ECDS         ISTIOD                      VERSION
catalog-6cf4b97d-x45bl.istioinaction                  Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-wplhm     1.17.8
istio-ingressgateway-996bc6bb6-chtgt.istio-system     Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-wplhm     1.17.8
netshoot.istioinaction                                Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-wplhm     1.17.8

# istio-ingressgateway
## LDS - Listener Discovery Service
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system --port 8080
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system --port 8080 -o json

## RDS - Route Discovery Service
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system --name http.8080 
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system --name http.8080 -o json

## CDS - Cluseter Discovery Service
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local -o json

## EDS - Endpoint Discovery Service
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||catalog.istioinaction.svc.cluster.local'
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||catalog.istioinaction.svc.cluster.local' -o json

# catalog
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250414220809.png)
LDS(Listener)
![]({{ site.url }}/img/post/devops/study/istio/3/20250426102458.png)
RDS(Routes)
![]({{ site.url }}/img/post/devops/study/istio/3/20250426102619.png)
CDS(Cluster)
![]({{ site.url }}/img/post/devops/study/istio/3/20250426102723.png)
EDS(Endpoint)
![]({{ site.url }}/img/post/devops/study/istio/3/20250426102836.png)
```bash
# catalog's xDS
$ docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/catalog.istioinaction
ADDRESS      PORT  MATCH                                                                                           DESTINATION
10.200.1.10  53    ALL                                                                                             Cluster: outbound|53||kube-dns.kube-system.svc.cluster.local
0.0.0.0      80    Trans: raw_buffer; App: http/1.1,h2c                                                            Route: 80
0.0.0.0      80    ALL                                                                                             PassthroughCluster
10.200.1.1   443   ALL                                                                                             Cluster: outbound|443||kubernetes.default.svc.cluster.local
10.200.1.172 443   ALL                                                                                             Cluster: outbound|443||istiod.istio-system.svc.cluster.local
10.200.1.199 443   ALL                                                                                             Cluster: outbound|443||istio-ingressgateway.istio-system.svc.cluster.local
10.200.1.214 443   ALL                                                                                             Cluster: outbound|443||metrics-server.kube-system.svc.cluster.local
10.200.1.59  3000  Trans: raw_buffer; App: http/1.1,h2c                                                            Route: grafana.istio-system.svc.cluster.local:3000
10.200.1.59  3000  ALL                                                                                             Cluster: outbound|3000||grafana.istio-system.svc.cluster.local
0.0.0.0      9090  Trans: raw_buffer; App: http/1.1,h2c                                                            Route: 9090
0.0.0.0      9090  ALL                                                                                             PassthroughCluster
10.200.1.10  9153  Trans: raw_buffer; App: http/1.1,h2c                                                            Route: kube-dns.kube-system.svc.cluster.local:9153
10.200.1.10  9153  ALL                                                                                             Cluster: outbound|9153||kube-dns.kube-system.svc.cluster.local
0.0.0.0      9411  Trans: raw_buffer; App: http/1.1,h2c                                                            Route: 9411
0.0.0.0      9411  ALL                                                                                             PassthroughCluster
10.200.1.75  14250 Trans: raw_buffer; App: http/1.1,h2c                                                            Route: jaeger-collector.istio-system.svc.cluster.local:14250
10.200.1.75  14250 ALL                                                                                             Cluster: outbound|14250||jaeger-collector.istio-system.svc.cluster.local
10.200.1.75  14268 Trans: raw_buffer; App: http/1.1,h2c                                                            Route: jaeger-collector.istio-system.svc.cluster.local:14268
10.200.1.75  14268 ALL                                                                                             Cluster: outbound|14268||jaeger-collector.istio-system.svc.cluster.local
0.0.0.0      15001 ALL                                                                                             PassthroughCluster
0.0.0.0      15001 Addr: *:15001                                                                                   Non-HTTP/Non-TCP
0.0.0.0      15006 Addr: *:15006                                                                                   Non-HTTP/Non-TCP
0.0.0.0      15006 Trans: tls; App: istio-http/1.0,istio-http/1.1,istio-h2; Addr: 0.0.0.0/0                        InboundPassthroughClusterIpv4
0.0.0.0      15006 Trans: raw_buffer; App: http/1.1,h2c; Addr: 0.0.0.0/0                                           InboundPassthroughClusterIpv4
0.0.0.0      15006 Trans: tls; App: TCP TLS; Addr: 0.0.0.0/0                                                       InboundPassthroughClusterIpv4
0.0.0.0      15006 Trans: raw_buffer; Addr: 0.0.0.0/0                                                              InboundPassthroughClusterIpv4
0.0.0.0      15006 Trans: tls; Addr: 0.0.0.0/0                                                                     InboundPassthroughClusterIpv4
0.0.0.0      15006 Trans: tls; App: istio,istio-peer-exchange,istio-http/1.0,istio-http/1.1,istio-h2; Addr: *:3000 Cluster: inbound|3000||
0.0.0.0      15006 Trans: raw_buffer; Addr: *:3000                                                                 Cluster: inbound|3000||
0.0.0.0      15010 Trans: raw_buffer; App: http/1.1,h2c                                                            Route: 15010
0.0.0.0      15010 ALL                                                                                             PassthroughCluster
10.200.1.172 15012 ALL                                                                                             Cluster: outbound|15012||istiod.istio-system.svc.cluster.local
0.0.0.0      15014 Trans: raw_buffer; App: http/1.1,h2c                                                            Route: 15014
0.0.0.0      15014 ALL                                                                                             PassthroughCluster
0.0.0.0      15021 ALL                                                                                             Inline Route: /healthz/ready*
10.200.1.199 15021 Trans: raw_buffer; App: http/1.1,h2c                                                            Route: istio-ingressgateway.istio-system.svc.cluster.local:15021
10.200.1.199 15021 ALL                                                                                             Cluster: outbound|15021||istio-ingressgateway.istio-system.svc.cluster.local
0.0.0.0      15090 ALL                                                                                             Inline Route: /stats/prometheus*
0.0.0.0      16685 Trans: raw_buffer; App: http/1.1,h2c                                                            Route: 16685
0.0.0.0      16685 ALL                                                                                             PassthroughCluster
0.0.0.0      20001 Trans: raw_buffer; App: http/1.1,h2c                                                            Route: 20001
0.0.0.0      20001 ALL                                                                                             PassthroughCluster

$ docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction
NAME                                                          DOMAINS                                             MATCH                  VIRTUAL SERVICE
80                                                            catalog, catalog.istioinaction + 1 more...          /*
80                                                            istio-ingressgateway.istio-system, 10.200.1.199     /*
80                                                            tracing.istio-system, 10.200.1.157                  /*
9090                                                          kiali.istio-system, 10.200.1.111                    /*
9090                                                          prometheus.istio-system, 10.200.1.248               /*
9411                                                          jaeger-collector.istio-system, 10.200.1.75          /*
9411                                                          zipkin.istio-system, 10.200.1.12                    /*
istio-ingressgateway.istio-system.svc.cluster.local:15021     *                                                   /*
15014                                                         istiod.istio-system, 10.200.1.172                   /*
grafana.istio-system.svc.cluster.local:3000                   *                                                   /*
15010                                                         istiod.istio-system, 10.200.1.172                   /*
jaeger-collector.istio-system.svc.cluster.local:14250         *                                                   /*
20001                                                         kiali.istio-system, 10.200.1.111                    /*
jaeger-collector.istio-system.svc.cluster.local:14268         *                                                   /*
kube-dns.kube-system.svc.cluster.local:9153                   *                                                   /*
16685                                                         tracing.istio-system, 10.200.1.157                  /*
InboundPassthroughClusterIpv4                                 *                                                   /*
                                                              *                                                   /stats/prometheus*
InboundPassthroughClusterIpv4                                 *                                                   /*
inbound|3000||                                                *                                                   /*
                                                              *                                                   /healthz/ready*
inbound|3000||                                                *                                                   /*

$ docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction
SERVICE FQDN                                            PORT      SUBSET     DIRECTION     TYPE             DESTINATION RULE
                                                        3000      -          inbound       ORIGINAL_DST
BlackHoleCluster                                        -         -          -             STATIC
InboundPassthroughClusterIpv4                           -         -          -             ORIGINAL_DST
PassthroughCluster                                      -         -          -             ORIGINAL_DST
agent                                                   -         -          -             STATIC
catalog.istioinaction.svc.cluster.local                 80        -          outbound      EDS
grafana.istio-system.svc.cluster.local                  3000      -          outbound      EDS
istio-ingressgateway.istio-system.svc.cluster.local     80        -          outbound      EDS
istio-ingressgateway.istio-system.svc.cluster.local     443       -          outbound      EDS
istio-ingressgateway.istio-system.svc.cluster.local     15021     -          outbound      EDS
istiod.istio-system.svc.cluster.local                   443       -          outbound      EDS
istiod.istio-system.svc.cluster.local                   15010     -          outbound      EDS
istiod.istio-system.svc.cluster.local                   15012     -          outbound      EDS
istiod.istio-system.svc.cluster.local                   15014     -          outbound      EDS
jaeger-collector.istio-system.svc.cluster.local         9411      -          outbound      EDS
jaeger-collector.istio-system.svc.cluster.local         14250     -          outbound      EDS
jaeger-collector.istio-system.svc.cluster.local         14268     -          outbound      EDS
kiali.istio-system.svc.cluster.local                    9090      -          outbound      EDS
kiali.istio-system.svc.cluster.local                    20001     -          outbound      EDS
kube-dns.kube-system.svc.cluster.local                  53        -          outbound      EDS
kube-dns.kube-system.svc.cluster.local                  9153      -          outbound      EDS
kubernetes.default.svc.cluster.local                    443       -          outbound      EDS
metrics-server.kube-system.svc.cluster.local            443       -          outbound      EDS
prometheus.istio-system.svc.cluster.local               9090      -          outbound      EDS
prometheus_stats                                        -         -          -             STATIC
sds-grpc                                                -         -          -             STATIC
tracing.istio-system.svc.cluster.local                  80        -          outbound      EDS
tracing.istio-system.svc.cluster.local                  16685     -          outbound      EDS
xds-grpc                                                -         -          -             STATIC
zipkin                                                  -         -          -             STRICT_DNS
zipkin.istio-system.svc.cluster.local                   9411      -          outbound      EDS

$ docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction
ENDPOINT                                                STATUS      OUTLIER CHECK     CLUSTER
10.10.0.15:15010                                        HEALTHY     OK                outbound|15010||istiod.istio-system.svc.cluster.local
10.10.0.15:15012                                        HEALTHY     OK                outbound|15012||istiod.istio-system.svc.cluster.local
10.10.0.15:15014                                        HEALTHY     OK                outbound|15014||istiod.istio-system.svc.cluster.local
10.10.0.15:15017                                        HEALTHY     OK                outbound|443||istiod.istio-system.svc.cluster.local
10.10.0.16:8080                                         HEALTHY     OK                outbound|80||istio-ingressgateway.istio-system.svc.cluster.local
10.10.0.16:8443                                         HEALTHY     OK                outbound|443||istio-ingressgateway.istio-system.svc.cluster.local
10.10.0.16:15021                                        HEALTHY     OK                outbound|15021||istio-ingressgateway.istio-system.svc.cluster.local
10.10.0.17:3000                                         HEALTHY     OK                outbound|3000||grafana.istio-system.svc.cluster.local
10.10.0.18:9090                                         HEALTHY     OK                outbound|9090||prometheus.istio-system.svc.cluster.local
10.10.0.19:9411                                         HEALTHY     OK                outbound|9411||jaeger-collector.istio-system.svc.cluster.local
10.10.0.19:9411                                         HEALTHY     OK                outbound|9411||zipkin.istio-system.svc.cluster.local
10.10.0.19:14250                                        HEALTHY     OK                outbound|14250||jaeger-collector.istio-system.svc.cluster.local
10.10.0.19:14268                                        HEALTHY     OK                outbound|14268||jaeger-collector.istio-system.svc.cluster.local
10.10.0.19:16685                                        HEALTHY     OK                outbound|16685||tracing.istio-system.svc.cluster.local
10.10.0.19:16686                                        HEALTHY     OK                outbound|80||tracing.istio-system.svc.cluster.local
10.10.0.2:53                                            HEALTHY     OK                outbound|53||kube-dns.kube-system.svc.cluster.local
10.10.0.2:9153                                          HEALTHY     OK                outbound|9153||kube-dns.kube-system.svc.cluster.local
10.10.0.20:9090                                         HEALTHY     OK                outbound|9090||kiali.istio-system.svc.cluster.local
10.10.0.20:20001                                        HEALTHY     OK                outbound|20001||kiali.istio-system.svc.cluster.local
10.10.0.21:3000                                         HEALTHY     OK                inbound|3000||
10.10.0.21:3000                                         HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local
10.10.0.4:53                                            HEALTHY     OK                outbound|53||kube-dns.kube-system.svc.cluster.local
10.10.0.4:9153                                          HEALTHY     OK                outbound|9153||kube-dns.kube-system.svc.cluster.local
10.10.0.5:10250                                         HEALTHY     OK                outbound|443||metrics-server.kube-system.svc.cluster.local
10.200.1.12:9411                                        HEALTHY     OK                zipkin
127.0.0.1:15000                                         HEALTHY     OK                prometheus_stats
127.0.0.1:15020                                         HEALTHY     OK                agent
172.18.0.2:6443                                         HEALTHY     OK                outbound|443||kubernetes.default.svc.cluster.local
unix://./etc/istio/proxy/XDS                            HEALTHY     OK                xds-grpc
unix://./var/run/secrets/workload-spiffe-uds/socket     HEALTHY     OK                sds-grpc
```

```bash
# 신규 터미널 : istio-ingressgateway 파드
kubectl port-forward deploy/istio-ingressgateway -n istio-system 15000:15000

# 
open http://127.0.0.1:15000
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426103237.png)
### catalog 서비스 v2 배포

```bash
# catalog 서비스 v2 를 배포 : v2에서는 imageUrl 필드가 추가
kubectl apply -f services/catalog/kubernetes/catalog-deployment-v2.yaml -n istioinaction

kubectl get deploy -n istioinaction --show-labels
NAME         READY   UP-TO-DATE   AVAILABLE   AGE   LABELS
catalog      1/1     1            1           30m   app=catalog,version=v1
catalog-v2   1/1     1            1           34s   app=catalog,version=v2

kubectl get pod -n istioinaction -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE                  NOMINATED NODE   READINESS GATES
catalog-6cf4b97d-ftl77        2/2     Running   0          43m   10.10.0.14   myk8s-control-plane   <none>           <none>
catalog-v2-6df885b555-6hmcl   2/2     Running   0          13m   10.10.0.15   myk8s-control-plane   <none>           <none>

docker exec -it myk8s-control-plane istioctl proxy-status
NAME                                                  CLUSTER        CDS        LDS        EDS        RDS        ECDS         ISTIOD                      VERSION
catalog-6cf4b97d-ftl77.istioinaction                  Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-fl492     1.17.8
catalog-v2-6df885b555-6hmcl.istioinaction             Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-fl492     1.17.8
istio-ingressgateway-996bc6bb6-zvtdc.istio-system     Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-fl492     1.17.8

# 호출 테스트 : v1 , v2 호출 확인
for i in {1..10}; do curl -s http://catalog.istioinaction.io:30000/items/ ; printf "\n\n"; done

# istio-ingressgateway proxy-config 확인
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local -o json
...
        "name": "outbound|80||catalog.istioinaction.svc.cluster.local",
        "type": "EDS",
        "edsClusterConfig": {
            "edsConfig": {
                "ads": {},
                "initialFetchTimeout": "0s",
                "resourceApiVersion": "V3"
            },
            "serviceName": "outbound|80||catalog.istioinaction.svc.cluster.local"
        },
        "connectTimeout": "10s",
        "lbPolicy": "LEAST_REQUEST",
        "circuitBreakers": {
            "thresholds": [
                {
                    "maxConnections": 4294967295,
                    "maxPendingRequests": 4294967295,
                    "maxRequests": 4294967295,
                    "maxRetries": 4294967295,
                    "trackRemaining": true
                }
            ]
        },
        "commonLbConfig": {
            "localityWeightedLbConfig": {}
        },
...

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||catalog.istioinaction.svc.cluster.local'
ENDPOINT            STATUS      OUTLIER CHECK     CLUSTER
10.10.0.21:3000     HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local
10.10.0.27:3000     HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||catalog.istioinaction.svc.cluster.local' -o json
...
   {
        "name": "outbound|80||catalog.istioinaction.svc.cluster.local",
        "addedViaApi": true,
        "hostStatuses": [
            {
                "address": {
                    "socketAddress": {
                        "address": "10.10.0.14",
                        "portValue": 3000
                    }
                },
                "stats": [
                    {
                        "name": "cx_connect_fail"
                    },
                    {
                        "value": "8",
                        "name": "cx_total"
                    },
                    {
                        "name": "rq_error"
                    },
                    {
                        "value": "315",
                        "name": "rq_success"
                    },
                    {
                        "name": "rq_timeout"
                    },
                    {
                        "value": "315",
                        "name": "rq_total"
                    },
                    {
                        "type": "GAUGE",
                        "value": "8",
                        "name": "cx_active"
                    },
                    {
                        "type": "GAUGE",
                        "name": "rq_active"
                    }
                ],
                "healthStatus": {
                    "edsHealthStatus": "HEALTHY"
                },
                "weight": 1,
                "locality": {}
            },
            {
                "address": {
                    "socketAddress": {
                        "address": "10.10.0.15",
                        "portValue": 3000
                    }
                },
                "stats": [
                    {
                        "name": "cx_connect_fail"
                    },
                    {
                        "value": "8",
                        "name": "cx_total"
                    },
                    {
                        "name": "rq_error"
                    },
                    {
                        "value": "308",
                        "name": "rq_success"
                    },
                    {
                        "name": "rq_timeout"
                    },
                    {
                        "value": "308",
                        "name": "rq_total"
                    },
                    {
                        "type": "GAUGE",
                        "value": "8",
                        "name": "cx_active"
                    },
                    {
                        "type": "GAUGE",
                        "name": "rq_active"
                    }
                ],
                "healthStatus": {
                    "edsHealthStatus": "HEALTHY"
                },
                "weight": 1,
                "locality": {}
            }
        ],
        "circuitBreakers": {
            "thresholds": [
                {
                    "maxConnections": 4294967295,
                    "maxPendingRequests": 4294967295,
                    "maxRequests": 4294967295,
                    "maxRetries": 4294967295
                },
                {
                    "priority": "HIGH",
                    "maxConnections": 1024,
                    "maxPendingRequests": 1024,
                    "maxRequests": 1024,
                    "maxRetries": 3
                }
            ]
        },
        "observabilityName": "outbound|80||catalog.istioinaction.svc.cluster.local",
        "edsServiceName": "outbound|80||catalog.istioinaction.svc.cluster.local"
    },
...

# catalog proxy-config 도 직접 확인해보자
$ docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction --cluster 'outbound|80||catalog.istioinaction.svc.cluster.local'
ENDPOINT            STATUS      OUTLIER CHECK     CLUSTER
10.10.0.21:3000     HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local
10.10.0.27:3000     HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local
```

![]({{ site.url }}/img/post/devops/study/istio/3/20250426104619.png)
![]({{ site.url }}/img/post/devops/study/istio/3/20250426113535.png)
### 모든 트래픽을 v1으로 라우팅
![]({{ site.url }}/img/post/devops/study/istio/3/20250419230133.png)
```bash
kubectl get pod -l app=catalog -n istioinaction --show-labels
NAME                          READY   STATUS    RESTARTS   AGE   LABELS
catalog-6cf4b97d-x45bl        2/2     Running   0          90m   app=catalog,pod-template-hash=6cf4b97d,security.istio.io/tlsMode=istio,service.istio.io/canonical-name=catalog,service.istio.io/canonical-revision=v1,version=v1
catalog-v2-6df885b555-kcvhl   2/2     Running   0          52m   app=catalog,pod-template-hash=6df885b555,security.istio.io/tlsMode=istio,service.istio.io/canonical-name=catalog,service.istio.io/canonical-revision=v2,version=v2

cat ch5/catalog-dest-rule.yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: catalog
spec:
  host: catalog.istioinaction.svc.cluster.local
  subsets:
  - name: version-v1
    labels:
      version: v1
  - name: version-v2
    labels:
      version: v2

kubectl apply -f ch5/catalog-dest-rule.yaml -n istioinaction

# 확인
kubectl get destinationrule -n istioinaction
NAME      HOST                                      AGE
catalog   catalog.istioinaction.svc.cluster.local   5s

# catalog proxy-config 확인 : SUBSET(v1, v2, -) 확인
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local
SERVICE FQDN                                PORT     SUBSET         DIRECTION     TYPE     DESTINATION RULE
catalog.istioinaction.svc.cluster.local     80       -              outbound      EDS      catalog.istioinaction
catalog.istioinaction.svc.cluster.local     80       version-v1     outbound      EDS      catalog.istioinaction
catalog.istioinaction.svc.cluster.local     80       version-v2     outbound      EDS      catalog.istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --subset version-v1 -o json
...
        "name": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local",
        "type": "EDS",
        "edsClusterConfig": {
            "edsConfig": {
                "ads": {},
                "initialFetchTimeout": "0s",
                "resourceApiVersion": "V3"
            },
            "serviceName": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local"
        },
        "connectTimeout": "10s",
        "lbPolicy": "LEAST_REQUEST",
...

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --subset version-v2 -o json
...
        "name": "outbound|80|version-v2|catalog.istioinaction.svc.cluster.local",
        "type": "EDS",
        "edsClusterConfig": {
            "edsConfig": {
                "ads": {},
                "initialFetchTimeout": "0s",
                "resourceApiVersion": "V3"
            },
            "serviceName": "outbound|80|version-v2|catalog.istioinaction.svc.cluster.local"
        },
        "connectTimeout": "10s",
        "lbPolicy": "LEAST_REQUEST",
...

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local -o json
...
        "name": "outbound|80||catalog.istioinaction.svc.cluster.local",
        "type": "EDS",
        "edsClusterConfig": {
            "edsConfig": {
                "ads": {},
                "initialFetchTimeout": "0s",
                "resourceApiVersion": "V3"
            },
            "serviceName": "outbound|80||catalog.istioinaction.svc.cluster.local"
        },
...

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system | egrep 'ENDPOINT|istioinaction'
ENDPOINT                                                STATUS      OUTLIER CHECK     CLUSTER
10.10.0.21:3000                                         HEALTHY     OK                outbound|80|version-v1|catalog.istioinaction.svc.cluster.local
10.10.0.21:3000                                         HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local
10.10.0.27:3000                                         HEALTHY     OK                outbound|80|version-v2|catalog.istioinaction.svc.cluster.local
10.10.0.27:3000                                         HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80|version-v1|catalog.istioinaction.svc.cluster.local'
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80|version-v1|catalog.istioinaction.svc.cluster.local' -o json
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80|version-v2|catalog.istioinaction.svc.cluster.local'
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80|version-v2|catalog.istioinaction.svc.cluster.local' -o json
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||catalog.istioinaction.svc.cluster.local'
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426114144.png)
```bash
# VirtualService 수정 (subset 추가)
cat ch5/catalog-vs-v1.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog-vs-from-gw
spec:
  hosts:
  - "catalog.istioinaction.io"
  gateways:
  - catalog-gateway
  http:
  - route:
    - destination:
        host: catalog
        subset: version-v1

kubectl apply -f ch5/catalog-vs-v1.yaml -n istioinaction

# 호출 테스트 : v1
for i in {1..10}; do curl -s http://catalog.istioinaction.io:30000/items/ ; printf "\n\n"; done


# 세부 정보 확인
# routes 에 virtualHosts 항목에 routes.route 에 cluster 부분이 ...version-v1... 설정 확인
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system --name http.8080 -o json
...
        "virtualHosts": [
            {
                "name": "catalog.istioinaction.io:80",
                "domains": [
                    "catalog.istioinaction.io"
                ],
                "routes": [
                    {
                        "match": {
                            "prefix": "/"
                        },
                        "route": {
                            "cluster": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local",
                            "timeout": "0s",
                            "retryPolicy": {
                                "retryOn": "connect-failure,refused-stream,unavailable,cancelled,retriable-status-codes",
                                "numRetries": 2,
...

# cluster 
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --subset version-v1
SERVICE FQDN                                PORT     SUBSET         DIRECTION     TYPE     DESTINATION RULE
catalog.istioinaction.svc.cluster.local     80       version-v1     outbound      EDS      catalog.istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --subset version-v1 -o json
...
        "name": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local",
        "type": "EDS",
        "edsClusterConfig": {
            "edsConfig": {
                "ads": {},
                "initialFetchTimeout": "0s",
                "resourceApiVersion": "V3"
            },
            "serviceName": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local"
        },
        ...
        "metadata": {
            "filterMetadata": {
                "istio": {
                    "config": "/apis/networking.istio.io/v1alpha3/namespaces/istioinaction/destination-rule/catalog",
                    "default_original_port": 80,
                    "services": [
                        {
                            "host": "catalog.istioinaction.svc.cluster.local",
                            "name": "catalog",
                            "namespace": "istioinaction"
                        }
                    ],
                    "subset": "version-v1"
...

# endpoint 
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system | egrep 'ENDPOINT|istioinaction'
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80|version-v1|catalog.istioinaction.svc.cluster.local'
ENDPOINT            STATUS      OUTLIER CHECK     CLUSTER
10.10.0.16:3000     HEALTHY     OK                outbound|80|version-v1|catalog.istioinaction.svc.cluster.local

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80|version-v1|catalog.istioinaction.svc.cluster.local' -o json
...

# istio-proxy (catalog)
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction --subset version-v1 -o json
...
        "metadata": {
            "filterMetadata": {
                "istio": {
                    "config": "/apis/networking.istio.io/v1alpha3/namespaces/istioinaction/destination-rule/catalog",
                    "default_original_port": 80,
                    "services": [
                        {
                            "host": "catalog.istioinaction.svc.cluster.local",
                            "name": "catalog",
                            "namespace": "istioinaction"
                        }
                    ],
                    "subset": "version-v1"
                }
            }
        },
...

```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426114338.png)
### 특정 요청을 v2로 라우팅
![]({{ site.url }}/img/post/devops/study/istio/3/20250419230525.png)
- HTTP 요청 헤더를 `x-istio-cohort: internal`를 포함한 트래픽은 v2로 보낸다.

```bash
cat ch5/catalog-vs-v2-request.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog-vs-from-gw
spec:
  hosts:
  - "catalog.istioinaction.io"
  gateways:
  - catalog-gateway
  http:
  - match:
    - headers:
        x-istio-cohort:
          exact: "internal"
    route:
    - destination:
        host: catalog
        subset: version-v2
  - route:
    - destination:
        host: catalog
        subset: version-v1

kubectl apply -f ch5/catalog-vs-v2-request.yaml -n istioinaction

# 호출 테스트 : 여전히 v1
for i in {1..10}; do curl -s http://catalog.istioinaction.io:30000/items/ ; printf "\n\n"; done

# 요청 헤더 포함 호출 테스트 : v2!
curl http://catalog.istioinaction.io:30000/items -H "x-istio-cohort: internal"

# (옵션) 신규 터미널 : v2 반복 접속
while true; do curl -s http://catalog.istioinaction.io:30000/items/ -H "x-istio-cohort: internal" -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 2; echo; done


# 상세 확인
# route 추가 : routes 에 2개의 route 확인 - 위에서 부터 적용되는 순서 중요!
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system --name http.8080
NAME          DOMAINS                      MATCH     VIRTUAL SERVICE
http.8080     catalog.istioinaction.io     /*        catalog-vs-from-gw.istioinaction
http.8080     catalog.istioinaction.io     /*        catalog-vs-from-gw.istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system --name http.8080 -o json
...
        "virtualHosts": [
            {
                "name": "catalog.istioinaction.io:80",
                "domains": [
                    "catalog.istioinaction.io"
                ],
                "routes": [
                    {
                        "match": {
                            "prefix": "/",
                            "caseSensitive": true,
                            "headers": [
                                {
                                    "name": "x-istio-cohort",
                                    "stringMatch": {
                                        "exact": "internal"
                                    }
                                }
                            ]
                        },
                        "route": {
                            "cluster": "outbound|80|version-v2|catalog.istioinaction.svc.cluster.local",
                            "timeout": "0s",
                ...
                   {
                        "match": {
                            "prefix": "/"
                        },
                        "route": {
                            "cluster": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local",
...

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system | egrep 'ENDPOINT|istioinaction'

# istio-proxy (catalog)에는 routes 정보가 아래 cluster 로 보내는 1개만 있다. 즉 istio-proxy(istio-ingressgateway)가 routes 분기 처리하는 것을 알 수 있다.
## "cluster": "outbound|80||catalog.istioinaction.svc.cluster.local"
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction --name 80 -o json
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction | grep catalog
80                                                            catalog, catalog.istioinaction + 1 more...          /*
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426120445.png)
### 호출 그래프 내 깊은 위치에서 라우팅

![]({{ site.url }}/img/post/devops/study/istio/3/20250419230637.png)

```bash
# 초기화
kubectl delete gateway,virtualservice,destinationrule --all -n istioinaction

# webapp 기동
kubectl apply -n istioinaction -f services/webapp/kubernetes/webapp.yaml
kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction # 이미 배포 상태
kubectl apply -f services/catalog/kubernetes/catalog-deployment-v2.yaml -n istioinaction # 이미 배포 상태

# 확인
kubectl get deploy,pod,svc,ep -n istioinaction
NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/catalog      1/1     1            1           55m
deployment.apps/catalog-v2   1/1     1            1           48m
deployment.apps/webapp       1/1     1            1           42s

NAME                              READY   STATUS    RESTARTS   AGE
pod/catalog-6cf4b97d-x45bl        2/2     Running   0          55m
pod/catalog-v2-6df885b555-kcvhl   2/2     Running   0          48m
pod/webapp-7685bcb84-dhprj        2/2     Running   0          42s

NAME              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/catalog   ClusterIP   10.200.1.229   <none>        80/TCP    55m
service/webapp    ClusterIP   10.200.1.113   <none>        80/TCP    42s

NAME                ENDPOINTS                         AGE
endpoints/catalog   10.10.0.21:3000,10.10.0.27:3000   55m
endpoints/webapp    10.10.0.28:8080                   42s
```

- GW, VS 설정 후 호출 테스트: webapp -> catalog는 k8s service(clusterIP) 라우팅 사용

```bash
# Now, set up the Istio ingress gateway to route to the webapp service
cat services/webapp/istio/webapp-catalog-gw-vs.yaml
---
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: coolstore-gateway
spec:
  selector:
    istio: ingressgateway # use istio default controller
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "webapp.istioinaction.io"
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: webapp-virtualservice
spec:
  hosts:
  - "webapp.istioinaction.io"
  gateways:
  - coolstore-gateway
  http:
  - route:
    - destination:
        host: webapp
        port:
          number: 80

kubectl apply -f services/webapp/istio/webapp-catalog-gw-vs.yaml -n istioinaction

# 확인
kubectl get gw,vs -n istioinaction
NAME                                            AGE
gateway.networking.istio.io/coolstore-gateway   3s

NAME                                                       GATEWAYS                HOSTS                         AGE
virtualservice.networking.istio.io/webapp-virtualservice   ["coolstore-gateway"]   ["webapp.istioinaction.io"]   3s

# 도메인 질의를 위한 임시 설정 : 실습 완료 후에는 삭제 해둘 것
echo "127.0.0.1       webapp.istioinaction.io" | sudo tee -a /etc/hosts
cat /etc/hosts | tail -n 3

# 호출테스트 : 외부(web, curl) → ingressgw → webapp → catalog (v1, v2)
curl -s http://webapp.istioinaction.io:30000/api/catalog | jq

# 반복 호출테스트 : 신규터미널 2개에 아래 각각 실행 해두기
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog -H "x-istio-cohort: internal" -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 2; echo; done

# proxy-config : istio-ingressgateway
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system --name http.8080 
NAME          DOMAINS                     MATCH     VIRTUAL SERVICE
http.8080     webapp.istioinaction.io     /*        webapp-virtualservice.istioinaction
=> route."cluster": "outbound|80||webapp.istioinaction.svc.cluster.local"

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system | egrep 'webapp|catalog'
catalog.istioinaction.svc.cluster.local                 80        -          outbound      EDS            
webapp.istioinaction.svc.cluster.local                  80        -          outbound      EDS

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn webapp.istioinaction.svc.cluster.local -o json
...
        "name": "outbound|80||webapp.istioinaction.svc.cluster.local",
        "type": "EDS",
...

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system --cluster 'outbound|80||webapp.istioinaction.svc.cluster.local'
ENDPOINT            STATUS      OUTLIER CHECK     CLUSTER
10.10.0.28:8080     HEALTHY     OK                outbound|80||webapp.istioinaction.svc.cluster.local

# proxy-config : webapp
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/webapp.istioinaction
...
## 80번 포트에서 HTTP/1.1, h2c 트래픽 수신
## raw_buffer: TLS 종료 없이 평문 통신 사용
## webapp의 아웃바운드 트래픽이 암호화되지 않은 상태로 catalog로 전송
0.0.0.0      80    Trans: raw_buffer; App: http/1.1,h2c  Route: 80
...
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction
...
## 모든 경로(/*)에 대해 기본 라우팅 적용
## VS 미설정 상태
80 webapp, webapp.istioinaction + 1 more...      /*
...
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction
...
## 클러스터 포트 80
catalog.istioinaction.svc.cluster.local 80 -  outbound      EDS
...
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction
...
## 2개의 정상 파드에 로드밸런싱
## 서비스의 80포트 -> 파드의 30000포트
10.10.0.21:3000 HEALTHY OK outbound|80||catalog.istioinaction.svc.cluster.local
10.10.0.27:3000 HEALTHY OK outbound|80||catalog.istioinaction.svc.cluster.local
...

# proxy-config : catalog
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/catalog.istioinaction
...
## 3000번 포트에서 HTTP 트래픽 수신
0.0.0.0      15006 Trans: tls; App: istio-http/1.0,istio-http/1.1,istio-h2; Addr: 0.0.0.0/0 InboundPassthroughClusterIpv4
...
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction


# webapp istio-proxy 로그 활성화
# 신규 터미널
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f

# webapp istio-proxy 로그 활성화 적용
cat << EOF | kubectl apply -f -
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: webapp
  namespace: istioinaction
spec:
  selector:
    matchLabels:
      app: webapp
  accessLogging:
  - providers:
    - name: envoy #2 액세스 로그를 위한 프로바이더 설정
    disabled: false #3 disable 를 false 로 설정해 활성화한다
EOF

# webapp → catalog 는 k8s service(clusterIP) 라우팅 사용 확인!
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426125903.png)
```
/items
webapp 서비스가 catalog 서비스로 HTTP 요청을 보냄
Envoy는 catalog.istioinaction이라는 k8s catalog 서비스(clusterIP 10.200.1.299:80)로 라우팅하고, 실제 Pod IP는 10.10.0.21:3000으로 연결됨
/api/catalog
이 로그는 webapp 서비스의 사이드카 클라이언트로부터 직접 HTTP 요청을 받음
이 요청을 10.10.0.28:8080(webapp 서비스의 실제 컨테이너)으로 보냄
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426121847.png)
- catalog의 v1으로 모든 트래픽을을 라우팅하는 VS,DR 생성

```bash
cat ch5/catalog-dest-rule.yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: catalog
spec:
  host: catalog.istioinaction.svc.cluster.local
  subsets:
  - name: version-v1
    labels:
      version: v1
  - name: version-v2
    labels:
      version: v2
      
kubectl apply -f ch5/catalog-dest-rule.yaml -n istioinaction

# istio-proxy
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn catalog.istioinaction.svc.cluster.local
SERVICE FQDN                                PORT     SUBSET         DIRECTION     TYPE     DESTINATION RULE
catalog.istioinaction.svc.cluster.local     80       -              outbound      EDS      catalog.istioinaction
catalog.istioinaction.svc.cluster.local     80       version-v1     outbound      EDS      catalog.istioinaction
catalog.istioinaction.svc.cluster.local     80       version-v2     outbound      EDS      catalog.istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system | egrep 'ENDPOINT|istioinaction'
ENDPOINT                                                STATUS      OUTLIER CHECK     CLUSTER
10.10.0.16:3000                                         HEALTHY     OK                outbound|80|version-v1|catalog.istioinaction.svc.cluster.local
10.10.0.16:3000                                         HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local
10.10.0.17:3000                                         HEALTHY     OK                outbound|80|version-v2|catalog.istioinaction.svc.cluster.local
10.10.0.17:3000                                         HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local
10.10.0.18:8080                                         HEALTHY     OK                outbound|80||webapp.istioinaction.svc.cluster.local

cat ch5/catalog-vs-v1-mesh.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog
spec:
  hosts:
  - catalog
  gateways: # 만약, gateways 부분을 제외하고 배포하면 암묵적으로 mesh gateways가 적용됨.
    - mesh  # VirtualService는 메시 내의 모든 사이드카(현재 webapp, catalog)에 적용된다. edge는 제외.
  http:
  - route:
    - destination:
        host: catalog
        subset: version-v1

kubectl apply -f ch5/catalog-vs-v1-mesh.yaml -n istioinaction

# VirtualService 확인 : GATEWAYS 에 mesh 확인
kubectl get vs -n istioinaction
NAME                    GATEWAYS                HOSTS                         AGE
catalog                 ["mesh"]                ["catalog"]                   12s
webapp-virtualservice   ["coolstore-gateway"]   ["webapp.istioinaction.io"]   28s


# 반복 호출테스트 : 신규터미널 2개에 아래 각각 실행 해두기 >> 현재는 v1만 라우팅 처리
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog -H "x-istio-cohort: internal" -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 2; echo; done


# webapp → catalog 호출도 istio 의 DestinationRule 라우팅 전달 처리! : 신규터미널
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426130908.png)
> 이 로그는 webapp이 내부적으로 catalog 서비스를 호출하는 로그
> version-v1이라는 subset으로 요청이 라우팅 됨
> 이는 DR에서 `subset: version-v1`으로 정의된 엔드포인트로 라우팅이 잘 되었다는 의미

```bash
# proxy-config (webapp) : 기존에 webapp 에서 catalog 로 VirtualService 정보는 없었는데, 추가됨을 확인
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction | egrep 'NAME|catalog'
NAME                                                          DOMAINS                                             MATCH                  VIRTUAL SERVICE
80                                                            catalog, catalog.istioinaction + 1 more...          /*                     catalog.istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction --name 80 -o json > webapp-routes.json
cat webapp-routes.json | jq
...
    "virtualHosts": [
      {
        "name": "catalog.istioinaction.svc.cluster.local:80",
        "domains": [
          "catalog.istioinaction.svc.cluster.local",
          "catalog",
          "catalog.istioinaction.svc",
          "catalog.istioinaction",
          "10.200.1.254" # 해당 IP는 catalog service(clusterIP)
        ],
        "routes": [
          {
            "match": {
              "prefix": "/"
            },
            "route": {
              "cluster": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local",
              "timeout": "0s",
...


docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction --fqdn catalog.istioinaction.svc.cluster.local
SERVICE FQDN                                PORT     SUBSET         DIRECTION     TYPE     DESTINATION RULE
catalog.istioinaction.svc.cluster.local     80       -              outbound      EDS      catalog.istioinaction
catalog.istioinaction.svc.cluster.local     80       version-v1     outbound      EDS      catalog.istioinaction
catalog.istioinaction.svc.cluster.local     80       version-v2     outbound      EDS      catalog.istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction --subset version-v1 -o json
...
        "name": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local",
        "type": "EDS",
...

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction | egrep 'ENDPOINT|catalog'
ENDPOINT                                                STATUS      OUTLIER CHECK     CLUSTER
10.10.0.16:3000                                         HEALTHY     OK                outbound|80|version-v1|catalog.istioinaction.svc.cluster.local
10.10.0.16:3000                                         HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local
10.10.0.17:3000                                         HEALTHY     OK                outbound|80|version-v2|catalog.istioinaction.svc.cluster.local
10.10.0.17:3000                                         HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local

# proxy-config (catalog) : gateway.mesh 이므로, 메시 내에 모든 사이드카에 VirtualService 적용됨을 확인. 아래 routes 부분
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction | egrep 'NAME|catalog'
NAME                                                          DOMAINS                                             MATCH                  VIRTUAL SERVICE
80                                                            catalog, catalog.istioinaction + 1 more...          /*                     catalog.istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426131138.png)
![]({{ site.url }}/img/post/devops/study/istio/3/istio-w3-kiali.png)
```bash
cat ch5/catalog-vs-v2-request-mesh.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog
spec:
  hosts:
  - catalog
  gateways:
    - mesh
  http:
  - match:
    - headers:
        x-istio-cohort:
          exact: "internal"
    route:
    - destination:
        host: catalog
        subset: version-v2
  - route:
    - destination:
        host: catalog
        subset: version-v1

kubectl apply -f ch5/catalog-vs-v2-request-mesh.yaml -n istioinaction


# 반복 호출테스트 : 신규터미널 2개에 아래 각각 실행 >> v1, v2 각기 라우팅 확인
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog -H "x-istio-cohort: internal" -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 2; echo; done


# proxy-config (webapp) : 기존에 webapp 에서 catalog 로 VirtualService 추가된 2개 항목 확인
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction | egrep 'NAME|catalog'
NAME                                                          DOMAINS                                             MATCH                  VIRTUAL SERVICE
80                                                            catalog, catalog.istioinaction + 1 more...          /*                     catalog.istioinaction
80                                                            catalog, catalog.istioinaction + 1 more...          /*                     catalog.istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction --name 80 -o json > webapp-routes.json
cat webapp-routes.json | jq
...
        "virtualHosts": [
            {
                "name": "catalog.istioinaction.svc.cluster.local:80",
                "domains": [
                    "catalog.istioinaction.svc.cluster.local",
                    "catalog",
                    "catalog.istioinaction.svc",
                    "catalog.istioinaction",
                    "10.200.1.254"
                ],
                "routes": [
                    {
                        "match": {
                            "prefix": "/",
                            "caseSensitive": true,
                            "headers": [
                                {
                                    "name": "x-istio-cohort",
                                    "stringMatch": {
                                        "exact": "internal"
                                    }
                                }
                            ]
                        },
                        "route": {
                            "cluster": "outbound|80|version-v2|catalog.istioinaction.svc.cluster.local",
                     ....
                    {
                        "match": {
                            "prefix": "/"
                        },
                        "route": {
                            "cluster": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local",
...

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction --fqdn catalog.istioinaction.svc.cluster.local
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction | egrep 'ENDPOINT|catalog'

# proxy-config (catalog) : mesh 이므로 VS가 아래 routes(catalog)에도 적용됨
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction
```
![]({{ site.url }}/img/post/devops/study/istio/3/istio-w3-kiali-2.png)

---
## 트래픽 전환
트래픽의 일부만 신버전(v2)으로 보내면서 점진적으로 배포를 확장하는 **카나리 릴리스**를 구현한다.
##### 실습전 트래픽 초기화
```bash
# 반복 호출테스트 : 신규터미널
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

# 모든 트래픽을 catalog service v1 으로 재설정
cat ch5/catalog-vs-v1-mesh.yaml
...
  http:
  - route:
    - destination:
        host: catalog
        subset: version-v1

kubectl apply -f ch5/catalog-vs-v1-mesh.yaml -n istioinaction

# 호출테스트
curl -s http://webapp.istioinaction.io:30000/api/catalog | jq
```
### 트래픽 10%만 v2로 보내기
```bash
cat ch5/catalog-vs-v2-10-90-mesh.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog
spec:
  hosts:
  - catalog
  gateways:
  - mesh
  http:
  - route:
    - destination:
        host: catalog
        subset: version-v1
      weight: 90
    - destination:
        host: catalog
        subset: version-v2
      weight: 10 

kubectl apply -f ch5/catalog-vs-v2-10-90-mesh.yaml -n istioinaction

kubectl get vs -n istioinaction catalog
NAME      GATEWAYS   HOSTS         AGE
catalog   ["mesh"]   ["catalog"]   112s

# 호출 테스트 : v2 호출 비중 확인
for i in {1..10};  do curl -s http://webapp.istioinaction.io:30000/api/catalog | grep -i imageUrl ; done | wc -l
for i in {1..100}; do curl -s http://webapp.istioinaction.io:30000/api/catalog | grep -i imageUrl ; done | wc -l

# proxy-config(webapp) : mesh 이므로 메시 내 모든 사이드카에 VS 적용
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction --name 80 -o json
...
                        "route": {
                            "weightedClusters": {
                                "clusters": [
                                    {
                                        "name": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local",
                                        "weight": 90
                                    },
                                    {
                                        "name": "outbound|80|version-v2|catalog.istioinaction.svc.cluster.local",
                                        "weight": 10
                                    }
                                ],
                                "totalWeight": 100
...

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction --fqdn catalog.istioinaction.svc.cluster.local
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction | grep catalog

# proxy-config(catalog) : mesh 이므로 메시 내 모든 사이드카에 VS 적용
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction --name 80 -o json
...
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426132650.png)
### 트래픽을 50:50으로 분할

```bash
cat ch5/catalog-vs-v2-50-50-mesh.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog
spec:
  hosts:
  - catalog
  gateways:
  - mesh
  http:
  - route:
    - destination:
        host: catalog
        subset: version-v1
      weight: 50
    - destination:
        host: catalog
        subset: version-v2
      weight: 50

kubectl apply -f ch5/catalog-vs-v2-50-50-mesh.yaml -n istioinaction

# 호출 테스트 : v2 호출 비중 확인
for i in {1..10};  do curl -s http://webapp.istioinaction.io:30000/api/catalog | grep -i imageUrl ; done | wc -l
for i in {1..100}; do curl -s http://webapp.istioinaction.io:30000/api/catalog | grep -i imageUrl ; done | wc -l

# proxy-config(webapp) 
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction --name 80 -o json
...
                      "route": {
                            "weightedClusters": {
                                "clusters": [
                                    {
                                        "name": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local",
                                        "weight": 50
                                    },
                                    {
                                        "name": "outbound|80|version-v2|catalog.istioinaction.svc.cluster.local",
                                        "weight": 50
                                    }
                                ],
                                "totalWeight": 100
...
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426132824.png)
> 소프트웨어 새 버전을 천천히 출시할 때는 구 버전과 신 버전을 모두 모니터링하고 관찰해 안정성, 성능, 정확성 등을 확인해야 한다.
> 문제 발견시 가중치를 변경하여 구 버전으로 쉽게 롤백이 가능하다.
> 이 방식은 여러 버전을 동시에 실행할 수 있도록 서비스를 구축해야 한다.
> 서비스가 더 많은 상태를 갖을수록(심지어 외부에 의존하더라도) 이런 작업은 더 어려워진다.
---
## Flagger로 카나리 릴리스 자동화

Flagger는 트래픽 전환을 수동으로 하지 않고, 메트릭 기반으로 자동화하는 도구다. 성공률이나 지연 시간 기준으로 릴리스를 진행하거나 롤백할 수 있다.

### Flagger 설치 및 설정

```bash
# catalog-v2 와 트래픽 라우팅을 명시적으로 제어하는 VirtualService를 제거
kubectl delete virtualservice catalog -n istioinaction
kubectl delete deploy catalog-v2 -n istioinaction
kubectl delete service catalog -n istioinaction
kubectl delete destinationrule catalog -n istioinaction

# 남은 리소스 확인
kubectl get deploy,svc,ep -n istioinaction
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/catalog   1/1     1            1           77m
deployment.apps/webapp    1/1     1            1           78m

NAME             TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
service/webapp   ClusterIP   10.200.1.73   <none>        80/TCP    78m

NAME               ENDPOINTS         AGE
endpoints/webapp   10.10.0.19:8080   78m

kubectl get gw,vs -n istioinaction
NAME                                            AGE
gateway.networking.istio.io/coolstore-gateway   73m

NAME                                                       GATEWAYS                HOSTS                         AGE
virtualservice.networking.istio.io/webapp-virtualservice   ["coolstore-gateway"]   ["webapp.istioinaction.io"]   73m        

```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426140421.png)
- helm을 사용하여 Flagger를 설치

```bash
# CRD 설치 
kubectl apply -f https://raw.githubusercontent.com/fluxcd/flagger/main/artifacts/flagger/crd.yaml

kubectl get crd | grep flagger
alertproviders.flagger.app                 2025-04-26T04:49:32Z
canaries.flagger.app                       2025-04-26T04:49:32Z
metrictemplates.flagger.app                2025-04-26T04:49:32Z

# Helm 설치
helm repo add flagger https://flagger.app
helm install flagger flagger/flagger \
  --namespace=istio-system \
  --set crd.create=false \
  --set meshProvider=istio \
  --set metricServer=http://prometheus:9090

# 디플로이먼트 flagger 에 의해 배포된 파드 확인
kubectl get pod -n istio-system -l app.kubernetes.io/name=flagger
NAME                       READY   STATUS    RESTARTS   AGE
flagger-6d4ffc5576-nvx5g   1/1     Running   0          22s

# 시크릿
kubectl get secret -n istio-system | grep flagger-token
flagger-token-gwqtv                                kubernetes.io/service-account-token   3      58s

# 시크릿 확인 : ca.crt 는 k8s 루프 인증서
kubectl view-secret -n istio-system flagger-token-gwqtv --all
ca.crt='-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----
'
namespace='istio-system'
token='...'

# token 을 jtw.io 에서 Decoded 확인
{
  "iss": "kubernetes/serviceaccount",
  "kubernetes.io/serviceaccount/namespace": "istio-system",
  "kubernetes.io/serviceaccount/secret.name": "flagger-token-gwqtv",
  "kubernetes.io/serviceaccount/service-account.name": "flagger",
  "kubernetes.io/serviceaccount/service-account.uid": "f793713c-4dc6-41d9-aed4-1cd97eeef074",
  "sub": "system:serviceaccount:istio-system:flagger"
}
```

### Flagger Canary 리소스 생성

- 45초마다 트래픽 상태 평가
- 10%씩 트래픽 비율 증가
- 최대 50%까지 증가 후 전체로 전환
- 성공률 99% 이상, P99 지연 시간 500ms 이하 기준 유지
- 기준 미달 5회 발생 시 자동 롤백

```bash
cat ch5/flagger/catalog-release.yaml        
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: catalog-release
  namespace: istioinaction
spec:   
  targetRef: #1 카나리 대상 디플로이먼트 https://docs.flagger.app/usage/how-it-works#canary-target
    apiVersion: apps/v1
    kind: Deployment
    name: catalog  
  progressDeadlineSeconds: 60
  # Service / VirtualService Config
  service: #2 서비스용 설정 https://docs.flagger.app/usage/how-it-works#canary-service
    name: catalog
    port: 80
    targetPort: 3000
    gateways:
    - mesh    
    hosts:
    - catalog
  analysis: #3 카니리 진행 파라미터 https://docs.flagger.app/usage/how-it-works#canary-analysis
    interval: 45s
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    match: 
    - sourceLabels:
        app: webapp
    metrics: # https://docs.flagger.app/usage/metrics , https://docs.flagger.app/faq#metrics
    - name: request-success-rate # built-in metric 요청 성공률
      thresholdRange:
        min: 99
      interval: 1m
    - name: request-duration # built-in metric 요청 시간
      thresholdRange:
        max: 500
      interval: 30s
```

```bash
# 반복 호출테스트 : 신규터미널
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done


# flagger (operator) 가 catalog를 위한 canary 배포환경을 구성
kubectl apply -f ch5/flagger/catalog-release.yaml -n istioinaction

# flagger 로그 확인 : Service, Deployment, VirtualService 등을 설치하는 것을 확인할 수 있습니다.
kubectl logs -f deploy/flagger -n istio-system
...

# 확인
kubectl get canary -n istioinaction -w
NAME              STATUS        WEIGHT   LASTTRANSITIONTIME
catalog-release   Initializing  0        2025-04-19T05:10:00Z
catalog-release   Initialized   0        2025-04-19T05:15:54Z

kubectl get canary -n istioinaction -owide
NAME              STATUS        WEIGHT   SUSPENDED   FAILEDCHECKS   INTERVAL   MIRROR   STEPWEIGHT   STEPWEIGHTS   MAXWEIGHT   LASTTRANSITIONTIME
catalog-release   Initialized   0                    0              45s                 10                         50          2025-04-19T05:15:54Z

# flagger Initialized 동작 확인
## catalog-primary deployment/service 가 생성되어 있음, 기존 catalog deploy/service 는 파드가 0으로 됨
kubectl get deploy,svc,ep -n istioinaction -o wide
```
![]({{ site.url }}/img/post/devops/study/istio/3/1.55.35.png)
```bash
## VS catalog 생성되었음
kubectl get gw,vs -n istioinaction
NAME                                            AGE
gateway.networking.istio.io/coolstore-gateway   137m

NAME                                                       GATEWAYS                HOSTS                         AGE
virtualservice.networking.istio.io/catalog                 ["mesh"]                ["catalog"]                   8m17s
virtualservice.networking.istio.io/webapp-virtualservice   ["coolstore-gateway"]   ["webapp.istioinaction.io"]   137m

## VS catalog 확인
kubectl get vs -n istioinaction catalog -o yaml | kubectl neat
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  annotations:
    helm.toolkit.fluxcd.io/driftDetection: disabled
    kustomize.toolkit.fluxcd.io/reconcile: disabled
  name: catalog
  namespace: istioinaction
spec:
  gateways:
  - mesh
  hosts:
  - catalog
  http:
  - match:
    - sourceLabels:
        app: webapp
    route:
    - destination:
        host: catalog-primary
      weight: 100
    - destination:
        host: catalog-canary
      weight: 0
  - route:
    - destination:
        host: catalog-primary
      weight: 100

# destinationrule 확인
kubectl get destinationrule -n istioinaction
NAME              HOST              AGE
catalog-canary    catalog-canary    2m51s
catalog-primary   catalog-primary   2m51s

kubectl get destinationrule -n istioinaction catalog-primary -o yaml | kubectl neat
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: catalog-primary
  namespace: istioinaction
spec:
  host: catalog-primary

kubectl get destinationrule -n istioinaction catalog-canary -o yaml | kubectl neat
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: catalog-canary
  namespace: istioinaction
spec:
  host: catalog-canary

docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction --name 80 -o json
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction --name 80 
NAME     DOMAINS                                                        MATCH     VIRTUAL SERVICE
80       catalog-canary, catalog-canary.istioinaction + 1 more...       /*        
80       catalog-primary, catalog-primary.istioinaction + 1 more...     /*        
80       catalog, catalog.istioinaction + 1 more...                     /*        catalog.istioinaction
...

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction | egrep 'RULE|catalog'
SERVICE FQDN                                            PORT      SUBSET     DIRECTION     TYPE             DESTINATION RULE
catalog-canary.istioinaction.svc.cluster.local          80        -          outbound      EDS              catalog-canary.istioinaction
catalog-primary.istioinaction.svc.cluster.local         80        -          outbound      EDS              catalog-primary.istioinaction
catalog.istioinaction.svc.cluster.local                 80        -          outbound      EDS 

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction --fqdn catalog.istioinaction.svc.cluster.local -o json
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction --fqdn catalog-primary.istioinaction.svc.cluster.local -o json
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction --fqdn catalog-canary.istioinaction.svc.cluster.local -o json

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction | grep catalog
10.10.0.30:3000                                         HEALTHY     OK                outbound|80||catalog-primary.istioinaction.svc.cluster.local
10.10.0.30:3000                                         HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local

# 해당 EDS에 메트릭 통계 값 0.
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction --cluster 'outbound|80||catalog.istioinaction.svc.cluster.local' -o json
...

# 현재 EDS primary 에 메트릭 통계 값 출력 중. 해당 EDS 호출.
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction --cluster 'outbound|80||catalog-primary.istioinaction.svc.cluster.local' -o json
...
```
![]({{ site.url }}/img/post/devops/study/istio/3/2.06.01.png)
![]({{ site.url }}/img/post/devops/study/istio/3/2.08.36.png)

아직은 기본 설정만 하였고, 아직 실제 카나리는 수행하지 않았다.
flagger는 원본 디플로이먼트 대상의 변경사항을 지켜보고, 카나리 디플로이먼트 및 서비스를 생성하고, VS의 가중치를 조정한다.
![]({{ site.url }}/img/post/devops/study/istio/3/20250426141430.png)

```bash
# 반복 호출테스트 : 신규터미널1 - 부하 만들기
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

# flagger 로그 확인 : 신규터미널2
kubectl logs -f deploy/flagger -n istio-system

# flagger 상태 확인 : 신규터미널3
## 카나리는 Carary 오브젝트에 설정한 대로 45초마다 진행될 것이다.
## 트래픽의 50%가 카나리로 이동할 때까지는 단계별로 10%씩 증가한다.
## flagger가 메트릭에 문제가 없고 기준과 차이가 없다고 판단되면, 모든 트래픽이 카나리로 이동해 카나리가 기본 서비스로 승격 될 때까지 카나리가 진행된다.
## 만약 문제가 발생하면 flagger는 자동으로 카나리 릴리스를 롤백할 것이다.
kubectl get canary -n istioinaction -w
NAME              STATUS        WEIGHT   LASTTRANSITIONTIME
catalog-release   Initialized   0        2025-04-19T05:15:54Z
catalog-release   Progressing   0        2025-04-19T06:09:09Z
catalog-release   Progressing   10       2025-04-19T06:09:54Z # 45초 간격
catalog-release   Progressing   20       2025-04-19T06:10:39Z
catalog-release   Progressing   30       2025-04-19T06:11:24Z
catalog-release   Progressing   40       2025-04-19T06:12:09Z
catalog-release   Progressing   50       2025-04-19T06:12:54Z
catalog-release   Promoting     0        2025-04-19T06:13:39Z
catalog-release   Finalising    0        2025-04-19T06:14:24Z
catalog-release   Succeeded     0        2025-04-19T06:15:09Z


# imageUrl 출력 (v2)을 포함하는 catalog deployment v2 배포
cat ch5/flagger/catalog-deployment-v2.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: catalog
    version: v1
  name: catalog
spec:
  replicas: 1
  selector:
    matchLabels:
      app: catalog
      version: v1
  template:
    metadata:
      labels:
        app: catalog
        version: v1
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

kubectl apply -f ch5/flagger/catalog-deployment-v2.yaml -n istioinaction
kubectl get vs -n istioinaction catalog -o yaml -w # catalog vs 에 가중치 변경 모니터링
```

![]({{ site.url }}/img/post/devops/study/istio/3/2.20.43.png)
```
# canary CRD 이벤트 확인
kubectl describe canary -n istioinaction catalog-release | grep Events: -A20
Events:
  Type     Reason  Age                From     Message
  ----     ------  ----               ----     -------
  Warning  Synced  32m                flagger  catalog-primary.istioinaction not ready: waiting for rollout to finish: observed deployment generation less than desired generation
  Normal   Synced  32m (x2 over 32m)  flagger  all the metrics providers are available!
  Normal   Synced  32m                flagger  Initialization done! catalog-release.istioinaction
  Normal   Synced  8m57s              flagger  New revision detected! Scaling up catalog.istioinaction
  Normal   Synced  8m12s              flagger  Starting canary analysis for catalog.istioinaction
  Normal   Synced  8m12s              flagger  Advance catalog-release.istioinaction canary weight 10
  Normal   Synced  7m27s              flagger  Advance catalog-release.istioinaction canary weight 20
  Normal   Synced  6m42s              flagger  Advance catalog-release.istioinaction canary weight 30
  Normal   Synced  5m57s              flagger  Advance catalog-release.istioinaction canary weight 40
  Normal   Synced  5m12s              flagger  Advance catalog-release.istioinaction canary weight 50
  Normal   Synced  4m27s              flagger  Copying catalog.istioinaction template spec to catalog-primary.istioinaction
  Normal   Synced  3m42s              flagger  Routing all traffic to primary
  Normal   Synced  2m57s              flagger  (combined from similar events): Promotion completed! Scaling down catalog.istioinaction

# 최종 v2 접속 확인
for i in {1..100}; do curl -s http://webapp.istioinaction.io:30000/api/catalog | grep -i imageUrl ; done | wc -l
     100
```
- Kiali
![]({{ site.url }}/img/post/devops/study/istio/3/20250426142928.png)
- Prometheus - `flagger_canary_weight`
![]({{ site.url }}/img/post/devops/study/istio/3/20250426143047.png)
- `flagger_canary_metirc_analysis(metric="request-duration")`
![]({{ site.url }}/img/post/devops/study/istio/3/20250426143110.png)
- `flagger_canary_metric_analysis(metric="request-seccess-rate")`
![]({{ site.url }}/img/post/devops/study/istio/3/20250426143134.png)
> (실습 중에 캡쳐를 못했습니다. ref: Istio Hands-on Study - 3주차 - Traffic control)

여기서는 Canary만 실습했지만, A/B Testing, Blue/Green 등도 지원한다.

```bash
# Canary 삭제 : Flagger가 만든 service (catalog, catalog-canary, catalog-primary), destinationrule (catalog-canary, catalog-primary), deployment (catalog-primary) 를 제거함
kubectl delete canary catalog-release -n istioinaction

# catalog 삭제
kubectl delete deploy catalog -n istioinaction

# Flagger 삭제
helm uninstall flagger -n istio-system
```
---
## 위험을 더욱 줄이기: 트래픽 미러링
운영 트래픽을 복제해 새 버전에 보내면서 사용자에게는 영향을 주지 않는다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250420005358.png)
##### 실습 환경 초기화
```bash
# catalog 디플로이먼트를 초기 상태로 돌리고, catalog-v2 를 별도의 디플로이먼트로 배포
kubectl apply -f services/catalog/kubernetes/catalog-svc.yaml -n istioinaction
kubectl apply -f services/catalog/kubernetes/catalog-deployment.yaml -n istioinaction
kubectl apply -f services/catalog/kubernetes/catalog-deployment-v2.yaml -n istioinaction
kubectl apply -f ch5/catalog-dest-rule.yaml -n istioinaction
kubectl apply -f ch5/catalog-vs-v1-mesh.yaml -n istioinaction

# 확인
kubectl get deploy -n istioinaction -o wide
kubectl get svc,ep -n istioinaction -owide
kubectl get gw,vs -n istioinaction

# 반복 접속
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

# catalog v1 으로만 접속 확인
for i in {1..100}; do curl -s http://webapp.istioinaction.io:30000/api/catalog | grep -i imageUrl ; done | wc -l
0
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426144209.png)
### 트래픽 미러링 설정

```bash
# cat ch5/catalog-vs-v2-mirror.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog
spec:
  hosts:
  - catalog
  gateways:
    - mesh
  http:
  - route:
    - destination:
        host: catalog
        subset: version-v1
      weight: 100
    mirror:
      host: catalog
      subset: version-v2

# 반복 접속
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog -I | head -n 1 ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; don

# catalog istio-proxy 로그 활성화
cat << EOF | kubectl apply -f -
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: catalog
  namespace: istioinaction
spec:
  accessLogging:
  - disabled: false
    providers:
    - name: envoy
  selector:
    matchLabels:
      app: catalog
EOF

kubectl get telemetries -n istioinaction
NAME      AGE
catalog   7s
webapp    109m

# istio-proxy 로그 확인 : 신규 터미널
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
kubectl logs -n istioinaction -l app=catalog -c istio-proxy -f
kubectl logs -n istioinaction -l version=v1 -c istio-proxy -f
kubectl logs -n istioinaction -l app=catalog -l version=v2 -c istio-proxy -f
혹은
kubectl stern -n istioinaction -l app=catalog -c istio-proxy

# proxy-config : webapp
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction | grep catalog 
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction | grep catalog
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction | grep catalog

# proxy-config : catalog
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction | grep catalog 
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction | grep catalog 
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction | grep catalog 
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426145002.png)

```bash
# 미러링 VS 설정
kubectl apply -f ch5/catalog-vs-v2-mirror.yaml -n istioinaction

# v1 으로만 호출 확인
for i in {1..100}; do curl -s http://webapp.istioinaction.io:30000/api/catalog | grep -i imageUrl ; done | wc -l
       0

# v1 app 로그 확인
kubectl logs -n istioinaction -l app=catalog -l version=v1 -c catalog -f
request path: /items
blowups: {}
number of blowups: 0
GET catalog.istioinaction:80 /items 200 502 - 0.651 ms
GET /items 200 0.651 ms - 502
...

# v2 app 로그 확인 : 미러링된 트래픽이 catalog v2로 향할때, Host 헤더가 수정돼 미러링/섀도잉된 트래픽임을 나타낸다.
## 따라서 Host:catalog:8080 대신 Host:catalog-shadow:8080이 된다.
## -shadow 접미사가 붙은 요청을 받는 서비스는 그 요청이 미러링된 요청임을 식별할 수 있어, 요청을 처리할 때 고려할 수 있다
## 예를 들어, 응답이 버려질 테니 트랜잭션을 롤백하지 않거나 리소스를 많이 사용하는 호출을 하지 않는 것 등.
kubectl logs -n istioinaction -l app=catalog -l version=v2 -c catalog -f
request path: /items
blowups: {}
number of blowups: 0
GET catalog.istioinaction-shadow:80 /items 200 698 - 0.619 ms
GET /items 200 0.619 ms - 698
```

![]({{ site.url }}/img/post/devops/study/istio/3/2.51.39.png)

```
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction --name 80 -o json > webapp-routes.json
cat webapp-routes.json
...
                        "route": {
                            "cluster": "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local",
                            "timeout": "0s",
                            "retryPolicy": {
                                "retryOn": "connect-failure,refused-stream,unavailable,cancelled,retriable-status-codes",
                                "numRetries": 2,
                                "retryHostPredicate": [
                                    {
                                        "name": "envoy.retry_host_predicates.previous_hosts",
                                        "typedConfig": {
                                            "@type": "type.googleapis.com/envoy.extensions.retry.host.previous_hosts.v3.PreviousHostsPredicate"
                                        }
                                    }
                                ],
                                "hostSelectionRetryMaxAttempts": "5",
                                "retriableStatusCodes": [
                                    503
                                ]
                            },
                            "requestMirrorPolicies": [
                                {
                                    "cluster": "outbound|80|version-v2|catalog.istioinaction.svc.cluster.local",
                                    "runtimeFraction": {
                                        "defaultValue": {
                                            "numerator": 100
                                        }
                                    },
                                    "traceSampled": false
...

# 위 webapp과 상동 : mesh(gateway)이니까...
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction --name 80 -o json > catalog-routes.json
cat catalog-routes.json
...
```
![]({{ site.url }}/img/post/devops/study/istio/3/2.55.36.png)

```bash
# Istio 메시 내부망에서 모든 mTLS 통신 기능 끄기 설정 : (참고) 특정 네임스페이스 등 세부 조절 설정 가능 
cat <<EOF | kubectl apply -f -
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: DISABLE
EOF

kubectl get PeerAuthentication -n istio-system
NAME      MODE      AGE
default   DISABLE   6h13m


--------------------------------------------------------------------------------
# catalog v2 파드의 vnic 와 vritual-pair 인 control-plane 노드(?)의 veth 이름 찾기
## catalog v2 파드 IP 확인
C2IP=$(kubectl get pod -n istioinaction -l app=catalog -l version=v2 -o jsonpath='{.items[*].status.podIP}')
echo $C2IP
10.10.0.34

## veth 이름 확인
docker exec -it myk8s-control-plane ip -c route | grep $C2IP | awk '{ print $3 }'
C2VETH=$(docker exec -it myk8s-control-plane ip -c route | grep $C2IP | awk '{ print $3 }')
echo $C2VETH
vethb8c60b86
--------------------------------------------------------------------------------

# ngrep 확인 : catalog v2 파드 tcp 3000
docker exec -it myk8s-control-plane sh -c "ngrep -tW byline -d vethb8c60b86 '' 'tcp port 3000'"
```

![]({{ site.url }}/img/post/devops/study/istio/3/3.27.09.png)

- 미러링 대상 서버는 응답은 안하는게 좋지만, 응답을 webapp 파드에 한다고 해도, webapp은 이 응답을 무시한다.

```bash
--------------------------------------------------------------------------------
# webapp 파드의 vnic 와 vritual-pair 인 control-plane 노드(?)의 veth 이름 찾기
## webapp 파드 IP 확인
WEBIP=$(kubectl get pod -n istioinaction -l app=webapp -o jsonpath='{.items[*].status.podIP}')
echo $WEBIP
10.10.0.28

## veth 이름 확인
docker exec -it myk8s-control-plane ip -c route | grep $WEBIP | awk '{ print $3 }'
WEBVETH=$(docker exec -it myk8s-control-plane ip -c route | grep $WEBIP | awk '{ print $3 }')
echo $WEBVETH
veth38e54d37
--------------------------------------------------------------------------------

# ngrep 확인 : webapp 파드 tcp 8080 
## => 아래 tcp 3000에서 미러링 응답이 있지만 8080에 없다는건, webapp istio-proxy 가 최초 외부 요청자에게는 전달하지 않고 무시(drop?).
docker exec -it myk8s-control-plane sh -c "ngrep -tW byline -d veth38e54d37 '' 'tcp port 8080'"
```

![]({{ site.url }}/img/post/devops/study/istio/3/3.19.47.png)

```
# ngrep 확인 : webapp 파드 tcp 3000
docker exec -it myk8s-control-plane sh -c "ngrep -tW byline -d veth38e54d37 '' 'tcp port 3000'"
```

![]({{ site.url }}/img/post/devops/study/istio/3/3.10.41.png)

![]({{ site.url }}/img/post/devops/study/istio/3/3.10.57.png)

---
## 클러스터 외부 서비스와 통신하기

Istio는 기본적으로 모든 아웃바운드 트래픽을 허용하지만, outboundTrafficPolicy를 `REGISTRY_ONLY`로 설정해 차단할 수 있다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250420005446.png)

ServiceEntry를 사용해 필요한 외부 도메인만 허용한다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250420005329.png)
#### 실습 준비
```bash
# 현재 istiooperators meshConfig 설정 확인
kubectl get istiooperators -n istio-system -o json
...
                "meshConfig": {
                    "defaultConfig": {
                        "proxyMetadata": {}
                    },
                    "enablePrometheusMerge": true
                },
...

# webapp 파드에서 외부 다운로드
kubectl exec -it deploy/webapp -n istioinaction -c webapp -- wget https://raw.githubusercontent.com/gasida/KANS/refs/heads/main/msa/sock-shop-demo.yaml

# webapp 로그 : 신규 터미널
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
[2025-04-26T06:32:06.582Z] "HEAD /api/catalog HTTP/1.1" 200 - via_upstream - "-" 0 0 4 4 "192.168.65.1" "curl/8.7.1" "31ec608e-0205-412f-aae8-b32f257672e4" "webapp.istioinaction.io:30000" "10.10.0.28:8080" inbound|8080|| 127.0.0.6:35431 10.10.0.28:8080 192.168.65.1:0 - default

# 다음 명령을 실행해 이스티오의 기본값을 ALLOW_ANY 에서 REGISTRY_ONLY 로 바꾸자.
# 이느 서비스 메시 저장소에 명시적으로 허용된 경우(화이트 리스트)에만 트래픽이 메시를 떠나도록 허용하겠다는 의미다.
# 아래 설정 방법 이외에도 IstioOperator 로 설정을 변경하거나, istio-system 의 istio configmap 을 변경해도 됨.
# outboundTrafficPolicy 3가지 모드 : ALLOW_ANY (default) , REGISTRY_ONLY , ALLOW_LIST
docker exec -it myk8s-control-plane bash
----------------------------------------
istioctl install --set profile=default --set meshConfig.outboundTrafficPolicy.mode=REGISTRY_ONLY
y 

exit
----------------------------------------

# 배포 확인
docker exec -it myk8s-control-plane istioctl proxy-status
NAME                                                   CLUSTER        CDS        LDS        EDS        RDS          ECDS         ISTIOD                    VERSION
catalog-6d5b9bbb66-vzg4j.istioinaction                 Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED       NOT SENT     istiod-8d74787f-6w77x     1.17.8
catalog-v2-6df885b555-n9nxw.istioinaction              Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED       NOT SENT     istiod-8d74787f-6w77x     1.17.8
istio-ingressgateway-6bb8fb6549-s4pt8.istio-system     Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED       NOT SENT     istiod-8d74787f-6w77x     1.17.8
webapp-7685bcb84-skzgg.istioinaction                   Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED       NOT SENT     istiod-8d74787f-6w77x     1.17.8


# webapp 파드에서 외부 다운로드
kubectl exec -it deploy/webapp -n istioinaction -c webapp -- wget https://raw.githubusercontent.com/gasida/KANS/refs/heads/main/msa/sock-shop-demo.yaml
Connecting to raw.githubusercontent.com (185.199.109.133:443)
wget: error getting response: Connection reset by peer
command terminated with exit code 1

# webapp 로그 : BlackHoleCluster 차단
# UH : NoHealthyUpstream - No healthy upstream hosts in upstream cluster in addition to 503 response code.
# https://www.envoyproxy.io/docs/envoy/latest/configuration/observability/access_log/usage
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
[2025-04-19T09:55:34.851Z] "- - -" 0 UH - - "-" 0 0 0 - "-" "-" "-" "-" "-" BlackHoleCluster - 185.199.109.133:443 10.10.0.19:34868 - -

# proxy-config : webapp
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction --fqdn BlackHoleCluster -o json
[
    {
        "name": "BlackHoleCluster",
        "type": "STATIC",
        "connectTimeout": "10s"
    }
]

# 현재 istiooperators meshConfig 설정 확인
kubectl get istiooperators -n istio-system -o json
...
                "meshConfig": {
                    "defaultConfig": {
                        "proxyMetadata": {}
                    },
                    "enablePrometheusMerge": true,
                    "outboundTrafficPolicy": {
                        "mode": "REGISTRY_ONLY"
                    }
                },
```
### ServiceEntry 생성 예시

```bash
# forum 설치
cat services/forum/kubernetes/forum-all.yaml
kubectl apply -f services/forum/kubernetes/forum-all.yaml -n istioinaction

# 확인
kubectl get deploy,svc -n istioinaction -l app=webapp
docker exec -it myk8s-control-plane istioctl proxy-status

# webapp 웹 접속
open http://webapp.istioinaction.io:30000/
```

- 메시 안에서 새로운 포럼 서비스를 호출

```bash
# 메시 안에서 새로운 포럼 서비스를 호출
curl -s http://webapp.istioinaction.io:30000/api/users
error calling Forum service

# forum 로그 확인
kubectl logs -n istioinaction -l app=forum -c istio-proxy -f
[2025-04-19T10:35:23.526Z] "GET /users HTTP/1.1" 502 - direct_response - "-" 0 0 0 - "172.18.0.1" "Go-http-client/1.1" "04bef923-b182-94e9-a58d-e2d9f957693b" "jsonplaceholder.typicode.com" "-" - - 104.21.48.1:80 172.18.0.1:0 - block_all
# 클러스터 내부 서비스에서 외부 도메인(jsonplaceholder.typicode.com) 으로 나가려 했지만, Istio가 요청을 막아서 502 오류와 함께 직접 응답 처리한 상황
## direct_response : Envoy가 요청을 외부로 보내지 않고 자체적으로 차단 응답을 반환했음을 의미
## block_all : Istio에서 egress(외부) 요청이 전면 차단됨을 나타내는 메시지
[2025-04-19T10:35:23.526Z] "GET /api/users HTTP/1.1" 500 - via_upstream - "-" 0 28 0 0 "172.18.0.1" "beegoServer" "04bef923-b182-94e9-a58d-e2d9f957693b" "forum.istioinaction:80" "10.10.0.31:8080" inbound|8080|| 127.0.0.6:60487 10.10.0.31:8080 172.18.0.1:0 - default
```

```bash
# istio proxy (forum)
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/forum.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/forum.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/forum.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config all deploy/forum.istioinaction -o short > forum-1.json

#
cat ch5/forum-serviceentry.yaml
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: jsonplaceholder
spec:
  hosts:
  - jsonplaceholder.typicode.com
  ports:
  - number: 80
    name: http
    protocol: HTTP
  resolution: DNS
  location: MESH_EXTERNAL
  
kubectl apply -f ch5/forum-serviceentry.yaml -n istioinaction

#
docker exec -it myk8s-control-plane istioctl proxy-config all deploy/forum.istioinaction -o short > forum-2.json
diff forum-1.json forum-2.json
25a26
> jsonplaceholder.typicode.com                            80        -              outbound      STRICT_DNS       
96a98
> 80                                                            jsonplaceholder.typicode.com                       /*  

#
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/forum.istioinaction | grep json
80                                                            jsonplaceholder.typicode.com                       /* 

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/forum.istioinaction --fqdn jsonplaceholder.typicode.com -o json
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/forum.istioinaction | grep json
jsonplaceholder.typicode.com                            80        -              outbound      STRICT_DNS  

# 목적 hosts 의 도메인 질의 응답 IP로 확인된 엔드포인트들 확인
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/forum.istioinaction --cluster 'outbound|80||jsonplaceholder.typicode.com'
ENDPOINT            STATUS      OUTLIER CHECK     CLUSTER
104.21.112.1:80     HEALTHY     OK                outbound|80||jsonplaceholder.typicode.com
104.21.16.1:80      HEALTHY     OK                outbound|80||jsonplaceholder.typicode.com
104.21.32.1:80      HEALTHY     OK                outbound|80||jsonplaceholder.typicode.com
104.21.48.1:80      HEALTHY     OK                outbound|80||jsonplaceholder.typicode.com
104.21.64.1:80      HEALTHY     OK                outbound|80||jsonplaceholder.typicode.com
104.21.80.1:80      HEALTHY     OK                outbound|80||jsonplaceholder.typicode.com
104.21.96.1:80      HEALTHY     OK                outbound|80||jsonplaceholder.typicode.com

# 메시 안에서 새로운 포럼 서비스를 호출 : 사용자 목록 반환 OK
curl -s http://webapp.istioinaction.io:30000/api/users

# 반복 접속
while true; do curl -s http://webapp.istioinaction.io:30000/ ; date "+%Y-%m-%d %H:%M:%S" ; sleep 2; echo; done

# webapp 웹 접속
open http://webapp.istioinaction.io:30000/
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426174222.png)
![]({{ site.url }}/img/post/devops/study/istio/3/5.44.39.png)
![]({{ site.url }}/img/post/devops/study/istio/3/5.43.42.png)

## (추가실습) - 미진행
외부에  web 서버(https://httpbin.org or docker container nginx 1대 가동 후)에 istio에 ServiceEntry 등록 후 통신 허용 설정
```bash
# example
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: httpbin-svc
spec:
  hosts:
  - httpbin.org
  location: MESH_EXTERNAL
  ports:
  - number: 80
  name: httpbin
    protocol: http
  resolution: DNS
```
---
### 도전과제
- `[도전과제1]` Flagger 공식문서에 주요 기능 실습 및 정리 - [Docs](https://docs.flagger.app/)
    - Flagger 배포 전략 실습 : A/B Testing, Blue/Green Deployments , Canary with Session Affinity - [Docs](https://docs.flagger.app/usage/deployment-strategies)
        - Blue/Green Deployments - [Docs](https://docs.flagger.app/tutorials/kubernetes-blue-green)
        - Istio Canary Deployments - [Docs](https://docs.flagger.app/tutorials/istio-progressive-delivery)
        - Istio A/B Testing - [Docs](https://docs.flagger.app/tutorials/istio-ab-testing)
    - 무중단 배포 Zero downtime deploymentes - [Docs](https://docs.flagger.app/tutorials/zero-downtime-deployments)
- `[도전과제2]` Istio 공식문서에 Egress 내용을 실습 및 정리 - [Docs](https://istio.io/v1.17/docs/tasks/traffic-management/egress/)
    - Accessing External Services - [Docs](https://istio.io/v1.17/docs/tasks/traffic-management/egress/egress-control/)
    - Egress Gateways - [Docs](https://istio.io/v1.17/docs/tasks/traffic-management/egress/egress-gateway/)
    - Kubernetes Services for Egress Traffic - [Docs](https://istio.io/v1.17/docs/tasks/traffic-management/egress/egress-kubernetes-services/)
    - Configuring Gateway Network Topology - [Docs](https://istio.io/v1.17/docs/ops/configuration/traffic-management/network-topologies/)
- `[도전과제3]` Istio ServiceEntry 에 경계 설정 해보기 (키알리에서 확인), 그외 활용 방안들 실습 해보고 정리 - [Docs](https://istio.io/v1.17/docs/reference/config/networking/service-entry/)
- `[도전과제4]` Istio Sidecar 내용 정리와 예시실습 해보고 정리 - [Docs](https://istio.io/v1.17/docs/reference/config/networking/sidecar/) , Istio Sidecar Object를 활용한 Sidecar Proxy Endpoint 제어 - [Blog](https://ssup2.github.io/blog-software/docs/theory-analysis/istio-endpoint-control-sidecar-object/)

---

# 6. 복원력: 애플리케이션 네트워킹 문제 해결하기

Istio를 이용해 애플리케이션의 네트워킹 장애를 자동으로 극복하는 방법을 다룬다.
애플리케이션 코드를 변경하지 않고도 재시도, 타임아웃, 서킷 브레이킹, 로드밸런싱 등을 적용해 복원력을 강화할 수 있다.
## **애플리케이션에 복원력 구축하기**

분산 시스템은 언제든 예측할 수 없이 실패한다.
문제가 발생할 때, 트래픽을 수작업으로 전환하기 어렵기 때문에
애플리케이션 자체가 장애를 인지하고 대처할 수 있어야 한다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250420144913.png)
서비스A가 서비스B를 호출했을 때:
- 특정 엔드포인트가 느리면 다른 엔드포인트나 리전으로 라우팅
- 오류 발생 시 재시도
- 심각한 장애 발생 시 요청 자체를 끊어버림 (서킷 브레이킹)
  
**목표:**
애플리케이션이 장애를 예상하고, 자동으로 복구하거나 실패를 관리할 수 있게 만드는 것.

---
## **이스티오로 복원력 패턴 구현하기**

기존에는 복원력을 각 애플리케이션에 직접 코딩해야 했다.
- Twitter: Finagle
- Netflix: Hystrix, Ribbon

문제는 각 언어/플랫폼마다 다르게 구현해야 하고, 코드가 오염되는 점이었다.
**Istio는** 네트워크 레벨에서 복원력 기능을 제공한다.
(서비스 프록시가 HTTP 요청 단위까지 이해하고 통제 가능)


![]({{ site.url }}/img/post/devops/study/istio/3/20250420152536.png)

Istio를 통해 구현할 수 있는 복원력 기능:
- 클라이언트 측 로드 밸런싱
- 지역 인식 로드 밸런싱
- 타임아웃 및 재시도
- 서킷 브레이킹

---
## **클라이언트 측 로드 밸런싱**

기존 중앙집중식 로드 밸런싱 대신,
클라이언트(프록시)가 직접 여러 엔드포인트 중 하나를 선택해 요청을 보낸다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250420154308.png)

- ROUND_ROBIN (기본값)
- RANDOM
- LEAST_CONN (활성 요청 수가 가장 적은 엔드포인트 선택)
### **실습: 클라이언트 측 로드 밸런싱 설정**

```bash
# (옵션) kiali 에서 simple-backend-1,2 버전 확인을 위해서 labels 설정 : ch6/simple-backend.yaml
cat ch6/simple-backend.yaml
...
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: simple-backend
    version: v1
  name: simple-backend-1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: simple-backend
  template:
    metadata:
      labels:
        app: simple-backend
        version: v1
...
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: simple-backend
    version: v2
  name: simple-backend-2
spec:
  replicas: 2
  selector:
    matchLabels:
      app: simple-backend
  template:
    metadata:
      labels:
        app: simple-backend
        version: v2
...

# 예제 서비스 2개 배포
kubectl apply -f ch6/simple-backend.yaml -n istioinaction
kubectl apply -f ch6/simple-web.yaml -n istioinaction

# 확인
kubectl get deploy,pod,svc,ep -n istioinaction -o wide
NAME                               READY   UP-TO-DATE   AVAILABLE   AGE    CONTAINERS       IMAGES                                 SELECTOR
deployment.apps/simple-backend-1   1/1     1            1           105m   simple-backend   nicholasjackson/fake-service:v0.17.0   app=simple-backend
deployment.apps/simple-backend-2   2/2     2            2           105m   simple-backend   nicholasjackson/fake-service:v0.17.0   app=simple-backend
deployment.apps/simple-web         1/1     1            1           105m   simple-web       nicholasjackson/fake-service:v0.17.0   app=simple-web
...

# gw,vs 배포
cat ch6/simple-web-gateway.yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: simple-web-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "simple-web.istioinaction.io"
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: simple-web-vs-for-gateway
spec:
  hosts:
  - "simple-web.istioinaction.io"
  gateways:
  - simple-web-gateway
  http:
  - route:
    - destination:
        host: simple-web
        
kubectl apply -f ch6/simple-web-gateway.yaml -n istioinaction

# 확인
kubectl get gw,vs -n istioinaction

docker exec -it myk8s-control-plane istioctl proxy-status
NAME                                                  CLUSTER        CDS        LDS        EDS        RDS        ECDS         ISTIOD                      VERSION
istio-ingressgateway-996bc6bb6-pvghz.istio-system     Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-2shm6     1.17.8
simple-backend-1-7449cc5945-7jrdj.istioinaction       Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-2shm6     1.17.8
simple-backend-2-6876494bbf-djhkn.istioinaction       Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-2shm6     1.17.8
simple-backend-2-6876494bbf-pvhdf.istioinaction       Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-2shm6     1.17.8
simple-web-7cd856754-nr66f.istioinaction              Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-2shm6     1.17.8

# 도메인 질의를 위한 임시 설정 : 실습 완료 후에는 삭제 해둘 것
echo "127.0.0.1       simple-web.istioinaction.io" | sudo tee -a /etc/hosts
cat /etc/hosts | tail -n 3

# 호출
curl -s http://simple-web.istioinaction.io:30000
open http://simple-web.istioinaction.io:30000

# 신규 터미널 : 반복 접속 실행 해두기
while true; do curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body" ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

# 로그 확인
kubectl stern -l app=simple-web -n istioinaction
kubectl stern -l app=simple-web -n istioinaction -c istio-proxy
kubectl stern -l app=simple-web -n istioinaction -c simple-web
kubectl stern -l app=simple-backend -n istioinaction
kubectl stern -l app=simple-backend -n istioinaction -c istio-proxy
kubectl stern -l app=simple-backend -n istioinaction -c simple-backend

# (옵션) proxy-config
# proxy-config : simple-web
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/simple-web.istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/simple-web.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/simple-web.istioinaction | grep backend
80                                                            simple-backend, simple-backend.istioinaction + 1 more...     /* 

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-web.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local
SERVICE FQDN                                       PORT     SUBSET     DIRECTION     TYPE     DESTINATION RULE
simple-backend.istioinaction.svc.cluster.local     80       -          outbound      EDS

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-web.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json
...
       "name": "outbound|80||simple-backend.istioinaction.svc.cluster.local",
        "type": "EDS",
        "edsClusterConfig": {
            "edsConfig": {
                "ads": {},
                "initialFetchTimeout": "0s",
                "resourceApiVersion": "V3"
            },
            "serviceName": "outbound|80||simple-backend.istioinaction.svc.cluster.local"
        },
        "connectTimeout": "10s",
        "lbPolicy": "LEAST_REQUEST",
...

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local'
ENDPOINT            STATUS      OUTLIER CHECK     CLUSTER
10.10.0.14:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
10.10.0.15:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
10.10.0.16:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' -o json
...
```

![]({{ site.url }}/img/post/devops/study/istio/3/20250426193859.png)

```bash
# DestinationRule 적용 : ROUND_ROBIN
cat ch6/simple-backend-dr-rr.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: simple-backend-dr
spec:
  host: simple-backend.istioinaction.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      simple: ROUND_ROBIN # 엔드포인트 결정을 '순서대로 돌아가며'

kubectl apply -f ch6/simple-backend-dr-rr.yaml -n istioinaction

# 확인 : DestinationRule 단축어 dr
kubectl get dr -n istioinaction
NAME                HOST                                             AGE
simple-backend-dr   simple-backend.istioinaction.svc.cluster.local   11s

kubectl get destinationrule simple-backend-dr -n istioinaction \
 -o jsonpath='{.spec.trafficPolicy.loadBalancer.simple}{"\n"}'
ROUND_ROBIN

# 호출 : 이 예시 서비스 집합에서는 호출 체인을 보여주는 JSON 응답을 받느다
## simple-web 서비스는 simple-backend 서비스를 호출하고, 우리는 궁극적으로 simple-backend-1 에서 온 응답 메시지 Hello를 보게 된다.
## 몇 번 더 반복하면 simple-backend-1 과 simple-backend-2 에게 응답을 받는다. 
curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body"

# 반복 호출 확인 : 파드 비중은 backend-2가 2개임
for in in {1..10}; do curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body"; done
for in in {1..50}; do curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body"; done | sort | uniq -c | sort -nr

## "lbPolicy": "LEAST_REQUEST"
# RR은 기본값이여서, 해당 부분 설정이 이전과 다르게 없다
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-web.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json
...

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' -o json
```

---

### **다양한 로드 밸런싱 알고리즘 성능 비교**

- **라운드 로빈**은 단순하지만 리소스 상태를 고려하지 않음
- **랜덤**도 리소스를 고려하지 않음
- **최소 커넥션(LEAST_CONN)** 은 가장 적은 요청이 걸린 엔드포인트를 선택

Fortio로 부하 테스트를 통해 차이를 관찰할 수 있다.

```bash
# 호출 3회 반복 : netshoot 에서 서비스명으로 내부 접속
kubectl exec -it netshoot -- time curl -s -o /dev/null http://simple-web.istioinaction
kubectl exec -it netshoot -- time curl -s -o /dev/null http://simple-web.istioinaction
kubectl exec -it netshoot -- time curl -s -o /dev/null http://simple-web.istioinaction
real    0m 0.17s
user    0m 0.00s
sys     0m 0.00s
...

# mac 설치(windows, docker 모두 지원함)
brew install fortio
fortio -h
fortio server
open http://127.0.0.1:8080/fortio

fortio curl http://simple-web.istioinaction.io:30000
21:27:33.233 r1 [INF] scli.go:122> Starting, command="Φορτίο", version="1.69.4 h1:G0DXdTn8/QtiCh+ykBXft8NcOCojfAhQKseHuxFVePE= go1.24.2 arm64 darwin", go-max-procs=10
HTTP/1.1 200 OK
...
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426212621.png)

![]({{ site.url }}/img/post/devops/study/istio/3/20250426212823.png)

> 그림 출처: https://netpple.github.io/docs/istio-in-action/Istio-ch6-resilience

- Fortio를 사용해서 60초 동안 10개의 커넥션을 통해 초단 1000개의 요청을 보낸다.
- Fortio는 각 호출의 지연 시간을 추적하고 지연 시간 백분위수 분석과 함께 히스토그램에 표시한다.
- 테스트전 지연시간을 1초까지 늘린 simple-backend-1 서비스를 도입할 것이다.
	- 이는 엔드포인트 중 하나에 긴 가비지 컬렉션 이벤트 또는 기타 애플리케이션 지연 시간이 발생한 상황을 시뮬레이션한 것
- 로드밸런싱 전략을 라운드로빈 / 랜던 /최소 커넥션으로 바꿔가며 차이를 관찰한다.

```bash
# 지연된 simple-backend-1 배포
cat ch6/simple-backend-delayed.yaml
...
      - env:
        - name: "LISTEN_ADDR"
          value: "0.0.0.0:8080"
        - name: "SERVER_TYPE"
          value: "http"                      
        - name: "NAME"
          value: "simple-backend"      
        - name: "MESSAGE"
          value: "Hello from simple-backend-1"
        - name: "TIMING_VARIANCE"
          value: "10ms"                              
        - name: "TIMING_50_PERCENTILE"
          value: "1000ms"                                      
        - name: KUBERNETES_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        image: nicholasjackson/fake-service:v0.17.0
...
kubectl apply -f ch6/simple-backend-delayed.yaml -n istioinaction

# 기존의 simple-backend-1과 simple-backend-2의 labelselector가 같은 값이기 때문에 TIMING_50_PERCENTILE 환경변수가 simple-backend-1에 적용이 되지 않을 수도 있다.
# 물론 다른 파드 중에 적용이 되기 때문에 실습자체에는 문제가 없다.
# 하지만 원하는 파드에 적용시키려면 simple-backend-1를 삭제하고,
# lebelselector에 simple-backend-2와 구분할 수 있는 값을 하나 더 추가 후
# 다시 배포해주어야한다.
kubectl delete -f ch6/simple-backend-delayed.yaml -n istioinaction

vi ch6/simple-backend-delayed.yaml
...
spec:
  replicas: 1
  selector:
    matchLabels:
      app: simple-backend
      v: v1
  template:
    metadata:
      labels:
        app: simple-backend
        v: v1
...

kubectl apply -f ch6/simple-backend-delayed.yaml -n istioinaction

kubectl exec -it deploy/simple-backend-1 -n istioinaction -- env | grep -e TIMING_50 -e HOSTNAME
HOSTNAME=simple-backend-1-7ccc8768cb-8j77l
TIMING_50_PERCENTILE=1000ms

# 테스트(반복 호출)
curl -s http://simple-web.istioinaction.io:30000 | grep duration              
  "duration": "1.039652s",
      "duration": "1.001206s",
```

![]({{ site.url }}/img/post/devops/study/istio/3/11.32.53.png)
- Title : **roundrobin**
- URL : **[http://simple-web.istioinaction.io:30000](http://simple-web.istioinaction.io:30000)**
- QPS : **1000**
- Duration : **60s**
- Threads : **10**
- Jitter: **Check**
- No Catch-up : **Uncheck**
- Extra Headers
    - **User-Agent: fortio**
- Timeout : **2000ms**

![]({{ site.url }}/img/post/devops/study/istio/3/20250426234216.png)
![]({{ site.url }}/img/post/devops/study/istio/3/20250426234240.png) 25%의 사용자는 불편함을 겪게 된다.
(RANDOM)
```bash
#
cat ch6/simple-backend-dr-random.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: simple-backend-dr
spec:
  host: simple-backend.istioinaction.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      simple: RANDOM

kubectl apply -f ch6/simple-backend-dr-random.yaml -n istioinaction

# 확인
kubectl get destinationrule simple-backend-dr -n istioinaction \
 -o jsonpath='{.spec.trafficPolicy.loadBalancer.simple}{"\n"}'
RANDOM

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-web.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json | grep lbPolicy
"lbPolicy": "RANDOM",
```
> fortio에서 이전 페이지로 가면 기존 설정값이 입력되어 있다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250426234852.png) 라운드 로빈과 비슷하다.


(Least connection)
```bash
cat ch6/simple-backend-dr-least-conn.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: simple-backend-dr
spec:
  host: simple-backend.istioinaction.svc.cluster.local
  trafficPolicy:
    loadBalancer:
      simple: LEAST_CONN

kubectl apply -f ch6/simple-backend-dr-least-conn.yaml -n istioinaction

# 확인
kubectl get destinationrule simple-backend-dr -n istioinaction \
 -o jsonpath='{.spec.trafficPolicy.loadBalancer.simple}{"\n"}'
LEAST_CONN

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-web.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json | grep lbPolicy
"lbPolicy": "LEAST_REQUEST",
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250426235147.png)
![]({{ site.url }}/img/post/devops/study/istio/3/20250426235212.png)
> 실습 완료 후 Ctrl + C로 Fortio 서버를 종료하자.

- 로드 테스트를 종합해보면
	1. 여러 로드 밸런서는 현실적인 서비스 지연 시간 동작하에서 만들어내는 결과가 서로 다르다.
	2. 히스토그램과 백분위수는 모두 다르다.
	3. 최소 커넥션이 랜덤과 라운드 로빈보다 성능이 좋다.
	- 라운드 로빈과 랜덤은 모두 간당한 로드 밸런싱 알고리듬이다. 즉, 구현과 이해가 쉽다.
		- 라운드로빈: 엔드포인트를 차례대로 요청을 전달
		- 랜덤: 엔드포인트를 무작위로 균일하고 전달
		- 테스트 결과는 로드 밸런서 풀의 엔드포인트가 일반적으로 균일하지 않음
		- 엔드포인트에는 지연 시간을 늘리는 가비지 컬렉션이나 리소스 경합이 일어날 수 있고 라운드 로빈과 랜덤은 런타임 동작을 고려하지 않는다.
	- 최소 커넥션 로드밸런서는 특정 엔드포인트의 지연 시간을 고려한다.
		- 요청을 엔드포인트로 보낼 때 대기열 깊이 queue depth를 살펴 활성 요청 개수를 파악하고, 활성 요청이 가장 적은 엔드포인트를 고른다.
		- 이런 알고리듬 유형을 사용하면, 형편없이 동작하는 엔드포인트로 요청을 보내는 것을 피하고 좀 더 빠르게 응답하는 엔드포인트를 선호할 수 있다.

---

## **지역 인식 로드 밸런싱**

서비스가 여러 리전에 배포되었을 때,
가장 가까운 지역으로 트래픽을 우선 라우팅하는 기능이다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250420175603.png)

ex) us-west1에 배포된 서비스는 us-west1에 있는 백엔드를 우선 호출한다.
- Istio는 쿠버네티스 노드 레이블 (topology.kubernetes.io/region)을 이용해 지역 인식 라우팅 수행
- 필요한 경우 수동으로 istio-locality 레이블 설정 가능

```bash
# cat ch6/simple-service-locality.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: simple-web
  name: simple-web
spec:
  replicas: 1
  selector:
    matchLabels:
      app: simple-web
  template:
    metadata:
      labels:
        app: simple-web
        istio-locality: us-west1.us-west1-a
...
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: simple-backend
  name: simple-backend-1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: simple-backend
  template:
    metadata:
      labels:
        app: simple-backend
        istio-locality: us-west1.us-west1-a
        version: v1 # 추가해두자!
...
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: simple-backend
  name: simple-backend-2
spec:
  replicas: 2
  selector:
    matchLabels:
      app: simple-backend
  template:
    metadata:
      labels:
        app: simple-backend
        istio-locality: us-west1.us-west1-b
        version: v2 # 추가해두자!
...
```

서비스를 배포
```bash
# 위 알고리즘 테스트에서 지연시간을 늘릴때 원하는 파드에 환경변수를 적용하기 위해
# 레이블을 추가했기 때문에 실습 파일과 싱크가 맞지 않는다.
# 그래서 지우고 다시 생성한다.
k delete -f ch6/simple-backend-delayed.yaml -n istioinaction
deployment.apps "simple-backend-1" deleted

kubectl apply -f ch6/simple-service-locality.yaml -n istioinaction
deployment.apps/simple-web unchanged
deployment.apps/simple-backend-1 created
deployment.apps/simple-backend-2 unchanged

# 확인
## simple-backend-1 : us-west1-a  (same locality as simple-web)
kubectl get deployment.apps/simple-backend-1 -n istioinaction \
-o jsonpath='{.spec.template.metadata.labels.istio-locality}{"\n"}'
us-west1.us-west1-a

## simple-backend-2 : us-west1-b
kubectl get deployment.apps/simple-backend-2 -n istioinaction \
-o jsonpath='{.spec.template.metadata.labels.istio-locality}{"\n"}'
us-west1.us-west1-b
```

![]({{ site.url }}/img/post/devops/study/istio/3/20250420175603.png)

호출 테스트 1 - 지역 정보를 고려하지 않고 simple-backend 모든 엔드포인트로 트래픽이 로드 밸런싱 됨
```bash
# 신규 터미널 : 반복 접속 실행 해두기
while true; do curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body" ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

# 호출 : 이 예시 서비스 집합에서는 호출 체인을 보여주는 JSON 응답을 받느다
curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body"

# 반복 호출 확인 : 파드 비중은 backend-2가 2개임
for in in {1..10}; do curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body"; done
for in in {1..50}; do curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body"; done | sort | uniq -c | sort -nr
  34 "Hello from simple-backend-2"
  16 "Hello from simple-backend-1"

```

- Istio에서 지역 인식 로드밸런싱을 하려면 헬스체크를 설정해야한다.
	- 헬스 체크가 없으면 Istio가 다음 지역으로 넘기는 판단 기준이 무엇인지 알 수 없다.
	- 이상값 감지는 엔드포인트의 동작, 엔드포인트가 정상적으로 보이는지 여부를 수동적으로 감시한다.
	- 엔드포인트가 오류를 반환하는지 지켜보다가, 오류가 반환되면 엔드포인트를 비정상으로 표시한다.

- simple-backend 서비스에 이상값 감지를 설정해 수동적인 헬스 체크 설정을 추가

```bash
cat ch6/simple-backend-dr-outlier.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: simple-backend-dr
spec:
  host: simple-backend.istioinaction.svc.cluster.local
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 1
      interval: 5s
      baseEjectionTime: 30s
      maxEjectionPercent: 100

kubectl apply -f ch6/simple-backend-dr-outlier.yaml -n istioinaction

# 확인
kubectl get dr -n istioinaction simple-backend-dr -o jsonpath='{.spec}' | jq

# 반복 호출 확인 : 파드 비중 확인
for in in {1..10}; do curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body"; done
for in in {1..50}; do curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body"; done | sort | uniq -c | sort -nr
  50 "Hello from simple-backend-1"

# proxy-config : simple-web 에서 simple-backend 정보 확인
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-web.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local        
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-web.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json
...
        },
        "outlierDetection": {
            "consecutive5xx": 1,
            "interval": "5s",
            "baseEjectionTime": "30s",
            "maxEjectionPercent": 100,
            "enforcingConsecutive5xx": 100,
            "enforcingSuccessRate": 0
        },
...

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local'
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' -o json
...
                "healthStatus": {
                    "edsHealthStatus": "HEALTHY"
                },
                "weight": 1,
                "priority": 1,
                "locality": {
                    "region": "us-west1",
                    "zone": "us-west1-b"
                }
            
...

# 로그 확인
kubectl logs -n istioinaction -l app=simple-backend -c istio-proxy -f
kubectl stern -l app=simple-backend -n istioinaction
...
```

![]({{ site.url }}/img/post/devops/study/istio/3/20250427000322.png)

호출 테스트 2 -> 오동작 주입 후 확인
```bash
# HTTP 500 에러를 일정비율로 발생
cat ch6/simple-service-locality-failure.yaml
...
        - name: "ERROR_TYPE"
          value: "http_error"           
        - name: "ERROR_RATE"
          value: "1"                              
        - name: "ERROR_CODE"
          value: "500"  
...
kubectl apply -f ch6/simple-service-locality-failure.yaml -n istioinaction

# simple-backend-1- Pod 가 Running 상태로 완전히 배포된 후에 호출 확인

# 반복 호출 확인 : 파드 비중 확인
for in in {1..10}; do curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body"; done
for in in {1..50}; do curl -s http://simple-web.istioinaction.io:30000 | jq ".upstream_calls[0].body"; done | sort | uniq -c | sort -nr
  50 "Hello from simple-backend-2"

# 확인
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local'        
ENDPOINT            STATUS      OUTLIER CHECK     CLUSTER
10.10.0.23:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
10.10.0.24:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
10.10.0.25:8080     HEALTHY     FAILED            outbound|80||simple-backend.istioinaction.svc.cluster.local

# simple-backend-1 500에러 리턴으로 outliercheck 실패 상태로 호출에서 제외됨
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' -o json
...
                "healthStatus": {
                    "failedOutlierCheck": true,
                    "edsHealthStatus": "HEALTHY"
                },
                ...
                "healthStatus": {
                    "edsHealthStatus": "HEALTHY"
                },
```

![]({{ site.url }}/img/post/devops/study/istio/3/20250427000443.png)

다음 실습을 위해 정상화
```bash
kubectl apply -f ch6/simple-service-locality.yaml -n istioinaction
```

---
## **요청 타임아웃 및 재시도**

네트워크 요청이 지연되거나 실패할 때 빠르게 감지하고 대처할 수 있다.
- **타임아웃**: 지연된 요청을 강제로 끊어버린다.
- **재시도**: 일시적인 실패를 다시 시도한다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250420175810.png)

타임아웃/재시도는 VirtualService 리소스 안에서 쉽게 설정할 수 있다.
### **실습: 타임아웃 설정**

```
# 환경을 재설정
kubectl apply -f ch6/simple-web.yaml -n istioinaction
kubectl apply -f ch6/simple-backend.yaml -n istioinaction
kubectl delete destinationrule simple-backend-dr -n istioinaction

# 호출 테스트
# simple-backend-1를 1초 delay로 응답
# 호출 테스트 : 보통 10~20ms 이내 걸림
curl -s http://simple-web.istioinaction.io:30000 | jq .code
time curl -s http://simple-web.istioinaction.io:30000 | jq .code
for in in {1..10}; do time curl -s http://simple-web.istioinaction.io:30000 | jq .code; done
200
curl -s http://simple-web.istioinaction.io:30000  0.00s user 0.00s system 3% cpu 0.177 total
jq .code  0.00s user 0.00s system 1% cpu 0.176 total
...

# simple-backend-1를 1초 delay로 응답하도록 배포
# (위에서 추가한 레이블을 삭제해두자.)
cat ch6/simple-backend-delayed.yaml
kubectl apply -f ch6/simple-backend-delayed.yaml -n istioinaction

kubectl describe pod -n istioinaction -l app=simple-backend | grep TIMING_50_PERCENTILE:
      TIMING_50_PERCENTILE:  1000ms
      TIMING_50_PERCENTILE:  150ms
      TIMING_50_PERCENTILE:  150ms

# 호출 테스트 : simple-backend-1로 로드밸런싱 될 경우 1초 이상 소요 확인
for in in {1..10}; do time curl -s http://simple-web.istioinaction.io:30000 | jq .code; done
...
200
curl -s http://simple-web.istioinaction.io:30000  0.00s user 0.01s system 1% cpu 1.032 total
jq .code  0.00s user 0.00s system 0% cpu 1.031 total
...

# 메시 클라이언트에서 simple-backend로 향하는 호출의 타임아웃을 0.5초로 지정
# 
cat ch6/simple-backend-vs-timeout.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: simple-backend-vs
spec:
  hosts:
  - simple-backend
  http:
  - route:
    - destination:
        host: simple-backend
    timeout: 0.5s
    
kubectl apply -f ch6/simple-backend-vs-timeout.yaml -n istioinaction

#
kubectl get vs -n istioinaction
NAME                        GATEWAYS                 HOSTS                             AGE
simple-backend-vs                                    ["simple-backend"]                14s
simple-web-vs-for-gateway   ["simple-web-gateway"]   ["simple-web.istioinaction.io"]   6h11m


# 호출 테스트 : 0.5s 이상 걸리는 호출은 타임아웃 발생 (500응답)
for in in {1..10}; do time curl -s http://simple-web.istioinaction.io:30000 | jq .code; done
...
200
curl -s http://simple-web.istioinaction.io:30000  0.00s user 0.00s system 5% cpu 0.174 total
jq .code  0.00s user 0.00s system 2% cpu 0.174 total
500
curl -s http://simple-web.istioinaction.io:30000  0.00s user 0.01s system 1% cpu 0.524 total
jq .code  0.00s user 0.00s system 0% cpu 0.523 total
...

# istio-proxy config 에서 위 timeout 적용 envoy 설정 부분 찾아 두자.
```

![]({{ site.url }}/img/post/devops/study/istio/3/12.17.04.png)
### **실습: 재시도 설정**

```
# 설정 초기화
kubectl apply -f ch6/simple-web.yaml -n istioinaction
kubectl apply -f ch6/simple-backend.yaml -n istioinaction

# VirtualService에서 최대 재시도를 0으로 설정
docker exec -it myk8s-control-plane bash
----------------------------------------
# Retry 옵션 끄기 : 최대 재시도 0 설정
istioctl install --set profile=default --set meshConfig.defaultHttpRetryPolicy.attempts=0
y
exit
----------------------------------------

# 확인
kubectl get istiooperators -n istio-system -o yaml
...
    meshConfig:
      defaultConfig:
        proxyMetadata: {}
      defaultHttpRetryPolicy:
        attempts: 0
      enablePrometheusMerge: true
...

# istio-proxy 에서 적용 부분 찾아보자
```

![]({{ site.url }}/img/post/devops/study/istio/3/20250420175743.png)

```bash
#
cat ch6/simple-backend-periodic-failure-503.yaml
...
        - name: "ERROR_TYPE"
          value: "http_error"           
        - name: "ERROR_RATE"
          value: "0.75"                              
        - name: "ERROR_CODE"
          value: "503"  
...

#
kubectl apply -f ch6/simple-backend-periodic-failure-503.yaml -n istioinaction

kubectl describe pod -n istioinaction -l app=simple-backend | grep ERROR
      ERROR_TYPE:            http_error
      ERROR_RATE:            0.75
      ERROR_CODE:            503

# 호출테스트 : simple-backend-1 호출 시 failures (500) 발생
# simple-backend-1 --(503)--> simple-web --(500)--> curl(외부)
for in in {1..10}; do time curl -s http://simple-web.istioinaction.io:30000 | jq .code; done
...
500
curl -s http://simple-web.istioinaction.io:30000  0.00s user 0.00s system 18% cpu 0.035 total
jq .code  0.00s user 0.00s system 7% cpu 0.035 total
...

# app, istio-proxy log 에서 500, 503 로그 확인해보자.
```

![]({{ site.url }}/img/post/devops/study/istio/3/12.22.37.png)

![]({{ site.url }}/img/post/devops/study/istio/3/12.23.15.png)

VirtualService를 사용해 simple-backend로 향하는 호출에 재시도를 2회로 명시적으로 설정
```bash
cat ch6/simple-backend-enable-retry.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: simple-backend-vs
spec:
  hosts:
  - simple-backend
  http:
  - route:
    - destination:
        host: simple-backend
    retries:
      attempts: 2

kubectl apply -f ch6/simple-backend-enable-retry.yaml -n istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/simple-web.istioinaction --name 80
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/simple-web.istioinaction --name 80 -o json
...
               "name": "simple-backend.istioinaction.svc.cluster.local:80",
                "domains": [
                    "simple-backend.istioinaction.svc.cluster.local",
                    "simple-backend",
                    "simple-backend.istioinaction.svc",
                    "simple-backend.istioinaction",
                    "10.200.1.161"
                ],
                "routes": [
                    {
                        "match": {
                            "prefix": "/"
                        },
                        "route": {
                            "cluster": "outbound|80||simple-backend.istioinaction.svc.cluster.local",
                            "timeout": "0s",
                            "retryPolicy": {
                                "retryOn": "connect-failure,refused-stream,unavailable,cancelled,retriable-status-codes",
                                "numRetries": 2,
...

# 호출테스트 : 모두 성공!
# simple-backend-1 --(503, retry 후 정상 응답)--> simple-web --> curl(외부)
for in in {1..10}; do time curl -s http://simple-web.istioinaction.io:30000 | jq .code; done

# app, istio-proxy log 에서 503 로그 확인해보자.

```

![]({{ site.url }}/img/post/devops/study/istio/3/12.29.35.png)
![]({{ site.url }}/img/post/devops/study/istio/3/12.29.51.png)
![]({{ site.url }}/img/post/devops/study/istio/3/12.34.38.png)
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: simple-backend-vs
spec:
  hosts:
  - simple-backend
  http:
  - route:
    - destination:
        host: simple-backend
    retries:
      attempts: 2 # 최대 재시도 횟수
      retryOn: gateway-error,connect-failure,retriable-4xx # 다시 시도해야 할 오류
      perTryTimeout: 300ms # 타임 아웃
      retryRemoteLocalities: true # 재시도 시 다른 지역의 엔드포인트에 시도할지 여부
```

500 이외의 다른 에러 발생 시에도 retry가 동작하는지 확인
```bash
# 500 에러 코드 리턴
cat ch6/simple-backend-periodic-failure-500.yaml
...
        - name: "ERROR_TYPE"
          value: "http_error"           
        - name: "ERROR_RATE"
          value: "0.75"                              
        - name: "ERROR_CODE"
          value: "500"
...

kubectl apply -f ch6/simple-backend-periodic-failure-500.yaml -n istioinaction

kubectl describe pod -n istioinaction -l app=simple-backend | grep ERROR
      ERROR_TYPE:            http_error
      ERROR_RATE:            0.75
      ERROR_CODE:            500

# envoy 설정 확인 : 재시도 동작(retryOn) 에 retriableStatusCodes 는 503만 있음.
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/simple-web.istioinaction --name 80 -o json
...
                       "route": {
                            "cluster": "outbound|80||simple-backend.istioinaction.svc.cluster.local",
                            "timeout": "0s",
                            "retryPolicy": {
                                "retryOn": "connect-failure,refused-stream,unavailable,cancelled,retriable-status-codes",
                                "numRetries": 2,
                                "retryHostPredicate": [
                                    {
                                        "name": "envoy.retry_host_predicates.previous_hosts",
                                        "typedConfig": {
                                            "@type": "type.googleapis.com/envoy.extensions.retry.host.previous_hosts.v3.PreviousHostsPredicate"
                                        }
                                    }
                                ],
                                "hostSelectionRetryMaxAttempts": "5",
                                "retriableStatusCodes": [
                                    503
                                ]
                            },
                            "maxGrpcTimeout": "0s"
                        },
...


# 호출테스트 : Retry 동작 안함.
# simple-backend-1 --(500, retry 안함)--> simple-web --(500)> curl(외부)
for in in {1..10}; do time curl -s http://simple-web.istioinaction.io:30000 | jq .code; done
...
200
curl -s http://simple-web.istioinaction.io:30000  0.00s user 0.00s system 4% cpu 0.184 total
jq .code  0.00s user 0.00s system 1% cpu 0.183 total
500
curl -s http://simple-web.istioinaction.io:30000  0.00s user 0.00s system 43% cpu 0.016 total
jq .code  0.00s user 0.00s system 17% cpu 0.015 total
...
```

![]({{ site.url }}/img/post/devops/study/istio/3/12.41.48.png)

모든 HTTP 500 코드(커넥션 수립 실패 및 스트림 거부 포함)를 재시도하는 VirtualService 재시도 정책 사용
```bash
cat ch6/simple-backend-vs-retry-500.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: simple-backend-vs
spec:
  hosts:
  - simple-backend
  http:
  - route:
    - destination:
        host: simple-backend
    retries:
      attempts: 2
      retryOn: 5xx # HTTP 5xx 모두에 재시도

kubectl apply -f ch6/simple-backend-vs-retry-500.yaml -n istioinaction

# 호출테스트 : 모두 성공!
# simple-backend-1 --(500, retry)--> simple-web --(200)> curl(외부)
for in in {1..10}; do time curl -s http://simple-web.istioinaction.io:30000 | jq .code; done

```

Advanced retries: Istio Extension API(EnvoyFilter)
- 기본적으로 백오프 시간은 25ms, 재시도할 수 있는 상태 코드는 HTTP 503 뿐이다.
- 이스티오 확장 API(EnvoyFilter)를 사용해 이 값들을 직접 바꿀 수 있다.

```bash
cat ch6/simple-backend-ef-retry-status-codes.yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
metadata:
  name: simple-backend-retry-status-codes
  namespace: istioinaction
spec:
  workloadSelector:
    labels:
      app: simple-web
  configPatches:
  - applyTo: HTTP_ROUTE
    match:
      context: SIDECAR_OUTBOUND
      routeConfiguration:
        vhost:
          name: "simple-backend.istioinaction.svc.cluster.local:80"          
    patch:
      operation: MERGE
      value:
        route:
          retry_policy: # 엔보이 설정에서 직접 나온다?
            retry_back_off: 
              base_interval: 50ms # 기본 간격을 늘린다
            retriable_status_codes: # 재시도할 수 있는 코드를 추가한다
            - 408
            - 400

# Envoy API를 직접 사용해 재시도 정책 설정값을 설정하고 재정의
# 408 에러코드를 발생
kubectl apply -f ch6/simple-backend-periodic-failure-408.yaml -n istioinaction

kubectl describe pod -n istioinaction -l app=simple-backend | grep ERROR
      ERROR_TYPE:            http_error
      ERROR_RATE:            0.75
      ERROR_CODE:            408

# 호출테스트 : 408 에러는 retryOn: 5xx 에 포함되지 않으므로 에러를 리턴.
# simple-backend-1 --(408)--> simple-web --(500)--> curl(외부)
for in in {1..10}; do time curl -s http://simple-web.istioinaction.io:30000 | jq .code; done
...
```

![]({{ site.url }}/img/post/devops/study/istio/3/12.49.47.png)

400 에러도 재시도 적용
```bash
cat ch6/simple-backend-ef-retry-status-codes.yaml
...
    patch:
      operation: MERGE
      value:
        route:
          retry_policy: # 엔보이 설정에서 직접 나온다?
            retry_back_off: 
              base_interval: 50ms # 기본 간격을 늘린다
            retriable_status_codes: # 재시도할 수 있는 코드를 추가한다
            - 408
            - 400

kubectl apply -f ch6/simple-backend-ef-retry-status-codes.yaml -n istioinaction

# 확인
kubectl get envoyfilter -n istioinaction -o json
kubectl get envoyfilter -n istioinaction
NAME                                AGE
simple-backend-retry-status-codes   45s

# VirtualService 에도 재시도 할 대상 코드 추가
cat ch6/simple-backend-vs-retry-on.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: simple-backend-vs
spec:
  hosts:
  - simple-backend
  http:
  - route:
    - destination:
        host: simple-backend
    retries:
      attempts: 2
      retryOn: 5xx,retriable-status-codes # retryOn 항목에 retriable-status-codes 를 추가

kubectl apply -f ch6/simple-backend-vs-retry-on.yaml -n istioinaction

# envoy 설정 확인 : 재시도 동작(retryOn) 에 5xx 과 retriableStatusCodes 는 408,400 있음.
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/simple-web.istioinaction --name 80 -o json
...
                        "route": {
                            "cluster": "outbound|80||simple-backend.istioinaction.svc.cluster.local",
                            "timeout": "0s",
                            "retryPolicy": {
                                "retryOn": "5xx,retriable-status-codes",
                                "numRetries": 2,
                                "retryHostPredicate": [
                                    {
                                        "name": "envoy.retry_host_predicates.previous_hosts",
                                        "typedConfig": {
                                            "@type": "type.googleapis.com/envoy.extensions.retry.host.previous_hosts.v3.PreviousHostsPredicate"
                                        }
                                    }
                                ],
                                "hostSelectionRetryMaxAttempts": "5",
                                "retriableStatusCodes": [
                                    408,
                                    400
                                ],
                                "retryBackOff": {
                                    "baseInterval": "0.050s"
                                }
                            },
                            "maxGrpcTimeout": "0s"
                        }
...

# 호출테스트 : 성공
# simple-backend-1 --(408, retry 성공)--> simple-web --> curl(외부)
for in in {1..10}; do time curl -s http://simple-web.istioinaction.io:30000 | jq .code; done
...
```

- 타임아웃과 재시도를 잘못 설정하면 시스템 아키텍처에서 의도치 않은 동작을 증폭시켜 시스템을 과부하시키고 연쇄 장애를 일으킬 수 있다.
- 복원력 있는 아키텍처를 구축하는 과정에서 마지막 퍼즐조각은 **재시도를 모두 건너뛰는 것**이다.
	- 즉, 재시도하는 대신 빠르게 실패하기!!
	- 부하를 더 늘리는 대신에 업스트림 시스템이 복구 될 수 있도록 부하를 잠시 제한할 수 있다.
	- 이를 위해 서킷 브레이커를 사용할 수 있다.

---

## **이스티오를 이용한 서킷 브레이킹**
**서킷 브레이커**는 장애가 심해졌을 때 시스템을 보호하는 장치다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250420175844.png)

Istio에서는 DestinationRule을 통해:
- 커넥션 수 제한
- 활성 요청 수 제한
- 이상값 감지로 비정상 엔드포인트 자동 제외
를 설정할 수 있다.
### **실습: 커넥션 풀 제한**

```bash
# (옵션) tracing 샘플링을 기본 1% -> 100% 늘려두기
# tracing.sampling=100
docker exec -it myk8s-control-plane bash
----------------------------------------
istioctl install --set profile=default --set meshConfig.accessLogFile=/dev/stdout --set meshConfig.defaultConfig.tracing.sampling=100 --set meshConfig.defaultHttpRetryPolicy.attempts=0
y
exit
----------------------------------------

# 확인
kubectl describe cm -n istio-system istio
...
defaultConfig:
  discoveryAddress: istiod.istio-system.svc:15012
  proxyMetadata: {}
  tracing:
    sampling: 100.0
    zipkin:
      address: zipkin.istio-system:9411
...

# 적용 : rollout 
kubectl rollout restart deploy -n istio-system istiod
kubectl rollout restart deploy -n istio-system istio-ingressgateway
kubectl rollout restart deploy -n istioinaction simple-web
kubectl rollout restart deploy -n istioinaction simple-backend-1
```

```bash
# 실습환경 구성
# 현재 적용되어 있는 상태
kubectl apply -f ch6/simple-web.yaml -n istioinaction
kubectl apply -f ch6/simple-web-gateway.yaml -n istioinaction
kubectl apply -f ch6/simple-backend-vs-retry-on.yaml -n istioinaction

# destinationrule 삭제
kubectl delete destinationrule --all -n istioinaction

# simple-backend-2 제거
kubectl scale deploy simple-backend-2 --replicas=0 -n istioinaction

# 응답지연(1초)을 발생하는 simple-backend-1 배포
kubectl apply -f ch6/simple-backend-delayed.yaml -n istioinaction

kubectl describe pod -n istioinaction -l app=simple-backend | grep TIMING_50_PERCENTILE:
      TIMING_50_PERCENTILE:  1000ms
      
# 테스트
curl -s http://simple-web.istioinaction.io:30000 | grep duration
  "duration": "1.018088s",
      "duration": "1.000413s",
```
이스티오의 커넥션 제한 서킷 브레이커 테스트
```bash
# 초당 요청을 하나 보내는(-qps1) 커넥션 하나(-c1)로 진행 : 백엔드가 대략 1초 후 반환하므로 트래픽이 원활하고 성공률이 100%여야 한다.
fortio load -quiet -jitter -t 30s -c 1 -qps 1 http://simple-web.istioinaction.io:30000
...
# target 50% 1.01282
# target 75% 1.01588
# target 90% 1.01772
# target 99% 1.01882
# target 99.9% 1.01893
...
Code 200 : 30 (100.0 %)
All done 30 calls (plus 1 warmup) 1013.289 ms avg, 1.0 qps
```

```bash
cat ch6/simple-backend-dr-conn-limit.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: simple-backend-dr
spec:
  host: simple-backend.istioinaction.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 1 # 커넥션 총 개수 Total number of connections
      http:
        http1MaxPendingRequests: 1 # 대기 중인 요청 Queued requests
        maxRequestsPerConnection: 1 # 커넥션당 요청 개수 Requests per connection
        maxRetries: 1 # Maximum number of retries that can be outstanding to all hosts in a cluster at a given time.
        http2MaxRequests: 1 # 모든 호스트에 대한 최대 동시 요청 개수 Maximum concurrent requests to all hosts

# DestinationRule 적용 (connection-limiting) 
kubectl apply -f ch6/simple-backend-dr-conn-limit.yaml -n istioinaction
kubectl get dr -n istioinaction

#
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-backend-1.istioinaction | egrep 'RULE|backend'
SERVICE FQDN                                            PORT      SUBSET     DIRECTION     TYPE             DESTINATION RULE
                                                        8080      -          inbound       ORIGINAL_DST     simple-backend-dr.istioinaction
simple-backend.istioinaction.svc.cluster.local          80        -          outbound      EDS              simple-backend-dr.istioinaction

# 설정 적용 확인
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-backend-1.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json
...
        "connectTimeout": "10s",
        "lbPolicy": "LEAST_REQUEST",
        "circuitBreakers": {
            "thresholds": [
                {
                    "maxConnections": 1, # tcp.maxConnections, 커넥션 총 개수 Total number of connections
                    "maxPendingRequests": 1, # http.http1MaxPendingRequests, 대기 중인 요청 Queued requests
                    "maxRequests": 1, # http.http2MaxRequests, 모든 호스트에 대한 최대 동시 요청 개수 
                    "maxRetries": 1, # http.maxRetries
                    "trackRemaining": true
                }
            ]
        },
        "typedExtensionProtocolOptions": {
            "envoy.extensions.upstreams.http.v3.HttpProtocolOptions": {
                "@type": "type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions",
                "commonHttpProtocolOptions": { 
                    "maxRequestsPerConnection": 1 # http.maxRequestsPerConnection, 커넥션당 요청 개수
...

# (참고) 기본값?
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system --fqdn simple-web.istioinaction.svc.cluster.local -o json
...
        "connectTimeout": "10s",
        "lbPolicy": "LEAST_REQUEST",
        "circuitBreakers": {
            "thresholds": [
                {
                    "maxConnections": 4294967295,
                    "maxPendingRequests": 4294967295,
                    "maxRequests": 4294967295,
                    "maxRetries": 4294967295,
                    "trackRemaining": true
...
```
테스트를 다시 실행해 이 설정을 검증한다.
커넥션 하나에 초당 요청을 하나 보낼 때 제대로 동작해야 한다.
```bash
# 초당 요청을 하나 보내는(-qps1) 커넥션 하나(-c1)로 진행 : 
fortio load -quiet -jitter -t 30s -c 1 -qps 1 --allow-initial-errors http://simple-web.istioinaction.io:30000
...
Sockets used: 5 (for perfect keepalive, would be 1)
Uniform: false, Jitter: true, Catchup allowed: true
IP addresses distribution:
127.0.0.1:30000: 5
Code 200 : 24 (85.7 %)
Code 500 : 4 (14.3 %)
All done 28 calls (plus 1 warmup) 1046.628 ms avg, 0.9 qps
```

```bash
# simple-web 디플로이먼트에 sidecar.istio.io/statsInclusionPrefixes="cluster.<이름>" 애너테이션 추가하자
## sidecar.istio.io/statsInclusionPrefixes: cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local
cat ch6/simple-web-stats-incl.yaml | grep statsInclusionPrefixes 
        sidecar.istio.io/statsInclusionPrefixes: "cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local"        
kubectl apply -f ch6/simple-web-stats-incl.yaml -n istioinaction

# 정확한 확인을 위해 istio-proxy stats 카운터 초기화
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
-- curl -X POST localhost:15000/reset_counters

# simple-web 에 istio-proxy 의 stats 조회
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend | grep overflow
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_cx_overflow: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_cx_pool_overflow: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_pending_overflow: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_retry_overflow: 0

kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend.istioinaction.svc.cluster.local.upstream
```
istio-proxy 상세 로그 확인 필요시
```bash
# 
kubectl exec -it deploy/simple-backend-1 -n istioinaction -c istio-proxy -- curl -X POST http://localhost:15000/logging\?connection\=debug
kubectl exec -it deploy/simple-backend-1 -n istioinaction -c istio-proxy -- curl -X POST http://localhost:15000/logging\?conn_handler\=debug
kubectl exec -it deploy/simple-backend-1 -n istioinaction -c istio-proxy -- curl -X POST http://localhost:15000/logging\?http2\=debug
kubectl exec -it deploy/simple-backend-1 -n istioinaction -c istio-proxy -- curl -X POST http://localhost:15000/logging\?multi_connection\=debug
kubectl exec -it deploy/simple-backend-1 -n istioinaction -c istio-proxy -- curl -X POST http://localhost:15000/logging\?pool\=debug
kubectl exec -it deploy/simple-backend-1 -n istioinaction -c istio-proxy -- curl -X POST http://localhost:15000/logging\?router\=debug
kubectl exec -it deploy/simple-backend-1 -n istioinaction -c istio-proxy -- curl -X POST http://localhost:15000/logging\?upstream\=debug
```
커넥션 개수와 초당 요청 수를 2로 늘리면?
커넥션고 ㅏ요청이 지정한 임계값(병렬 요청이 너무 많거나 요청이 너무 많이 쌓임)을 충분히 넘겨 서킷 브레이커를 동작시켰음을 확인
```bash
# 2개의 커넥션에서 요청을 초당 하나씩 보내기 : 요청이 28개 실패한 것으로 반환됐다(HTTP 5xx)
fortio load -quiet -jitter -t 30s -c 2 -qps 2 --allow-initial-errors http://simple-web.istioinaction.io:30000
...
Sockets used: 31 (for perfect keepalive, would be 2)
Uniform: false, Jitter: true, Catchup allowed: true
IP addresses distribution:
127.0.0.1:30000: 31
Code 200 : 27 (49.1 %)
Code 500 : 28 (50.9 %)
All done 55 calls (plus 2 warmup) 711.293 ms avg, 1.7 qps
...

# 로그 확인 : simple-web
kubectl logs -n istioinaction -l app=simple-web -c istio-proxy -f
...
# 오류 요청 (503 Service Unavailable, UO 플래그
## HTTP 503: 서비스가 일시적으로 사용 불가능. Envoy가 업스트림 서버(simple-backend:80)에 요청을 전달하지 못함.
## UO 플래그: "Upstream Overflow"로, Envoy의 서킷 브레이커가 트리거되었거나 최대 연결/요청 제한에 도달했음을 의미.
## upstream_reset_before_response_started{overflow}: 업스트림 서버가 응답을 시작하기 전에 연결이 리셋되었으며, 이는 오버플로우(리소스 제한)로 인함.
[2025-04-26T16:13:48.699Z] "GET // HTTP/1.1" 503 UO upstream_reset_before_response_started{overflow} - "-" 0 81 4 - ...

# 오류 요청 (500 Internal Server Error) : 최종 사용자에게 500 에러 리턴
[2025-04-26T16:13:48.650Z] "GET / HTTP/1.1" 500 - via_upstream - "-" 0 687 11 11 ...
## simple-web 서비스에서 backend 정보를 가져오지 못하여 애플리케이션 레벨 오류 발생
## HTTP 500: 서버 내부 오류. 업스트림 서버(simple-web:30000)가 요청을 처리하는 중 예기치 않은 오류 발생.
## via_upstream: 오류가 Envoy가 아니라 업스트림 서버에서 발생했음을 나타냄.
...

# 통계 확인 : 18개로 +/- 1개 정도는 무시하고 보자. 성능 테스트 실패 갯수(17개)와 아래 통계값이 일치 한다(18-1).
# 큐 대기열이 늘어나 결국 서킷 브레이커를 발동함. 
# fail-fast 동작은 이렇게 보류 중 혹은 병행 요청 갯수가 서킷 브레이커 임계값을 넘어 수행된다.
# The fail-fast behavior comes from those pending or parallel requests exceeding the circuit-breaking thresholds. 
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend | grep overflow
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_cx_overflow: 56
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_cx_pool_overflow: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_pending_overflow: 18
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_retry_overflow: 0

kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend.istioinaction.svc.cluster.local.upstream
```


![]({{ site.url }}/img/post/devops/study/istio/3/1.16.21.png)

![]({{ site.url }}/img/post/devops/study/istio/3/1.16.36.png)

jaeger 확인 - 실패 trace 확인 - simple-backend istio-proxy가 UO로 503을 리턴 -> simple-web은 500을 사용자에게 최종 리턴

![]({{ site.url }}/img/post/devops/study/istio/3/1.19.10.png)

프로메테우스 메트릭
- `envoy_cluster_upstream_cx_overflow`

![]({{ site.url }}/img/post/devops/study/istio/3/1.20.27.png)
- `envoy_cluster_upstream_rq_pending_overflow`

![]({{ site.url }}/img/post/devops/study/istio/3/1.21.02.png)

... (여기서부터는 시간 부족으로 추후 업데이트 예정 / 일단 스터디 자료로 대체)
병렬로 발생하는 요청(현재 로드테스트 동시 요청 2)을 더 처리하고자 http2MaxRequests(parallel requests)를 늘려보자.
```bash
# 설정 전 확인
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-web.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json | grep maxRequests 
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-backend-1.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json | grep maxRequests 
                    "maxRequests": 1,
                    "maxRequestsPerConnection": 1

# http2MaxRequests 조정: 1 → 2, '동시요청 처리개수'를 늘림
kubectl patch destinationrule simple-backend-dr -n istioinaction \
-n istioinaction --type merge --patch \
'{"spec": {"trafficPolicy": {"connectionPool": {"http": {"http2MaxRequests": 2}}}}}'

# 설정 후 확인
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-backend-1.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json | grep maxRequests 
                    "maxRequests": 2,
                    "maxRequestsPerConnection": 1

# istio-proxy stats 카운터 초기화
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
-- curl -X POST localhost:15000/reset_counters

# 로그 확인 : simple-web >> 아래 500(503) 발생 로그 확인
kubectl logs -n istioinaction -l app=simple-web -c istio-proxy -f
... 
## jaeger 에서 Tags 필터링 찾기 : guid:x-request-id=3e1789ba-2fa4-94b6-a782-cfdf0a405e13
[2025-04-26T16:27:45.735Z] "GET / HTTP/1.1" 503 UO upstream_reset_before_response_started{overflow} - "-" 0 81 0 - "172.18.0.1" "fortio.org/fortio-1.69.3" "3e1789ba-2fa4-94b6-a782-cfdf0a405e13" "simple-backend:80" "-" outbound|80||simple-backend.istioinaction.svc.cluster.local - 10.200.1.137:80 172.18.0.1:0 - -
[2025-04-26T16:27:45.734Z] "GET / HTTP/1.1" 500 - via_upstream - "-" 0 688 15 15 "172.18.0.1" "fortio.org/fortio-1.69.3" "3e1789ba-2fa4-94b6-a782-cfdf0a405e13" "simple-web.istioinaction.io:30000" "10.10.0.18:8080" inbound|8080|| 127.0.0.6:43259 10.10.0.18:8080 172.18.0.1:0 outbound_.80_._.simple-web.istioinaction.svc.cluster.local default
...

# 로그 확인 : simple-backend >> 503 에러가 발생하지 않았다??? 
kubectl logs -n istioinaction -l app=simple-backend -c istio-proxy -f


# 2개의 커넥션에서 요청을 초당 하나씩 보내기 : 동시요청 처리개수가 기존 1 에서 2로 증가되어서 거의 대부분 처리했다. >> 참고로 모두 성공 되기도함.
fortio load -quiet -jitter -t 30s -c 2 -qps 2 --allow-initial-errors http://simple-web.istioinaction.io:30000
...
Sockets used: 3 (for perfect keepalive, would be 2)
Code 200 : 33 (97.1 %)
Code 500 : 1 (2.9 %)
All done 34 calls (plus 2 warmup) 1789.433 ms avg, 1.1 qps
...

# 'cx_overflow: 40' 대비 'rq_pending_overflow: 1' 가 현저히 낮아짐을 확인
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend | grep overflow
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_cx_overflow: 40
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_cx_pool_overflow: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_pending_overflow: 1
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_retry_overflow: 0

kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend.istioinaction.svc.cluster.local.upstream
```
- kiali 확인: 실제 simple-web 입장에서는 500(503)이 출력되지만, simple-backend에는 503이 없다.

![]({{ site.url }}/img/post/devops/study/istio/3/20250427013145.png)
- jaeger 에서 Tags 필터링 찾기 : `guid:x-request-id=3e1789ba-2fa4-94b6-a782-cfdf0a405e13`, `guid:x-request-id=304fd07c-0d09-9749-8e36-c0758c7464e3`

![]({{ site.url }}/img/post/devops/study/istio/3/20250427013204.png)
- simple-backend에서는 정상 301 응답을 주었고, simple-web에서 503(UO)가 발생되었다. 503 발생 주체는 simple-web istio-proxy인가?

![]({{ site.url }}/img/post/devops/study/istio/3/20250427013437.png)
보류 대기열 깊이를 2로 늘리고 다시 실행
```bash
# http1MaxPendingRequests : 1 → 2, 'queuing' 개수를 늘립니다
kubectl patch destinationrule simple-backend-dr \
-n istioinaction --type merge --patch \
'{"spec": {"trafficPolicy": {"connectionPool": {"http": {"http1MaxPendingRequests": 2}}}}}'

#
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-web.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json | grep maxPendingRequests 
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-backend-1.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json | grep maxPendingRequests           
                    "maxPendingRequests": 2,
                    
# istio-proxy stats 카운터 초기화
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
-- curl -X POST localhost:15000/reset_counters


# 2개의 커넥션에서 요청을 초당 하나씩 보내기 : 모두 성공!
fortio load -quiet -jitter -t 30s -c 2 -qps 2 --allow-initial-errors http://simple-web.istioinaction.io:30000
...
Sockets used: 2 (for perfect keepalive, would be 2) # 큐 길이 증가 덕분에, 소켓을 2개만 사용했다.
Code 200 : 33 (100.0 %)
All done 33 calls (plus 2 warmup) 1846.745 ms avg, 1.1 qps
...

# 'cx_overflow가 45이 발생했지만, upstream_rq_pending_overflow 는 이다!
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend | grep overflow
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_cx_overflow: 45
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_cx_pool_overflow: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_pending_overflow: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_retry_overflow: 0

kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend.istioinaction.svc.cluster.local.upstream
```
![]({{ site.url }}/img/post/devops/study/istio/3/20250427013513.png)
- 서킷 브레이커가 발동되면 통계를 보고 무슨 일이 일어났는지 확인할 수 있다. 그런데 런타임은?
- simple-web -> simple-backend 호출
	- 그런데 서킷 브레이커 때문에 요청이 실패한다면, simple-web은 그 사실을 어떻게 알고 애플리케이션이나 네트워크 장애 문제와 구별할 수 있는가?

- 요청 서킷 브레이커 임계값을 넘겨 실패하면, 이스티오 서비스 프록시는 `x-envoy-overloaded` 헤더를 추가한다.
- 이를 테스트하는 한 가지 방법은 커넥션 제한을 가장 엄격한 수준으로 설정하고(커넥션, 보류 요청, 최대 요청을 1로 설정) 로드 테스트를 다시 수행한다.
- 로드 테스트를 실행하는 도중에 단일 curl 명령도 실행하면 서킷 브레이커 때문에 실패할 가능성이 높다.

```bash
kubectl patch destinationrule simple-backend-dr \
-n istioinaction --type merge --patch \
'{"spec": {"trafficPolicy": {"connectionPool": {"http": {"http1MaxPendingRequests": 1}}}}}'

kubectl patch destinationrule simple-backend-dr -n istioinaction \
-n istioinaction --type merge --patch \
'{"spec": {"trafficPolicy": {"connectionPool": {"http": {"http2MaxRequests": 1}}}}}'

# 설정 적용 확인
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-backend-1.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json

# istio-proxy stats 카운터 초기화
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
-- curl -X POST localhost:15000/reset_counters

# 로드 테스트
fortio load -quiet -jitter -t 30s -c 2 -qps 2 --allow-initial-errors http://simple-web.istioinaction.io:30000

# 로드 테스트 하는 상태에서 아래 curl 접속 
curl -v http://simple-web.istioinaction.io:30000
{
  "name": "simple-web",
  "uri": "/",
  "type": "HTTP",
  "ip_addresses": [
    "10.10.0.18"
  ],
  "start_time": "2025-04-22T04:23:50.468693",
  "end_time": "2025-04-22T04:23:50.474941",
  "duration": "6.247ms",
  "body": "Hello from simple-web!!!",
  "upstream_calls": [
    {
      "uri": "http://simple-backend:80/",
      "headers": {
        "Content-Length": "81",
        "Content-Type": "text/plain",
        "Date": "Tue, 22 Apr 2025 04:23:50 GMT",
        "Server": "envoy",
        "X-Envoy-Overloaded": "true" # Header indication
      },
      "code": 503,
      "error": "Error processing upstream request: http://simple-backend:80//, expected code 200, got 503"
    }
  ],
  "code": 500
}
```

- 일반적으로 네트워크가 실패할 수 있다는 점을 감안해 애플리케이션 코드를 작성해야 한다.
- 애플리케이션 코드가 이 헤더를 확인하면 호출한 클라이언트에게 응답을 보내기 위해 대체 전략(fallback)을 사용하는 결정을 내릴 수 있다.
### **실습: 이상값 감지 설정**

- 실습 환경 초기화
	- 이스티오의 기본 재시도 메커니즘도 비활성화
	- 재시도와 이상값 감지는 잘 어울리지만, 여기서는 이상값 감지 기능을 고립시킨다.
	- 재시도는 마지막에 추가하여 이상값 감지와 재시도가 어떻게 서로 보완하는지 확인

```bash
#
kubectl delete destinationrule --all -n istioinaction
kubectl delete vs simple-backend-vs -n istioinaction

# disable retries (default) : 이미 적용 되어 있음
docker exec -it myk8s-control-plane bash
----------------------------------------
istioctl install --set profile=default --set meshConfig.defaultHttpRetryPolicy.attempts=0
y
exit
----------------------------------------

#
kubectl apply -f ch6/simple-backend.yaml -n istioinaction
kubectl apply -f ch6/simple-web-stats-incl.yaml -n istioinaction # 통계 활성화

# istio-proxy stats 카운터 초기화
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
-- curl -X POST localhost:15000/reset_counters

# 호출 테스트 : 모두 성공
fortio load -quiet -jitter -t 30s -c 2 -qps 2 --allow-initial-errors http://simple-web.istioinaction.io:30000

# 확인
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend.istioinaction.svc.cluster.local.upstream
```
이상값 감지를 설정
```bash
#
cat ch6/simple-backend-dr-outlier-5s.yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: simple-backend-dr
spec:
  host: simple-backend.istioinaction.svc.cluster.local
  trafficPolicy:
    outlierDetection:
      consecutive5xxErrors: 1 # 잘못된 요청이 하나만 발생해도 이상값 감지가 발동. 기본값 5
      interval: 5s # 이스티오 서비스 프록시가 체크하는 주기. 기본값 10초. Time interval between ejection sweep analysis
      baseEjectionTime: 5s # 서비스 엔드포인트에서 제거된다면, 제거 시간은 n(해당 엔드포인트가 쫓겨난 횟수) * baseEjectionTime. 해당 시간이 지나면 로드 밸런싱 풀에 다시 추가됨. 기본값 30초. 
      maxEjectionPercent: 100 # 로드 밸런싱 풀에서 제거 가능한 호스트 개수(%). 모든 호스트가 오동작하면 어떤 요청도 통과 못함(회로가 열린 것과 같다). 기본값 10%

kubectl apply -f ch6/simple-backend-dr-outlier-5s.yaml -n istioinaction
kubectl get dr -n istioinaction

#
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/simple-web.istioinaction --fqdn simple-backend.istioinaction.svc.cluster.local -o json
...
        "outlierDetection": {
            "consecutive5xx": 1,
            "interval": "5s",
            "baseEjectionTime": "5s",
            "maxEjectionPercent": 100,
            "enforcingConsecutive5xx": 100,
            "enforcingSuccessRate": 0
        },
...

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local'
ENDPOINT            STATUS      OUTLIER CHECK     CLUSTER
10.10.0.27:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
10.10.0.29:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
10.10.0.30:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local



# 통계 초기화
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
-- curl -X POST localhost:15000/reset_counters

# 엔드포인트 모니터링 먼저 해두기 : 신규 터미널
	while true; do docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' ; date; sleep 1; echo; done
	ENDPOINT            STATUS      OUTLIER CHECK     CLUSTER
10.10.0.27:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
10.10.0.29:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
10.10.0.30:8080     HEALTHY     FAILED            outbound|80||simple-backend.istioinaction.svc.cluster.local


# 로드 테스트 실행 : 기존 오류율 대비 극적으로 감소. 오동작하는 엔드포인트를 잠시 제거했기 때문이다.
fortio load -quiet -jitter -t 30s -c 2 -qps 2 --allow-initial-errors http://simple-web.istioinaction.io:30000
...
Sockets used: 5 (for perfect keepalive, would be 2)
Code 200 : 58 (96.7 %)
Code 500 : 2 (3.3 %)
All done 60 calls (plus 2 warmup) 166.592 ms avg, 2.0 qps
...

# 통계 확인
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend.istioinaction.svc.cluster.local.upstream

# 엔드포인트 이상 감지 전에 3번 실패했고, 이상 상태가 되고 나면 로드 밸런서 풀에서 제거되어서 이후 부터는 정상 엔드포인트로 호출 응답됨.
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend | grep outlier
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_active: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_consecutive_5xx: 3
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_detected_consecutive_5xx: 3
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_detected_consecutive_gateway_failure: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_detected_consecutive_local_origin_failure: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_detected_failure_percentage: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_detected_local_origin_failure_percentage: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_detected_local_origin_success_rate: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_detected_success_rate: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_enforced_consecutive_5xx: 3
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_enforced_consecutive_gateway_failure: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_enforced_consecutive_local_origin_failure: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_enforced_failure_percentage: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_enforced_local_origin_failure_percentage: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_enforced_local_origin_success_rate: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_enforced_success_rate: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_enforced_total: 3
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_overflow: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_success_rate: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.outlier_detection.ejections_total: 3


# 5초 후(baseEjectionTime: 5s) 다시 엔드포인트 모니터링
ENDPOINT            STATUS      OUTLIER CHECK     CLUSTER
10.10.0.27:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
10.10.0.29:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local
10.10.0.30:8080     HEALTHY     OK                outbound|80||simple-backend.istioinaction.svc.cluster.local

```

![]({{ site.url }}/img/post/devops/study/istio/3/20250420175919.png)
![]({{ site.url }}/img/post/devops/study/istio/3/20250427014204.png)
![]({{ site.url }}/img/post/devops/study/istio/3/20250427014224.png)

- 오류률을 더 개선해보자.
- 기본 재시도 설정을 추가
- VirtualService에 명시적으로 설정 가능(현재 mesh 기본 재시도 0)

```bash
#
cat ch6/simple-backend-vs-retry-500.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: simple-backend-vs
spec:
  hosts:
  - simple-backend
  http:
  - route:
    - destination:
        host: simple-backend
    retries:
      attempts: 2
      retryOn: 5x

kubectl apply -f ch6/simple-backend-vs-retry-500.yaml -n istioinaction

# 통계 초기화
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
-- curl -X POST localhost:15000/reset_counters

# 엔드포인트 모니터링 먼저 해두기 : 신규 터미널
while true; do docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/simple-web.istioinaction --cluster 'outbound|80||simple-backend.istioinaction.svc.cluster.local' ; date; sleep 1; echo; done

# 로드 테스트 실행 : 모두 성공!
fortio load -quiet -jitter -t 30s -c 2 -qps 2 --allow-initial-errors http://simple-web.istioinaction.io:30000
...
Sockets used: 2 (for perfect keepalive, would be 2)
Code 200 : 60 (100.0 %)
All done 60 calls (plus 2 warmup) 173.837 ms avg, 2.0 qps
...

# 엔드포인트 이상 감지 전에 3번 실패했지만, 재시도 retry 덕분에 결과적으로 모두 성공!
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend | grep outlier

# 통계 확인
kubectl exec -it deploy/simple-web -c istio-proxy -n istioinaction \
 -- curl localhost:15000/stats | grep simple-backend.istioinaction.svc.cluster.local.upstream | grep retry
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_retry: 4
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_retry_backoff_exponential: 4
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_retry_backoff_ratelimited: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_retry_limit_exceeded: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_retry_overflow: 0
cluster.outbound|80||simple-backend.istioinaction.svc.cluster.local.upstream_rq_retry_success: 4

```
- jaeger 확인: 아래처럼 재시도해서 최종적으로 사용자 입장에서는 정상 응답
![]({{ site.url }}/img/post/devops/study/istio/3/20250427014311.png)
> 로드 테스트를 다시 실행하면 오류가 없음을 확인할 수 있다.

---
### 도전과제
- `[도전과제1]` Flagger 공식문서에 주요 기능 실습 및 정리 - [Docs](https://docs.flagger.app/)
    - Flagger 배포 전략 실습 : A/B Testing, Blue/Green Deployments , Canary with Session Affinity - [Docs](https://docs.flagger.app/usage/deployment-strategies)
        - Blue/Green Deployments - [Docs](https://docs.flagger.app/tutorials/kubernetes-blue-green)
        - Istio Canary Deployments - [Docs](https://docs.flagger.app/tutorials/istio-progressive-delivery)
        - Istio A/B Testing - [Docs](https://docs.flagger.app/tutorials/istio-ab-testing)
    - 무중단 배포 Zero downtime deploymentes - [Docs](https://docs.flagger.app/tutorials/zero-downtime-deployments)
- `[도전과제2]` Istio 공식문서에 Egress 내용을 실습 및 정리 - [Docs](https://istio.io/v1.17/docs/tasks/traffic-management/egress/)
    - Accessing External Services - [Docs](https://istio.io/v1.17/docs/tasks/traffic-management/egress/egress-control/)
    - Egress Gateways - [Docs](https://istio.io/v1.17/docs/tasks/traffic-management/egress/egress-gateway/)
    - Kubernetes Services for Egress Traffic - [Docs](https://istio.io/v1.17/docs/tasks/traffic-management/egress/egress-kubernetes-services/)
    - Configuring Gateway Network Topology - [Docs](https://istio.io/v1.17/docs/ops/configuration/traffic-management/network-topologies/)
- `[도전과제3]` Istio ServiceEntry 에 경계 설정 해보기 (키알리에서 확인), 그외 활용 방안들 실습 해보고 정리 - [Docs](https://istio.io/v1.17/docs/reference/config/networking/service-entry/)
- `[도전과제4]` Istio Sidecar 내용 정리와 예시실습 해보고 정리 - [Docs](https://istio.io/v1.17/docs/reference/config/networking/sidecar/) , Istio Sidecar Object를 활용한 Sidecar Proxy Endpoint 제어 - [Blog](https://ssup2.github.io/blog-software/docs/theory-analysis/istio-endpoint-control-sidecar-object/)
- `[도전과제5]` Istio 공식문서에 DestinationRule 내용을 실습 및 정리 - [Docs](https://istio.io/v1.17/docs/reference/config/networking/destination-rule/)
- `[도전과제6]` Istio 공식문서에 Envoy Filter 내용을 실습 및 정리 - [Docs](https://istio.io/v1.17/docs/reference/config/networking/envoy-filter/)
