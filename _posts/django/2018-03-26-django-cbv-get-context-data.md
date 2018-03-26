---
layout: post
section-type: post
title: Django CBV에서 특정 데이터 가져오기, 기능 추가하기(get_context_data)
category: django
tags: [ 'django' ]
---

FBV로 렌딩시 특정 기능을 추가 및 적용하는 것은 간단하지만, CBV에서 적용하기는 조금 까다롭습니다.

DB에서 특정 데이터를 불러오기 위해 필요한 `pk`등을 개발자가 직접 선언하지 않기 때문에, 원하는 데이터를 불러오기가 단순하지 않습니다.

물론 답은 [django document](https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-display/)에 나와 있긴하지만, 답을 봐도 잘 이해가 어렵습니다.

현재 이 작업은 [GPS를 추출하는 작업을 FBV에서는 간단히 구현](https://kimdoky.github.io/front/2018/03/22/front-google-map.html)해본 상태이고, CBV에서 구현하기 위한 것이 목적입니다.

### DetailView에서 PK 값 얻기
DetailView는 개발자가 따로 pk를 지정하지 않아도 url에서 pk를 받아와서 detail view를 구현해 주는 고마운 CBV입니다.  
하지만 직접 pk를 지적하지 않기 때문에 pk값을 얻어서 사용하려면 `get_context_data` 함수를 추가해주어야 합니다.

```python
class PhotoDetailView(DetailView):
    model = Album

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.kwargs['pk']를 통해서 url에서 pk값을 받을 수 있습니다.
        # url은 `path('<pk>/', PhotoView.as_view())으로 구현되어있어서 해당 pk 부분을 받아옵니다.`
        context['photo_list'] = Photo.objects.filter(album_id=self.kwargs['pk'])
        return context

PhotoView = PhotoDetailView.as_view()
```

### 특정 함수 실행하기
PK값을 얻었으니 FBV와 동일하게 구현하면 됩니다. (클래스 안에서 함수를 선언하는 것뿐이니...)

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['photo_list'] = Photo.objects.filter(album_id=self.kwargs['pk'])
    # google map에 표기하기 위해 google api키를 불러옵니다.
    context['api'] = settings.GOOGLE_API
    # 원하는 데이터들을 pk를 이용하여 추출하고, 데이터들을 순회하면서 원하는 데이터를 구현해둔 함수를 통해 데이터를 채워넣습니다.
    for instance in context['photo_list']:
        # get_gps는 이전에 구현해둔 사진 파일에서 gps 정보를 추출하는 함수입니다.
        # https://kimdoky.github.io/front/2018/03/22/front-google-map.html
        instance.lat, instance.lng = get_gps(instance.photo.path)
        instance.save()
    return context
```

DB를 보거나, 서버 화면, 템플릿, 어드민 페이지를 통해서 원하는 기능들이 적용 된 것을 확인 할 수 있습니다.
