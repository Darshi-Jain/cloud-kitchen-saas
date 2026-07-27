from django.db import models

class Kitchen(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=150)
    manager = models.CharField(max_length=100, default="Not Assigned")
    status = models.CharField(max_length=30, default="Active")

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, default="General")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, default="Walk-in Customer")
    item_name = models.CharField(max_length=100, default="Unknown Item")
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=30, default="Pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.item_name}"


class Inventory(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    stock_quantity = models.IntegerField()
    minimum_stock = models.IntegerField(default=10)
    supplier = models.CharField(max_length=100)

    def __str__(self):
        return self.item_name
