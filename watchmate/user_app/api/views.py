from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .serializers import RegistrationSerializer
from .. import models


@api_view(['POST'])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'Registration successful'
            data['username'] = user.username
            data['email'] = user.email
            data['token'] = Token.objects.get(user=user).key
        else:
            data = serializer.errors

        return Response(data)
