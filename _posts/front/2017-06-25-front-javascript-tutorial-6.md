---
layout: post
section-type: post
title: JavaScript Tutorial - 6. Comments
category: front
tags: [ 'front' ]
---

## JavaScript Comments

### Single Line Comments
`//` 으로 시작하면 됩니다.

```JavaScript
// Change heading:
document.getElementById("myH").innerHTML = "My First Page";
// Change paragraph:
document.getElementById("myP").innerHTML = "My first paragraph.";
```

```JavaScript
var x = 5;      // Declare x, give it the value of 5
var y = x + 2;  // Declare y, give it the value of x + 2
```

### Multi-line Comments
`/*`와 `*/`의 사이에 주석내용을 기입합니다.

```JavaScript
/*
The code below will change
the heading with id = "myH"
and the paragraph with id = "myP"
in my web page:
*/
document.getElementById("myH").innerHTML = "My First Page";
document.getElementById("myP").innerHTML = "My first paragraph.";
```

### Using Comments to Prevent Execution

```JavaScript
//document.getElementById("myH").innerHTML = "My First Page";
document.getElementById("myP").innerHTML = "My first paragraph.";
```

```JavaScript
/*
document.getElementById("myH").innerHTML = "My First Page";
document.getElementById("myP").innerHTML = "My first paragraph.";
*/
```
