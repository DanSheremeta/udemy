from rest_framework.authtoken.views import obtain_auth_token
from .views import registrations_view
from django.urls import path


urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('sign-in/', registrations_view, name='sign-in'),

]
