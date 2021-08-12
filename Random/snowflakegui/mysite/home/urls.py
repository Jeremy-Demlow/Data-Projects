from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home_index, name='home_index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile_index, name='profile'),
    path('contact/', views.contact_index, name='contact'),
    path('about/', views.about_index, name='about'),
    path('pricing/', views.pricing_index, name='pricing'),
    path('tutorials/', views.tutorials_index, name='tutorials'),
]
