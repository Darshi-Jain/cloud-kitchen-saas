from django.core.management.base import BaseCommand
from kitchen.models import Kitchen, MenuItem, Order, Inventory
import random

class Command(BaseCommand):
    help = "Seed database with demo cloud kitchen data"

    def handle(self, *args, **kwargs):
        Order.objects.all().delete()
        MenuItem.objects.all().delete()
        Inventory.objects.all().delete()
        Kitchen.objects.all().delete()

        kitchens = [
            Kitchen.objects.create(name="Downtown Kitchen", location="San Francisco", manager="Aarav Shah"),
            Kitchen.objects.create(name="Mission Kitchen", location="San Francisco", manager="Neha Patel"),
            Kitchen.objects.create(name="Bay Kitchen", location="Oakland", manager="Rohan Mehta"),
            Kitchen.objects.create(name="Central Kitchen", location="San Jose", manager="Priya Rao"),
        ]

        items = ["Burger", "Pizza", "Pasta", "Wrap", "Biryani", "Noodles", "Salad", "Coffee"]
        statuses = ["Pending", "Preparing", "Out for Delivery", "Delivered"]

        for kitchen in kitchens:
            for item in items[:5]:
                MenuItem.objects.create(
                    kitchen=kitchen,
                    name=item,
                    category=random.choice(["Fast Food", "Italian", "Indian", "Beverage"]),
                    price=random.randint(8, 25),
                    available=True
                )

        for i in range(40):
            kitchen = random.choice(kitchens)
            item = random.choice(items)
            qty = random.randint(1, 5)
            Order.objects.create(
                kitchen=kitchen,
                customer_name=f"Customer {i+1}",
                item_name=item,
                quantity=qty,
                status=random.choice(statuses),
                total_amount=qty * random.randint(8, 25)
            )

        for kitchen in kitchens:
            for item in ["Tomatoes", "Cheese", "Bread", "Rice", "Oil"]:
                Inventory.objects.create(
                    kitchen=kitchen,
                    item_name=item,
                    stock_quantity=random.randint(5, 100),
                    minimum_stock=15,
                    supplier=random.choice(["Sysco", "Fresh Farms", "Local Market"])
                )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully"))
