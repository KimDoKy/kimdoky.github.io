---
layout: post
section-type: post
title: django - QuerySet Method
category: django
tags: [ 'django' ]
---

### `filter()`
QuerySet을 필터링하기

```python
Post.objects.filter(publish__year=2018)
```

### `exclude()`
해당 내용을 쿼리셋에서 제외하기

```python
Post.objects.filter(publish__year=2018).exclude(title__startswith='New')
```

### `order_by()`
정렬 순서 정하기

```python
# 오름차순
>>> Post.objects.order_by('title')
<QuerySet [<Post: Change Title>, <Post: New title>, <Post: One more post>]>
# 내림차순
>>> Post.objects.order_by('-title')
<QuerySet [<Post: One more post>, <Post: New title>, <Post: Change Title>]>
```

### `delete()`
객체를 삭제하기  
객체를 삭제하면 종속 관계도 삭제된다.

```python
>>> post = Post.objects.get(id=2)
>>> post.delete()
(1, {'blog.Post': 1})
# shell에서 해당 커맨드를 입력하면 DB에서는 삭제가 되지만, 객체는 저장된 상태로 남아있다.
>>> post
<Post: New title>
>>> post.title
'New title'
```

Django의 QuerySet은 평가(?)가 이루어지기 전까지는 데이터베이스에 도달하지 않는다.

평가가 이루어지는 경우

- 처음 반복 할 때
- 슬라이스할 때. `Post.objects.all()[:3]`
- pickle이나 cache할 때
- `repr()`이나 `len()`을 호출 할 때
- 명시적으로 `list()`를 호출 할 때
- `bool()`, `or`, `and`, `if`와 같은 명령문에서 테스트 할 때
