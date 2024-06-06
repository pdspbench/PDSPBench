from django.urls import path

from . import views

urlpatterns = [
    path('healthy',views.HealthyChecker.as_view(),name='Healthy checker'),
    path('register',views.RegisterUser.as_view(), name='Register user'),
    path('login',views.LoginUser.as_view(), name='Login user'),
]