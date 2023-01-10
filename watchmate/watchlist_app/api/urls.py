from django.urls import path, include
from .views import (WatchListDetailAV, WatchListAV, ReviewList, WatchListGV,
                    ReviewDetail, ReviewCreate, StreamPlatformVS, UserReview)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')
# router.register('', WatchListVS, basename='watchlist')

urlpatterns = [
    path('list/', WatchListAV.as_view(), name='watch-list'),
    path('<int:pk>/', WatchListDetailAV.as_view(), name='watch-list-details'),
    path('new-list/', WatchListGV.as_view(), name='new-watch-list'),

    path('', include(router.urls)),

    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>/', StreamPlatformDetailsAV.as_view(), name='streamplatform-detail'),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),

    path('review/', UserReview.as_view(), name='user-review-detail'),
    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]
