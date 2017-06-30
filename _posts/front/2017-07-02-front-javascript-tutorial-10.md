---
layout: post
section-type: post
title: JavaScript Tutorial - 10. Assignment
category: front
tags: [ 'front' ]
---

## JS Assignment
할당 연산자는 JavaScript 변수에 값을 할당합니다.

Operator | Example | Same As
---|---|---
= | x = y | x = y
+= | x += y | x = x + y
-= | x -= y | x = x - y
*= | x *= y | x = x * y
/= | x /= y | x = x / y
%= | x %= y | x = x % y
<<= | x <<= y | x = x << y
>>= | x >>= y | x = x >> y
>>>= | x >>>= y | x = x >>> y
&= | x &= y | x = x & y
^= | x ^= y | x = x ^ y
|= | x |= y | x = x | y

### Assignment Examples

`=` 는 변수에 값을 할당합니다.
```JavaScript
var x = 10;

out:
x : 10
```

`+=`는 변수에 값을 추가합니다.
```JavaScript
var x = 10;
x += 5;

out:
x : 15
```

`-=`는 변수에 값을 뺍니다.
```JavaScript
var x = 10;
x -= 5;

out:
x : 5
```

`*=`는 변수에 곱합니다.

```JavaScript
var x = 10;
x *= 5;

out:
x : 50
```

`/=`는 변수를 나눕니다.

```JavaScript
var x = 10;
x /= 5;

out:
x : 2
```

`%=`는 변수에 나머지를 대입합니다.

```JavaScript
var x = 10;
x %= 4;

out:
x : 2
```
