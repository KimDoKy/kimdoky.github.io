---
layout: post
section-type: post
title: ZSH - alias로 자주 사용하는 명령어 단축하기
category: tip
tags: [ 'tip' ]
---

터미널을 사용하다보면 긴 명령어들을 타이핑하기가 귀찮아지기 마련입니다.

그래서 자주 사용하는 명령어들을 자신만의 단축키로 지정하여 사용합니다.

명령어를 입력할 파일은 `~/.zshrc` 입니다.

입력 양식

```
alias dr='python manage.py runserver'
alias js='jekyll serve'
```

장고 서버 실행이나 깃 상태확인, 블로그 돌려보기 등의 단축키를 등록해두었는데,  

맥북을 포맷하거나 새로운 작업환경에서 등록은 필수.
