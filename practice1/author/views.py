from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


@api_view(['GET', 'POST'])
def author_list(request):

    if request.method == 'GET':
        books = Author.objects.all()
        serializer = AuthorSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(request, pk):

    if request.method == 'GET':
        try:
            book = Author.objects.get(pk=pk)
            serializer = AuthorSerializer(book)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response({'Error': 'Book does not exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        book = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        book = Author.objects.get(pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
