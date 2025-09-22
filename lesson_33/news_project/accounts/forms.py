from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class LoginForm(forms.Form):
  username = forms.CharField(
    label="Username",
    widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  password = forms.CharField(
    label="Password",
    widget=forms.PasswordInput(attrs={'class': 'form-control'}) 
  )
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})