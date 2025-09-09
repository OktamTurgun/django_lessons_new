from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
  name = models.CharField(max_length=100, unique=True)

  class Meta:
    verbose_name_plural = 'Categories'

  def __str__(self):
    return self.name


class News(models.Model):

  class Status(models.TextChoices):
    DRAFT = 'Df', 'Draft'
    PUBLISHED = 'Pu', 'Published'
    ARCHIVED = 'Ar', 'Archived'

  class PublishedManager(models.Manager):
    def get_queryset(self):
      return super().get_queryset().filter(status=News.Status.PUBLISHED)

  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250, unique=True)
  content = models.TextField()
  image = models.ImageField(upload_to='news/images/', blank=True, null=True)
  category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='news')
  published_at = models.DateTimeField(default=timezone.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=2, 
                            choices=Status.choices, 
                            default=Status.DRAFT
                            )
  
  objects = models.Manager() # default manager
  published = PublishedManager() # custom manager

  class Meta:
    ordering = ['-published_at']

  def __str__(self):
    return self.title

class Contact(models.Model):
  name = models.CharField(max_length=100)
  email = models.EmailField()
  message = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'Message from {self.name} <{self.email}>'
  
  class Meta:
    ordering = ['-created_at']
    verbose_name = 'Contact Message'
    verbose_name_plural = 'Contact Messages'
    
    

  