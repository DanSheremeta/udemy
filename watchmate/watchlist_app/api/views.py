from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, generics, viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView

from . import serializers, pagination, throttling, permissions
from .. import models


# Review Views
class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    throttle_classes = [throttling.ReviewListThrottle, AnonRateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return models.Review.objects.filter(watchlist=pk)


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    # throttle_scope = 'review-detail'


class ReviewCreate(generics.CreateAPIView):
    serializer_class = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]

    # throttle_classes = throttling.ReviewCreateThrottle

    def get_queryset(self):
        return models.Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = models.WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = models.Review.objects.filter(watchlist=movie, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie")

        if movie.review_number == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2

        movie.review_number += 1
        movie.save()

        serializer.save(watchlist=movie, review_user=review_user)


class UserReview(generics.ListAPIView):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return models.Review.objects.filter(review_user__username=username)


# Watch List Views
class WatchListGV(generics.ListAPIView):
    queryset = models.WatchList.objects.all()
    serializer_class = serializers.WatchListSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = pagination.WatchListPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['title', 'platform__name', 'avg_rating']
    search_fields = ['title', 'platform__name']
    ordering_fields = ['-avg_rating']


class WatchListAV(APIView):
    # permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request):
        movies = models.WatchList.objects.all()
        serializer = serializers.WatchListSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = serializers.WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchListDetailAV(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = models.WatchList.objects.get(pk=pk)
            serializer = serializers.WatchListSerializer(movie)
            return Response(serializer.data)
        except models.WatchList.DoesNotExist:
            return Response({'Error': 'Movie is not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        movie = models.WatchList.objects.get(pk=pk)
        serializer = serializers.WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = models.WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Stream Platform Views
class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = models.StreamPlatform.objects.all()
    serializer_class = serializers.StreamPlatformSerializer
    permission_classes = [permissions.IsAdminOrReadOnly]
