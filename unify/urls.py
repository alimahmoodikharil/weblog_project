from django.urls import path, include
from rest_framework_nested import routers

from . import views

router = routers.DefaultRouter()

router.register('post', views.PostViewSet, basename='post')

post_router = routers.NestedDefaultRouter(router, 'post', lookup= 'post')
post_router.register('comment', views.CommentViewSet, basename='post-comment')


urlpatterns = router.urls + post_router.urls
