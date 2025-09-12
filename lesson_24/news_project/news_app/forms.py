from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):

  class Meta:
    model = Contact
    fields = ['name', 'email', 'message']
    widgets = {
      'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
      'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
      'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5}),
    }
    labels = {
      'name': 'Full Name',
      'email': 'Email Address',
      'message': 'Message',
    }
    help_texts = {
      'name': 'Please enter your full name.',
      'email': 'We will never share your email with anyone else.',
      'message': 'Write your message here.',
    }
    error_messages = {
      'name': {
        'max_length': 'Name is too long.',
        'required': 'Please enter your name.',
      },
      'email': {
        'invalid': 'Enter a valid email address.',
        'required': 'Please enter your email.',
      },
      'message': {
        'required': 'Please enter your message.',
      },
    }
  
  def clean_email(self):
    email = self.cleaned_data.get('email')
    if email and email.split('@')[1].lower() in ['spam.com', 'fake.com']:
        raise forms.ValidationError('Emails from this domain are not allowed.')
    return email
  
  def clean_message(self):
    message = self.cleaned_data.get('message')
    if 'spam' in message.lower():
      raise forms.ValidationError('Message contains inappropriate content.')
    return message
  
  def clean(self):
    cleaned_data = super().clean()
    name = cleaned_data.get('name')
    message = cleaned_data.get('message')
    if name and message:
      if name.lower() in message.lower():
        self.add_error('message', 'Message should not contain your name.')
    return cleaned_data
  
  def save(self, commit=True):
    instance = super().save(commit=False)
    instance.name = instance.name.title()
    if commit:
      instance.save()
    return instance
