from django import forms

class EditImgForm(forms.Form):
    picture = forms.ImageField()
    
    def __str__(self): 
        return self.title 