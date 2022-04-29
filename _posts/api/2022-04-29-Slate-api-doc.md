---
layout: post
section-type: post
title: Slate으로 API 문서 만들기
category: api
tags: [ 'api' ]
---

## Slate는??

예쁜 API 문서를 빨리 만들수 있습니다.  

[sample page](https://slatedocs.github.io/slate/#introduction)

## 사용방법

[Slate](https://github.com/slatedocs/slate)에서 클론합니다.

slate 프로젝트의 `source` 디렉터리안의 `index.html.md`에 API를 작성합니다.

## Deploy

배포 방법에는 크게 **Github을 이용하는 것**과 **자신의 서버에 배포**하는 방법이 있습니다.  

자세한 내용은 [여기](https://github.com/slatedocs/slate/wiki/Deploying-Slate)

전 이미 Github 페이지를 블로그로 사용하고 있기 때문에 자신의 서버에 배포하는 방법만 기록합니다.

- 실행환경: macbook

```
bundle exec middleman build --clean
```

위 명령어를 실행하면 build라는 디렉터리가 생기며

그 안에 index.html 파일을 실행하면 됩니다.


정적으로 문서를 생성하기 때문에 관리도 편하고 예쁘고 좋습니다.  

물론 Swagger와 같은 자동 api 생성 도구도 좋지만, 결국 주석을 코드에 모두 적어야 하기 때문에 그게 그거 아닌가... 라는 생각이 듭니다. 개인의 취향이나 팀의 성격에 따라 고르시면 되겠죠.
