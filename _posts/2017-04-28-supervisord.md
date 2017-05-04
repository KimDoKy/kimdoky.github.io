---
layout: post
section-type: post
title: supervisord
category: deploy
tags: [ 'deploy' ]
---

Docker 공부중.

supervisord 는 서버상에서 지정한 프로그램이 다운되면 다시 실행해줌 (nginx, wsagi 등을 지정함으로써 서버가 다운되는걸 막아준다.)

supervisord는 Docker를 통해 이용시 demon을 off로 설정하여 이미지를 빌드해주어야 한다.

<http://hochulshin.com/python-supervisord/>
