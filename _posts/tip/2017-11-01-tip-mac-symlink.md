---
layout: post
section-type: post
title: symlink 파일 생성하기 on Mac
category: tip
tags: [ 'tip' ]
---

심볼릭 링크(symbolic link)는 절대 혹은 상대 경로의 형태로 된 다른 파일이나 디렉터리에 대한 참조를 포함하고 있는 파일입니다.


```
$ ln -s {타겟이 되는 파일} {생성할 파일}
```

```
$ echo sample > _a.txt
$ cat _a.txt
sample

$ l
total 8
drwxr-xr-x   3 dokyungkim  staff   102B 11  1 23:39 .
drwxr-xr-x  14 dokyungkim  staff   476B 11  1 23:18 ..
-rw-r--r--   1 dokyungkim  staff     7B 11  1 23:39 _a.txt

$ ln -s _a.txt a.txt

$ l
total 16
drwxr-xr-x   4 dokyungkim  staff   136B 11  1 23:40 .
drwxr-xr-x  14 dokyungkim  staff   476B 11  1 23:18 ..
-rw-r--r--   1 dokyungkim  staff     7B 11  1 23:39 _a.txt
lrwxr-xr-x   1 dokyungkim  staff     6B 11  1 23:40 a.txt -> _a.txt

$ cat a.txt
sample

$ cat _a.txt
sample
```
