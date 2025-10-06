from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("news:category_detail", kwargs={"slug": self.slug})


# Custom Manager (PublishedManager) ni tashqarida aniqlaymiz
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=self.model.Status.PUBLISHED)


class News(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'Df', 'Draft'
        PUBLISHED = 'Pu', 'Published'
        ARCHIVED = 'Ar', 'Archived'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    content = models.TextField()
    image = models.ImageField(upload_to='news/images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT
    )

    views = models.PositiveIntegerField(default=0) # Ko'rishlar soni

    # Managers
    objects = models.Manager()   # Default manager
    published = PublishedManager()  # Custom manager faqat PUBLISHED postlarni qaytaradi

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("news:news_detail", kwargs={"slug": self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField (auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'Comment by {self.author.username} - {self.news.title}'

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f'Message from {self.name} <{self.email}>'
