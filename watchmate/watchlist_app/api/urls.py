from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', views.StreamPlatformVS, basename='streamplatform')

urlpatterns = [
    path('', views.WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>/', views.WatchListDetailAV.as_view(), name='watch-list-details'),

    path('', include(router.urls)),

    path('<int:pk>/review/create/', views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', views.ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
    path('user-reviews/', views.UserReview.as_view(), name='user-review-detail'),
]
