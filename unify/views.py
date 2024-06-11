from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from django.db.models import Prefetch
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .serializers import PostSerializer, CommentSerializer, DetailedPostSerializer, CommentDetailSerializer
from .models import Post, Comment


class PostViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title']


    queryset = Post.objects.select_related('category','author').prefetch_related(
        Prefetch('comment', 
                queryset= Comment.approved.all(),
                to_attr= 'comment_status',
                )
        ).all()
    
    

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostSerializer
        return DetailedPostSerializer
    

    def get_serializer_context(self):
        return {'user_pk': self.request.user.id}

    
class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentSerializer
        
        return CommentDetailSerializer

    def get_queryset(self):
        post_pk = self.kwargs['post_pk']
        return Comment.approved.filter(post_id = post_pk).all()
        

    def get_serializer_context(self):
        return {'post_pk': self.kwargs['post_pk'], 'user_pk': self.request.user.id}
    
        

    

    