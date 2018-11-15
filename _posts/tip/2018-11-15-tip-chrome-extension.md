---
layout: post
section-type: post
title: tip. selenium으로 chrome 확장 프로그램 사용하기
category: tip
tags: [ 'tip' ]
---

## selenium으로 chrome 컨트롤시 확장 프로그램 적용하기

```python
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_extension('chrome_extention_path')

webdriver.Chrome('driver_path', chrome_options=chrome_optinos)
```

### extention path 알아내는 방법

[Where does Chrome store extensions?](https://stackoverflow.com/questions/14543896/where-does-chrome-store-extensions)


### 윈도우 환경에서는 권한 오류가 발생한다.

```
Permission denied
```

### 권한 오류 해결법

[stackoverflow](https://stackoverflow.com/questions/14543896/where-does-chrome-store-extensions)  

[muo](https://www.makeuseof.com/tag/fix-access-denied-folders-windows-10/)

> 아직 시간이 없어서 시도는 못해봤습니다.
