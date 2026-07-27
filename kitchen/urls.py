from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("kitchens", KitchenViewSet)
router.register("menu", MenuItemViewSet)
router.register("orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("ui/kitchens/", kitchens_page, name="kitchens_page"),
    path("ui/kitchens/add/", kitchen_create, name="kitchen_create"),
    path("ui/kitchens/<int:pk>/edit/", kitchen_edit, name="kitchen_edit"),
    path("ui/kitchens/<int:pk>/delete/", kitchen_delete, name="kitchen_delete"),

    path("ui/orders/", orders_page, name="orders_page"),
    path("ui/orders/add/", order_create, name="order_create"),
    path("ui/orders/<int:pk>/edit/", order_edit, name="order_edit"),
    path("ui/orders/<int:pk>/delete/", order_delete, name="order_delete"),

    path("ui/menu/", menu_page, name="menu_page"),
    path("ui/inventory/", inventory_page, name="inventory_page"),
]
