from django import forms
from home.models import ImageDB

class ImageForm(forms.ModelForm):
    class Meta:
        model=ImageDB
        fields='__all__'
        labels={"photo":''}