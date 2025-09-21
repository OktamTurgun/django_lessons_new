# Dars 32: Foydalanuvchi profilini yaratish

## Dars maqsadi
Bu darsda Django'da foydalanuvchi profili yaratish, uni ko'rsatish va tahrirlash funksiyalarini o'rganamiz. Foydalanuvchi o'z shaxsiy ma'lumotlarini ko'ra olish va o'zgartira olish imkoniyatini beramiz.

## Nazariy qism

### Foydalanuvchi profili nima?
Foydalanuvchi profili - bu Django'ning standart User modeliga qo'shimcha ma'lumotlar qo'shish usuli. Profil orqali foydalanuvchi haqida qo'shimcha ma'lumotlarni saqlash mumkin:
- Profil rasmi
- Bio ma'lumotlari  
- Telefon raqami
- Manzil
- Ijtimoiy tarmoq havolalari va boshqalar

### Profile yaratishning usullari:
1. **OneToOneField** - eng keng tarqalgan usul
2. **User modelini kengaytirish** - murakkab hollarda
3. **Custom User modeli** - loyiha boshida

Biz OneToOneField usulidan foydalanamiz.

## 1-bosqich: Profile modelini yaratish

Avval `users` deb yangi app yaratamiz:

```bash
python manage.py startapp users
```

`settings.py`ga qo'shamiz:

```python
# config/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news.apps.NewsConfig',
    'users.apps.UsersConfig',  # Yangi app
]
```

`users/models.py` faylini yaratamiz:

```python
# users/models.py
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, verbose_name="Bio")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Telefon")
    location = models.CharField(max_length=100, blank=True, verbose_name="Manzil")
    website = models.URLField(blank=True, verbose_name="Veb-sayt")
    image = models.ImageField(
        default='profile_pics/default.jpg', 
        upload_to='profile_pics',
        verbose_name="Profil rasmi"
    )
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"

    def __str__(self):
        return f"{self.user.username} profili"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Rasmni kichraytiramiz
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
```

**Kod tushuntirishi:**
- `OneToOneField` - har bir User uchun bitta Profile
- `PIL` - rasm o'lchamini boshqarish uchun
- `save` metodi - rasm yuklanganda uni avtomatik kichraytiradi

## 2-bosqich: Pillow kutubxonasini o'rnatish

Rasmlar bilan ishlash uchun Pillow kerak:

```bash
pip install Pillow
```

## 3-bosqich: Media fayllar uchun sozlamalar

`settings.py`ga media sozlamalarini qo'shamiz:

```python
# config/settings.py
import os

# Media files (rasmlar)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Asosiy `urls.py`ni o'zgartiramiz:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('users/', include('users.urls')),
]

# Media fayllar uchun
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 4-bosqich: Default profil rasmini qo'shish

`media/profile_pics/` papka yaratib, `default.jpg` rasmini qo'yamiz.

## 5-bosqich: Migration qilish

```bash
python manage.py makemigrations
python manage.py migrate
```

## 6-bosqich: Signal orqali avtomatik profil yaratish

Har yangi foydalanuvchi ro'yxatdan o'tganda avtomatik profil yaratish uchun `users/signals.py` yaratamiz:

```python
# users/signals.py
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```

`users/apps.py`da signalni ulash:

```python
# users/apps.py
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self):
        import users.signals
```

**Signal tushuntirishi:**
- Yangi User yaratilganda avtomatik Profile yaratiladi
- User saqlanganida Profile ham saqlanadi

## 7-bosqich: Views yaratish

`users/views.py` faylini yaratamiz:

```python
# users/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import Profile
from .forms import ProfileUpdateForm, UserUpdateForm

@login_required
def profile(request):
    """Foydalanuvchi profili"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        # Agar profil yo'q bo'lsa, yaratamiz
        profile = Profile.objects.create(user=request.user)
    
    context = {
        'profile': profile
    }
    return render(request, 'users/profile.html', context)

@login_required 
def profile_update(request):
    """Profilni tahrirlash"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Profilingiz muvaffaqiyatli yangilandi!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile_update.html', context)

def user_profile(request, username):
    """Boshqa foydalanuvchi profilini ko'rish"""
    user = get_object_or_404(User, username=username)
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)
    
    context = {
        'profile_user': user,
        'profile': profile
    }
    return render(request, 'users/user_profile.html', context)
```

## 8-bosqich: Forms yaratish

`users/forms.py` faylini yaratamiz:

```python
# users/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'phone', 'location', 'website', 'image']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'O\'zingiz haqingizda qisqacha...'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Toshkent, O\'zbekiston'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file'
            })
        }
```

## 9-bosqich: URLs yaratish

`users/urls.py` faylini yaratamiz:

```python
# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
]
```

## 10-bosqich: Templates yaratish

`users/templates/users/` papka yaratib, quyidagi fayllarni yaratamiz:

### profile.html
```html
<!-- users/templates/users/profile.html -->
{% extends 'base.html' %}

{% block title %}Mening profilim{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    <img src="{{ profile.image.url }}" 
                         alt="Profil rasmi" 
                         class="rounded-circle mb-3"
                         width="150" height="150"
                         style="object-fit: cover;">
                    <h5 class="card-title">{{ user.get_full_name|default:user.username }}</h5>
                    {% if user.email %}
                        <p class="text-muted">{{ user.email }}</p>
                    {% endif %}
                    
                    <a href="{% url 'users:profile_update' %}" 
                       class="btn btn-primary btn-sm">Profilni tahrirlash</a>
                </div>
            </div>
        </div>
        
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h5>Profil ma'lumotlari</h5>
                </div>
                <div class="card-body">
                    {% if profile.bio %}
                        <div class="mb-3">
                            <strong>Bio:</strong>
                            <p>{{ profile.bio }}</p>
                        </div>
                    {% endif %}
                    
                    <div class="row">
                        {% if profile.birth_date %}
                        <div class="col-sm-6">
                            <strong>Tug'ilgan sana:</strong>
                            <p>{{ profile.birth_date|date:"d.m.Y" }}</p>
                        </div>
                        {% endif %}
                        
                        {% if profile.phone %}
                        <div class="col-sm-6">
                            <strong>Telefon:</strong>
                            <p>{{ profile.phone }}</p>
                        </div>
                        {% endif %}
                        
                        {% if profile.location %}
                        <div class="col-sm-6">
                            <strong>Manzil:</strong>
                            <p>{{ profile.location }}</p>
                        </div>
                        {% endif %}
                        
                        {% if profile.website %}
                        <div class="col-sm-6">
                            <strong>Veb-sayt:</strong>
                            <p><a href="{{ profile.website }}" target="_blank">{{ profile.website }}</a></p>
                        </div>
                        {% endif %}
                    </div>
                    
                    <small class="text-muted">
                        Ro'yxatdan o'tgan: {{ user.date_joined|date:"d.m.Y" }}
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### profile_update.html
```html
<!-- users/templates/users/profile_update.html -->
{% extends 'base.html' %}

{% block title %}Profilni tahrirlash{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h5>Profilni tahrirlash</h5>
                </div>
                <div class="card-body">
                    <form method="POST" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <!-- Foydalanuvchi ma'lumotlari -->
                        <fieldset class="mb-4">
                            <legend class="border-bottom pb-2 mb-3">Foydalanuvchi ma'lumotlari</legend>
                            
                            <div class="row">
                                <div class="col-sm-6 mb-3">
                                    <label for="{{ u_form.username.id_for_label }}" class="form-label">Username</label>
                                    {{ u_form.username }}
                                    {% if u_form.username.errors %}
                                        <div class="text-danger">
                                            {{ u_form.username.errors }}
                                        </div>
                                    {% endif %}
                                </div>
                                
                                <div class="col-sm-6 mb-3">
                                    <label for="{{ u_form.email.id_for_label }}" class="form-label">Email</label>
                                    {{ u_form.email }}
                                    {% if u_form.email.errors %}
                                        <div class="text-danger">
                                            {{ u_form.email.errors }}
                                        </div>
                                    {% endif %}
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-sm-6 mb-3">
                                    <label for="{{ u_form.first_name.id_for_label }}" class="form-label">Ism</label>
                                    {{ u_form.first_name }}
                                </div>
                                
                                <div class="col-sm-6 mb-3">
                                    <label for="{{ u_form.last_name.id_for_label }}" class="form-label">Familiya</label>
                                    {{ u_form.last_name }}
                                </div>
                            </div>
                        </fieldset>
                        
                        <!-- Profil ma'lumotlari -->
                        <fieldset class="mb-4">
                            <legend class="border-bottom pb-2 mb-3">Profil ma'lumotlari</legend>
                            
                            <div class="mb-3">
                                <label for="{{ p_form.image.id_for_label }}" class="form-label">Profil rasmi</label>
                                {{ p_form.image }}
                                {% if p_form.image.errors %}
                                    <div class="text-danger">
                                        {{ p_form.image.errors }}
                                    </div>
                                {% endif %}
                            </div>
                            
                            <div class="mb-3">
                                <label for="{{ p_form.bio.id_for_label }}" class="form-label">Bio</label>
                                {{ p_form.bio }}
                                {% if p_form.bio.errors %}
                                    <div class="text-danger">
                                        {{ p_form.bio.errors }}
                                    </div>
                                {% endif %}
                            </div>
                            
                            <div class="row">
                                <div class="col-sm-6 mb-3">
                                    <label for="{{ p_form.birth_date.id_for_label }}" class="form-label">Tug'ilgan sana</label>
                                    {{ p_form.birth_date }}
                                </div>
                                
                                <div class="col-sm-6 mb-3">
                                    <label for="{{ p_form.phone.id_for_label }}" class="form-label">Telefon</label>
                                    {{ p_form.phone }}
                                </div>
                            </div>
                            
                            <div class="row">
                                <div class="col-sm-6 mb-3">
                                    <label for="{{ p_form.location.id_for_label }}" class="form-label">Manzil</label>
                                    {{ p_form.location }}
                                </div>
                                
                                <div class="col-sm-6 mb-3">
                                    <label for="{{ p_form.website.id_for_label }}" class="form-label">Veb-sayt</label>
                                    {{ p_form.website }}
                                </div>
                            </div>
                        </fieldset>
                        
                        <div class="text-center">
                            <button type="submit" class="btn btn-primary">Saqlash</button>
                            <a href="{% url 'users:profile' %}" class="btn btn-secondary">Bekor qilish</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 11-bosqich: Admin qismini sozlash

`users/admin.py` faylini o'zgartiramiz:

```python
# users/admin.py
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'location', 'created']
    list_filter = ['created', 'updated']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created', 'updated']
```

## 12-bosqich: Base template'da profilga havola qo'shish

`base.html` fayliga profil havolasini qo'shamiz:

```html
<!-- base.html'da navbar qismida -->
{% if user.is_authenticated %}
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" role="button" 
           data-bs-toggle="dropdown">
            {{ user.username }}
        </a>
        <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="{% url 'users:profile' %}">Mening profilim</a></li>
            <li><a class="dropdown-item" href="{% url 'users:profile_update' %}">Profilni tahrirlash</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="{% url 'account_logout' %}">Chiqish</a></li>
        </ul>
    </li>
{% endif %}
```

## Xulosa

Bu darsda biz foydalanuvchi profilini yaratishni o'rgandik:

**O'rgangan narsalar:**
- Profile modeli yaratish (OneToOneField)
- Signal orqali avtomatik profil yaratish
- Media fayllar bilan ishlash
- Profil rasmini yuklash va o'lchamini o'zgartirish
- Forms yaratish va validatsiya
- Template'larda profil ma'lumotlarini ko'rsatish

**Keyingi darsda:**
33-darsda Foydalanuvchi parolini o'zgartirish.

## Maslahatlar va Best Practices

1. **Rasm optimizatsiyasi:** Har doim rasm o'lchamini tekshiring
2. **Validatsiya:** Form ma'lumotlarini tekshirish
3. **Signal ishlatish:** Avtomatik profil yaratish uchun
4. **Media sozlamalari:** Production'da AWS S3 ishlatish tavsiya etiladi
5. **Xavfsizlik:** Faqat login qilgan foydalanuvchilar profil tahrirlashi mumkin