from django.urls import path
from contact_tracer import views
from django.views.static import serve
#from django.conf import settings

urlpatterns = [
    path('', views.registration, name='registration'),
    path('register/', views.register, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('qr_generator/', views.qr_generator, name="qr_generator"),
    path('generate/', views.generate, name="generate"),
    path('export_to_csv/', views.export_to_csv, name="export_to_csv")
#    path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
#    path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
