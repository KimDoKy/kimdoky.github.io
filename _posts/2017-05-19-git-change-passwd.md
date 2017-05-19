---
layout: post
section-type: post
title: git password 변경시 로컬에 적용하기
category: git
tags: [ 'git' ]
---

github을 사용하다 보면 password이 기억이 나지 않는 경우들이 종종 있다.

그래서 password를 변경 했을 경우, 로컬에 인증실패가 발생하여 push가 되지 않는다.

![]({{ url.site }}/img/post/git/change_pw.png)

기존 정보를 삭제하고 다시 입력하면 된다.

```
git config --unset credential.helper
```

![]({{ url.site }}/img/post/git/change_pw2.png)
