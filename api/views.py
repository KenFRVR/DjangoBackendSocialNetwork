from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import UserRegisterSerializer, UserProfileSerializer
from django.contrib.auth import authenticate
from .models import UserProfile
from rest_framework import permissions


class LoginApiView(APIView):

    def post(self, request, *args, **kwargs):

        username_or_email = request.data.get('username-email')
        password = request.data.get('password')

        if '@' in username_or_email:
            user = User.objects.get(email=username_or_email)
        else:
            user = authenticate(username=username_or_email, password=password)

        if user is not None and user.is_active:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterApiView(APIView):

    def post(self, request):
        serializer_user = UserRegisterSerializer(data=request.data)

        if serializer_user.is_valid(raise_exception=True):
            user = serializer_user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)


class UserProfilesView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


@api_view(['POST'])
def logout_user(request):
    try:
        token = Token.objects.get(key=request.data.get('token'))
        token.delete()
        return Response("User logged out successfully", status=status.HTTP_200_OK)
    except Token.DoesNotExist as tdn:
        return Response({'error': str(tdn)})


class UpdateUserProfile(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        user = profile.user

        username = request.data['user.username']
        profile_name = request.data['name']
        profile_bio = request.data['bio']

        try:
            if user.username != username and username:
                user.username = username
                user.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if profile_name:
            profile.name = profile_name
        if profile_bio:
            profile.bio = profile_bio
        profile.save()

        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        return serializer.save(partial=True)


@api_view(['GET'])
def allowed_urls(request):
    urls = [
        {
            "POST": ["http://127.0.0.1:8000/api/login",
                     "http://127.0.0.1:8000/api/register",
                     "http://127.0.0.1:8000/api/logout",
                     ]
        },
        {
            "GET": ["http://127.0.0.1:8000/api/users",
                    "http://127.0.0.1:8000/api/users/<str:pk>",
                    ]
        },
        {
            "PUT": "http://127.0.0.1:8000/api/update-user/<str:pk>"
        }
    ]
    return Response(urls)
