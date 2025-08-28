# Django 13-dars: Amaliyot - Loyiha modelini tuzish

## Maqsad
Ushbu amaliyotda siz "Kutubxona boshqaruv tizimi" uchun to'liq modellar tuzasiz va ular bilan amaliy ishni o'rganasiz.

## Loyiha yaratish va sozlash

### 1-bosqich: Django loyiha yaratish

```bash
# Yangi Django loyiha yaratish
django-admin startproject library_system
cd library_system

# App yaratish
python manage.py startapp books

# Virtual environment yaratish (agar yo'q bo'lsa)
python -m venv venv
source venv/bin/activate  # Linux/Mac uchun
# yoki
venv\Scripts\activate  # Windows uchun

# Django o'rnatish
pip install django pillow
```

### 2-bosqich: Settings sozlash

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'books',  # Bizning app'imiz
]

# Media fayllar uchun
import os
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 3-bosqich: URL sozlash

```python
# library_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
]

# Media fayllar uchun URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

```python
# books/urls.py (yangi fayl yarating)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

## Modellarni yaratish

### 4-bosqich: Asosiy modellar

```python
# books/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date, timedelta

class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Ism")
    last_name = models.CharField(max_length=100, verbose_name="Familiya")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Tug'ilgan sana")
    death_date = models.DateField(blank=True, null=True, verbose_name="Vafot sana")
    biography = models.TextField(blank=True, verbose_name="Biografiya")
    photo = models.ImageField(
        upload_to='authors/', 
        blank=True, 
        null=True,
        verbose_name="Rasm"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Yoshi yoki vafot vaqtidagi yoshi"""
        if self.birth_date:
            end_date = self.death_date or date.today()
            return end_date.year - self.birth_date.year
        return None
    
    class Meta:
        verbose_name = "Muallif"
        verbose_name_plural = "Mualliflar"
        ordering = ['last_name', 'first_name']

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nomi")
    description = models.TextField(blank=True, verbose_name="Tavsifi")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @property
    def book_count(self):
        """Bu kategoriyada nechta kitob bor"""
        return self.books.count()
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['name']

class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="Nomi")
    address = models.TextField(blank=True, verbose_name="Manzil")
    website = models.URLField(blank=True, verbose_name="Veb-sayt")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Nashriyot"
        verbose_name_plural = "Nashriyotlar"
        ordering = ['name']

class Book(models.Model):
    LANGUAGE_CHOICES = [
        ('uz', "O'zbek"),
        ('en', 'English'),
        ('ru', 'Русский'),
        ('fr', 'Français'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    subtitle = models.CharField(max_length=200, blank=True, verbose_name="Qo'shimcha sarlavha")
    authors = models.ManyToManyField(Author, related_name='books', verbose_name="Mualliflar")
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='books',
        verbose_name="Kategoriya"
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        related_name='books',
        verbose_name="Nashriyot"
    )
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    publication_date = models.DateField(verbose_name="Nashr sanasi")
    pages = models.PositiveIntegerField(verbose_name="Sahifalar soni")
    language = models.CharField(
        max_length=2, 
        choices=LANGUAGE_CHOICES, 
        default='uz',
        verbose_name="Til"
    )
    description = models.TextField(blank=True, verbose_name="Tavsifi")
    cover_image = models.ImageField(
        upload_to='books/', 
        blank=True, 
        null=True,
        verbose_name="Muqova rasmi"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        verbose_name="Narxi"
    )
    total_copies = models.PositiveIntegerField(default=1, verbose_name="Jami nusxalar")
    available_copies = models.PositiveIntegerField(default=1, verbose_name="Mavjud nusxalar")
    is_available = models.BooleanField(default=True, verbose_name="Mavjudmi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def is_in_stock(self):
        """Kitob mavjudmi?"""
        return self.available_copies > 0 and self.is_available
    
    @property
    def borrowed_copies(self):
        """Olingan kitoblar soni"""
        return self.total_copies - self.available_copies
    
    def clean(self):
        """Custom validation"""
        from django.core.exceptions import ValidationError
        
        if self.available_copies > self.total_copies:
            raise ValidationError('Mavjud nusxalar jami nusxalardan ko\'p bo\'lishi mumkin emas')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"
        ordering = ['-created_at']

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_number = models.CharField(max_length=20, unique=True, verbose_name="A'zolik raqami")
    phone = models.CharField(max_length=15, verbose_name="Telefon")
    address = models.TextField(verbose_name="Manzil")
    birth_date = models.DateField(verbose_name="Tug'ilgan sana")
    membership_date = models.DateField(auto_now_add=True, verbose_name="A'zo bo'lgan sana")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.membership_number})"
    
    @property
    def age(self):
        """A'zoning yoshi"""
        return date.today().year - self.birth_date.year
    
    @property
    def active_borrows(self):
        """Faol qarzdagi kitoblar soni"""
        return self.borrows.filter(return_date__isnull=True).count()
    
    class Meta:
        verbose_name = "A'zo"
        verbose_name_plural = "A'zolar"
        ordering = ['user__last_name']

class BookBorrow(models.Model):
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='borrows',
        verbose_name="Kitob"
    )
    member = models.ForeignKey(
        Member, 
        on_delete=models.CASCADE, 
        related_name='borrows',
        verbose_name="A'zo"
    )
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name="Olingan sana")
    due_date = models.DateField(verbose_name="Qaytarish sanasi")
    return_date = models.DateTimeField(blank=True, null=True, verbose_name="Qaytarilgan sana")
    fine_amount = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0,
        verbose_name="Jarima miqdori"
    )
    notes = models.TextField(blank=True, verbose_name="Izohlar")
    
    def __str__(self):
        return f"{self.member.user.username} - {self.book.title}"
    
    @property
    def is_overdue(self):
        """Muddati o'tganmi?"""
        if self.return_date:
            return False  # Qaytarilgan
        return date.today() > self.due_date
    
    @property
    def days_overdue(self):
        """Necha kun muddati o'tgan"""
        if not self.is_overdue:
            return 0
        return (date.today() - self.due_date).days
    
    def save(self, *args, **kwargs):
        """Kitob olinganda due_date avtomatik belgilanadi"""
        if not self.due_date:
            self.due_date = date.today() + timedelta(days=14)  # 14 kunlik muddat
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Kitob qarz"
        verbose_name_plural = "Kitob qarzlar"
        ordering = ['-borrow_date']

class BookReview(models.Model):
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name="Kitob"
    )
    member = models.ForeignKey(
        Member, 
        on_delete=models.CASCADE,
        verbose_name="A'zo"
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Reyting"
    )
    comment = models.TextField(blank=True, verbose_name="Sharh")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.book.title} - {self.rating} yulduz"
    
    class Meta:
        verbose_name = "Kitob sharhi"
        verbose_name_plural = "Kitob sharhlari"
        unique_together = ['book', 'member']  # Har bir a'zo bitta kitobga faqat bir marta sharh yoza oladi
        ordering = ['-created_at']
```

### 5-bosqich: Signallar qo'shish

```python
# books/signals.py (yangi fayl yarating)
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Member, BookBorrow, Book
import uuid

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    """Yangi user yaratilganda Member profili ham yaratiladi"""
    if created:
        # Unique membership number yaratish
        membership_number = f"LIB{str(uuid.uuid4().int)[:8]}"
        Member.objects.create(
            user=instance,
            membership_number=membership_number
        )

@receiver(pre_save, sender=BookBorrow)
def update_book_availability(sender, instance, **kwargs):
    """Kitob olingan/qaytarilgan vaqtda mavjudlikni yangilash"""
    if instance.pk:  # Mavjud obyekt yangilanayotgan bo'lsa
        old_instance = BookBorrow.objects.get(pk=instance.pk)
        
        # Kitob qaytarildi
        if not old_instance.return_date and instance.return_date:
            instance.book.available_copies += 1
            instance.book.save()
    else:  # Yangi obyekt yaratilayotgan bo'lsa
        # Kitob olindi
        if instance.book.available_copies > 0:
            instance.book.available_copies -= 1
            instance.book.save()
```

```python
# books/apps.py
from django.apps import AppConfig

class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books'
    
    def ready(self):
        import books.signals  # Signallarni import qilish
```

### 6-bosqich: Admin panelni sozlash

```python
# books/admin.py
from django.contrib import admin
from .models import Author, Category, Publisher, Book, Member, BookBorrow, BookReview

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'birth_date', 'age']
    list_filter = ['birth_date']
    search_fields = ['first_name', 'last_name']
    readonly_fields = ['age']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('first_name', 'last_name', 'photo')
        }),
        ('Biografiya', {
            'fields': ('birth_date', 'death_date', 'biography'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'book_count', 'created_at']
    search_fields = ['name']
    readonly_fields = ['book_count']

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email']
    search_fields = ['name']

class BookBorrowInline(admin.TabularInline):
    model = BookBorrow
    extra = 0
    readonly_fields = ['borrow_date', 'days_overdue']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'publisher', 'available_copies', 'is_in_stock']
    list_filter = ['category', 'publisher', 'language', 'is_available']
    search_fields = ['title', 'isbn']
    filter_horizontal = ['authors']
    readonly_fields = ['borrowed_copies', 'is_in_stock']
    inlines = [BookBorrowInline]
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'subtitle', 'authors', 'category')
        }),
        ('Nashr ma\'lumotlari', {
            'fields': ('publisher', 'isbn', 'publication_date', 'pages', 'language')
        }),
        ('Tavsif va rasm', {
            'fields': ('description', 'cover_image'),
            'classes': ('collapse',)
        }),
        ('Narx va mavjudlik', {
            'fields': ('price', 'total_copies', 'available_copies', 'is_available')
        }),
    )

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'membership_number', 'phone', 'active_borrows', 'is_active']
    list_filter = ['is_active', 'membership_date']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'membership_number']
    readonly_fields = ['membership_date', 'active_borrows', 'age']

@admin.register(BookBorrow)
class BookBorrowAdmin(admin.ModelAdmin):
    list_display = ['member', 'book', 'borrow_date', 'due_date', 'return_date', 'is_overdue']
    list_filter = ['borrow_date', 'due_date', 'return_date']
    search_fields = ['member__user__username', 'book__title']
    readonly_fields = ['borrow_date', 'is_overdue', 'days_overdue']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('member__user', 'book')

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'member__user__username']
```

### 7-bosqich: Migration yaratish va qo'llash

```bash
# Migration fayllarini yaratish
python manage.py makemigrations books

# Migrationlarni qo'llash
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser
```

### 8-bosqich: Test ma'lumotlar yaratish

```python
# books/management/__init__.py (bo'sh fayl yarating)
# books/management/commands/__init__.py (bo'sh fayl yarating)
# books/management/commands/populate_db.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from books.models import Author, Category, Publisher, Book, Member
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with sample data'
    
    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Kategoriyalar yaratish
        categories = [
            {'name': 'Adabiyot', 'description': 'Badiiy adabiyot kitoblari'},
            {'name': 'Texnologiya', 'description': 'IT va texnologiya kitoblari'},
            {'name': 'Tarix', 'description': 'Tarixiy kitoblar'},
            {'name': 'Fan', 'description': 'Ilmiy kitoblar'},
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(**cat_data)
            if created:
                self.stdout.write(f'Category created: {category.name}')
        
        # Mualliflar yaratish
        authors_data = [
            {'first_name': 'Abdulla', 'last_name': 'Qodiriy', 'birth_date': date(1894, 4, 10)},
            {'first_name': 'Cho\'lpon', 'last_name': 'Cho\'lponov', 'birth_date': date(1897, 9, 25)},
            {'first_name': 'Oybek', 'last_name': 'Muso Toshmuhammad o\'g\'li', 'birth_date': date(1905, 1, 10)},
        ]
        
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(**author_data)
            if created:
                self.stdout.write(f'Author created: {author.full_name}')
        
        # Nashriyotlar yaratish
        publishers_data = [
            {'name': 'Sharq', 'address': 'Toshkent sh.'},
            {'name': 'O\'zbekiston', 'address': 'Toshkent sh.'},
            {'name': 'Yangi asr avlodi', 'address': 'Toshkent sh.'},
        ]
        
        for pub_data in publishers_data:
            publisher, created = Publisher.objects.get_or_create(**pub_data)
            if created:
                self.stdout.write(f'Publisher created: {publisher.name}')
        
        # Kitoblar yaratish
        books_data = [
            {
                'title': 'O\'tkan kunlar',
                'isbn': '9785123456789',
                'publication_date': date(2020, 1, 1),
                'pages': 300,
                'price': 25000,
                'total_copies': 5,
                'available_copies': 5,
            },
            {
                'title': 'Django dasturlash',
                'isbn': '9785123456790',
                'publication_date': date(2021, 6, 15),
                'pages': 450,
                'price': 45000,
                'total_copies': 3,
                'available_copies': 3,
            },
        ]
        
        categories = Category.objects.all()
        publishers = Publisher.objects.all()
        authors = Author.objects.all()
        
        for book_data in books_data:
            if not Book.objects.filter(isbn=book_data['isbn']).exists():
                book_data['category'] = random.choice(categories)
                book_data['publisher'] = random.choice(publishers)
                
                book = Book.objects.create(**book_data)
                book.authors.add(random.choice(authors))
                
                self.stdout.write(f'Book created: {book.title}')
        
        # Test userlar yaratish
        for i in range(1, 4):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f'user{i}@example.com',
                    password='testpass123',
                    first_name=f'Test{i}',
                    last_name='User'
                )
                
                # Member profili avtomatik yaratiladi (signals orqali)
                member = Member.objects.get(user=user)
                member.phone = f'+998901234567{i}'
                member.address = f'Toshkent sh., {i}-manzil'
                member.birth_date = date(1990 + i, i, 15)
                member.save()
                
                self.stdout.write(f'User created: {user.username}')
        
        self.stdout.write(self.style.SUCCESS('Successfully populated database!'))
```

```bash
# Test ma'lumotlarni yaratish
python manage.py populate_db
```

### 9-bosqich: Oddiy view yaratish

```python
# books/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Book, Category, Author, BookBorrow, Member

def home(request):
    """Bosh sahifa"""
    books = Book.objects.filter(is_available=True)[:6]
    categories = Category.objects.all()
    
    context = {
        'books': books,
        'categories': categories,
    }
    return render(request, 'books/home.html', context)

def book_list(request):
    """Kitoblar ro'yxati"""
    books = Book.objects.filter(is_available=True).select_related('category', 'publisher')
    
    # Kategoriya bo'yicha filterlash
    category_id = request.GET.get('category')
    if category_id:
        books = books.filter(category_id=category_id)
    
    # Qidiruv
    search = request.GET.get('search')
    if search:
        books = books.filter(title__icontains=search)
    
    categories = Category.objects.all()
    
    context = {
        'books': books,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'search_query': search or '',
    }
    return render(request, 'books/book_list.html', context)

def book_detail(request, book_id):
    """Kitob tafsilotlari"""
    book = get_object_or_404(
        Book.objects.select_related('category', 'publisher').prefetch_related('authors', 'reviews'),
        id=book_id,
        is_available=True
    )
    
    # O'rtacha reyting hisoblash
    reviews = book.reviews.all()
    average_rating = sum([r.rating for r in reviews]) / len(reviews) if reviews else 0
    
    context = {
        'book': book,
        'average_rating': round(average_rating, 1),
        'review_count': len(reviews),
    }
    return render(request, 'books/book_detail.html', context)

@login_required
def my_borrows(request):
    """Mening olingan kitoblarim"""
    try:
        member = request.user.member
        borrows = member.borrows.filter(return_date__isnull=True).select_related('book')
        
        context = {
            'borrows': borrows,
            'member': member,
        }
        return render(request, 'books/my_borrows.html', context)
    except Member.DoesNotExist:
        return render(request, 'books/no_member.html')
```

### 10-bosqich: Template yaratish

```html
<!-- books/templates/books/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Kutubxona tizimi{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'home' %}">Kutubxona</a>
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <a class="nav-link" href="{% url 'my_borrows' %}">Mening kitoblarim</a>
                    <a class="nav-link" href="{% url 'admin:index' %}">Admin</a>
                {% endif %}
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {% block content %}
        {% endblock %}
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

```html
<!-- books/templates/books/home.html -->
{% extends 'books/base.html' %}

{% block content %}
<div class="row">
    <div class="col-md-12">
        <h1>Kutubxona tizimiga xush kelibsiz!</h1>
        
        <div class="row mt-4">
            <div class="col-md-8">
                <h3>Yangi kitoblar</h3>
                <div class="row">
                    {% for book in books %}
                    <div class="col-md-4 mb-3">
                        <div class="card">
                            {% if book.cover_image %}
                            <img src="{{ book.cover_image.url }}" class="card-img-top" style="height: 200px; object-fit: cover;">
                            {% endif %}
                            <div class="card-body">
                                <h5 class="card-title">{{ book.title }}</h5>
                                <p class="card-text">{{ book.description|truncatewords:20 }}</p>
                                <a href="{% url 'book_detail' book.id %}" class="btn btn-primary">Batafsil</a>
                            </div>
                        </div>
                    </div>
                    {% empty %}
                    <p>Hozircha kitoblar yo'q.</p>
                    {% endfor %}
                </div>
            </div>
            
            <div class="col-md-4">
                <h3>Kategoriyalar</h3>
                <div class="list-group">
                    {% for category in categories %}
                    <a href="{% url 'book_list' %}?category={{ category.id }}" 
                       class="list-group-item list-group-item-action">
                        {{ category.name }} ({{ category.book_count }})
                    </a>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 11-bosqich: URL'larni to'ldirish

```python
# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('my-borrows/', views.my_borrows, name='my_borrows'),
]
```

### 12-bosqich: Django shell orqali ma'lumotlar bilan ishlash

```python
# Terminal da quyidagi buyruqni yozing:
# python manage.py shell

# ORM bilan ishlash misollari
from books.models import *
from django.contrib.auth.models import User

# 1. Barcha kitoblarni ko'rish
books = Book.objects.all()
for book in books:
    print(f"{book.title} - {book.available_copies} mavjud")

# 2. Kategoriya bo'yicha kitoblar
tech_books = Book.objects.filter(category__name="Texnologiya")

# 3. Muallif bo'yicha kitoblar
author = Author.objects.get(first_name="Abdulla", last_name="Qodiriy")
author_books = author.books.all()

# 4. Kitob qarz berish
user = User.objects.get(username="user1")
member = user.member
book = Book.objects.first()

borrow = BookBorrow.objects.create(
    book=book,
    member=member
)
print(f"Kitob olindi: {borrow}")

# 5. Kitobni qaytarish
borrow.return_date = timezone.now()
borrow.save()

# 6. Statistika
total_books = Book.objects.count()
available_books = Book.objects.filter(available_copies__gt=0).count()
active_borrows = BookBorrow.objects.filter(return_date__isnull=True).count()

print(f"Jami kitoblar: {total_books}")
print(f"Mavjud kitoblar: {available_books}")
print(f"Faol qarzlar: {active_borrows}")
```

## Qo'shimcha funksiyalar

### 13-bosqich: Custom Manager yaratish

```python
# books/models.py ga qo'shing
class AvailableBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True, available_copies__gt=0)

class Book(models.Model):
    # ... mavjud maydonlar ...
    
    objects = models.Manager()  # Default manager
    available = AvailableBookManager()  # Custom manager
    
    # ... qolgan kod ...
```

### 14-bosqich: Custom Form yaratish

```python
# books/forms.py (yangi fayl)
from django import forms
from .models import BookReview, BookBorrow

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} yulduz") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class BookSearchForm(forms.Form):
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Kitob qidirish...',
            'class': 'form-control'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Barcha kategoriyalar",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
```

## Xulosa va tavsiyalar

### Best Practices:
1. **Model nomlarini to'g'ri tanlang** - singular shaklda
2. **Related_name ishlatilng** - teskari bog'lanishlar uchun
3. **Meta klassidan foydalaning** - ordering, verbose_name uchun
4. **Custom metodlar yozing** - takroriy logikani modelga joylashtiring
5. **Signallardan foydalaning** - avtomatik harakatlar uchun
6. **Admin panelni sozlang** - qulay boshqaruv uchun
7. **Validatsiya qo'shing** - ma'lumotlar to'g'riligini ta'minlash uchun

### Keyingi qadamlar:
1. REST API yaratish (Django REST Framework)
2. Caching qo'shish (Redis)
3. Testing yozish
4. Frontend (React/Vue) bilan birlashtirish
5. Production ga deploy qilish

Bu amaliyot orqali siz Django modellarini to'liq tushunib oldingiz va real loyihada qo'llay olasiz!