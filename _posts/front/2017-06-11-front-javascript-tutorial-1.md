---
layout: post
section-type: post
title: JavaScript Tutorial - 1
category: front
tags: [ 'front' ]
---

Django로 작업 하던 중, 혼자서 진행하는 부분에서 front-end 작업에서 막히게 되었습니다.

그래서 JavaScript를 공부하기로 했습니다.

[JavaScript Tutorial](https://www.w3schools.com/js/default.asp){:target="_blank"}

---

# JS Introduction

## JavaScript Can Change HTML Content

JavaScript HTML 메소드 중 하나는 `getElementById()`입니다. 아래 예제에서는 메서드를 사용하여 HTML요소 `(id="demo")`를 "검색"하고 요소 내용(innerHTML)을 "Hello JavaScript"로 변경합니다.

```JavaScript
document.getElementById("demo").innerHTML = "Hello JavaScript";  
# 큰 따옴표와 작은 따옴표 모두 사용 가능합니다.
```
> Example :
> <p id="demo">JavaScript can change HTML content.</p>
<button type="button" onclick='document.getElementById("demo").innerHTML = "Hello JavaScript!"'>Click Me!</button>

```html
<p id="demo">JavaScript can change HTML content.</p>

<button type="button" onclick='document.getElementById("demo").innerHTML = "Hello JavaScript!"'>Click Me!</button>
```

## JavaScript Can Change HTML Attributes

이 예제는 `<img>`태그의 `src(source)` 속성을 변경하여 HTML 이미지를 변경합니다.

> Example :
> <button onclick="document.getElementById('myImage').src='{{ site.url }}/img/post/front/javascript/pic_bulbon.gif'">Turn on the light</button>
<button onclick="document.getElementById('myImage').src='{{ site.url }}/img/post/front/javascript/pic_bulboff.gif'">Turn off the light</button>
<img id="myImage" src="{{ site.url }}/img/post/front/javascript/pic_bulboff.gif" style="width:100px">


```
<button onclick="document.getElementById('myImage').src='pic_bulbon.gif'">Turn on the light</button>

<button onclick="document.getElementById('myImage').src='pic_bulboff.gif'">Turn off the light</button>

<img id="myImage" src="pic_bulboff.gif" style="width:100px">
```

## JavaScript Can Change HTML Styles (CSS)

```javascript
document.getElementById("demo").style.fontSize = "25px";
or
document.getElementById('demo').style.fontSize = '25px';
```
> Example :
> <p id="demo1">JavaScript can change the style of an HTML element.</p>
<button type="button" onclick="document.getElementById('demo1').style.fontSize='35px'">Click Me!</button>

```html
<p id="demo">JavaScript can change the style of an HTML element.</p>

<button type="button" onclick="document.getElementById('demo').style.fontSize='35px'">Click Me!</button>
```

## JavaScript Can Hide HTML Elements

```javascript
document.getElementById("demo").style.display = "none";
or
document.getElementById('demo').style.display = 'none';
```

> <p id="demo2">JavaScript can hide HTML elements.</p>
> <button type="button" onclick="document.getElementById('demo2').style.display='none'">Click Me!</button>

```html
<p id="demo">JavaScript can hide HTML elements.</p>

<button type="button" onclick="document.getElementById('demo').style.display='none'">Click Me!</button>
```

## JavaScript Can Show HTML Elements

```javascript
document.getElementById("demo").style.display = "block";
or
document.getElementById('demo').style.display = 'block';
```

> <p id="demo3" style="display:none">Hello JavaScript!</p>
> <button type="button" onclick="document.getElementById('demo3').style.display='block'">Click Me!</button>

```html
<p id="demo" style="display:none">Hello JavaScript!</p>

<button type="button" onclick="document.getElementById('demo').style.display='block'">Click Me!</button>
```
