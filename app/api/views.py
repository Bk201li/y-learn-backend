from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, action
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework import filters as drf_filters
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
import django_filters
from django_filters import rest_framework as filters
from .models import Exercice, Category, MyUser
from .serializers import RegistrationSerializer, PasswordChangeSerializer, ExerciceSerializer, CategorySerializer, UserSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'http://localhost:8000/api/accounts/register/',
        'http://localhost:8000/api/accounts/change-password/',
        'http://localhost:8000/api/users/',
        'http://localhost:8000/api/users/me/',
        'http://localhost:8000/api/exercices/',
        'http://localhost:8000/api/categories/',
        'http://localhost:8000/api/token/',
        'http://localhost:8000/api/token/refresh/',
    ]

    return Response(routes)


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = PasswordChangeSerializer(context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True) #Another way to write is as in Line 17
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExerciceViewset(ModelViewSet):
    serializer_class = ExerciceSerializer
    filter_backends = [
        drf_filters.OrderingFilter,
        drf_filters.SearchFilter,
        filters.DjangoFilterBackend,
    ]

    def get_queryset(self):
        return Exercice.objects.all()


class CategoryViewset(ModelViewSet):
    serializer_class = CategorySerializer
    filter_backends = [
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
        filters.DjangoFilterBackend,
    ]
    search_fields = ["label"]

    def get_queryset(self):
        return Category.objects.all()


@action(detail=False, methods=["GET"], serializer_class=UserSerializer)
class UserViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer

    def me(self, request):
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
