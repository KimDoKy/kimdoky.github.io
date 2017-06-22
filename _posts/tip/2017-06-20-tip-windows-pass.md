---
layout: post
section-type: post
title: tip - Windows 암호 잃어버렸을 때
category: tip
tags: [ 'tip' ]
---

오랫만에 윈도우 컴퓨터를 켰더니... 비밀번호가 생각나지 않는다...

구글링 결과 매우 간단히 풀 수 있었다.... 윈도우... 보안이 취약하다...

---

준비물 : Windows 설치 cd 혹은 usb(usb 추천), 패스워드 변경 프로그램([ntpwedit]({{ site.url }}/upload/ntpwed04.zip))

일단 이 방법만 있으면 Windows의 암호는 다 뚫을 수 있는 것으로 추정된다. admin 계정 조차도 뚫어버린다.  

그리고 방법 또한 매우 간단하다.

1. 윈도우 설치 모드로 부팅한다.

2. shift + f10 으로 커맨드창을 연다.

3. diskpart - disk volume - exit

위 명령으로 usb가 어떤 경로로 잡혀있는지 확인한다.

5. 프로그램이 있는 위치로 이동해서 프로그램을 실행한다.

```
etc:
f:
dir 또는 cd 프로그램 폴더
ntpwedit (Windows는 프로그램명만 입력하면 실행된다)
```

해당 계정을 선택해서 패스워드를 바꿔준 후 저장하고 종료한다.

재부팅이 되면 바꾼 패스워드로 접속한다.

끗.
