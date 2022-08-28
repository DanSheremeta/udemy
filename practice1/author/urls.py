from django.urls import path

from .views import *

urlpatterns = [
    path('list/', author_list, name='authors_list'),
    path('<int:pk>/', author_detail, name='author_details'),
]
