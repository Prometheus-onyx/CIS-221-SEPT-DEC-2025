from atexit import register
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib import admin

from . import views

router = DefaultRouter()
#router.register('customers', views.CustomerViewSet)

urlpatterns = [
    path('Customers/', include(router.urls)),
    path('home/', views.home, name='home'),
    path('', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('admin/', admin.site.urls),
]