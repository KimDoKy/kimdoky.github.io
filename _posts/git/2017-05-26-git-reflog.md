---
layout: post
section-type: post
title: git. 버전 되돌아가기(reset.reflog)
category: git
tags: [ 'git' ]
---

한참 TDD를 하고 있는데 풀리지 않는 오류가 발생하였다.

무언가 놓친 것이 있었던 것이다...

한참 헤맷지만 점점 refactoring Cat이 되고 있었다.

그래서 이전 버젼으로 돌아가서 다시 작업을 하였다.

`git reflog`

```
1261456 HEAD@{0}: commit: ch 7.8 a URL for Adding List Items
71ba079 HEAD@{1}: commit (amend): ch7.3 Ensuring we have a regression test & ch7.7 new URL, view and template to display lists
ce98599 HEAD@{2}: commit (amend): ch7.3 Ensuring we have a regression test
8ce4440 HEAD@{3}: commit: ch7 Ensuring we have a regression test
[...]
```

되돌아갈 시점의 HEAD를 확인하고

```
git reset --hard HEAD@{1}
```

이렇게 고트님에게 되돌아 갈 방법이 생겼다.
