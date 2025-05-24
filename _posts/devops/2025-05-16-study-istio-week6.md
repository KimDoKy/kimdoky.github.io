---
layout: post
section-type: post
title: ServiceMesh - Istio - Week6
category: devops
tags: ["k8s", "istio", "servicemesh"]
---

# chap10. 데이터 플레인 트러블 슈팅하기
- 요청 처리 구성요소
	- istiod: 데이터 플레인과 desired state 동기화
	- Ingress Gateway: 트래픽 허용
	- Service Proxy: 트래픽 처리 및 접근 제어
	- Application: 요청 처리 및 체인 연결

![]({{ site.url }}/img/post/devops/study/istio/6/20250502234748.png)

## 가장 흔한 실수: 잘못 설정한 데이터 플레인
- 문제 시나리오
	- VirtualService는 정의했지만, DestinationRule 없이 Subset으로 라우팅
	- -> 503 오류 발생

![]({{ site.url }}/img/post/devops/study/istio/6/20250502235231.png)

```bash
# 샘플 애플리케이션 배포
kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction # catalog v1 배포
kubectl apply -f ch10/catalog-deployment-v2.yaml -n istioinaction # catalog v2 배포
kubectl apply -f ch10/catalog-gateway.yaml -n istioinaction # catalog-gateway 배포
kubectl apply -f ch10/catalog-virtualservice-subsets-v1-v2.yaml -n istioinaction

# Gateway 
cat ch10/catalog-gateway.yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: catalog-gateway
  namespace: istioinaction
spec:
  selector:
    istio: ingressgateway
  servers:
  - hosts:
    - "catalog.istioinaction.io"
    port:
      number: 80
      name: http
      protocol: HTTP

# VirtualService
cat ch10/catalog-virtualservice-subsets-v1-v2.yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: catalog-v1-v2
  namespace: istioinaction
spec:
  hosts:
  - "catalog.istioinaction.io"
  gateways:
  - "catalog-gateway"
  http:
  - route:
    - destination:
        host: catalog.istioinaction.svc.cluster.local
        subset: version-v1
        port:
          number: 80
      weight: 20
    - destination:
        host: catalog.istioinaction.svc.cluster.local
        subset: version-v2
        port:
          number: 80
      weight: 80

# 확인
kubectl get deploy,svc -n istioinaction
kubectl get gw,vs -n istioinaction 
```

- 통신 확인
	- subset 설정 누락으로 503 Error.

```bash
# 로그 확인 : NC - NoClusterFound : Upstream cluster not found.
kubectl logs -n istio-system -l app=istio-ingressgateway -f

# 반복 호출 시도
for i in {1..100}; do curl http://catalog.istioinaction.io:30000/items -w "\nStatus Code %{http_code}\n"; sleep .5;  done
```

## 데이터 플레인 문제 식별하기

### 데이터 플레인이 최신 상태인지 확인하는 방법
- 컨트롤 플레인 동기화 확인 우선

![]({{ site.url }}/img/post/devops/study/istio/6/20250504130743.png)

- istioctl proxy-status
	- SYNCED: 정상 동기화
	- NOTSENT: 보낼 게 없음
	- STALE: 커넥션/성능 문제 가능성

```bash
docker exec -it myk8s-control-plane istioctl proxy-status
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250513224042.png)

### 키알리로 잘못된 설정 발견하기

- 대시보드 접근

```bash
istioctl dashboard kiali
```

- 경고 예시: `KIA1107 Subset not found`
	- Kiali 문서에서 오류 코드로 해결 방안 확인 가능

![]({{ site.url }}/img/post/devops/study/istio/6/20250514203603.png)
![]({{ site.url }}/img/post/devops/study/istio/6/20250514203708.png)
![]({{ site.url }}/img/post/devops/study/istio/6/20250514203819.png)

### istioctl 로 잘못된 설정 발견하기
#### istioctl로 이스티오 설정 분석하기
- `analyze`로 설정 검증
	- 클러스터에 적용하기 전에 설정이 유효한지 검사

```bash
istioctl analyze -n istioinaction
```

```bash
docker exec -it myk8s-control-plane istioctl analyze -h
docker exec -it myk8s-control-plane istioctl analyze --list-analyzers
...
docker exec -it myk8s-control-plane istioctl analyze -n istioinaction

# 이전 명령어 종료 코드 확인
## 이걸 활용해서 CI/CD에서 활용할 수도 있음
echo $? # (참고) 0 성공
79
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250514215510.png)
[Istio Configuration Analysis Message](https://istio.io/v1.17/docs/reference/config/analysis/)

![]({{ site.url }}/img/post/devops/study/istio/6/20250514215700.png)

#### 워크로드별로 설정 오류 찾기
- `describe`로 워크로드 상세 확인

```bash
istioctl x describe pod catalog-xxx-xxx
```

```bash
kubectl get pod -n istioinaction -l app=catalog -o jsonpath='{.items[0].metadata.name}'
CATALOG_POD1=$(kubectl get pod -n istioinaction -l app=catalog -o jsonpath='{.items[0].metadata.name}')

# 단축키 : experimental(x), describe(des)
docker exec -it myk8s-control-plane istioctl experimental describe -h
docker exec -it myk8s-control-plane istioctl x des pod -n istioinaction $CATALOG_POD1

# 문제 해결 후 확인
cat ch10/catalog-destinationrule-v1-v2.yaml       
kubectl apply -f ch10/catalog-destinationrule-v1-v2.yaml
docker exec -it myk8s-control-plane istioctl x des pod -n istioinaction $CATALOG_POD1

# 다음 점검 방법을 위해 오류 상황으로 원복
kubectl delete -f ch10/catalog-destinationrule-v1-v2.yaml
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250514220716.png)

## 엔보이 설정에서 수동으로 잘못된 설정 발견하기

### 엔보이 관리 인터페이스
```bash
kubectl port-forward deploy/catalog -n istioinaction 15000:15000
open http://localhost:15000

# 현재 적재한 엔보이 설정 출력 : 데이터양이 많다!
curl -s localhost:15000/config_dump | wc -l
  12377
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250514222305.png)

### istioctl로 프록시 설정 쿼리하기
- xDS API 기반 설정 쿼리
	- listeners, routes, clusters, endpoints, secrets

#### 요청을 라우팅하기 위한 엔보이 API의 상호작용
![]({{ site.url }}/img/post/devops/study/istio/6/20250504130945.png)
- Envoy Listener
	- 네트워크 설정(다운스트림 트래픽을 프록시로 허용하는 IP주소, 포트)를 정의
- Envoy Routes
	- 가상 호스트를 클러스터에 일치시키는 규칙 집합
		- 일치하는 첫 번째 항목이 트래픽을 워크로드 클러스터로 라우팅하는데 사용됨
		- 이스티오에서는 RDS를 사용해 동적으로 설정함
- Envoy Clusters
	- 각 클러스터에는 유사한 워크로드에 대한 엔드포인트 그룹이 있다.
	- Cluster Subset은 클러스터 내에서 워크로드를 더 분할(정밀한 트래픽 관리)
- Envoy Endpoints
	- 요청을 처리하는 워크로드의 IP 주소

#### 엔보이 리스너 설정 쿼리하기
```bash
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway -n istio-system

kubectl get svc -n istio-system  istio-ingressgateway -o yaml | grep "ports:" -A10
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250514223803.png)

#### 엔보이 Route 설정 쿼리하기
- Envoy Route 설정
	- 트래픽을 라우팅할 클러스터를 결정하는 규칙 집합을 정의
- Envoy Route를 VirtualService로 설정함
- Cluster는 디스커버리로 자동 설정 / DestinationRule로 정의됨

```bash
# http.8080 루트의 트래픽을 어느 클러스터로 라우팅할지 알아내기 위해 설정을 쿼리
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway -n istio-system --name http.8080

## 호스트 catalog.istioinaction.io 의 트래픽 중 URL이 경로 접두사 /*과 일치하는 것이 istioinaction 네임스페이스의 catalog 서비스에 있는 catalog VirtualService 로 라우팅됨을 보여준다.

# 세부 정보 확인
docker exec -it myk8s-control-plane istioctl proxy-config routes deploy/istio-ingressgateway -n istio-system --name http.8080 -o json
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250514225058.png)
- **라우팅 대상 클러스터 예시**
	- `outbound|80|version-v2|...`
    - `outbound|80|version-v1|...`

#### 엔보이 클러스터 설정 쿼리하기
- Envoy Cluster 설정
	- 요청을 라우팅할 수 있는 백엔드 서비스를 정의
	- Cluster는 부하를 여러 인스턴스나 엔드포인트에 분산
	- 이 엔드포인트는 최종 사용자 트래픽을 처리하는 개별 워크로드 인스턴스

- 클러스터 이름을 구분하는 구성 요소

![]({{ site.url }}/img/post/devops/study/istio/6/20250504131401.png)

```bash
docker exec -it myk8s-control-plane istioctl proxy-config clusters deploy/istio-ingressgateway -n istio-system \
--fqdn catalog.istioinaction.svc.cluster.local --port 80

docker exec -it myk8s-control-plane istioctl proxy-config clusters deploy/istio-ingressgateway -n istio-system \
--fqdn catalog.istioinaction.svc.cluster.local --port 80 --subset version-v1
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250514230036.png)
```bash
# 해당 파일이 없을 경우 'copy & paste'로 작성 후 진행 하자
docker exec -it myk8s-control-plane cat /istiobook/ch10/catalog-destinationrule-v1-v2.yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: catalog
  namespace: istioinaction
spec:
  host: catalog.istioinaction.svc.cluster.local
  subsets:
  - name: version-v1
    labels:
      version: v1
  - name: version-v2
    labels:
      version: v2

# istioctl analyze 명령어를 사용해서, 설정할 yaml 파일이 식별한 서비스 메시 오류를 고칠 수 있는지 확인
docker exec -it myk8s-control-plane istioctl analyze /istiobook/ch10/catalog-destinationrule-v1-v2.yaml -n istioinaction

✔ No validation issues found when analyzing /istiobook/ch10/catalog-destinationrule-v1-v2.yaml.
```

```bash
# 문제 해결
cat ch10/catalog-destinationrule-v1-v2.yaml
kubectl apply -f ch10/catalog-destinationrule-v1-v2.yaml

# 확인
docker exec -it myk8s-control-plane istioctl proxy-config clusters deploy/istio-ingressgateway -n istio-system \
--fqdn catalog.istioinaction.svc.cluster.local --port 80

CATALOG_POD1=$(kubectl get pod -n istioinaction -l app=catalog -o jsonpath='{.items[0].metadata.name}')
docker exec -it myk8s-control-plane istioctl x des pod -n istioinaction $CATALOG_POD1
docker exec -it myk8s-control-plane istioctl analyze -n istioinaction

# 호출 확인
curl http://catalog.istioinaction.io:30000/items
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250514230522.png)

#### 클러스터는 어떻게 설정되는가?
```bash
docker exec -it myk8s-control-plane istioctl proxy-config clusters deploy/istio-ingressgateway -n istio-system \
--fqdn catalog.istioinaction.svc.cluster.local --port 80 --subset version-v1 -o json
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250514230934.png)

#### 엔보이 클러스터 엔드포인트 쿼리하기
- Ingress Gateway에서 Cluster의 Endpoints를 `istioctl proxy-config endpoints`으로 수동으로 쿼리

```bash
# 엔드포인트 정보 확인 : IP 정보
docker exec -it myk8s-control-plane istioctl proxy-config endpoints deploy/istio-ingressgateway -n istio-system \
--cluster "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local"

# 해당 IP 쿼리로 실제 워크로드가 있는지 확인
kubectl get pod -n istioinaction --field-selector status.podIP=10.10.0.13 -owide --show-labels
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250514231318.png)

### 애플리케이션 문제 트러블슈팅하기
- 서비스 프록시가 생성하는 로그와 메트릭은 성능 병목을 일으키는 문제들의 트러블 슈팅에 도움이 된다.
	- 성능 병목을 일으키는 서비스 디스커버리
	- 빈번하게 실패하는 엔드포인트 식별
	- 성능 저하 감지 등

#### 간혈적으로 제한시간을 초과하는 느린 워크로드 준비하기

```bash
# 신규 터미널
for in in {1..9999}; do curl http://catalog.istioinaction.io:30000/items -w "\nStatus Code %{http_code}\n"; sleep 1; done
```

![]({{ site.url }}/img/post/devops/study/istio/6/20250515193450.png)

![]({{ site.url }}/img/post/devops/study/istio/6/20250515193727.png)
![]({{ site.url }}/img/post/devops/study/istio/6/20250515193947.png)

- Grafana - Istio Mesh Dashboard

![]({{ site.url }}/img/post/devops/study/istio/6/20250515192900.png)

- catalog 워크로드가 간혈적으로 응답을 느리게 반환하도록 설정

```bash
# catalog v2 파드 중 첫 번째 파드 이름 변수 지정
CATALOG_POD=$(kubectl get pods -l version=v2 -n istioinaction -o jsonpath={.items..metadata.name} | cut -d ' ' -f1)
echo $CATALOG_POD
catalog-v2-56c97f6db-fcrhr

# 해당 파드에 latency (지연) 발생하도록 설정
kubectl -n istioinaction exec -c catalog $CATALOG_POD \
-- curl -s -X POST -H "Content-Type: application/json" \
-d '{"active": true, "type": "latency", "volatile": true}' \
localhost:3000/blowup ;
blowups=[object Object]

# 신규 터미널
for in in {1..9999}; do curl http://catalog.istioinaction.io:30000/items -w "\nStatus Code %{http_code}\n"; sleep 1; done
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250515194502.png)
![]({{ site.url }}/img/post/devops/study/istio/6/20250515194713.png)

- Istio에 요청 처리 제한 시간을 0.5초로 VirtualService 설정

![]({{ site.url }}/img/post/devops/study/istio/6/20250504131657.png)

```bash
kubectl get vs -n istioinaction
NAME            GATEWAYS              HOSTS                          AGE
catalog-v1-v2   ["catalog-gateway"]   ["catalog.istioinaction.io"]   45h

# 타임아웃(0.5s) 적용
kubectl patch vs catalog-v1-v2 -n istioinaction --type json \
-p '[{"op": "add", "path": "/spec/http/0/timeout", "value": "0.5s"}]'

# 적용확인 
kubectl get vs catalog-v1-v2 -n istioinaction -o jsonpath='{.spec.http[?(@.timeout=="0.5s")]}' | jq
...
  "timeout": "0.5s"
}

# 신규 터미널
for in in {1..9999}; do curl http://catalog.istioinaction.io:30000/items -w "\nStatus Code %{http_code}\n"; sleep 1; done
upstream request timeout
Status Code 504
upstream request timeout
Status Code 504
..

#
kubectl logs -n istio-system -l app=istio-ingressgateway -f
[2025-05-15T20:00:21.626Z] "GET /items HTTP/1.1" 504 UT response_timeout - "-" 0 24 501 - "172.18.0.1" "curl/8.7.1" "cb846eff-07ac-902e-9890-7af478c84166" "catalog.istioinaction.io:30000" "10.10.0.13:3000" outbound|80|version-v2|catalog.istioinaction.svc.cluster.local 10.10.0.7:58078 10.10.0.7:8080 172.18.0.1:61108 - -

kubectl logs -n istio-system -l app=istio-ingressgateway -f | grep 504

kubectl logs -n istioinaction -l version=v2 -c istio-proxy -f
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250515195653.png)
![]({{ site.url }}/img/post/devops/study/istio/6/20250515195736.png)
![]({{ site.url }}/img/post/devops/study/istio/6/20250515195826.png)

#### 엔보이 액세스 로그 이해하기
- 로그 포맷 커스터마이징
- 로깅 수준 조정(ex. `istioctl proxy-config log`)

#### 엔보이 엑세스 로그 형식 바꾸기
```bash
# 형식 설정 전 로그 확인
kubectl logs -n istio-system -l app=istio-ingressgateway -f | grep 504
...

# MeshConfig 설정 수정
kubectl edit -n istio-system cm istio
...
  mesh: |-
    accessLogFile: /dev/stdout # 기존 설정되어 있음
    accessLogEncoding: JSON # 추가
...

# 형식 설정 후 로그 확인
kubectl logs -n istio-system -l app=istio-ingressgateway -f | jq

# slow 동작되는 파드 IP로 느린 동작 파드 확인!
CATALOG_POD=$(kubectl get pods -l version=v2 -n istioinaction -o jsonpath={.items..metadata.name} | cut -d ' ' -f1)
kubectl get pod -n istioinaction $CATALOG_POD -owide
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250515212720.png)
![]({{ site.url }}/img/post/devops/study/istio/6/20250515213011.png)

#### 인그레스 게이트웨이의 로깅 수준 높이기

```bash
# 현재 로깅 수준 확인
docker exec -it myk8s-control-plane istioctl proxy-config log deploy/istio-ingressgateway -n istio-system
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250515213537.png)

- 로깅 수준
	- none, error, warning, info, debug
- 각 범위에 로깅 수준을 다르게 지정할 수 있다.
	- 집중하고 싶은 영역의 로깅 수준만 높일 수 있다.

```bash
# connection, http, router, pod 로거의 수준은 debug로 높이자.
docker exec -it myk8s-control-plane istioctl proxy-config log deploy/istio-ingressgateway -n istio-system \
--level http:debug,router:debug,connection:debug,pool:debug

# 로그 확인
kubectl logs -n istio-system -l app=istio-ingressgateway -f
# 편집기로 열어서 보기
k logs -n istio-system -l app=istio-ingressgateway -f > istio-igw-log.txt
```

```bash
# 504 검색
2025-05-15T12:38:51.021034Z	debug	envoy http external/envoy/source/common/http/filter_manager.cc:967	[C63517][S15112341109905330088] Sending local reply with details response_timeout	thread=40
2025-05-15T12:38:51.021094Z	debug	envoy http external/envoy/source/common/http/conn_manager_impl.cc:1687	[C63517][S15112341109905330088] encoding headers via codec (end_stream=false):
':status', '504'
'content-length', '24'
'content-type', 'text/plain'
'date', 'Thu, 15 May 2025 12:38:50 GMT'
'server', 'istio-envoy'
	thread=40

# 커넥션 ID(C63517)로 검색
2025-05-15T12:38:50.520048Z	debug	envoy http external/envoy/source/common/http/conn_manager_impl.cc:329	[C63517] new stream	thread=40
2025-05-15T12:38:50.520091Z	debug	envoy http external/envoy/source/common/http/conn_manager_impl.cc:1049	[C63517][S15112341109905330088] request headers complete (end_stream=true):
':authority', 'catalog.istioinaction.io:30000'
':path', '/items'
':method', 'GET'
'user-agent', 'curl/8.7.1'
'accept', '*/*'
	thread=40

# /items 요청이 cluster로 매칭됨
2025-05-15T12:38:50.520095Z	debug	envoy http external/envoy/source/common/http/conn_manager_impl.cc:1032	[C63517][S15112341109905330088] request end stream	thread=40
2025-05-15T12:38:50.520106Z	debug	envoy connection external/envoy/source/common/network/connection_impl.h:92	[C63517] current connecting state: false	thread=40
2025-05-15T12:38:50.520183Z	debug	envoy router external/envoy/source/common/router/router.cc:470	[C63517][S15112341109905330088] cluster 'outbound|80|version-v2|catalog.istioinaction.svc.cluster.local' match for URL '/items'	thread=40
2025-05-15T12:38:50.520219Z	debug	envoy router external/envoy/source/common/router/router.cc:678	[C63517][S15112341109905330088] router decoding headers:
':authority', 'catalog.istioinaction.io:30000'
':path', '/items'
':method', 'GET'
':scheme', 'http'
'user-agent', 'curl/8.7.1'
'accept', '*/*'
'x-forwarded-for', '192.168.65.1'
'x-forwarded-proto', 'http'
'x-envoy-internal', 'true'
'x-request-id', '6611c73c-d8ae-4175-b487-4c2ce30844b1'
'x-envoy-decorator-operation', 'catalog-v1-v2:80/*'
'x-envoy-peer-metadata', 'ChQKDkFQUF9DT05UQUlORVJTEgIaAAoaCgpDTFVTVEVSX0lEEgwaCkt1YmVybmV0ZXMKGwoMSU5TVEFOQ0VfSVBTEgsaCTEwLjEwLjAuNwoZCg1JU1RJT19WRVJTSU9OEggaBjEuMTcuOAqcAwoGTEFCRUxTEpEDKo4DCh0KA2FwcBIWGhRpc3Rpby1pbmdyZXNzZ2F0ZXdheQoTCgVjaGFydBIKGghnYXRld2F5cwoUCghoZXJpdGFnZRIIGgZUaWxsZXIKNgopaW5zdGFsbC5vcGVyYXRvci5pc3Rpby5pby9vd25pbmctcmVzb3VyY2USCRoHdW5rbm93bgoZCgVpc3RpbxIQGg5pbmdyZXNzZ2F0ZXdheQoZCgxpc3Rpby5pby9yZXYSCRoHZGVmYXVsdAowChtvcGVyYXRvci5pc3Rpby5pby9jb21wb25lbnQSERoPSW5ncmVzc0dhdGV3YXlzChIKB3JlbGVhc2USBxoFaXN0aW8KOQofc2VydmljZS5pc3Rpby5pby9jYW5vbmljYWwtbmFtZRIWGhRpc3Rpby1pbmdyZXNzZ2F0ZXdheQovCiNzZXJ2aWNlLmlzdGlvLmlvL2Nhbm9uaWNhbC1yZXZpc2lvbhIIGgZsYXRlc3QKIgoXc2lkZWNhci5pc3Rpby5pby9pbmplY3QSBxoFZmFsc2UKGgoHTUVTSF9JRBIPGg1jbHVzdGVyLmxvY2FsCi4KBE5BTUUSJhokaXN0aW8taW5ncmVzc2dhdGV3YXktOTk2YmM2YmI2LWdqa3YyChsKCU5BTUVTUEFDRRIOGgxpc3Rpby1zeXN0ZW0KXQoFT1dORVISVBpSa3ViZXJuZXRlczovL2FwaXMvYXBwcy92MS9uYW1lc3BhY2VzL2lzdGlvLXN5c3RlbS9kZXBsb3ltZW50cy9pc3Rpby1pbmdyZXNzZ2F0ZXdheQoXChFQTEFURk9STV9NRVRBREFUQRICKgAKJwoNV09SS0xPQURfTkFNRRIWGhRpc3Rpby1pbmdyZXNzZ2F0ZXdheQ=='
'x-envoy-peer-metadata-id', 'router~10.10.0.7~istio-ingressgateway-996bc6bb6-gjkv2.istio-system~istio-system.svc.cluster.local'
'x-envoy-expected-rq-timeout-ms', '500'
'x-envoy-attempt-count', '1'
	thread=40

# upstream timeout으로 client에서 끊음 (disconnect)
2025-05-15T12:38:49.502208Z	debug	envoy pool external/envoy/source/common/http/http1/conn_pool.cc:53	[C61444] response complete	thread=38
2025-05-15T12:38:49.502220Z	debug	envoy pool external/envoy/source/common/conn_pool/conn_pool_base.cc:215	[C61444] destroying stream: 0 remaining	thread=38
2025-05-15T12:38:49.503254Z	debug	envoy connection external/envoy/source/common/network/connection_impl.cc:656	[C63514] remote close	thread=38
2025-05-15T12:38:49.503266Z	debug	envoy connection external/envoy/source/common/network/connection_impl.cc:250	[C63514] closing socket: 0	thread=38
2025-05-15T12:38:49.733792Z	debug	envoy router external/envoy/source/common/router/router.cc:947	[C63512][S7686129311861908490] upstream timeout	thread=31
2025-05-15T12:38:49.733888Z	debug	envoy router external/envoy/source/common/router/upstream_request.cc:500	[C63512][S7686129311861908490] resetting pool request	thread=31
2025-05-15T12:38:49.733923Z	debug	envoy connection external/envoy/source/common/network/connection_impl.cc:139	[C63513] closing data_to_write=0 type=1	thread=31
2025-05-15T12:38:49.733928Z	debug	envoy connection external/envoy/source/common/network/connection_impl.cc:250	[C63513] closing socket: 1	thread=31
2025-05-15T12:38:49.734099Z	debug	envoy connection external/envoy/source/extensions/transport_sockets/tls/ssl_socket.cc:320	[C63513] SSL shutdown: rc=0thread=31
2025-05-15T12:38:49.734197Z	debug	envoy pool external/envoy/source/common/conn_pool/conn_pool_base.cc:484	[C63513] client disconnected, failure reason: 	thread=31
2025-05-15T12:38:49.734212Z	debug	envoy pool external/envoy/source/common/conn_pool/conn_pool_base.cc:454	invoking idle callbacks - is_draining_for_deletion_=false	thread=31

# 504 응답
2025-05-15T12:38:49.734280Z	debug	envoy http external/envoy/source/common/http/filter_manager.cc:967	[C63512][S7686129311861908490] Sending local reply with details response_timeout	thread=31
2025-05-15T12:38:49.734348Z	debug	envoy http external/envoy/source/common/http/conn_manager_impl.cc:1687	[C63512][S7686129311861908490] encoding headers via codec (end_stream=false):
':status', '504'
'content-length', '24'
'content-type', 'text/plain'
'date', 'Thu, 15 May 2025 12:38:49 GMT'
'server', 'istio-envoy'
	thread=31
2025-05-15T12:38:49.734773Z	debug	envoy pool external/envoy/source/common/conn_pool/conn_pool_base.cc:215	[C63513] destroying stream: 0 remaining	thread=31
2025-05-15T12:38:49.737354Z	debug	envoy connection external/envoy/source/common/network/connection_impl.cc:656	[C63512] remote close	thread=31
2025-05-15T12:38:49.737373Z	debug	envoy connection external/envoy/source/common/network/connection_impl.cc:250	[C63512] closing socket: 0	thread=31
```
- 응답이 느린 업스트림의 IP 주소가 액세스 로그에서 가져온 IP와 일치한다.
	- 오동작하는 인스턴스가 딱 하나라는 추리의 신빙성이 Up
- 로그 `[C63513] client disconnected`에 표시된 대로 클라이언트(프록시)는 업스트림 커넥션을 종료했다.
	- 업스트림 인스턴스가 제한 시간 설정을 초과해 클라이언트(프록시)가 요청을 종료했다는 시나리오와 일치
### ksniff로 네트워크 트래픽 검사
- ksniff: tcpdump를 사용해 파드의 네트워크 트래픽을 포착하고 이를 wireshark로 리다이렉트하는 kubectl 플러그인
- wireshark: 네트워크 패킷 분석 도구
#### krew, ksniff, wireshark 설치하기
```bash
# ksniff 설치
kubectl krew install sniff
```
#### 로컬호스트 인터페이스에서 네트워크 트래픽 검사하기
- 오작동하는 파드의 네트워크 트래픽 검사
	- 연결이 성공하면
		- ksniff는 tcpdump를 사용해 로컬호스트 네트워크 인터페이스에서 네트워크 트래픽을 포착하고 로컬 wireshark 인스턴스로 리다이렉션한다.

```bash
kubectl sniff -n istioinaction $CATALOG_POD -i lo

# 트래픽 생성
for in in {1..9999}; do curl http://catalog.istioinaction.io:30000/items -w "\nStatus Code %{http_code}\n"; sleep 1; done
```
- `http contains "GET /items"`
	- 경로 `/items`, GET 메서드인 HTTP 프로토콜 패킷만 표시
- TCP 스트림을 따라가면 TCP 커넥션 시작부터 취소된 시점까지 자세한 정보를 얻을 수 있음
- 첫 라인의 우클릭 -> Follow -> TCP Stream

![]({{ site.url }}/img/post/devops/study/istio/6/20250517003622.png)

![]({{ site.url }}/img/post/devops/study/istio/6/20250517004323.png)
![]({{ site.url }}/img/post/devops/study/istio/6/20250517004638.png)
- TCP 커넥션을 설정하기 위해 3-way handshake를 수행하였다.
	- `[SYN], [SYN, ACK], [ACK]`으로 확인
- 커넥션이 설정된 후, 요청이 성공적으로 처리되고 있다.
- 클라이언트에서 요청이 들어와 서버가 응답했지만, 반응하는데 0.5초 이상 소요되었다.
	- 509번 패킷(11.866..)과 579번 패킷(12.373..)의 시간 차이 확인
- 요청 처리 시간이 너무 길어져, 클라이언트가 FIN 플래그를 보내 TCP 커넥션 종료를 시작한다.
- 서버 측에서 이에 응답하고 커넥션이 종료된다.

#### TCP 제어 플래그
- Synchronization(SYN): 커넥션을 새로 수립하는데 사용
- Acknowledgement(ACK): 패킷 수신이 성공했음을 확인하는데 사용
- Finish(FIN): 커넥션 종료를 요청하는데 사용

## 엔보이 텔레메트리로 자신의 애플리케이션 이해하기
### 그라파나에서 실패한 요청 비율 찾기
- Grafana - Istio Service Dashboard -> Service(catalog.istioinaction.svc.cluster.local) / Reporter(source)

![]({{ site.url }}/img/post/devops/study/istio/6/20250517184307.png)
![]({{ site.url }}/img/post/devops/study/istio/6/20250517183721.png)

- 클라이언트 성공률은 요청중 79%로 21% 실패 -> Client 응답에 5xx가 21% 정도 존재
	- StatusCode 504(Gateway Timeout)로 표기되어 클라이언트측 실패율에 반영됨
- 서버 성공률은 100%. 즉, 서버 문제는 아님 -> Server 응답에는 5xx 없음
	- Envoy Proxy가 다운스트림 종료 요청에 대한 응답코드를 0으로 표시하며, 이는  5xx 응답이 아니라서 실패율에 포함되지 않는다.

![]({{ site.url }}/img/post/devops/study/istio/6/20250504134259.png)

### 프로메테우스를 사용해 영향받는 파드 쿼리하기
- Grafana로 정보가 부족하다면, 프로메테우스에 직접 쿼리할 수 있다.

```bash
sort_desc( # 가장 높은 값부터 내림차순 정렬
  sum( # irate 값들을 집계
    irate( #  요청 수 초당 증가율
      istio_requests_total {
        reporter="destination",   # 서버(destination) 측에서 보고한 메트릭만 필터링
        destination_service=~"catalog.istioinaction.svc.cluster.local",   # catalog 가 서버(destination)측인 메트릭만 필터링
        response_flags="DC"       # DC (다운스트림 커넥션 종료)로 끝난 메트릭만 필터링
      }[5m]
    )
  )by(response_code, pod, version) # 응답 코드(response_code), 대상 pod, 버전(version) 별로 분리 => sum.. 합산
)
```
- 위 쿼리 후 Graph 화면을 보자.
	- destination이 보고한 요청
	- destination 서비스가 catalog 인 요청
	- 응답 플래그가 DC(다운스트림 커넥션 종료)인 요청
		- 서버 입장에서는 응답하려는데, 클라이언트가 먼저 끊어 버린 것

```bash
# 쿼리1
istio_requests_total
istio_requests_total{reporter="destination", destination_service=~"catalog.istioinaction.svc.cluster.local"}
istio_requests_total{reporter="destination", destination_service=~"catalog.istioinaction.svc.cluster.local",response_flags="DC"}

# 쿼리2
istio_requests_total{reporter="destination", destination_service=~"catalog.istioinaction.svc.cluster.local",response_flags="DC"}[5m]
irate(istio_requests_total{reporter="destination", destination_service=~"catalog.istioinaction.svc.cluster.local",response_flags="DC"}[5m])
sum(irate(istio_requests_total{reporter="destination", destination_service=~"catalog.istioinaction.svc.cluster.local",response_flags="DC"}[5m]))

# 쿼리3
sum(irate(istio_requests_total{reporter="destination", destination_service=~"catalog.istioinaction.svc.cluster.local",response_flags="DC"}[5m])) by(response_code, pod, version)
sort_desc(sum(irate(istio_requests_total{reporter="destination", destination_service=~"catalog.istioinaction.svc.cluster.local",response_flags="DC"}[5m]))by(response_code, pod, version))

```
![]({{ site.url }}/img/post/devops/study/istio/6/20250517204622.png)

```bash
sort_desc(sum(irate(istio_requests_total{reporter="destination", destination_service=~"catalog.istioinaction.svc.cluster.local"}[5m]))by(response_code, pod, version))
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250517204938.png)

# chap11. 컨트롤 플레인 성능 튜닝하기
- 컨트롤 플레인의 성능에 영향을 미치는 요소들
- 컨트롤 플레인 최적화 방법 및 핵심 메트릭 이해

## 컨트롤 플레인의 주요 목표
- 서비스 메시의 **두뇌 역할** 수행
- API를 통해 서비스 프록시 설정
- 설정 지연 시 발생하는 **유령 워크로드 현상**
- 자동 복원 기능
	- 재시도
	- 이상값 감지

![]({{ site.url }}/img/post/devops/study/istio/6/20250504135136.png)

### 데이터 플레인 동기화 단계 이해하기

![]({{ site.url }}/img/post/devops/study/istio/6/20250504182827.png)
1. 들어오는 이벤트가 동기화 과정을 시작한다.
2. istiod의 DiscoveryServer 구성 요소가 이 이벤트들을 수신한다.
	- 성능을 향상시키기 위해, 푸시 대기열에 이벤트를 추가하는 작업을 일정 시간 미루고 그 동안의 후속 이벤트를 병합해 일괄 처리한다.
	- 이를 'debounce 한다'라고하는데, 디바운스는 시간은 잡아먹는 작업이 너무 자주 실행되는 것을 방지한다.
1. 지연 시간이 만료되면, DiscoveryServer가 병합된 이벤트를 푸시 대기열에 추가한다. 푸시 대기열은 처리 대기 중인 푸시 목록을 유지한다.
2. istiod 서버는 동시에 처리되는 푸시 요청 개수를 제한하는데, 이는 처리 중인 항목이 더 빨리 처리되도록 보장하고 CPU 시간이 작업 간 콘텐스트 스위칭에 낭비되는 것을 방지한다.
3. 처리된 항목은 엔보이 설정으로 변환돼 워크로드로 푸시된다.
###  성능을 결정짓는 요소
- 변경 속도
	- 빠를수록 처리량 증가
- 리소스 할당량
	- 부족 시 푸시 지연
- 워크로드 수
	- 많은수록 동시 처리량 요구
- 설정 크기
	- 클수록 CPU/네트워크 부담

![]({{ site.url }}/img/post/devops/study/istio/6/20250504184529.png)

## 컨트롤 플레인 모니터링하기

### 컨트롤 플레인의 4가지 황금신호

#### 지연시간: 데이터 플레인을 업데이트하는데 필요한 시간(푸시 완료까지 걸린 시간)
- 관련 메트릭
	- `pilot_proxy_convergence_time`
		- 프록시 푸시 요청이 대기열에 안착한 순간부터 워크로드에 배포되기까지 전체 과정의 지속 시간을 측정한다.
		- Grafana - Istio Control Plane Dashboard의 Proxy Push Time이라는 Pilot Push 정보 부분에 있다.
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517213949.png)
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517214232.png)
	- `pilot_proxy_queue_time`
		- 워커가 처리할 때까지 푸시 요청이 대기열에서 기다린 시간을 측정한다.
		- 푸시 대기열에서 상당한 시간이 걸리는 경우, istiod를 수직으로 확장해 동시 처리 능력을 높일 수 있다.
	- `pilot_xds_push_time`
		- 엔보이 설정을 워크로드로 푸시하는데 필요한 시간을 측정한다.
		- 시간이 늘어나면, 전송되는 데이터양 때문에 네트워크 대역푹이 과부하된 것
		- 설정 업데이트 크기와 프록시별 변화 빈도를 줄여서 상황을 개선한다.

![]({{ site.url }}/img/post/devops/study/istio/6/20250506100222.png)

```bash
pilot_proxy_convergence_time_bucket
# le="0.1": 0.1초 이하로 동기화 완료된 프록시가 10개
# le="1": 1초 이하로 완료된 프록시가 누적 20개
# le="+Inf": 모든 프록시 포함 → 누적 41개
...

pilot_proxy_convergence_time_bucket[1m]
rate(pilot_proxy_convergence_time_bucket[1m])
sum(rate(pilot_proxy_convergence_time_bucket[1m]))
sum(rate(pilot_proxy_convergence_time_bucket[1m])) by (le)

histogram_quantile(0.5, sum(rate(pilot_proxy_convergence_time_bucket[1m])) by (le))
histogram_quantile(0.9, sum(rate(pilot_proxy_convergence_time_bucket[1m])) by (le))
...
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250517214709.png)
- Grafana에 2개의 패널(메트릭)을 추가
	- dashboard 편집 설정
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517215355.png)
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517215433.png)
		- 뒤로 가기(Edit가 활성화됨)
	- 기존 Proxy Push Time 패널 복제
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517215626.png)
		- 추가(복제)된 패널 수정
            - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517221114.png)
	- Proxy Queue Time: PromQL - `pilot_proxy_queue_time`
		- `histogram_quantile(0.5, sum(rate(pilot_proxy_queue_time_bucket[1m])) by (le))`
		- `histogram_quantile(0.9, sum(rate(pilot_proxy_queue_time_bucket[1m])) by (le))`
		- `histogram_quantile(0.99, sum(rate(pilot_proxy_queue_time_bucket[1m])) by (le))`
		- `histogram_quantile(0.999, sum(rate(pilot_proxy_queue_time_bucket[1m])) by (le))`
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517221035.png)
	- xDS Push Time: PromQL - `pilot_xds-push_time_bucket`
		- `histogram_quantile(0.5, sum(rate(pilot_xds_push_time_bucket[1m])) by (le))`
		- `histogram_quantile(0.9, sum(rate(pilot_xds_push_time_bucket[1m])) by (le))`
		- `histogram_quantile(0.99, sum(rate(pilot_xds_push_time_bucket[1m])) by (le))`
		- `histogram_quantile(0.999, sum(rate(pilot_xds_push_time_bucket[1m])) by (le))`
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517221209.png)
- 임계값 권장 사항
	- Warning: 10초 이상 동안 지연 시간이 1초를 초과하는 경우
	- Critical: 10초 이상 동안 지연 시간이 2초를 초과하는 경우

#### 포화도: CPU 사용률
- `container_cpu_usage_seconds_total`
```bash
# Cumulative cpu time consumed by the container in core-seconds
container_cpu_usage_seconds_total
container_cpu_usage_seconds_total{container="discovery"}
container_cpu_usage_seconds_total{container="discovery", pod=~"istiod-.*|istio-pilot-.*"}
sum(irate(container_cpu_usage_seconds_total{container="discovery", pod=~"istiod-.*|istio-pilot-.*"}[1m]))
```
- `process_cpu_seconds_total`
```bash
# Total user and system CPU time spent in seconds
process_cpu_seconds_total{app="istiod"}
irate(process_cpu_seconds_total{app="istiod"}[1m])
```

![]({{ site.url }}/img/post/devops/study/istio/6/20250517222855.png)
- `kubectl top` pod/container 리소스 사용 확인

```bash
kubectl top pod -n istio-system -l app=istiod --containers=true
kubectl top pod -n istioinaction --containers=true

kubectl resource-capacity -n istioinaction -c -u -a
kubectl resource-capacity -n istioinaction -c -u   

kubectl get pod -n istio-system -l istio.io/rev=default
kubectl resource-capacity -n istio-system -c -u
kubectl resource-capacity -n istio-system -c -u -a -l istio.io/rev=default
kubectl resource-capacity -n istio-system -c -u -l istio.io/rev=default
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250517223955.png)
- 일반적으로 대부분의 시간은 idle 시간이다.
	- 서비스가 배포될 때 컴퓨팅 요청이 급증하는데, istiod가 엔보이 설정을 생성해 모든 워크로드로 푸시하기 때문
- 컨트롤 플레인이 포화되면 리소스가 부족한것
- 컨트롤 플레인 최적화를 위해 다른 방법들을 시도했었다면, 리소스를 늘리는 것이 최선일 수도 있다.

#### 트래픽: 컨트롤 플레인의 부하는 어느 정도인가?(수신/송신 설정 이벤트 수)
- 수신 트래픽
	- `pilot_inbound_update`
		- 각 istiod 인스턴스가 설정 변경 수신 횟수
	- `pilot_push_triggers`
		- 푸시를 유발한 전체 이벤트 횟수
		- 푸시 원인: 서비스, 엔드포인트, 설정(Gateway / VirtualService 같은 이스티오 커스텀 리소스)
	- `pilot_services`
		- 파일럿이 인지하고 있는 서비스 개수를 측정
		- 파일럿이 인지하는 서비스 개수가 늘어날수록, 이벤트를 수신할 때 엔보이 설정을 만들어내는데 필요한 처리가 더 많이진다.
		- 이 메트릭은 Istio Controle Plane Dashboard에서 ADS Monitoring 그래프의 Services로 표시
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517225833.png)
		- `avg(pilot_virt_services{app="istiod"})` : istio vs 개수: `kubectl get vs -A --no-headers=true | wc -l`
		- `avg(pilot_services{app="istiod"})` : k8s service 개수: `kubectl get svc -A --no-headers=true | wc -l`

- 발신 트래픽
	- `pilot_xds_pushes`
		- Listeners, Routes, Cluster, Endpoints 업데이트와 같이 컨트롤 플레인이 수행하는 모든 유형의 푸시를 측정
		- 이 메트릭은 Istio Controle Plane Dashboard에서 Pilot Pushed 그래프로 표시
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517225711.png)
		- `sum(irate(pilot_xds_pushes{type="cds"}[1m]))`
		- `sum(irate(pilot_xds_pushes{type="eds"}[1m]))`
		- `sum(irate(pilot_xds_pushes{type="lds"}[1m]))`
		- `sum(irate(pilot_xds_pushes{type="rds"}[1m]))`
	- `pilot_xds`
		- 워크로드의 전체 커넥션 개수를 파일럿 인스턴스별로 보여준다.
		- 이 메트릭은 Istio Control Plane Dashboard에서 ADS Monitoring 그래프로 표시
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517225833.png)
		- `avg(pilot_virt_services{app="istiod"})`: istio vs 개수: `kubectl get vs -A --no-headers=true | wc -l`
		- `avg(pilot_services{app="istiod"})`: k8s service 개수: `kubectl get svc -A --no-headers=true | wc -l`
	- `envoy_cluster_upstream_cx_tx_bytes_total`
		- 네트워크로 전송된 설정 크기를 측정
		- XDS Requests Size 패널의 Legend: XDS Request Bytes Average
        - ![]({{ site.url }}/img/post/devops/study/istio/6/20250517230703.png)
		- rx
			- `max(rate(envoy_cluster_upstream_cx_rx_bytes_total{cluster_name="xds-grpc"}[1m]))`
			- `quantile(0.5, rate(envoy_cluster_upstream_cx_rx_bytes_total{cluster_name="xds-grpc"}[1m]))`
		- tx
			- `max(rate(envoy_cluster_upstream_cx_tx_bytes_total{cluster_name="xds-grpc"}[1m]))`
			- `quantile(.5, rate(envoy_cluster_upstream_cx_tx_bytes_total{cluster_name="xds-grpc"}[1m]))`
- 수신 트래픽과 송신 트래픽을 구분하면 포화의 원인과 사용할 수 있는 완화책이 명확해진다.
- 포화가 수신 트래픽 때문이라면?
	- 성능 병목은 변화율 때문
	- 해결책: 이벤트 배치 처리를 늘리거나 스케일 업
- 포화수 송신 트래픽 관련이라면?
	- 해결책
		- 컨트롤 플레인을 스케일아웃
		- 모든 워크로드에 대해 사이드카 리소스를 정의

#### 오류: 컨트롤 플레인의 실패율은 어떻게 되는가?(푸시 실패/거부)
![]({{ site.url }}/img/post/devops/study/istio/6/20250517231204.png)
- 관련 메트릭
	- `pilot_total_xds_rejects`
		- 설정 푸시 거부 횟수
	- `pilot_xds_[cds/lds/rds/cds]_reject`
		- `pilot_total_xds_rejects` 메트릭의 부분집합
		- 어느 API 푸시가 거부됐는지 수사망을 좁히는데 유용
	- `pilot_xds_write_timeout`
		- push를 시작할 때 발생하는 오류와 타임아웃의 합계
	- `pilot_xds_push_context_errors`
		- 엔보이 설정을 생성하는 동안 발생한 이스티오 파일럿 오류 횟수
		- 주로 이스티오 파일럿의 버그와 관련

```bash
Legend(Rejected CDS Configs) : sum(pilot_xds_cds_reject{app="istiod"}) or (absent(pilot_xds_cds_reject{app="istiod"}) - 1)
Legend(Rejected EDS Configs) : sum(pilot_xds_eds_reject{app="istiod"}) or (absent(pilot_xds_eds_reject{app="istiod"}) - 1)
Legend(Rejected RDS Configs) : sum(pilot_xds_rds_reject{app="istiod"}) or (absent(pilot_xds_rds_reject{app="istiod"}) - 1)
Legend(Rejected LDS Configs) : sum(pilot_xds_lds_reject{app="istiod"}) or (absent(pilot_xds_lds_reject{app="istiod"}) - 1)
Legend(Write Timeouts) : sum(rate(pilot_xds_write_timeout{app="istiod"}[1m]))
Legend(Internal Errors) : sum(rate(pilot_total_xds_internal_errors{app="istiod"}[1m]))
Legend(Config Rejection Rate) : sum(rate(pilot_total_xds_rejects{app="istiod"}[1m]))
Legend(Push Context Errors) : sum(rate(pilot_xds_push_context_errors{app="istiod"}[1m]))
Legend(Push Timeouts) : sum(rate(pilot_xds_write_timeout{app="istiod"}[1m]))
```

## 성능 튜닝하기
- 컨트롤 플레인의 성능 요인
	- 클러스터/환경의 변화 속도
	- 리소스 할당량
	- 관리하는 워크로드 개수
	- 그 워크로드로 푸시하는 설정 크기
- 기본 전략
	- 불필요한 이벤트 무시
	- 이벤트 배치 처리 증가
	- istiod 스케일 업/아웃
	- Sidecar 리소스로 설정 범위 축소

![]({{ site.url }}/img/post/devops/study/istio/6/20250506101041.png)

### 워크스페이스 준비하기

```bash
# 모니터링
while true; do kubectl top pod -n istio-system -l app=istiod --containers=true ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

# 더미 워크로드 10개 생성
cat ch11/sleep-dummy-workloads.yaml
...
apiVersion: v1
kind: Service
...
spec:
  ports:
  - port: 80
    name: http
  selector:
    app: sleep
---
apiVersion: apps/v1
kind: Deployment
...
    spec:
      serviceAccountName: sleep
      containers:
      - name: sleep
        image: governmentpaas/curl-ssl
        command: ["/bin/sleep", "3650d"]
        imagePullPolicy: IfNotPresent
...

kubectl -n istioinaction apply -f ch11/sleep-dummy-workloads.yaml

# 확인
kubectl get deploy,svc,pod -n istioinaction

docker exec -it myk8s-control-plane istioctl proxy-status

docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction --fqdn sleep.istioinaction.svc.cluster.local
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction
```

```bash
cat ch11/resources-600.yaml
cat ch11/resources-600.yaml | wc -l
    9200

# 각각 200개
cat ch11/resources-600.yaml | grep 'kind: Service' | wc -l
cat ch11/resources-600.yaml | grep 'kind: Gateway' | wc -l
cat ch11/resources-600.yaml | grep 'kind: VirtualService' | wc -l
     200

# 배포 : svc 200개, vs 200개, gw 200개
kubectl -n istioinaction apply -f ch11/resources-600.yaml

# 확인
kubectl get deploy,svc,pod -n istioinaction
...

# k8s service 개수 202개
kubectl get svc -n istioinaction --no-headers=true | wc -l 
     202

kubectl get gw,vs -n istioinaction
...

docker exec -it myk8s-control-plane istioctl proxy-status
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250517233259.png)

### 최적화 전 성능 측정하기
- 서비스를 반복적으로 만들어 부하를 생성하고, 프록시에 설정을 업데이트하는데 걸리는 지연 시간과 P99 값과 푸시 개수를 측정한다.

#### 테스트를 2.5초 간격으로 10회 반복
> 성능 측정이 너무 오래 걸려서 추후 다시 진행 예정. 우선 스터디 자료로 보충

```bash
# 성능 테스트 스크립트 실행!
./bin/performance-test.sh --reps 10 --delay 2.5 --prom-url prometheus.istio-system.svc.cluster.local:9090
Pre Pushes: 335
...
ateway.networking.istio.io/service-00a9-9 created
service/service-00a9-9 created
virtualservice.networking.istio.io/service-00a9-9 created
==============

Push count: 510 # 변경 사항을 적용하기 위한 푸시 함수
Latency in the last minute: 0.45 seconds # 마지막 1분 동안의 지연 시간

# 확인
kubectl get svc -n istioinaction --no-headers=true | wc -l
kubectl get gw -n istioinaction --no-headers=true | wc -l
kubectl get vs -n istioinaction --no-headers=true | wc -l

```
#### 딜레이 없이 실행
```bash
# 성능 테스트 스크립트 실행 : 딜레이 없이
./bin/performance-test.sh --reps 10 --prom-url prometheus.istio-system.svc.cluster.local:9090
Push count: 51
Latency in the last minute: 0.47 seconds

# 확인
kubectl get svc -n istioinaction --no-headers=true | wc -l
kubectl get gw -n istioinaction --no-headers=true | wc -l
kubectl get vs -n istioinaction --no-headers=true | wc -l
```
#### 딜레이 늘려서 실행
```bash
# 성능 테스트 스크립트 실행 : 딜레이 없이
./bin/performance-test.sh --reps 10 --delay 5 --prom-url prometheus.istio-system.svc.cluster.local:9090
Push count: 510
Latency in the last minute: 0.43 seconds
```

#### 테스트 정리
(1)
```bash
Push count: 510 # 변경 사항을 적용하기 위한 푸시 함수
Latency in the last minute: 0.45 seconds # 마지막 1분 동안의 지연 시간, 책은 ms로 표기..
```
(2)
```bash
Push count: 51
Latency in the last minute: 0.47 seconds
```
(3)
#### 사이드카를 사용해 푸시 횟수 및 설정 크기 줄이기
```bash
# catalog 워크로드의 설정 크기를 계산
CATALOG_POD=$(kubectl -n istioinaction get pod -l app=catalog -o jsonpath={.items..metadata.name} | cut -d ' ' -f 1)
kubectl -n istioinaction exec -ti $CATALOG_POD -c catalog -- curl -s localhost:15000/config_dump > /tmp/config_dump
du -sh /tmp/config_dump
1.8M    /tmp/config_dump

docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction

docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction | wc -l
     275
```
- 설정크기 대략 2MB
- 워크로드가 200개인 중간 클러스터만 돼도 엔보이 설정이 400MB로 증가
	- 이로 인해 연산 성능, 네트워크 대역폭, 메모리가 더 많이 필요함
	- 이 설정이 모든 사이드카 프록시에 저장되기 때문
#### Sidecar 리소스
- workloadSelector: 사이드카 설정을 적용할 워크로드를 제한
- ingress: 애플리케이션에 들어오는 트래픽 처리를 지정
	- 생략시, 이스티오는 파드 정의를 조회해 서비스 프록시를 자동으로 설정함
- egress: 허용할 외부 서비스 제한
	- 생략시, 설정은 좀 더 일반적인 사이드카에서 egress 설정(있다면)을 상속
		- 없으면, 다른 모든 서비스에 접근할 수 있도록 설정하는 기본 동작으로 대처
- outboundTrafficPolicy: 송신 트래픽 처리시 모드 지정
	- `REGISTRY_ONLY`: 명시 서비스만 허용
	- `ALLOW_ANY`: 어디로든 트래픽 송싱 허용

```bash
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
metadata:
  name: default
  namespace: istioinaction
spec:
  workloadSelector:
    labels:
      app: foo
  egress:
  -hosts:
   - "./bar.istioinaction.svc.cluster.local"
   - "istio-system/*"
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY
```
#### 메시 범위 사이드카 설정으로 더 나은 기본값 정의하기
- 트래픽 송싱을 istio-system 네임스페이스의 서비스로만 허용하는 사이드카 설정 -> 메시 범위로 정의
- 기본값을 이렇게 정의시, 최소 설정으로 메시 내 모든 프록시가 컨트롤 플레인에만 연결하도록 하고, 다른 서비스로의 연결 설정은 모두 삭제할 수 있다.
	- 서비스 소유자를 올바른 길로 유도
	- 워크로드용 사이드카 정의를 좀 더 구체적으로 정의
	- 서비스에 필요한 트래픽 송신을 모두 명시적으로 기술하게 함
		- 워크로드가 프로세스에 필요한 관련 설정을 최소한으로 수신

```bash
# cat ch11/sidecar-mesh-wide.yaml
apiVersion: networking.istio.io/v1beta1
kind: Sidecar
metadata:
  name: default # istio-system 네임스페이스의 사이드카는 메시 전체에 적용된다.
  namespace: istio-system # 위 설명 동일.
spec:
  egress:
  - hosts:
    - "istio-system/*" # istio-system 네임스페이스의 워크로드만 트래픽 송신을 할 수 있게 설정한다.
    - "prometheus/*"   # 프로메테우스 네임스페이스도 트래픽 송신을 할 수 있게 설정한다.
  outboundTrafficPolicy:
    mode: REGISTRY_ONLY # 모드는 사이드카에 설정한 서비스로만 트래픽 송신을 허용한다
```

```bash
# 테스트를 위해 샘플 nginx 배포
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
EOF

# catalog 에서 nginx 서비스 접속 확인
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/catalog.istioinaction | grep nginx
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction | grep nginx                                        
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction | grep nginx
10.10.0.26:80                                           HEALTHY     OK                outbound|80||nginx.default.svc.cluster.local

kubectl exec -it deploy/catalog -n istioinaction -- curl nginx.default | grep title
<title>Welcome to nginx!</title>


# istio-system, prometheus 네임스페이스만 egress 허용 설정
kubectl -n istio-system apply -f ch11/sidecar-mesh-wide.yaml
kubectl get sidecars -A

# catalog 에서 nginx 서비스 접속 확인
docker exec -it myk8s-control-plane istioctl proxy-config route deploy/catalog.istioinaction | grep nginx
docker exec -it myk8s-control-plane istioctl proxy-config cluster deploy/catalog.istioinaction | grep nginx                                        
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/catalog.istioinaction | grep nginx
kubectl exec -it deploy/catalog -n istioinaction -- curl nginx.default | grep title

# envoy config 크기 다시 확인!
CATALOG_POD=$(kubectl -n istioinaction get pod -l app=catalog -o jsonpath={.items..metadata.name} | cut -d ' ' -f 1)
kubectl -n istioinaction exec -ti $CATALOG_POD -c catalog -- curl -s localhost:15000/config_dump > /tmp/config_dump
du -sh /tmp/config_dump
520K    /tmp/config_dump
```
- 설정 크기가 2MB -> 520K로 대폭 줄어듬

```bash
# 성능 테스트 스크립트 실행!
./bin/performance-test.sh --reps 10 --delay 2.5 --prom-url prometheus.istio-system.svc.cluster.local:9090
...
Push count: 88 # 변경 사항을 적용하기 위한 푸시 함수
Latency in the last minute: 0.10 seconds # 마지막 1분 동안의 지연 시간

# 확인
kubectl get svc -n istioinaction --no-headers=true | wc -l
kubectl get gw -n istioinaction --no-headers=true | wc -l
kubectl get vs -n istioinaction --no-headers=true | wc -l
```
- 푸시 횟수와 지연 시간이 모두 줄어듬

- 기존 클러스터에서는 서비스 중단을 방지하기 위해 플랫폼의 사용자들과 신중히 협의
- 그들이 좀 더 구체적인 Sidecar 리소스를 워크로드의 송신 트래픽을 먼저 정의하도록 해야 한다.
- 그 후 메시 범위에 디폴트 사이드카 설정을 적용할 수 있다.

### 이벤트 무시하기: 디스커버리 셀렉터로 디스커버리 범위 줄이기
- 감시할 네임스페이스 제한
- 불필요한 네임스페이스에서 이벤트 발생 방지

```bash
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
spec:
  meshConfig:
    discoverySelectors: # 디스커버리 셀렉터 활성화
      - matchLabels:
          istio-discovery: enabled # 사용할 레이블 지정
```

```bash
# 네임스페이스 대부분을 포함하고 소규모만 제외하려는 경우
# 레이블 비교 표현식을 사용
apiVersion: install.istio.io/v1alpha1
kind: IstioOperator
metadata:
  namespace: istio-system
spec:
  meshConfig:
    discoverySelectors:
      - matchExpressions:
        - key: istio-exclude
          operator: NotIn
          values:
            - "true"
```


```bash
# 모든 항목을 살피는 기본 동작을 방해하지 않고
# istio-exclude: true 레이블이 있는 네임스페이스만 제외하도록 업데이트
cat ch11/istio-discovery-selector.yaml

docker exec -it myk8s-control-plane cat /istiobook/ch11/istio-discovery-selector.yaml
docker exec -it myk8s-control-plane istioctl install -y -f /istiobook/ch11/istio-discovery-selector.yaml

kubectl get istiooperators.install.istio.io -A -o json
...
                "meshConfig": {
                    "accessLogEncoding": "JSON",
                    "accessLogFile": "/dev/stdout",
                    "defaultConfig": {
                        "proxyMetadata": {}
                    },
                    "discoverySelectors": [
                        {
                            "matchExpressions": [
                                {
                                    "key": "istio-exclude",
                                    "operator": "NotIn",
                                    "values": [
                                        "true"
...
```


```bash
kubectl create ns new-ns
kubectl label namespace new-ns istio-injection=enabled
kubectl get ns --show-labels

# 테스트를 위해 샘플 nginx 배포
cat << EOF | kubectl apply -n new-ns -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx
spec:
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
  type: ClusterIP
EOF

# 확인
kubectl get deploy,svc,pod -n new-ns
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system | grep nginx
10.10.0.26:80                                           HEALTHY     OK                outbound|80||nginx.default.svc.cluster.local
10.10.0.27:80                                           HEALTHY     OK                outbound|80||nginx.new-ns.svc.cluster.local

# 설정
kubectl label ns new-ns istio-exclude=true
kubectl get ns --show-labels

# 다시 확인
docker exec -it myk8s-control-plane istioctl proxy-config endpoint deploy/istio-ingressgateway.istio-system | grep nginx
10.10.0.26:80                                           HEALTHY     OK                outbound|80||nginx.default.svc.cluster.local

```

### 이벤트 배치 처리 및 푸시 스로틀링 속성
- 디바운스 기반
	- 데이터 플레인 설정을 바꾸는 런타임 환경 이벤트는 보통 운영자가 제어할 수 없는 것이다.
		- 이벤트들(새로운 서비스가 온라인 상태가 되는 것 / 복제본 스케일 아웃 / 서비스가 비정상이 되는 것 등)은 모두 컨트롤 플레인이 감지해 데이터 플레인 프록시를 조정함
	- 업데이트를 얼마나 지연해서 배치 처리할지 정도는 제어할 수 있음
		- 배치 처리시, 이벤트를 한 묶음으로 처리하여 엔보이 설정을 한 번만 만들어 데이터 플레인 프록ㄷ시로 한 번에 푸시할 수 있다.
![]({{ site.url }}/img/post/devops/study/istio/6/20250506102052.png)

- 디바운스 기반을 더 늘리면
	- 지연 기간에서 제외됐던 마지막 이벤트도 배치에 포함시켜 모든 이벤트를 하나의 배치로 합쳐 하나의 요청으로 푸시
- 푸시를 너무 미루면
	- 데이터 플레인 설정이 최신상태와 어긋난다.
- 기간을 줄이면
	- 업데이트가 더 빠르게 수행되는 것을 보장
	- 컨트롤 플레인이 미쳐 배포할 수 없을 정도로 푸시 요청이 증가
	- 이런 요청들은 푸시 대기열에서 스로틀링돼 대기 시간 증가로 이어짐

#### 배치 기간과 푸시 스로틀링을 정의하는 환경 변수

**환경 변수**                 | **설명**            | **기본값** |
------------------------- | ----------------- | ------- |
PILOT_DEBOUNCE_AFTER      | 푸시 지연 시작 시간       | 100ms   |
PILOT_DEBOUNCE_MAX        | 최대 디바운스 시간        | 10s     |
PILOT_ENABLE_EDS_DEBOUNCE | 엔드포인트도 디바운스 포함 여부 | true    |
PILOT_PUSH_THROTTLE       | 동시에 푸시할 수 있는 최대 수 | 100     |

- 설정 옵션 사용시 지침
	- 컨트롤 플레인이 포화상태 / 수신 트래픽이 성능 병목을 야기하는 경우
		- 이벤트 배치 처리를 늘린다.
	- 목표가 업데이트 전파를 더 빠르게 하는 것이라면
		- 이벤트 배치 처리를 줄이고, 동시 푸시 개수를 늘린다.
			- 컨트롤 플레인이 포화상태가 아닐때만 권장
	- 컨트롤 플레인이 포화 상태 / 송신 트래픽이 성능 병목인 경우
		- 동시에 푸시하는 개수를 줄인다.
	- 컨트롤 플레인이 포화상태 or 스케일 업을 했고 빠른 업데이틀르 원하는 경우
		- 동시 푸시하는 개수를 늘린다.

#### 배치 기간 늘리기
```bash
# myk8s-control-plane 진입 후 설치 진행
docker exec -it myk8s-control-plane bash
-----------------------------------
# demo 프로파일 컨트롤 플레인 배포 시 적용
istioctl install --set profile=demo --set values.pilot.env.PILOT_DEBOUNCE_AFTER="2500ms" --set values.global.proxy.privileged=true --set meshConfig.accessLogEncoding=JSON -y
exit
-----------------------------------

#
kubectl get deploy/istiod -n istio-system -o yaml
...
        - name: PILOT_DEBOUNCE_AFTER
          value: 2500ms
...

# 성능 테스트 스크립트 실행!
./bin/performance-test.sh --reps 10 --delay 2.5 --prom-url prometheus.istio-system.svc.cluster.local:9090
Push count: 28 # 변경 사항을 적용하기 위한 푸시 함수
Latency in the last minute: 0.10 seconds # 마지막 1분 동안의 지연 시간
```
#### 지연 시간 메트릭은 디바운스 기간을 고려하지 않는다!
- 지연 시간 메트릭이 측정하는 기간은 푸시 요청이 푸시 대기열에 추가된 시점부터 시작된다.
	- 즉, 이벤트들이 디바운스되는 동안 업데이트는 전달되지 않음
- 업데이트를 푸시하는 시간은 늘어났지만, 이는 지연 시간 메트릭에서는 나타나지 않는다.

- 이벤트를 너무 오래 디바운스해 지연시간이 늘어나면 성능이 낮을 때와 마찬가지로 설정이 최신상태와 어긋난다.
	- 따라서 배치 속성 조정시 한 번에 너무 크게 변강하지 말고, 조금씩 변경하자.
#### 컨트롤 플레인에 리소스 추가 할당하기
- Sidecar 리소스를 정의하고 discovery selectors를 사용하고 배치를 설정한 후, 성능을 더 향상 시키려면
	- 컨트롤 플레인에 리소스를 더 할당하는 것
	- 리소스를 더 할당시 istiod 인스턴스를 추가해 스케일 아웃하거나, 모든 istiod 인스턴스에 리소스를 추가로 제공해 스케입 업할 수 있다.
- 스케일 아웃? 스케일 업?
	- 송신 트래픽이 병목 -> 스케일 아웃
		- istiod 인스턴스당 관리하는 워크로드가 많아서 발생
		- istiod 인스턴스가 관리하는 워크로드 개수를 줄임
	- 수신 트래픽이 병목 -> 스케일 업
		- 엔보이 설정을 생성하는데 리소스를 많이 처리시 발생
		- istiod 인스턴스의 처리 능력 상승

```bash
kubectl get pod -n istio-system -l app=istiod
kubectl resource-capacity -n istio-system -u -l app=istiod
NODE                  CPU REQUESTS   CPU LIMITS   CPU UTIL   MEMORY REQUESTS   MEMORY LIMITS   MEMORY UTIL
myk8s-control-plane   10m (0%)       0m (0%)      8m (0%)    100Mi (0%)        0Mi (0%)        90Mi (0%)

# myk8s-control-plane 진입 후 설치 진행
docker exec -it myk8s-control-plane bash
-----------------------------------
# demo 프로파일 컨트롤 플레인 배포 시 적용
istioctl install --set profile=demo \
--set values.pilot.resources.requests.cpu=1000m \
--set values.pilot.resources.requests.memory=1Gi \
--set values.pilot.replicaCount=2 -y

exit
-----------------------------------

kubectl get pod -n istio-system -l app=istiod
NAME                      READY   STATUS    RESTARTS   AGE
istiod-5485dd8c48-6ngdc   1/1     Running   0          11s
istiod-5485dd8c48-chjsz   1/1     Running   0          11s

kubectl resource-capacity -n istio-system -u -l app=istiod
NODE                  CPU REQUESTS   CPU LIMITS   CPU UTIL    MEMORY REQUESTS   MEMORY LIMITS   MEMORY UTIL
myk8s-control-plane   2000m (25%)    0m (0%)      119m (1%)   2048Mi (17%)      0Mi (0%)        107Mi (0%)

kubectl describe pod -n istio-system -l app=istiod
...
    Requests:
      cpu:      1
      memory:   1Gi
...
```
#### istiod 디플로이먼트 오토스케일링
- 점진적인 부하 증가에 맞춰 오토스케일링 구성(며칠, 몇주, 심지어 몇 달 단위에 걸쳐서)

## 성능 튜닝 가이드라인
- 이스티오는 성능이 좋다.
	- 이스티오 팀의 테스트
		- 엔보이 설정을 부풀리는 쿠버네티스 서비스 1,000개
		- 동기화해야 하는 워크로드 2,000개
		- 서비스 메시 전체에서 초당 요청 70,000개
	- 이 정도 부하로도 메시 전체를 동기화하는 이스티오 파일럿 인스턴스 하나가 1vCPU , Memory 1.5GB 사용함
	- 대부분의 운영환경 클러스터에는 2 vCPU, Memory 2GB 정도로 충분함

1. 문제의 원인 파악
	- 컨트롤 플레인, 데이터 플레인, API 서버 문제 여부
2. 병목 구분
	- 지연, 트래픽, 포화도 지표 확인
3. 점진적 변경
	- 설정을 10 ~ 30% 단위로 조정
4. 안정성 우선
	- istiod 복제본 2개 이하 금지
	- generous한 자원 설정 권장
5. Sidecar 및 discoverySelector 적극 활용

# 부록 D. 이스티오 구성 요소 트러블슈팅하기
포트와 엔드포인트 정보를 활용한 디버깅 및 트러블슈팅 전략
## 이스티오 에이전트가 노출하는 정보
- 기능별 역할
	- 헬스 체크
		- 설정 완료, ID 할당 등 메시 준비 여부 감사
	- 메트릭 수집
		- 애플리케이션, 에이전트, 프록시 통계 병합
	- DNS 해석
		- Iptable 기반 인바운드/아웃바운드 트래픽 라우팅

```bash
# 기존 리소스 삭제
kubectl delete -n istioinaction deploy,svc,gw,vs,dr,envoyfilter --all

# 샘플 애플리케이션 배포
kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction
kubectl apply -f services/webapp/kubernetes/webapp.yaml -n istioinaction
kubectl apply -f services/webapp/istio/webapp-catalog-gw-vs.yaml -n istioinaction

# 확인
kubectl get gw,vs -n istioinaction
curl -s http://webapp.istioinaction.io:30000/api/catalog | jq

# 신규 터미널 : 반복 접속
while true; do curl -s http://webapp.istioinaction.io:30000/api/catalog ; date "+%Y-%m-%d %H:%M:%S" ; sleep 1; echo; done

```

```bash
kubectl -n istioinaction exec -it deploy/webapp -c istio-proxy -- netstat -tnl
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:15000         0.0.0.0:*               LISTEN     
tcp        0      0 127.0.0.1:15004         0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:15021           0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:15021           0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:15001           0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:15001           0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:15006           0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:15006           0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:15090           0.0.0.0:*               LISTEN     
tcp        0      0 0.0.0.0:15090           0.0.0.0:*               LISTEN     
tcp6       0      0 :::15020                :::*                    LISTEN     
tcp6       0      0 :::8080                 :::*                    LISTEN   

# 포트별 프로세스 확인 : 파일럿에이전트, 엔보이
kubectl -n istioinaction exec -it deploy/webapp -c istio-proxy --  ss -tnlp
State                Recv-Q               Send-Q                             Local Address:Port                                Peer Address:Port               Process                                            
LISTEN               0                    4096                                   127.0.0.1:15000                                    0.0.0.0:*                   users:(("envoy",pid=21,fd=18))                    
LISTEN               0                    4096                                   127.0.0.1:15004                                    0.0.0.0:*                   users:(("pilot-agent",pid=1,fd=11))               
LISTEN               0                    4096                                     0.0.0.0:15021                                    0.0.0.0:*                   users:(("envoy",pid=21,fd=25))                    
LISTEN               0                    4096                                     0.0.0.0:15021                                    0.0.0.0:*                   users:(("envoy",pid=21,fd=24))                    
LISTEN               0                    4096                                     0.0.0.0:15001                                    0.0.0.0:*                   users:(("envoy",pid=21,fd=36))                    
LISTEN               0                    4096                                     0.0.0.0:15001                                    0.0.0.0:*                   users:(("envoy",pid=21,fd=35))                    
LISTEN               0                    4096                                     0.0.0.0:15006                                    0.0.0.0:*                   users:(("envoy",pid=21,fd=38))                    
LISTEN               0                    4096                                     0.0.0.0:15006                                    0.0.0.0:*                   users:(("envoy",pid=21,fd=37))                    
LISTEN               0                    4096                                     0.0.0.0:15090                                    0.0.0.0:*                   users:(("envoy",pid=21,fd=23))                    
LISTEN               0                    4096                                     0.0.0.0:15090                                    0.0.0.0:*                   users:(("envoy",pid=21,fd=22))                    
LISTEN               0                    4096                                           *:15020                                          *:*                   users:(("pilot-agent",pid=1,fd=7))                
LISTEN               0                    4096                                           *:8080                                           *:*               

# istio-proxy 컨테이너에 Readiness Probe 정보 확인 : 15021 헬스체크 포트
kubectl describe pod -n istioinaction -l app=webapp | grep Readiness:
    Readiness:  http-get http://:15021/healthz/ready delay=1s timeout=3s period=2s #success=1 #failure=30
```
![]({{ site.url }}/img/post/devops/study/istio/6/20250503154613.png)
- 주요 포트 및 용도
	- 15000: 엔보이 관리 인터페이스
	- 15001: 아웃바운드 트래픽 진입점
	- 15004: 파일럿 디버그 엔드포인트 노출
	- 15006: 인바운드 트래픽 진입점
	- 15020: 메트릭 노출, 헬스체크, 에이전트 디버그
	- 15021: 사이드카 준비 상태 헬스체크
	- 15053: 로컬 DNS 프록시
	- 15090: 엔보이 메트릭 노출 (xDS, 연결, HTTP 등)

### 이스티오 에이전트를 조사하고 트러블슈팅하기위한 엔드포인트들
- Agent 디버깅용 엔드포인트
	- `/healthz/ready`: 프록시 및 DNS 프록시 상태 확인
	- `/stats/prometheus`: 엔보이 + 애플리케이션 메트릭 병합 노출
	- `/quitquitquit`: 파일럿 에이전트 프로세스 종료
	- `/app-health/`: 애플리케이션 헬스 프록시
	- `/debug/ndsz`: istiod가 설정한 DNS 목록
	- `/debug/pprof/*`: Go 프로파일링 정보 노출 (성능 디버깅용)

```bash
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: liveness-http
  namespace: istioinaction
spec:
  selector:
    matchLabels:
      app: liveness-http
      version: v1
  template:
    metadata:
      labels:
        app: liveness-http
        version: v1
    spec:
      containers:
      - name: liveness-http
        image: docker.io/istio/health:example
        ports:
        - containerPort: 8001
        livenessProbe:
          httpGet:
            path: /foo
            port: 8001
          initialDelaySeconds: 5
          periodSeconds: 5
EOF

#
kubectl get pod -n istioinaction -l app=liveness-http
kubectl describe pod -n istioinaction -l app=liveness-http
...
Containers:
  liveness-http:
    Container ID:   containerd://edaf01bff5d553e03290b3d44f60bb26958319e615a27a9b38309aad9b2df477
    Image:          docker.io/istio/health:example
    Image ID:       docker.io/istio/health@sha256:d8a2ff91d87f800b4661bec5aaadf73d33de296d618081fa36a0d1cbfb45d3d5
    Port:           8001/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Sat, 10 May 2025 16:58:35 +0900
    Ready:          True
    Restart Count:  0
    Liveness:       http-get http://:15020/app-health/liveness-http/livez delay=5s timeout=1s period=5s #success=1 #failure=3
    ...
  istio-proxy:
    Container ID:  containerd://d4b0955372bdb7b3e1490eb3f290c6c6f5a9f2691eabea4cebafaafa8be85fc9
    Image:         docker.io/istio/proxyv2:1.17.8
    Image ID:      docker.io/istio/proxyv2@sha256:d33fd90e25c59f4f7378d1b9dd0eebbb756e03520ab09cf303a43b51b5cb01b8
    Port:          15090/TCP
    ...
    Readiness:  http-get http://:15021/healthz/ready delay=1s timeout=3s period=2s #success=1 #failure=30
    Environment:
      ...                          
      ISTIO_META_POD_PORTS:          [
                                         {"containerPort":8001,"protocol":"TCP"}
                                     ]
      ISTIO_META_APP_CONTAINERS:     liveness-http
      ISTIO_META_CLUSTER_ID:         Kubernetes
      ISTIO_META_NODE_NAME:           (v1:spec.nodeName)
      ISTIO_META_INTERCEPTION_MODE:  REDIRECT
      ISTIO_META_WORKLOAD_NAME:      liveness-http
      ISTIO_META_OWNER:              kubernetes://apis/apps/v1/namespaces/istioinaction/deployments/liveness-http
      ISTIO_META_MESH_ID:            cluster.local
      TRUST_DOMAIN:                  cluster.local
      ISTIO_KUBE_APP_PROBERS:        {"/app-health/liveness-http/livez":{"httpGet":{"path":"/foo","port":8001,"scheme":"HTTP"},"timeoutSeconds":1}}


kubectl get pod -n istioinaction -l app=liveness-http -o json | jq '.items[0].spec.containers[0].livenessProbe.httpGet'
{
  "path": "/app-health/liveness-http/livez",
  "port": 15020,
  "scheme": "HTTP"
}

# 헬스체크 확인
kubectl exec -n istioinaction deploy/liveness-http -c istio-proxy -- curl -s localhost:15020/app-health/liveness-http/livez -v

# 실습 확인 후 삭제
kubectl delete deploy liveness-http -n istioinaction

```

```bash
kubectl exec -n istioinaction deploy/webapp -c istio-proxy -- curl -s localhost:15020/healthz/ready -v

# webapp 워크로드의 병합된 통계 확인 : istio_agent로 시작하는 메트릭(에이전트에서 온 것) + envoy로 시작하는 메트릭(프록시에서 온 것)
kubectl exec -n istioinaction deploy/webapp -c istio-proxy -- curl -s localhost:15020/stats/prometheus
## 응답에서는 istio_agent로 시작하는 메트릭(에이전트에서 온 것)과 envoy로 시작하는 메트릭(프록시에서 온 것)을 볼 수 있는데,
## 이는 이 둘이 병합됐음을 보여준다.

kubectl exec -n istioinaction deploy/webapp -c istio-proxy -- curl -s localhost:15020/quitquitquit

kubectl exec -n istioinaction deploy/webapp -c istio-proxy -- curl -s localhost:15020/debug/ndsz

kubectl port-forward deploy/webapp -n istioinaction 15020:15020
open http://localhost:15020/debug/pprof # 혹은 웹 브라우저에서 열기
```
### 이스티오 에이전트를 통해 이스티오 파일럿 디버그 엔드포인드를 쿼리하기

```bash
kubectl exec -n istioinaction deploy/webapp -c istio-proxy -- curl -s localhost:15004/debug/syncz -v
kubectl exec -n istioinaction deploy/webapp -c istio-proxy -- curl -s localhost:15004/debug/syncz | jq
...
      "@type": "type.googleapis.com/envoy.service.status.v3.ClientConfig",
      "node": {
        "id": "catalog-6cf4b97d-fbftr.istioinaction", # 워크로드 ID
        "metadata": {
          "CLUSTER_ID": "Kubernetes"
        }
      },
      "genericXdsConfigs": [
        {
          "typeUrl": "type.googleapis.com/envoy.config.listener.v3.Listener",
          "configStatus": "SYNCED" # xDS API는 최신 상태로 동기화됬다
        },
        {
          "typeUrl": "type.googleapis.com/envoy.config.route.v3.RouteConfiguration",
          "configStatus": "SYNCED" # xDS API는 최신 상태로 동기화됬다
        },
        {
          "typeUrl": "type.googleapis.com/envoy.config.endpoint.v3.ClusterLoadAssignment",
          "configStatus": "SYNCED" # xDS API는 최신 상태로 동기화됬다
        },
        {
          "typeUrl": "type.googleapis.com/envoy.config.cluster.v3.Cluster",
          "configStatus": "SYNCED" # xDS API는 최신 상태로 동기화됬다
        },
...

docker exec -it myk8s-control-plane istioctl x internal-debug -h
docker exec -it myk8s-control-plane istioctl x internal-debug syncz
```
## 이스티오 파일럿이 노출하는 정보
```bash
kubectl -n istio-system exec -it deploy/istiod -- netstat -tnl
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 127.0.0.1:9876          0.0.0.0:*               LISTEN     
tcp6       0      0 :::15017                :::*                    LISTEN     
tcp6       0      0 :::15014                :::*                    LISTEN     
tcp6       0      0 :::15012                :::*                    LISTEN     
tcp6       0      0 :::15010                :::*                    LISTEN     
tcp6       0      0 :::8080                 :::*                    LISTEN 

# pilot-discovery 프로세스 확인
kubectl -n istio-system exec -it deploy/istiod -- ss -tnlp
State          Recv-Q         Send-Q                 Local Address:Port                  Peer Address:Port         Process                                          
LISTEN         0              4096                       127.0.0.1:9876                       0.0.0.0:*             users:(("pilot-discovery",pid=1,fd=8))          
LISTEN         0              4096                               *:15017                            *:*             users:(("pilot-discovery",pid=1,fd=12))         
LISTEN         0              4096                               *:15014                            *:*             users:(("pilot-discovery",pid=1,fd=9))          
LISTEN         0              4096                               *:15012                            *:*             users:(("pilot-discovery",pid=1,fd=10))         
LISTEN         0              4096                               *:15010                            *:*             users:(("pilot-discovery",pid=1,fd=11))         
LISTEN         0              4096                               *:8080                             *:*             users:(("pilot-discovery",pid=1,fd=3)) 

kubectl describe pod -n istio-system -l app=istiod
...
Containers:
  discovery:
    Container ID:  containerd://f13d7ad8a32cc0cecf47392ef426ea4687ce12d1abf64b5a6d2a60c2f8934e04
    Image:         docker.io/istio/pilot:1.17.8
    Image ID:      docker.io/istio/pilot@sha256:cb9e7b1b1c7b8dcea37d5173b87c40f38a5ae7b44799adfdcf8574c57a52ad2c
    Ports:         8080/TCP, 15010/TCP, 15017/TCP
    Host Ports:    0/TCP, 0/TCP, 0/TCP
    Args:
      discovery
      --monitoringAddr=:15014
      --log_output_level=default:info
      --domain
      cluster.local
      --keepaliveMaxServerConnectionAge
      30m
    ...
    Readiness:  http-get http://:8080/ready delay=1s timeout=5s period=3s #success=1 #failure=3
    Environment:
      REVISION:                                     default
      JWT_POLICY:                                   third-party-jwt
      PILOT_CERT_PROVIDER:                          istiod
      POD_NAME:                                     istiod-8d74787f-ltkhs (v1:metadata.name)
      POD_NAMESPACE:                                istio-system (v1:metadata.namespace)
      SERVICE_ACCOUNT:                               (v1:spec.serviceAccountName)
      KUBECONFIG:                                   /var/run/secrets/remote/config
      PILOT_TRACE_SAMPLING:                         100
      PILOT_ENABLE_PROTOCOL_SNIFFING_FOR_OUTBOUND:  true
      PILOT_ENABLE_PROTOCOL_SNIFFING_FOR_INBOUND:   true
      ISTIOD_ADDR:                                  istiod.istio-system.svc:15012
      PILOT_ENABLE_ANALYSIS:                        false
      CLUSTER_ID:                                   Kubernetes
...
```

![]({{ site.url }}/img/post/devops/study/istio/6/20250503150809.png)
- 주요 포트
	- 15010: xDS API (비암호화, 사용 지양)
	- 15012: xDS API (TLS, 상호 인증 지원)
	- 15014: 컨트롤 플레인 메트릭 노출
	- 15017: 쿠버네티스 웹훅 서버
	- 8080: 파일럿 디버그 엔드포인트
	- 9876: ControlZ 관리자 UI

### 이스티오 파일럿 디버그 엔드포인트
- 프록시 동기화 상태 확인: `/debug/syncz`
- 프록시 최종 푸시 시간 확인: `/debug/adsz` 등
- xDS API 상태 검사:`/debug/configz` 등

> 보안 주의: 운영 환경에서는 `ENABLE_DEBUG_ON_HTTP=false` 설정으로 비활성화 권장

```bash
kubectl -n istio-system port-forward deploy/istiod 8080
open http://localhost:8080/debug

# 파일럿이 알고 있는 서비스 메시 상태
## 클러스터, 루트, 리스너 설정
curl -s http://localhost:8080/debug/adsz | jq

## 이 파일럿이 관리하는 모든 프록시에 대한 푸시를 트리거한다.
curl -s http://localhost:8080/debug/adsz?push=true
Pushed to 4 servers

## /debug/edsz=proxyID=<pod>.<namespace> : 프록시가 알고 있는 엔드포인트들
curl -s http://localhost:8080/debug/edsz=proxyID=webapp.istioninaction

## /debug/authorizationz : 네임스페이스에 적용되는 인가 정책 목록
curl -s http://localhost:8080/debug/authorizationz | jq


# 파일럿이 알고 있는 데이터 플레인 설정을 나타내는 엔드포인트
## 이 파일럿 인스턴스에 연결된 모든 엔보이의 버전 상태 : 현재 비활성화되어 있음
curl -s http://localhost:8080/debug/config_distribution
Pilot Version tracking is disabled. It may be enabled by setting the PILOT_ENABLE_CONFIG_DISTRIBUTION_TRACKING environment variable to true

## 이스티오 파일럿의 현재 알려진 상태에 따라 엔보이 설정을 생성한다.
curl -s http://localhost:8080/debug/config_dump?=proxyID=webapp.istioninaction

## 이 파일럿이 관리하는 프록시들을 표시한다.
curl -s http://localhost:8080/debug/syncz | jq
...
  {
    "cluster_id": "Kubernetes",
    "proxy": "webapp-7685bcb84-lwsvj.istioinaction",
    "istio_version": "1.17.8",
    "cluster_sent": "ff5e6b2c-e857-4e12-b17e-46ad968567f4",
    "cluster_acked": "ff5e6b2c-e857-4e12-b17e-46ad968567f4",
    "listener_sent": "7280c908-010d-4788-807f-7138e74fe72e",
    "listener_acked": "7280c908-010d-4788-807f-7138e74fe72e",
    "route_sent": "2a1916c3-9c05-4ce5-8cfa-d777105b9205",
    "route_acked": "2a1916c3-9c05-4ce5-8cfa-d777105b9205",
    "endpoint_sent": "dffacd32-2674-4e39-8e76-17016ff32514",
    "endpoint_acked": "dffacd32-2674-4e39-8e76-17016ff32514"
  },
...
```

![]({{ site.url }}/img/post/devops/study/istio/6/202505060950.png)

### ControlZ 인터페이스
- 파일럿 프로세스 정보 확인 및 일부 설정 가능
- 주요 기능
	- 로깅 범위 설정: 범위별 로그 레벨 조정 가능
	- 메모리 사용량: Go 런타임 기준 사용량 표시
	- 환경 변수: 현재 설정된 환경 변수 목록
	- 프로세스 정보: PID, 경로, 실행 인자
	- 메트릭 확인: Pilot 메트릭 직접 조회
	- 시그널 전송: SIGUSR1 시그널 테스트용

```bash
kubectl -n istio-system port-forward deploy/istiod 9876
open http://localhost:9876
```

![]({{ site.url }}/img/post/devops/study/istio/6/20250506085200.png)
