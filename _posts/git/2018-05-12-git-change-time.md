---
layout: post
section-type: post
title: git. Change commit time
category: git
tags: [ 'git' ]
---

git이 아무리 뛰어나다고는 해도 푸시하기 전까진 내 컴퓨터 안에서 작동하기 때문에

기존의 커밋들의 시간도 변경이 가능하지 않을까 라는 호기심이 생겼다.

역시나... 가능했다. 푸시를 하면 github의 contribution에도 영향이 주었다.

하지만 위험하므로 사용은 왠만해서는 하면 안된다. 열심히 쌓은 커밋들이 날아갈수도 있으니..

```
git filter-branch --env-filter \
    'if [ $GIT_COMMIT = 119f9ecf58069b265ab22f1f97d2b648faf932e0 ]
     then
         export GIT_AUTHOR_DATE="Fri Jan 2 21:38:53 2009 -0800"
         export GIT_COMMITTER_DATE="Sat May 19 01:01:01 2007 -0700"
     fi'
```

변경할 커밋의 해쉬값이 필요로 하고 변경할 시간을 지정해주면 된다.

unstage에 변경되거나 추가된 파일이 없는 상태에서만 작동한다.

출처[stackoverflow](https://stackoverflow.com/questions/454734/how-can-one-change-the-timestamp-of-an-old-commit-in-git)
