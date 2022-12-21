from rest_framework.authtoken.views import obtain_auth_token
from .views import registration_view
from django.urls import path


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('sign-in/', registration_view, name='sign-in'),

]
