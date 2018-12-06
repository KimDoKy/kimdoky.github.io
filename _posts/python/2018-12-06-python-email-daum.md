---
layout: post
section-type: post
title: Python - Daum 메일 보내기
category: python
tags: [ 'python' ]
---

Django는 `django.core.mail.send_mail`을 통해서 메일을 발송하도록 하고 있다.

온라인 상의 메일 발송 예제는 대부분 gmail을 기준으로 한다.

```python
>>> from django.core.mail import send_mail
>>> send_mail('Django mail', 'This e-mail was sent with Django.',
'your_account@gmail.com', ['your_account@gmail.com'], fail_
silently=False)
```

하지만, 실제로 업무에서 사용할 때는 Daum이나 Naver 메일로 발송을 해야 하는 경우들이 종종 있다.

그래서 Django의 `send_mail`을 이용해서 발송하려 했지만, 실패했다.

Django setting에서 `EMAIL_USE_SSL`를 통해 SSL로 접속해도 계속 실패했다.

국내 메일의 SMTP를 사용하려면 `smtplib` 모듈이 필요하다.

```python
>>> from smtplib import SMTP_SSL
>>> toEmail = 'abmu333@hanmail.net'
>>> fromEmail = 'neverlandpan@hanmail.net'
>>> titleEmail = 'Test Title'
>>> body = "한글 테스트 메일"
>>> body = str(body)
>>> msg = "\r\n".join(["From: " + fromEmail, "To: " + toEmail, "Subject: " + titleEmail, "", body])
>>> conn = SMTP_SSL('smtp.daum.net:465')
>>> conn.ehlo()
>>> conn.login(user, pw)
(235, b'PLAIN authentication successful for DaumID - auth_daum')
>>> conn.sendmail(fromEmail, toEmail, msg)
>>> conn.close()
```

메일 발신까지는 몇 분의 시간차가 있다.  

주의 할 점은 한글을 사용시 `UnicodeEncodeError`가 발생한다. string으로 형변환을 해주면 해결된다. 그리고 SMTP로 발송하면 다음의 메일 콘솔창에서 메일 발송 이력이 남지 않는다.

> 출처 [webisfree.com](https://webisfree.com/2018-08-05/python-daum-smtp%EB%A1%9C-%EC%9D%B4%EB%A9%94%EC%9D%BC-%EB%B3%B4%EB%82%B4%EB%8A%94-%EB%B0%A9%EB%B2%95)
