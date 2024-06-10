from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django.db.models import Prefetch


from .serializers import PostSerializer, CommentSerializer, DetailedPostSerializer, CommentDetailSerializer
from .models import Post, Comment


class PostViewSet(ModelViewSet):
    queryset = Post.objects.prefetch_related(
        Prefetch('comment', 
                queryset= Comment.approved.all(),
                to_attr= 'comment_status',
                )
        )
    filter_backends = [SearchFilter]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostSerializer
        return DetailedPostSerializer
    

    def get_serializer_context(self):
        return {'user_pk': self.request.user.id}

    
class CommentViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentSerializer
        
        return CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.filter(status= Comment.COMMENT_STATUS_APPROVED)
        

    def get_serializer_context(self):
        return {'post_pk': self.kwargs['post_pk'], 'user_pk': self.request.user.id}
    
        

    

    