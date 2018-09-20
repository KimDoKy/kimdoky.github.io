---
layout: post
section-type: post
title: JavaScript Tutorial - 5. Statements
category: javascript
tags: [ 'javascript' ]
---

## JavaScript Statements
이 명령문은 브라우저에 "Hello Dolly"라고 쓰도록 명령합니다.  
```JavaScript
document.getElementById("demo").innerHTML = "Hello Dolly.";
```
><p id="demo"></p>
<script>
document.getElementById("demo").innerHTML = "Hello Dolly.";
</script>

```JavaScript
<p id="demo"></p>

<script>
document.getElementById("demo").innerHTML = "Hello Dolly.";
</script>
```

### JavaScript Programs
명령문은 작성된 순서대로 하나씩 실행됩니다.  

```JavaScript
var x, y, z;
x = 5;
y = 6;
z = x + y;
document.getElementById("demo").innerHTML = z;
```

> <p id="demo1"></p>
<script>
var x, y, z;
x = 5;
y = 6;
z = x + y;
document.getElementById("demo1").innerHTML = z;
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

### Semicolons `;`
JavaScript 문은 세미콜론으로 구분됩니다.  
각 실행 문 끝에 세미콜론을 추가하세요.  
```JavaScript
var a, b, c;
a = 5;
b = 6;
c = a + b;
```
세미콜론으로 구분하면 한 줄에 여러 문장을 사용할 수 있습니다.
```JavaScript
a = 5; b = 6; c = a + b;
```

> 세미콜론으로 끝나는 문장은 필수는 아니지만 적극 권장됩니다.

### JavaScript White Space
JavaScript는 여러 공백을 무시합니다.  
스크립트를 쉽게 읽을 수 있도록 공백을 사용 할 수 있습니다.  
```JavaScript
var person = "Hege";
var person="Hege";
# 위 두 줄은 같습니다.
```
연산자(`= + - * /`) 앞뒤에 공백을 넣는 것도 좋은 방법입니다.  
```JavaScript
var x = y + z;
```

### JavaScript Line Length and Line Breaks
가독성을 극대화하기 위해 프로그래머는 종종 80자보다 긴 코드 라인을 피하려고 합니다.  
JavaScript 문이 한 줄에 들어 가지 않을때 가장 좋은 방법은 연산자 뒤에 이어쓰는 것입니다.
```JavaScript
document.getElementById("demo").innerHTML =
"Hello Dolly!";
```

### JavaScript Code Blocks
JavaScript 문은 중괄호(`{...}`) 안에 코드 블록으로 그룹화 할 수 있습니다.  
코드 블록의 목적은 함께 실행될 명령문을 정의하는 것입니다.  
블록으로 그룹화하는 경우는 대부분 JavaScript 함수에서 사용합니다.
```JavaScript
function myFunction() {
    document.getElementById("demo1").innerHTML = "Hello Dolly!";
    document.getElementById("demo2").innerHTML = "How are you?";
}
```

### JavaScript Keywords
JavaScript 문은 실행 할 JavaScript 동작을 식별하기 위한 **키워드** 로 시작하는 경우가 많습니다.  


Keyword	| Description
---|---
break	| 스위치 또는 루프를 종료합니다
continue	| 루프 밖으로 튀어 나와 맨 위에서 시작합니다
debugger	| JavaScript의 실행을 중지하고 디버깅 기능을 호출합니다 (사용 가능한 경우)
do ... while	| 조건문이 true 인 동안 명령문 블록을 실행하고 블록을 반복합니다
for	| 조건이 true 인 한 실행될 명령문 블록을 표시합니다
function	| 함수를 선언합니다
if ... else	| 조건에 따라 실행될 명령문 블록을 표시합니다
return	| 함수를 빠져 나갑니다
switch	| 경우에 따라 실행될 문 블록을 표시합니다
try ... catch	| 명령문 블록에 오류 처리를 구현합니다
var	| 변수를 선언합니다

> JavaScript 키워드는 예약어입니다. 예약어는 변수의 이름으로 사용할 수 없습니다.
