from dataclasses import fields
from django import forms
from .models import *

class CatigoryForm(forms.ModelForm):
    class Meta:
        model = Catigory
        fields = ['catigory_name']
        widgets = {
            'catigory_name': forms.TextInput(attrs={"class":"form-control"})
        }
            
class LotForm(forms.ModelForm):
    class Meta:
        model = Lot
        fields = [ 'lot_title', 'lot_img', 'lot_description', 'lot_catigory', 'lot_price']
        widgets = {
            'lot_title' : forms.TextInput(attrs={"class": "form-control"}),
            'lot_description' : forms.Textarea(attrs={"rows":"4", "class":"form-control"}),
            'lot_img' : forms.FileInput(attrs={"class":"form-control"}),            
            'lot_price' : forms.TextInput(attrs={"class":"form-control", 'placeholder': 'price'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {'comment_text': forms.Textarea(attrs={
            'rows':'4',
            'class':'form-control'
        })}
    

    