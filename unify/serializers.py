from rest_framework import serializers
from .models import Post, Comment

class CommentDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    time = serializers.DateTimeField(source= 'datetime_modified', read_only = True)


    class Meta:
        model = Comment
        fields = ['user','description','time',]

    def get_user(self, obj: Comment):
        return obj.user.first_name

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'description','datetime_modified',]
        read_only_fields = ['status','user']

    def create(self, validated_data):
        post_id = self.context['post_pk']
        user_id = self.context['user_pk']
        return Comment.objects.create(post_id = post_id,user_id= user_id, **validated_data)


class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializer(source = 'comment_status' ,many=True, read_only= True)

    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'description', 'datetime_modified','comment', ]
        read_only_fields = ['author']


    def create(self, validated_data):
        user_id = self.context['user_pk']
        return Post.objects.create(author_id = user_id, **validated_data)
    
class DetailedPostSerializer(serializers.ModelSerializer):
    comment = CommentDetailSerializer(source = 'comment_status' ,many=True, read_only= True)
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['title', 'author', 'category', 'description', 'datetime_modified','comment', ]
        read_only_fields = ['author']

    def get_author(self, obj: Post):
        return obj.author.first_name
    
    def get_category(self, obj: Post):
        return obj.category.name
    
