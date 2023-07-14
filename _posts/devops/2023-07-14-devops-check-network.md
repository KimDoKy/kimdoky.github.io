---
layout: post
section-type: post
title: 통신 상태를 확인하는 방법
category: deploy
tags: [ 'network' ]
---

## IP 패킷이 도착하는지 확인하기

- 네트워크에 문제가 발생했다면 패킷 도착 여부를 확인하는 작업부터 시작해야 한다.
- 상대방에게 IP 패킷이 도착하지 않는다면 문제 원인을 분리해서 어디까지 IP 패킷이 도착하는지 문제 범위를 좁혀가야 한다.

```bash
# IP 패킷이 도착하는 경우
$ ping 142.250.206.206 -c 4
PING 142.250.206.206 (142.250.206.206): 56 data bytes
64 bytes from 142.250.206.206: icmp_seq=0 ttl=57 time=45.671 ms  <- 응답의 바이트 수, 응답시간, TTL을 표시
64 bytes from 142.250.206.206: icmp_seq=1 ttl=57 time=46.694 ms       상대방까지 IP 패킷이 도착했다는 의미
64 bytes from 142.250.206.206: icmp_seq=2 ttl=57 time=42.507 ms
64 bytes from 142.250.206.206: icmp_seq=3 ttl=57 time=45.939 ms

--- 142.250.206.206 ping statistics ---
4 packets transmitted, 4 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 42.507/45.203/46.694/1.601 ms

# IP 패킷이 도착하지 않는 경우
$ ping 223.130.200.104 -c 4
PING 223.130.200.104 (223.130.200.104): 56 data bytes
Request timeout for icmp_seq 0
Request timeout for icmp_seq 1
Request timeout for icmp_seq 2

--- 223.130.200.104 ping statistics ---
4 packets transmitted, 0 packets received, 100.0% packet loss
```

## DNS로 이름 해석이 가능한지 확인하기

- 상대방까지 IP 패킷이 도착해도 도메인명을 IP 주소로 변환하는 기능에 문제가 있다면 통신이 불가능하다.
- 많은 경우 목적지 주소를 도메인명으로 지정하기 때문이다.
- DNS 설정에 문제가 있거나, DNS 서버가 무응답이거나, DNS 서버까지 IP 패킷이 도달하지 않는 등의 원인이 있다.

```bash
# 정상 동작 중
$ nslookup google.com
Server:		192.168.0.1
Address:	192.168.0.1#53

Non-authoritative answer:
Name:	google.com
Address: 142.250.206.206  <- 도메인명에 대응하는 IP 주소
```

## 라우팅의 정상 동작 여부 확인하기

- IP 패킷은 여러 라우터를 경우해서 상대방에게 도착한다. 

```bash
$ traceroute 142.250.206.206
traceroute to 142.250.206.206 (142.250.206.206), 64 hops max, 52 byte packets
 1  192.168.0.1 (192.168.0.1)  3.962 ms  3.262 ms  3.534 ms
 2  59.16.85.254 (59.16.85.254)  105.549 ms *  17.081 ms
 3  112.190.107.65 (112.190.107.65)  5.961 ms  5.441 ms  4.475 ms
 4  112.190.109.73 (112.190.109.73)  6.966 ms
    112.190.109.69 (112.190.109.69)  4.908 ms
    112.190.111.237 (112.190.111.237)  4.762 ms
 5  112.174.49.145 (112.174.49.145)  10.753 ms  10.253 ms
    112.174.47.153 (112.174.47.153)  11.213 ms
 6  112.174.84.54 (112.174.84.54)  11.321 ms
    112.174.84.22 (112.174.84.22)  18.619 ms
    112.174.84.18 (112.174.84.18)  11.200 ms
 7  72.14.243.228 (72.14.243.228)  43.593 ms
    72.14.202.136 (72.14.202.136)  35.115 ms  34.829 ms
 8  * 108.170.243.97 (108.170.243.97)  42.374 ms *
 9  142.251.60.192 (142.251.60.192)  44.700 ms
 ...
```

## 할당된 글로벌 IP 주소 확인하기

웹에서 ip 주소를 확인한다.
