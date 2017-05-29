---
layout: post
section-type: post
title: tip. Systemctl 명령어
category: tip
tags: [ 'tip' ]
---

### 서비스 상태 확인

```
systemctl status service_name.service_name
```

### 서비스 시작, 중지, 재시작

```
systemctl start service_name.service
systemctl stop service_name.service
systemctl restart service_name.service
```

### 부팅시 자동 실행

```
systemctl enable service_name.service
```

### 실행 중인 서비스 리스트 보기

```
systemctl list-units --type=service
```
