---
layout: post
section-type: post
title: django - Paginator
category: django
tags: [ 'django' ]
---

콘텐츠가 많아지면 콘텐츠들을 페이지로 분할해야 한다.  

Django에는 페이지를 쉽게 관리할 수 있는 pagenation 클래스가 내장되어 있다.

```python
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:  # 페이지가 정수가 아닌 경우
        posts = paginator.page(1)
    except EmptyPage:  # 페이지가 범위를 벗어나는 경우
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page':page, 'posts':posts})
```

pagination의 작동흐름이다.

1. `Paginator` 클래스를 각 페이지에 표시 할 객체 수로 인스턴스화 한다.
2. 현재 페이지 번호를 나타내는 GET 매개 변수 페이지를 얻는다.
3. `Paginator`의 `page()` 메소드를 호출하는 페이지에 대한 객체를 얻는다.
4. 페이지 매개 변수가 정수가 아니면 결과의 첫 페이지를 검색한다. 매개 변수가 마지막 페이지보다 큰 숫자라면 마지막 페이지를 검색한다.
5. 페이지 번호와 검색된 객체를 템플릿에 전달한다.

Pagenation을 표시할 템플릿을 생성한다.

{% raw %}
```html
<div class="pagination">
  <span class="step-links">
  {% if page.has_previous %}
    <a href="?page={{ page.previous_page_number }}">Previous</a>
  {% endif %}
  <span class="current">
    Page {{ page.number }} of {{ page.paginator.num_pages }}.
  </span>
  {% if page.has_next %}
    <a href="?page={{ page.next_page_number }}">Next</a>
  {% endif %}
  </span>
</div>
```

list를 표시하는 템플릿(html)에 적용한다.

```html
...
{% include "pagination.html" with page=posts %}
```


Django에는 위 기능들을 CBV를 통해 더 쉽게 제공한다.

```python
from django.views.generic import ListView

class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
```

Django의 `ListView`는 `page_obj`라는 변수에 선택된 페이지를 전달하기 때문에 템플릿도 같이 수정해야 한다.

```html
{% include "pagination.html" with page=page_obj %}
```

{% endraw %}
