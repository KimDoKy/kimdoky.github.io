---
layout: post
section-type: post
title: TDD chromedriver error
category: diary
tags: [ 'diary', 'tdd' ]
---

포맷 후 이전에 스터디하던 TDD git을 그대로 다시 적용하고 실행하니 이것저것 오류들이 발생하였다.

당연히 대부분 install error.

가상환경을 만든 후 모두 설치 했지만 해결이 안되는 것이 있었으니

```
selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH. Please see https://sites.google.com/a/chromium.org/chromedriver/home
```

selenium에서 chrome을 사용할때 드라이버 오류가 일어난다.

당연히 가상환경상에 pip로 아무리 install하여도 해결이 안된다.

해결법은

`brew install chromedriver`

사랑해요 [스택오버플로](http://stackoverflow.com/questions/8255929/running-webdriver-chrome-with-selenium)
