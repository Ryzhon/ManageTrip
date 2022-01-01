from django.urls import include, path
from rest_framework.routers import DefaultRouter

from trips.api import views as tv

router = DefaultRouter()
router.register(r"trips", tv.TripViewSet)

urlpatterns = [
    path("", include(router.urls)), 

    path("trips/<slug:slug>/todos/", 
         tv.TodoListAPIView.as_view(),
         name="todo-list"),

    path("trips/<slug:slug>/todo/", 
         tv.TodoCreateAPIView.as_view(),
         name="todo-create"),

    path("todo/<uuid:uuid>/", 
         tv.TodoRUDAPIView.as_view(),
         name="todo-detail"),
     path("userinfo/",tv.UserInfoAPIView.as_view(),
     name="user-info")

    # path("answers/<uuid:uuid>/like/",
    #      tv.AnswerLikeAPIView.as_view(),
    #      name="answer-like")
]