from django.urls import path, include, re_path
from rest_framework import routers
from app import views

router = routers.DefaultRouter()
router.register('categories', viewset=views.CategoryViewSet, basename='categories')
router.register('users', viewset=views.UserViewSet, basename='users')
router.register('houses', viewset=views.HouseViewSet, basename='houses')
router.register('posts', viewset=views.PostViewSet, basename='posts')
router.register('comments', viewset=views.CommentViewSet, basename='comments')
router.register('upload_image', viewset=views.ImageViewSet, basename='upload_image')
router.register('follow', viewset=views.FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls))
]

