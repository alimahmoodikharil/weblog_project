from django.contrib import admin
from .models import Post, Category, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'author', 'category', 'datetime_modified',]
    prepopulated_fields = {
        'slug': ['title', ]
    }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name',]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id','post', 'status']
    list_editable = ['status']
    list_per_page = 10

class CommentInLine(admin.TabularInline):
    model = Comment
    fields = ['post', 'user','description', 'status']
    extra = 1
    min_num = 1
