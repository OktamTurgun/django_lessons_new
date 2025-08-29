# Django Lesson 14: Loyihaning Admin Qismi bilan Ishlash

## Maqsad
Django admin panelini sozlash, foydalanuvchilarni boshqarish, modellarni admin panelida ko'rsatish va sozlash usullarini o'rganish.

## Nazariy Qism

### Django Admin Nima?
Django admin - bu Django frameworkining eng kuchli xususiyatlaridan biri bo'lib, avtomatik ravishda yaratilgan web-based admin interfeysidir. U orqali ma'lumotlar bazasidagi ma'lumotlarni osongina boshqarish mumkin.

### Django Admin Afzalliklari:
- Avtomatik interfeys yaratadi
- Ma'lumotlarni CRUD operatsiyalarini osonlashtiradi
- Foydalanuvchi huquqlarini boshqaradi
- Tez va oson sozlanadi

## 1-Bosqich: Superuser Yaratish

Admin panelga kirish uchun avval superuser yaratish kerak:

```bash
# Terminal yoki Command Prompt da
python manage.py createsuperuser
```

**Izoh:** Bu buyruq sizdan username, email va parol so'raydi. Ularni kiritganingizdan so'ng superuser yaratiladi.

```bash
Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

## 2-Bosqich: Admin Panel Sozlamalari

### settings.py faylida kerakli sozlamalar:

```python
# myproject/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',  # Bu albatta bo'lishi kerak
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',  # Sizning appingiz
]

# Admin paneli uchun til sozlamasi (ixtiyoriy)
LANGUAGE_CODE = 'uz-uz'  # O'zbek tili uchun
# yoki
LANGUAGE_CODE = 'en-us'  # Ingliz tili uchun

# Vaqt mintaqasi
TIME_ZONE = 'Asia/Tashkent'
```

### urls.py faylida admin yo'nalishini qo'shish:

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneli yo'nalishi
    path('', include('myapp.urls')),
]
```

## 3-Bosqich: Modellarni Admin Panelida Ro'yxatdan O'tkazish

### Oddiy model yaratish:

```python
# myapp/models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('published', 'Nashr qilingan'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Postlar"
        ordering = ['-created_at']
```

### Admin.py faylida modellarni ro'yxatdan o'tkazish:

```python
# myapp/admin.py
from django.contrib import admin
from .models import Category, Post

# Oddiy ro'yxatdan o'tkazish
admin.site.register(Category)
admin.site.register(Post)
```

## 4-Bosqich: Admin Panelini Sozlash va Mukammalashtirish

### Admin klasslarini yaratish:

```python
# myapp/admin.py
from django.contrib import admin
from .models import Category, Post

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Ro'yxatda ko'rsatiladigan maydonlar
    list_display = ['name', 'description', 'created_at']
    
    # Qidiruv imkoniyati
    search_fields = ['name']
    
    # Filtr paneli
    list_filter = ['created_at']
    
    # Sahifalash
    list_per_page = 20
    
    # Tahrirlash formasi
    fields = ['name', 'description']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content']
    list_per_page = 25
    
    # Tahrirlash uchun maydonlarni guruhlash
    fieldsets = (
        ('Asosiy Ma\'lumotlar', {
            'fields': ('title', 'content', 'author')
        }),
        ('Qo\'shimcha Ma\'lumotlar', {
            'fields': ('category', 'status'),
            'classes': ('collapse',)  # Yopiq holda ko'rsatish
        }),
    )
    
    # Dropdown o'rniga radio button
    radio_fields = {'status': admin.HORIZONTAL}
    
    # Raw ID widgets (katta ma'lumotlar uchun)
    raw_id_fields = ['author']
    
    # Readonly maydonlar
    readonly_fields = ['created_at', 'updated_at']
    
    # Inline editing (bog'langan modellar uchun)
    # filter_horizontal = ['tags']  # Agar tags modeli bo'lsa
```

## 5-Bosqich: Inline Admin

Bog'langan modellarni bitta sahifada tahrirlash uchun:

```python
# myapp/models.py - qo'shimcha model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.author} - {self.post.title}"

# myapp/admin.py - inline qo'shish
class CommentInline(admin.TabularInline):  # yoki admin.StackedInline
    model = Comment
    extra = 1  # Qo'shimcha bo'sh form
    readonly_fields = ['created_at']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]  # Bu qatorni qo'shish
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    # ... boshqa sozlamalar
```

## 6-Bosqich: Admin Panelini Shaxsiylashtirish

### Admin saytining nomini o'zgartirish:

```python
# myproject/urls.py yoki myapp/admin.py
from django.contrib import admin

# Admin paneli sarlavhalarini o'zgartirish
admin.site.site_header = "Mening Saytim Admin Paneli"
admin.site.site_title = "Mening Saytim Admin"
admin.site.index_title = "Boshqaruv Paneli"
```

### Custom admin actions yaratish:

```python
# myapp/admin.py
from django.contrib import admin
from django.http import HttpResponse

def make_published(modeladmin, request, queryset):
    queryset.update(status='published')
    
make_published.short_description = "Tanlangan postlarni nashr qilish"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    actions = [make_published]  # Custom action qo'shish
    # ... boshqa sozlamalar
```

## 7-Bosqich: Foydalanuvchi Huquqlarini Boshqarish

### Staff va Superuser farqi:
- **Superuser**: Barcha huquqlarga ega
- **Staff**: Admin panelga kira oladi, lekin faqat belgilangan huquqlarga ega

### Guruh va huquqlar yaratish:

```python
# Django shell orqali
python manage.py shell

>>> from django.contrib.auth.models import User, Group, Permission
>>> from django.contrib.contenttypes.models import ContentType
>>> from myapp.models import Post

# Guruh yaratish
>>> editors_group = Group.objects.create(name='Editors')

# Huquqlar berish
>>> content_type = ContentType.objects.get_for_model(Post)
>>> permission = Permission.objects.get(
...     codename='add_post',
...     content_type=content_type,
... )
>>> editors_group.permissions.add(permission)

# Foydalanuvchini guruhga qo'shish
>>> user = User.objects.get(username='editor_user')
>>> user.groups.add(editors_group)
```

## 8-Bosqich: Advanced Admin Customization

### Custom admin form yaratish:

```python
# myapp/forms.py
from django import forms
from .models import Post

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError("Sarlavha kamida 5 ta belgidan iborat bo'lishi kerak")
        return title

# myapp/admin.py
from .forms import PostAdminForm

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm  # Custom form ishlatish
    # ... boshqa sozlamalar
```

### List display bilan custom metodlar:

```python
# myapp/models.py
class Post(models.Model):
    # ... boshqa maydonlar
    
    def short_description(self):
        return self.content[:100] + "..." if len(self.content) > 100 else self.content
    short_description.short_description = "Qisqa tavsif"

# myapp/admin.py
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'short_description', 'status', 'created_at']
    # ...
```

## 9-Bosqich: Admin Panel Performance Optimization

### Database query optimizatsiyasi:

```python
# myapp/admin.py
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    
    # N+1 query muammosini hal qilish
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('author', 'category')
    
    # Prefetch related objects
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('comments')
```

## Xulosa

Django admin paneli - bu kuchli vosita bo'lib, tez va samarali ma'lumotlar boshqaruvi imkoniyatini beradi. To'g'ri sozlanganda, u juda professional va foydalanish uchun qulay interfeys yaratadi.

**Keyingi Dars:**
Keyingi darsda Queryset va model manager