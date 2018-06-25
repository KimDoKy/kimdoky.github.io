---
layout: post
section-type: post
title: Introducing Python - chap7 - 연습문제
category: python
tags: [ 'python' ]
---

## 7.1 유니코드 문자열 변수 mystery를 생성하고, 여기에 값 '\U0001f4a9'를 할당하라. mystery와 mystery에 대한 유니코드 이름을 찾아서 출력하라.

```Python
>>> import unicodedata
>>> mystery = '\U0001f4a9'
>>> mystery
'💩'
>>> unicodedata.name(mystery)
'PILE OF POO'
```

## 7.2 mystery를 인코딩해보자. 이번에는 UTF-8로 바이트 변수 pop_bytes에 할당하고, 이를 출력한다.

```Python
>>> pop_bytes = mystery.encode('UTF-8')
>>> print(pop_bytes)
b'\xf0\x9f\x92\xa9'
```

## 7.3 UTF-8을 이용하여 pop_bytes를 문자열 변수 pop_string에 디코딩하여 출력하라. pop_string은  mystery와 같은가?

```Python
>>> pop_string = pop_bytes.decode('UTF-8')
>>> print(pop_string)
💩
>>> pop_string == mystery
True
```

## 7.4 옛 스타일의 포매팅을 사용하여 시를 써보자. 문자열 'roast beef', 'ham', 'head', 'clam'을 아래 문자열에 대체한다.

My kitty cat likes %s,  
My kitty cat likes %s,  
My kitty cat fell in his %s  
And now thinks he's a %s.  

```Python
>>> print("My kitty cat likes %s,\nMy kitty cat likes %s,\nMy kitty cat fell in his %s\nAnd now thinks he's a %s." % ('roast beef','ham','head','clam'))
My kitty cat likes roast beef,
My kitty cat likes ham,
My kitty cat fell in his head
And now thinks he's a clam.

# 모범 답안
>>> poem = '''
My kitty cat likes %s,
My kitty cat likes %s,
My kitty cat fell in his %s
And now thinks he's a %s.
'''
>>> args = ('roast beef','ham','head','clam')
>>> print(poem % args)
My kitty cat likes roast beef,
My kitty cat likes ham,
My kitty cat fell in his head
And now thinks he's a clam.
```

## 7.5 새로운 스타일의 포매팅을 사용하여 편지를 써보자. 다음 문자열을 letter 변수에 저장한다(다음 문제에서 이 변수를 사용한다.)

Dear {salutation} {name},  

Thank you for your letter. Wa are sorry that our {product}   {verbed} in your {room}. Please note that it should never be used in a {room}, especially near any {animals}.  

Send us your receipt and {amount} for shipping and handling. We will send you another {product} that, in our tests, is {percent}% less likely to have {verbed}.  

Thank you for you support.  

Sincerely,  
{spokesman}  
{jop_title}  

```Python
letter = '''
Dear {salutation} {name},

Thank you for your letter. Wa are sorry that our {product} {verbed} in your {room}. Please note that it should never be used in a {room}, especially near any {animals}.

Send us your receipt and {amount} for shipping and handling. We will send you another {product} that, in our tests, is {percent}% less likely to have {verbed}.

Thank you for you support.

Sincerely,
{spokesman}
{jop_title}
'''
```

## 7.6 response 딕셔너리를 만들어보라. 문자열의 키값은 'salutation', 'name', 'product', 'verbed'(verb의 과거), 'room', 'animals', 'amount', 'percision', 'spokesman', 'jop_title'이다. response 딕셔너리의 값을 임의로 넣어서 letter를 출력하라.

```Python
>>> response = {'salutation':'good',
...             'name':'DK',
...             'product':'apple',
...             'verbed':'error',
...             'room':'S+',
...             'animals':'dragon',
...             'amount':'$100',
...             'percent':50,
...             'spokesman':'Dick',
...             'jop_title':'ApComp'}
>>> print(letter.format(**response))
Dear good DK,

Thank you for your letter. Wa are sorry that our apple error in your S+. Please note that it should never be used in a S+, especially near any dragon.

Send us your receipt and $100 for shipping and handling. We will send you another apple that, in our tests, is 50% less likely to have error.

Thank you for you support.

Sincerely,
Dick
ApComp
```

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

```Python
mammoth = """
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
"""
```

## 7.8 파이썬의 정규표현식 함수를 사용하기 위해 re 모듈을 임포트하라. c로 시작하는 단어를 모두 출력하기 위해 re.findall()을 사용하라.

```Python
>>> import re
>>> re.findall('c\w*',mammoth)
['cheese', 'cial', 'city', 'ceive', 'car', 'cheek', 'could', 'cast', 'crush']

# 모범 답안
>>> pat = r'\bc\w*'
>>> re.findall(pat, mammoth)
['cheese', 'city', 'cheek', 'could', 'cast', 'crush']
```

`\b`는 단어와 비단어 사이의 경계의 시작을 의미한다. 단어의 시작이나 끝을 지정하기 위해 `\b`를 사용한다.   
`\w`는 문자, 숫자, 언더스코어를 포함한다.  
`*`는 0회이상 반복되는 단어 문자를 의미한다.  
이들을 결합하여 단도긍로 나오는 'c'를 포함한 c로 시작하는 단어를 찾는다.  
부호 앞에 등장하는 `r`을 입력하지 않으면, 파이썬은 `\b`를 백스페이스로 인식하여 전혀 다른 결과가 나올것이다.

## 7.9 c로 시작하는 네 글자의 단어를 모두 찾아라.

```Python
>>> for word in re.findall('c\w*', mammoth):
...     if len(word) == 4:
...         print(word)
cial
city
cast

# 모범 답안
# 단어의 끝을 가리키기 위해 마지막에 \b를 사용했다.
>>> pat = r'\bc\w{3}\b'
>>> re.findall(pat, mammoth)
['city', 'cast']

# 마지막 \b를 빼면 c로 시작하는 4글자 이상의 모든 단어에 대해 처음 4글자가 검색된다.
>>> pat = r'\bc\w{3}'
>>> re.findall(pat, mammoth)
['chee', 'city', 'chee', 'coul', 'cast', 'crus']
```

## 7.10 r로 끝나는 단어를 모두 찾아라.

```Python
# 모범 답안
# r로 끝나는 단어
>>> pat = r'\b\w*r\b'
>>> re.findall(pat, mammoth)
['your', 'fair', 'Or', 'scar', 'Mr', 'far', 'For', 'your', 'or']

# l로 끝나는 단어는 제대로 된 결과를 얻기 어렵다
>>> pat = r'\b\w*l\b'
>>> re.findall(pat, mammoth)
['All', 'll', 'Provincial', 'fall']

# 결과에 'll'이 있는 이유는?  
# \w 패턴은 아스키코드의 '를 제외한 문자, 숫자, 언더스코어만 매칭한다.
# 그 결과 you'll로 부터 ll만 찾게 된다.
# 문자 집합을 매칭하기 위해 '을 추가하면 된다.
>>> pat = r'\b[\w\']*l\b'
>>> re.findall(pat, mammoth)
['All', "you'll", 'Provincial', 'fall']
>>> pat = r"\b[\w']*l\b"
>>> re.findall(pat, mammoth)
['All', "you'll", 'Provincial', 'fall']
```

## 7.11 알파벳 모음 문자(a, e, i, o, u)가 세 번 연속으로 나오는 단어를 모두 찾아라.

```Python
# [^aeiou]는 \n를 포함한 모든 비모음 문자와 매칭한다.
# 'beau\nIn'를 제외하고는 잘 동작한다.
>>> pat = r'\b\w*[aeiou]{3}[^aeiou]\w*\b'
>>> re.findall(pat, mammoth)
['Queen', 'quietly', 'beau\nIn', 'Queen', 'squeeze', 'Queen']

# \s는 \n을 포함한 모든 공백 문자와 매칭한다.
# beau를 찾지 못한다. 세 번 연속으로 나오는 모듬 이후에 비모음을 매칭한다.
>>> pat = r'\b\w*[aeiou]{3}[^aeiou\s]\w*\b'
>>> re.findall(pat, mammoth)
['Queen', 'quietly', 'Queen', 'squeeze', 'Queen']

>>> pat = r'\b\w*[aeiou]{3}[^aeiou\s]*\w*\b'
>>> re.findall(pat, mammoth)
['Queen', 'quietly', 'beau', 'Queen', 'squeeze', 'Queen']
```

## 7.12 binascii 모듈의 unhexlify를 사용하여 다음 16진수 문자열을 바이트 변수 gif로 변환하라.

'47494638396101000100800000000000ffffff21f9' + '0401000000002c000000000100010000020144003b'

```Python
>>> import binascii
>>> hex_str = '47494638396101000100800000000000ffffff21f9' + '0401000000002c000000000100010000020144003b'
>>> gif = binascii.unhexlify(hex_str)
>>> len(gif)
42
```

## 7.13 gif 변수의 바이트는 한 픽셀의 투명한 GIF 파일을 정의한다. 유효한 GIF 파일은 문자열 GIF89a로 시작한다. 이 파일과 gif는 일치하는가?

```Python
>>> gif[:6] == b'GIF89a'
True
```

## 7.14 GIF의 가로 픽셀은 6바이트 오프셋으로 시작하는 16비트의 리틀엔디안 정수다. 세로 픽셀은 같은 크기의 8바이트 오프셋으로 시작한다. gif에서 이 값을 추출하여 출력하라. 이들은 모두 1인가?

```Python
>>> import struct
>>> width, height = struct.unpack('<HH', gif[6:10])
>>> width, height
(1, 1)
```
