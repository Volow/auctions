from dataclasses import fields
from django import forms
from .models import *

class CatigoryForm(forms.ModelForm):
    class Meta:
        model = Catigory
        fields = ['catigory_name']
        widget = {
            'catigory_name': forms.TextInput(attrs={"class" : "form-control"})
        }


class AddLotForm (forms.Form):
    lot_title = forms.CharField(max_length=64,                                 
                                 widget=forms.TextInput(
                                     attrs={
                                        # "placeholder": "Title",
                                        "class": "form-control",
                                        "label":"",
                                        "id": "exampleFormControlInput1"
                                            }
                                 ))
    lot_description = forms.CharField(widget=forms.Textarea(
                                        attrs={
                                            # "placeholder":"Description",
                                            "rows":"4",
                                            "class":"form-control",
                                            "label":"",
                                            "id": "exampleFormControlInput2"
                                                }))
    lot_img = forms.ImageField()
    lot_img.widget.attrs.update({'class': 'form-control-file'})

    lot_price = forms.DecimalField(max_digits=10, decimal_places=2)
    lot_price.widget.attrs.update({'placeholder': 'price'})

    

    