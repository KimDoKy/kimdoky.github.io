---
layout: post
section-type: post
title: OAuth 2.0 - 액세스 토큰 갱신하기
category: oauth
tags: [ 'oauth' ]
---

# Refresh Token Flow

```
+--------+                                           +---------------+
|        |--(A)------- Authorization Grant --------->|               |
|        |                                           |               |
|        |<-(B)----------- Access Token -------------|               |
|        |               & Refresh Token             |               |
|        |                                           |               |
|        |                            +----------+   |               |
|        |--(C)---- Access Token ---->|          |   |               |
|        |                            |          |   |               |
|        |<-(D)- Protected Resource --| Resource |   | Authorization |
| Client |                            |  Server  |   |     Server    |
|        |--(E)---- Access Token ---->|          |   |               |
|        |                            |          |   |               |
|        |<-(F)- Invalid Token Error -|          |   |               |
|        |                            +----------+   |               |
|        |                                           |               |
|        |--(G)----------- Refresh Token ----------->|               |
|        |                                           |               |
|        |<-(H)----------- Access Token -------------|               |
+--------+           & Optional Refresh Token        +---------------+
```

액세스 토큰이 만료되기 전까지는 (C),(D) 단계를 반복하다가, 액세스 토큰이 만료됨을 인지하게되면 (G)단계로 가야한다.
(G): 클라이언트는 서비스 제공자로부터 인증을 받고 리프레시 토큰을 전달하여 새로운 액세스 토큰을 요청한다.
(H): 인가 서버는 클라이언트를 인증하고 전달된 리프레시 토큰을 확인한다. 확인되면 새로운 액세스 토큰과 새로운 리프레시 토큰을 발급한다.

## 액세스 토큰 갱신 요청

클라이언트는 서비스 제공자의 토큰 엔드포인트로 액세스 토큰 갱신 요청을 보낸다. 전달되는 모든 데이터는 `application/x-www-form-urlencoded` 포맷으로 인코딩돼야 한다.

- `grant_type`: (필수) 파라미터 값은 `refresh_token`이어야 한다.
- `refresh_token`: (필수) 클라이언트에게 발급된 리프레시 토큰
- `scope`: (선택) 접근이 허가된 범위를 나타내는 문자열. 공백, 대소문자 구분. 생략하면 원래의 접근 권한 범위와 동일하게 처리

```
POST /token HTTP/1.1
Host: server.example.com
Authorization: Bearer {access_token}
Content-type: application/x-www-form-urlencoded

grant_type=refresh_token&
refresh_token={refresh_token}
```

### 액세스 토큰 응답

```
HTTP/1.1 200 OK
Content_Type: application/json;charset=UTF-8
Cache-Control: no-store
Pramgma: no-cache

{
  "access_token":"xxxxxxxxxxxxxxxxxx",
  "token_type":"bearer",
  "expires_in":3600,
  "refresh_token":"yyyyyyyyyyyyyyyyyy",
}
```

### 에러 응답

```
HTTP/1.1 400 Bad Request
Content-Type: application/json;charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
{
    "error":"invalid_request"
}
```

---

> 시간이 되는대로 짬짬이 [RFC 6749](https://tools.ietf.org/html/rfc6749) 문서를 읽어보자.

> 출처 및 참조  
[OAuth 2.0 마스터](http://book.interpark.com/product/BookDisplay.do?_method=detail&sc.prdNo=266585781)
