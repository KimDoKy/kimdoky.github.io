---
layout: post
section-type: post
title: OAuth, Djang로 social login 구현하기
category: api
tags: [ 'project' ]
---

## OAuth는??

### [OAuth](http://d2.naver.com/helloworld/24942)

최근 인터넷 서비스들은 서비스 중에서 사용자가 일부 필요한 것만 사용할 수 있게 하는 SaaS(Softwarer as a Service)의 형태로 서비스된다.(Facebook, 트위터  등)
외부 서비스와 연동되는 facebook이나 트위터의 기능을 이용하기 위해 사용자가 facebook이나 트위터에 로그인하는 것이 아니라, 별도의 인증 절차를 거치면 다른 서비스에서 Facebook과 트위터의 기능을 이용할 수 있게 되는것이다.  
이 방식에서 사용하는 인증 절차가 OAuth이다.

용어 | 설명
---|---
User|Service Provider에 계정을 가지고 있으면서, Consumer를 이용하려는 사용자
Service Provider|OAuth를 사용하는 Open API를 제공하는 서비스
Consumer|OAuth 인증을 사용해  Service Provider의 기능을 사용하려는 애플리케이션이나 웹 서비스
Request Token|Consumer가 Service Provider에세 권한을 인증받기 위해 사용하는 값. 인증이 완료된 후에는 Acceses Token으로 교환한다.
Access Token|인증 후 Consumer가 Service Provider의 자원에 접근하기 위한 키를 포함한 값



#### 회사 방문 과정의 예로 비교

 	|회사 방문 과정|	OAuth 인증 과정
---|---|---
1|	나방문씨가 안내 데스크에서 업무적인 목적으로 김목적씨를 만나러 왔다고 말한다.	|Request Token의 요청과 발급
2|	안내 데스크에서는 김목적씨에게 나방문씨가 방문했다고 연락한다.	|사용자 인증 페이지 호출
3|	김목적씨가 안내 데스크로 찾아와 나방문씨의 신원을 확인해 준다.	|사용자 로그인 완료
4|	김목적씨는 업무 목적과 인적 사항을 안내 데스크에서 기록한다.	|사용자의 권한 요청 및 수락
5|	안내 데스크에서 나방문 씨에게 방문증을 발급해 준다.	|Access Token 발급
6|	김목적씨와 나방문씨는 정해진 장소로 이동해 업무를 진행한다.	|Access Token을 이용해 서비스 정보 요청


#### Request Token 발급 요청시 사용하는 매개변수

매개변수|	설명
---|---
`oauth_callback`|	Service Provider가 인증을 완료한 후 리다이렉트할 Consumer의 웹 주소. 만약 Consumer가 웹 애플리케이션이 아니라 리다이렉트할 주소가 없다면 소문자로 'oob'(Out Of Band라는 뜻)를 값으로 사용한다.
`oauth_consumer_key`|	Consumer를 구별하는 키 값. Service Provider는 이 키 값으로 Consumer를 구분한다.
`oauth_nonce`|	Consumer에서 임시로 생성한 임의의 문자열. `oauth_timestamp`의 값이 같은 요청에서는 유일한 값이어야 한다. 이는 악의적인 목적으로 계속 요청을 보내는 것을 막기 위해서이다.
`oauth_signature`|	OAuth 인증 정보를 암호화하고 인코딩하여 서명 값. OAuth 인증 정보는 매개변수 중에서 `oauth_signature`를 제외한 나머지 매개변수와 HTTP 요청 방식을 문자열로 조합한 값이다. 암화 방식은 `oauth_signature_method`에 정의된다.
`oauth_signature_method`|	`oauth_signature`를 암호화하는 방법. HMAC-SHA1, HMAC-MD5 등을 사용할 수 있다.
`oauth_timestamp`|	요청을 생성한 시점의 타임스탬프. 1970년1월 1일 00시 00분 00초 이후의 시간을 초로 환산한 초 단위의 누적 시간이다.
`oauth_version`|	OAuth 사용 버전. 1.0a는 1.0이라고 명시하면 된다.

<!--#### oauth_signature 만들기

1. 요청 매개변수를 모두 모은다. `oauth_signature`를 제외하고, `oauth_`로 시작하는 OAuth 관련 매개변수를 모은다. POST body에서 매개변수를 사용하고 있다면 이 매개변수도 모아야 한다.
2. 매개변수를 정규화(Normalize)한다. 모든 매개변수를 사전순을 정렬하고 각각의 키(key)와 값(value)애 URL 인코딩을 적용한다.URL 인코딩을 실시한 결과를 = 형태로 나열하고 각 쌍 사이에는 & 을 넣는다. 이렇게 나온 결과 전체에 또  URL 인코딩을 적용한다.
3. Signature Base String을 만든다. HTTP method 명(GET, POST), Consumer가 호출한 HTTP URL 주소(매개변수 제외), 정규화한 매개변수를 '&'를 사용해 결합한다. 즉 '[GET|POST] + & + [URL 문다렿호 매개변수는 제외] + [정규화한 매개변수]' 형태가 된다.
4. 키 생성.  3번 과정을 거쳐 생성한 문자열을 암호화한다. 암호화할 때 Consumer Secret Key를 사용한다. Consumer Secret Key는 Consumer가 Service Provider에 사용 등록할때 발급받은 값이다.
-->

#### OAth 2.0
OAuth 1.0은 웹 애플리케이션이 아닌 애플리케이션에서는 사용하기 곤한하고, 절차가 복잡하여 OAuth 구현 라이브러리흫 제작하기 어렵고, 이런저런 복잡한 절차 때문에 Service Provider에게도 연산 부담이 발생한다.

이러한 단점을 개선한 것이 OAuth 2.0 이다. OAuth 1.0과 호환성이 없고, 아직 최종안이 발표되지 않았지만 많은 기업이 OAuth 2.0을 사용하고 있디.

- 웹 애플리케이션이 아닌 애플리케이션 지원 강화
- 암호화가 필요 없음. HTTP를 사용하고 HMAC을 사용하지 않는다.
- Signature 단순화 정렬과 URL 인코딩이 필요없다.
- Access Token 갱신 OAuth 1.0에서 Access Token을 받으면 Access Token을 계속 사용할 수 있었다.

### Django에 oAuth2.0 소셜 로그인 기능

#### 1. Insrall python-social-auth

```
pip install python-social-auth
```

#### 2. settings.py
	- INSTALLED_APPS에 항목 추가
		- 새롭게 설치한 python-social-auth app을 설정
		- 새롭게 User social auths 테이블에 생성되어 Third party 가입한 사용자를 관리 합니다.
	- TEMPLATE_CONTEXT_PROCESSORS 에 항목 추가
		- social.apps.django_apps.context_processors.backends
		- social.apps.django_apps.context_processors.login_redirect
	- AUTHENTICATION_BACKENDS 새롭게 추가
		- 인증 체계에 사용될 backend를 등록하는 항목
		- 기본으로 django.contrib.auth.backends.ModelBackend
		- python-social-auth의 facebook을 추가
	- OAuth 관련 변수 설정
		- SOCIAL_AUTH_LOGIN_REDIRECT_URL
			- 로그인 후 되돌아올 URL
		- SOCIAL_AUTH_URL_NAMESPACE
			- 인증 URL의 Namespace
		- SOCIAL_AUTH_FACEBOOK_KEY/Secret
			- Facebook 인증 Key/Secret
		- SESSION_SERIALIZER
			- 세션 객체를 직렬화하는 처리기
			- [참고자료](http://lueseypid.tistory.com/42)

```python
INSTALLED_APPS = (  
   ...
   'social.apps.django_app.default',
   ...
)

TEMPLATE_CONTEXT_PROCESSORS = (  
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (  
   'social.backends.facebook.FacebookOAuth2',
   # 'social.backends.google.GoogleOAuth2',
   # 'social.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'  
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Facebook
SOCIAL_AUTH_FACEBOOK_KEY = 'Facebook App ID'  
SOCIAL_AUTH_FACEBOOK_SECRET = 'Facebook App Secret Key'

# Google
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

# Twitter
# SOCIAL_AUTH_TWITTER_KEY = ''
# SOCIAL_AUTH_TWITTER_SECRET = ''

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'  
```

#### 3. `urls.py`

```
url(r'', include('social.apps.django_app.urls', namespace='social')),  
```
위에서 지정한 social의 경우 탬플릿에서 아래처럼 사용할 수 있음.
{% raw %}
```
<a href="{% url 'social:begin' 'facebook' %}?next={{ request.path }}">Login with Facebook</a>
```
{% endraw %}

- in case of google
- `url 'social:begin' 'facebook'` 대신에 `'goole-oauth2'`를 입력

필요에 따라 아래처럼 Django에서 기본으로 제공하는 login/logout을 가져올 수 있음

```
url(r'', include('django.contrib.auth.urls', namespace='auth')),  
```

위에서 지정한 auth라는 이름은 후에 템플릿에서 아래처럼 사용할 수 있음
{% raw %}
```
 <a href="{% url 'auth:logout' %}?next={{ request.path }}">Logout</a>
```
{% endraw %}

#### 4. Get Client IDs for the social sites

- [facebook 개발자 사이트](https://developers.facebook.com/)에 접속
- 상단 메뉴의 My Apps의 Add a New App 클릭
- 앱 종류는 웹 사이트를 선택
- 앱 이름을 입력하고 Create New Facebook ID를 클릭
- 다른 앱의 테스트 앱인지 물어보는 팝업착에서 No를 선택하고, 카테고리를 선택하고, Create App ID를 클릭
- Site URL, Mobile Site URL 실제 도메인으 입력함. 나중에 수정할 수 있으므로 아무거나 입력해도 됨.
- 위 과정으로 새로운 앱을 다 만든것. 화면을 Refresh하면 상단의 My Apps에 새롭게 생성된 앱이 보일 것임.
- My Apps에서 새로 추가한 앱을 선택
- 이는 실제로 운영할 서비스용 앱에 대한 설정 화면임. 따라서 테스트를 해복기 위해 좌측 메뉴 중 Test Apps를 클릭
- 우측 상단의 Create a Test App을 클릭하여 새롭게 추가
- 새롭게 생성한 Test App의 좌측 메뉴중 Settings를 클릭하면 Basic, Advanced, Migrations 가 나옴
- 그 중 Basic 탭에 있는 App Domains, Site URL, Mobile Site URL 모두 'http://localhost/'를 입력하고 Save Changes 버튼을 클릭. (우리가 테스트 할 곳이기 때문에 localhost로 설정하는 것.)

#### 5. settings.py에 key 입력

```
SOCIAL_AUTH_FACEBOOK_KEY = 'Facebook App ID'  
SOCIAL_AUTH_FACEBOOK_SECRET = 'Facebook App Secret Key'  
```

이렇게 Facebook에 앱을 등록하여 받은 key값으로 본인의 Django 사이트에 로그인 할 수 있습니다.


#### 해당 내용들 참고할 사이트
>
[Facebook 개발자 문서](https://developers.facebook.com/docs/facebook-login/permissions#reference-public_profile)
>
[Pipeline](https://python-social-auth.readthedocs.io/en/latest/pipeline.html#authentication-pipeline)
>
[KwangYoun Jung](http://initialkommit.github.io/2015/04/27/django-newbie-adding-facebook-authentication-to-a-django-app/)
>
[코딩도장](http://codingdojang.com/scode/280)
>
[django-social-auth](https://github.com/omab/django-social-auth)
>
[Javier Aguirre|사용자 프로필 만들기](http://javaguirre.me/2013/11/06/creating-a-user-profile-in-python-social-auth-in-django/)
>
[Django에서 social login library 사용](http://i5on9i.blogspot.kr/2016/01/django-social-log-in-library.html)
