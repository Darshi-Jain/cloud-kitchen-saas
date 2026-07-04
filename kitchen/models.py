from django.db import models

class Kitchen(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name


class Order(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    status = models.CharField(default="PENDING", max_length=20)

    def __str__(self):
        return self.item_name