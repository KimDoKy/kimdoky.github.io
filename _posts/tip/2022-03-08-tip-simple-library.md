---
layout: post
section-type: post
title: tip - 셸 스크립트로 파일안의 문자열 치환
category: tip
tags: [ 'tip' ]
---

레거시 코드에 이거저거 추가하다보니 이참에 프레임워크의 버전을 업그레이드하려고 하였습니다.

프레임워크 업그레이드를 하니 당연히 여기저기에서 라이브러리 충돌이 일어났습니다.

하나하나 해결해 나가던중, 공식 라이브러리 깃에서는 코드가 수정되어 있는데,

pip로 최신 버전을 설치해도 수정된 코드가 적용되지 않았습니다.

코드 한 줄만 수정하면 되는거라, 해당 라이브러리를 포크해서 작업하기 보다는 

셸 스크립트로 처리하는게 간편할 것이라고 판단했습니다.

(`drf_tracking` 라이브러리였고, 현재는 `drf_api_tracking`으로 바뀌었습니다.)

```
CMD find /usr/local/lib/python3.8/site-packages/rest_framework_tracking/base_models.p  y -exec perl -pi -e 's/django.utils.six/six/g' {} \;
```

Docker에 해당 스크립트를 추가하고 빌드해보니 잘 적용됨을 확인하였습니다.
