---
layout: post
section-type: post
title: github contribution graph
category: git
tags: [ 'git' ]
---

commit 후 contribution graph에 적용이 안되는 현상이 발생했다.

몇일전 맥북 포맷하면서 git config가 날라가서 나타난 현상이었다.

git config 설정이 안되어 있어도 git-commit-push 모두 정상적으로 작동이 되어서

늦게 파악이 되었다. 덕분데 요 몇일동안의 커밋이 graph에 적용이 안되게 되었다.ㅠ


anyway..

해결법. 다시 셋팅해주면 된다!!


```
$ git config --global user.name "username"
$ git config --global user.email user@example.com
```
