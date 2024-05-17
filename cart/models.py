from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Price(models.Model):
    original_price = models.DecimalField(max_digits=10, decimal_places=2)  # e.g., 100.00
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=1000, blank=True, null=True)
    images = models.CharField(max_length=1000)  # Will be updated based on the discount

    def save(self, *args, **kwargs):
        # Calculate discounted price if there's a discount
        current_discount = Discount.objects.first()
        if current_discount:
            discount_percentage = current_discount.discount / 100
            self.discounted_price = self.original_price * (1 - discount_percentage)
        else:
            self.discounted_price = self.original_price
        super().save(*args, **kwargs)


class Discount(models.Model):
    discount = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 20.00 for 20%

    def __str__(self):
        return f"Discount: {self.discount}%"


@receiver(post_save, sender=Discount)
def apply_discount_to_prices(sender, instance, **kwargs):
    discount_percentage = instance.discount / 100
    prices = Price.objects.all()
    for price in prices:
        price.discounted_price = price.original_price * (1 - discount_percentage)
        price.save()
