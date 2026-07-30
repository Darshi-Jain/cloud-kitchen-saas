from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum, Count
from rest_framework import viewsets
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import csv

from .models import Kitchen, MenuItem, Order, Inventory, Integration
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


# ==========================================================
# TECHNICAL OPERATIONS
# ==========================================================

def technical_operations(request):
    context = {
        "application_status": "Operational",
        "database_status": "Connected",
        "api_status": "Healthy",
        "deployment_version": "v7",
    }
    return render(
        request,
        "kitchen/technical_operations.html",
        context,
    )






def reports(request):
    today = timezone.localdate()
    default_start_date = today - timedelta(days=6)

    start_date_text = request.GET.get(
        "start_date",
        default_start_date.isoformat(),
    )
    end_date_text = request.GET.get(
        "end_date",
        today.isoformat(),
    )

    try:
        start_date = datetime.strptime(
            start_date_text,
            "%Y-%m-%d",
        ).date()

        end_date = datetime.strptime(
            end_date_text,
            "%Y-%m-%d",
        ).date()

    except ValueError:
        start_date = default_start_date
        end_date = today

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    orders = Order.objects.select_related("kitchen").filter(
        order_date__range=(start_date, end_date)
    )

    total_orders = orders.count()

    total_revenue = orders.aggregate(
        total=Sum("total_amount")
    )["total"] or Decimal("0")

    average_order_value = (
        total_revenue / total_orders
        if total_orders
        else Decimal("0")
    )

    kitchen_performance = list(
        orders.values(
            "kitchen__id",
            "kitchen__name",
        )
        .annotate(
            orders=Count("id"),
            revenue=Sum("total_amount"),
        )
        .order_by("-revenue")
    )

    top_kitchen = (
        kitchen_performance[0]["kitchen__name"]
        if kitchen_performance
        else "No data"
    )

    top_items = list(
        orders.values("item_name")
        .annotate(
            orders=Count("id"),
            quantity=Sum("quantity"),
            revenue=Sum("total_amount"),
        )
        .order_by("-revenue")[:5]
    )

    date_labels = []
    revenue_data = []
    order_data = []

    current_date = start_date

    while current_date <= end_date:
        daily_orders = orders.filter(order_date=current_date)

        daily_revenue = daily_orders.aggregate(
            total=Sum("total_amount")
        )["total"] or Decimal("0")

        date_labels.append(current_date.strftime("%d %b"))
        revenue_data.append(float(daily_revenue))
        order_data.append(daily_orders.count())

        current_date += timedelta(days=1)

    if request.GET.get("export") == "csv":
        response = HttpResponse(
            content_type="text/csv",
        )

        response["Content-Disposition"] = (
            f'attachment; filename="kitchen-report-'
            f'{start_date}-to-{end_date}.csv"'
        )

        writer = csv.writer(response)

        writer.writerow([
            "Cloud Kitchen Report",
            f"{start_date} to {end_date}",
        ])

        writer.writerow([])
        writer.writerow(["Summary"])
        writer.writerow(["Total Revenue", total_revenue])
        writer.writerow(["Total Orders", total_orders])
        writer.writerow([
            "Average Order Value",
            round(average_order_value, 2),
        ])
        writer.writerow(["Top Kitchen", top_kitchen])

        writer.writerow([])
        writer.writerow([
            "Order ID",
            "Order Date",
            "Kitchen",
            "Customer",
            "Item",
            "Quantity",
            "Status",
            "Total Amount",
        ])

        for order in orders.order_by("-order_date", "-id"):
            writer.writerow([
                order.id,
                order.order_date,
                order.kitchen.name,
                order.customer_name,
                order.item_name,
                order.quantity,
                order.status,
                order.total_amount,
            ])

        return response

    context = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_order_value": average_order_value,
        "top_kitchen": top_kitchen,
        "date_labels": date_labels,
        "revenue_data": revenue_data,
        "order_data": order_data,
        "top_items": top_items,
        "kitchen_performance": kitchen_performance,
    }

    return render(
        request,
        "kitchen/reports.html",
        context,
    )


def integrations(request):
    default_integrations = [
        {
            "name": "DoorDash",
            "provider": "DoorDash",
            "category": "Delivery",
            "description": "Receive and manage DoorDash orders directly in KitchenOS.",
        },
        {
            "name": "Uber Eats",
            "provider": "Uber",
            "category": "Delivery",
            "description": "Synchronize Uber Eats orders and delivery activity.",
        },
        {
            "name": "Grubhub",
            "provider": "Grubhub",
            "category": "Delivery",
            "description": "Manage Grubhub orders from your central dashboard.",
        },
        {
            "name": "Stripe",
            "provider": "Stripe",
            "category": "Payments",
            "description": "Accept and track secure online payments.",
        },
        {
            "name": "QuickBooks",
            "provider": "Intuit",
            "category": "Accounting",
            "description": "Synchronize revenue and transaction data with QuickBooks.",
        },
        {
            "name": "Slack",
            "provider": "Slack",
            "category": "Communication",
            "description": "Send order and operational alerts to your Slack workspace.",
        },
    ]

    for integration_data in default_integrations:
        Integration.objects.get_or_create(
            name=integration_data["name"],
            defaults=integration_data,
        )

    if request.method == "POST":
        integration_id = request.POST.get("integration_id")
        action = request.POST.get("action")

        integration = get_object_or_404(
            Integration,
            id=integration_id,
        )

        if action == "connect":
            integration.connected = True
        elif action == "disconnect":
            integration.connected = False

        integration.save()

        return redirect("integrations")

    integrations_list = Integration.objects.all().order_by(
        "category",
        "name",
    )

    context = {
        "integrations": integrations_list,
        "connected_count": integrations_list.filter(
            connected=True
        ).count(),
        "total_integrations": integrations_list.count(),
    }

    return render(
        request,
        "kitchen/integrations.html",
        context,
    )


def settings_page(request):
    return render(
        request,
        "kitchen/settings.html",
    )
