---
layout: post
section-type: post
title: git. Change branch name
category: git
tags: [ 'git' ]
---

기존에 공부용으로 사용하고 있는 Git을 정리하다가 Branch name도 따로 정리할 필요가 있다고 판단되었습니다.

[Doky's Study Git](https://github.com/KimDoKy/study/)의 브랜치를 따로 정리하였습니다.

![]({{ url.site }}/img/post/git/branch.png)
> 정리하고 나니 마음이 평화로워지는군요 :)

Branch 이름을 변경하는 것은 간단히 생각해서

로컬에서 바꾸려는 브랜치를 새로운 이름으로 복사한다. -> 리모트에서 기존 브랜치를 삭제한다 -> 교체된 브랜치를 푸시한다.

라는 수순이 됩니다. (브랜치 복사시 커밋 내역도 그대로 복사되어 기존의 브랜치를 그대로 계승합니다.)
> 제가 잘못 이해하고 있다면 알려주세요.

## 브랜치 이름 변경하기

1. local에 있는 branch 이름 변경하기
```
git branch -m oldbranch newbranch
```

2. remote에 존재하는 oldbranch 삭제하기
```
git push origin :oldbranch
```
3. newbranch push 하기
```
git push origin newbranch
```

출처:[uujing의 블로그](http://you9010.tistory.com/entry/git-remote-branch-이름-변경하기)
