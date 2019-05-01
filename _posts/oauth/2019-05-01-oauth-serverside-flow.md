---
layout: post
section-type: post
title: OAuth 2.0 - Authorization Code Flow로 액세스 토큰 얻기
category: oauth
tags: [ 'oauth' ]
---

## Authorization Code Flow

authorization code grant(인가 코드 그랜트)는 일반적으로 백엔드와 함께 동작하는 웹 어플리케이션에서 사용된다. 예로 파이썬 서버와 HTML/JS 프론트엔드 애플리케이션 등이 있다.

```
# Authorization Code Flow
(RFC 6749)

+----------+
| Resource |
|   Owner  |
|          |
+----------+
     ^
     |
    (B)
+----|-----+          Client Identifier      +---------------+
|         -+----(A)-- & Redirection URI ---->|               |
|  User-   |                                 | Authorization |
|  Agent  -+----(B)-- User authenticates --->|     Server    |
|          |                                 |               |
|         -+----(C)-- Authorization Code ---<|               |
+-|----|---+                                 +---------------+
  |    |                                         ^      v
 (A)  (C)                                        |      |
  |    |                                         |      |
  ^    v                                         |      |
+---------+                                      |      |
|         |>---(D)-- Authorization Code ---------'      |
|  Client |          & Redirection URI                  |
|         |                                             |
|         |<---(E)----- Access Token -------------------'
+---------+       (w/ Optional Refresh Token)
```

1. 사용자가 client의 서비스에 접근한다.
2. client는 사용자에게 접근권한을 요청한다.
3. client는 사용자를 서비스 제공자와 연결한다. 서비스 제공자는 사용자에게 client가 리소스에 접근할 권한에 대해 허용 여부를 직접 질의한다.
4. (사용자가 허락했다는 가정) 서비스 제공자는 client server(backend)에게 사용자의 리소스에 접근할 수 있는 액세스 토큰과 교환할 수 있는 태그(인가 코드)를 전달한다.
5. client는 인가 코드를 이용해서 액세스 토큰을 요청한다.
6. 서비스 제공자는 인가 코드를 확인후 client server에게 액서스 토큰을 전달한다.
7. client server는 서비스 제공자가 준 액세스 토큰을 이용해서 서비스 제공자에게 필요한 리소스를 요청한다.
8. 서비스 제공자는 액세스 토큰을 확인후 client에게 리소스를 전달한다.
9. client는 전달받은 리소스를 이용해 사용자에게 서비스를 제공한다.


## authorization code grant flow

### 인가 요청

사용자 동의를 얻기 위한 첫 단계이다. 암시적 그랜트 플로우의 차이점은 `response_type` 파라미터의 값이 `token`이 아닌 `code`로 셋팅된다는 것이다. 이 파라미터 하나만 수정하면 플로우가 바뀌게 된다.

#### 스펙의 내용

인가 요청 엔드포인트는 서비스 제공자의 인가 엔드포인트으로서 관련 파라미터를 URL에 포함하여 전달한다. 전달된 파라미터는 `application/x-www-form-urlencoded` 포맷으로 인코딩되어야 한다.

```
GET /authorize?
    client_id={client_id}&
    redirect_uri={redirect_uri}&
    response_type=code&
    scope={scope}&
    state={state} HTTP/1.1
Host: server.example.com
```

- `client_id`: (필수) 애플리케이션의 고유한 클라이언트 ID
- `redirect_uri`: (선택) 서비스 제공자가 인가 요청에 대한 응답을 전달할 리다이렉션 엔드포인트
- `response_type`: (필수) 인가 코드 그랜트 플로우를 사용한다는 것을 나타내기 위한 파라미터. `code`로 셋팅되어야 한다.
- `scope`: (선택) 요청하는 접근 범위
- `state`: (권장) 옵션이지만 사용하는 것을 권장. 클라이언트의 요청과 그에 따른 콜백 간의 상태를 유지하기 위해 사용되며, 클라이언트가 서비스 제공자에게 전달하면 서비스 제공자는 이 값을 다시 응답에 포함해서 전달한다. CSRF 공격을 차단하가 위한 수단이 될 수 있다.

### 인가 응답

올바른 파라미터를 이용해 인가 요청 URL에 질의를 보내면 사용자는 사용자 동의 화면을 보게 된다.  
사용자가 동의하면 그에 대한 응답으로 액세스 토큰과 교환할 수 있는 인가 코드를 받을 수 있다.
(implicit grant의 경우 이 단계에서 액세스 토큰을 받는다.) 이 과정에서 두 가지 응답 형태로 나뉜다.

#### 성공

사용자가 승인하였다면, 관련된 모든 정보가 URL에 포함돼 리다이렉션 엔드포인트로 인가 코드를 전달된다.

```
# 성공 응답 형태

HTTP/1.1 302 Found
Location: {redirect_uri}?
    code={authorize_code}&
    state={state}
```

> 응답 값이 리다이렉션 엔드포인트의 URL 질의 컴포넌트로 전달된다. URL 질의 컴포넌트 부분을 하싱해야 한다.

응답 데이터로 받을 수 있는 파라미터는 다음과 같다.

- `code`: (필수) 액세스 토큰과 교환하는데 사용할 인가 코드
- `state`: (조건부 필수) 만약 state 파라미터가 인가 요청에 존대하면 그에 대한 응답에도 state 파라미터가 존재한다.

> 인가 코드는 1회용이기 때문에, 동일한 인가 코드로 새로운 액세스 토큰을 요청하면 실패한다.
그리고 인가 코드는 보안적인 이유로 비교적 짧은 만료 시간을 갖기 때문에 client는 인가 코드를 받으면 곧바로 사용해야 한다. OAuth 2.0에서는 인가 코드 만료시간을 10분으로 제한하도록 권장한다.

#### 에러

어떤 이유로 인가 요청이 거부되면 액세스 토큰은 전달되지 않는다. 인가 코드 그랜트 플로우에서 사용되는 에러 응답은 암시적 그랜트 플로우와 동일하지만, URL 프래그먼트가 아닌 URL 질의 컴포넌트로 전달된다.

```
# 에러 응답 형태

HTTP/1.1 302 Found
Location: {redirect_uri}?
    error={error_code}&
    error_description={error_description}&
    error_uri={error_uri}&
    state={state}
```

- `error`: (필수) 에러 코드로서 인가 요청이 실패한 이유를 나타낸다.
 - `invalid_request`: 요청 데이터가 잘못됨
 - `unauthorized_client`: 클라이언트 애플리케이션이 요청을 전달할 권한이 없음
 - `access_denied`: 사용자가 거부함
 - `unsupported_response_type`: 잘못된 응답 유형이 사용됨.(`response_type`을 잘못 지정함)
 - `server_error`: 서버 내에서 에러 발생으로 인가 요청이 처리가 안됨
 - `temporarily_unavailable`: 인가 서버가 일시적 장애 상태
- `error_description`: (선택) 사람이 읽을 수 있는 형태의 에러 메시지
- `error_uri`: (선택) 에러에 대한 자세한 정보위 웹 문서 링크
- `state`: (조건부 필수)

### 액세스 토큰 요청

인가 코드로 액세스 토큰을 요청해야 한다.

#### 스펙의 내용

인가 코드를 액세스 토큰과 교환하려면, 서비스 제공자의 토큰 엔드포인트로 필요한 파라미터를 POST 요청해야 한다. 파라미터는 `application/x-www-form-urlencoded` 포맷으로 전달해야 한다.

```
POST /token HTTP/1.1
Host: server.exmple.com
Authorization: Basic [encoded_client_credentials]   // 클라이언트 인증
Content-type: application/x-www-form-urlencoded

grant_type=authorization_code&
     code={authorization_code}&
     redirect_uri={redirect_uri}&
     client_id={client_id}
```

- `grant_type`: (필수) 액세스 토큰으로 교환하고자 한다는 것을 나타기 위해 `authorization_code`으로 셋팅해야 한다.
- `code`: 인가 요청으로 받은 인가 코드 값
- `redirect_uri`: (조건부 필수) 인가 요청에 리다이렉션 엔드포인트가 포함되었다면 액세스 토큰 요청에도 리다이렉션 엔드포인트가 포함되어야 한다.
- `client_id`: 애플리케이션의 고유 클라이언트 ID

액세스 토큰을 요청하려면 위 파라미터를 전달하고, 클라이언트 애플리케이션은 서비스 제공자에게 자기 자신을 증명해야 한다(= 클라이언트 인증).

> OAuth 2.0 스펙에서는 클라이언트 인증을 구현하도록 권장하지만, 실제로는 지원하지 않는 서비스 제공자가 많다. 이는 OAuth 2.0 스펙이 정식으로 승인되기 이전부터 많은 기업들이 사용하고 있었기 때문이다. 이 때문에 기업들이 아직 구현하지 않은 부분에 대해 스펙의 내용이 변경되기도 한다.  
따라서 여러 클라이언트 인증 방식이 존재하게 되었는데, (1)최종 버전의 스펙을 지원하는 서비스 제공자는 전달된 HTTP 요청의 인가 헤더로 클라이언트를 확인하고, (2)최종 버전 이전의 메커니즘을 지원하는 서비스 제공자는 요청 파라미터로 전달되는 클라이언트 시크릿을 보고 클라이언트를 확인한다.

#### 최종 버전 스펙 이전의 클라이언트 인증 방식

```
POST /token HTTP/1.1
Host: server.exmple.com
Content-type: application/x-www-form-urlencoded

grant_type=authorization_code&
     code={authorization_code}&
     redirect_uri={redirect_uri}&
     client_id={client_id}&
     client_secret={client_secret}
```

HTTP 질의에 인가 헤더가 빠지고, 클라이언트 시크릿 파라미터가 추가되었다.

### 액세스 토큰 응답

액세스 토큰 요청과 인가 코드가 유효하다면 응답으로 액세스 토큰을 받게 된다.

#### 성공

- `access_token`: (필수) 인가 요청의 성공으로 얻은 access_token
- `token_type`: 전달되는 토큰의 유형. 거의 bearer 토큰 유형.
- `expires_in`: (선택) 토큰의 유효기(초 단위)
- `refresh_token`: (선택) 액세스 토큰이 만료돼었을때 갱신을 위한 토큰
- `scope`: (조건부 필수) 인가된 범위와 요청된 범위가 같다면 생략될 수 있음. 다르다면 인가된 범위가 전달된다.

```
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
{
    "access_token":"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "token_type":"bearer",
    "refresh_token":"yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
    "expires_in":43199,
    "scope":"Basic_Profile"
}
```

위 응답은 json 포맷으로 전달되었지만, 서비스 제공자는 XML이나 Key-Value 같은 포맷으로 보낼 수도 있으니, 서비스 제공자의 문서에 토큰의 응답 포맷을 먼저 확인해야 한다.

#### 에러

인가 요청이 어떤 이유거 거부되면 아래의 파라미터를 포함한 HTTP 400(Bad Request) 에러 코드를 반환할 것이다.

- `error`: (필수) 에러 코드로서 요청이 실패한 이유를 나타낸다.
 - `invalid_request`: 요청 데이터가 잘못됨
 - `invalid_client`: 클라이언트 인증 실패
 - `invalid_grant`: 제공되 그랜트가 유효하지 않음
 - `unauthorized_client`: 클라이언트 애플리케이션이 요청을 전달할 권한이 없음
 - `unsupported_grant_type`: 지원하지 않는 그랜트 유형
 - `invalid_scope`: 전달된 권한이 유효하지 않음
- `error_description`: (선택) 사람이 읽을 수 있는 형태의 에러 메시지
- `error_uri`: (선택) 에러에 대한 자세한 정보위 웹 문서 링크

```
# 에러 응답 형태

HTTP/1.1 400 Bad Request
Content-Type: application/json;charset=UTF-8
Cache-Control: no-store
Pragma: no-cache
{
    "error":"invalid_client"
}
```

---

> 클라이언트 사이드 플로우는 나중에 다룰 예정.

> 시간이 되는대로 짬짬히 [RFC 6749](https://tools.ietf.org/html/rfc6749) 문서를 읽어보자.

> 출처 및 참조  
[OAuth 2.0 마스터](http://book.interpark.com/product/BookDisplay.do?_method=detail&sc.prdNo=266585781)
