from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse



class User(AbstractUser):
    pass

class Catigory(models.Model):
    catigory_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.catigory_name


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
    lot_last_bid = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    lot_owner = models.ForeignKey(User, on_delete=models.CASCADE)   
    lot_status = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.id}:{self.lot_title} - catigory:{self.lot_catigory} ${self.lot_price}"

    def save(self, *args, **cmd_options):                
        self.lot_title = self.lot_title.capitalize()
        super().save(*args, **cmd_options)

    def get_absolute_url(self):
        return reverse('lot_detail_url', args=[self.id])


class Comment(models.Model):
    comment_text = models.TextField()
    comment_user_name = models.CharField(blank=True, max_length=100)
    comment_data_create = models.DateTimeField(auto_now_add=True)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE, related_name="comments", default=None)

class Bid(models.Model):
    bid = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Bid")
    bid_user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    bid_data_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bid_user} made bid ${self.bid} for {self.bid_lot.lot_title}"

class WatchList(models.Model):
    watchlist_lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    watchlist_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Winner(models.Model):
    winner_user = models.ForeignKey(User, on_delete=models.CASCADE)
    winner_lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    winner_data = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"{self.winner_lot.lot_title} - user: {self.winner_user}"


