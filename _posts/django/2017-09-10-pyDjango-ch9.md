---
layout: post
section-type: post
title: pyDjango - chap9. Blog 앱 확장 -  검색 기능
category: django
tags: [ 'django' ]
published: false
---
블로그의 검색 기능을 개발합니다. 검색 기능도 블로그 앱에서 자주 쓰는 기능이므로 오픈 소스로 제공하는 패키지도 많은데, 종류도 다양하고 기능도 풍부한 편입니다. 구글 검색 기능을 제공해주는 패키지도 있고, AJAX 기능으로 검색을 해주는 패키지도 있습니다.  

## 9.1 애플리케이션 설계하기
검색 기능은 블로그 앱 내에서 검색 기능을 구현하는 것으로, 이 정도의 기능은 장고 자체의 Q-객체를 이용하면 쉽게 구현할 수 있습니다. 장고의 Q-객체는 테이블에 대한 복잡한 쿼리를 처리하기 위한 객체입니다.  

검색 기능을 위해서, 검색 단어를 입력받는 폼 기능 및 Q-객체를 사용해 검색 단어가 들어 있는 블로그를 찾고 그 결과를 보여주는 기능 개발이 필요합니다.

### 9.1.1 화면 UI 설계
상단의 [Search] 메뉴를 클릭하면 검색 폼을 보여줍니다. 검색할 단어를 입력하고 [Submit] 버튼을 누르면 검색 결과가 나옵니다. 그리고 검색 폼과 검색 결과를 같은 페이지에 보여주도록 설계했습니다.

### 9.1.2 테이블 설계
pass
### 9.1.3 URL 설계
기존 URL에 검색 폼 처리를 위한 URL 하나를 추가합니다.

URL 패턴 | 뷰 이름 | 템플릿 파일명
---|---|---
/blog/search/ | SearchFormView(FormView) | post_search.html

### 9.1.4 작업/코딩 순서
검색 폼을 출력하기 위해, forms.py 파일에 대한 코딩이 추가됩니다.

작업 순서 | 관련 명령/파일 | 필요한 작업 내용
---|---|---
URLconf | urls.py | URL 정의 추가
뷰 코딩하기 | views.py | 뷰 로직 추가
템플릿 코딩하기 | templates 디렉터리 | 템플릿 파일 수정 및 추가
그 외 작업하기 | forms.py | 검색 폼 클래스 정의

## 9.2 개발 코딩하기

뷰애서 검색 폼을 사용하므로, 검색 폼에 대한 코딩은 뷰 코딩 전에 작업합니다.

### 9.2.1 뼈대 만들기
pass
### 9.2.2 모델 코딩하기
pass
### 9.2.3 URLconf 코딩하기

- blog/urls.py

```python
# ex: /search/
url(r'^search/$', SearchFormView.as_view(), name='search'), # 1
```

- 1 : URL /search/ 요청을 처리할 뷰 클래스를 지정합니다. URL 패턴의 이름은 이름공간을 포함해 'blog:search'가 됩니다. SearchFormView 클래스형 뷰는 폼을 보여주고 폼에 들어 있는 데이터를 처리하기 위한 뷰이므로, FormView를 상속받아 정의합니다.

### 9.2.4 뷰 코딩하기

검색 기능을 제공하기 위해 검색 폼을  보여줘야 하고, 검색 폼의 데이터가 제출되어야 뷰가 처리하는 순서이므로, 뷰를 코딩하기 전에 폼을 먼저 만듭니다.

#### forms.py
장고에서는 폼도 클래스로 정의할 수 있습니다.

- blog/forms.py

```python
from django import forms # 1

class PostSearchForm(forms.Form): # 2
    search_word = forms.CharField(label='Search Word') # 3
```

- 1 : 폼을 클래스로 표현할 수 있도록 하는 기능을 django.forms 모듈에서 제공합니다.
- 2 : 폼을 정의하기 위해서는 django.forms 모듈의 Form 클래스를 상속받아 클래스를 정의합니다.
- 3 : 폼을 정의하는 방법은 테이블의 모델 클래스를 정의하는 방법과 비슷합니다. CharField 필드는 TextInput 위젯으로 표현되며, label 인자인 Search Word는 폼 앞에 출력되는 레이블이 되고, 변수 serach_word는 필드에 대한 id로 각 필드를 구분하는데 사용됩니다.

#### views.py

- blog/views.py

```python
from django.views.generic.edit import FormView # 1
from blog.forms import PostSearchForm
from django.db.models import Q # 2
from django.shortcuts import render # 3

#-- FormView
class SearchFormView(FormView): # 4
    form_class = PostSearchForm # 5
    template_name = 'blog/post_search.html' # 6

    def form_valid(self, form):
        schWord = '%s' % self.request.POST['search_word'] #7
        post_list = Post.objects.filter(Q(title__icontains=schWord) | Q(description__icontains=schWord) | Q(content__icontains=schWord)).distinct() # 8
        context = {} # 9
        context['form'] = form # 10
        context['search_term'] = schWord
        context['object_list'] = post_list

        return render(self.request, self.template_name, context) # 11
```

- 1 : FormView 클래스형 제네릭 뷰를 임포트합니다.
- 2 : 검색 기능에 필요한 Q 클래스를 임포트합니다.
- 3 : 단축 함수 render() 를 임포트합니다.
- 4 : FromView 제네릭 뷰를 상속받아 SearchFormView 클래스형 뷰를 정의합니다. FormView 제네릭 뷰는 GET 요청인 경우 폼을 화면에 보여주고 사용자의 입력을 기다립니다. 사용자가 폼에 데이터를 입력한 후 제출하면 이는 POST 요청으로 접수되어, FormView 클래스는 데이터에 대한 유효성 검사를 합니다. 데이터가 유효하면 form_valid() 함수를 실행한 후 적절한 URL로 리다이렉트시키는 기능을 가지고 있습니다.
- 5 : 폼으로 사용될 클래스를 PostSearchForm으로 지정합니다.
- 6 : 템플릿 파일을 지정합니다.
- 7 : POST 요청의 search_word 파라미터 값을 추출해, schWord 변수에 지정합니다. search_word 파라미터는 PostSearchForm 클래스에서 정의한 필드 id입니다.
- 8 : Q 객체는 filter() 메소드의 매칭 조건을 다양하게 줄 수 있도록 합니다. 여기서는 3개의 조건을 OR 문장으로 연결하고 있습니다. 각 조건의 icontains 연산자는 대소문자를 구분하지 않고 단어가 포함되어 있는지를 검색합니다. distinct() 메소드는 중복된 객체는 제외합니다. 즉 이 줄의 의미는 Post 테이블의 모든 레코드에 대해서 title, description, content 컬럼에 schWord가 포함된 레코드를 대소문자 구별없이 검색해, 서로 다른 레코드들만 리스트로 만들어서 post_list 변수에 지정합니다.
- 9 : 템플릿에 넘겨줄 컨텍스트 변수 context 를 사전 형식으로 정의합니다.
- 10 : form 객체, 즉 PostSearchForm 객체를 컨텍스트 변수 form에 지정합니다.
- 11 : 단축 함수 render()는 템플릿 파일과 컨텍스트 변수를 처리해, 최종적으로 HttpResponse 객체를 반환합니다. form_valid() 함수는 보통 리다이렉트 처리를 위해 HttpResponseRedirect 객체를 반환하는데, 이 render() 함수에 의해 리다이렉트 처리가 되지 않습니다.

### 9.2.5 템플릿 코딩하기
상단의 [Search] 메뉴에 링크를 달아주고 검색 폼과 검색 결과를 보여줄 수 있도록 템플릿 파일을 코딩합니다.

#### base.html 수정

- templates/base.html
{% raw %}
```html
</li>
<li><a href="{% url 'blog:post_archive' %}">Archive</a></li>
<li><a href="{% url 'blog:search' %}">Search</a></li> # 추가
<li><a href="{% url 'admin:index' %}">Admin</a></li>
</div>
{% block content %}{% endblock %}
```

#### post_search.html
검색 폼과 검색 결과를 한 화면에 보여줄 수 있도록 템플릿 파일을 코딩합니다.

- blog/templates/blog/post_search.html

```html
{% extends "base.html" %}

{% block title %}post_search.html{% endblock %}

{% block content %}
<div id="content">
    <h1>Blog Search</h1>
    <form action="." method="post"> {% csrf_token %}
    {{ form.as_table }} # 1
        <input type="submit" value="Submit">
    </form>

    <br><br>
    {% if object_list %} # 2
    {% for post in object_list %} # 3
    <h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2> # 4
    {{ post.modify_date|date:"N d, Y" }}
    <p>{{ post.description }}</p>
    {% endfor %}

{% elif search_term %} # 5
<b><i>Serach Word({{ search_term }}) Not Found !</i></b> # 6
{% endif %}
</div>
{% endblock %}
```
{% endraw %}
- 1 : form을 테이블 형식으로 표시합니다. 여기서 form 은 뷰에서 넘겨준 PostSearchForm 객체입니다.
- 2 : object_list에 내용이 있는지를 확인합니다. 즉 검색 결과가 1개 이상 있는지를 확인합니다.
- 3 : 검색 결과가 있다면, 검색 결과를 순회하면서 Post 객체의 title, modify_date, description 속성을 출력합니다.
- 4 : URL 링크는 객체의 get_absolute_url() 메소드를 호출해 구하는데, /blog/post/slug단어/ 와 같은 형식이 될 것입니다.
- 5 : 검색 결과가 없으면, search_term에 값이 있는지를 확인합니다. 이는 사용자가 검색 단어를 입력했는지 여부를 판단하기 위한 것으로, [Search] 메뉴를 클릭한 후 처음으로 검색 폼을 보여주는 경우를 제외하기 위함입니다. 즉 사용자가 검색 단어를 입력하고 검색 결과가 없는 경우에, 다음 줄에 Not Found 문장을 표시합니다.

## 9.2 지금까지의 작업 확인하기
상단 메인 메뉴의 [Search] 버튼을 클릭하면 검색 폼이 나타납니다. 검색 폼에 단어를 입력하고 [Submit] 버튼을 클릭하면 검색 결과가 같은 화면에 나타나야 합니다.

검색 결과가 있다면.
![]({{site.url}}/img/post/python/django/book_9_1.png)

검색 결과가 없다면
![]({{site.url}}/img/post/python/django/book_9_2.png)
