---
layout: post
section-type: post
title: SSH - Upload
category: tip
tags: [ 'tip' ]
---

### 원격 서버 → 로컬 서버로 파일 전송
#### scp [옵션] [계정명]@[원격지IP주소]:[원본 경로 및 파일] [전송받을 위치]

```ssh
scp abc@111.222.333.444:/src/app/index.html /src/app/project
```


### 로컬 서버 → 원격 서버로 파일 전송
#### scp [옵션] [원본 경로 및 파일] [계정명]@[원격지IP주소]:[전송할 경로]

```ssh
scp /src/app/project/index.html abc@111.222.333.444:/src/app/
```
