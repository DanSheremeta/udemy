from django.urls import path
from .views import *

urlpatterns = [
    path('list/', book_list, name='book_list'),
    path('<int:pk>/', book_detail, name='book_detail'),
]
