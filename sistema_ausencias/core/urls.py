from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/solicitudes', views.SolicitudViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),
]