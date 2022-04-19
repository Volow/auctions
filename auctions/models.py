from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Catigory(models.Model):
    catigory_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.catigory_name}"

class Lot(models.Model):
    lot_title = models.CharField(max_length=64)    
    lot_img = models.ImageField(blank = True, upload_to = "pic/")
    lot_description = models.TextField(blank=True)
    lot_catigory = models.ForeignKey(Catigory, on_delete=models.CASCADE, related_name="categories")
    lot_price = models.DecimalField(max_digits=10, decimal_places=2)
    lot_owner = models.ForeignKey(User, on_delete=models.CASCADE)  
    # lot_date_create = models.DateTimeField(auto_now_add=True)
    lot_status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.lot_title}({self.lot_description}) - catigory:{self.lot_catigory} ${self.lot_price}"
