from django.db import models
from django.conf import settings

class Item(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title



class OrderItem(models.Model):
    pass

    def __str__(self):
        return self.title

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                            on_delete = models.CASCADE)
    
    items = models.ManyToManyField(OrderItem)
    start_date = models.Da
    ordered = models.BooleanField(default = False)
    
    def __str__(self):
        return self.user.username

