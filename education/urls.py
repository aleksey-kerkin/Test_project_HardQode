from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, LessonViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'products/(?P<product_id>\d+)/lessons', LessonViewSet, basename='product-lessons')

urlpatterns = [
    path('', include(router.urls)),
]
