from django.urls import path, include
from rest_framework import routers

from core import views

app_name = 'core'

router = routers.DefaultRouter()
router.register(r'items', views.ItemViewSet)
router.register(r'category', views.CategoryViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
