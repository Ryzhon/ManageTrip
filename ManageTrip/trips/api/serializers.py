from rest_framework import serializers
from django.conf import settings

from trips.models import Todo, Trip, ChatModel
from users.models import CustomUser


##what self happens is in web
##what instance happens is in database

# class CalcSeriarizer(serializers.ModelSerializer):
#     class Meta:
#         model = CalcUser
#         fields = "__all__"


class TodoListSerializer(serializers.ModelSerializer):

    # calc = CalcSeriarizer()

    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()
    nices_count = serializers.SerializerMethodField()
    user_has_niced_todo = serializers.SerializerMethodField()
    From = serializers.StringRelatedField()
    To = serializers.StringRelatedField()
    
    trip_slug = serializers.SerializerMethodField()
    


    class Meta:
        model = Todo
        exclude = ["id","trip","voters", "updated_at"]
      

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_nices_count(self, instance):
        return instance.voters.count()

    def get_user_has_niced_todo(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

    def get_trip_slug(self, instance):
        return instance.trip.slug


class TripSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    user_has_answered = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        exclude = [ "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")



    def get_user_has_answered(self, instance):
        request = self.context.get("request")
        return instance.todo.filter(author=request.user).exists()


class TodoCreateSerializer(serializers.ModelSerializer):

    # calc = CalcSeriarizer()

    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()
    nices_count = serializers.SerializerMethodField()
    user_has_niced_todo = serializers.SerializerMethodField()
  
    class Meta:
        model = Todo
        exclude = ["id","trip","voters", "updated_at"]  

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_nices_count(self, instance):
        return instance.voters.count()

    def get_user_has_niced_todo(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

    def get_trip_slug(self, instance):
        return instance.trip.slug


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields=("id", "username", "total_charge")
        # fields="__all__"

class ChatSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = ChatModel
        exclude=["id", "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%b %d %H:%M")




