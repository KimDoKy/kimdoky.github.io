---
layout: post
section-type: post
title: jekyll notes
category: tip
tags: [ 'tip' ]
---

## 템플릿 코드 표기하기

jekyll은 템플릿 언어를 사용하여 포스트를 작성합니다.

그에 따라 코드에서 사용이 제한되는 부분들이 존재합니다.
> 해당 이유로 에러가 발생하면 친절히 메일로 오류가 났음을 알려준다.

템플릿 코드를 포스트에 표기하기 위해서는 다음의 코드를 붙여주어야 합니다.

{% raw %}
```
{'% raw %'}
{'% endraw %'}
# jekyll은 템플릿 언어를 사용하기 때문에 코드를 그대로 넣으면 표기할수 없기 때문에 '를 첨가하였다.
```
{% endraw %}


## 제목에서 사용하면 안되는 기호

title에는 `:`를 넣으면 안된다.

> 제목에서 에러가 나면 에러가 난채로 업로드 되기 때문에, 에러가 난 사유를 금방 발견하지 못한다.