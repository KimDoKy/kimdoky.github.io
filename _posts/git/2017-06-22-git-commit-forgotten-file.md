---
layout: post
section-type: post
title: git. commit 후 빠진 파일 추가하기
category: git
tags: [ 'git' ]
---

간혹 commit 후에 commit에서 빠진 파일을 발견하는 경우가 종종 있다.

```
$ git commit -m 'initial commit'
$ git add 파일
$ git commit --amend
```

3개의 명령어 모두 하나의 커밋으로 기록되고, 두 번째 커밋이 첫 번째 커밋을 덮어쓴다.
