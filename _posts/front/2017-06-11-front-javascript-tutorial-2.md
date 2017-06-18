---
layout: post
section-type: post
title: JavaScript Tutorial - 2. Where To
category: front
tags: [ 'front' ]
---

# JS Where To

## The `<script>` Tag
HTML에서는 `<script>`와 `</script>` 태그 사이에 JavaScript 코드를 삽입해야합니다.  

```JavaScript
<script>
document.getElementById("demo").innerHTML = "My First JavaScript";
</script>
```

> <p id="demo"></p> <script> document.getElementById("demo").innerHTML = "My First JavaScript"; </script>

```html
<p id="demo"></p>
<script>
document.getElementById("demo").innerHTML = "My First JavaScript";
</script>
```

## JavaScript Functions and Events

JavaScript 함수는 JavaScript 코드 블록으로, "호출"될 때 실행됩니다.  
예를 들어, 사용자가 버튼을 클릭 할 때와 같이 이벤트가 발생할 때 함수를 호출합니다.  

## JavaScript in <head> or <body>

HTML 파일안에 원하는 만큼의 스크립트를 배치 할 수 있습니다.  
스크립트는 HTML 파일안의 `<body>`나 `<head>` 섹션에 배치할 수 있습니다.(둘중 하나 또는 둘 다 가능)  

## JavaScript in <head>

이 예에선 JavaScript 함수가 `<head>` 섹션에 배치합니다.
이 함수는 버튼을 클릭할 때 호출됩니다.

```HTML
<html>
<head>
<script>
function myFunction() {
    document.getElementById("demo").innerHTML = "Paragraph changed.";
}
</script>
</head>

<body>

<h1>A Web Page</h1>
<p id="demo">A Paragraph</p>
<button type="button" onclick="myFunction()">Try it</button>

</body>
</html>
```

이 예제의 동작은 [w3school](https://www.w3schools.com/js/tryit.asp?filename=tryjs_whereto_head){:target="`_`blank"} 페이지에서 확인가능합니다.(포스팅 내에서 head를 건들수가 없네요..)

## JavaScript in <body>

이 예에선 JavaScript 함수가 `<body>` 섹션에 배치합니다.
이 함수는 버튼을 클릭할 때 호출됩니다.

```html
<html>
<body>

<h1>A Web Page</h1>
<p id="demo">A Paragraph</p>
<button type="button" onclick="myFunction()">Try it</button>

<script>
function myFunction() {
   document.getElementById("demo").innerHTML = "Paragraph changed.";
}
</script>

</body>
</html>
```

> <p id="demo1">A Paragraph</p>
> <button type="button" onclick="myFunction()">Try it</button>
>
> <script>
> function myFunction() {
>   document.getElementById("demo1").innerHTML = "Paragraph changed.";
> }
> </script>

> `<body>` 요소의 맨 아래에 스크립트를 배치하면 스크립트 컴파일이 화면 속도를 늦추기 때문에 웹페이지 로딩 속도가 향상됩니다.

## External JavaScript

스크립트를 외부 파일에 배치 할 수도 있습니다.  
외부 스크립트는 여러 html 파일에 동일한 반복적으로 사용되는 경우에 실용적입니다.  
JavaScript 파일의 확장자는 `.js`입니다.  
외부 스크립트를 사용하려면 스크립트 파일을 `<script>`태그의 `src`속성에 선언해주어야 합니다.

```JavaScript
External file: myScript.js
function myFunction() {
   document.getElementById("demo").innerHTML = "Paragraph changed.";
}
```

```html
Example
<!DOCTYPE html>
<html>
<body>

<script src="myScript.js"></script>

</body>
</html>
```

> 외부 스크립트는 `<script>` 태그를 포함 할 수 없습니다.

## External JavaScript Advantages

스크립트는 분리해두는 것은 몇 가지 이점이 있습니다.  

- HTML과 코드를 분리합니다.
- HTML과 JavaScript를 더 쉽게 읽고 유지할 수 있습니다.
- 캐시 된 JavaScript 파일로 인해 페이지로드 속도가 향상됩니다.

한 페이지에 여러 스크립트 파일을 추가 할 수 있습니다.

```html
<script src="myScript1.js"></script>
<script src="myScript2.js"></script>
```

## External References

외부 스크립트는 전체 URL 또는 웹페이지와 관련된 경로를 참조 할 수 있습니다.  

```html
<script src="https://www.w3schools.com/js/myScript1.js"></script>
```

한 인스턴스에 있는 경우 절대 경로를 이용하여 참조할 수 있습니다.

```html
<script src="/js/myScript1.js"></script>
```

같은 디렉터리에 있으면 아래와 같이 선언하면 됩니다.

```html
<script src="myScript1.js"></script>
```
