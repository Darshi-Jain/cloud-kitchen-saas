from django import forms
from .models import Kitchen, MenuItem, Order, Inventory

class KitchenForm(forms.ModelForm):
    class Meta:
        model = Kitchen
        fields = "__all__"

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"
