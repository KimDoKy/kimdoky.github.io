---
layout: post
section-type: post
title: JavaScript Tutorial - 11. Data Types
category: javascript
tags: [ 'javascript' ]
---

## JS Data Types

###JavaScript Data Types

JavaScript 변수는 숫자, 문자열, 객체 등 많은 데이터 타입을 가지고 있습니다.
```JavaScript
var length = 16;                               // Number
var lastName = "Johnson";                      // String
var x = {firstName:"John", lastName:"Doe"};    // Object
```

### The Concept of Data Types

프로그래밍에서 데이터 타입은 중요한 개념입니다.  
변수를 조작하려면 타입에 대해 알고 있어야 합니다.  
데이터 타입이 없으면 아래와 같은 문제를 해결할 수 없습니다.

```JavaScript
var x = 16 + "Volvo";
```

> 숫자와 문자열을 추가할 때 JavaScript는 숫자를 문자열로 취급합니다.

```JavaScript
var x = 16 + "Volvo";

out:
16Volvo
```

```JavaScript
var x = "Volvo" + 16;

out:
Volvo16
```

JavaScript는 표현식을 왼쪽에서 오른쪽으로 실행합니다. 시퀀스가 다르면 다른 결과가 발생합니다.

```JavaScript
var x = 16 + 4 + "Volvo";

out:
20Volvo
```

```JavaScript
var x = "Volvo" + 16 + 4;

out:
Volvo164
```

### JavaScript Types are Dynamic.

JavaScript에는 동적 타입이 있습니다. 즉, 동일한 변수를 사용하여 다른 데이터 유형을 유지할 수 있습니다.

```JavaScript
var x;               // Now x is undefined
var x = 5;           // Now x is a Number
var x = "John";      // Now x is a String
```

### JavaScript Strings

문자열은 작은 따옴표나 큰 따옴표로 기록할 수 있습니다.

```JavaScript
var carName = "Volvo XC60";   // Using double quotes
var carName = 'Volvo XC60';   // Using single quotes
```

문자열 주위의 따옴표와 일치하지 않는 한 문자열 내에서 따옴표를 사용할 수 있습니다.

```JavaScript
var answer = "It's alright";             // Single quote inside double quotes
var answer = "He is called 'Johnny'";    // Single quotes inside double quotes
var answer = 'He is called "Johnny"';    // Double quotes inside single quotes
```

### JavaScript Numbers

JavaScript에는 한가지 타입의 숫자만 있습니다. 숫자는 십진수나 십진법없이 사용이 가능합니다.

```JavaScript
var x1 = 34.00;     // Written with decimals
var x2 = 34;        // Written without decimals
```

특 대형(exponential) 표기법을 사용하여 매우 크거나 작은 숫자를 작성할 수 있습니다.

```JavaScript
var y = 123e5;      // 12300000
var z = 123e-5;     // 0.00123
```

### JavaScript Booleans

Boolean은 True와 False 값만 가질 수 있습니다.

```JavaScript
var x = true;
var y = false;
```

Boolean은 조건부 테스트에 사용됩니다.

### JavaScript Arrays

JavaScript 배열은 대괄호로 작성됩니다. 배열 항목은 쉽표로 구분됩니다.

```JavaScript
var cars = ["Saab", "Volvo", "BMW"];
```

배열 인덱스는 0부터 시작합니다.

### JavaScript Objects

JavaScript 객체는 중괄호로 작성됩니다. 객체 속성은 이름:값 쌍으로 구분하여 작성합니다.

```JavaScript
var person = {firstName:"John", lastName:"Doe", age:50, eyeColor:"blue"};
```

### The typeof Operator

JavaScript의 `typeof` 연산자를 사용하여 변수의 타입을 찾을 수 있습니다.

```JavaScript
typeof ""                  // Returns "string"
typeof "John"              // Returns "string"
typeof "John Doe"          // Returns "string"
typeof 0                   // Returns "number"
typeof 314                 // Returns "number"
typeof 3.14                // Returns "number"
typeof (3)                 // Returns "number"
typeof (3 + 4)             // Returns "number"
```

### Primitive Data

원시 데이터 값은 추가 속성 및 메서드가 없는 단일 단순 데이터 값입니다.

typeof 연산자를 사용하면 밑의 타입 중 하나를 반환 합니다.

- string
- number
- boolean
- null
- undefined

```JavaScript
typeof "John"              // Returns "string"
typeof 3.14                // Returns "number"
typeof true                // Returns "boolean"
typeof false               // Returns "boolean"
```

### Complex Data

typeof을 사용하면 Complex Data는 두가지 중 하나를 반환합니다.

- function
- object

```JavaScript
typeof [1,2,3,4]             // Returns "object" (not "array", see note below)
typeof {name:'John', age:34} // Returns "object"
typeof function myFunc(){}   // Returns "function"
Try it Yourself »
```

### Undefined

JavaScript에서 값이 없는 변수의 값은 typeof을 사용해도 정의되지 않습니다.

```JavaScript
var person;   // Value is undefined, type is undefined
```

값을 `undefined`으로 설정하면 모든 변수를 비울 수 있습니다.

```JavaScript
person = undefined;        // Value is undefined, type is undefined
```

### Empty Values

빈 값과 undefined은 다릅니다. 빈 문자열 변수에는 빈 값과 타입이 있습니다.

```JavaScript
var car = "";              // The value is "", the typeof is "string"
```

### Null

JavaScript에서 null은 "nothing"입니다. (None과 null은 다릅니다.)  

객체를 null로 설정하여 객체를 비울 수 있습니다.

```JavaScript
var person = null;  // Value is null, but type is still an object
```

### Difference Between Undefined and Null

```JavaScript
typeof undefined           // undefined
typeof null                // object
null === undefined         // false
null == undefined          // true
```
