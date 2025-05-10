---
layout: post
section-type: post
title: ServiceMesh - Istio - Week5
category: devops
tags: ["k8s", "istio", "servicemesh"]
---

# chap9. 마이크로서비스 통신 보호하기

## 애플리케이션 네트워크 보안의 필요성
애플리케이션 보안은 인가되지 않은 접근으로부터 데이터를 보호하고, 네트워크 도청을 방지하기 위해 전송 중 암호화를 필요로 한다.
- 인증: 사용자나 서비스의 신원을 확인하는 과정
- 인가: 인증된 주체에게 특정 작업을 허용하거나 거부

### 서비스 간 인증
이스티오는 SPIFFE 프레임워크를 기반으로 서비스 ID를 자동 부여하며, 인증서는 서비스 간 상호 인증과 암호화된 통신에 사용된다.

### 최종 사용자 인증
사용자는 인증 서버를 통해 로그인 후, JWT나 쿠키 같은 자격 증명을 서비스에 전달하고, 서비스는 이를 검증한다.

### 인가
인가는 인증 이후 수행되며, 서비스나 사용자의 ID에 따라 접근 권한이 결정된다. 이스티오는 세분화된 인가 정책을 제공한다.

### 모놀리스와 마이크로서비스의 보안 비교
- 모놀리스: IP 기반 인증이 가능
- 마이크로서비스: 동적 환경에서는 IP 인증이 어려워 SPIFFE 기반 ID 필요

### 이스티오의 SPIFFE 구현 방식
- SPIFFE ID 형식: `spiffe://trust-domain/path`
- ID는 서비스 어카운트를 기반으로 하며, SVID(X.509 인증서)로 인코딩되어 전송 암호화에 사용됨

### 이스티오 보안 리소스 요약
- **PeerAuthentication**: 서비스 간 인증 구성
- **RequestAuthentication**: 최종 사용자 JWT 인증
- **AuthorizationPolicy**: 인증 정보를 기반으로 요청 인가 수행

![]({{ site.url }}/img/post/devops/study/istio/5/20250430201417.png)

- 인증 정보를 필터 메타데이터로 저장하여 인가 판단 기준으로 사용
- 인증 → 정보 추출 → 인가의 흐름으로 구성됨

## 자동 상호 TLS
이스티오는 사이드카 프록시를 통해 서비스 간 TLS 암호화를 기본으로 제공하며, 인증서의 발급과 갱신은 자동화되어 있다.
![]({{ site.url }}/img/post/devops/study/istio/5/20250430202501.png)

### 환경 설정하기
- mTLS 기능 실습을 위한 3가지 서비스 준비

![]({{ site.url }}/img/post/devops/study/istio/5/20250430212445.png)

```bash
# catalog와 webapp 배포
kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction
kubectl apply -f services/webapp/kubernetes/webapp.yaml -n istioinaction

# webapp과 catalog의 gateway, virtualservice 설정
kubectl apply -f services/webapp/istio/webapp-catalog-gw-vs.yaml -n istioinaction

# default 네임스페이스에 sleep 앱 배포
cat ch9/sleep.yaml
...
    spec:
      serviceAccountName: sleep
      containers:
      - name: sleep
        image: governmentpaas/curl-ssl
        command: ["/bin/sleep", "3650d"]
        imagePullPolicy: IfNotPresent
        volumeMounts:
        - mountPath: /etc/sleep/tls
          name: secret-volume
      volumes:
      - name: secret-volume
        secret:
          secretName: sleep-secret
          optional: true

kubectl apply -f ch9/sleep.yaml -n default

# 확인
kubectl get deploy,pod,sa,svc,ep
kubectl get deploy,svc -n istioinaction
kubectl get gw,vs -n istioinaction
```

- 기본 통신 확인: 레거시 sleep 워크로드 -> webapp 워크로드로 평문 요청 실행

```bash
# 요청 실행
kubectl exec deploy/sleep -c sleep -- curl -s webapp.istioinaction/api/catalog -o /dev/null -w "%{http_code}\n"

# 반복 요청
watch 'kubectl exec deploy/sleep -c sleep -- curl -s webapp.istioinaction/api/catalog -o /dev/null -w "%{http_code}\n"'
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250507220524.png)

- 응답이 성공했다는 것 -> 서비스들이 올바르게 준비됨
	- webapp 서비스가 sleep 서비스의 평문(HTTP) 요청을 받아들임
- 이스티오는 기본적으로 평문(HTTP) 요청을 허용한다.
	- 모든 워크로드를 메시로 옮길 때까지 서비스 중단을 일으키지 않고
	- 점진적으로 서비스 메시를 채택하기 위함이다.
- PeerAuthentication으로 평문 트래픽을 금지할 수 있다.

## 이스티오의 PeerAuthentication 리소스 이해하기
PeerAuthentication 리소스는 서비스 간 트래픽 인증 방식을 지정하며, 다음과 같은 모드를 제공한다:
- `STRICT`: 암호화된 트래픽만 허용
- `PERMISSIVE`: 암호화와 일반 트래픽 모두 허용

적용 범위는 전체 메시, 네임스페이스, 워크로드 수준으로 설정할 수 있다.

### 메시 범위 정책으로 모든 미인증 트래픽 거부하기
다음 정책을 메시 전체에 적용해 모든 미인증 트래픽을 차단할 수 있다.
- PeerAuthentication 리소스를 STRICT 모드로 설정

```bash
cat ch9/meshwide-strict-peer-authn.yaml 
apiVersion: "security.istio.io/v1beta1"
kind: "PeerAuthentication"
metadata:
  name: "default" # Mesh-wide policies must be named "default"
  namespace: "istio-system" # Istio installation namespace
spec:
  mtls:
    mode: STRICT # mutual TLS mode

# 적용
kubectl apply -f ch9/meshwide-strict-peer-authn.yaml -n istio-system

# 요청 실행
kubectl exec deploy/sleep -c sleep -- curl -s http://webapp.istioinaction/api/catalog -o /dev/null -w "%{http_code}\n"
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250507221545.png)

- 평문 요청이 거부되었다.

### 상호 인증하지 않은 트래픽 허용하기

```bash
cat << EOF | kubectl apply -f -
apiVersion: "security.istio.io/v1beta1"
kind: "PeerAuthentication"
metadata:
  name: "default"             # Uses the "default" naming convention so that only one namespace-wide resource exists
  namespace: "istioinaction"  # Specifies the namespace to apply the policy
spec:
  mtls:
    mode: PERMISSIVE          # PERMISSIVE allows HTTP traffic.
EOF

# 요청 실행
kubectl exec deploy/sleep -c sleep -- curl -s http://webapp.istioinaction/api/catalog -o /dev/null -w "%{http_code}\n"

# 확인
kubectl get PeerAuthentication -A 
NAMESPACE       NAME      MODE         AGE
istio-system    default   STRICT       2m51s
istioinaction   default   PERMISSIVE   7s
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250507221910.png)
- 이렇게는 사용하지 말자.
- 미인증 트래픽은 sleep 워크로드에서 webapp으로 향하는 것만 허용
- catalog 워크로드에는 STRICT 상호 인증을 계속 유지
	- 이렇게 하면 보안이 뚫렸을때 공격 범위를 좁힐 수 있다.

```bash
# 다음 실습을 위해 삭제 : PeerAuthentication 단축어 pa
kubectl delete pa default -n istioinaction
```

### 워크로드별 PeerAuthentication 정책 적용하기

```bash
# istiod 는 PeerAuthentication 리소스 생성을 수신하고, 이 리소스를 엔보이용 설정으로 변환하며, 
# LDS(Listener Discovery Service)를 사용해 서비스 프록시에 적용
docker exec -it myk8s-control-plane istioctl proxy-status

cat ch9/workload-permissive-peer-authn.yaml
apiVersion: "security.istio.io/v1beta1"
kind: "PeerAuthentication"
metadata:
  name: "webapp"
  namespace: "istioinaction"
spec:
  selector:
    matchLabels:
      app: "webapp"  # 레이블이 일치하는 워크로드만 PERMISSIVE로 동작
  mtls:
    mode: PERMISSIVE

kubectl apply -f ch9/workload-permissive-peer-authn.yaml
kubectl get pa -A

# sleep -> webapp (succes)
kubectl logs -n istioinaction -l app=webapp -c webapp -f
kubectl exec deploy/sleep -c sleep -- curl -s http://webapp.istioinaction/api/catalog -o /dev/null -w "%{http_code}\n"

# sleep -> catalog (fail)
kubectl logs -n istioinaction -l app=catalog -c catalog -f
kubectl exec deploy/sleep -c sleep -- curl -s http://catalog.istioinaction/api/items -o /dev/null -w "%{http_code}\n"
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250507223640.png)
![]({{ site.url }}/img/post/devops/study/istio/5/20250430230448.png)

### 두 가지 추가적인 상호 인증 모드
- `STRICT`, `PERMISSIVE` 외 2개의 모드
	- `UNSET` : 부모의 PeerAuthentication 정책을 상속
	- `DISABLE` : 트래픽을 터널링하지 않음. 서비스로 직접 보냄
- 상호 인증 트래픽, 평문 트래픽 등 워크로드로 터널링항 트래픽 유형을 지정하거나
- 요청을 프록시로 보내지 않고 애플리케이션으로 바로 포워딩할 수 있다.

### tcpdump로 서비스 간 트래픽 스니핑하기
- 이스티오 프록시에는 tcpdump가 설치되어 있다.
- tcpdump는 보안 때문에 권한 privileged permission이 필요하다.(기본값: false)
- `values.global.proxy.priviliged`를 `true`로 설정하여 이스티오를 업데이트한다.

```bash
# 확인
kubectl get istiooperator -n istio-system installed-state -o yaml
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250507224500.png)

```bash
kubectl get pod -n istioinaction -l app=webapp -o json
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250507224906.png)

```bash
istioctl install -y --set profile=demo \
--set values.global.proxy.privileged=true

# 사이드카 프록시를 주입하도록 업데이트 한 후 webapp 워크로드를 다시 만들어줘야 한다.
k delete po -l app=webapp -n istioinaction

# 확인
kubectl get istiooperator -n istio-system installed-state -o yaml
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250508202614.png)

```
# 권한을 확인해보자.
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- whoami
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- id
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- sudo whoami
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- sudo tcpdump -h
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250508202823.png)

- 파드 트래픽을 스니핑 해보자

```bash
# 패킷 모니터링 실행 해두기
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy \
  -- sudo tcpdump -l --immediate-mode -vv -s 0 '(((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0) and not (port 53)'
# -l : 표준 출력(stdout)을 라인 버퍼 모드로 설정. 터미널에서 실시간으로 결과를 보기 좋게 함 (pipe로 넘길 때도 유용).
# --immediate-mode : 커널 버퍼에서 패킷을 모아서 내보내지 않고, 캡처 즉시 사용자 공간으로 넘김 → 딜레이 최소화.
# -vv : verbose 출력. 패킷에 대한 최대한의 상세 정보를 보여줌.
# -s 0 : snap length를 0으로 설정 → 패킷 전체 내용을 캡처. (기본값은 262144 bytes, 예전 버전에서는 68 bytes로 잘렸음)
# '(((ip[2:2] - ((ip[0]&0xf)<<2)) - ((tcp[12]&0xf0)>>2)) != 0) and not (port 53)' : DNS패킷 제외하고 TCP payload 길이가 0이 아닌 패킷만 캡처
# 즉, SYN/ACK/FIN 같은 handshake 패킷(데이터 없는 패킷) 무시, 실제 데이터 있는 패킷만 캡처
# 결론 : 지연 없이, 전체 패킷 내용을, 매우 자세히 출력하고, DNS패킷 제외하고 TCP 데이터(payload)가 1 byte 이상 있는 패킷만 캡처

# 요청 실행
kubectl exec deploy/sleep -c sleep -- curl -s webapp.istioinaction/api/catalog -o /dev/null -w "%{http_code}\n"

## (1) sleep -> webapp 호출 HTTP
11:32:01.624805 IP (tos 0x0, ttl 63, id 11453, offset 0, flags [DF], proto TCP (6), length 146)
    10-10-0-14.sleep.default.svc.cluster.local.40514 > webapp-7685bcb84-jttmh.http-alt: Flags [P.], cksum 0x14bc (incorrect -> 0x7295), seq 1914134141:1914134235, ack 3484444467, win 512, options [nop,nop,TS val 3349047754 ecr 1349340000], length 94: HTTP, length: 94
	GET /api/catalog HTTP/1.1
	Host: webapp.istioinaction
	User-Agent: curl/8.5.0
	Accept: */*

## (2) webapp -> catalog 호출 HTTPS
11:32:01.629654 IP (tos 0x0, ttl 64, id 3135, offset 0, flags [DF], proto TCP (6), length 1304)
    webapp-7685bcb84-jttmh.38974 > 10-10-0-21.catalog.istioinaction.svc.cluster.local.3000: Flags [P.], cksum 0x1949 (incorrect -> 0xfdd9), seq 6001:7253, ack 9142, win 871, options [nop,nop,TS val 880716688 ecr 1442128005], length 1252

## (3) catalog -> webapp 응답 HTTPS
11:32:01.647257 IP (tos 0x0, ttl 63, id 29504, offset 0, flags [DF], proto TCP (6), length 1789)
    10-10-0-21.catalog.istioinaction.svc.cluster.local.3000 > webapp-7685bcb84-jttmh.38974: Flags [P.], cksum 0x1b2e (incorrect -> 0x8ae6), seq 9142:10879, ack 7253, win 729, options [nop,nop,TS val 1442213662 ecr 880716688], length 1737

## (4) webapp -> sleep 응답 HTTP
11:32:01.648333 IP (tos 0x0, ttl 64, id 4548, offset 0, flags [DF], proto TCP (6), length 663)
    webapp-7685bcb84-jttmh.http-alt > 10-10-0-14.sleep.default.svc.cluster.local.40514: Flags [P.], cksum 0x16c1 (incorrect -> 0x0f22), seq 1:612, ack 94, win 512, options [nop,nop,TS val 1349340024 ecr 3349047754], length 611: HTTP, length: 611
	HTTP/1.1 200 OK
	content-length: 357
	content-type: application/json; charset=utf-8
	date: Thu, 08 May 2025 11:32:01 GMT
	x-envoy-upstream-service-time: 22
	server: istio-envoy
	x-envoy-decorator-operation: webapp.istioinaction.svc.cluster.local:80/*

	[{"id":1,"color":"amber","department":"Eyewear","name":"Elinor Glasses","price":"282.00"},{"id":2,"color":"cyan","department":"Clothing","name":"Atlas Shirt","price":"127.00"},{"id":3,"color":"teal","department":"Clothing","name":"Small Metal Shoes","price":"232.00"},{"id":4,"color":"red","department":"Watches","name":"Red Dragon Watch","price":"232.00"}] [|http]

# 밑의 방법으로 해도 된다.
kubectl get svc,ep -n istioinaction
NAME              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/catalog   ClusterIP   10.200.1.243   <none>        80/TCP    11m
service/webapp    ClusterIP   10.200.1.240   <none>        80/TCP    11m

NAME                ENDPOINTS         AGE
endpoints/catalog   10.10.0.21:3000   11m
endpoints/webapp    10.10.0.22:8080   11m

kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy \
  -- sudo tcpdump -l --immediate-mode -vv -s 0 'tcp port 3000 or tcp port 8080'

# 요청 실행
kubectl exec deploy/sleep -c sleep -- curl -s webapp.istioinaction/api/catalog -o /dev/null -w "%{http_code}\n"
```

### 워크로드 ID가 워크로드 서비스 어카운트에 연결돼 있는지 확인하기

```bash
# (참고) 패킷 모니터링 : 아래 openssl 실행 시 동작 확인
kubectl exec -it -n istioinaction deploy/catalog -c istio-proxy \
  -- sudo tcpdump -l --immediate-mode -vv -s 0 'tcp port 3000'

# catalog 의 X.509 인증서 내용 확인
kubectl -n istioinaction exec deploy/webapp -c istio-proxy -- ls -l /var/run/secrets/istio/root-cert.pem

kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- openssl x509 -in /var/run/secrets/istio/root-cert.pem -text -noout

kubectl -n istioinaction exec deploy/webapp -c istio-proxy -- openssl -h
kubectl -n istioinaction exec deploy/webapp -c istio-proxy -- openssl s_client -h
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250508210058.png)

```
# openssl s_client → TLS 서버에 연결해 handshake와 인증서 체인을 보여줌
# -showcerts → 서버가 보낸 전체 인증서 체인 출력
# -connect catalog.istioinaction.svc.cluster.local:80 → Istio 서비스 catalog로 TCP 80 연결
# -CAfile /var/run/secrets/istio/root-cert.pem → Istio의 root CA로 서버 인증서 검증
# 결론 : Envoy proxy에서 catalog 서비스로 연결하여 TLS handshake 및 인증서 체인 출력 후 사람이 읽을 수 있는 형식으로 해석
kubectl -n istioinaction exec deploy/webapp -c istio-proxy \
  -- openssl s_client -showcerts \
  -connect catalog.istioinaction.svc.cluster.local:80 \
  -CAfile /var/run/secrets/istio/root-cert.pem | \
  openssl x509 -in /dev/stdin -text -noout
...
        Validity 
            Not Before: May  1 09:55:10 2025 GMT # 유효기간 1일 2분
            Not After : May  2 09:57:10 2025 GMT
        ...
        X509v3 extensions:
            X509v3 Extended Key Usage:
                TLS Web Server Authentication, TLS Web Client Authentication # 사용처 : 웹서버, 웹클라이언트
            ...
            X509v3 Subject Alternative Name: critical
                URI:spiffe://cluster.local/ns/istioinaction/sa/catalog # SPIFFE ID 확인

# catalog 파드의 서비스 어카운트 확인
kubectl describe pod -n istioinaction -l app=catalog | grep 'Service Account'
Service Account:  catalog
```

루트 인증서 서명 확인

```bash
# webapp.istio-proxy 쉘 접속
kubectl -n istioinaction exec -it deploy/webapp -c istio-proxy -- /bin/bash
-----------------------------------------------
# 인증서 검증
openssl verify -CAfile /var/run/secrets/istio/root-cert.pem \
  <(openssl s_client -connect \
  catalog.istioinaction.svc.cluster.local:80 -showcerts 2>/dev/null)
/dev/fd/63: OK
# 검증에 성공 시 OK 메시지 출력: 이스티오 CA가 인증서에 서명했으며, 내부 데이터가 믿을 수 있다는 것임을 알려줌.

exit
-----------------------------------------------
```

## 서비스 간 트래픽 인가하기
- 인가: 인증된 주체가 리소스 접근, 편집, 삭제 같은 작업을 수행하도록 허용됐는지 정의하는 절차
- 정책: 인증된 주체(누가)와 인가(무엇)을 결합해 형성되며, 누가 무슨 일을 할 수 있는지 정의

- 공격을 당했다면??

![]({{ site.url }}/img/post/devops/study/istio/5/20250501153927.png)

- 이스티오는 AuthorizationPolicy로 접근 정책을 정의한다.
	- 범위
		- 서비스 메시 전체
		- 네임스페이스
		- 워크로드별

#### 인가 정책의 속성
- 사이드카 프록시가 인가 or 집행 엔진이다.
	- 서비스 프록시가 요청을 허용/거절 여부를 판단하는 정택을 모두 포함하기 때문
	- 모든 결정이 프록시에서 직접 내려진다.
- AuthorizationPolicy로 정책을 정의한다.
	- istiod가 새 AuthorizationPolicy가 클러스터에 적용됐음을 확인
	- 다른 이스티오 리소스들처럼 해당 리소스로 데이터 플레인 프록시를 처리하고 업데이트한다.

```yaml
apiVersion: "security.istio.io/v1beta1"
kind: "AuthorizationPolicy"
metadata:
  name: "allow-catalog-requests-in-web-app"
  namespace: istioinaction
spec:
  selector:
    matchLabels:
      app: webapp
  actino: ALLOW
  rules:
  - to:
    - operation:
        path: ["/api/catalog"]
```

#### 인가 정책의 속성
- selector
	- 정책을 적용할 워크로드 부분집합을 정의한다.
- action
	- 이 정책을 허용(ALLOW) / 거부(DENY) /  커스텀(CUSTOM)인지 지정한다.
	- 규칙 중 하나가 요청과 일치해야만 적용된다.
- rules
	- 정책을 활성화할 요청을 식별하는 규칙 목록을 정의한다.

#### 인가 정책 규칙 이해하기
- 인가 정책 규칙은 커넥션의 출처(source)를 지정한다.
- 단일 규칙의 필드
	- from: 요청의 출처를 다음 유형 중 하나로 지정한다.
		- principals
			- 출처 ID(mTLS의 SPIFFE ID) 목록
			- 요청이 주체(principal) 집합에서 온 것이 아니면 부정 속성인 notPrincipals가 적용된다.
			- 이 기능을 작동하려면 서비스가 상호 인증해야 한다.
		- namespaces
			- 출처 네임스페이스와 비교할 네임스페이스 목록
			- 출처 네임스페이스는 참가자의 SVID에서 가져온다.
			- 그래서, 작동하려면 mTLS가 활성화돼야 한다.
		- ipBlocks
			- 출처 IP 주소와 비교할 단일 IP 주소나 CIDR 범위 목록
	- to: 요청의 작업을 지정하며, 호스트나 요청의 메서드 등이 있다.
	- when: 규칙이 부합한 후 충족해야 하는 조건 목록을 지정한다.

### 작업 공간 설정하기
```bash
# 9.2.1 에서 이미 배포함
kubectl -n istioinaction apply -f services/catalog/kubernetes/catalog.yaml
kubectl -n istioinaction apply -f services/webapp/kubernetes/webapp.yaml
kubectl -n istioinaction apply -f services/webapp/istio/webapp-catalog-gw-vs.yaml
kubectl -n default apply -f ch9/sleep.yaml

# gw,vs 확인 
kubectl -n istioinaction get gw,vs

# PeerAuthentication 설정 : 앞에서 이미 설정함
cat ch9/meshwide-strict-peer-authn.yaml
apiVersion: "security.istio.io/v1beta1"
kind: "PeerAuthentication"
metadata:
  name: "default"
  namespace: "istio-system"
spec:
  mtls:
    mode: STRICT
    
kubectl -n istio-system apply -f ch9/meshwide-strict-peer-authn.yaml
kubectl get peerauthentication -n istio-system

cat ch9/workload-permissive-peer-authn.yaml
apiVersion: "security.istio.io/v1beta1"
kind: "PeerAuthentication"
metadata:
  name: "webapp"
  namespace: "istioinaction"
spec:
  selector:
    matchLabels:
      app: webapp 
  mtls:
    mode: PERMISSIVE

kubectl -n istioinaction apply -f ch9/workload-permissive-peer-authn.yaml
kubectl get peerauthentication -n istioinaction
```

### 워크로드에 정책 적용시 동작 확인
- 워크로드에 하나 이상의 ALLOW 인가 정책이 적용되면
	- 모든 트래픽에서 해당 워크로드로의 접근은 기본적으로 DENY
- 트래픽을 받아들이려면, ALLOW 정책이 최소 하나는 부합해야 한다.

```bash
# cat ch9/allow-catalog-requests-in-web-app.yaml
apiVersion: "security.istio.io/v1beta1"
kind: "AuthorizationPolicy"
metadata:
  name: "allow-catalog-requests-in-web-app"
  namespace: istioinaction
spec:
  selector:
    matchLabels:
      app: webapp # 워크로드용 셀렉터 Selector for workloads
  rules:
  - to:
    - operation:
        paths: ["/api/catalog*"] # 요청을 경로 /api/catalog 와 비교한다 Matches requests with the path /api/catalog
  action: ALLOW # 일치하면 허용한다 If a match, ALLOW

# 로그
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f

# 적용 전 확인 
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction/api/catalog
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction/hello/world # 404 리턴

# AuthorizationPolicy 리소스 적용
kubectl apply -f ch9/allow-catalog-requests-in-web-app.yaml
kubectl get authorizationpolicy -n istioinaction

# 
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/webapp.istioinaction --port 15006
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/webapp.istioinaction --port 15006 -o json > webapp-listener.json
...
          {
              "name": "envoy.filters.http.rbac",
              "typedConfig": {
                  "@type": "type.googleapis.com/envoy.extensions.filters.http.rbac.v3.RBAC",
                  "rules": {
                      "policies": {
                          "ns[istioinaction]-policy[allow-catalog-requests-in-web-app]-rule[0]": {
                              "permissions": [
                                  {
                                      "andRules": {
                                          "rules": [
                                              {
                                                  "orRules": {
                                                      "rules": [
                                                          {
                                                              "urlPath": {
                                                                  "path": {
                                                                      "prefix": "/api/catalog"
                                                                  }
                                                              }
                                                          }
                                                      ]
                                                  }
                                              }
                                          ]
                                      }
                                  }
                              ],
                              "principals": [
                                  {
                                      "andIds": {
                                          "ids": [
                                              {
                                                  "any": true
                                              }
                                          ]
                                      }
                                  }
                              ]
                          }
                      }
                  },
                  "shadowRulesStatPrefix": "istio_dry_run_allow_" #  실제로 차단하지 않고, 정책이 적용됐을 때 통계만 수집 , istio_dry_run_allow_로 prefix된 메트릭 생성됨
              }
          },
...

# 로그 : 403 리턴 체크!
docker exec -it myk8s-control-plane istioctl proxy-config log deploy/webapp -n istioinaction --level rbac:debug
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
[2025-05-03T10:08:52.918Z] "GET /hello/world HTTP/1.1" 403 - rbac_access_denied_matched_policy[none] - "-" 0 19 0 - "-" "curl/8.5.0" "b272b991-7a79-9581-bb14-55a6ee705311" "webapp.istioinaction" "-" inbound|8080|| - 10.10.0.3:8080 10.10.0.13:50172 - -

# 적용 후 확인
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction/api/catalog
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction/hello/world # 403 리턴
RBAC: access denied
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250508212535.png)
![]({{ site.url }}/img/post/devops/study/istio/5/20250508215705.png)
![]({{ site.url }}/img/post/devops/study/istio/5/20250508215839.png)

```
# 다음 실습을 위해 정책 삭제
kubectl delete -f ch9/allow-catalog-requests-in-web-app.yaml
```

### 전체 정책으로 기본적으로 모든 요청 거부하기

```bash
# cat ch9/policy-deny-all-mesh.yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: deny-all
  namespace: istio-system # 이스티오를 설치한 네임스페이스의 정책은 메시의 모든 워크로드에 적용된다
spec: {} # spec 이 비어있는 정책은 모든 요청을 거부한다

# 적용 전 확인 
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction/api/catalog
curl -s http://webapp.istioinaction.io:30000/api/catalog

# 정책 적용
kubectl apply -f ch9/policy-deny-all-mesh.yaml
kubectl get authorizationpolicy -A

# 적용 후 확인 1
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction/api/catalog
...
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
[2025-05-03T14:45:31.051Z] "GET /api/catalog HTTP/1.1" 403 - rbac_access_denied_matched_policy[none] - "-" 0 19 0 - "-" "curl/8.5.0" "f1ec493b-cc39-9573-b3ad-e37095bbfaeb" "webapp.istioinaction" "-" inbound|8080|| - 10.10.0.3:8080 10.10.0.13:60780 - -

# 적용 후 확인 2
curl -s http://webapp.istioinaction.io:30000/api/catalog
...
kubectl logs -n istio-system -l app=istio-ingressgateway -f
...

# cat ch9/policy-allow-all-mesh.yaml                         
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-all
  namespace: istio-system
spec: 
  rules: 
  - {}
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250508214737.png)

### 특정 네임스페이스에서 온 요청 허용하기

- `source.namespace` 으로 특정 네임스페이스 트래픽 허용

```bash
cat << EOF | kubectl apply -f -
apiVersion: "security.istio.io/v1beta1"
kind: "AuthorizationPolicy"
metadata:
  name: "webapp-allow-view-default-ns"
  namespace: istioinaction # istioinaction의 워크로드
spec:
  rules:
  - from: # default 네임스페이스에서 시작한
    - source:
        namespaces: ["default"]
    to:   # HTTP GET 요청에만 적용 
    - operation:
        methods: ["GET"]
EOF

kubectl get AuthorizationPolicy -A
NAMESPACE       NAME                           AGE
istio-system    deny-all                       11h
istioinaction   webapp-allow-view-default-ns   11h

docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/webapp.istioinaction --port 15006 -o json
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250508221227.png)

```
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f

# 호출 테스트
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction/api/catalog
RBAC: access denied%
```
- sleep 서비스는 레거시 워크로드
	- 사이드카가 없으므로, ID도 없다.
	- 적, webapp 프록시는 default ns의 워크로드에서 온 것인지 알 수가 없다.
- 해결방법
	- sleep 서비스에 서비스 프록시 주입(권장)
	- webapp에서 미인증 요청 허용

```bash
kubectl label ns default istio-injection=enabled
kubectl delete pod -l app=sleep

# 이제 sleep의 네임스페이스 확인 가능
docker exec -it myk8s-control-plane istioctl proxy-status
NAME                                                   CLUSTER        CDS        LDS        EDS        RDS          ECDS         ISTIOD                    VERSION
sleep-6f8cfb8c8f-8nkf5.default                         Kubernetes     SYNCED     SYNCED     SYNCED     SYNCED       NOT SENT     istiod-8d74787f-7csln     1.17.8
...

# 호출 테스트 : webapp
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction # default -> webapp 은 성공
...

kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction/api/catalog 
error calling Catalog service

docker exec -it myk8s-control-plane istioctl proxy-config log deploy/webapp -n istioinaction --level rbac:debug
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f # webapp -> catalog 는 deny-all 로 거부됨
[2025-05-08T13:19:20.172Z] "GET /items HTTP/1.1" 403 - via_upstream - "-" 0 19 0 0 "-" "beegoServer" "75b6ef62-c054-9b9a-92d0-65b53e4f422a" "catalog.istioinaction:80" "10.10.0.21:3000" outbound|80||catalog.istioinaction.svc.cluster.local 10.10.0.22:49444 10.200.1.243:80 10.10.0.22:54730 - default
[2025-05-08T13:19:20.170Z] "GET /api/catalog HTTP/1.1" 500 - via_upstream - "-" 0 29 2 2 "-" "curl/8.5.0" "75b6ef62-c054-9b9a-92d0-65b53e4f422a" "webapp.istioinaction" "10.10.0.22:8080" inbound|8080|| 127.0.0.6:50479 10.10.0.22:8080 10.10.0.23:45516 outbound_.80_._.webapp.istioinaction.svc.cluster.local default

# 호출 테스트 : catalog
kubectl logs -n istioinaction -l app=catalog -c istio-proxy -f
kubectl exec deploy/sleep -- curl -sSL catalog.istioinaction/items # default -> catalog 은 성공


# 다음 실습을 위해 default 네임스페이스 원복
kubectl label ns default istio-injection-
kubectl rollout restart deploy/sleep

docker exec -it myk8s-control-plane istioctl proxy-status
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction # 거부 확인
```

### 미인증 레거시 워크로드에서 온 요청 허용하기
- `from` 필드를 삭제
- webapp에만 적용하기 위해 app:webapp 셀렉터 추가
	- catalog 서비스는 여전히 상호 인증이다.

```bash
# cat ch9/allow-unauthenticated-view-default-ns.yaml
apiVersion: "security.istio.io/v1beta1"
kind: "AuthorizationPolicy"
metadata:
  name: "webapp-allow-unauthenticated-view-default-ns"
  namespace: istioinaction
spec:
  selector:
    matchLabels:
      app: webapp
  rules:
    - to:
      - operation:
          methods: ["GET"]
```

```bash
#
kubectl apply -f ch9/allow-unauthenticated-view-default-ns.yaml
kubectl get AuthorizationPolicy -A
NAMESPACE       NAME                                           AGE
istio-system    deny-all                                       21m
istioinaction   webapp-allow-unauthenticated-view-default-ns   8s
istioinaction   webapp-allow-view-default-ns                   16m

# 여러개의 정책이 적용 시에 우선순위는?
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/webapp.istioinaction --port 15006 -o json | jq
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250508222503.png)

```
# 호출 테스트 : webapp
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction # default -> webapp 은 성공
...

kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f # webapp -> catalog 는 deny-all 로 거부됨
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction/api/catalog 
error calling Catalog service

# (옵션) 호출 테스트 : catalog
kubectl logs -n istioinaction -l app=catalog -c istio-proxy -f
kubectl exec deploy/sleep -- curl -sSL catalog.istioinaction/items
```

### 특정 서비스 어카운트에서 온 요청 허용하기
- 트래픽이 webapp 서비스에서 왔는지 인증하는 간단한 방법
	- 주입된 서비스 어카운트를 사용
- 서비스 어카운트 정보는 SVID에 인코딩돼 있으며, 상호 인증 중에 그 정보를 검증하고 필터 메타데이터에 저장한다.
- ex. catalog 서비스가 필터 메타데이터를 사용햐 서비스 어카운트가 webapp인 워크로드에서 온 트래픽만 허용

```bash
# cat ch9/catalog-viewer-policy.yaml
apiVersion: "security.istio.io/v1beta1"
kind: "AuthorizationPolicy"
metadata:
  name: "catalog-viewer"
  namespace: istioinaction
spec:
  selector:
    matchLabels:
      app: catalog
  rules:
  - from:
    - source: 
        principals: ["cluster.local/ns/istioinaction/sa/webapp"] # Allows requests with the identity of webapp
    to:
    - operation:
        methods: ["GET"]
```

```bash
kubectl apply -f ch9/catalog-viewer-policy.yaml
kubectl get AuthorizationPolicy -A
NAMESPACE       NAME                                           AGE
istio-system    deny-all                                       13h
istioinaction   catalog-viewer                                 10s
istioinaction   webapp-allow-unauthenticated-view-default-ns   61m
istioinaction   webapp-allow-view-default-ns                   12h

docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/catalog.istioinaction --port 15006 -o json
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250508223102.png)

```
# 호출 테스트 : sleep --(미인증 레거시 허용)--> webapp --(principals webapp 허용)--> catalog
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction
kubectl exec deploy/sleep -- curl -sSL webapp.istioinaction/api/catalog 
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
kubectl logs -n istioinaction -l app=catalog -c istio-proxy -f

# (옵션) 호출 테스트 : catalog
kubectl exec deploy/sleep -- curl -sSL catalog.istioinaction/items
...
```
- 워크로드 ID가 도난시 피해 범위를 최소한으로 제한하는 엄격한 인가 정책을 갖고 있어야 한다.

### 정책의 조건부 적용
- 특정 조건이 충족되는 경우에만 적용
	- ex. 사용자가 관리자라면 모든 작업을 허용
		- 토큰은 요청 주체 `auth@istioinaction.io/*`가 발급한 것
		- JWT에 값이 'admin'인 group claim이 포함되야 함
		- 위 2가지 조건이 충족해야 요청을 허용
- 인가 정책의 `when` 속성으로 구현

```yaml
apiVersion: "security.istio.io/v1beta1"
kind: "AuthorizationPolicy"
metadata:
  name: "allow-mesh-all-ops-admin"
  namespace: istio-system
spec:
  rules:
  - from:
    - source:
        requestPrincipals: ["auth@istioinaction.io/*"]
    when:
    - key: request.auth.claims[groups] # 이스티오 속성을 지정한다
      values: ["admin"] # 반드시 일치해야 하는 값의 목록을 지정한다
```
- `notValues`으로 반대 정의도 가능하다.
### 값 비교 표현식 이해하기
- 일치
	- ex. GET은 값이 정확히 일치해야 한다.
- 접두사 비교
	- ex. `/api/catalog*`는 `/api/catalog/1` 과 같이 이 접두사로 시작하는 모든 값에 부합한다.
- 접미사 비교
	- ex. `*.istioinaction.io`는 `login.istioinaction.io`와 같이 모든 서브도메인에 부합한다.
- 존재성 비교
	- 모든 값에 부합하며 `*`로 표기
	- 이는 필드가 존재해야 하지만, 값은 중요하지 않아 어떤 값이든 괜찮음을 의미한다.

```yaml
apiVersion: "security.istio.io/v1beta1"
kind: "AuthorizationPolicy"
metadata:
  name: "allow-mesh-all-ops-admin"
  namespace: istio-system
spec:
  rules: 
  - from: # 첫 번째 규칙
    - source:
        principals: ["cluster.local/ns/istioinaction/sa/webapp"]
    - source:
        namespace: ["default"]
    to:
    - operation:
        methods: ["GET"]
        paths: ["/users*"]
    - operation:
        methods: ["POST"]
        paths: ["/data"]
    when:
    - key: request.auth.claims[group]
      values: ["beta-tester", "admin", "developer"]
  - to: # 두 번째 규치
    - operation:
        paths: ["*.html", "*.js", "*.png"]
```

#### 인가정책이 평가되는 순서

![]({{ site.url }}/img/post/devops/study/istio/5/20250508223806.png)
> https://istio.io/v1.17/docs/concepts/security/#implicit-enablement

많은 솔루션이 priority 필드를 사용해 순서를 정의한다.
- 정책 평가에 따른 접근법
	1. CUSTOM 정책이 가장 먼저 평가된다. 추후 외부 인가 서버와 통합시 CUSTOM 정책의 사례를 볼 수 있다.
	2. DENY 정책이 평가된다. 일치하는 DENY 정책이 없으면...
	3. ALLOW 정책이 평가된다. 일치하는 것이 있으면 허용. 아니면...?
	4. 일반 정책의 존재 유무에 따라 2가지 결과가 나타난다.
		- 일반 정책이 존재하면, 일반 정책이 요청 승인 여부를 결정
		- 읿반 정책이 없으면?
			- ALLOW 정책이 없어면 허용
			- ALLOW 정책이 있지만 아무것도 해당되지 않으면 거부

![]({{ site.url }}/img/post/devops/study/istio/5/20250501212224.png)

## 최종 사용자 인증 및 인가
### JWT란?
- JWT
	- 헤더: 유형 및 해싱 알고리듬으로 구성
	- 페이로드: 사용자 클레임 포함
	- 서명: JWT의 진위 여부를 파악하는데 사용
- 각 파트는 점(.)으로 구분
- Base64 URL로 인코딩(HTTP 적합)

```bash
cat ./ch9/enduser/user.jwt

# 디코딩 방법 1
jwt decode $(cat ./ch9/enduser/user.jwt)

# 디코딩 방법 2
cat ./ch9/enduser/user.jwt | cut -d '.' -f1 | base64 --decode | sed 's/$/}/'  | jq
cat ./ch9/enduser/user.jwt | cut -d '.' -f2 | base64 --decode | sed 's/$/"}/' | jq
{
  "exp": 4745145038, # 만료 시간 Expiration time
  "group": "user",   # 'group' 클레임
  "iat": 1591545038, # 발행 시각 Issue time
  "iss": "auth@istioinaction.io", # 토큰 발행자 Token issuer
  "sub": "9b792b56-7dfa-4e4b-a83f-e20679115d79" # 토큰의 주체 Subject or principal of the token
}
```

### JWT 발행 / 검증
![]({{ site.url }}/img/post/devops/study/istio/5/20250501213328.png)

### 인그레스 게이트웨이에서의 최종 사용자 인증 및 인가
- 이스티오 워크로드가 JWT로 최종 사용자 요청은 인증/인가하도록 설정할 수 있음
	- 최종사용자: ID 제공자에게 인증받고, ID와 클레임을 나타내는 토큰을 발급받은 사용자
- 최종 사용자 인가는 모든 워크로드 수준에서 수행할 수 있음
	- 보통 이스티오 인그레스 게이트웨에서 수행
- 유효하지 않은 요청을 조기에 거부하여 성능 향상됨
- 요청에서 JWT를 제거함
	- 해커의 재전송 공격에 JWT를 사용하지 못하게 방지

#### 실습 준비
```bash
kubectl delete virtualservice,deployment,service,\
destinationrule,gateway,peerauthentication,authorizationpolicy --all -n istioinaction

kubectl delete peerauthentication,authorizationpolicy -n istio-system --all

# 삭제 확인
kubectl get gw,vs,dr,peerauthentication,authorizationpolicy -A

# 실습 환경 배포
kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction
kubectl apply -f services/webapp/kubernetes/webapp.yaml -n istioinaction
cat ch9/enduser/ingress-gw-for-webapp.yaml
kubectl apply -f ch9/enduser/ingress-gw-for-webapp.yaml -n istioinaction
```

### RequestAuthentication으로 JWT 검증
- `RequestAuthentication`
	- JWT 검증
	- 유효한 토큰의 클레임 추출
	- 클레임을 필터 메타데이터에 저장
		- 필터 메타데이터
			- 서비스 프록시에서 필터 간 요청을 처리하는 동안 사용할 수 있는 key-value
			- 인가 정책이 조치를 취하는 근거로 사용됨
- 최종 사용자의 결과
	- 유효한 토큰을 갖고 있는 요청
		- 허용
		- 클레임은 필터 메타데이터 형태로 정책에 전달
		- RequestAuthenticatino 필터로 검증
	- 유효하지 않은 토큰을 갖고 있는 요청
		- 거부
	- 토큰이 없는 요청
		- 허용(클러스터로 받아들여짐)
		- 요청 ID가 없음 = 어떤 클레임도 필터 메타데이터에 저장되지 않음
- 즉, RequestAuthentication 자체는 인가를 적용하지 않음(인가 강제 X)
	- 토큰 검증
	- claim 추출을 통해 인증의 유효성 검증
	- 인가에서 활용한 정보를 저장하는 역할
- AuthorizationPolicy가 필요하다!!

#### RequestAuthentication 리소스 만들기
- 다음 RequestAuthentication는 이스티오 인그레스 게이트웨이에 적용된다.
	- 인그레스 게이트웨이가 `auth@istioinaction.io`에서 발급한 토큰을 검증하도록 설정한다.

```bash
# cat ch9/enduser/jwt-token-request-authn.yaml 
apiVersion: "security.istio.io/v1beta1"
kind: "RequestAuthentication"
metadata:
  name: "jwt-token-request-authn"
  namespace: istio-system # 적용할 네임스페이스
spec:
  selector:
    matchLabels:
      app: istio-ingressgateway
  jwtRules:
  - issuer: "auth@istioinaction.io" # 발급자 Expected issuer
    jwks: | # 특정 JWKS로 검증
      { "keys":[ {"e":"AQAB","kid":"CU-ADJJEbH9bXl0tpsQWYuo4EwlkxFUHbeJ4ckkakCM","kty":"RSA","n":"zl9VRDbmVvyXNdyoGJ5uhuTSRA2653KHEi3XqITfJISvedYHVNGoZZxUCoiSEumxqrPY_Du7IMKzmT4bAuPnEalbY8rafuJNXnxVmqjTrQovPIerkGW5h59iUXIz6vCznO7F61RvJsUEyw5X291-3Z3r-9RcQD9sYy7-8fTNmcXcdG_nNgYCnduZUJ3vFVhmQCwHFG1idwni8PJo9NH6aTZ3mN730S6Y1g_lJfObju7lwYWT8j2Sjrwt6EES55oGimkZHzktKjDYjRx1rN4dJ5PR5zhlQ4kORWg1PtllWy1s5TSpOUv84OPjEohEoOWH0-g238zIOYA83gozgbJfmQ"}]}

kubectl apply -f ch9/enduser/jwt-token-request-authn.yaml
kubectl get requestauthentication -A

docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system
docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system --port 8080 -o json
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250509234631.png)

#### 유효한 발행자의 토큰이 있는 요청은 받아들여진다.
```bash
cat ch9/enduser/user.jwt
USER_TOKEN=$(< ch9/enduser/user.jwt)
jwt decode $USER_TOKEN

# 호출 
curl -H "Authorization: Bearer $USER_TOKEN" \
     -sSl -o /dev/null -w "%{http_code}" webapp.istioinaction.io:30000/api/catalog

# 로그
docker exec -it myk8s-control-plane istioctl proxy-config log deploy/istio-ingressgateway -n istio-system --level rbac:debug
kubectl logs -n istio-system -l app=istio-ingressgateway -f 
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250509235823.png)

#### 유효하지 않은 발행자의 토큰이 있는 요청은 거부된다.
```bash
cat ch9/enduser/not-configured-issuer.jwt
WRONG_ISSUER=$(< ch9/enduser/not-configured-issuer.jwt)
jwt decode $WRONG_ISSUER
...
Token claims
------------
{
  "exp": 4745151548,
  "group": "user",
  "iat": 1591551548,
  "iss": "old-auth@istioinaction.io", # 현재 설정한 정책의 발급자와 다름 issuer: "auth@istioinaction.io" 
  "sub": "79d7506c-b617-46d1-bc1f-f511b5d30ab0"
}
...


# 호출 
curl -H "Authorization: Bearer $WRONG_ISSUER" \
     -sSl -o /dev/null -w "%{http_code}" webapp.istioinaction.io:30000/api/catalog

# 로그
kubectl logs -n istio-system -l app=istio-ingressgateway -f
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250509235837.png)

#### 토큰이 없는 요청은 클러스터로 받아들여진다.
```bash
# 호출 
curl -sSl -o /dev/null -w "%{http_code}" webapp.istioinaction.io:30000/api/catalog

# 로그
kubectl logs -n istio-system -l app=istio-ingressgateway -f
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510000049.png)

#### JWT가 없는 요청 거부하기
```bash
# cat ch9/enduser/app-gw-requires-jwt.yaml # vi에서 포트 30000 추가
# 실습환경의 차이
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: app-gw-requires-jwt
  namespace: istio-system
spec:
  selector:
    matchLabels:
      app: istio-ingressgateway
  action: DENY
  rules:
  - from:
    - source:
        notRequestPrincipals: ["*"] # 요청 주체에 값이 없는 source는 모두 해당된다
    to:
    - operation:
        hosts: ["webapp.istioinaction.io:30000"] # 이 규칙은 이 특정 호스트에만 적용된다

kubectl apply -f ch9/enduser/app-gw-requires-jwt.yaml

kubectl get AuthorizationPolicy -A
NAMESPACE      NAME                  AGE
istio-system   app-gw-requires-jwt   9s

docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system --port 8080 -o json
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510000914.png)
```
# 호출 1
curl -sSl -o /dev/null -w "%{http_code}" webapp.istioinaction.io:30000/api/catalog
403

# 호출 2
curl -H "Authorization: Bearer $USER_TOKEN" \
     -sSl -o /dev/null -w "%{http_code}" webapp.istioinaction.io:30000/api/catalog

# 로그
kubectl logs -n istio-system -l app=istio-ingressgateway -f
```

![]({{ site.url }}/img/post/devops/study/istio/5/20250510003453.png)

#### JWT 클레임에 기반한 다양한 접근 수준
```bash
# 일반 사용자 토큰 : 'group: user' 클레임
jwt decode $(cat ch9/enduser/user.jwt)
...
{
  "exp": 4745145038,
  "group": "user",
  "iat": 1591545038,
  "iss": "auth@istioinaction.io",
  "sub": "9b792b56-7dfa-4e4b-a83f-e20679115d79"
}

# 관리자 토큰 : 'group: admin' 클레임
jwt decode $(cat ch9/enduser/admin.jwt)
...
{
  "exp": 4745145071,
  "group": "admin",
  "iat": 1591545071,
  "iss": "auth@istioinaction.io",
  "sub": "218d3fb9-4628-4d20-943c-124281c80e7b"
}
```

```bash
# cat ch9/enduser/allow-all-with-jwt-to-webapp.yaml # vi/vim, vscode 에서 포트 30000 추가
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: allow-all-with-jwt-to-webapp
  namespace: istio-system
spec:
  selector:
    matchLabels:
      app: istio-ingressgateway
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["auth@istioinaction.io/*"] # 최종 사용자 요청 주체를 표현 Represents the end-user request principal
    to:
    - operation:
        hosts: ["webapp.istioinaction.io:30000"] # 여기 실습환경에 맞게 포트 추가
        methods: ["GET"]
```

```bash
# cat ch9/enduser/allow-mesh-all-ops-admin.yaml
apiVersion: "security.istio.io/v1beta1"
kind: "AuthorizationPolicy"
metadata:
  name: "allow-mesh-all-ops-admin"
  namespace: istio-system
spec:
  selector:
    matchLabels:
      app: istio-ingressgateway
  action: ALLOW
  rules:
  - from:
    - source:
        requestPrincipals: ["auth@istioinaction.io/*"]
    when:
    - key: request.auth.claims[group]
      values: ["admin"] # 이 클레임을 포함한 요청만 허용.
```

```bash
kubectl apply -f ch9/enduser/allow-all-with-jwt-to-webapp.yaml
kubectl apply -f ch9/enduser/allow-mesh-all-ops-admin.yaml

kubectl get authorizationpolicy -A
NAMESPACE      NAME                           AGE
istio-system   allow-all-with-jwt-to-webapp   5m45s
istio-system   allow-mesh-all-ops-admin       15m
istio-system   app-gw-requires-jwt            25m

docker exec -it myk8s-control-plane istioctl proxy-config listener deploy/istio-ingressgateway.istio-system --port 8080 -o json
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510005307.png)
![]({{ site.url }}/img/post/devops/study/istio/5/20250510005316.png)

```
# 수집된 메타데이터를 관찰하고자 서비스 프록시에 rbac 로거 설정
## 기본적으로 envoy rbac 로거는 메타데이터를 로그에 출력하지 않는다. 출력을 위해 로깅 수준을 debug 로 설정하자
docker exec -it myk8s-control-plane istioctl proxy-config log deploy/istio-ingressgateway -n istio-system --level rbac:debug

# 일반유저 : [GET]과 [POST] 호출
USER_TOKEN=$(< ch9/enduser/user.jwt)

curl -H "Authorization: Bearer $USER_TOKEN" \
     -sSl -o /dev/null -w "%{http_code}\n" webapp.istioinaction.io:30000/api/catalog

curl -H "Authorization: Bearer $USER_TOKEN" \
     -XPOST webapp.istioinaction.io:30000/api/catalog \
     --data '{"id": 2, "name": "Shoes", "price": "84.00"}'

# 로그
kubectl logs -n istio-system -l app=istio-ingressgateway -f

# 관리자 : [GET]과 [POST] 호출
ADMIN_TOKEN=$(< ch9/enduser/admin.jwt)

curl -H "Authorization: Bearer $ADMIN_TOKEN" \
     -sSl -o /dev/null -w "%{http_code}\n" webapp.istioinaction.io:30000/api/catalog

curl -H "Authorization: Bearer $ADMIN_TOKEN" \
     -XPOST webapp.istioinaction.io:30000/api/catalog \
     --data '{"id": 2, "name": "Shoes", "price": "84.00"}'

# 로그
kubectl logs -n istio-system -l app=istio-ingressgateway -f
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510010618.png)

## 커스텀 외부 인가 서비스와 통합하기
- 인가에 좀 더 정교한 커스텀 메커니즘
	- 요청을 허용할지 여부를 결정시 외부 인가 서비스를 호출하도록 이스티오의 서비스 프록시를 설정

![]({{ site.url }}/img/post/devops/study/istio/5/20250501214210.png)
- 서비스 프록시에 들어온 요청은 프록시가 외부 인가(ExtAuthz) 서비스를 호출하는 동안 잠시 멈춘다.
- 외부 인가 서비스는 메시 안/밖에 존재할 수 있다.
- 외부 인가는 엔보이의 CheckRequest API를 구현해야 한다.
- 외부 인가 서비스들
	- [Open Policy Agent](https://www.openpolicyagent.org/docs/latest/envoy-tutorial-istio/)
	- [Signal Sciences](https://www.fastly.com/products/web-application-api-protection)
	- [Gloo Edge Ext Auth](https://docs.solo.io/gloo-edge/latest/guides/security/auth/extauth/)
	- [Istio sample Ext Authz](https://github.com/istio/istio/tree/release-1.21/samples/extauthz)
- 외부 인가 서비스는 프록시가 인가를 집행시 사용하는 '허용/거부' 메시지를 반환한다.

### 외부 인가 실습
```bash
# 기존 인증/인가 정책 모두 삭제
kubectl delete authorizationpolicy,peerauthentication,requestauthentication --all -n istio-system

# 실습 애플리케이션 배포
kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction
kubectl apply -f services/webapp/kubernetes/webapp.yaml -n istioinaction
kubectl apply -f services/webapp/istio/webapp-catalog-gw-vs.yaml -n istioinaction
kubectl apply -f ch9/sleep.yaml -n default

# 이스티오 샘플에서 샘플 외부 인가 서비스 배포
docker exec -it myk8s-control-plane bash
-----------------------------------
# 
ls -l istio-$ISTIOV/samples/extauthz/
total 24
-rw-r--r-- 1 root root 4238 Oct 11  2023 README.md
drwxr-xr-x 3 root root 4096 Oct 11  2023 cmd
drwxr-xr-x 2 root root 4096 Oct 11  2023 docker
-rw-r--r-- 1 root root 1330 Oct 11  2023 ext-authz.yaml
-rw-r--r-- 1 root root 2369 Oct 11  2023 local-ext-authz.yaml

cat istio-$ISTIOV/samples/extauthz/ext-authz.yaml
apiVersion: v1
kind: Service
metadata:
  name: ext-authz
  labels:
    app: ext-authz
spec:
  ports:
  - name: http
    port: 8000
    targetPort: 8000
  - name: grpc
    port: 9000
    targetPort: 9000
  selector:
    app: ext-authz
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ext-authz
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ext-authz
  template:
    metadata:
      labels:
        app: ext-authz
    spec:
      containers:
      - image: gcr.io/istio-testing/ext-authz:latest
        imagePullPolicy: IfNotPresent
        name: ext-authz
        ports:
        - containerPort: 8000
        - containerPort: 9000

kubectl apply -f istio-$ISTIOV/samples/extauthz/ext-authz.yaml -n istioinaction

# 빠져나오기
exit
-----------------------------------

# 설치 확인 : ext-authz
kubectl get deploy,svc ext-authz -n istioinaction
NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/ext-authz   0/1     1            0           8s

NAME                TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)             AGE
service/ext-authz   ClusterIP   10.200.1.33   <none>        8000/TCP,9000/TCP   8s

# 로그
kubectl logs -n istioinaction -l app=ext-authz -c ext-authz -f
```

### 이스티오에 외부 인가 설정하기
- 이스티오가 새로운 외부 인가 서비스를 인식하도록 설정
	- `meshconfig` 설정에서 `extensionProviders`를 설정
	- `istio-system` NS의 `istio` configMap에 있다.

```bash
# includeHeadersInCheck (DEPRECATED)
kubectl edit -n istio-system cm istio
--------------------------------------------------------
...
    extensionProviders:
    - name: "sample-ext-authz-http"  # 추가
      envoyExtAuthzHttp:
        service: "ext-authz.istioinaction.svc.cluster.local"
        port: "8000"
        includeRequestHeadersInCheck: ["x-ext-authz"]
...
--------------------------------------------------------

# 확인
kubectl describe -n istio-system cm istio
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510015310.png)
- 외부 인가 서비스에 전달할 헤더를 구성
	- `x-ext-authz` 헤더를 전달
	- 이 헤더가 인가 결과를 결정하는데 사용된다.
- AuthorizationPolicy에 이 기능을 사용하도록 설정

### 커스텀 AuthorizationPolicy 리소스 사용하기
```bash
# 아래 AuthorizationPolicy 는 istioinaction 네임스페이스에 webapp 워크로드에 적용되며, 
# sample-ext-authz-http 이라는 외부 인가 서비스에 위임한다.
cat << EOF | kubectl apply -f -
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: ext-authz
  namespace: istioinaction
spec:
  selector:
    matchLabels:
      app: webapp
  action: CUSTOM    # custom action 사용
  provider:
    name: sample-ext-authz-http  # meshconfig 이름과 동일해야 한다
  rules:
  - to:
    - operation:
        paths: ["/*"]  # 인가 정책을 적용할 경로
EOF

kubectl get AuthorizationPolicy -A
NAMESPACE       NAME        AGE
istioinaction   ext-authz   15s
```

```bash
docker exec -it myk8s-control-plane istioctl proxy-config log deploy/webapp -n istioinaction --level rbac:debug
kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
kubectl logs -n istioinaction -l app=ext-authz -c ext-authz -f

# 헤더 없이 호출
kubectl -n default exec -it deploy/sleep -- curl webapp.istioinaction/api/catalog

kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
kubectl logs -n istioinaction -l app=ext-authz -c ext-authz -f

# 헤더 적용 호출
kubectl -n default exec -it deploy/sleep -- curl -H "x-ext-authz: allow" webapp.istioinaction/api/catalog

kubectl logs -n istioinaction -l app=webapp -c istio-proxy -f
kubectl logs -n istioinaction -l app=ext-authz -c ext-authz -f
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510020521.png)
![]({{ site.url }}/img/post/devops/study/istio/5/20250510172022.png)

# 부록 C.  SPIFFE
## PKI를 사용한 인증
- PKI
	- 공개 키와 개인 키를 사용하는 인증 프레임워크
	- 클라이언트는 서버의 공개키로 데이터를 암호화
	- 서버는 개인 키로 복호화하여 보안 통신을 가능하게 함
	- 표준 형식은 X.509 인증서. TLS에서 사용된다.

### TLS 및 최종 사용자 인증을 통한 트래픽 암호화
![]({{ site.url }}/img/post/devops/study/istio/5/20250505190023.png)
- 비대칭키보다 대칭키가 성능 상 우수
	- 데이터 덩어리를 빠르게 처리 가능하며, 연산이 단순함
- 최종 사용자 인증
	- JWT를 사용하여 세션 인증 가능
	- 이스티오는 JWT 기반 최종 사용자 인증을 지원

## SPIFFE - 안전한 운영 환경 ID 프레임워크
- SPIFFE(Secure Production Identity Framework for Everyone)
	- 동적 환경에서 워크로드에 고유한 ID를 주여하는 표준
	- SPIFFE가 정의하는 사양
		- SPIFFE ID: 신뢰 도메인 내에서 서비스를 고유하게 구별한다.
		- Workload Endpoint: 워크로드의 ID를 부트스트랩한다.
		- Workload API: SPIFFE ID가 포함된 인증서를 서명하고 발급한다.
		- SVID(SPIFFE Verifiable Identity Document): 워크로드 API가 발급한 인증서로 표현된다.

### SPIFFE ID
- `spiffe://trust-domain/path` 형식의 URI
	- trust-domain: 발급자
	- path: 워크로드 식별 경로

### Workload API
- CSR에 서명하여 SVID 발급
- 워크로드는 사전에 비밀을 보유하지 않음
- 인증 수단 없이 보안 통신을 위한 Workload Endpoint가 필요

### Workload endpoint
- 기능
	- 워크로드 무결성 증명
	- 워크로드 API와의 보안 통신 유지
- ID 발급 과정
	- 워크로드 무결성 확인 후 CSR 생성
	- CSR을 워크로드 API에 제출
	- SVID 인증서 응답

![]({{ site.url }}/img/post/devops/study/istio/5/20250505175408.png)

### 검증할 수 있는 ID 문서
- 형식
	- X.509 인증서
	- JWT
- 구성 요소
	- SPIFFE ID
	- 유효한 서명
	- (선택) 공개키
- 이스티오에서는 X.509 인증서로 구현됨

![]({{ site.url }}/img/post/devops/study/istio/5/20250505175924.png)

### 이스티오가 SPIFFE를 구현하는 방법
- Workload Endpoint: 이스티오 파일럿 에이전트
- Workload API: 이스티오 CA(istiod 구성요소)
- Workload: 서비스 프록시

![]({{ site.url }}/img/post/devops/study/istio/5/20250505175034.png)

### 워크로드 ID의 단계별 부트스트랩
- 초기 파드 시크릿 위치
	- /var/run/secrets/kubernetes.io/serviceaccount/
	- ca.crt, namespace, token  포함
- 과정
	1. 토큰을 기반으로 SPIFFE ID 생성
	2. CSR과 함께 istiod에 전송
	3. istiod가 TokenReview API로 유효성 확인 후 인증서 발급
	4. 인증서 -> SDS 통해 엔보이 프록시에 전달
	5. 프록시가 상호 인증 및 트래픽 암호화 시작

```bash
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- ls -l /var/run/secrets/kubernetes.io/serviceaccount/
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- cat /var/run/secrets/kubernetes.io/serviceaccount/token

TOKEN=$(kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- cat /var/run/secrets/kubernetes.io/serviceaccount/token)

# 헤더 디코딩 
echo $TOKEN | cut -d '.' -f1 | base64 --decode | sed 's/$/}/' | jq

# 페이로드 디코딩
echo $TOKEN | cut -d '.' -f2 | base64 --decode | sed 's/$/}/' | jq
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510191706.png)
```
# (옵션) brew install jwt-cli  # Linux 툴 추천 부탁드립니다.
jwt decode $TOKEN
Token header
------------
{
  "alg": "RS256",
  "kid": "nKgUYnbjH9BmgEXYbu56GFoBxwDF_jF9Q6obIWvinAM"
}

Token claims
------------
{
  "aud": [ # 이 토큰의 대상(Audience) : 토큰이 어떤 API나 서비스에서 사용될 수 있는지 정의 -> k8s api가 aud 가 일치하는지 검사하여 올바른 토큰인지 판단.
    "https://kubernetes.default.svc.cluster.local"
  ],
  "exp": 1777689454, # 토큰 만료 시간 Expiration Time (Unix timestamp, 초 단위) , date -r 1777689454 => (1년) Sat May  2 11:37:34 KST 2026
  "iat": 1746153454, # 토큰 발급 시간 Issued At (Unix timestamp), date -r 1746153454 => Fri May  2 11:37:34 KST 2025
  "iss": "https://kubernetes.default.svc.cluster.local", # Issuer, 토큰을 발급한 주체, k8s api가 발급
  "kubernetes.io": {
    "namespace": "istioinaction",
    "pod": {
      "name": "webapp-7685bcb84-hp2kl",
      "uid": "98444761-1f47-45ad-b739-da1b7b22013a" # 파드 고유 식별자
    },
    "serviceaccount": {
      "name": "webapp",
      "uid": "5a27b23e-9ed6-46f7-bde0-a4e4684949c2" # 서비스 어카운트 고유 식별자
    },
    "warnafter": 1746157061 # 이 시간 이후에는 새로운 토큰을 요청하라는 Kubernetes의 신호 (토큰 자동 갱신용) date -r 1746157061 (1시간) => Fri May  2 12:37:41 KST 2025
  },
  "nbf": 1746153454, # Not Before, 이 시간 이전에는 토큰이 유효하지 않음. 보통 iat와 동일하게 설정됩니다.
  "sub": "system:serviceaccount:istioinaction:webapp" # 토큰의 주체(Subject)
}

# sa 에 토큰 유효 시간 3600초 = 1시간 + 7초
kubectl get pod -n istioinaction -l app=webapp -o yaml
...
    - name: kube-api-access-bh7d8
      projected:
        defaultMode: 420
        sources:
        - serviceAccountToken:
            expirationSeconds: 3607
            path: token
...
```
- 파일럿 에이전트는 토큰을 디코딩하고, 이 페이로드 데이터를 사용해 SPIFFE ID를 생성한다.
- 이 SPIFFE ID는 CSR안에서 URI 유형의 SAN 확장으로 사용한다.
- 이스티오 CA로 보낸 요청에 토큰과 CSR이 모두 전송
	- CSR에 대한 응답을 발급된 인증서가 반환됨
- CSR에 서명하기 전에 이스티오 CA는 TokenReview API를 사용해 토큰이 k8s API가 발급한 것인지 확인
	- SPIFFE 사양에서는 워크로드 엔드포인트가 워크로드 증명을 수행해야 하기 때문
- 검증을 통과하면 CSR에 서명하고, 결과 인증서가 파일럿에 반환됨

```bash
kubectl api-resources | grep -i token
tokenreviews                                   authentication.k8s.io/v1               false        TokenReview

kubectl explain tokenreviews.authentication.k8s.io
...
DESCRIPTION:
     TokenReview attempts to authenticate a token to a known user. Note:
     TokenReview requests may be cached by the webhook token authenticator
     plugin in the kube-apiserver.
...

# Kubernetes API 서버에 TokenReview API 를 호출하여 토큰이 여전히 유효한지 확인 : C(Create)
## 이때 사용되는 Kubernetes API 가 POST /apis/authentication.k8s.io/v1/tokenreviews
## 즉, istiod가 이 API를 호출하려면 tokenreviews.authentication.k8s.io 리소스에 create 권한이 필요. C(Create)
kubectl rolesum istiod -n istio-system
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510192807.png)

```bash
# 유닉스 도메인 소켓 listen 정보 확인
# x: unix / l: listen
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- ss -xpl
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- ss -xp

# 유닉스 도메인 소켓 정보 확인
# TYPE 파일 유형 (unix → Unix Domain Socket)
## 11u → 11번 디스크립터, u = 읽기/쓰기
## 15u → 15번 디스크립터, u = 읽기/쓰기
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- lsof -U

# 유닉스 도메인 소켓 파일 정보 확인
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- ls -l /var/run/secrets/workload-spiffe-uds/socket
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510231852.png)
```
# istio 인증서 확인 : 
docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/webapp.istioinaction
RESOURCE NAME     TYPE           STATUS     VALID CERT     SERIAL NUMBER                               NOT AFTER                NOT BEFORE
default           Cert Chain     ACTIVE     true           124860945214475929960471703970846463244     2025-05-11T08:52:30Z     2025-05-10T08:50:30Z
ROOTCA            CA             ACTIVE     true           322978064217889301818806346024680167222     2035-05-03T23:50:27Z     2025-05-05T23:50:27Z

docker exec -it myk8s-control-plane istioctl proxy-config secret deploy/webapp.istioinaction -o json
...

echo "." | base64 -d  | openssl x509 -in /dev/stdin -text -noout
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510234959.png)
```
# istio ca 관련
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- ls -l /var/run/secrets/istio
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- openssl x509 -in /var/run/secrets/istio/root-cert.pem -text -noout

kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- ls -l /var/run/secrets/tokens
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- cat /var/run/secrets/tokens/istio-token
TOKEN=$(kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- cat /var/run/secrets/tokens/istio-token)
# 헤더 디코딩 
echo $TOKEN | cut -d '.' -f1 | base64 --decode | sed 's/$/}/' | jq
# 페이로드 디코딩
echo $TOKEN | cut -d '.' -f2 | base64 --decode | sed 's/$/"}/' | jq
# (옵션) brew install jwt-cli 
jwt decode $TOKEN
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250510235233.png)
```
# (참고) k8s ca 관련
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- ls -l /var/run/secrets
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- ls -l /var/run/secrets/kubernetes.io/serviceaccount
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- openssl x509 -in /var/run/secrets/kubernetes.io/serviceaccount/ca.crt -text -noout
kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- cat /var/run/secrets/kubernetes.io/serviceaccount/token
TOKEN=$(kubectl exec -it -n istioinaction deploy/webapp -c istio-proxy -- cat /var/run/secrets/kubernetes.io/serviceaccount/token)
# 헤더 디코딩 
echo $TOKEN | cut -d '.' -f1 | base64 --decode | sed 's/$/}/' | jq
# 페이로드 디코딩
echo $TOKEN | cut -d '.' -f2 | base64 --decode | sed 's/$/}/' | jq
# (옵션) brew install jwt-cli 
jwt decode $TOKEN

# (참고)
kubectl port-forward deploy/webapp -n istioinaction 15000:15000
open http://localhost:15000
curl http://localhost:15000/certs
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250505173326.png)

## 요청 ID 이해하기
- 요청 ID의 저장 위치: 필터 메타데이터
- 저장되는 정보 예시
	- 주체, 네임스페이스, 요청 주체, 인증 클레임

### RequestAuthentication 리소스로 수집한 메타데이터
- rbac 로그를 출력하려면 디버그 모드 필요

```bash
# rbac 로그를 출력하려면 디버그 모드 필요
docker exec -it myk8s-control-plane istioctl proxy-config log deploy/istio-ingressgateway -n istio-system --level rbac:debug

kubectl apply -f services/catalog/kubernetes/catalog.yaml -n istioinaction
kubectl apply -f services/webapp/kubernetes/webapp.yaml -n istioinaction
kubectl apply -f services/webapp/istio/webapp-catalog-gw-vs.yaml -n istioinaction

kubectl apply -f ch9/enduser/jwt-token-request-authn.yaml
kubectl apply -f ch9/enduser/allow-all-with-jwt-to-webapp.yaml # :30000 포트 추가 필요, 아래 실습 설정 참고.
kubectl get requestauthentication,authorizationpolicy -A

# 로깅
kubectl logs -n istio-system -l app=istio-ingressgateway -f

# admin 토큰을 사용하는 요청 : 필터 메타데이터 확인
ADMIN_TOKEN=$(< ch9/enduser/admin.jwt)

curl -H "Authorization: Bearer $ADMIN_TOKEN" \
     -sSl -o /dev/null -w "%{http_code}\n" webapp.istioinaction.io:30000/api/catalog
```
![]({{ site.url }}/img/post/devops/study/istio/5/20250511002655.png)
![]({{ site.url }}/img/post/devops/study/istio/5/20250505171804.png)

### 한 요청의 대략적인 흐름
- 필터 순서
	1. JWT 인증 필터: 클레임 추출
	2. PeerAuthentication 필터: Peer ID 추출
	3. Authz 필터: 메타데이터 기반 인가
