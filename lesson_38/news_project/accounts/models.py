from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.TextField(blank=True)
  location = models.CharField(max_length=30, blank=True)
  birth_date = models.DateField(null=True, blank=True)
  avatar = models.ImageField(upload_to='profile_photos/', null=True, blank=True)


  def __str__(self):
    return f"{self.user.username} Profile"
