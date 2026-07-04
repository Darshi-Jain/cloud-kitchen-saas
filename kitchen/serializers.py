from rest_framework import serializers
from .models import Kitchen, MenuItem, Order

class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'