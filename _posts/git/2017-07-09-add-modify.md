---
layout: post
section-type: post
title: git. add 에 포함 된 파일 취소하기
category: git
tags: [ 'git' ]
---

commit을 하기 위해 파일들을 add를 하였는데,

일부 파일을 따로 commit하기 위해서 add한 파일의 일부를 취소하려고 하였다. 파일의 갯수가 많아서 따로 분리하기 위함이었다.

```
$ git rm --cached <filename>
```

디렉터리라면 `-r` 옵션을 붙여준다.
