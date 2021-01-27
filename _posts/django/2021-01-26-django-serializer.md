---
layout: post
section-type: post
title: django - Model Object의 모든 field 값 가져오기
category: django
tags: [ 'django' ]
---

model object의 필드값을 커스텀하여 api 응답으로 보내주어야 하는 경우들이 있습니다.  
  
구현한 코드를 기록합니다.
  
```python
contents = Contents.objects.first()
fields = [i.name for i in contents._meta.fields]
exclude_fields = [
    'description',
    'etc',...
    ]

for u in fields:
    if i not in exclude_fields:
        result[i] = getattr(contents, i, None)
```

구현하고 보니 DRF의 serializer와 비슷합니다.
  
그래서 DRF의 serializer로 다시 구현합니다.
  
```python
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents
        exclude = ['description', ...]
```
  
serializer의 소스 코드도 비슷합니다.
  
쳇...

### 의미 있는 삽질

DRF의 serializer로 값을 불러오면 FK필드의 경우 int값이 나옵니다.  
  
삽질한 코드로 작업을 하면 좀 더 세밀하게 가공할 수 있습니다.  

## 결론

둘 다 잘 조합해서 문제 해결!
