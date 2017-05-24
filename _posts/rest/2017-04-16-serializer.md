---
layout: post
section-type: post
title: 다중 serializer
category: rest
tags: [ 'rest' ]
---

계획을 변경하여 content view api에서 content의 comment를 바로 출력하기로 함.

serializer를 통하여 구현하려고 한다.


```python
          from rest_framework import serializers

from content_api.models import Content
from content_api.models.content import PostComment

__all__ = (
    'ContentDetailSerializer',
    'ContentSimpleSerializer',
)


# 전체 콘텐츠 출력시 기본정보만 나오는 시리얼라이저
class ContentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('seq', 'title', 'start_date', 'end_date', 'place', 'realm_name',
                  'area', 'price', 'thumbnail',)


# 상세페이지에서 추가 정보 불러오기 위한 필드(작업중)
class CommentListField(serializers.RelatedField):
    def to_representation(self, value):
        return 'review %s' % (value.username,)


# 상세 페이지 출력시 상세정보까지 나오는 시리얼라이저
class ContentDetailSerializer(serializers.ModelSerializer):
    comment = CommentListField(many=True, read_only=True)

    class Meta:
        model = Content
        fields = '__all__'

# 코멘트 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = '__all__'
```

하지만 model의 relation 때문에 막힌다...
시리얼라이저로 content에서 comment를 출력하려하지만
MyUser의 필드가 없기 때문에 안됨...

comment 모델을 지정하였지만 동작하지 않는다...

[참고문서 REST](https://github.com/KimDoKy/DjangoRestFramework-Tutorial/blob/master/doc/Django%20REST%20Framework%20-%2011.%20Serializer%20relations.md)

> 구현하려던 serializer(두개 이상의 모델을 중첩으로 보여주는 serializer)는 APIView에서는 구현이 가능하지만 ViewSet에서는 동작하지 않는다.
