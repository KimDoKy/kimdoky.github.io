---
layout: post
section-type: post
title: Git modify commit message
category: git
tags: [ 'git' ]
---

# Git commit message 수정하기

## 바로 이전 commit message 수정하기

```
git commit --amend
```
## 특정 commit을 지정하여 message 수정하기

```
git rebase -i HEAD~~
```
> `~`갯수당 최근으로부터 commit 갯수

![]({{ url.site }}/img/post/git/modify1.png)

수정하려는 commit의 `pick`을 `edit`으로 수정하고 저장, 종료한다.

![]({{ url.site }}/img/post/git/modify2.png)
![]({{ url.site }}/img/post/git/modify3.png)

```
git commit --amend
```
`--amend` 옵션을 지정하면 `edit`으로 수정한 commit의 message를 수정할 수 있다.
![]({{ url.site }}/img/post/git/modify4.png)

수정이 완료되면 `--continue` 옵션을 지정한 `rebase`를 실행합니다.
![]({{ url.site }}/img/post/git/modify5.png)
