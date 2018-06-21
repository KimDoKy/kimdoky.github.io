---
layout: post
section-type: post
title: Introducing Python - chap7 - 연습문제
category: python
tags: [ 'python' ]
---

## 7.1 유니코드 문자열 변수 mystery를 생성하고, 여기에 값 '\U0001f4a9'를 할당하라. myst퓨ery와 mystery에 대한 유니코드 이름을 찾아서 출력하라.

## 7.2 mystery를 인코딩해보자. 이번에는 UTF-8로 바이트 변수 pop_bytes에 할당하고, 이를 출력한다.

## 7.3 UTF-8을 이용하여 pop_bytes를 문자열 변수 pop_string에 디코딩하여 출력하라. pop_string은  mystery와 같은가?

## 7.4 옛 스타일의 포매팅을 사용하여 시를 써보자. 문자열 'roast beef', 'ham', 'head', 'clam'을 아래 문자열에 대체한다.

My kitty cat likes %s,
My kitty cat likes %s,
My kitty cat fell in his %s
And now thinks he's a %s.

## 7.5 새로운 스타일의 포매팅을 사용하여 편지를 써보자. 다음 문자열을 letter 변수에 저장한다(다음 문제에서 이 변수를 사용한다.)

Dear {salutation} {name},

Thank you for your letter. Wa are sorry that our {product} {verbed} in your {room}. Please note that it should never be used in a {room}, especially near any {animals}.

Send us your receipt and {amount} for shipping and handling. We will send you another {product} that, in our tests, is {percent}% less likely to have {verbed}.

Thank you for you support.

Sincerely,
{spokesman}
{jop_title}

## 7.6 response 딕셔너리를 만들어보라. 문자열의 키값은 'salutation', 'name', 'product', 'verbed'(verb의 과거), 'room', 'animals', 'amount', 'percision', 'spokesman', 'jop_title'이다. response 딕셔너리의 값을 임의로 넣어서 letter를 출력하라.

## 7.7 정규표현식은 텍스트 작업에 매우 편리하다. 다음의 텍스트 샘플에 정규표현식을 적용해보라. 이것은 1866년에 제임스 맥킨타이어가 쓴 '맘모스 치즈 예찬'이다. 이 시는 여행 중에 온타리오에서 만든 7천 파운드의 치즈에 대한 시다. 이 텍스트 문자열을 mammoth 변수에 할당한다.

We have seen the Queen of cheese,
Laying quietly at your ease,
Gently fanned by evening breeze,
Thy fair form no flies dare seize.

All gaily dressed soon you'll go
To the great Provincial Show,
To be admired by many a beau
In the city of Toronto.

Cows numerous as a swarm of bees,
Or as the leaves upon the trees,
It did require to make thee please,
And stand unrivalled Queen of Cheese.

May you not receive a scar as
We have heard that Mr. Harris
Intends to send you off as far as
The great World's show at Paris.

Of the youth beware of these,
For some of them might rudely squeeze
And bite your cheek; then songs or glees
We could not sing o' Queen of Cheese.

We'rt thou suspended from baloon,
You'd cast a shade, even at noon,
Folks would think it was the moon
About to fall and crush them soon.

## 7.8 파이썬의 정규표현식 함수를 사용하기 위해 re 모듈을 임포트하라. c로 시작하는 단어를 모두 출력하기 위해 re.findall()을 사용하라.

## 7.9 c로 시작하는 네 글자의 단어를 모두 찾아라.

## 7.10 r로 끝나는 단어를 모두 찾아라.

## 7.11 알파벳 모음 문자(a, e, i, o, u)가 세 번 연속으로 나오는 단어를 모두 찾아라.

## 7.12 binascii 모듈의 unhexlify를 사용하여 다음 16진수 문자열을 바이트 변수 gif로 변환하라.

'47494638396101000100800000000000ffffff21f9' + '0401000000002c000000000100010000020144003b'


## 7.13 gif 변수의 바이트는 한 픽셀의 투명한 GIF 파일을 정의한다. 유효한 GIF 파일은 문자열 GIF89a로 시작한다. 이 파일과 gif는 일치하는가?

## 7.14 GIF의 가로 픽셀은 6바이트 오프셋으로 시작하는 16비트의 리틀엔디안 정수다. 세로 픽셀은 같은 크기의 8바이트 오프셋으로 시작한다. gif에서 이 값을 추출하여 출력하라. 이들은 모두 1인가?
