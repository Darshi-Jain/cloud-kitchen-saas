from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from rest_framework import viewsets

from .models import Kitchen, MenuItem, Order, Inventory
from .forms import KitchenForm, MenuItemForm, OrderForm, InventoryForm
from .serializers import (
    KitchenSerializer,
    MenuItemSerializer,
    OrderSerializer,
    InventorySerializer,
)


# ==========================================================
# DASHBOARD
# ==========================================================

def dashboard(request):
    context = {
        "total_kitchens": Kitchen.objects.count(),
        "total_menu_items": MenuItem.objects.count(),
        "total_orders": Order.objects.count(),
        "pending_orders": Order.objects.filter(status="Pending").count(),
        "total_revenue": Order.objects.aggregate(
            Sum("total_amount")
        )["total_amount__sum"] or 0,
        "recent_orders": Order.objects.select_related("kitchen").order_by("-id")[:10],
    }

    return render(request, "kitchen/dashboard.html", context)


# ==========================================================
# KITCHENS
# ==========================================================

def kitchens_page(request):
    kitchens = Kitchen.objects.all()

    return render(
        request,
        "kitchen/kitchens.html",
        {"kitchens": kitchens},
    )


def kitchen_create(request):

    form = KitchenForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("kitchens_page")

    return render(
        request,
        "kitchen/form.html",
        {
            "form": form,
            "title": "Add Kitchen",
        },
    )


def kitchen_edit(request, pk):

    kitchen = get_object_or_404(Kitchen, pk=pk)

    form = KitchenForm(
        request.POST or None,
        instance=kitchen,
    )

    if form.is_valid():
        form.save()
        return redirect("kitchens_page")

    return render(
        request,
        "kitchen/form.html",
        {
            "form": form,
            "title": "Edit Kitchen",
        },
    )


def kitchen_delete(request, pk):

    kitchen = get_object_or_404(Kitchen, pk=pk)

    kitchen.delete()

    return redirect("kitchens_page")


# ==========================================================
# ORDERS
# ==========================================================

def orders_page(request):

    orders = Order.objects.select_related("kitchen").all()

    return render(
        request,
        "kitchen/orders.html",
        {"orders": orders},
    )


def order_create(request):

    form = OrderForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("orders_page")

    return render(
        request,
        "kitchen/form.html",
        {
            "form": form,
            "title": "Create Order",
        },
    )


def order_edit(request, pk):

    order = get_object_or_404(Order, pk=pk)

    form = OrderForm(
        request.POST or None,
        instance=order,
    )

    if form.is_valid():
        form.save()
        return redirect("orders_page")

    return render(
        request,
        "kitchen/form.html",
        {
            "form": form,
            "title": "Edit Order",
        },
    )


def order_delete(request, pk):

    order = get_object_or_404(Order, pk=pk)

    order.delete()

    return redirect("orders_page")


# ==========================================================
# MENU
# ==========================================================

def menu_page(request):

    menu_items = MenuItem.objects.select_related("kitchen").all()

    return render(
        request,
        "kitchen/menu.html",
        {
            "menu_items": menu_items,
        },
    )


# ==========================================================
# INVENTORY
# ==========================================================

def inventory_page(request):

    inventory_items = Inventory.objects.select_related("kitchen").all()

    return render(
        request,
        "kitchen/inventory.html",
        {
            "inventory_items": inventory_items,
        },
    )


# ==========================================================
# REST API
# ==========================================================

class KitchenViewSet(viewsets.ModelViewSet):

    queryset = Kitchen.objects.all()

    serializer_class = KitchenSerializer


class MenuItemViewSet(viewsets.ModelViewSet):

    queryset = MenuItem.objects.all()

    serializer_class = MenuItemSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()

    serializer_class = OrderSerializer


class InventoryViewSet(viewsets.ModelViewSet):

    queryset = Inventory.objects.all()

    serializer_class = InventorySerializer
