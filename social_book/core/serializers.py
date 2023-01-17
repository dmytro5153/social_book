from rest_framework import serializers
from django.contrib.auth.models import User
from .models import LikePost

class LikePostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LikePost
        fields = ('post_id', 'username', 'liked_at')

class CustomUserFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('username','email','is_active','is_superuser','date_joined','last_login', 'last_activity')