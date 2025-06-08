---
layout: post
section-type: post
title: ServiceMesh - Istio - Week8-2
category: devops
tags: ["k8s", "istio", "servicemesh"]
---

# Istio Traffic Flow
- 아래 흐름은 **요청(Request) 트래픽**만 표기
- **응답(Response) 트래픽** 흐름은 별도 설명 없음

### **Type 1: 외부 → Local Pod (Inbound 트래픽)**
![]({{ site.url }}/img/post/devops/study/istio/8/20250608195708.png)
**외부에서 Application 컨테이너로 요청 유입**
```
Remote Pod(외부) → PREROUTING → ISTIO_INBOUND → ISTIO_IN_REDIRECT 
→ Envoy 15006 (Inbound) → OUTPUT → ISTIO_OUTPUT RULE 1 
→ POSTROUTING → Local Pod (Application 컨테이너)
```
### **Type 2: Local Pod → 외부 (Outbound 트래픽)**
![]({{ site.url }}/img/post/devops/study/istio/8/20250608195727.png)
**Application 컨테이너에서 외부(다른 파드)로 요청 시작**

```
Local Pod (Application 컨테이너) → OUTPUT → ISTIO_OUTPUT RULE 9 
→ ISTIO_REDIRECT → Envoy 15001 (Outbound) → OUTPUT 
→ ISTIO_OUTPUT RULE 4 → POSTROUTING → Remote Pod(외부)
```
### **Type 3: Prometheus → Local Pod (메트릭 수집)**
![]({{ site.url }}/img/post/devops/study/istio/8/20250608195747.png)
**Prometheus 서버가 Application에서 메트릭 수집**
```
Prometheus(서버) → PREROUTING → ISTIO_INBOUND 
(ports 15002, 15090 → INPUT) → INPUT → OUTPUT 
→ ISTIO_OUTPUT RULE 3 → POSTROUTING → Local Pod(Application Container)
```
**특징**: **Sidecar Proxy(Envoy)를 경유하지 않음**
### **Type 4: Local Pod → Local Pod (Pod 내부 통신)**

![]({{ site.url }}/img/post/devops/study/istio/8/20250608195806.png)
**Application 컨테이너의 서비스 간 통신**

```
Local Pod → OUTPUT → ISTIO_OUTPUT RULE 9 → ISTIO_REDIRECT 
→ Envoy 15001(Outbound) → OUTPUT → ISTIO_OUTPUT RULE 2 
→ ISTIO_IN_REDIRECT → Envoy 15006(Inbound) → OUTPUT 
→ ISTIO_OUTPUT RULE 1 → POSTROUTING → Local Pod
```
### **Type 5: Envoy 내부 프로세스 통신**
![]({{ site.url }}/img/post/devops/study/istio/8/20250608195825.png)
**Envoy 내부 프로세스(UID/GID 1337)의 localhost 통신**

```
Envoy process (Localhost) → OUTPUT → ISTIO_OUTPUT RULE 8 
→ POSTROUTING → Envoy process (Localhost)
```
### **Type 6: Sidecar → Istiod 통신**
![]({{ site.url }}/img/post/devops/study/istio/8/20250608195843.png)
**pilot-agent가 컨트롤 플레인과 설정 동기화**
```
pilot-agent process → OUTPUT → ISTIO_OUTPUT RULE 9 
→ Envoy 15001 (Outbound Handler) → OUTPUT 
→ ISTIO_OUTPUT RULE 4 → POSTROUTING → Istiod(컨트롤 플레인)
```
### **주요 포트 및 구성요소**

| **포트**    | **용도**         | **방향**      |
| --------- | -------------- | ----------- |
| **15001** | Envoy Outbound | 외부로 나가는 트래픽 |
| **15006** | Envoy Inbound  | 들어오는 트래픽    |
| **15002** | Prometheus 메트릭 | 메트릭 수집      |
| **15090** | Prometheus 메트릭 | 메트릭 수집      |

### **핵심 iptables 체인**
- **ISTIO_INBOUND**: 인바운드 트래픽 처리
- **ISTIO_OUTPUT**: 아웃바운드 트래픽 처리
- **ISTIO_REDIRECT**: 15001 포트로 리디렉션
- **ISTIO_IN_REDIRECT**: 15006 포트로 리디렉션

**Type 3 (Prometheus)**: 유일하게 Envoy를 거치지 않는 트래픽으로, 메트릭 수집의 효율성을 위해 직접 연결
이러한 트래픽 플로우를 통해 Istio가 다양한 통신 시나리오에서 투명하게 트래픽을 제어하고 보안을 적용함을 알 수 있다.

## Client(request) -> Pod(인입)
- 트래픽 흐름
	- 외부 클라이언트 PC에서 k8s 클러스터 내부의 웹 서버 파드로 인입 시 트래픽 흐름

![]({{ site.url }}/img/post/devops/study/istio/8/20250608200439.png)

파드 내 IP Tables 적용 흐름
![]({{ site.url }}/img/post/devops/study/istio/8/20250608200515.png)
> https://jimmysong.io/en/blog/sidecar-injection-iptables-and-traffic-routing/#understand-outbound-handler

### Life of a Packet in ISTIO
1. (통신 시작) 트래픽 인입 -> 목적지 파드
![]({{ site.url }}/img/post/devops/study/istio/8/20250608200621.png)
2. (통신 시작) 파드 -> 외부
![]({{ site.url }}/img/post/devops/study/istio/8/20250608200646.png)

![]({{ site.url }}/img/post/devops/study/istio/8/20250608201031.png)

## Client PC -> Istio IngressGateway Pod 구간

- 외부 **클라이언트 PC**(192.168.10.254) 에서 **웹 서버 파드**로 접속 시도
    - 외부에서 Istio IngressGateway 파드로 인입 과정 부분은 생략

```bash
# 아래 처럼 정상적으로 웹 서버 접속 정보 출력 확인
curl -s -v $MYDOMAIN:$IGWHTTP
curl -s $MYDOMAIN:$IGWHTTP | grep -o "<title>.*</title>"
while true; do curl -s $MYDOMAIN:$IGWHTTP | grep -o "<title>.*</title>" ; echo "--------------" ; sleep 1; done
while true; do curl -s $MYDOMAIN:$IGWHTTP | grep -o "<title>.*</title>" ; echo "--------------" ; sleep 0.1; done

curl -s --user-agent "IPHONE" $MYDOMAIN:$IGWHTTP | grep -o "<title>.*</title>"
while true; do curl -s $MYDOMAIN:$IGWHTTP | grep -o "<title>.*</title>"; date "+%Y-%m-%d %H:%M:%S" ; echo "--------------" ; sleep 1; done

# 로그 확인
kubetail -l app=nginx-app -f
```

([istio-INBOUND-1.pcap]({{ site.url }}/upload/istio/istio-INBOUND-1.pcap))

## Istio IngressGateway Pod -> Node 인입
- Istio **IngressGateway**(envoy) 파드를 경유하여 **웹 서버 파**드가 있는 **노드**로 인입
    - Istio IngressGateway(envoy) 파드는 **클라이언트 PC**의 **IP**를 HTTP `XFF`(**X-Forwarded-for**) 헤더에 담아서 전달합니다.
    - Istio IngressGateway(envoy) 파드 **x-envoy-Y** 헤더를 추가해서 전달합니다.

![]({{ site.url }}/img/post/devops/study/istio/8/20250608201420.png)
## (Pod 내부) IP Tables 적용 -> Istio-proxy 컨테이너 인입
- 'PAUSE 컨테이너'가 파드 네트워크 네임스페이스를 생성하여 제공하며, 'Init 컨테이너'는 Istio-proxy가 트래픽을 가로챌 수 있게 파드 내에 iptables rules 설정을 완료합니다.

```bash
# 아래 처럼 'istio-init 컨테이너' 의 로그에 iptables rules 설정을 확인할 수 있습니다.
# 참고로, NAT Tables 만 설정되고, 그외(filter, mangle, raw 등)은 설정하지 않습니다.
(istio-k8s:default) root@k8s-m:~# kubectl logs nginx-pod -c istio-init
* nat
-N ISTIO_INBOUND
-N ISTIO_REDIRECT
-N ISTIO_IN_REDIRECT
-N ISTIO_OUTPUT
-A ISTIO_INBOUND -p tcp --dport 15008 -j RETURN
-A ISTIO_REDIRECT -p tcp -j REDIRECT --to-ports 15001
-A ISTIO_IN_REDIRECT -p tcp -j REDIRECT --to-ports 15006
-A PREROUTING -p tcp -j ISTIO_INBOUND
-A ISTIO_INBOUND -p tcp --dport 22 -j RETURN
-A ISTIO_INBOUND -p tcp --dport 15090 -j RETURN
-A ISTIO_INBOUND -p tcp --dport 15021 -j RETURN
-A ISTIO_INBOUND -p tcp --dport 15020 -j RETURN
-A ISTIO_INBOUND -p tcp -j ISTIO_IN_REDIRECT
-A OUTPUT -p tcp -j ISTIO_OUTPUT
-A ISTIO_OUTPUT -o lo -s 127.0.0.6/32 -j RETURN
-A ISTIO_OUTPUT -o lo ! -d 127.0.0.1/32 -m owner --uid-owner 1337 -j ISTIO_IN_REDIRECT
-A ISTIO_OUTPUT -o lo -m owner ! --uid-owner 1337 -j RETURN
-A ISTIO_OUTPUT -m owner --uid-owner 1337 -j RETURN
-A ISTIO_OUTPUT -o lo ! -d 127.0.0.1/32 -m owner --gid-owner 1337 -j ISTIO_IN_REDIRECT
-A ISTIO_OUTPUT -o lo -m owner ! --gid-owner 1337 -j RETURN
-A ISTIO_OUTPUT -m owner --gid-owner 1337 -j RETURN
-A ISTIO_OUTPUT -d 127.0.0.1/32 -j RETURN
-A ISTIO_OUTPUT -j ISTIO_REDIRECT
COMMIT
```

- **파드 내 IPTables Chains/Rules 적용** (NAT 테이블) → '**Istio-proxy 컨테이너**'로 **인입**됩니다.
    - **PREROUTING** → **ISTIO_INBOUND** → **ISTIO_IN_REDIRECT** (**redir ports 15006**)

```bash
nginx 파드가 배치된 노드에서 아래 실행
# 아래 확인은 istio-proxy 대신 pause 에서 iptables 확인 해보자...

# 변수 지정 : C1(Istio-proxy, Envoy , 단축키 지정
lsns -t net
ps -ef |grep istio
1337      347173  347155  0 18:52 ?        00:00:01 /usr/local/bin/envoy -c etc/istio/proxy/envoy-rev.json --drain-time-s 45 --drain-strategy immediate --local-address-ip-version v4 --file-flush-interval-msec 1000 --disable-hot-restart --allow-unknown-static-fields -l warning --component-log-level misc:error --concurrency 2
C1PID=347173
alias c1="nsenter -t $C1PID -n"

# Istio-proxy 컨테이너의 iptables 확인
c1 iptables -t nat --zero # 패킷 카운트 초기화

# 트래픽 인입 시 TCP 경우 모든 트래픽을 15006 으로 리다이렉트한다, 일부 포트는 제외(22, 15008, 15020, 15021, 15090)
c1 iptables -t nat -L -n -v
Chain PREROUTING (policy ACCEPT 44 packets, 2640 bytes)
 pkts bytes target     prot opt in     out     source               destination
   45  2700 ISTIO_INBOUND  tcp  --  *      *       0.0.0.0/0            0.0.0.0/0

Chain ISTIO_INBOUND (1 references)
 pkts bytes target             prot opt in     out     source               destination
...
    1    60 ISTIO_IN_REDIRECT  tcp  --  *      *       0.0.0.0/0            0.0.0.0/0

Chain ISTIO_IN_REDIRECT (3 references)
 pkts bytes target     prot opt in     out     source               destination
    1    60 REDIRECT   tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            redir ports 15006

# 모니터링 >> 아래 ss 소켓 강제 Reset 참고
c1 iptables -t nat --zero
c1 iptables -t nat -S | grep 15006
c1 iptables -v --numeric --table nat --list ISTIO_IN_REDIRECT
watch -d "nsenter -t $C1PID -n iptables -v --numeric --table nat --list PREROUTING ; echo ; nsenter -t $C1PID -n iptables -v --numeric --table nat --list ISTIO_INBOUND; echo ; nsenter -t $C1PID -n iptables -v --numeric --table nat --list ISTIO_IN_REDIRECT"
watch -d "nsenter -t $C1PID -n iptables -t nat -L -n -v"
```

- 'Istio-proxy 컨테이너'의 15006 Listener 확인

```bash
# ss (socket statistics)로 시스템 소켓 상태 확인 : 15006 은 envoy 프로세스가 Listen 하고 있다
root@k8s-w2:~# c1 ss -tpnl '( dport = :15006 or sport = :15006 )'
State      Recv-Q      Send-Q           Local Address:Port            Peer Address:Port     Process
LISTEN     0           4096                   0.0.0.0:15006                0.0.0.0:*         users:(("envoy",pid=3928,fd=37))
LISTEN     0           4096                   0.0.0.0:15006                0.0.0.0:*         users:(("envoy",pid=3928,fd=36))

# 확인 예시
c1 ss -tpnt '( dport = :15006 or sport = :15006 or sport = :80 or dport = :80 )'
watch -d "nsenter -t $C1PID -n  ss -tpnt '( dport = :15006 or sport = :15006 or sport = :80 or dport = :80 )'"

# 연결된 소켓 강제 Reset
# c0 ss -K dst 172.16.228.66 dport = 44526
c1 ss -K dst 172.16.228.66
c1 ss -K dst 172.16.46.13
```
### (참고) istioctl proxy-config listener 과 cluster 정보 확인
```bash
# istio-proxy(envoy) 로 nginx-pod 정보 확인
istioctl proxy-config listener nginx-pod
istioctl proxy-config listener nginx-pod --address 0.0.0.0 --port 15006
0.0.0.0 15006 Trans: raw_buffer; App: HTTP; Addr: *:80                                 Cluster: inbound|80||
...
istioctl proxy-config listener nginx-pod --address 0.0.0.0 --port 15006 -o json
[
    {
        "name": "virtualInbound",
        "address": {
            "socketAddress": {
                "address": "0.0.0.0",
                "portValue": 15006
...

#
istioctl proxy-config cluster nginx-pod
istioctl proxy-config cluster nginx-pod --direction inbound -o json
...
				"upstreamBindConfig": {
            "sourceAddress": {
                "address": "127.0.0.6",
                "portValue": 0
            }
        },
        "metadata": {
            "filterMetadata": {
                "istio": {
                    "services": [
                        {
                            "host": "svc-nginx.default.svc.cluster.local",
                            "name": "svc-nginx",
                            "namespace": "default"
```
### (참고) nginx 파드 내에서 istio-proxy 컨테이너와 nginx 컨테이너 정보 확인 → 스터디에서는 Skip
```bash
마스터 노드에서 아래 실행
# 노드에서 -c 옵션으로 istio-proxy 컨테이너와 nginx-container 컨테이너간 구별되어 정보가 확인된다
kubectl exec nginx-pod -c istio-proxy -- ls -l /proc/1/ns
lrwxrwxrwx 1 istio-proxy istio-proxy 0 Dec 14 14:52 mnt -> mnt:[4026532435]
lrwxrwxrwx 1 istio-proxy istio-proxy 0 Dec 14 14:52 net -> net:[4026532367]
lrwxrwxrwx 1 istio-proxy istio-proxy 0 Dec 14 14:52 pid -> pid:[4026532437]

kubectl exec nginx-pod -c nginx-container -- ls -l /proc/1/ns
lrwxrwxrwx 1 root root 0 Dec 14 14:52 mnt -> mnt:[4026532432]
lrwxrwxrwx 1 root root 0 Dec 14 14:52 net -> net:[4026532367]
lrwxrwxrwx 1 root root 0 Dec 14 14:52 pid -> pid:[4026532434]

lsns -t net


# 단축키(alias) 지정
alias c1="kubectl exec -it nginx-pod -c istio-proxy --"
alias c2="kubectl exec -it nginx-pod -c nginx-container --"

# nginx 컨테이너에 툴 설치
c2 apt update
c2 apt install -y iproute2 procps tree tcpdump ngrep

# PID 비교
c1 ps afxuwww
c2 ps afxuwww

# MNT 비교
c1 ls -al /etc/nginx
c2 ls -al /etc/nginx

# NET 비교
c1 ip -c addr
c2 ip -c addr
```
### (참고) debug 파드 활용 : tcpdump, ngrep 등
```bash
# debug 컨테이너
kubectl debug nginx-pod -it --image=nicolaka/netshoot -c netdebug
-----
ip -c addr
curl localhost
ss
ss -l
ss -4tpl
ss -4tp
ss -xpl
ss -xp
tcpdump -i any -nnq
ngrep -d any -tW byline
exit
-----
```
## (Pod 내부) Istio-proxy 컨테이너 -> IP Tables 적용
- '**Istio-proxy 컨테이너'** 는 대리인(Proxy) 역할로, **출발지 IP**를 **127.0.0.6** 으로 변경하여 '**Nginx 컨테이너**'와 연결을 한다
    - '**Istio-proxy 컨테이너'**의 로그 확인

```bash
# 로그 내용 중 출발지 정보(127.0.0.6:50763)를 변경하고 전달하는 것을 알 수 있다
(istio-k8s:default) root@k8s-m:~# kubectl logs nginx-pod -c istio-proxy -f
[2021-12-15T18:05:56.334Z] "GET / HTTP/1.1" 200 - via_upstream - "-" 0 615 0 0 "192.168.10.254" "curl/7.68.0" "0844349b-d290-994b-93b2-da36bf929c62" "www.gasida.dev:30384" "172.16.46.11:80" inbound|80|| 127.0.0.6:50763 172.16.46.11:80 192.168.10.254:0 - default
```

- 파드 내에서 패킷 덤프 후 확인 : 출발지 IP가 127.0.0.6 으로 변경되었다!

```bash
# 패킷 덤프 (예시) 
c1 tcpdump -nni any  not net 10.0.2.15 and not udp and not tcp port 15012 and not tcp port 15020 -q
c1 tcpdump -nni any  not net 10.0.2.15 and not udp and not tcp port 15012 and not tcp port 15020 -q -w /tmp/istio-nginx.pcap
c1 tcpdump -nni lo   not net 10.0.2.15 and not udp and not tcp port 15012 and not tcp port 15020 -q
c1 tcpdump -nni eth0 not net 10.0.2.15 and not udp and not tcp port 15012 and not tcp port 15020 -q

c2 tcpdump -nni any  not net 10.0.2.15 and not udp and not tcp port 15012 and not tcp port 15020 -q
c2 tcpdump -nni any  not net 10.0.2.15 and not udp and not tcp port 15012 and not tcp port 15020 -q -w /tmp/istio-nginx.pcap
c2 tcpdump -nni lo   not net 10.0.2.15 and not udp and not tcp port 15012 and not tcp port 15020 -q
c2 tcpdump -nni eth0 not net 10.0.2.15 and not udp and not tcp port 15012 and not tcp port 15020 -q

#
kubectl exec nginx-pod -c istio-proxy -- bash
------------------
tcpdump -i any -nnq
------------------

# debug 컨테이너
tcpdump -i any -nnq
07:09:19.911008 eth0  In  IP 10.0.2.15.35822 > 172.16.184.18.15021: tcp 0
07:09:19.911029 eth0  Out IP 172.16.184.18.15021 > 10.0.2.15.35822: tcp 0
07:09:19.911048 eth0  In  IP 10.0.2.15.35822 > 172.16.184.18.15021: tcp 0
07:09:19.911286 eth0  In  IP 10.0.2.15.35822 > 172.16.184.18.15021: tcp 119
07:09:19.911293 eth0  Out IP 172.16.184.18.15021 > 10.0.2.15.35822: tcp 0
07:09:19.911587 lo    In  IP 127.0.0.1.60644 > 127.0.0.1.15020: tcp 216
07:09:19.911756 lo    In  IP 127.0.0.1.15020 > 127.0.0.1.60644: tcp 75
07:09:19.911770 lo    In  IP 127.0.0.1.60644 > 127.0.0.1.15020: tcp 0
07:09:19.911950 eth0  Out IP 172.16.184.18.15021 > 10.0.2.15.35822: tcp 143
07:09:19.911966 eth0  In  IP 10.0.2.15.35822 > 172.16.184.18.15021: tcp 0
```

![]({{ site.url }}/img/post/devops/study/istio/8/20250608201824.png)

- 파드 내 lsof (list open files) 확인

```bash
# 아래 처럼 126.0.0.6 -> 172.16.46.11(nginx)로 TCP 세션이 연결된것을 알 수 있다
c1 lsof -i TCP:80,15006 -n
COMMAND  PID            USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
envoy   3928            1337   40u  IPv4 901362      0t0  TCP 127.0.0.6:41109->172.16.46.11:http (ESTABLISHED)
nginx   3864 systemd-resolve    9u  IPv4 901363      0t0  TCP 172.16.46.11:http->127.0.0.6:41109 (ESTABLISHED)
envoy   3928            1337   38u  IPv4 901360      0t0  TCP 172.16.46.11:15006->172.16.228.76:40486 (ESTABLISHED)

# 확인 예시
c1 lsof -i TCP:80,15006 -n
c1 lsof -i TCP:80,15001,15006 -n
watch -d "nsenter -t $C0PID -n lsof -i TCP:80,15006 -n"
watch -d "nsenter -t $C0PID -n lsof -i TCP:80,15001,15006 -n"

# 연결된 TCP 강제 Reset
# c0 ss -K dst 172.16.228.66 dport = 44526
c1 ss -K dst 172.16.228.95
c1 ss -K dst 172.16.46.14
```

### (참고) '**Istio-proxy 컨테이너'** → '**Nginx 컨테이너**' 와 통신 시에는 **로컬 통신**
- 두 컨테이너는 동일한 NET NS 를 사용하므로, 별도 통신을 위해서 'istio-proxy' 는 lo 통신이 가능한 127.0.0.6 주소로 변경 후 로컬 통신을 수행한다

```bash
# 기본적으로 127.0.0.0/8 대역 통신은 lo local 통신 라우팅 처리다!
c1 ip route show table local
broadcast 127.0.0.0 dev lo proto kernel scope link src 127.0.0.1
local 127.0.0.0/8 dev lo proto kernel scope host src 127.0.0.1
local 127.0.0.1 dev lo proto kernel scope host src 127.0.0.1

# lo 인터페이스도 통신에 사용된다 : 실제 아래 RX/TX packets 이 증가한다!
c1 ifconfig lo
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 28141  bytes 19036394 (19.0 MB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 28141  bytes 19036394 (19.0 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
## (Pod 내부) IP Tables 적용 -> Nginx 컨테이너 인입
- 파드 내에 IPTables 는 전역(?)으로 적용되므로, 'Istio-proxy' 의 인/아웃 시 트래픽 구별이 중요하다.
    - 'Istio-proxy' 를 빠져나올때는 출발지 IP가 127.0.0.6 이므로 ISTIO_OUTPUT 에 적용되어 리턴되어 POSTROUTING 를 통해 nginx 로 도착한다
    - IPTables 확인 : istio-proxy → OUTPUT → **ISTIO_OUTOUT**(맨 상단 Rule 매칭으로 RETURN) -> POSTROUTING -> **NGINX 컨테이너**

```bash
# 출발IP가 127.0.0.6 이고, 빠져나오는 인터페이스가(-o lo)에 매칭되어 리턴됨
c1 iptables -v --numeric --table nat --list ISTIO_OUTPUT
Chain ISTIO_OUTPUT (1 references)
 pkts bytes target     prot opt in     out     source               destination
    2   120 RETURN     all  --  *      lo      127.0.0.6            0.0.0.0/0

# POSTROUTING 은 특별한 rule 이 없으니 통과!
Chain POSTROUTING (policy ACCEPT 144 packets, 12545 bytes)
 pkts bytes target     prot opt in     out     source               destination

# 모니터링 예시
c1 iptables -t nat --zero
c1 iptables -v --numeric --table nat --list ISTIO_OUTPUT
watch -d "nsenter -t $C1PID -n iptables -v --numeric --table nat --list OUTPUT; echo ; nsenter -t $C1PID -n iptables -v --numeric --table nat --list ISTIO_OUTPUT; echo ; nsenter -t $C1PID -n iptables -v --numeric --table nat --list POSTROUTING"
watch -d "nsenter -t $C1PID -n iptables -t nat -L -n -v"
```
- 최종적으로 **nginx 컨테이너**에 클라이언트의 **요청 트래픽**이 도착한다.
    - nginx 컨테이너의 웹 액세스 로그에서 확인 : **XFF 헤더**에서 클라이언트의 **출발지 IP**를 확인!

```bash
# nginx 웹 데몬에 도착하여 액세스 로그 기록되고, 이후 200ok 리턴되며, XFF 헤더에서 클라이언트의 IP를 확인 할 수 있다
(istio-k8s:default) root@k8s-m:~# kubectl logs nginx-pod -f
127.0.0.6 - - [15/Dec/2021:18:37:38 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/7.68.0" "192.168.10.254"
127.0.0.6 - - [15/Dec/2021:18:40:52 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/7.68.0" "192.168.10.254"
... 
```
## Pod(return traffic) -> Client
`트래픽 흐름`
- nginx (웹 서버)컨테이너에서 리턴 트래픽(응답, 200 OK)를 클라이언트에 전달합니다.
- IPTables CT(Connection Table)에 정보를 참고해서 역변환 등이 적용되어 전달됩니다.

![]({{ site.url }}/img/post/devops/study/istio/8/20250608204832.png)

**`8번 과정의 패킷`**
- 200 OK 응답이며, 'Istio-proxy' 에 의해서 x-envoy-upstream-Y 헤더가 추가되어 있습니다.

![]({{ site.url }}/img/post/devops/study/istio/8/20250608204851.png)

([istio-INBOUND-2.pcap]({{ site.url }}/upload/istio/istio-INBOUND-2.pcap))


### (참고) 1.1 에서 알아본 3번 과정 직전과 위 8번 과정의 NAT 트래픽 정보
```bash
c1 conntrack -L --dst-nat
tcp      6 430172 ESTABLISHED src=172.16.228.76 dst=172.16.46.11 sport=40882 dport=80 src=172.16.46.11 dst=172.16.228.76 sport=15006 dport=40882 [ASSURED] mark=0 use=1
 src=172.16.228.76 dst=172.16.46.11 sport=40882 dport=80     # 3번 과정 직전(IPTables 적용 전)의 IP/Port 정보
 src=172.16.46.11 dst=172.16.228.76 sport=15006 dport=40882  # 8번 과정 의 IP/Port 정보, 특히 출발지 포트가 15006 으로, 'istio-proxy' 경유를 했음을 알 수 있다
```
## Pod(request) -> 외부 웹서버
`트래픽 흐름`
- **파드**에서 업데이트 나 패치 다운로드 처럼 **외부 웹서버** 나 **인터넷** 연결 과정에서의 트래픽의 흐름입니다.

![]({{ site.url }}/img/post/devops/study/istio/8/20250608204957.png)
`파드 내 IPTables 적용 흐름` : 아래 **(9) ~ (15)** 까지의 과정을 먼저 설명합니다.
![]({{ site.url }}/img/post/devops/study/istio/8/20250608205013.png)
> https://jimmysong.io/en/blog/sidecar-injection-iptables-and-traffic-routing/

## (Pod 내부) Client PC -> Istio IngressGateway Pod 구간
'nginx 컨테이너' 에서 외부 웹서버 요청을 합니다.
```bash
# 아래 처럼 'nginx 컨테이너' 에서 외부 웹서버 요청
kubectl exec -it nginx-pod -c nginx-container -- curl -s 192.168.10.254
kubectl exec -it nginx-pod -c nginx-container -- curl -s http://wttr.in/seoul
kubectl exec -it nginx-pod -c nginx-container -- curl -s wttr.in/seoul?format=3
kubectl exec -it nginx-pod -c nginx-container -- curl -s 'wttr.in/{London,Busan}'
kubectl exec -it nginx-pod -c nginx-container -- curl -s http://ipinfo.io/city
kubectl exec -it nginx-pod -c nginx-container -- curl -k https://www.google.com | grep -o "<title>.*</title>";echo
while true; do kubectl exec -it nginx-pod -c nginx-container -- curl -s http://ipinfo.io/city; date "+%Y-%m-%d %H:%M:%S" ; echo "--------------" ; sleep 3; done
```
(참고) 파드 내에서 NAT 트래픽 정보
```bash
root@k8s-w2:~# c1 conntrack -L --dst-nat
tcp      6 0 TIME_WAIT src=172.16.46.11 dst=34.117.59.81 sport=59010 dport=80 src=127.0.0.1 dst=172.16.46.11 sport=15001 dport=59010 [ASSURED] mark=0 use=1
conntrack v1.4.5 (conntrack-tools): 1 flow entries have been shown.
 src=172.16.46.11 dst=34.117.59.81 sport=59010 dport=80     # 최초 요청 트래픽 정보
 src=127.0.0.1    dst=172.16.46.11 sport=15001 dport=59010  # 리턴 트래픽에서 IP/Port 정보를 보면, 출발지 포트가 15001 으로, 'istio-proxy' 경유를 했음을 알 수 있다
```
## (Pod 내부) IP Tables -> Istio-proxy 컨테이너 인입
- **파드 내 IPTables Chains/Rules 적용** (NAT 테이블) → '**Istio-proxy 컨테이너**'로 **인입**됩니다.
    - **OUTPUT → ISTIO_OUTPUT → ISTIO_REDIRECT** (**redir ports 15001**)

```bash
# iptables 확인
c1 iptables -t nat --zero
c1 iptables -v --numeric --table nat --list ISTIO_REDIRECT
watch -d "nsenter -t $C1PID -n iptables -v --numeric --table nat --list OUTPUT; echo ; nsenter -t $C1PID -n iptables -v --numeric --table nat --list ISTIO_OUTPUT; echo ; nsenter -t $C1PID -n iptables -v --numeric --table nat --list ISTIO_REDIRECT"
watch -d "nsenter -t $C1PID -n iptables -t nat -L -n -v"

# nginx 파드에서 TCP 트래픽 요청으로 인입 시, ISTIO_REDIRECT 에서 redir ports 15001 되어 'Istio-proxy 컨테이너'로 인입됩니다.
c1 iptables -t nat -L -n -v
Chain OUTPUT (policy ACCEPT 5 packets, 455 bytes)
 pkts bytes target        prot opt in     out     source               destination
    0     0 ISTIO_OUTPUT  tcp  --  *      *       0.0.0.0/0            0.0.0.0/0

Chain ISTIO_OUTPUT (1 references)
 pkts bytes target          prot opt in     out     source               destination
 ...
    0     0 ISTIO_REDIRECT  all  --  *      *       0.0.0.0/0            0.0.0.0/0

Chain ISTIO_REDIRECT (1 references)
 pkts bytes target     prot opt in     out     source               destination
    0     0 REDIRECT   tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            redir ports 15001
```

![]({{ site.url }}/img/post/devops/study/istio/8/20250608205204.png)
## (Pod 내부) Istio-proxy 컨테이너 -> Node의 host namespace
- '**Istio-proxy 컨테이너'** 는 대리인(Proxy) 역할로, **출발지 포트**를 **변경(+2)** 후 외부 웹서버에 연결을 한다
    - '**Istio-proxy 컨테이너'**의 로그 확인

```bash
(istio-k8s:default) root@k8s-m:~# kubectl logs nginx-pod -c istio-proxy -f
[2021-12-15T21:13:34.787Z] "GET /loc HTTP/1.1" 200 - via_upstream - "-" 017 187 187 "-" "curl/7.74.0" "d86b9c0b-9519-9c96-9b06-17938fa6ed3b" "ipinfo.io" "34.117.59.81:80" PassthroughCluster 172.16.46.11:36198 34.117.59.81:80 172.16.46.11:36196 - allow_any
```

- 파드 내에서 패킷 덤프 후 확인 : 출발지 포드를 변경(+2) 및 x-envoy 헤더를 추가

![]({{ site.url }}/img/post/devops/study/istio/8/20250608205254.png)

- lsof 확인 : envoy 에서 외부로 연결되는 정보이며, User ID(UID)가 1337 이다.

```bash
root@k8s-w2:~# c1 lsof -i TCP:80,15006 -n
COMMAND  PID            USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
envoy   3928            1337   40u  IPv4 1405154      0t0  TCP 172.16.46.11:38428->34.117.59.81:http (ESTABLISHED)
```

- 파드를 빠져나가기 전, 다시 한번 더 IPTables 적용 된다 ⇒ 이때, 이전 트래픽과 **매칭**되는 **Rule** 이 다른 것은 **UID 1337** 때문입니다. - [Docs](https://istio.io/latest/docs/ops/deployment/application-requirements/#pod-requirements)
    - **OUTPUT → ISTIO_OUTPUT**

```bash
# iptables 확인
c1 iptables -t nat --zero # 패킷 카운트 초기화

# 아래 처럼 Istio-proxy(15001)에서 빠져나온 부분은 UID 1337 매칭되어서 RETURN 되어 파드를 빠져나오게 됩니다!
c1 iptables -t nat -L -n -v
Chain ISTIO_OUTPUT (1 references)
 pkts bytes target             prot opt in     out     source               destination
    0     0 RETURN             all  --  *      lo      127.0.0.6            0.0.0.0/0
    0     0 ISTIO_IN_REDIRECT  all  --  *      lo      0.0.0.0/0           !127.0.0.1            owner UID match 1337
    0     0 RETURN             all  --  *      lo      0.0.0.0/0            0.0.0.0/0            ! owner UID match 1337
    2   120 RETURN             all  --  *      *       0.0.0.0/0            0.0.0.0/0            owner UID match 1337
    0     0 ISTIO_IN_REDIRECT  all  --  *      lo      0.0.0.0/0           !127.0.0.1            owner GID match 1337
    0     0 RETURN             all  --  *      lo      0.0.0.0/0            0.0.0.0/0            ! owner GID match 1337
    0     0 RETURN             all  --  *      *       0.0.0.0/0            0.0.0.0/0            owner GID match 1337
    0     0 RETURN             all  --  *      *       0.0.0.0/0            127.0.0.1
    2   120 ISTIO_REDIRECT     all  --  *      *       0.0.0.0/0            0.0.0.0/0
```

- **istio 애플리케이션 요구 사항 중 일부** - [Docs](https://istio.io/latest/docs/ops/deployment/application-requirements/#pod-requirements)
    - **Application UIDs**: Ensure your pods do **not** run applications as a user with the user ID (UID) value of `1337` because `1337` is reserved for the **sidecar proxy.**

## Node -> 외부
노드에 SNAT(masquerading) 설정이 되어 있을 경우, 출발지 IP 를 노드의 NIC IP로 변환하여 외부 웹서버에 요청을 전달합니다.
## 외부 웹서버(return traffic) -> Pod
웹 서버에서 리턴 트래픽이 파드에 돌아오는 과정은 **1.**2 에서 알아본 흐름과 유사합니다.

다만, 파드 내로 인입 시 **목적지 포트(+2)** 이므로, ‘**Nginx 컨테이너**’ 로 바로 가지 않고, '**Istio-proxy 컨테이너'** 로 먼저 가게 됩니다.
