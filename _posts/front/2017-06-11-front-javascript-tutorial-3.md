---
layout: post
section-type: post
title: JavaScript Tutorial - 3. Output
category: front
tags: [ 'front' ]
---

# JS Output

## JavaScript Display Possibilities

JavaScript는 다양한 방식으로 데이터를 "표시" 할 수 있습니다.

- **innerHTML** 을 사용하여 HTML 요소에 작성하기.
- `document.write()`를 사용하여 HTML 출력에 쓰기.
- `window.alert()`를 사용하여 경고 상자에 쓰기.
- `console.log()`를 사용하여 브라우저 콘솔에 기록하기.

## Using innerHTML

HTML에 액세스하기 위해 JavaScript는 `document.getElementById(id)` 메소드를 사용할 수 있습니다.  
**id** 속성은 HTML 요소를 정의합니다. **innerHTML** 속성은 HTML 내용을 정의합니다.


```
<html>
<body>
<h1>My First Web Page</h1>
<p>My First Paragraph</p>

<p id="demo"></p>

<script>
document.getElementById("demo").innerHTML = 5 + 6;
</script>

</body>
</html>
```

> <p id="demo"></p>
> <script>
> document.getElementById("demo").innerHTML = 5 + 6;
> </script>

## Using document.write()

테스트 목적으로는 `document.write()`를 사용하는 것이 편리합니다.

```html
<html>
<body>

<h1>My First Web Page</h1>
<p>My first paragraph.</p>

<script>
document.write(5 + 6);
</script>

</body>
</html>
```

HTML가 로드 완료 된 후 `document.write()`를 사용하면 기존 HTML을 모두 삭제합니다.

```html
<html>
<body>

<h1>My First Web Page</h1>
<p>My first paragraph.</p>

<button onclick="document.write(5 + 6)">Try it</button>

</body>
</html>
```

> 동작은 [w3school](https://www.w3schools.com/js/tryit.asp?filename=tryjs_output_write_over){:target="`_`blank"}에서 확인가능합니다.(여기서 실행하면 포스팅을 볼 수 없습니다...)

> `document.write()` 메소드는 테스트에만 사용해야합니다.

## Using `window.alert()`

경고 상자를 사용하여 데이터를 표시 할 수 있습니다.

```html
<html>
<body>

<h1>My First Web Page</h1>
<p>My first paragraph.</p>

<script>
window.alert(5 + 6);
</script>

</body>
</html>
```
> 동작은 [w3school](https://www.w3schools.com/js/tryit.asp?filename=tryjs_output_alert){:target="`_`blank"}에서 확인가능합니다.


## Using `console.log()`

디버깅을 위해 데이터를 표시 할 수 있습니다.

```html
<html>
<body>

<h2>Activate debugging with F12</h2>

<p>Select "Console" in the debugger menu. Then click Run again.</p>

<script>
console.log(5 + 6);
</script>

</body>
</html>
```
> 동작은 [w3school](https://www.w3schools.com/js/tryit.asp?filename=tryjs_output_console){:target="`_`blank"}에서 확인가능합니다.
