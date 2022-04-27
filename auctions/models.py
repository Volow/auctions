from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator



class User(AbstractUser):
    pass

class Catigory(models.Model):
    catigory_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.catigory_name

class Comment(models.Model):
    comment_text = models.TextField()
    comment_user_name = models.CharField(max_length=100)
    comment_data_create = models.DateTimeField(auto_now_add=True)

class Lot(models.Model):
    lot_title = models.CharField(max_length=64, unique=True, verbose_name="Title")    
    lot_img = models.ImageField(
        blank = True, upload_to = "pic/",
        verbose_name="Photo", default='pic/no_img.jpg')
    lot_description = models.TextField(blank=True)
    lot_catigory = models.ForeignKey(Catigory, on_delete=models.CASCADE, related_name="categories")
    lot_price = models.DecimalField(
        max_digits=20, decimal_places=2,
        validators=[MinValueValidator(0.001)], verbose_name="Price",        
        help_text="Min prise is $0.01")
    lot_owner = models.ForeignKey(User, on_delete=models.CASCADE)  
    # lot_date_create = models.DateTimeField(auto_now_add=True)
    lot_status = models.BooleanField(default=True)
    lot_comments = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.lot_title} - catigory:{self.lot_catigory} ${self.lot_price}"

    def save(self, *args, **cmd_options):                
        self.lot_title = self.lot_title.capitalize()
        super().save(*args, **cmd_options)



