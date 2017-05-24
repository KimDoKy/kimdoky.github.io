---
layout: post
section-type: post
title: permission
category: rest
tags: [ 'rest' ]
---

게시물에 대해 댓글 기능 구현중..

댓글은 작성자만 편집할 수 있고 보기는 누구나 가능해야 한다.

게시물을 출력시 댓글도 같이 불러와야한다..

일단 권한은 아래처럼 permissions.py 으로 custom permission 을 적용해 주면 된다.

권한을 이용해 게시물에도 똑같이 적용할 수 있다. (지금 구현하는건 공공데이터를 통해 자동저장하므로 작성자가 없어서 관리자 외에는 수정권한이 없게 하였다.)

```
# permissions.py

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
```

```
#views..py

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    # IsAuthenticatedOrReadOnly : 익명의 사
    pagination_class = CommentPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
```

```
# serializers.py

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = PostComment
        fields = '__all__'

```

```
#models.py

from django.db import models

class PostComment(models.Model):
    body = models.TextField()
    score = models.CharField(max_length=1, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Content, on_delete=models.CASCADE)
    author = models.ForeignKey(MyUser, related_name='post_author')

    class Meta:
        ordering = ('created_date',)
```
