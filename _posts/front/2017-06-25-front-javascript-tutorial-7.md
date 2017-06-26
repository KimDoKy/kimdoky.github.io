---
layout: post
section-type: post
title: JavaScript Tutorial - 7. Variables
category: front
tags: [ 'front' ]
---

## JS Variables

### JavaScript Variables

```JavaScript
var x = 5;
var y = 6;
var z = x + y;
```


### Much Like Algebra

```JavaScript
var price1 = 5;
var price2 = 6;
var total = price1 + price2;
```

### JavaScript Identifiers
JavaScript에서 Variables는 고유한 이름을 갖아야 합니다.  
이런 고유한 이름을 **식별자(identifiers)** 라고 합니다.  
식별자는 짧은 이름(x, y...)보다는 기능적인 이름(age, sum, totalVolume)으로 만듭니다.  

변수 이름을 작명하는 일반적인 규칙들입니다.  

- 이름에는 문자, 숫자, 밑줄, 달러 기호가 포함될 수 있습니다.
- 이름은 문자로 시작해야 합니다.
- 이름은 `$` 및 `_`로 시작할 수도 있습니다.
- 이름은 대소문자를 구분합니다.
- 예약어는 사용할 수 없습니다.

### The Assignment Operator
JavaScript에서 등호(`=`)는 "대입 연산자"이며 "같음"연산자가 아닙니다.  
"같음"연산자는 `==`입니다.

### JavaScript Data Types
프로그래밍에서 텍스트 값은 **텍스트 문자열** 이라고합니다.  
문자열은 큰 따옴표 나 작은 따옴표로 작성됩니다. 숫자는 따옴표 없이 쓰여집니다.  

```JavaScript
var pi = 3.14;
var person = "John Doe";
var answer = 'Yes I am!';
```

### Declaring (Creating) JavaScript Variables
**var** 키워드를 사용하여 JavaScript 변수를 선언합니다.

```JavaScript
var carName;
```

등호(`=`)를 사용하여 변수에 값을 할당 합니다.

```JavaScript
carName = "Volvo";
```

변수를 선언 할 때 변수에 값을 할당 할 수도 있습니다.

```JavaScript
var carName = "Volvo";
```
#### Example
```html
<p id="demo"></p>

<script>
var carName = "Volvo";
document.getElementById("demo").innerHTML = carName;
</script>
```

> ** 스크립트의 시작 부분에 모든 변수를 선언하는 것이 좋은 프로그래밍 습관입니다.**

### One Statement, Many Variables
var를 사용하여 명령문을 시작하고 변수를 쉼표로 구분함으로 한 문장에서 많은 변수를 선언 할 수 있습니다.  
```JavaScript
var person = "John Doe", carName = "Volvo", price = 200;
```
선언은 여러 줄로도 할 수 있습니다.

```JavaScript
var person = "John Doe",
carName = "Volvo",
price = 200;
```

### Value = undefined

컴퓨터 프로그램에서 변수는 종종 값없이 선언됩니다.  
이 값은 사용자 입력과 같이 나중에 제공 될 수 있습니다.  

```JavaScript
var carName;
```

### Re-Declaring JavaScript Variables
JavaScript의 Variables는 재선언하여도 이전의 값이 손실되지 않습니다.

```JavaScript
var carName = "Volvo";
var carName;
```
carName 변수는 다음 명령문 실행 후에도 여전히 "Volvo"값을 갖습니다.

### JavaScript Arithmetic

```JavaScript
var x = 5 + 2 + 3;
```
문자열을 연결할 때도 사용할 수 있습니다.

```JavaScript
var x = "John" + " " + "Doe";
```

숫자를 따옴표로 묶으면 나머지 숫자도 문자열로 처리되고 연결됩니다.
```JavaScript
var x = "5" + 2 + 3;

// result : 523
```

```JavaScript
var x = 2 + 3 + "5";

// result : 55
```
