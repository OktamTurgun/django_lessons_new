from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

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

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    confirm_password = forms.CharField(
        label="Confirm Password", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # parolni hashlaydi
        if commit:
            user.save()
        return user