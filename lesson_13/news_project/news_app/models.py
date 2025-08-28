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

  title = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250, unique=True)
  content = models.TextField()
  image = models.ImageField(upload_to='news/images/')
  category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='news')
  published_at = models.DateTimeField(default=timezone.now)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=2, 
                            choices=Status.choices, 
                            default=Status.DRAFT
                            )

  class Meta:
    ordering = ['-published_at']

  def __str__(self):
    return self.title
