---
layout: post
section-type: post
title: JavaScript Tutorial - 9. Arithmetic
category: front
tags: [ 'front' ]
---

## JS Arithmetic

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

### Arithmetic Operations

두 숫자는 리터럴일 수 있습니다.

```JavaScript
var x = 100 + 50;
```
혹은 변수이거나

```JavaScript
var x = a + b;
```
혹은 표현일 수 있습니다.

```JavaScript
var x = (100 + 50) * a;
```

### Operators and Operands

숫자(산술 연산에서)는 **피연산자** 라고합니다.  

Operand | Operator | Operand
---|---|---
100 | + | 50

### Operator Precedence

연산자 우선 순위는 연산이 산술 식에서 수행되는 순서와 같습니다.  

```JavaScript
var x = 100 + 50 * 3;

result
250
```

```JavaScript
var x = (100 + 50) * 3;

result
450
```

```JavaScript
var x = 100 + 50 - 3;

result
147
```
