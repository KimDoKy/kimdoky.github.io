---
layout: post
section-type: post
title: ServiceMesh - Istio - Week4
category: devops
tags: ["k8s", "istio", "servicemesh"]
---


# chap7. 관찰 가능성: 서비스의 동작 이해하기

## 관찰 가능성이란 무엇인가?

관찰 가능성(observability)은 시스템의 외부에서 수집할 수 있는 데이터(메트릭, 로그, 트레이스 등)를 바탕으로 내부 상태를 이해할 수 있는 능력이다. 제어 이론에서 유래한 개념으로, 시스템의 복잡도가 증가함에 따라 점점 더 중요해지고 있다.

마이크로서비스 구조에서는 하나의 요청이 여러 서비스에 걸쳐 처리되므로, 단순한 로그만으로는 문제를 파악하기 어렵다. 이럴 때 관찰 가능성 도구는 내부 상태를 시각화하고, 성능 병목이나 장애 원인을 빠르게 파악할 수 있도록 돕는다.
![]({{ site.url }}/img/post/devops/study/istio/4/20250503133302.png)

#### 모니터링 vs 관찰 가능성
- **모니터링**은 사전에 정의된 상태나 임계값을 기반으로 동작한다. 예: CPU 사용량 90% 초과 경고
- **관찰 가능성**은 미리 정의하지 않은 문제도 추론 가능하게 한다. 예: 사용자 A의 요청만 느려지는 경우

### 이스티오는 어떻게 관찰 가능성을 돕는가?

이스티오는 사이드카 프록시(Envoy)를 통해 모든 네트워크 트래픽을 가로채고, 이를 통해 다양한 메트릭을 자동 수집한다. 또한 트레이싱, 로깅, 시각화 도구(Grafana, Kiali, Jaeger 등)와도 손쉽게 연동된다.

Envoy는 요청별로 다음과 같은 정보들을 추적할 수 있다:
- 요청 수
- 실패율
- 지연 시간 (평균, p50, p90, p99 등)
- 요청/응답 바이트 수

또한 이스티오는 사용자가 메트릭을 커스터마이징하거나 새로운 메트릭을 추가하는 기능도 제공한다.

## 이스티오 메트릭 살펴보기
### 데이터 플레인의 메트릭
- Envoy는 커넥션, 요청, 런타임 메트릭을 다양하게 갖추고 있음
	- 이들을 사용해 서비스의 네트워크 및 통신 상태를 파악한다.
- 먼저 예제 애플리케이션 부분 집합을 배포
	- 실습을 통해 메트릭의 출처와 접근 방법을 알아보자.
	- 애플리케이션 네트워킹 관련 메트릭 수집 / 탐색 / 시각화할 수 있는 영역으로 가져와 관찰

#### 초기화 및 실습 환경 구성

```bash
# istioinaction 네임스페이스 초기화
kubectl delete -n istioinaction deploy,svc,gw,vs,dr,envoyfilter --all

# catalog 앱 기동
kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction

# webapp 앱 기동
kubectl apply -f services/webapp/kubernetes/webapp.yaml -n istioinaction

# gateway, virtualservice 설정
kubectl apply -f services/webapp/istio/webapp-catalog-gw-vs.yaml -n istioinaction

# 확인
kubectl get deploy,pod,svc,ep,gw,vs -n istioinaction

# 호출테스트
curl -s http://webapp.istioinaction.io:30000
curl -s http://webapp.istioinaction.io:30000/api/catalog | jq
curl -s http://webapp.istioinaction.io:30000/api/catalog | jq
...
```

#### 서비스외 사이드카 프록시가 유지하는 메트릭 확인

```bash
kubectl get pod -n istioinaction
docker exec -it myk8s-control-plane istioctl proxy-status

# 쿼리를 실행해 파드의 통계 확인 : 정보가 많음. 프록시가 보관하는 정보는 휠씬 더 많지만, 대부분은 기본적으로 제거됨.
kubectl exec -it deploy/catalog -c istio-proxy -n istioinaction -- curl localhost:15000/stats
kubectl exec -it deploy/webapp  -c istio-proxy -n istioinaction -- curl localhost:15000/stats
```
- 우리가 봐야 할 것은 `istio_requests_total`이다.
- 나머지 부분을 읽으면, 이것이 인그레스 게이트웨이에서 webapp 서비스로 들어오는 요청에 대한 메트릭이며, 그 요청이 총 2개임을 알 수 있다.
- 각 프록시가 인바운드/아웃바운드 호출에 유지하는 표준 이스티오 메트릭
	- `istio_requests_total`: 요청 횟수
	- `istio_requests_duration`: 요청 처리 시간 분포
	- `istio_requests_duration_milliseconds`
	- `istio_request_bytes`: 요청 바이트 수
	- `istio_response_bytes`: 응답 바이트 수

#### CRUL을 사용하지 않고 envoy 관리자 엔드포인트 쿼리하기
```
# 보안상의 이유로 이스티오는 pilot-agent를 실행할 수 있는 최소한의 종속성만 포함하는 distroless 이미지 집합을 제공한다.
# 당연히 curl을 포함되지 않는다.
istioctl install --set values.global.variant=distroless

# 엔드포인트를 쿼리하는 것은 envoy 프록시를 디버깅할 때 중요하므로, 엔드포인트를 쿼리할 수 있도록 최소한의 CLI를 pilot-agent에 추가한 것이다. 다음과 같이 통계를 쿼리할 수 있다.
k exec -it deploy/webapp -c istio-proxy -- pilot-agent request GET help
k exec -it deploy/webapp -c istio-proxy -- pilot-agent request GET /stats
k exec -it deploy/webapp -c istio-proxy -- pilot-agent request GET /stats/prometheus
k exec -it deploy/webapp -c istio-proxy -- pilot-agent request GET /listeners
k exec -it deploy/webapp -c istio-proxy -- pilot-agent request GET /clusters
```
#### 프록시가 엔보이 통계를 더 많이 보고하도록 설정
- 트러블슈팅시 표준 이스티오 메트릭보다 더 많은 정보가 필요한 경우가 있다.
- 애플리케이션 호출이 자신의 클라이언트 측 프록시를 거칠때, 프록시는 라우팅 결정을 내리고 업스트림 클러스터로 라우팅한다.

```bash
# 방법1.메시 전체 적용
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: control-plane
spec:
  profile: demo
  meshConfig:
    defaultConfig: # Defines the default proxy configuration for all services
      proxyStatsMatcher: # Customizes the reported metrics
        inclusionPrefixes: # Metrics matching the prefix will be reported alongside the default ones.
        - "cluster.outbound|80||catalog.istioinaction"

# 방법2. 워크로드 단위별로 적용(권장)
# cat ch7/webapp-deployment-stats-inclusion.yaml
...
  template:
    metadata:
      annotations:
        proxy.istio.io/config: |-
          proxyStatsMatcher:
            inclusionPrefixes:
            - "cluster.outbound|80||catalog.istioinaction"
      labels:
        app: webapp
```

```bash
# 호출테스트
curl -s http://webapp.istioinaction.io:30000/api/catalog | jq

# 적용 전 확인
kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15000/stats | grep catalog

# 적용
cat ch7/webapp-deployment-stats-inclusion.yaml
kubectl apply -n istioinaction -f ch7/webapp-deployment-stats-inclusion.yaml

# 호출테스트
curl -s http://webapp.istioinaction.io:30000/api/catalog | jq

# 적용 후 확인 : catalog.istioinaction 에 대한 metrics 추가
# upstream 클러스터로 향햐는 커넥션 혹은 요청 시 circuit breaking 작동 확인
kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15000/stats | grep catalog
...
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.upstream_cx_active: 1
...
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.upstream_rq_200: 1
...
```
- Envoy는 트래픽을 식별할 때 출처가 내부/외부를 구분한다.
	- 내부: 보통 메시 내부 트래픽
	- 외부: 메시 외부에서 시작하는 트래픽(Ingress Gateay로 들어온 트래픽)

```bash
# cluster_name.internal.*. 메트릭을 보면 
# 메시 내부에서 시작해 성공한 요청 개수를 확인할 수 있다.
kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15000/stats | grep catalog | grep internal
...
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.internal.upstream_rq_200: 1
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.internal.upstream_rq_2xx: 1
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.internal.upstream_rq_completed: 1

# cluster_name.ssl.* 메트릭
# 트래픽인 TLS로 업스트림 클러스터로 이동하는지 여부와 커넥션과 관련된 기타 세부정보(cipher, curve 등)을 알아낼 수 이따.
# 메시 내부에서 시작해 성공한 요청 개수를 확인할 수 있다.
kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15000/stats | grep catalog | grep ssl
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.ssl.ciphers.TLS_AES_128_GCM_SHA256: 1
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.ssl.connection_error: 0
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.ssl.curves.X25519: 1
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.ssl.fail_verify_cert_hash: 0
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.ssl.fail_verify_error: 0
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.ssl.fail_verify_no_cert: 0
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.ssl.fail_verify_san: 0
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.ssl.handshake: 1
...

# upstream_cx, upstream_rq는 네트워크에서 일어나는 일에 대한 좀 더 정확한 정보 제공
kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15000/stats | grep catalog | egrep 'local.upstream_cx|local.upstream_rq'
...
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.upstream_cx_active: 1
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.upstream_cx_close_notify: 0
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.upstream_cx_connect_attempts_exceeded: 0
...
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.upstream_rq_timeout: 0
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.upstream_rq_total: 1
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.upstream_rq_tx_reset: 0

# 기타 업스트림 클러스터용 메트릭은 Envoy 문서 참고
# lb 정보
kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15000/stats | grep catalog | grep lb
...
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.lb_healthy_panic: 0
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.lb_local_cluster_not_ok: 0
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.lb_recalculate_zone_structures: 0
cluster.outbound|80||catalog.istioinaction.svc.cluster.local.lb_subsets_active: 0
...
```
- 프록시가 알고 있는 모든 백엔드 클러스터에 대한 정보와 그들의 엔드포인트 나열하는 쿼리
	- 특정 업스트림 클러스터에 대한 자세한 정보를 볼 수 있다.
		- 이 클러스터에는 어떤 엔드포인트(여긴 10.10.0.10)가 있는지,
		- 해당 엔드포인트가 속한 리전, 영역, 하위 영역은 어디인지,
		- 해당 엔드포인트에 활성 요청 또는 요류가 있는지 등의 정보가 포함된다.
	- 이전 통계는 클러스터 전체였지만, 이 통계 집합은 엔드포인트별로 자세한 정보를 볼 수 있음

```bash
kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15000/clusters kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15000/clusters | grep catalog
```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503145329.png)
- 프록시는 메트릭을 잘 수집하지만, 귀찮고 불편하다.
- 이스티오 프록시는 메트릭 수집 시스템(프로메테우스, 데이터독 등)으로 긁어 갈 수 있다.

### 컨트롤 플레인의 메트릭

컨트롤 플레인(istiod)은 인증서 관리, 프록시 설정 배포, 서비스 디스커버리 등의 기능을 담당한다. 해당 구성요소에서도 다양한 메트릭이 수집된다.

```bash
# istiod 파드에 tcp LISTEN port 정보 확인
kubectl exec -it deploy/istiod -n istio-system -- netstat -tnl
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:9876          0.0.0.0:*               LISTEN
tcp6       0      0 :::8080                 :::*                    LISTEN
tcp6       0      0 :::15012                :::*                    LISTEN
tcp6       0      0 :::15014                :::*                    LISTEN
tcp6       0      0 :::15010                :::*                    LISTEN
tcp6       0      0 :::15017                :::*                    LISTEN

# 다음 명령어를 실행해 컨트롤 플레인 메트릭을 보자
## CSR : Certificate Signing Request 인증서 발급 요청
## Citadel : Istio 보안 컴포넌트
kubectl exec -it -n istio-system deploy/istiod -n istio-system -- curl localhost:15014/metrics
...
citadel_server_root_cert_expiry_timestamp ...
citadel_server_csr_count ..
citadel_server_success_cert_issuance_count ..
# 컨트롤 플레인 버전에 대한 런타인 정보
istio_build{component="pilot",tag="1.13.0"} 1
# 설정을 데이터 플레인 프록시에 밀어넣고 동기화하는데 소요되는 시간의 분포
## 0.1초 내에 1,101개의 업데이트가 프록시에 배포됐다.
pilot_proxy_convergence_time_bucket{le="0.1"} 1101
## 요청 하나는 좀 더 걸려서 0.1~0.5초 범위에 속했다.
pilot_proxy_convergence_time_bucket{le="0.5"} 1102
...
pilot_proxy_convergence_time_sum ...
pilot_proxy_convergence_time_count ...
# 컨트롤 플레인에 알려진 서비스 개수, 사용자가 설정한 VirtualService 리소스 개수, 연결된 프록시 개수
pilot_services 14
pilot_virt_services 1
pilot_vservice_dup_domain 0
pilot_xds{version="1.13.0"} 4
# 특정 xDS API의 업데이트 횟수
pilot_xds_pushed{type="cds"} ...
pilot_xds_pushed{type="eds"} ...
pilot_xds_pushed{type="lds"} ...
pilot_xds_pushed{type="rds"} ...
pilot_xds_pushed{type="sds"} ...

# 컨트롤 플레인 버전에 대한 런타임 정보 확인 : istio 버전정보
kubectl exec -it -n istio-system deploy/istiod -n istio-system -- curl localhost:15014/metrics | grep istio_build
istio_build{component="pilot",tag="1.17.8"} 1
```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503150809.png)
```bash
# 설정을 데이터 플레인 프록시에 밀어넣고 동기화하는데 소요되는 시간의 분포를 보여준다.
kubectl exec -it -n istio-system deploy/istiod -n istio-system -- curl localhost:15014/metrics | grep convergence
```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503151301.png)
```bash
# 컨트롤 플레인에 알려진 서비스 개수, 사용자가 설정한 VirtualService 리소스 개수, 연결된 프록시 개수
kubectl exec -it -n istio-system deploy/istiod -n istio-system -- curl localhost:15014/metrics | grep pilot | egrep 'service|^pilot_xds'
```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503151744.png)
```bash
# xDS API의 업데이트 횟수
kubectl exec -it -n istio-system deploy/istiod -n istio-system -- curl localhost:15014/metrics | grep pilot_xds_pushes
```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503151905.png)
## Prometheus로 이스티오 메트릭 긁어오기
![]({{ site.url }}/img/post/devops/study/istio/4/20250424201751.png)

Envoy는 Prometheus와 호환되는 포맷으로 메트릭을 `/stats/prometheus` 경로에 노출한다. 이를 Prometheus가 수집하도록 설정하면 클러스터 전반의 메트릭을 중앙 집중화할 수 있다.

```bash
# webapp 파드 정보 확인
# istiod 파드에 tcp LISTEN port 정보 확인
kubectl exec -it deploy/webapp -n istioinaction -c istio-proxy -- netstat -tnl
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 0.0.0.0:15021           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:15021           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:15006           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:15006           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:15001           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:15001           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:15090           0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:15090           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:15004         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:15000         0.0.0.0:*               LISTEN
tcp6       0      0 :::15020                :::*                    LISTEN
tcp6       0      0 :::8080                 :::*                    LISTEN

# 앞서 살펴본 /stats 을 프로메테우스 형식으로 출력 : 서비스 프록시가 프로메테우스 메트릭을 노출하는 15090 포트로 curl 실행 확인
## /stats 는 istio-proxy 가 수집한 통계정보 출력. 디버깅/모니터링 용도. /reset_counters 로 초기화
## /stats/prometheus 는 istio-proxy 가 수집한 통계정보를 prometheus에 제공하기 위한 exporter endpoint. /reset_counters 로 초기화 할 수 없음
kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15090/stats
kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15090/stats/prometheus
...

kubectl exec -it deploy/webapp -c istio-proxy -n istioinaction -- curl localhost:15020/metrics
...
```
- 프로메테우스가 예상하는 형식으로 된 메트릭 리스트가 출력된다.
- 이스티오 프록시가 주입된 모든 애플리케이션은 자동으로 이런 프로메테우스 메트릭을 노출한다.

![]({{ site.url }}/img/post/devops/study/istio/4/20250503154613.png)

### 프로메테우스와 그라파나 설정
- kube-prometheus-stack 프로젝트
	- 부수적인 부분들을 포함해 프로메테우스의 현실적이고 고가용성인 배포 형상을 사전에 선별하고 통합하는 것
	- Prometheus Operator, Grafana, Alertmanager, NOde exporter, etc..

#### kube-prometheus-stack 설치

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

cat ch7/prom-values.yaml
...

cat << EOF > prom-values-2.yaml
prometheusOperator:
  tls:
    enabled: false
  admissionWebhooks:
    patch:
      enabled: false

prometheus:
  service:
    type: NodePort
    nodePort: 30001
    
grafana:
  service:
    type: NodePort
    nodePort: 30002
EOF

# helm 설치
kubectl create ns prometheus
helm install prom prometheus-community/kube-prometheus-stack --version 13.13.1 \
-n prometheus -f ch7/prom-values.yaml -f prom-values-2.yaml

# 확인
helm list -n prometheus
kubectl get-all -n prometheus # krew plugin
kubectl get sts,deploy,pod,svc,ep,cm,secret -n prometheus
kubectl get crd | grep monitoring
kubectl get prometheus,servicemonitors -n prometheus

# Prometheus 접속 : Service Discovery, Target 확인
kubectl patch svc -n prometheus service/prom-kube-prometheus-stack-prometheus -p '{"spec": {"type": "NodePort", "ports": [{"port": 9090, "targetPort": 9090, "nodePort": 30001}]}}'
open http://127.0.0.1:30001

# 
kubectl get servicemonitors -n prometheus
NAME                                                 AGE
prom-kube-prometheus-stack-grafana                   12m
prom-kube-prometheus-stack-kube-controller-manager   12m
prom-kube-prometheus-stack-operator                  12m
prom-kube-prometheus-stack-prometheus                12m


# (참고) 프로메테우스 버전 확인
kubectl exec -it sts/prometheus-prom-kube-prometheus-stack-prometheus -n prometheus -c prometheus -- prometheus --version
prometheus, version 2.24.0 (branch: HEAD, revision: 02e92236a8bad3503ff5eec3e04ac205a3b8e4fe)
...

# Grafana 접속 : admin / prom-operator
open http://127.0.0.1:30002
```

```bash
# 참고) kube-controller-manager 메트릭 수집 설정
# https://stackoverflow.com/questions/65901186/kube-prometheus-stack-issue-scraping-metrics
docker exec -it myk8s-control-plane curl -s https://172.18.0.2:10257/metrics -k
kubectl edit svc -n kube-system prom-kube-prometheus-stack-kube-controller-manager # 10252 -> 10257로 포트 변경
...
  ports:
  - name: http-metrics
    port: 10257
    protocol: TCP
    targetPort: 10257
...
kubectl edit servicemonitors -n prometheus prom-kube-prometheus-stack-kube-controller-manager
...
spec:
  endpoints:
  - bearerTokenFile: /var/run/secrets/kubernetes.io/serviceaccount/token
    port: http-metrics
    scheme: https
    tlsConfig:
      caFile: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
      insecureSkipVerify: true
  jobLabel: jobLabel
  namespaceSelector:
    matchNames:
    - kube-system
  selector:
    matchLabels:
      app: kube-prometheus-stack-kube-controller-manager
      release: prom
```
- 새로 배포된 프로메테우스는 이스티오 워크로드의 메트릭을 어떻게 수집할지 모른다.
- ![]({{ site.url }}/img/post/devops/study/istio/4/20250503162017.png)

### 이스티오 컨트롤 플레인 워크로드를 긁어가도록 프로메테우스 오퍼레이터 설정
- 프로메테우스의 커스텀 리소스 `ServiceMonitor`, `PodMonitor`를 사용하여 프로메테우스가 이스티오에서 메트릭을 수집하도록 설정한다.
![](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/img/custom-metrics-elements.png?raw=true)
![](https://github.com/prometheus-operator/prometheus-operator/blob/main/Documentation/img/architecture.png?raw=true)

#### ServiceMonitor 설정
```yaml
cat ch7/service-monitor-cp.yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: istio-component-monitor
  namespace: prometheus
  labels:
    monitoring: istio-components
    release: prom
spec:
  jobLabel: istio
  targetLabels: [app]
  selector:
    matchExpressions:
    - {key: istio, operator: In, values: [pilot]}
  namespaceSelector:
    any: true
  endpoints:
  - port: http-monitoring
    interval: 15s
```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503161514.png)
```bash
#  istiod의 Service Spec ServiceMonitor 에서 selector 에 istio=pilot 매칭 확인
kubectl describe svc istiod -n istio-system
Name:                     istiod
Labels:                   app=istiod
                          ...
                          istio=pilot
...
Port:                     http-monitoring  15014/TCP
TargetPort:               15014/TCP
Endpoints:                10.10.0.7:15014
...

kubectl get pod -n istio-system -l istio=pilot              
NAME                      READY   STATUS    RESTARTS   AGE
istiod-7df6ffc78d-hfv8m   1/1     Running   0          104m

# ServiceMonitor 적용
kubectl apply -f ch7/service-monitor-cp.yaml -n prometheus

# 확인
kubectl get servicemonitor -n prometheus
NAME                                                 AGE
istio-component-monitor                              7s
prom-kube-prometheus-stack-grafana                   25m
prom-kube-prometheus-stack-kube-controller-manager   25m
prom-kube-prometheus-stack-operator                  25m
prom-kube-prometheus-stack-prometheus                25m

kubectl get svc,ep istiod -n istio-system
kubectl exec -it netshoot -- curl -s istiod.istio-system:15014/metrics
kubectl exec -it netshoot -- curl -s istiod.istio-system:15014/metrics | grep pilot_xds
kubectl exec -it netshoot -- curl -s istiod.istio-system:15014/metrics | grep citadel

```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503162116.png)
![]({{ site.url }}/img/post/devops/study/istio/4/20250503162147.png)
####  PodMonitor 설정
```bash
kubectl describe pod -n istioinaction
...
Annotations:      ...
                  prometheus.io/path: /stats/prometheus
                  prometheus.io/port: 15020
                  prometheus.io/scrape: true

cat ch7/pod-monitor-dp.yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: envoy-stats-monitor
  namespace: prometheus
  labels:
    monitoring: istio-proxies
    release: prom
spec:
  selector:
    matchExpressions:
    - {key: istio-prometheus-ignore, operator: DoesNotExist}
  namespaceSelector:
    any: true
  jobLabel: envoy-stats
  podMetricsEndpoints:
  - path: /stats/prometheus
    interval: 15s
    relabelings:
    - action: keep
      sourceLabels: [__meta_kubernetes_pod_container_name]
      regex: "istio-proxy"
    - action: keep
      sourceLabels: [__meta_kubernetes_pod_annotationpresent_prometheus_io_scrape]
    - sourceLabels: [
    __address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
      action: replace
      regex: ([^:]+)(?::\d+)?;(\d+)
      replacement: $1:$2
      targetLabel: __address__
    - action: labeldrop
      regex: "__meta_kubernetes_pod_label_(.+)"
    - sourceLabels: [__meta_kubernetes_namespace]
      action: replace
      targetLabel: namespace
    - sourceLabels: [__meta_kubernetes_pod_name]
      action: replace
      targetLabel: pod_name

# PodMonitor 설정 적용
kubectl apply -f ch7/pod-monitor-dp.yaml -n prometheus

kubectl get podmonitor -n prometheus
NAME                  AGE
envoy-stats-monitor   6s

# metric 확인을 위해서 호출테스트
for in in {1..10}; do curl -s http://webapp.istioinaction.io:30000/ ; sleep 0.5; done
for in in {1..10}; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; sleep 0.5; done

# 반복 접속
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

WEBAPP=$(kubectl get pod -n istioinaction -l app=webapp -o jsonpath='{.items[0].status.podIP}')
kubectl exec -it netshoot -- curl -s $WEBAPP:15020/stats/prometheus
...
kubectl exec -it netshoot -- curl -s $WEBAPP:15090/stats/prometheus
...
```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503165242.png)
![]({{ site.url }}/img/post/devops/study/istio/4/20250503165312.png)
## 이스티오 표준 메트릭 커스터마이징하기
이스티오의 기본 메트릭은 실무에 대부분 유용하지만, 상황에 따라 더 세부적인 라벨 추가나 특정 조건별 카운팅이 필요할 수 있다.
#### 이스티오의 표준 메트릭
- `istio_requests_total`
	- COUNTER. 요청이 들어올 때마다 증가
- `istio_request_duration_miliseconds`
	- DISTRIBUTION. 요청 지속 시간의 분포
- `istio_request_bytes`
	- DISTRIBUTION. 요청 바디 크기의 분포
- `istio_response_bytes`
	- DISTRIBUTION. 응답 바디 크기의 분포
- `istio_request_message_total`
	- (gRPC) COUNTER. 클라이언트에게서 메시지가 올 때마다 증가
- `istio_response_messages_total`
	- (gRPC) COUNTER. 서버가 메시지를 보낼 때마다 증가
#### 주요 개념
- 메트릭(metric)
	- 서비스 호출(inbound/outbound) 간 텔레메트리의 Counter나 Gause, Histogram, Distrubtion
	- ex. `istio_requests_total` 메트릭
		- 서비스로 향하는(inbound) 혹은 서비스에 나오는(outbound) 요청의 총 갯수
- 디멘션(dimension)
	- ex. inbound / outbound
- 속성(attribute)
	- 기본 Envoy 요청 속성
		- `request.path`: URL 중 경로 부분
		- `request.url_path`: URL 중 경로 부분. 쿼리 문자열 제외
		- `request.host`: URL 중 호스트 부분
		- `request.scheme`: URL 중 스킴 부분(ex. 'http')
		- `request.method`: 요청 메서드
		- `request.headers`: 모든 요청 헤더. 헤더 이름은 소문자로 변환
		- `request.referer`: 요청 헤더 Referer
		- `request.useragent`: 요청 헤더 User agent
		- `request.time`: 첫 번째 바이트 수신 시각
		- `request.id`: x-request-id 헤더 값에 해당하는 요청 ID
		- `request.protocol`: 요청 프로토콜
	- 다른 속성
		- 응답 속성
		- 커넥션 속성
		- 업스트림 속성
		- 메타데이터/필터 상태 속성
		- 웹어셈블리(Wasm) 속성
	- [Envoy에서 기본적으로 사용할 수 있는 속성들](https://www.envoyproxy.io/docs/envoy/latest/intro/arch_overview/advanced/attributes#request-attributes)
	- 메타데이터 교환 필터가 제공하는 이스티오 전용 속성
		- name: 파드 이름
		- namespace: 파드가 위치한 네임스페이스
		- labels: 워크로드 레이블
		- owner: 워크로드 소유자
		- workload_name: 워크로드 이름
		- platform_metadata: 접두사 키가 있는 플랫폼 메타데이터
		- istio_version: 프록시의 버전 식별자
		- mesh_id: 메시의 고유 식별자
		- cluster_id: 해당 워크로드가 속한 클러스터의 식별자
		- app_containers: 애플리케이션 컨테이너별 짧은 이름 목록
	- upstream(프록시에서 나가는) / downstream(프록시에 들어오는) 메트릭인지에 따라
		- upstream_peer / downstream_peer 접두사가 붙는다.

이스티오의 프록시에 통계를 쿼리하면, 메트릭과 디멘션의 조합마다 통계가 따로 표시된다.
(즉, 조합이 조금이라도 다르다면 따로 표시된다.)
```bash
# 메트릭에는 디멘션이 여럿일 수 있다.
# istio_requests_total의 기본 디멘션들
# TYPE istio_requests_total_counter
istio_requests_total{
  response_code="200"  # 요청 세부 사항
  reporter="destination",  # 메트릭이 누구의 관점인가?
  source_workload="istio-ingressgateway",
  ...
  source_app="istio-ingressgateway",  # 호출 주체
  ...
  destination_app="webapp",  # 호출 대상
  ...
} 6  # 호출 개수
```

### 기존 메트릭 설정하기
- 이스티오 메트릭은 이스티오 설치시 설치되는 EnvoyFileter 리소스를 사용해 stats 프록시 플러그인에서 설정한다.

```bash
k get envoyfilter -n istio-system
NAME                    AGE
stats-filter-1.13       3h22m # 스터디 실습용
stats-filter-1.14       3h22m
stats-filter-1.15       3h22m
stats-filter-1.16       3h22m
stats-filter-1.17       3h22m
tcp-stats-filter-1.13   3h22m # 현재 실습용 istiod 버전
tcp-stats-filter-1.14   3h22m
tcp-stats-filter-1.15   3h22m
tcp-stats-filter-1.16   3h22m
tcp-stats-filter-1.17   3h22m

# 이 Envoy 필터는 istio.stats 필터를 직접 구성한다.
# 이 필터는 통계 기능을 구현한 웹어셈블리 플러그인이다.
# 실제로는 Envoy 코드베이스 내에서 직접 컴파일돼 NULL 가상머신에서 실행된다.
# 웹어셈블리 가상머신에서 실행되지 않지만, 웹어셈블리 가상머신에서 실행은 14장에서 다룬다.
kubectl get envoyfilter stats-filter-1.13 -n istio-system -o yaml
...
spec:
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: SIDECAR_OUTBOUND
      listener:
        filterChain:
          filter:
            name: envoy.filters.network.http_connection_manager
            subFilter:
              name: envoy.filters.http.router
      proxy:
        proxyVersion: ^1\.13.*
    patch:
      operation: INSERT_BEFORE
      value:
        name: istio.stats # 필터 이름
        typed_config:
          '@type': type.googleapis.com/udpa.type.v1.TypedStruct
          type_url: type.googleapis.com/envoy.extensions.filters.http.wasm.v3.Wasm
          value:
            config: # 필터 설정
              configuration:
                '@type': type.googleapis.com/google.protobuf.StringValue
                value: |
                  {
                    "debug": "false",
                    "stat_prefix": "istio"
                  }
              root_id: stats_outbound
              vm_config:
                code:
                  local:
                    inline_string: envoy.wasm.stats
                runtime: envoy.wasm.runtime.null
                vm_id: stats_outbound
...
```

#### 기존 메트릭에 디멘션 추가하기
- `istio_requests_total` 메트릭에 디멘션 2개를 추가해보자.
	- 업스트림 호출에서 meshId 별로 프록시의 버전이 어떤지 확인
	- 추가되는 디멘션: `upstream_proxy_version`, `source_mesh_id`
- 기존 디멘션을 제거할 수도 있다.

```bash
cat ch7/metrics/istio-operator-new-dimensions.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: demo
  values:
    telemetry:
      v2:
        prometheus:
          configOverride:
            inboundSidecar:
              metrics:
              - name: requests_total
                dimensions: # 추가한 새 디멘션
                  upstream_proxy_version: upstream_peer.istio_version
                  source_mesh_id: node.metadata['MESH_ID']
                tags_to_remove: # 제거한 태그 목록
                - request_protocol
            outboundSidecar:
              metrics:
              - name: requests_total
                dimensions:
                  upstream_proxy_version: upstream_peer.istio_version
                  source_mesh_id: node.metadata['MESH_ID']
                tags_to_remove:
                - request_protocol
            gateway:
              metrics:
              - name: requests_total
                dimensions:
                  upstream_proxy_version: upstream_peer.istio_version
                  source_mesh_id: node.metadata['MESH_ID']
                tags_to_remove:
                - request_protocol

# 기존 설정 확인
kubectl get istiooperator installed-state -n istio-system -o yaml | grep -E "prometheus:|telemetry:" -A2
    telemetry:
      enabled: true
      v2:
--
        prometheus:
          enabled: true
          wasmEnabled: false

# 메트릭 확인 : request_protocol 디멘션이 메트릭에 있는지 먼저 확인 >> 아래 설정 적용 후에 확인 시 해당 디멘션 없이 출력됨.
# 프로메테우스 UI 에서도 확인 : istio_requests_total - Link
kubectl -n istioinaction exec -it deploy/webapp -c istio-proxy \
-- curl localhost:15000/stats/prometheus | grep istio_requests_total
...

# 설정 적용
docker exec -it myk8s-control-plane bash
----------------------------------------
# 파일 작성
cat << EOF > istio-operator-new-dimensions.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: demo
  values:
    telemetry:
      v2:
        prometheus:
          configOverride:
            inboundSidecar:
              metrics:
              - name: requests_total
                dimensions:
                  upstream_proxy_version: upstream_peer.istio_version
                  source_mesh_id: node.metadata['MESH_ID']
                tags_to_remove:
                - request_protocol
            outboundSidecar:
              metrics:
              - name: requests_total
                dimensions:
                  upstream_proxy_version: upstream_peer.istio_version
                  source_mesh_id: node.metadata['MESH_ID']
                tags_to_remove:
                - request_protocol
            gateway:
              metrics:
              - name: requests_total
                dimensions:
                  upstream_proxy_version: upstream_peer.istio_version
                  source_mesh_id: node.metadata['MESH_ID']
                tags_to_remove:
                - request_protocol
EOF

istioctl verify-install -f istio-operator-new-dimensions.yaml # 리소스별로 적용결과를 출력
istioctl install -f istio-operator-new-dimensions.yaml -y

exit
----------------------------------------

# 변경 설정 확인
kubectl get istiooperator -n istio-system installed-state -o yaml | grep -E "prometheus:" -A9
        prometheus:
          configOverride:
            gateway:
              metrics:
              - dimensions:
                  source_mesh_id: node.metadata['MESH_ID']
                  upstream_proxy_version: upstream_peer.istio_version
                name: requests_total
                tags_to_remove:
                - request_protocol
                
# envoyfilter "stats-filter-{stat-postfix}"도 업데이트 확인
kubectl get envoyfilter stats-filter-1.13 -n istio-system -o yaml
...
spec:
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: SIDECAR_OUTBOUND
      listener:
        filterChain:
          filter:
            name: envoy.filters.network.http_connection_manager
            subFilter:
              name: envoy.filters.http.router
      proxy:
        proxyVersion: ^1\.13.*
    patch:
      operation: INSERT_BEFORE
      value:
        name: istio.stats
        typed_config:
          '@type': type.googleapis.com/udpa.type.v1.TypedStruct
          type_url: type.googleapis.com/envoy.extensions.filters.http.wasm.v3.Wasm
          value:
            config:
              configuration:
                '@type': type.googleapis.com/google.protobuf.StringValue
                value: |
                  {"metrics":[{"dimensions":{"source_mesh_id":"node.metadata['MESH_ID']","upstream_proxy_version":"upstream_peer.istio_version"},"name":"requests_total","tags_to_remove":["request_protocol"]}]}
              root_id: stats_outbound
              vm_config:
                code:
                  local:
                    inline_string: envoy.wasm.stats
                runtime: envoy.wasm.runtime.null
                vm_id: stats_outbound
...

# 나머지 버전에서도 업데이트 반영되었는지 확인해보자.
kubectl get envoyfilter stats-filter-1.14 -n istio-system -o yaml | grep MESH_ID
kubectl get envoyfilter stats-filter-1.15 -n istio-system -o yaml | grep MESH_ID
kubectl get envoyfilter stats-filter-1.16 -n istio-system -o yaml | grep MESH_ID
kubectl get envoyfilter stats-filter-1.17 -n istio-system -o yaml | grep MESH_ID
...

# 메트릭에서 이 디멘션을 확인 전에 이스티오 프록시가 이 디멘션을 알게 해야 한다.
# 디플로이먼트 파드 spec에 sidecar.istio.io/extraStatTags 애노테이션을 추가해야 한다.
# 디플로이먼트 메타데이터가 아니다!!
# istio 1.17+부터 custom demension 설정에서 extraStatTags에 애노테이션을 설정 안해도 된다.
#
#  cat ch7/metrics/webapp-deployment-extrastats.yaml
#  apiVersion: apps/v1
#  kind: Deployment
#  ...
#  spec:
#    replicas: 1
#    selector:
#      matchLabels:
#        app: webapp
#    ...

# kubectl apply -n istioinaction -f ch7/metrics/webapp-deployment-extrastats.yaml

# metric 확인을 위해서 호출테스트
for in in {1..10}; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; sleep 0.5; done
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

# 메트릭 확인
# 새로 추가한 2개의 디멘션이 각 메트릭 끝에 추가되어 있다.
kubectl -n istioinaction exec -it deploy/webapp -c istio-proxy \
-- curl localhost:15000/stats/prometheus | grep istio_requests_total
istio_requests_total{
...
source_mesh_id="cluster.local",upstream_proxy_version="unknown"} 52

istio_requests_total{
...
source_mesh_id="cluster.local",upstream_proxy_version="1.17.8"} 52
```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503182429.png)
```bash
# (참고) 새로운 텔레메트리 API 사용하기
cat ch7/metrics/v2/add-dimensions-telemetry.yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: add-dimension-tags
  namespace: istioinaction
spec:
  metrics:
  - providers:
      - name: prometheus
    overrides:
      - match:
          metric: REQUEST_COUNT
          mode: CLIENT_AND_SERVER
        disabled: false
        tagOverrides:
          upstream_proxy_version:
            operation: UPSERT
            value: upstream_peer.istio_version
          source_mesh_id:
            operation: UPSERT
            value: node.metadata['MESH_ID']
          request_protocol:
            operation: REMOVE

kubectl apply -n istioinaction -f ch7/metrics/v2/add-dimensions-telemetry.yaml
```

### 새로운 메트릭 만들기
- stats 플러그인으로 새 메트릭을 만들 수 있다.

```bash
# istio_get_calls 메트릭 추가
# istio_ 는 자동으로 추가되는 접두사이다.
# COUNTER / GAUGE / HISTOGRAM 중 선택(여기는 COUNTER)
# 메트릭 값은 CEL(Common Expression Language) 표현식을 따른다.
## COUNTER -> Int
# HTTP GET 요청 갯수를 센다.
cat ch7/metrics/istio-operator-new-metric.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: demo
  values:
    telemetry:
      v2:
        prometheus:
          configOverride:
            inboundSidecar:
              definitions:
              - name: get_calls
                type: COUNTER
                value: "(request.method.startsWith('GET') ? 1 : 0)"
            outboundSidecar:
              definitions:
              - name: get_calls
                type: COUNTER
                value: "(request.method.startsWith('GET') ? 1 : 0)"
            gateway:
              definitions:
              - name: get_calls
                type: COUNTER
                value: "(request.method.startsWith('GET') ? 1 : 0)"

# 설정 적용
docker exec -it myk8s-control-plane bash
----------------------------------------
cat << EOF > istio-operator-new-metric.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: demo
  values:
    telemetry:
      v2:
        prometheus:
          configOverride:
            inboundSidecar:
              definitions:
              - name: get_calls
                type: COUNTER
                value: "(request.method.startsWith('GET') ? 1 : 0)"
            outboundSidecar:
              definitions:
              - name: get_calls
                type: COUNTER
                value: "(request.method.startsWith('GET') ? 1 : 0)"
            gateway:
              definitions:
              - name: get_calls
                type: COUNTER
                value: "(request.method.startsWith('GET') ? 1 : 0)"
EOF

istioctl verify-install -f istio-operator-new-metric.yaml # 리소스별로 적용결과를 출력
istioctl install -f istio-operator-new-metric.yaml -y

exit
----------------------------------------

# 확인
kubectl get istiooperator -n istio-system installed-state -o yaml  | grep -A2 get_calls$
              - name: get_calls
                type: COUNTER
                value: '(request.method.startsWith(''GET'') ? 1 : 0)''
...

kubectl get envoyfilter -n istio-system stats-filter-1.13 -o yaml | grep get_calls
...
{"definitions":[{"name":"get_calls","type":"COUNTER","value":"(request.method.startsWith('GET') ? 1 : 0)"}]}
...
```
- 새 메트릭을 만들면 프록시에 노출하기 위헤 이스티오에 알려야한다.
	- 1.17+부터는 안해도 됨

```bash
# webapp 디플로이먼트의 파드 사양에 애너테이션을 추가한다
# 안해도 됨!!!
cat ch7/metrics/webapp-deployment-new-metric.yaml
...
  template:
    metadata:
      annotations:
        proxy.istio.io/config: |-
          proxyStatsMatcher:
            inclusionPrefixes:
            - "istio_get_calls"
      labels:
        app: webapp
...

kubectl -n istioinaction apply -f ch7/metrics/webapp-deployment-new-metric.yaml
```

```bash
# 확인
kubectl -n istioinaction exec -it deploy/webapp -c istio-proxy -- curl localhost:15000/stats/prometheus | grep istio_get_calls

# TYPE istio_get_calls counter
istio_get_calls{} 772
```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503183618.png)
### 새 속성으로 호출 그룹화하기
- 기존 속성을 기반으로 더 세분화 / 도메인 특화 새 속성 생성

```bash
# istio_operationId 속성 생성
# request.path.url + request.method으로 catalog/items GET API 호출 갯수 추적
# 이를 위해 attribute-gen 프록시 플러그인 사용
# attribute-gen은 stats 플러그인은 보완한다.
cat ch7/metrics/attribute-gen.yaml
apiVersion: networking.istio.io/v1alpha3
kind: EnvoyFilter
...
spec:
  ...
                  {
                    "attributes": [
                      {
                        "output_attribute": "istio_operationId", # 속성 이름
                        "match": [
                         {
                           "value": "getitems", # 속성 값
                           "condition": "request.url_path == '/items' && request.method == 'GET'"
                         },
                         {
                           "value": "createitem",
                           "condition": "request.url_path == '/items' && request.method == 'POST'"
                         },     
                         {
                           "value": "deleteitem",
                           "condition": "request.url_path == '/items' && request.method == 'DELETE'"
                         }                                             
                       ]
                      }
                    ]
                  }
              ...

docker exec -it myk8s-control-plane istioctl version
client version: 1.17.8
control plane version: 1.17.8
data plane version: 1.17.8 (4 proxies)

vi ch7/metrics/attribute-gen.yaml
...
      proxy:
        proxyVersion: ^1\.17.* # 수정
...

# 버전을 수정 후 envoyfilter 를 배포합니다. envoyfilter를 배포한 네임스페이스의 istio-proxy들에 적용 됩니다
kubectl apply -f ch7/metrics/attribute-gen.yaml -n istioinaction

# 확인
kubectl get envoyfilter -n istioinaction -o yaml | kubectl neat
kubectl get envoyfilter -n istioinaction
NAME                    AGE
attribute-gen-example   12s

# catalog에 대한 API 호출을 식별하기 위해
# istio_requests_total 메트릭에 upstream_operation 디멘션을 추가한다.
cat ch7/metrics/istio-operator-new-attribute.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: demo
  values:
    telemetry:
      v2:
        prometheus:
          configOverride:
            outboundSidecar:
              metrics:
              - name: requests_total
                dimensions:
                  upstream_operation: istio_operationId # 새 디멘션
# 설정 적용
docker exec -it myk8s-control-plane bash
----------------------------------------
cat << EOF > istio-operator-new-attribute.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
spec:
  profile: demo
  values:
    telemetry:
      v2:
        prometheus:
          configOverride:
            outboundSidecar:
              metrics:
              - name: requests_total
                dimensions:
                  upstream_operation: istio_operationId # 새 디멘션
EOF
istioctl verify-install -f istio-operator-new-attribute.yaml # 리소스별로 적용결과를 출력
istioctl install -f istio-operator-new-attribute.yaml -y

exit
----------------------------------------

# 확인 : outboundSidecar 에만 적용됨
kubectl get istiooperator -n istio-system installed-state -o yaml | grep -B2 -A1 istio_operationId$
              metrics:
              - dimensions:
                  upstream_operation: istio_operationId
                name: requests_total

kubectl get envoyfilter -n istio-system stats-filter-1.17 -o yaml | kubectl neat
...
spec:
  configPatches:
  - applyTo: HTTP_FILTER
    match:
      context: SIDECAR_OUTBOUND
      listener:
        filterChain:
          filter:
            name: envoy.filters.network.http_connection_manager
            subFilter:
              name: envoy.filters.http.router
      proxy:
        proxyVersion: ^1\.17.*
    patch:
      operation: INSERT_BEFORE
      value:
        name: istio.stats
        typed_config:
          '@type': type.googleapis.com/udpa.type.v1.TypedStruct
          type_url: type.googleapis.com/stats.PluginConfig
          value:
            metrics:
            - dimensions:
                upstream_operation: istio_operationId
              name: requests_total
...

kubectl get envoyfilter -n istio-system stats-filter-1.16 -o yaml | grep istio_operationId -B15 -A5
kubectl get envoyfilter -n istio-system stats-filter-1.15 -o yaml | grep istio_operationId -B15 -A5
kubectl get envoyfilter -n istio-system stats-filter-1.14 -o yaml | grep istio_operationId -B15 -A5
kubectl get envoyfilter -n istio-system stats-filter-1.13 -o yaml | grep istio_operationId -B15 -A5
...

# (이제 안해도 됨) 새 디멘션을 추가시 extraStats 애노테이션 추가
# kubectl apply -f ch7/metrics/webapp-deployment-extrastats-new-attr.yaml

# 메트릭 확인 : dimension (upstream_operation) 추가 확인!
kubectl -n istioinaction exec -it deploy/webapp -c istio-proxy -- curl localhost:15000/stats/prometheus | grep istio_requests_total

# TYPE istio_requests_total counter
istio_requests_total{
...
upstream_operation="getitems"} 542
```
- 프로메테우스 UI: `istio_requests_total{upstream_+operation!=""}`
![]({{ site.url }}/img/post/devops/study/istio/4/20250503195211.png)
- 애플리케이션 간 네트워크를 통한 통신이 늘어날 수록 문제 발생 가능성은 높아진다.
- MSA를 운영시 누가 무슨 언어로 애플리케이션을 만든 것과 상관없이 한결같은 시야를 갖아야 한다.
- 이스티오는 서비스 간 메트릭 수집을 더 쉽게 만들어 준다.
	- 개발자아 애플리케이션에 명시적으로 코딩하지 않아도
	- 성공률, 실패율, 재시도 횟수, 지연 시간 등은 관찰한다.
- 이스티오는 황금 신호 메트릭(지연시간, 처리량, 오류, 포화도) 수집을 간편하게 만들 뿐이다.

---

# chap8. 관찰 가능성: 그라파나, 예거, 키알리로 네트워크 동작 시각화하기
Grafana와 Kiali 같응 도구로 메트릭들을 시각화한다.
분산 트레이싱 도구(Jaeger)를 사용해 네트워크 호출 그래프도 시각화한다.

## 그라파나를 사용해 이스티오 서비스와 컨트롤 플레인 메트릭 시각화하기
```bash
# Grafana 접속 : admin / prom-operator
open http://127.0.0.1:30002
open http://127.0.0.1:30002/dashboards

# login in
# username: admin
# password: prom-operator

# 반복 호출 해두기
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

```
### **이스티오의 그라파나 대시보드 설정하기**
```bash
cd ch8

# 대시보드 JSON 소스가 포함된 cm이 생성
# 그라파나로 가져 올 수 있다.
kubectl -n prometheus create cm istio-dashboards \
--from-file=pilot-dashboard.json=dashboards/\
pilot-dashboard.json \
--from-file=istio-workload-dashboard.json=dashboards/\
istio-workload-dashboard.json \
--from-file=istio-service-dashboard.json=dashboards/\
istio-service-dashboard.json \
--from-file=istio-performance-dashboard.json=dashboards/\
istio-performance-dashboard.json \
--from-file=istio-mesh-dashboard.json=dashboards/\
istio-mesh-dashboard.json \
--from-file=istio-extension-dashboard.json=dashboards/\
istio-extension-dashboard.json

# 확인
cd ..
kubectl describe cm -n prometheus  istio-dashboards

# Grafana (오퍼레이터)가 configmap(istio-dashboards)을 마운트(인식) 하도록 레이블 지정
kubectl label -n prometheus cm istio-dashboards grafana_dashboard=1

# (참고) Grafana 대시보드 추가
kubectl stern -n prometheus prom-grafana
prom-grafana-d7f5cb646-555zp grafana-sc-dashboard [2025-04-27 05:58:21] File in configmap istio-extension-dashboard.json ADDED
prom-grafana-d7f5cb646-555zp grafana-sc-dashboard [2025-04-27 05:58:21] File in configmap istio-mesh-dashboard.json ADDED
prom-grafana-d7f5cb646-555zp grafana-sc-dashboard [2025-04-27 05:58:21] File in configmap istio-performance-dashboard.json ADDED
prom-grafana-d7f5cb646-555zp grafana-sc-dashboard [2025-04-27 05:58:21] File in configmap istio-service-dashboard.json ADDED
prom-grafana-d7f5cb646-555zp grafana-sc-dashboard [2025-04-27 05:58:21] File in configmap istio-workload-dashboard.json ADDED
prom-grafana-d7f5cb646-555zp grafana-sc-dashboard [2025-04-27 05:58:21] File in configmap pilot-dashboard.json ADDED
...
```
![]({{ site.url }}/img/post/devops/study/istio/4/20250503202653.png)

### 컨트롤 플레인 메트릭 보기
- Grafana Dashboard -> Istio Control Plane Dashboard

![]({{ site.url }}/img/post/devops/study/istio/4/20250503203746.png)
![]({{ site.url }}/img/post/devops/study/istio/4/20250503211742.png)
![]({{ site.url }}/img/post/devops/study/istio/4/20250503211840.png)

- 해당 쿼리를 프로메테우스에서 확인: `pilot_xds_pushes`

![]({{ site.url }}/img/post/devops/study/istio/4/20250503203421.png)

### 데이터 플레인 메트릭 보기
- Grafana Dashboard -> Istio Service Dashboard

![]({{ site.url }}/img/post/devops/study/istio/4/20250503212216.png)
- 이 그래프들은 이스티오 표준 메트릭으로 채워지며, 이를 변경하고 조정하거나 다른 메트릭의 새 그래프를 추가할 수 있다.
- 커스텀 메트릭이나 특정 엔보이 메트릭 활성화는 7장을 참조하자.

## 분산 트레이싱
- 더 많은 애플리케이션을 MSA로 구축할수록, 비즈니스 목표를 달성하기 위해 협업하는 분산 구성 요소의 네트워크를 만들어간다.
- 요청 경로에 문제 발생시, 무슨 일이 일어나고 있는지 이해해야한다.
- 앞에서 이스티오가 네트워크 관련 메트릭, 텔레메트리를 수집하는 것을 다뤘다.
- 이제 분산 트레이싱이라는 개념을 살려보고, MSA 망을 통과시 오동작하는 요청을 진단하는 걸 다룬다.

![]({{ site.url }}/img/post/devops/study/istio/4/20250428212329.png)
- 모놀리스는 친숙한 도구로 디버깅한다.
	- 디버거, 런타임 프로파일러, 메모리 분석 도구 등
- 분산 구조 애플리케이션은 새로운 도구가 필요하다.
- 분산 트레이싱은 요청에 주석을 붙이는 작업을 포함한다.
- 주석 
	- 상관관계 ID: 서비스 간 호출을 나타냄
	- trace ID: 서비스 간 호출 그래프를 거치는 측정 요청을 나타냄
- 이스티오의 데이터 플레인은 요청이 데이터 플레인을 통과할 때 이런 메타데이터(주석)을 요청에 추가할 수 있다.
	- 인식할 수 없거나 외부 개체에서 온 메타데이터는 제거한다.
- OpenTelemetry: 분산 트레이싱과 관련된 개념 및 API를 정의하는 사양
	- 오픈트레이싱을 포함한다.
- 오픈트레이싱은 어느 정도 개발자에게 의존한다.
	- 애플리케이션에서 요청을 처리하고 다른 시스템으로 새로운 요청을 보낼때 요청에 주석을 붙이는 작업을 한다.
- 트레이싱 엔진: 요청 흐름의 전체 상황을 파악하는데 도움을 줌
	- 아키텍처에서 오동작하는 영역 식별에 유용함

-> 이스티오를 사용하면 개발자의 부담이 줄어들며, 분산 트레이싱을 서비스 메시 일부로 제공할 수 있다.

### 분산 트레이싱은 어떻게 동작하는가?

- OpenTracing을 활용한 분산 트레이싱
	- 애플리케이션이 Span을 생성
	- 이를 오픈트레이싱 엔진과 공유
	- 뒤이어 호출하는 서비스로 Trace Context를 전파
- Upstream 서비스도 동일한 작업을 수행함
	- 요청 중 자신이 처리하는 부분을 나타내는 Span을 생성
	- 이를 오픈트레이싱 엔진에 전달
	- TraceContext를 다시 다른 서비스로 전파
- **Span**: 서비스 내부의 작업 단위. 시작시간, 종료시간, 태그, 로그 등을 포함
	- SpanID
	- TraceID
	- 이 ID들은 서비스 간의 상관관계를 파악하는데 사용.
	- 서비스 간에 전파돼야 한다.
- **Trace**: 여러 span으로 구성된 전체 요청 흐름

![]({{ site.url }}/img/post/devops/study/istio/4/20250503214433.png)

- OpenTracing 구현체의 시스템들
	- Jaeger
	- Zipkin
	- Lightstep
	- Instana

- 이스티오는 Span을 분산 트레이싱 엔진으로 보낼수 있어서, 이를 위해 추가 설정이 필요 없다.
- 요청이 이스티오 서비스 프록시를 통과시, 진행 중인 Trace가 없으면 Trace를 새로 시작
	- 이때 요청의 시작/종료 시각을 Span의 일부로 기록함
- 이스티오는 일반적으로 Zipkin Tracing Header라고 하는 HTTP 헤더를 요청에 더한다.
	- 이스티오는 후속 Span을 전체 Trace에 연관짓는데 사용
- 요청이 서비스로 들어오면 이스티오 프록시가 분산 트레이싱 헤더를 인식하면
	- 프록시는 Trace가 진행 중인 것으로 인식하여 Trace를 새로 만들지 않는다.

- 이스티오와 분산 트레이싱 기능에서 사용하는 Zipkin Tracing header
	- x-request-id
	- x-b3-traceid
	- x-b3-spanid
	- x-b3-parentspanid
	- x-b3-sampled
	- x-b3-flags
	- x-ot-span-context

- 이스티오가 제공하는 분산 트레이싱 기능이 요청 호출 그래프 전체에 걸쳐 작동하려면,
	- 각 애플리케이션이 이 헤더들이 자신이 하는 모든 호출에 전파해야 한다.

![]({{ site.url }}/img/post/devops/study/istio/4/20250428215309.png)

### 분산 트레이싱 시스템 설치하기
- Jaeger는 대표적인 오픈소스 분산 트레이싱 시스템이다.
- all-in-one 배포 파일은 Zipkin과 호환되는 서비스를 포함하며, 별도 설정 없이 이스티오와 바로 연동된다.
- 운영 환경 배포 단계는 [Jaeger Docs](https://www.jaegertracing.io/docs/1.22/operator/#production-strategy)을 참조하자.

```bash
# myk8s-control-plane 진입 후 설치 진행
docker exec -it myk8s-control-plane bash
-----------------------------------
# 설치 파일 확인
pwd
ls istio-$ISTIOV/samples/addons
cat istio-$ISTIOV/samples/addons/jaeger.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
  namespace: istio-system
  labels:
    app: jaeger
spec:
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
        sidecar.istio.io/inject: "false"
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "14269"
    spec:
      containers:
        - name: jaeger
          image: "docker.io/jaegertracing/all-in-one:1.35"
          env:
            - name: BADGER_EPHEMERAL
              value: "false"
            - name: SPAN_STORAGE_TYPE
              value: "badger"
            - name: BADGER_DIRECTORY_VALUE
              value: "/badger/data"
            - name: BADGER_DIRECTORY_KEY
              value: "/badger/key"
            - name: COLLECTOR_ZIPKIN_HOST_PORT
              value: ":9411"
            - name: MEMORY_MAX_TRACES
              value: "50000"
            - name: QUERY_BASE_PATH
              value: /jaeger
          livenessProbe:
            httpGet:
              path: /
              port: 14269
          readinessProbe:
            httpGet:
              path: /
              port: 14269
          volumeMounts:
            - name: data
              mountPath: /badger
          resources:
            requests:
              cpu: 10m
      volumes:
        - name: data
          emptyDir: {}
---
apiVersion: v1
kind: Service
metadata:
  name: tracing
  namespace: istio-system
  labels:
    app: jaeger
spec:
  type: ClusterIP
  ports:
    - name: http-query
      port: 80
      protocol: TCP
      targetPort: 16686
    # Note: Change port name if you add '--query.grpc.tls.enabled=true'
    - name: grpc-query
      port: 16685
      protocol: TCP
      targetPort: 16685
  selector:
    app: jaeger
---
# Jaeger implements the Zipkin API. To support swapping out the tracing backend, we use a Service named Zipkin.
apiVersion: v1
kind: Service
metadata:
  labels:
    name: zipkin
  name: zipkin
  namespace: istio-system
spec:
  ports:
    - port: 9411
      targetPort: 9411
      name: http-query
  selector:
    app: jaeger
---
apiVersion: v1
kind: Service
metadata:
  name: jaeger-collector
  namespace: istio-system
  labels:
    app: jaeger
spec:
  type: ClusterIP
  ports:
  - name: jaeger-collector-http
    port: 14268
    targetPort: 14268
    protocol: TCP
  - name: jaeger-collector-grpc
    port: 14250
    targetPort: 14250
    protocol: TCP
  - port: 9411
    targetPort: 9411
    name: http-zipkin
  selector:
    app: jaeger
    
# 설치
kubectl apply -f istio-$ISTIOV/samples/addons/jaeger.yaml
deployment.apps/jaeger created
service/tracing created
service/zipkin created
service/jaeger-collector created

# 빠져나오기
exit
-----------------------------------

# 설치 확인 : 예거는 집킨 형식과 호환됨 Jaeger is compatible with the Zipkin format.
# https://www.jaegertracing.io/docs/1.22/features/#backwards-compatibility-with-zipkin
kubectl get deploy,pod,svc,ep -n istio-system

# NodePort 변경 및 nodeport tracing(30004) 변경
kubectl describe svc -n istio-system tracing
...
Port:                     http-query  80/TCP
TargetPort:               16686/TCP
NodePort:                 http-query  31345/TCP
Endpoints:                10.10.0.20:16686
...

kubectl patch svc -n istio-system tracing -p '{"spec": {"type": "NodePort", "ports": [{"port": 80, "targetPort": 16686, "nodePort": 30004}]}}'

# tracing 접속 : 예거 트레이싱 대시보드
open http://127.0.0.1:30004
```

### **분산 트레이싱을 수행하도록 이스티오 설정하기**
- 이스티오에서 분산 트레이싱의 수준
	- 메시 전체
	- 네임스페이스
	- 특정 워크로드

#### **설치 시 트레이싱 설정하기**
- 이스티오 설치 시 IstioOperator 파일을 통해 트레이싱 백엔드(zipkin, datadog, stackdriver 등)를 지정할 수 있다.

##### 방법 1
- 이스티오 설치시 IstioOperator 리소스를 사용하는 샘플 설정으로, 다양한 분산 트레이싱 백엔드를 설정

```bash
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
spec:
  meshConfig:
    defaultConfig:
      tracing:
        lightstep: {}
        zipkin: {}
        datadog: {}
        stackdriver: {}

# Jaeger(Zipkin 호환형)를 사용하려 한다면..(현재 실습)
cat ch8/install-istio-tracing-zipkin.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
spec:
  meshConfig:
    defaultConfig:
      tracing:
        sampling: 100
        zipkin:
          address: zipkin.istio-system:9411

# 기존 설정 확인
kubectl get IstioOperator -n istio-system installed-state -o json        
kubectl describe cm -n istio-system istio
...
defaultConfig:
  discoveryAddress: istiod.istio-system.svc:15012
  proxyMetadata: {}
  tracing:
    zipkin:
      address: zipkin.istio-system:9411
...

# 적용
docker exec -it myk8s-control-plane bash
-----------------------------------
cat << EOF > install-istio-tracing-zipkin.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
spec:
  meshConfig:
    defaultConfig:
      tracing:
        sampling: 100
        zipkin:
          address: zipkin.istio-system:9411
EOF

istioctl install -y -f install-istio-tracing-zipkin.yaml

exit
-----------------------------------

# 확인
kubectl describe cm -n istio-system istio
...
  tracing:
    sampling: 100
    zipkin:
      address: zipkin.istio-system:9411
...
```

##### 방법 2 (실습 skip)
- istio configmap 설정 - MeshConfig를 이용한 트레이싱 설정
- 설치 후에도 istio ConfigMap을 수정하여 meshConfig.defaultConfig.tracing 설정을 바꿀 수 있다.

```bash
kubectl edit cm -n istio-system istio
...
```

##### 방법 3
- 워크로드별로 트레이싱 설정
- Pod Spec에 애노테이션 설정
- 디플로이먼트의 애노테이션을 이용해 샘플링 비율이나 트레이싱 백엔드를 오버라이드할 수 있다.

```bash
apiVersion: apps/v1
kind: Deployment
...
spec:
  template:
    metadata:
      annotations:
        proxy.istio.io/config: |
          tracing:
            zipkin:
              address: zipkin.istio-system:9411
...
```

#### 기본 트레이싱 헤더 살펴보기
- 이 시점. 트레이스를 올바른 위치에 보내도록 분산 트레이싱 엔진과 이스티로를 설정함
- 이스티오가 생성하는 트레이싱용 Zipkim 헤더가 우리가 예상대로인지 확인
- 이스티오 Ingress Gateway를 사용해 외부 httpbin 서비스를 호출
	- 요청 헤더를 표시하는 엔드포인트를 호출
	- 이스티오가 오픈트레이싱 헤더와 상관관계 ID를 자동으로 주입하는 것을 확인

```bash
cat ch8/tracing/thin-httpbin-virtualservice.yaml
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
    - "httpbin.istioinaction.io"
---
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: thin-httbin-virtualservice
spec:
  hosts:
  - "httpbin.istioinaction.io"
  gateways:
  - coolstore-gateway
  http:
  - route:
    - destination:
        host: httpbin.org
---        
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: external-httpbin-org
spec:
  hosts:
  - httpbin.org 
  ports:
  - number: 80
    name: http
    protocol: HTTP
  location: MESH_EXTERNAL
  resolution: DNS

kubectl apply -n istioinaction -f ch8/tracing/thin-httpbin-virtualservice.yaml

# 확인
kubectl get gw,vs,serviceentry -n istioinaction

# 도메인 질의를 위한 임시 설정 : 실습 완료 후에는 삭제 해둘 것
echo "127.0.0.1       httpbin.istioinaction.io" | sudo tee -a /etc/hosts
cat /etc/hosts | tail -n 5

# 호스트에서 호출 시, 어떻게 외부 서비스로 전달되는지 살펴봄
# 원래 요청에서 사용된 헤더를 반환해야 한다.
# client(curl) -> istio-ingress-gateway -> httpbin.org(external)
curl -s http://httpbin.istioinaction.io:30000/headers | jq
{
  "headers": {
    "Accept": "*/*",
    "Host": "httpbin.istioinaction.io",
    "User-Agent": "curl/8.7.1",
    "X-Amzn-Trace-Id": "Root=1-681615f8-40260de76d2ff11408c091c5",
    "X-B3-Sampled": "1",
    "X-B3-Spanid": "eb103242cc602d9c",
    "X-B3-Traceid": "802206a791da8fb4eb103242cc602d9c",
    "X-Envoy-Attempt-Count": "1",
    "X-Envoy-Decorator-Operation": "httpbin.org:80/*",
    "X-Envoy-Internal": "true",
    "X-Envoy-Peer-Metadata": "ChQKDkFQUF9DT05UQUlORVJTEgIaAAoaCgpDTFVTVEVSX0lEEgwaCkt1YmVybmV0ZXMKHAoMSU5TVEFOQ0VfSVBTEgwaCjEwLjEwLjAuMjMKGQoNSVNUSU9fVkVSU0lPThIIGgYxLjE3LjgKnAMKBkxBQkVMUxKRAyqOAwodCgNhcHASFhoUaXN0aW8taW5ncmVzc2dhdGV3YXkKEwoFY2hhcnQSChoIZ2F0ZXdheXMKFAoIaGVyaXRhZ2USCBoGVGlsbGVyCjYKKWluc3RhbGwub3BlcmF0b3IuaXN0aW8uaW8vb3duaW5nLXJlc291cmNlEgkaB3Vua25vd24KGQoFaXN0aW8SEBoOaW5ncmVzc2dhdGV3YXkKGQoMaXN0aW8uaW8vcmV2EgkaB2RlZmF1bHQKMAobb3BlcmF0b3IuaXN0aW8uaW8vY29tcG9uZW50EhEaD0luZ3Jlc3NHYXRld2F5cwoSCgdyZWxlYXNlEgcaBWlzdGlvCjkKH3NlcnZpY2UuaXN0aW8uaW8vY2Fub25pY2FsLW5hbWUSFhoUaXN0aW8taW5ncmVzc2dhdGV3YXkKLwojc2VydmljZS5pc3Rpby5pby9jYW5vbmljYWwtcmV2aXNpb24SCBoGbGF0ZXN0CiIKF3NpZGVjYXIuaXN0aW8uaW8vaW5qZWN0EgcaBWZhbHNlChoKB01FU0hfSUQSDxoNY2x1c3Rlci5sb2NhbAouCgROQU1FEiYaJGlzdGlvLWluZ3Jlc3NnYXRld2F5LTk5NmJjNmJiNi1scnpneAobCglOQU1FU1BBQ0USDhoMaXN0aW8tc3lzdGVtCl0KBU9XTkVSElQaUmt1YmVybmV0ZXM6Ly9hcGlzL2FwcHMvdjEvbmFtZXNwYWNlcy9pc3Rpby1zeXN0ZW0vZGVwbG95bWVudHMvaXN0aW8taW5ncmVzc2dhdGV3YXkKFwoRUExBVEZPUk1fTUVUQURBVEESAioACicKDVdPUktMT0FEX05BTUUSFhoUaXN0aW8taW5ncmVzc2dhdGV3YXk=",
    "X-Envoy-Peer-Metadata-Id": "router~10.10.0.23~istio-ingressgateway-996bc6bb6-lrzgx.istio-system~istio-system.svc.cluster.local"
  }
}

# (참고) X-Envoy-Peer-Metadata 정보 디코딩 확인
echo "ChQKDkFQUF9DT05UQUlORVJTEgIaAAoaCgpDTFVTVEVSX0lEEgwaCkt1YmVybmV0ZXMKHAoMSU5TVEFOQ0VfSVBTEgwaCjEwLjEwLjAuMjMKGQoNSVNUSU9fVkVSU0lPThIIGgYxLjE3LjgKnAMKBkxBQkVMUxKRAyqOAwodCgNhcHASFhoUaXN0aW8taW5ncmVzc2dhdGV3YXkKEwoFY2hhcnQSChoIZ2F0ZXdheXMKFAoIaGVyaXRhZ2USCBoGVGlsbGVyCjYKKWluc3RhbGwub3BlcmF0b3IuaXN0aW8uaW8vb3duaW5nLXJlc291cmNlEgkaB3Vua25vd24KGQoFaXN0aW8SEBoOaW5ncmVzc2dhdGV3YXkKGQoMaXN0aW8uaW8vcmV2EgkaB2RlZmF1bHQKMAobb3BlcmF0b3IuaXN0aW8uaW8vY29tcG9uZW50EhEaD0luZ3Jlc3NHYXRld2F5cwoSCgdyZWxlYXNlEgcaBWlzdGlvCjkKH3NlcnZpY2UuaXN0aW8uaW8vY2Fub25pY2FsLW5hbWUSFhoUaXN0aW8taW5ncmVzc2dhdGV3YXkKLwojc2VydmljZS5pc3Rpby5pby9jYW5vbmljYWwtcmV2aXNpb24SCBoGbGF0ZXN0CiIKF3NpZGVjYXIuaXN0aW8uaW8vaW5qZWN0EgcaBWZhbHNlChoKB01FU0hfSUQSDxoNY2x1c3Rlci5sb2NhbAouCgROQU1FEiYaJGlzdGlvLWluZ3Jlc3NnYXRld2F5LTk5NmJjNmJiNi1scnpneAobCglOQU1FU1BBQ0USDhoMaXN0aW8tc3lzdGVtCl0KBU9XTkVSElQaUmt1YmVybmV0ZXM6Ly9hcGlzL2FwcHMvdjEvbmFtZXNwYWNlcy9pc3Rpby1zeXN0ZW0vZGVwbG95bWVudHMvaXN0aW8taW5ncmVzc2dhdGV3YXkKFwoRUExBVEZPUk1fTUVUQURBVEESAioACicKDVdPUktMT0FEX05BTUUSFhoUaXN0aW8taW5ncmVzc2dhdGV3YXk=" | base64 -d
...
```

- 이스티오 ingress-gateway를 호출시 간단한 HTTP 테스트 서비스인 외부 URL(httpbin.org)로 라우팅되었다.
	- 이 서비스의 /headers 엔드포인트로 GET 요청하면
		- 요청에 사용한 요청 헤더를 반환
		- `x-b3-*` Zipkin 헤더가 요청에 자동으로 붙었다.
		- 이 Zipkin 헤더들은 Span을 만드는데 사용되며, Jaeger로 보내진다.

![]({{ site.url }}/img/post/devops/study/istio/4/20250503221733.png)

### 분산 트레이싱 데이터 보기
- Span이 Jaeger(혹은 기타 오픈트레이싱 엔진)로 보내질때, 트레이스 및 관련 Span을 쿼리하고 볼 수 잇는 방법이 필요함
- Jaeger UI를 사용
- Service - istio-ingressgateway - 좌측 하단 Find Traces

![]({{ site.url }}/img/post/devops/study/istio/4/20250503222133.png)
![]({{ site.url }}/img/post/devops/study/istio/4/20250503222331.png)

- 애플리케이션이 제대로 동작하려면 Zipkin 트레이스 헤더를 전파해야 한다.
	- `x-request=id`
	- `x-b3-traceid`
	- `x-b3-spanid`
	- `x-b3-parentspanid`
	- `x-b3-sampled`
	- `x-b3-flags`
	- `x-ot-span-context`
- 애플리케이션 코드가 요청을 받아 처리 시작시
	- 이 헤더와 그 값을 저장했다가 애플리케이션이 수행해야 하는 모든 발신 요청에 삽입해야 한다.
	- 프록시는 자동으로 이 작업 못함

### 트레이스 샘플링, 강제 트레이스, 커스텀 태그
#### 트레이스 샘플링
- 샘플링 비율도 이전에 했던 것처럼 설정할 수 있다.

```bash
# 메시 전역 설정
kubectl edit -n istio-system cm istio
...
     sampling: 10  # <-- from 100
...

# 워크로드별 설정
# pod template의 애노테이션을 수정한다.
cat ch8/webapp-deployment-zipkin.yaml
...
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      annotations:
        proxy.istio.io/config: |
          tracing:
            sampling: 10
            zipkin:
              address: zipkin.istio-system:9411
...

kubectl apply -f ch8/webapp-deployment-zipkin.yaml -n istioinaction

# 샘플링 적용하려면 istio-ingressgateway를 재배포해야 한다.
kubectl rollout restart deploy -n istio-system istio-ingressgateway

# 호출 테스트
# 10번 호출하면 10% 정도 수집되어야 함
for i in {1..10}; do curl -s http://webapp.istioinaction.io:30000/api/catalog | jq; sleep 0.5; done
...
```

- 호출 테스트 후 Jaeger UI에서 샘플링 비율 대로 수집되는지 확인...

![]({{ site.url }}/img/post/devops/study/istio/4/20250503230825.png)

#### 강제 트레이싱
- 운영 환경에서 트레이스의 샘플링 비율을 최소로 설정한 후
	- 문제 발생시에만 특정 워크로드에 대해 활성화해야 한다.
- 하지만 가깜 특정 요청에 트레이싱을 활성화해야 하는 경우가 있다.
- 이때!! 특정 요청에만 트레이싱을 강제하도록 설정한다.
	- 요청 헤더에 x-envoy-force-trace: true 추가

```bash
# 테스트를 위해 sampling을 0으로 수정하였음
# 헤더를 붙인 요청만큼만 수집되어야 함
# 헤더를 붙여서 5번, 안붙여서 2번 요청한다면. 5개 수집되어야 함
for i in {1..5}; do curl -s -H "x-envoy-force-trace: true" http://webapp.istioinaction.io:30000/api/catalog -v; sleep 0.5; done
for i in {1..2}; do curl -s http://webapp.istioinaction.io:30000/api/catalog -v; sleep 0.5; done
...
```

![]({{ site.url }}/img/post/devops/study/istio/4/20250503230225.png)

- `x-envoy-force-trace` 헤더를 보낼 때마다 해당 요청과 그 요청의 호출 그래프 전체에 대해 트레이싱을 트리거 한다.
- 이 헤더를 주입할 수 있는 API 게이트웨이와 진단 서비스 같은 도구를 이스티오 위에 구축할 수 있다.
	- 특정 요청에 대해 더 많은 정보를 얻기 위해서

#### 커스텀 태그
- Span에 태그를 추가하는 것
	- 애플리케이션이 트레이스에 추가 메타데이터를 첨부하는 방법
- Tags?
	- 단순 Key - Value 쌍
	- 애플리케이션 혹은 조직별 커스텀 정보
	- 백엔드 분산 트레이싱 엔진으로 보내는 Span에 추가됨
- 커스텀 태그 유형
	- 명시적으로  값 지정
	- 환경 변수에서 값 가져오기
	- 요청 헤더에서 값 가져오기

``` bash
# webapp 서비스의 Span에 커스텀 태그 추가
# 해당 워크로드의 Deployment에 애노테이션으로 추가함
cat ch8/webapp-deployment-zipkin-tag.yaml
...
  template:
    metadata:
      annotations:
        proxy.istio.io/config: |
          tracing:
            sampling: 100
            customTags:
              custom_tag: # 커스텀 태그의 키
                literal:
                  value: "Test Tag" # 커스텀 태그의 값
            zipkin:
              address: zipkin.istio-system:9411
...

# webapp 에 커스텀 태그 적용
kubectl apply -n istioinaction -f ch8/webapp-deployment-zipkin-tag.yaml

# 호출
for in in {1..10}; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; sleep 0.5; done
```

![]({{ site.url }}/img/post/devops/study/istio/4/20250503231430.png)

- 커스텀 태그는 reporting, filtering, 트레이싱 탐색에 사용할 수 있다.
- 하지만 Span 레벨에 태그가 추가된 것이기 때문에 JaegerUI에서는 Filtering 할 수 없다.

#### 백엔드 분산 트레이싱 엔진 커스터마이징

- 이스티오 1.12 버전에서 트레이싱을 포함하는 새로운 텔레메트리용 alpha API를 릴리스했다.
	- 트레이싱 설정 면에서 사용자 경험이 개선될 것이다.
	- 일단 기존 방식으로 스터디 진행
- 지금까지는 백엔드 트레이싱 엔진의 호스트네임과 포트로 이스티오를 설정했음
- 더 많은 설정을 해야 한다면?
	- ex. Jaeger의 Zipkin 호환성을 사용하려면 Jaeger 수집기의 특정 엔드포인트로 추적을 전송
- 기본) 이스티오 프록시에서 정적 설정

```bash
# deploy/webapp 트레이싱 설정 조회 : 현재 기본 설정
istioctl pc bootstrap -n istioinaction deploy/webapp -o json | jq .bootstrap.tracing
{
  "http": {
    "name": "envoy.tracers.zipkin",
    "typedConfig": {
      "@type": "type.googleapis.com/envoy.config.trace.v3.ZipkinConfig",
      "collectorCluster": "zipkin",
      "collectorEndpoint": "/api/v2/spans",
      "traceId128bit": true,
      "sharedSpanContext": false,
      "collectorEndpointVersion": "HTTP_JSON"
    }
  }
}
# 현재 설정
- tracing engine: Zipkin-based
- Span: /api/v2/spans
- JSON 엔드포인트로 처리

# 커스텀 부트스트랩 설정으로 기본 설정을 변경
# configmap에서 튜닝하고자 하는 설정 스니펫을 지정
# 해당 configmap 은 collectorEndpoint 를 변경한 설정 스니펫
# /api/v2/spans -> /zipkin/api/v1/spans
cat ch8/istio-custom-bootstrap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: istio-custom-zipkin
data:
  custom_bootstrap.json: |
    {
      "tracing": {
        "http": {
          "name": "envoy.tracers.zipkin",
          "typedConfig": {
            "@type": "type.googleapis.com/envoy.config.trace.v3.ZipkinConfig",
            "collectorCluster": "zipkin",
            "collectorEndpoint": "/zipkin/api/v1/spans",
            "traceId128bit": "true",
            "collectorEndpointVersion": "HTTP_JSON"
          }
        }
      }
    }

# 이 부트스트랩 설정을 덮어 쓰려는 워크로드가 있는 네임스페이스에 configmap 을 적용할 수 있다.
kubectl apply -n istioinaction -f ch8/istio-custom-bootstrap.yaml

# 확인
kubectl get cm -n istioinaction

# 해당 configmap 을 참조하는 Deployment 리소스의 파드 템플릿에 애노테이션을 추가
cat ch8/webapp-deployment-custom-boot.yaml
...
  template:
    metadata:
      annotations:
        sidecar.istio.io/bootstrapOverride: "istio-custom-zipkin" # 부트스트랩 설정을 istio-custom-zipkin 사용
        proxy.istio.io/config: |
          tracing:
            sampling: 10
            zipkin:
              address: zipkin.istio-system:9411
      labels:
        app: webapp
...

# 변경된 설정으로 webapp을 재배포 합니다
kubectl apply -n istioinaction -f ch8/webapp-deployment-custom-boot.yaml

# deploy/webapp 트레이싱 설정 조회 : 현재 기본 설정
istioctl pc bootstrap -n istioinaction deploy/webapp -o json | jq .bootstrap.tracing
{
  "http": {
    "name": "envoy.tracers.zipkin",
    "typedConfig": {
      "@type": "type.googleapis.com/envoy.config.trace.v3.ZipkinConfig",
      "collectorCluster": "zipkin",
      "collectorEndpoint": "/zipkin/api/v1/spans",
      "traceId128bit": true,
      "collectorEndpointVersion": "HTTP_JSON"
    }
  }
}

# 호출
for in in {1..10}; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; sleep 0.5; done
for in in {1..10}; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; sleep 0.5; done
...
```

- Jaeger 대시보드 확인
	- webapp 추적시 collectorEndpoint에 잘못된 경로 설정으로 webapp Span이 출력되지 않는다.

![]({{ site.url }}/img/post/devops/study/istio/4/20250503233600.png)
![]({{ site.url }}/img/post/devops/study/istio/4/20250503233447.png)

```bash
# 다시 원상 복구
# istio-custom-zipkin 어노테이션이 없는 webapp으로 재배포
kubectl apply -n istioinaction -f services/webapp/kubernetes/webapp.yaml

# 호출
for in in {1..10}; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; sleep 0.5; done
```

![]({{ site.url }}/img/post/devops/study/istio/4/20250503233759.png)

## Kiali를 이용한 시각화
- 이스티오는 Kiali의 강력한 시각화 대시보드를 함깨 사용할 수 있음
- 프로메테우스와 기반 플랫폼에서 많은 양의 메트릭을 가져와 메시 내 구성 요소의 런타임 그래프를 구성
- 그래프와 상호작용
	- 문제 가능성 영역을 파고들 수 있음
- 실시간으로 갱신되는 메트릭을 사용해 서비스가 어떻게 통신하는지에 대한 방향 그래프를 구축
- 다른 대시보드들(게이지, 카운터, 차트 등의 Grafana의 대시보드)도 훌륭하지만, 클러스터 내 서비스에 대한 상호작용형 그림이나 지도는 보여주지 않음

### 키알리 설치하기
- 이스티오는 Kiali 샘플 버전을 기본으로 제공
- Istio / Kiali 팀은 실제 배포시 Kiali Operator를 사용하는 것을 권장
	- [공식 설치 가이드](https://kiali.io/docs/installation/installation-guide/)를 참조
- Kiali는 프로메테우스에 저장된 이스티오 메트릭을 시각화한다.
	- Kiali 설치 전에 반드시 프로메테우스를 설치/설정해야 한다.

```bash
# helm repo
helm repo add kiali https://kiali.org/helm-charts
helm repo update 

# kiali-operator install : 책은 1.40.1
helm install --namespace kiali-operator --create-namespace --version 1.63.2 kiali-operator kiali/kiali-operator

# kiali-operator 확인
kubectl get pod -n kiali-operator
NAME                             READY   STATUS    RESTARTS   AGE
kiali-operator-584858fb7-rvj8w   1/1     Running             0          59s

# istio-system에 kiali 인스턴스 배포
cat ch8/kiali.yaml
apiVersion: kiali.io/v1alpha1
kind: Kiali
metadata:
  namespace: istio-system
  name: kiali
spec:
  istio_namespace: "istio-system"  
  istio_component_namespaces:
    prometheus: prometheus
  auth:    
    strategy: anonymous # 익명 접근 허용
  deployment:
    accessible_namespaces:
    - '**'
  external_services:    
    prometheus: # 클러스터 내에서 실행 중인 프로메테우스 설정
      cache_duration: 10
      cache_enabled: true
      cache_expiration: 300
      url: "http://prom-kube-prometheus-stack-prometheus.prometheus:9090"    
    tracing: # 클러스터 내에서 실행 중인 예거 설정
      enabled: true
      in_cluster_url: "http://tracing.istio-system:16685/jaeger"
      use_grpc: true

# 키알리 인스턴스(대시보드) 설치
kubectl apply -f ch8/kiali.yaml

# 확인
kubectl get deploy,svc -n istio-system kiali
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/kiali   1/1     1            1           36s

NAME            TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)              AGE
service/kiali   ClusterIP   10.200.1.179   <none>        20001/TCP,9090/TCP   36s

# NodePort 변경 및 nodeport kiali(30003)
kubectl patch svc -n istio-system kiali -p '{"spec": {"type": "NodePort", "ports": [{"port": 20001, "targetPort": 20001, "nodePort": 30003}]}}'

# Kiali 접속 1 : NodePort
open http://127.0.0.1:30003

# 트래픽 주입
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done
```

![]({{ site.url }}/img/post/devops/study/istio/4/20250503235253.png)

- Graph
	- 트래픽의 이동과 흐름
	- 바이트 수, 요청 개수 등
	- 여러 버전에 대한 여러 트래픽 흐름(ex. 카나리 릴리스나 가중치 라우팅)
	- 초당 요청 수. 총량 대비 여러 버전의 트래픽 비율
	- 네트워크 트래픽에 기반한 애플리케이션 상태(health)
	- HTTP/TCP 트래픽
	- 빠르게 식별할 수 있는 네트워크 실패

![]({{ site.url }}/img/post/devops/study/istio/4/20250503235604.png)

- Workloads - Traces

![]({{ site.url }}/img/post/devops/study/istio/4/20250503235829.png)

#### 트레이스, 메트릭, 로그의 연관성
- Workloads 메뉴
	- Overview: 서비스의 파드들, 거기에 적용된 이스티오 설정, 업스트립 및 다운스트림의 그래프
	- Traffic: 인바운드 및 아웃바운드 트래픽의 성공률
	- Logs: 애플리케이션 로그, 엔보이 액세스 로그, 연관된 스팬
	- Inbound Metrics 및 Outbound Metrics: 스팬과 연관된 메트릭
	- Traces: Jaeger가 보고한 트레이스
	- Envoy: 워크로드에 적용된 엔보이 설정. 클러스터, 리스터, 라우트 등

![]({{ site.url }}/img/post/devops/study/istio/4/20250504002418.png)

- 서비스 메시 운영자에게 Kiali란..
	- 이스티오 리소스의 유효성 검사
		- 존재하지 않는 Gateway를 가리키는 VirtualService
		- 존재하지 않는 목적지로의 라우팅
		- 동일한 호스트에 대한 둘 이상의 VirtualService
		- 찾을 수 없는 서비스 부분집합
		- [그 외](https://kiali.io/docs/features/validations/)

---
- `도전과제1` **Istio** 1.17 **공식 문서**에 **7장 관련 기술 내용들 실습 및 정리** 해보기
    - Tasks > Observability > Telemetry API - [Docs](https://istio.io/v1.17/docs/tasks/observability/telemetry/)
    - Operations > Configuration > Observability > Envoy Statistics - [Docs](https://istio.io/v1.17/docs/ops/configuration/telemetry/envoy-stats/)
    - Operations > Integrations > Prometheus - [Docs](https://istio.io/v1.17/docs/ops/integrations/prometheus/)
    - Reference > Configuration > Telemetry - [Docs](https://istio.io/v1.17/docs/reference/config/telemetry/)
- `도전과제2` Telemetry 를 사용하여 특정 ‘네임스페이스, 워크로드’에 특정 ‘메트릭, 로그, 트레이스’ 설정을 적용 해보자
- `도전과제3` **도커**(컴포즈)를 이용하여 **컨테이너 로그** 부터 **Otel** exporter/Collector, **Trace**(zipkin), **프로메테우스/그라파나/Tempo** 설정
- `도전과제4` Istio 최신 버전에 Trace 를 Otel 를 사용하여 설치 및 설정 후 분산 트레이싱 확인 해보자 - [Docs](https://istio.io/latest/docs/tasks/observability/distributed-tracing/opentelemetry/)
