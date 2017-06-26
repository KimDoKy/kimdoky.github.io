---
layout: post
section-type: post
title: JavaScript Tutorial - 8. Operators
category: front
tags: [ 'front' ]
---

## JS Operators

```JavaScript
var x = 5;         // assign the value 5 to x
var y = 2;         // assign the value 2 to y
var z = x + y;     // assign the value 7 to z (x + y)
```

#### Assignment

대입 연산자 (`=`)는 변수에 값을 할당합니다.

```JavaScript
var x = 10;
```

#### Adding

더하기 연산자 (`+`)는 숫자를 더합니다.

```JavaScript
var x = 5;
var y = 2;
var z = x + y;
```

#### Multiplying

곱하기 연산자 (`*`)는 숫자를 곱합니다.

```JavaScript
var x = 5;
var y = 2;
var z = x * y;
```

### JavaScript Arithmetic Operators

Operator | Description
---|---
+ | Addition
- | Subtraction
* | Multiplication
/ | Division
% | Modulus
++ | Increment
-- | Decrement

### JavaScript Assignment Operators

Operator | Example | Same As
---|---|---
= | x = y | x = y
+= | x += y | x = x + y
-= | x -= y | x = x - y
*= | x *= y | x = x * y
/= | x /= y | x = x / y
%= | x %= y | x = x % y

```JavaScript
var x = 10;
x += 5;
```

### JavaScript String Operators

`+` 연산자를 사용하여 문자열을 연결 할 수 있습니다.  

```JavaScript
txt1 = "John";
txt2 = "Doe";
txt3 = txt1 + " " + txt2;

result txt3
John Doe
```
`+=` 대입 연산자를 사용하여 문자열을 추가 할 수도 있습니다.

```JavaScript
txt1 = "What a very ";
txt1 += "nice day";

result
What a very nice day
```

> 문자열에 사용되면 `+` 연산자를 **연결 연산자** 라고합니다.

### Adding Strings and Numbers

두 개의 숫자를 추가하면 합계가 반환되지만 숫자와 문자열을 추가하면 문자열이 반환됩니다.

```JavaScript
x = 5 + 5;
y = "5" + 5;
z = "Hello" + 5;

The result of x, y, and z will be:

10
55
Hello5
```

### JavaScript Comparison Operators

Operator | Description
---|---
== | equal to
=== | equal value and equal type
!= | not equal
!== | not equal value or not equal type
> | greater than
< | less than
>= | greater than or equal to
<= | less than or equal to
? | ternary operator

### JavaScript Logical Operators

Operator | Description
---|---
&& | logical and
|| | logical or
! | logical not

### JavaScript Type Operators

Operator | Description
---|---
typeof | 변수의 유형을 반환합니다.
instanceof | 객체가 객체 유형의 인스턴스인 경우 `true`를 반환합니다.

### JavaScript Bitwise Operators

비트 연산자는 32 비트 숫자에서 작동합니다.  
연산의 숫자 피연산자는 32 비트 숫자로 변환됩니다. 결과는 JavaScript 번호로 다시 변환됩니다.

Operator | Description | Example | Same as | Result | Decimal
---|---|---|---|---|---
& | AND | 5 & 1 | 0101 & 0001 | 0001 | 1
`|`	| OR | 5 `|` 1 | 0101 `|` 0001 | 0101 `|` 5
~ | NOT | ~ 5 | ~0101 | 1010 | 10
^ | XOR | 5 ^ 1 | 0101 ^ 0001 | 0100 | 4
<< | Zero fill left shift | 5 << 1 | 0101 << 1 | 1010 | 10
>> | Signed right shift | 5 >> 1 | 0101 >> 1 | 0010 | 2
>>> | Zero fill right shift | 5 >>> 1 | 0101 >>> 1 | 0010 | 2
