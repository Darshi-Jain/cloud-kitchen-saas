from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KitchenViewSet, MenuItemViewSet, OrderViewSet

router = DefaultRouter()
router.register('kitchens', KitchenViewSet)
router.register('menu', MenuItemViewSet)
router.register('orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]