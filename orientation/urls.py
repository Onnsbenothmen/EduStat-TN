from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrientationRecordViewSet

router = DefaultRouter()
router.register(r"orientations", OrientationRecordViewSet, basename="orientation")

urlpatterns = [
    path("", include(router.urls)),
]
