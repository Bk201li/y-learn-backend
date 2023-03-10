from django.urls import path, include
from .views import RegistrationView ,ChangePasswordView, ExerciceViewset, CategoryViewset, UserViewSet, getRoutes
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register('exercices', ExerciceViewset, basename='exercice')
router.register('categories', CategoryViewset, basename='category')
router.register("users", UserViewSet)


urlpatterns = [
    path('', getRoutes),
    path('accounts/register/', RegistrationView.as_view(), name='register'),
    path('accounts/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]