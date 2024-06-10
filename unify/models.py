from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.PROTECT)
    category = models.ForeignKey(Category, on_delete= models.PROTECT, related_name='posts')
    description = models.TextField()
    slug = models.SlugField()
    datetime_created = models.DateTimeField(auto_now_add= True)
    datetime_modified = models.DateTimeField(auto_now= True)
    
    def __str__(self) -> str:
        return self.title
    


class CommentStatusManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status= Comment.COMMENT_STATUS_APPROVED)
    
class Comment(models.Model):
    COMMENT_STATUS_WAITING = 'w'
    COMMENT_STATUS_APPROVED = 'a'
    COMMENT_STATUS_NOT_APPROVED = 'no'
    COMMENT_STATUS = [
        (COMMENT_STATUS_WAITING, 'Waiting'),
        (COMMENT_STATUS_APPROVED, 'Approved'),
        (COMMENT_STATUS_NOT_APPROVED, 'Not Approved'),
    ]


    post = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comment')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='comment')
    description = models.TextField()
    status = models.CharField(choices=COMMENT_STATUS, default=COMMENT_STATUS_WAITING, max_length=2)
    datetime_created = models.DateTimeField(auto_now_add= True)
    datetime_modified = models.DateTimeField(auto_now= True)

    objects = models.Manager()
    approved = CommentStatusManager()