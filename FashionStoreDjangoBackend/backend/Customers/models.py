from decimal import Decimal
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category'

class Product(models.Model):
    name = models.CharField(max_length=100)
    curr_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    orig_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'product'
        
class SaleOffers(models.Model):
    sale_Event = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percentage = models.FloatField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.sale_Event
    
    class Meta:
        db_table = 'saleoffers'