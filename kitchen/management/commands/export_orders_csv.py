from django.core.management.base import BaseCommand
from kitchen.models import Order
import csv

class Command(BaseCommand):
    help = "Export orders to CSV for Looker Studio"

    def handle(self, *args, **kwargs):
        with open("orders_export.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Kitchen",
                "Location",
                "Customer",
                "Item",
                "Quantity",
                "Status",
                "Amount",
                "Date"
            ])

            for order in Order.objects.select_related("kitchen").all():
                writer.writerow([
                    order.kitchen.name,
                    order.kitchen.location,
                    order.customer_name,
                    order.item_name,
                    order.quantity,
                    order.status,
                    order.total_amount,
                    order.order_date
                ])

        self.stdout.write(self.style.SUCCESS("orders_export.csv created successfully"))
