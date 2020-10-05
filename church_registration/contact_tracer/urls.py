from django.urls import path
from contact_tracer import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
]