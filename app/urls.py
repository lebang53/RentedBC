from django.urls import path, include, re_path
from rest_framework import routers
from app import views
from app.views import stats_view, stats_view2

router = routers.DefaultRouter()
router.register('categories', viewset=views.CategoryViewSet, basename='categories')
router.register('users', viewset=views.UserViewSet, basename='users')
router.register('houses', viewset=views.HouseViewSet, basename='houses')
router.register('posts', viewset=views.PostViewSet, basename='posts')
router.register('comments', viewset=views.CommentViewSet, basename='comments')
router.register('upload_image', viewset=views.ImageViewSet, basename='upload_image')
router.register('follow', viewset=views.FollowViewSet, basename='follow')
router.register('house_stats', viewset=views.HouseStatsViewSet, basename='house_stats')
router.register('api/user-stats', viewset=views.UserStatsViewSet, basename='user_stats')

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', stats_view, name='stats'),
    path('stats2/', stats_view2, name='stats2'),
]
# Thống kê số lượng người dùng, chủ trọ(theo khoảng thời gian, tháng, năm, quý)
# thống kê bao nhiêu cái nhà đc đăng lên(nhà)
# thống kê trong tháng có bao nhiêu nhà đc thuê

