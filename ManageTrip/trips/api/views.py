from rest_framework import generics, serializers, status, viewsets
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser

from trips.api.permissions import IsAuthorOrReadOnly
from trips.api.serializers import TodoCreateSerializer, TripSerializer, TodoListSerializer, UserInfoSerializer
from trips.models import Trip, Todo

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all().order_by("-created_at")
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class TodoCreateAPIView(generics.CreateAPIView):

    queryset = Todo
    serializer_class = TodoCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        trip = get_object_or_404(Trip, slug=kwarg_slug)

        # if trip.todo.filter(author=request_user).exists():
        #     raise ValidationError("You have already answered this Question")

        serializer.save(author=request_user, trip=trip)


class TodoListAPIView(generics.ListAPIView):
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Todo.objects.filter(trip__slug=kwarg_slug).order_by("-created_at")

class TodoRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Provide *RUD functionality for an answer instance to it's author."""

    queryset = Todo.objects.all()
    serializer_class = TodoCreateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    lookup_field = "uuid"

class UserInfoAPIView(generics.ListAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        return CustomUser.objects.all().order_by("id")

