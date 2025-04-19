---
layout: post
section-type: post
title: ServiceMesh - Istio - Week2 - Envoy, IstioGateway
category: devops
tags: [ 'k8s', 'istio', 'servicemesh', 'envoy', 'istiogateway' ]
---

# 3. 이스티오의 데이터 플레인: 엔보이 프록시
서비스 메시에서 데이터 플레인을 구성하는 핵심 컴포넌트는 Envoy Proxy다. 

## Envoy Proxy란?
- Lyft에서 개발
- 2016년에 오픈소스화. 2017년에 CNCF에 합류
- C++로 작성, 높은 부하에서 안정적으로 돌도록 설계됐다.

프록시는 클라이언트랑 서버 사이에 끼어드는 녀석이다. 로드 밸런싱, 보안, 프라이버시 등 여러 기능을 제공한다.
![]({{ site.url }}/img/post/devops/study/istio/2/20250409203255.png)
예를 들어 클라이언트가 어떤 IP를 호출해야 할지 몰라도, Envoy가 중간에서 알아서 인스턴스 골라준다.
![]({{ site.url }}/img/post/devops/study/istio/2/20250409203616.png)

그냥 단순한 커넥션 레벨 프록시가 아니라 L7 프로토콜까지 이해한다.
HTTP 1.1, HTTP 2, gRPC 기본 지원. 타임아웃, 재시도, 서킷 브레이커 등 복원력 기능도 붙일 수 있음.

DB나 비동기 프로토콜(MongoDB, DynamoDB, AMQP 등)도 필터 확장으로 처리 가능하다.
텔레메트리도 풍부하게 수집할 수 있어서 관측성 확보에 좋음.

Envoy는 독립 실행도 가능하고, 클러스터 엣지 프록시나 공유 프록시로도 가능.
Istio에서는 각 서비스마다 하나씩 붙이는 패턴을 채택했음.
에지 프록시랑 똑같이 구성하면 관리 편해진다.

## 핵심 개념 정리
- **리스너(listener)**: 외부로 포트 노출
- **라우트(routes)**: 리스너로 들어온 요청에 라우팅 규칙 적용
- **클러스터(cluster)**: 요청이 향할 백엔드 그룹
    
![]({{ site.url }}/img/post/devops/study/istio/2/20250414220809.png)
트래픽은 다운스트림 → Envoy → 업스트림 순서로 흐른다.

## Envoy의 핵심 기능

### 서비스 디스커버리(Service Discovery)
IP를 몰라도 Envoy가 알아서 디스커버리 API 통해 찾음.
Istio는 이걸 Control Plane에서 자동화한다.

### **로드 밸런싱**
Envoy는 애플리케이션이 활용할 수 있는 고급 로드 밸런싱 알고리듬을 여러 가지 구현하고 있다.
- 랜덤(Random)
	- 무작위로 분배
	- 성능 부하가 균등하지 않을 수 있으나, 간단하고 빠름
- 라운드 로빈(Round Robin)
	- 요청을 순서대로 분배
- Weighted
	- 특정 비율에 따라 분산
	- 실제로는 서브셋과 트래픽 분배로 구현됨
- Hash
	- 세션 유지나 캐시 적중률이 중요한 서비스에 적합
	- Consistent hash
		- 세션 어피니티를 위해 HTTP 헤어, 쿠키, URL 등을 기준으로 일관된 분배
	- Ring hash
		- [Ketama algorithm](https://www.metabrew.com/article/libketama-consistent-hashing-algo-memcached-clients)을 이용한 분산
	- Maglev
		-  Ring Hash보다 더 빠르고 고르게 분산
		- Google 논문 기반
		- 큰 규모의 트래픽에도 안정적
  
지역 기반(locality aware) 로드 밸런싱도 지원한다.

### **트래픽 라우팅**
HTTP 1.1, 2 다 지원.
Header 기반, context-path 기반, 우선순위 기반 등 정교한 라우팅 가능.
재시도, 타임아웃, 오류 주입도 가능

### **트래픽 전환/분할과 섀도잉**
- 카나리 릴리스 가능
	- 비율 기반(가중치 적용) 트래픽 분할(splitting)/전환(shifting)을 지원
- 섀도잉(Shadowing)
	- 요청 복사본을 다른 백엔드로 보내서 실트래픽 없이 테스트할 수 있는 기능

### **네트워크 복원력**
타임아웃, 재시도, 서킷 브레이커 다 지원.
이상값 감지(outlier detection)로 오동작 인스턴스를 제거할 수 있음.

### **HTTP/2와 gRPC**
- HTTP/2
	- 단일 커넥션으로 여러 요청을 처리
	- 서버 푸시, 스트리밍, 요청 백프래셔(backpressure) 지원
- gRPC
	- 강력하지만 구현이 어려움
	- 다른 서비스 프록시보다 Envoy가 잘 구현함

### 메트릭 수집을 통한 관찰 가능성
- 통계: 카운터, 게이지, 히스토그램
    - `downstream_cx_tota`
        - 총 커넥션 개수
    - `downstream_cx_http1_active`
        - 총 활성 HTTP/1.1 커넥션 개수
    - `downstream_rq_http2_total`
        - 총 HTTP/2 요청 개수
    - `cluster.<name>.upstream_cx_overflow`
        - 클러스터의 커넥션 서킷 브레이커가 임계값을 넘겨 발동한 횟수
    - `cluster.<name>.upstream_rq_retry`
        - 총 요청 재시도 횟수
    - `cluster.<name>.ejections_detected_consecutive_5xx`
        - 5xx 오류가 계속돼 퇴출된 횟수<br>(시행되지 않은 경우도 포함)
- 통계 출력 포맷: StatsD, Datadog, Prometheus 등 지원

### **분산 트레이싱**
트레이스 스팬을 오픈 트래이싱(OpenTracing) 엔진에 보고하여 호출 그래프 내 트래픽 흐름, 홉, 지연 시간을 시각화 할 수 있다.
- Jaeger, Zipkin 연동 가능
- x-b3-* 헤더 필요.
	- Envoy가 자동 생성도 가능.
	- 애플리케이션이 전파해야 하는 헤더
		- x-b3-traceid
		- x-b3-spanid
		- x-b3-parentspain
		- x-b3-sampled
		- x-b3-flags

### **TLS/mTLS 처리**
- TLS 시작/종료 자동화 가능
- 인증서도 Istio가 자동 관리.

### **속도 제한**
보호받는 리소스로의 접근을 차단/제한.
- 리소스들(DB, 캐시, 공유 서비스 등)이 보호받을 이유
	- 호출(call) 비용이 비쌈(실행(invocation)당 비용)
	- 지연 시간이 길거나 예측 불가능
	- 기아(starvation)을 방지하기 위해 공정성 알고리듬 필요
재시도 폭발 방지에 유용.

### **확장성**
필터 체계(L7 Filter)로 필요에 맞게 확장.
- C++로 작성
- Lua, WebAssembly 지원.

### Envoy와 다른 프록시 비교
- Envoy의 뛰어난 영역
	- 웹어셈블리를 통한 확장성
	- 공개 커뮤니티
	- 유지 보수 및 확장이 용이하도록 구축한 모듈식 코드베이스
	- HTTP/2 지원(업/다운 스트림)
	- 심층 프로토콜 메트릭 수집
	- C++ / 가비지 수집 없음
	- 동적 설정으로 hot restart가 필요 없음

## Envoy 설정하기

### 정적 구성
```yaml
static_resources:
  listeners:  # listener 정의
  - name: httpbin-demo
    address:
      socket_address:
        address: 0.0.0.0
        port_value: 15001
    filter_chains:
    - filters:
      - name: envoy.http_connection_manager # HTTP 필터
        typed_config:  
          route_config: # 라우팅 규칙
            name: httpin_local_route
            virtual_hosts:
            - name: httpbin_local_service
              domains: ["*"] # 와일드카드 가상 호스트
              routes:
              - match:
                  prefix: "/"
                route:
                  auto_host_rewrite: true
                  cluster: httpbin_service # 클러스터로 라우팅
          http_filters:
          - name: envoy.filters.http.router
  clusters:
  - name: httpbin_service # 업스트림 클러스터
    connect_timeout: 5s
    type: LOGICAL_DNS
    dns_lookup_family: V4_ONLY # ipv6 네트워크에서 테스트하려면 주석처리해야 함
    ib_policy: ROUND_ROBIN
    hosts: [{ socket_address: {
      address: httpbin, port_value: 8000 }}]
```
많은 설정(리스너, 라우팅 규칙, 필터, 클러스터 등)를 명시적으로 선언한다.

### 동적 구성 (xDS API)
- LDS(Listener Discovery Service)
	- Envoy가 자신이 어떤 listener를 노출해야 하는지 쿼리할 수 있게 하는 API
- RDS(Route Discovery Service)
	- listener 설정의 일부로, 사용할 루투를 지정한다.
	- 정적/동적 설정을 사용할 때 LDS의 부분집합이다.
- CDS(Cluster Discovery Service)
	- Envoy가 클러스터 목록과 각 클러스터용 설정을 찾을 수 있는 API
- EDS(Endpoint Discovery Service)
	- 클러스터 설정의 일부
	- 특정 클러스터에 어떤 엔드포인트를 사용해야 하는 지 지정
	- CDS의 부분 집합
- SDS(Secret Discovery Service)
	- 인증서를 배부하는데 사용하는 API
- ADS(Aggregate Discovery Service)
	- 나머지 API에 대한 모든 변경사항을 직렬화된 스트림으로 제공
	- 이 API 하나로 모든 변경 사항을 순차적으로 가져올 수 있다.

```yaml
dynamic_resources:
  lds_config: # LDS
    api_config_source:
      api_type: GRPC
      grpc_services:
        - envoy_grpc: # 이 클러스터로 이동해 리스터 API를 확인하자.
            cluster_name: xds_cluster
clusters:
- name: xds_cluster # LDS를 구현하는 gRPC 클러스터
  connect_timeout: 0.25s
  type: STATIC
  lb_policy: ROUND_ROBIN
  http2_protocol_options: {}
  hosts: [{ socket_address: {
    address: 1217.0.0.3, port_value: 5678 }}]
```

동적으로 구성 가능하다.
하지만 LDS API가 위치할 클러스터는 명시적으로 설정해야 한다.

Istio는 서비스 프록시용 부트스트랩 설정
```yaml
bootstrap:
  dynamicResources:    ldsConfig:
      ads: {}  # 리스터용 ADS
    cdsConfig:
      ads: {}  # 클러스터용 ADS
    adsConfig:
      apiType: GRPC
      grpcServices:
      - envoyGrpc:
          clusterName: xds-grpc # xds-grpc라는 클러스터를 사용
      refreshDelay: 1.000s
  staticResources:
    clusters:
    - name: xds-grpc # xds-grpc라는 클러스터를 정의
      type: STRICT_DNS
      connectTimout: 10.000s
      hosts:
      - socketAddress:
          address: istio-pilog.istio-system
          portValue: 15010
      circuitBreakers: # 신뢰성 및 서킷 브레이커 설정
        thresholds:
        - maxConnections: 100000
          maxPendingRequests: 100000
          maxRequests: 100000
        - priority: HIGH
          maxConnections: 100000
          maxPendingRequests: 100000
          maxRequests: 100000
      http2ProtocolOptions: {}
```

## **Istio에서 Envoy의 위치**
Envoy는 데이터를 다루는 쪽(Data Plane), Istio는 설정과 제어(Control Plane).
Istio가 xDS API로 Envoy 설정을 날려줌. 
![]({{ site.url }}/img/post/devops/study/istio/2/20250409204431.png)

Prometheus, Jaeger, Zipkin 등과 연동도 Istio가 해줌. 
![]({{ site.url }}/img/post/devops/study/istio/2/20250409205050.png)

TLS 인증서도 Istio가 관리.
![]({{ site.url }}/img/post/devops/study/istio/2/20250409205158.png)

## 실습
```bash
# 도커 이미지 가져오기 
docker pull envoyproxy/envoy:v1.19.0 
docker pull curlimages/curl 
docker pull mccutchen/go-httpbin 
# docker pull citizenstig/httpbin 

# 확인 
docker images

# mccutchen/go-httpbin 는 기본 8080 포트여서, 책 실습에 맞게 8000으로 변경 
# docker run -d -e PORT=8000 --name httpbin mccutchen/go-httpbin -p 8000:8000 
docker run -d -e PORT=8000 --name httpbin mccutchen/go-httpbin 
docker ps 

# curl 컨테이너로 httpbin 호출 확인 
# /headers 엔드포인트를 호출하는데 사용한 헤더가 반환된다.
docker run -it --rm --link httpbin curlimages/curl curl -X GET http://httpbin:8000/headers 
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250418222211.png)

```bash
# Envoy 실행
# 유효한 설정 파일을 전달하지 않음
docker run -it --rm envoyproxy/envoy:v1.19.0 envoy
...
At least one of --config-path or --config-yaml or Options::configProto() should be non-empty

# 설정파일과 함께 Envoy 실행
# 터미널1
docker run --name proxy --link httpbin envoyproxy/envoy:v1.19.0 --config-yaml "$(cat ch3/simple.yaml)" 
...
[2025-04-18 13:14:56.227][1][info][config] [source/server/listener_manager_impl.cc:834] all dependencies initialized. starting workers
[2025-04-18 13:14:56.230][1][info][main] [source/server/server.cc:804] starting main dispatch loop

# 터미널2 
docker logs proxy
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15001/headers
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250418222404.png)

> `X-Envoy-Expected-Rq-Timeout-Ms`, `X-Forwarded-Proto`, `X-Request-Id` header가 추가되었다.
> 이 부분은 Envoy가 추가한 것이다.

```bash
# 타임아웃을 1초로 변경 
docker rm -f proxy

cat ch3/simple_change_timeout.yaml
	...
              - match: { prefix: "/" }
                route:
                  auto_host_rewrite: true
                  cluster: httpbin_service
                  timeout: 1s
	...

docker run --name proxy --link httpbin envoyproxy/envoy:v1.19.0 --config-yaml "$(cat ch3/simple_change_timeout.yaml)" 
docker ps
# 변경된 타임아웃 설정 확인
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15001/headers
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250418222759.png)
> `X-Envoy-Expected-Rq-Timeout-Ms`가 15000 -> 1000으로 변경되었다.

```bash
# 추가 테스트 : Envoy Admin API(TCP 15000) 를 통해 delay 설정 
## logging 모드를 확인 및 설정할 수 있다.
docker run -it --rm --link proxy curlimages/curl curl -X POST http://proxy:15000/logging 
docker run -it --rm --link proxy curlimages/curl curl -X POST http://proxy:15000/logging?http=debug 

# /delay/<second> 를 호출하면 httpbin 서비스가 해당 시간만큼 지연하고 응답한다.
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15001/delay/0.5 
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15001/delay/1 
## Envoy가 요청을 받아서 httpbin으로 보내는데,
## httpbin이 2초 후에 응답을 한다.
## Envoy의 셋팅은 현재 1초만 기다리도록 되어 있기 때문에,
## Envoy가 중간에 끊어버린다.
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15001/delay/2

docker rm -f proxy
```

![]({{ site.url }}/img/post/devops/study/istio/2/2025-04-18.png)

## 실습 - Envoy's AdminAPI
```bash
docker run --name proxy --link httpbin envoyproxy/envoy:v1.19.0 --config-yaml "$(cat ch3/simple_change_timeout.yaml)"

# admin API로 Envoy stat 확인 : 응답은 리스너, 클러스터, 서버에 대한 통계 및 메트릭
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15000/stats

# retry 통계만 확인
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15000/stats | grep retry

# 다른 엔드포인트 일부 목록들도 확인
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15000/certs # 머신상의 인증서
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15000/clusters # 엔보이에 설정한 클러스터
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15000/config_dump # 엔보이 설정 덤프
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15000/listeners # 엔보이에 설정한 리스너
docker run -it --rm --link proxy curlimages/curl curl -X POST http://proxy:15000/logging # 로깅 설정 확인 가능
docker run -it --rm --link proxy curlimages/curl curl -X POST http://proxy:15000/logging?http=debug # 로깅 설정 편집 가능
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15000/stats # 엔보이 통계
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15000/stats/prometheus # 엔보이 통계(프로메테우스 레코드 형식)
```

## 실습 - Envoy request retries
```bash
docker rm -f proxy

cat ch3/simple_retry.yaml
	...
              routes:
              - match: { prefix: "/" }
                route:
                  auto_host_rewrite: true
                  cluster: httpbin_service
                  retry_policy:
                      retry_on: 5xx
                      num_retries: 3
	...
               
docker run -p 15000:15000 --name proxy --link httpbin envoyproxy/envoy:v1.19.0 --config-yaml "$(cat ch3/simple_retry.yaml)"
docker run -it --rm --link proxy curlimages/curl curl -X POST http://proxy:15000/logging?http=debug

# /stats/500 경로로 프록시를 호출 : 이 경로로 httphbin 호출하면 오류가 발생
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15001/status/500

# 호출이 끝났는데 아무런 응답도 보이지 않는다. 엔보이 Admin API에 확인
docker run -it --rm --link proxy curlimages/curl curl -X GET http://proxy:15000/stats | grep retry
```

![]({{ site.url }}/img/post/devops/study/istio/2/20250418225842.png)
> retry를 3번한 것을 볼 수 있다.

> [envoy quick start](https://www.envoyproxy.io/docs/envoy/latest/start/quick-start/) - 굉장히 잘 정리되어 있으니 꼭 해보자.

---

### 실습 준비
- kind로 cluster 셋팅
	- https://raw.githubusercontent.com/KimDoKy/istio-in-action-book-source-code/refs/heads/master/kind_2.sh
- istio 설치 및 추가 설정
	- https://raw.githubusercontent.com/KimDoKy/istio-in-action-book-source-code/refs/heads/master/install_istio_on_control_plane.sh

---

# 4. 이스티오 게이트웨이: 클러스터로 트래픽 들이기

서비스 메시 밖에서 시작한 트래픽을 클러스터 내부로 안전하게 유입시키려면, Istio Ingress Gateway가 필요하다. 서비스 메시의 엣지에 위치해서 라우팅, 보안, 로드 밸런싱까지 담당하는 핵심 컴포넌트다.

![]({{ site.url }}/img/post/devops/study/istio/2/20250409205603.png)

## 인그레스 개념
- Ingress Point: 외부 트래픽이 클러스터 내부로 들어오는 진입 지점
- Ingress: 외부 → 내부로 흐르는 트래픽

이 트래픽은 먼저 네트워크 문지기인 Ingress Point를 거친다. 
허용된 요청만 프록시를 통해 로컬 네트워크의 올바른 엔드포인트로 들어갈 수 있다.

## 가상 IP & 가상 호스팅
단일 인스턴스에 도메인을 바인딩하면 장애 발생 시 고장난 인스턴스를 향하게 된다. 
가상 IP(Reverse Proxy)를 통해 여러 인스턴스에 분산하고 고가용성 보장.
- 하나의 IP로 여러 호스트네임을 매핑 가능 (ex. prod.istioinaction.io, api.istioinaction.io)
- HTTP 1.1 → Host 헤더, HTTP 2 → :authority, TCP → SNI로 판단
![]({{ site.url }}/img/post/devops/study/istio/2/20250409211552.png)

## Istio Ingress Gateway 구조
Istio는 하나의 Envoy Proxy로 Ingress Gateway를 구현한다.
이 Envoy는 외부 트래픽을 클러스터 안으로 라우팅하고, 로드 밸런싱 및 TLS 종료 등도 맡는다.
![]({{ site.url }}/img/post/devops/study/istio/2/20250409211918.png)

```bash
# 파드에 컨테이너 1개 기동 : 별도의 애플리케이션 컨테이너가 불필요.
kubectl get pod -n istio-system -l app=istio-ingressgateway
NAME                                   READY   STATUS    RESTARTS   AGE
istio-ingressgateway-996bc6bb6-mktpr   1/1     Running   0          13m

# proxy 상태 확인
docker exec -it myk8s-control-plane istioctl proxy-status
NAME                                                  CLUSTER        CDS        LDS        EDS        RDS          ECDS         ISTIOD                      VERSION
istio-ingressgateway-996bc6bb6-mktpr.istio-system     Kubernetes     SYNCED     SYNCED     SYNCED     NOT SENT     NOT SENT     istiod-7df6ffc78d-r7h54     1.17.8

# proxy 설정 확인
docker exec -it myk8s-control-plane istioctl proxy-config all deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system
ADDRESS PORT  MATCH DESTINATION
0.0.0.0 15021 ALL   Inline Route: /healthz/ready*
0.0.0.0 15090 ALL   Inline Route: /stats/prometheus*

docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system
NAME     DOMAINS     MATCH                  VIRTUAL SERVICE
         *           /stats/prometheus*
         *           /healthz/ready*
         
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config log deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/istio-ingressgateway.istio-system

# 설정 참고
kubectl get istiooperators -n istio-system -o yaml
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250418234121.png)

```bash
# pilot-agent 프로세스가 envoy 를 부트스트랩
kubectl exec -n istio-system deploy/istio-ingressgateway -- ps            
kubectl exec -n istio-system deploy/istio-ingressgateway -- ps aux

# 프로세스 실행 유저 정보 확인
kubectl exec -n istio-system deploy/istio-ingressgateway -- whoami
kubectl exec -n istio-system deploy/istio-ingressgateway -- id
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250418234302.png)

## 설정 구성요소
### 1. Gateway 리소스
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: coolstore-gateway # 게이트웨이 이름
spec:
  selector:
    istio: ingressgateway # 어느 게이트웨이 구현체인가?
  servers:
  - port:
      number: 80 # 노출할 포트
      name: http
      protocol: HTTP
    hosts:
    - "webapp.istioinaction.io" # 이 포트의 호스트
```
- 어떤 포트를 열 것인지
- 어떤 프로토콜을 받을 것인지
- 어떤 호스트를 허용할 것인지 정의

```bash
# 신규터미널 : istiod 로그
kubectl stern -n istio-system -l app=istiod
...

# 터미널2
cat ch4/coolstore-gw.yaml
kubectl -n istioinaction apply -f ch4/coolstore-gw.yaml

# 확인
kubectl get gw,vs -n istioinaction
NAME                                            AGE
gateway.networking.istio.io/coolstore-gateway   14s

docker exec -it myk8s-control-plane istioctl proxy-status
NAME                                                  CLUSTER        CDS        LDS        EDS        RDS        ECDS         ISTIOD                      VERSION
istio-ingressgateway-996bc6bb6-mktpr.istio-system     Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED     NOT SENT     istiod-7df6ffc78d-r7h54     1.17.8

docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system
ADDRESS PORT  MATCH DESTINATION
0.0.0.0 8080  ALL   Route: http.8080
...

docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system
NAME          DOMAINS     MATCH                  VIRTUAL SERVICE
http.8080     *           /*                     404
...     

# http.8080 정보의 의미는? 그외 나머지 포트의 역할은?
kubectl get svc -n istio-system istio-ingressgateway -o jsonpath="{.spec.ports}" | jq
[
  {
    "name": "status-port",
    "nodePort": 30326,
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

# HTTP 포트(80)을 올바르게 노출했다. VirtualService 는 아직 아무것도 없다.
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system -o json
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system -o json --name http.8080
[
    {
        "name": "http.8080",
        "virtualHosts": [
            {
                "name": "blackhole:80",
                "domains": [
                    "*"
                ]
            }
        ],
        "validateClusters": false,
        "ignorePortInHostMatching": true
    }
]
```

### 2. VirtualService 리소스
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: webapp-vs-from-gw # VirtualService 이름
spec:
  hosts:
  - "webapp.istioinaction.io" # 비교할 가상 호스트네임들
  gateways:
  - coolstore-gateway  # 이 VirtualService를 적용할 게이트웨이
  http:
  - route:
    - destination:  # 이 트래픽의 목적 서비스
        host: webapp
        port:
          number: 80
```
- Gateway와 연동
- 어떤 요청이 어느 서비스로 라우팅될지 정의

```bash
# 신규터미널 : istiod 로그
kubectl stern -n istio-system -l app=istiod
...

cat ch4/coolstore-vs.yaml
kubectl apply -n istioinaction -f ch4/coolstore-vs.yaml
kubectl get gw,vs -n istioinaction

docker exec -it myk8s-control-plane istioctl proxy-status
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system
...     
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250418235204.png)

```bash
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway.istio-system -o json --name http.8080
[
    {
        "name": "http.8080",
        "virtualHosts": [
            {
                "name": "webapp.istioinaction.io:80",
                "domains": [
                    "webapp.istioinaction.io" #1 비교할 도메인
                ],
                "routes": [
                    {
                        "match": {
                            "prefix": "/"
                        },
                        "route": { #2 라우팅 할 곳
                            "cluster": "outbound|80||webapp.istioinaction.svc.cluster.local",
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
                        "metadata": {
                            "filterMetadata": {
                                "istio": {
                                    "config": "/apis/networking.istio.io/v1alpha3/namespaces/istioinaction/virtual-service/webapp-vs-from-gw"
                                }
                            }
                        },
                        "decorator": {
                            "operation": "webapp.istioinaction.svc.cluster.local:80/*"
                        }
                    }
                ],
                "includeRequestAttemptCount": true
            }
        ],
        "validateClusters": false,
        "ignorePortInHostMatching": true
    }
]

# 실제 애플리케이션(서비스)를 배포 전으로 cluster 에 webapp, catalog 정보가 없다.
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system
...

# 동작을 위해 애플리케이션(서비스)를 배포
# 로그
kubectl stern -n istioinaction -l app=webapp
kubectl stern -n istioinaction -l app=catalog
kubectl stern -n istio-system -l app=istiod
...

# 배포
cat services/catalog/kubernetes/catalog.yaml
cat services/webapp/kubernetes/webapp.yaml 
kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction
kubectl apply -f services/webapp/kubernetes/webapp.yaml -n istioinaction

kubectl get pod -n istioinaction -owide

# krew plugin images 설치 후 사용
kubectl images -n istioinaction

# krew plugin resource-capacity 설치 후 사용 : istioinaction 네임스페이스에 파드에 컨테이너별 CPU/Mem Request/Limit 확인
kubectl resource-capacity -n istioinaction -c --pod-count
kubectl resource-capacity -n istioinaction -c --pod-count -u
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419000203.png)

```bash
docker exec -it myk8s-control-plane istioctl proxy-status
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/istio-ingressgateway.istio-system | egrep 'TYPE|istioinaction'
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419000020.png)

```bash
# istio-ingressgateway 에서 catalog/webapp 의 Service(ClusterIP)로 전달하는게 아니라, 바로 파드 IP인 Endpoint 로 전달함.
## 즉, istio 를 사용하지 않았다면, Service(ClusterIP) 동작 처리를 위해서 Node에 iptable/conntrack 를 사용했었어야 하지만,
## istio 사용 시에는 Node에 iptable/conntrack 를 사용하지 않아서, 이 부분에 대한 통신 라우팅 효율이 있다.
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system | egrep 'ENDPOINT|istioinaction'
ENDPOINT                                                STATUS      OUTLIER CHECK     CLUSTER
10.10.0.15:3000                                         HEALTHY     OK                outbound|80||catalog.istioinaction.svc.cluster.local
10.10.0.16:8080                                         HEALTHY     OK                outbound|80||webapp.istioinaction.svc.cluster.local


docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/webapp.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/webapp.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/webapp.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/webapp.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction | egrep 'ENDPOINT|istioinaction'
...

# 현재 모든 istio-proxy 가 EDS로 K8S Service(Endpoint) 정보를 알 고 있다
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction | egrep 'ENDPOINT|istioinaction'
...

# netshoot로 내부에서 catalog 접속 확인
kubectl exec -it netshoot -- curl -s http://catalog.istioinaction/items/1 | jq

# netshoot로 내부에서 webapp 접속 확인 : 즉 webapp은 다른 백엔드 서비스의 파사드 facade 역할을 한다.
kubectl exec -it netshoot -- curl -s http://webapp.istioinaction/api/catalog/items/1 | jq
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419000521.png)

```bash
# (추가) catalog, webapp에 replicas를 1 -> 2로 증가 후
# istio EDS(Endpoint) 정보 확인
# 로그 모니터링
kubectl stern -n istio-system -l app=istiod

# catalog, webapp 에 replicas=1 → 2로 증가
kubectl scale deployment -n istioinaction webapp --replicas 2
kubectl scale deployment -n istioinaction catalog --replicas 2# 모든 istio-proxy 가 EDS로 해당 K8S Service의 Endpoint 목록 정보 동기화되어 알고 있음을 확인
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system | egrep 'ENDPOINT|istioinaction'
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/webapp.istioinaction | egrep 'ENDPOINT|istioinaction'
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction | egrep 'ENDPOINT|istioinaction'
...
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419000707.png)

```bash
# 다음 실습을 위해서 catalog, webapp 에 replicas=2 → 1로 감소 해두기
kubectl scale deployment -n istioinaction webapp --replicas 1
kubectl scale deployment -n istioinaction catalog --replicas 1

# 인증서 정보 확인
kubectl exec -it deploy/webapp -n istioinaction -c istio-proxy -- curl http://localhost:15000/certs | jq
...
    {
      "ca_cert": [ # 루트 인증서
        {
          "path": "<inline>",
          "serial_number": "cbd3d7e892836cdd099317d163b64351",
          "subject_alt_names": [],
          "days_until_expiration": "3649",
          "valid_from": "2025-04-18T14:24:16Z",
          "expiration_time": "2035-04-16T14:24:16Z" # 만료 기간 10년
        }
      ],
      "cert_chain": [ # 사용자 인증서
        {
          "path": "<inline>",
          "serial_number": "27d38cfeff252e481aafd8aad152f3c4",
          "subject_alt_names": [
            {
              "uri": "spiffe://cluster.local/ns/istioinaction/sa/webapp"
            }
          ],
          "days_until_expiration": "0",
          "valid_from": "2025-04-18T14:55:31Z",
          "expiration_time": "2025-04-19T14:57:31Z" # 만료 기간 1일
        }
      ]
    },
...


istioctl proxy-config secret deploy/webapp.istioinaction -o json | jq '.dynamicActiveSecrets[0].secret.tlsCertificate.certificateChain.inlineBytes' -r | base64 -d | openssl x509 -noout -text

istioctl proxy-config secret deploy/catalog.istioinaction -o json | jq '.dynamicActiveSecrets[0].secret.tlsCertificate.certificateChain.inlineBytes' -r | base64 -d | openssl x509 -noout -text

istioctl proxy-config secret deploy/istio-ingressgateway.istio-system -o json | jq '.dynamicActiveSecrets[0].secret.tlsCertificate.certificateChain.inlineBytes' -r | base64 -d | openssl x509 -noout -text
```
![]({{ site.url }}/img/post/devops/study/istio/2/2025-04-19-2.png)

```bash
# 외부에서 호출
# 터미널 : istio-ingressgateway 로깅 수준 상향
kubectl exec -it deploy/istio-ingressgateway -n istio-system -- curl -X POST http://localhost:15000/logging?http=debug

kubectl stern -n istio-system -l app=istio-ingressgateway
혹은
kubectl logs -n istio-system -l app=istio-ingressgateway -f

# 외부(?)에서 호출 시도 : Host 헤더가 게이트웨이가 인식하는 호스트가 아니다
curl http://localhost:30000/api/catalog -v

# curl 에 host 헤더 지정 후 호출 시도
curl -s http://localhost:30000/api/catalog -H "Host: webapp.istioinaction.io" | jq
```
![]({{ site.url }}/img/post/devops/study/istio/2/2025-04-19-3.png)

### 전체적인 트래픽 흐름 개요
![]({{ site.url }}/img/post/devops/study/istio/2/20250409212708.png)

### SIMPLE TLS
- 인증서 + 키를 k8s secret으로 등록
- Gateway에 TLS 설정 추가

```yaml
# istio gateway 리소스가 인증서와 키를 사용하도록 설정
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: coolstore-gateway
spec:
  selector:
    istio: ingressgateway
  severs:
  - port:
      number: 80 # HTTP 트래픽 허용
      name: http
      protocol: HTTP
    hosts:
    - "webapp.istioinaction.io"
  - port:
      number: 443 # 보안 HTTPS 트래픽 허용
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE # 보안 커넥션
      credentialName: webapp-credential # TLS 인증서가 들어있는 k8s secret 이름
    hosts:
    - "webapp.istioinaction.io"
```

```bash
# 기본 istio-ingressgateway가 인증서와 키를 사용하도록 설정하려면
# 먼저 인증서/키를 k8s secret으로 만들어야 한다.

# istio ingressgateway가 가지고 있는 인증서를 확인
docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/istio-ingressgateway.istio-system

# 우리가 원하는 인증서를 주입해야 한다.
## 비밀키(개인키)
cat ch4/certs/3_application/private/webapp.istioinaction.io.key.pem
cat ch4/certs/3_application/certs/webapp.istioinaction.io.cert.pem
openssl x509 -in ch4/certs/3_application/certs/webapp.istioinaction.io.cert.pem -noout -text
```

![]({{ site.url }}/img/post/devops/study/istio/2/2025-04-19-4.png)
```bash
# webapp-credential 시크릿 만들기
kubectl create -n istio-system secret tls webapp-credential \
--key ch4/certs/3_application/private/webapp.istioinaction.io.key.pem \
--cert ch4/certs/3_application/certs/webapp.istioinaction.io.cert.pem

# 확인 : krew view-secret
kubectl view-secret -n istio-system webapp-credential --all

# istio-system 네임스페이스에 secret을 만든다.
# 운영 환경에서는 인그레스 게이트웨이를 istio-system과 분리해서 자체 네임스페이스에서 실행해야 한다.

# 이스티오 게이트웨이 리소스가 인증서와 키를 사용하도록 설정할 수 있다.
cat ch4/coolstore-gw-tls.yaml
kubectl apply -f ch4/coolstore-gw-tls.yaml -n istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/istio-ingressgateway.istio-system

# 호출 테스트 1
curl -v -H "Host: webapp.istioinaction.io" https://localhost:30005/api/catalog
# 서버(istio-ingressgateway 파드)에서 제공하는 인증서는 기본 CA 인증서 체인을 사용해 확인할 수 없다는 의미다.
# curl 클라이언트에 적절한 CA 인증서 체인을 전달해보자.
# (호출 실패) 원인: (기본 인증서 경로에) 인증서 없음. 사설인증서 이므로 “사설CA 인증서(체인)” 필요
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419170338.png)

```bash
# istio-ingressgateway에서 사용하는 신뢰할 수 있는 기본 인증서
kubectl exec -it deploy/istio-ingressgateway -n istio-system -- ls -l /etc/ssl/certs
...

cat ch4/certs/2_intermediate/certs/ca-chain.cert.pem
openssl x509 -in ch4/certs/2_intermediate/certs/ca-chain.cert.pem -noout -text
...
           X509v3 Basic Constraints: critical
                CA:TRUE, pathlen:0
...

# 호출 테스트 2
curl -v -H "Host: webapp.istioinaction.io" https://localhost:30005/api/catalog \
--cacert ch4/certs/2_intermediate/certs/ca-chain.cert.pem
# (호출 실패) 원인: 인증실패. 서버인증서가 발급된(issued) 도메인 “webapp.istioinaction.io”로 호출하지 않음 (localhost로 호출함)

# 도메인 질의를 위한 임시 설정 : 실습 완료 후에는 삭제 해둘 것
echo "127.0.0.1       webapp.istioinaction.io" | sudo tee -a /etc/hosts
cat /etc/hosts | tail -n 1

# 호출 테스트 3
curl -v https://webapp.istioinaction.io:30005/api/catalog \
--cacert ch4/certs/2_intermediate/certs/ca-chain.cert.pem
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419170820.png)

```bash
# https로 접속 확인
open https://webapp.istioinaction.io:30005
open https://webapp.istioinaction.io:30005/api/catalog
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419171348.png)

```bash
# http 접속도 확인해보자
curl -v http://webapp.istioinaction.io:30000/api/catalog
open http://webapp.istioinaction.io:30000

```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419171150.png)
![]({{ site.url }}/img/post/devops/study/istio/2/20250419171255.png)

### HTTPS Redirect
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: coolstore-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "webapp.istioinaction.io"
    tls:
      httpsRedirect: true # HTTP를 HTTPS로 리다이렉트
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: webapp-credential
    hosts:
    - "webapp.istioinaction.io"
```
- HTTP 요청을 HTTPS로 자동 리다이렉트

```bash
kubectl apply -f ch4/coolstore-gw-tls-redirect.yaml

# HTTP 301 리다이렉트
curl -v http://webapp.istioinaction.io:30000/api/catalog
```
![]({{ site.url }}/img/post/devops/study/istio/2/2025-04-19-5.png)

### MUTUAL TLS
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: coolstore-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - "webapp.istioinaction.io"
  - port:
      number: 443
      name: https
      protocol: HTTPS
    tls:
      mode: MUTUAL # 상호 TLS 설정
      credentialName: webapp-credential-mtls # 신뢰할 수 있는 CA가 구성된 자격 증명
    hosts:
    - "webapp.istioinaction.io"
```
- 클라이언트 인증서 검증까지 수행
- 인증서 + 키 + CA 체인 모두 secret에 등록

```bash
# 인증서 파일들 확인
cat ch4/certs/3_application/private/webapp.istioinaction.io.key.pem
cat ch4/certs/3_application/certs/webapp.istioinaction.io.cert.pem
cat ch4/certs/2_intermediate/certs/ca-chain.cert.pem
openssl x509 -in ch4/certs/2_intermediate/certs/ca-chain.cert.pem -noout -text

# Secret 생성 : (적절한 CA 인증서 체인) 클라이언트 인증서
kubectl create -n istio-system secret \
generic webapp-credential-mtls --from-file=tls.key=\
ch4/certs/3_application/private/webapp.istioinaction.io.key.pem \
--from-file=tls.crt=\
ch4/certs/3_application/certs/webapp.istioinaction.io.cert.pem \
--from-file=ca.crt=\
ch4/certs/2_intermediate/certs/ca-chain.cert.pem

# 확인
kubectl view-secret -n istio-system webapp-credential-mtls --all

# 이제 CA 인증서 체인의 위치를 가리키도록 이스티오 Gateway 리소스를 업데이트하고,
# expected 프로토콜을 mTLS로 구성
kubectl apply -f ch4/coolstore-gw-mtls.yaml -n istioinaction

# (옵션) SDS 로그 확인
kubectl stern -n istio-system -l app=istiod
...

docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/istio-ingressgateway.istio-system
...

# 호출 테스트 1 : (호출실패) 클라이언트 인증서 없음 - SSL 핸드섀이크가 성공하지 못하여 거부됨
curl -v https://webapp.istioinaction.io:30005/api/catalog \
--cacert ch4/certs/2_intermediate/certs/ca-chain.cert.pem

# 웹브라우저에서 확인 시 클라이언트 인증서 확인되지 않아서 접속 실패 확인
open https://webapp.istioinaction.io:30005
open https://webapp.istioinaction.io:30005/api/catalog
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419172043.png)
![]({{ site.url }}/img/post/devops/study/istio/2/20250419172059.png)

```bash
# 호출 테스트 2 : 클라이언트 인증서/키 추가 성공!
curl -v https://webapp.istioinaction.io:30005/api/catalog \
--cacert ch4/certs/2_intermediate/certs/ca-chain.cert.pem \
--cert ch4/certs/4_client/certs/webapp.istioinaction.io.cert.pem \
--key ch4/certs/4_client/private/webapp.istioinaction.io.key.pem

# 이스티오 게이트웨이는 istio-proxy를 시작하는데 사용하는 istio-agent 프로세스에 내장된 SDS에서 인증서를 가져온다.
# SDS는 업데이트를 자동으로 전파해야 하는 동적 API이다.

```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419172155.png)

### MULTI TLS
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: coolstore-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 443  # 첫 번째 항목
      name: https-webapp
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: webapp-credential
    hosts:
    - "webapp.istioinaction.io"
  - port:
      number: 443  # 두 번째 항목
      name: https-catalog
      protocol: HTTPS
    tls:
      mode: SIMPLE
      credentialName: catalog-credential
    hosts:
    - "catalog.istioinaction.io"
```
- 동일 포트(443)에서 SNI로 인증서 스위칭 가능
- 여러 호스트를 각각 다른 인증서로 처리 가능

```bash
# 각 항목에는 서빙하는 가상 호스트용으로 사용하는 고유한 인증서와 키가 있다.
cat ch4/certs2/3_application/private/catalog.istioinaction.io.key.pem
cat ch4/certs2/3_application/certs/catalog.istioinaction.io.cert.pem
openssl x509 -in ch4/certs2/3_application/certs/catalog.istioinaction.io.cert.pem -noout -text
...
        Issuer: C=US, ST=Denial, O=Dis, CN=catalog.istioinaction.io
        Validity
            Not Before: Jul  4 13:30:38 2021 GMT
            Not After : Jun 29 13:30:38 2041 GMT
        Subject: C=US, ST=Denial, L=Springfield, O=Dis, CN=catalog.istioinaction.io
...

kubectl create -n istio-system secret tls catalog-credential \
--key ch4/certs2/3_application/private/catalog.istioinaction.io.key.pem \
--cert ch4/certs2/3_application/certs/catalog.istioinaction.io.cert.pem

# Gateway 설정 업데이트
kubectl apply -f ch4/coolstore-gw-multi-tls.yaml -n istioinaction


# Gateway 로 노출한 catalog 서비스용 VirtualService 리소스 생성
cat ch4/catalog-vs.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog-vs-from-gw
spec:
  hosts:
  - "catalog.istioinaction.io"
  gateways:
  - coolstore-gateway
  http:
  - route:
    - destination:
        host: catalog
        port:
          number: 80

kubectl apply -f ch4/catalog-vs.yaml -n istioinaction
kubectl get gw,vs -n istioinaction

# 도메인 질의를 위한 임시 설정 : 실습 완료 후에는 삭제 해둘 것
echo "127.0.0.1       catalog.istioinaction.io" | sudo tee -a /etc/hosts
cat /etc/hosts | tail -n 2

# 호출테스트 1 - webapp.istioinaction.io
curl -v https://webapp.istioinaction.io:30005/api/catalog \
--cacert ch4/certs/2_intermediate/certs/ca-chain.cert.pem

# 호출테스트 2 - catalog.istioinaction.io (cacert 경로가 ch4/certs2/* 임에 유의)
curl -v https://catalog.istioinaction.io:30005/items \
--cacert ch4/certs2/2_intermediate/certs/ca-chain.cert.pem
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419172502.png)

## **TCP 트래픽 수용**
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: echo-tcp-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 31400 # 노출할 포트
      name: tcp-echo
      protocol: TCP # 기대하는 프로토콜
    hosts:
    - "*" # 모든 호스트
```
- TCP 기반 서비스도 라우팅 가능
- 단, L7 기능들(재시도, 타임아웃 등)은 불가

```bash
kubectl apply -f ch4/echo.yaml -n istioinaction 

kubectl get pod -n istioinaction 

# tcp 서빙 포트 추가 : 편집기는 vi 대신 nano 선택 <- 편한 툴 사용
kubectl edit svc istio-ingressgateway -n istio-system
...
  - name: tcp
    nodePort: 30006
    port: 31400
    protocol: TCP
    targetPort: 31400
...

# 확인
kubectl get svc istio-ingressgateway -n istio-system -o jsonpath='{.spec.ports[?(@.name=="tcp")]}'

# 게이트웨이 생성
cat ch4/gateway-tcp.yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: echo-tcp-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 31400
      name: tcp-echo
      protocol: TCP
    hosts:
    - "*"
    
kubectl apply -f ch4/gateway-tcp.yaml -n istioinaction
kubectl get gw -n istioinaction

# 에코 서비스로 라우팅하기 위해 VirtualService 리소스 생성
cat ch4/echo-vs.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: tcp-echo-vs-from-gw
spec:
  hosts:
  - "*"
  gateways:
  - echo-tcp-gateway
  tcp:
  - match:
    - port: 31400
    route:
    - destination:
        host: tcp-echo-service
        port:
          number: 2701

kubectl apply -f ch4/echo-vs.yaml -n istioinaction
kubectl get vs -n istioinaction

brew install telnet

telnet localhost 30006
...
hello istio! # <-- type here
hello istio! # <-- echo here

# telnet 종료하기 : 세션종료 Ctrl + ] > 텔넷 종료 quit
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419174415.png)

## SNI Passthrough
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: sni-passthrough-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - port:
      number: 31400 # HTTP 포트라 아닌 특정 포트 열기
      name: tcp-sni
      protocol: TLS
    hosts:
    - "simple-sni-1.istioinaction.io" # 이 호스트를 포트와 연결
    tls:
      mode: PASSTHROUGH # 통과 트래픽으로 처리
```
- TLS 종료 없이 단순 라우팅
- SNI 정보 기반 라우팅만 수행

```bash
# TLS를 종료하는 애플리케이션 배포
# TLS 인증을 직접 처리하는 앱 배포. (gw는 route 만 처리, pass through )
cat ch4/sni/simple-tls-service-1.yaml
kubectl apply -f ch4/sni/simple-tls-service-1.yaml -n istioinaction
kubectl get pod -n istioinaction

# 기존 Gateway 명세(echo-tcp-gateway) 제거 : istio-ingressgateway의 동일한 port (31400, TCP)를 사용하므로 제거함
kubectl delete gateway echo-tcp-gateway -n istioinaction

# 신규 Gateway 설정
kubectl apply -f ch4/sni/passthrough-sni-gateway.yaml -n istioinaction
kubectl get gw -n istioinaction

# VirtualService 리소스 라우팅 규칙 지정
# 
kubectl apply -f ch4/sni/passthrough-sni-vs-1.yaml -n istioinaction
kubectl get vs -n istioinaction


# 호출테스트1
echo "127.0.0.1       simple-sni-1.istioinaction.io" | sudo tee -a /etc/hosts

curl https://simple-sni-1.istioinaction.io:30006/ \
 --cacert ch4/sni/simple-sni-1/2_intermediate/certs/ca-chain.cert.pem
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419175011.png)

```bash
# 라우팅을 더 명확하게 하기 위해 인증서가 다르고 SNI 호스트에 기반해 라우팅을 하는 두 번째 서비스 배포
# 두 번째 서비스 배포
cat ch4/sni/simple-tls-service-2.yaml
kubectl apply -f ch4/sni/simple-tls-service-2.yaml -n istioinaction

# gateway 설정 업데이트
cat ch4/sni/passthrough-sni-gateway-both.yaml
kubectl apply -f ch4/sni/passthrough-sni-gateway-both.yaml -n istioinaction

# VirtualService 설정
cat ch4/sni/passthrough-sni-vs-2.yaml
kubectl apply -f ch4/sni/passthrough-sni-vs-2.yaml -n istioinaction

# 호출테스트2
echo "127.0.0.1       simple-sni-2.istioinaction.io" | sudo tee -a /etc/hosts

curl https://simple-sni-2.istioinaction.io:30006 \
--cacert ch4/sni/simple-sni-2/2_intermediate/certs/ca-chain.cert.pem

```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419175153.png)

## 운영 전략
### 게이트웨이 다중 구성
- 인그레스/이그레스를 분리
- 팀별, 도메인별, 보안 레벨별 게이트웨이 분할 가능
![]({{ site.url }}/img/post/devops/study/istio/2/20250411205252.png)

```bash
docker exec -it myk8s-control-plane bash
------------------------------------------
# istioinaction 네임스페이스에 Ingress gateway 설치
cat <<EOF > my-user-gateway-edited.yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: my-user-gateway-install
  namespace: istioinaction
spec:
  profile: empty
  values:
    gateways:
      istio-ingressgateway:
        autoscaleEnabled: false
  components:
    ingressGateways:
    - name: istio-ingressgateway
      enabled: false    
    - name: my-user-gateway
      namespace: istioinaction
      enabled: true
      label:
        istio: my-user-gateway
      k8s:
        service:
          ports:
            - name: tcp  # my-user-gateway 에서 사용할 포트 설정
              port: 31400
              targetPort: 31400
              nodePort: 30007 # 외부 접속을 위해 NodePort Number 직접 설정
EOF

# istioctl manifest generate -n istioinaction -f my-user-gateway-edited.yaml
istioctl install -y -n istioinaction -f my-user-gateway-edited.yaml

exit
------------------------------------------

# IstioOperator 확인
kubectl get IstioOperator -A

kubectl get deploy my-user-gateway -n istioinaction

# 포트 확인
kubectl get svc my-user-gateway -n istioinaction -o yaml
...
  - name: tcp
    nodePort: 30007
    port: 31400
    protocol: TCP
    targetPort: 31400
...

# my-user-gateway를 경우하여 TCP 통신
# Gateway
cat <<EOF | kubectl apply -n istioinaction -f -
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: echo-tcp-gateway
spec:
  selector:
    istio: my-user-gateway  #  New gateway
  servers:
  - port:
      number: 31400
      name: tcp-echo
      protocol: TCP
    hosts:
    - "*"
EOF

# VirtualService 명세
cat ch4/echo-vs.yaml
kubectl apply -f ch4/echo-vs.yaml -n istioinaction

# 앱 배포
cat ch4/echo.yaml
kubectl apply -f ch4/echo.yaml -n istioinaction

# 호출 테스트 : NodePort 30007로 접속 테스트
telnet localhost 30007
Trying ::1...
Connected to localhost.
Escape character is '^]'.
..
Service default.
hello Istio    # <-- type here
hello Istio    # <-- echo here

# telnet 종료하기 : 세션종료 Ctrl + ] > 텔넷 종료 quit
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419175858.png)

### 게이트웨이 주입 (Injection)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-user-gateway-injected
  namespace: istioinaction
spec:
  selector:
    matchLabels:
      ingress: my-user-gateway-injected
  template:
    metadata:
      annotations:
        sidecar.istio.io/inject: "true" # 주입 활성화
        inject.istio.io/templates: gateway # gateway 템플릿 사용
      labels:
        ingress: my-user-gateway-injected
    spec:
      containers:
      - name: istio-proxy # 반드시 이 이름이어야 한다.
        image: auto # 미완성 이미지
```
- 사용자가 IstioOperator 없이도 Deployment 형태로 게이트웨이 구성 가능

```bash
kubectl apply -f ch4/my-user-gw-injection.yaml

kubectl get deploy,svc,ep my-user-gateway-injected -n istioinaction
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419180001.png)

### 액세스 로그 설정
```yaml
apiVersion: telemetry.istio.io/v1alpha1
kind: Telemetry
metadata:
  name: ingress-gateway
  namespace: istio-system
spec:
  selector:
    matchLabels:
      app: istio-ingressgateway # 레이블과 일치하는 파드는 텔레메트리 설정을 가져온다.
  accessLogging:
  - providers:
    - name: envoy  # 액세스 로그를 위한 프로바이더 설정
    disabled: false # disabled를 false로 설정해 활성화
```
- 로그는 default로 꺼져 있음
- 텔레메트리 리소스로 선택적 활성화

```bash
# 액세스 로그를 보려면 컨테이너 로그를 출력하기만 하면 된다.
kubectl logs -f deploy/istio-ingressgateway -n istio-system

# 반복 호출
watch -d -n 1 curl -s -v https://webapp.istioinaction.io:30005/api/catalog --cacert ch4/certs/2_intermediate/certs/ca-chain.cert.pem

# 애플리케이션 컨테이너는 실시간 로그 출력
kubectl stern -n istioinaction -l app=webapp -c webapp
webapp-7685bcb84-h5knf webapp 2025/04/14 09:28:40.248 [M] [router.go:1014]  172.18.0.1 - - [14/Apr/2025 09:28:40] "GET /api/catalog HTTP/1.1 200 0" 0.004840  curl/8.7.1
...

# 초기 부팅 로그 이외에 별다른 로그 출력이 없음
kubectl stern -n istioinaction -l app=webapp -c istio-proxy
...
```
![]({{ site.url }}/img/post/devops/study/istio/2/20250419180408.png)

```bash
# 표준 출력 스트림으로 출력하도록 accessLogFile 속성을 변경할 수 있다.
kubectl get cm -n istio-system istio -o yaml
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
..

#
docker exec -it myk8s-control-plane bash
------------------------------------------
# 표준 출력 스트림으로 출력하도록 accessLogFile 속성을 변경
istioctl install --set meshConfig.accessLogFile=/dev/stdout
y 입력

exit
------------------------------------------

# configmap 에 mesh 바로 아래에 accessLogFile 부분 추가됨
kubectl get cm -n istio-system istio -o yaml
...
  mesh: |-
    accessLogFile: /dev/stdout
...

# 애플리케이션 호출에 대한 로그도 출력됨!
kubectl stern -n istioinaction -l app=webapp -c istio-proxy
...
```
![]({{ site.url }}/img/post/devops/study/istio/2/2025-04-19-06.png)

### 설정 최적화
```yaml
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  name: control-plane
spec:
  profile: minimal
  components:
    pilot:
      k8s:
        env:
        - name: PILOT_FILTER_GATEWAY_CLUSTER_CONFIG
          value: "true"
  meshConfig:
    defaultConfig:
      proxyMetadata:
        ISTIO_META_DNS_CAPTURE: "true"
    enablePrometheusMerge: true
```
- 게이트웨이가 사용하지 않는 서비스 설정 제외
- 설정 사이즈 감소 및 성능 개선

```bash
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/my-user-gateway.istioinaction

SERVICE FQDN                                                 PORT      SUBSET     DIRECTION     TYPE           DESTINATION RULE
BlackHoleCluster                                             -         -          -             STATIC
agent                                                        -         -          -             STATIC
catalog.istioinaction.svc.cluster.local                      80        -          outbound      EDS
...

# 현재 37개 cluster 정보
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/my-user-gateway.istioinaction | wc -l
      37
      
# 아래 추가
kubectl edit IstioOperator -n istioinaction installed-state-my-user-gateway-install
...
    pilot:
      enabled: false
      k8s:
        env:
        - name: PILOT_FILTER_GATEWAY_CLUSTER_CONFIG
          value: "true"
...

# 동일... 해당 gw pod 삭제 후 재시작 되어도 동일.. 다른 설정 방법이 있나?... kubectl edit 대신 IstioOperator 로 설정해야할지도..
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/my-user-gateway.istioinaction | wc -l
      37
```
![]({{ site.url }}/img/post/devops/study/istio/2/2025-04-19-7.png)

---

### 실습 후 정리
- `kind delete cluster --name myk8s`
- `/etc/hosts` 파일에서 도메인 삭제

---

# 도전 과제
- [도전과제1] Envoy 공식문서에 **Quick start** 전체 내용을 실습 및 정리 - [Docs](https://www.envoyproxy.io/docs/envoy/latest/start/quick-start/)
- [도전과제2] Envoy 공식문서에 **Sandboxes** 내용을 실습 및 정리 - [Docs](https://www.envoyproxy.io/docs/envoy/latest/start/sandboxes/)
- [도전과제3] solo academy 에 **Get Started with Envoy Proxy** 온라인 실습 렙 정리 - [Link](https://academy.solo.io/learn/courses/7/get-started-with-envoy-proxy)
- [도전과제4] **Istio** ingress 이외에 **egress-gateway** 를 추가 배포해보고, 외부에서 서비스 메시 내부 app 접속 후 리턴까지 E2E 호출 경로 확인    
- [도전과제5] Istio **v1.17 공식 문서**에 **Ingress** 에 각 기능과 **실습 시나리오**를 직접 테스트 후 정리 - [Docs](https://istio.io/v1.17/docs/tasks/traffic-management/ingress/)
- [도전과제6] k8s / istio **최신 버전** 설치 후 Istio API 대신 **k8s Gateway API** 를 이용하여 위 실습 시나리오를 구성해보기
