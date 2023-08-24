from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import UserProfile


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email_exists = User.objects.filter(email=attrs['email']).exists()

        if email_exists:
            raise ValidationError('Email already in use')

        return super().validate(attrs)

    def create(self, validated_data):
        username = validated_data['email'].split('@')[0]
        user = User.objects.create(
            username=username,
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        UserProfile.objects.create(user=user)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'bio', 'user']

    def update(self, instance, validated_data):
        user = instance.user

        username = validated_data['user']['username']
        profile_name = validated_data['name']
        profile_bio = validated_data['bio']

        if user.username != username:
            user.username = username
            user.save()

        if profile_name:
            instance.name = profile_name
        if profile_bio:
            instance.bio = profile_bio

        return instance


