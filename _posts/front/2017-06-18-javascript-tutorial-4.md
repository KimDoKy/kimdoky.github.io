---
layout: post
section-type: post
title: JavaScript Tutorial - 4. Syntax
category: javascript
tags: [ 'javascript' ]
---

## JS Syntax

### JavaScript Programs

컴퓨터 프로그램은 컴퓨터가 "실행" 할 "명령" 목록입니다. 이러한 "명령"을 **명령문** 이라고 합니다.  
JavaScript는 프로그래밍 언어입니다.  
JavaScript 문은 세미콜론`(;)`으로 구분됩니다.  

```JavaScript
var x, y, z;
x = 5;
y = 6;
z = x + y;
```

><p id="demo"></p>
<script>
var x, y, z;
x = 5;
y = 6;
z = x + y;
document.getElementById("demo").innerHTML = z;
</script>

```JavaScript
<p id="demo"></p>
<script>
var x, y, z;
x = 5;
y = 6;
z = x + y;
document.getElementById("demo").innerHTML = z;
</script>
```
> In HTML, JavaScript programs are executed by the web browser.

### JavaScript Statements

JavaScript는 Values(값), Operators(연산자), Expressions(표현식), Keywords, Comments 으로 구성됩니다.

### JavaScript Values
JavaScript 구문은 **고정 값** 과 **가변 값** 이라는 두 가지 유형의 값을 정의합니다.  
고정 값은 리터럴(literals)이라고합니다. 가변 값을 변수(variables)라고합니다.  

### JavaScript Literals

고정 값에 대한 규칙은 다음과 같습니다.

- **숫자** 는 십진수 여부와 상관없이 사용합니다.

```JavaScript
10.50

1001
```
<p id="demo1"></p>

<script>
document.getElementById("demo1").innerHTML = 10.50;
</script>

```JavaScript
<p id="demo"></p>

<script>
document.getElementById("demo").innerHTML = 10.50;
</script>
```

- **문자열** 은 이중 따옴표(`"`) 또는 작은 따옴표(`'`)로 작성된 텍스트입니다.

```JavaScript
"John Doe"

'John Doe'
```
> <p id="demo2"></p>
<script>
document.getElementById("demo2").innerHTML = 'John Doe';
</script>

```JavaScript
<p id="demo"></p>

<script>
document.getElementById("demo").innerHTML = 'John Doe';
</script>
```

### JavaScript Variables

프로그래밍 언어에서 변수는 데이터 값을 저장하는 데 사용됩니다.  
JavaScript는 `var` 키워드를 사용하여 변수를 선언합니다.  
등호(`=`)는 변수에 값을 할당하는 데 사용됩니다.  

```JavaScript
var x;

x = 6;
```

> <p id="demo3"></p>
<script>
var x;
x = 6;
document.getElementById("demo3").innerHTML = x;
</script>

```JavaScript
<p id="demo"></p>

<script>
var x;
x = 6;
document.getElementById("demo").innerHTML = x;
</script>
```

### JavaScript Operators
JavaScript는 값을 계산하기 위해 산술 연산자(` + - *  / `)를 사용합니다.  

```JavaScript
(5 + 6) * 10
```

><p id="demo4"></p>
<script>
document.getElementById("demo4").innerHTML = (5 + 6) * 10;
</script>

```
<p id="demo"></p>

<script>
document.getElementById("demo").innerHTML = (5 + 6) * 10;
</script>
```

JavaScript는 할당 연산자 (`=`)를 사용하여 변수에 값을 할당합니다.

```JavaScript
var x, y;
x = 5;
y = 6;
```
> <p id="demo5"></p>
<script>
var x, y;
x = 5;
y = 6;
document.getElementById("demo5").innerHTML = x + y;
</script>

```JavaScript
<p id="demo"></p>

<script>
var x, y;
x = 5;
y = 6;
document.getElementById("demo").innerHTML = x + y;
</script>
```

### JavaScript Expressions
표현식은 값으로 계산되는 값, 변수 및 연산자의 조합입니다.  

```JavaScript
5 * 10
```
> <p id="demo6"></p>
<script>
document.getElementById("demo6").innerHTML = 5 * 10;
</script>

```JavaScript
<p id="demo"></p>

<script>
document.getElementById("demo").innerHTML = 5 * 10;
</script>
```
표현식에는 변수 값이 포함될 수도 있습니다.  
```JavaScript
x * 10
```

> <p id="demo9"></p>
<script>
var x;
x = 5;
document.getElementById("demo9").innerHTML = x * 10;
</script>

```JavaScript
<p id="demo"></p>

<script>
var x;
x = 5;
document.getElementById("demo").innerHTML = x * 10;
</script>
```
값은 숫자 및 문자열과 같은 다양한 유형이 될 수 있습니다.

```JavaScript
"John" + " " + "Doe"
```

> <p id="demo7"></p>
<script>
document.getElementById("demo7").innerHTML = "John" + " "  + "Doe";
</script>

```JavaScript
<p id="demo"></p>

<script>
document.getElementById("demo").innerHTML = "John" + " "  + "Doe";
</script>
```

### JavaScript Keywords
JavaScript 키워드는 수행 할 작업을 식별하는 데 사용됩니다.  
`var` 키워드는 브라우저에 변수를 작성하도록 지시합니다.  

```JavaScript
var x, y;
x = 5 + 6;
y = x * 10;
```

> <p id="demo8"></p>
<script>
var x, y;
x = 5 + 6;
y = x * 10;
document.getElementById("demo8").innerHTML = y;
</script>

```JavaScript
<p id="demo"></p>

<script>
var x, y;
x = 5 + 6;
y = x * 10;
document.getElementById("demo").innerHTML = y;
</script>
```

### JavaScript Comments
이중 슬래시(`//`) 또는 `/*` 와 `*/` 사이의 코드는 주석으로 처리됩니다.
```JavaScript
var x = 5;   // I will be executed

// var x = 6;   I will NOT be executed
```

```JavaScript
<p id="demo"></p>

<script>
var x;
x = 5;
// x = 6; I will not be executed
document.getElementById("demo").innerHTML = x;
</script>
```

### JavaScript Identifiers
식별자는 이름입니다.  
자바 스크립트에서 식별자는 변수(및 키워드, 함수 및 레이블)의 이름을 지정하는 데 사용됩니다.  
이름에 대한 규칙은 대부분의 프로그래밍 언어에서 거의 동일합니다.  
JavaScript에서 첫 번째 문자는 문자 또는 밑줄(`_`) 또는 달러 기호(`$`) 이어야합니다.  
후속 문자는 문자, 숫자, 밑줄 또는 달러 기호 일 수 있습니다.  
숫자는 첫 번째 문자로 사용할 수 없습니다.  

### JavaScript is Case Sensitive
모든 JavaScript 식별자는 대/소문자를 구분합니다.  
변수 `lastName`과 `lastname`은 두 개의 다른 변수입니다.

```JavaScript
var lastname, lastName;
lastName = "Doe";
lastname = "Peterson";
```
>
JavaScript는 `VAR` 또는 `Var`을 키워드 `var`로 해석하지 않습니다.

### JavaScript and Camel Case

역사적으로 프로그래머는 여러 단어를 하나의 변수 이름으로 결합하는 다양한 방법을 사용했습니다.  

#### Hyphens(`-`)
first-name, last-name, master-card, inter-city.  
JavaScript에서는 하이픈(`-`)을 사용할 수 없습니다. 뺄셈을 위해 예약되어 있기 때문입니다.

#### Underscore(`_`)
first_name, last_name, master_card, inter_city.

#### Upper Camel Case (Pascal Case)
FirstName, LastName, MasterCard, InterCity.
![]({{ site.url }}/img/post/front/javascript/pic_camelcase.jpg)

#### Lower Camel Case
javascript 프로그래머는 소문자로 시작하는 Pascal Case를 사용하는 경향이 있습니다.  
firstName, lastName, masterCard, interCity.

### JavaScript Character Set
JavaScript는 **Unicode** 문자 집합을 사용합니다.  
Unicode는 세계의 모든 문자, 구두점 및 기호를 (거의)포함합니다.
