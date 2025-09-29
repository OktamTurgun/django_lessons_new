# Lesson 40: Profilda rasm va boshqa ma'lumotlarni chiqarish

## Kirish

Oldingi darsda biz foydalanuvchi profilini yaratdik va tahrirlash funksiyasini qo'shdik. Endi esa profil sahifasida foydalanuvchi rasmi va boshqa ma'lumotlarni to'liq ko'rsatishni o'rganamiz. Bu darsda quyidagilarni amalga oshiramiz:

- Profil sahifasida foydalanuvchi rasmini ko'rsatish
- Rasm yuklanmagan bo'lsa, standart rasm ko'rsatish
- Foydalanuvchi ma'lumotlarini chiroyli tarzda joylashtirish
- Media fayllar bilan ishlashni sozlash

## Nazariy qism

### Media fayllar nima?

Django'da ikki xil statik fayllar mavjud:
- **Static fayllar** - CSS, JavaScript, ikonkalar (development vaqtida o'zgarmaydigan fayllar)
- **Media fayllar** - Foydalanuvchilar yuklagan rasmlar, dokumentlar, videolar

Media fayllar foydalanuvchilar tomonidan yuklanadi va ular dinamik ravishda o'zgarishi mumkin.

### MEDIA_URL va MEDIA_ROOT

Django'da media fayllar bilan ishlash uchun ikkita muhim sozlama kerak:

```python
# settings.py

# Media fayllarning URL manzili
MEDIA_URL = '/media/'

# Media fayllar saqlanadigan joyning to'liq yo'li
MEDIA_ROOT = BASE_DIR / 'media'
```

**Tushuntirish:**
- `MEDIA_URL` - Brauzerda rasmlarni ko'rsatish uchun URL prefiksi
- `MEDIA_ROOT` - Serverda rasmlar saqlanadigan papka yo'li

## Amaliy qism

### 1-qadam: settings.py faylini sozlash

Avval loyihamizning `config/settings.py` fayliga media sozlamalarini qo'shamiz:

```python
# config/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ... boshqa sozlamalar ...

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files (User uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Tushuntirish:**
- `os` modulini import qildik (kerak bo'lishi mumkin)
- `MEDIA_URL = '/media/'` - barcha media fayllar `/media/` URL'i orqali ochiladi
- `MEDIA_ROOT = BASE_DIR / 'media'` - loyiha ildiz papkasida `media` papkasini yaratamiz

### 2-qadam: URL'larni sozlash

Development (ishlab chiqish) rejimida media fayllarni ko'rsatish uchun asosiy `urls.py` faylini o'zgartiramiz:

```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('news.urls')),
]

# Development rejimida media fayllarni xizmat qilish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Tushuntirish:**
- `django.conf.urls.static` dan `static` funksiyasini import qildik
- `settings.DEBUG` - faqat development rejimida ishlaydi
- `static()` funksiyasi media fayllarni URL orqali ochish imkonini beradi
- Production rejimida media fayllar web-server (Nginx, Apache) orqali xizmat qilinadi

### 3-qadam: Profile modelini tekshirish

Oldingi darsda yaratgan `Profile` modelimizda rasm maydoni mavjud ekanligini tekshiramiz:

```python
# accounts/models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} profili"
```

**Tushuntirish:**
- `photo = models.ImageField()` - rasm yuklash uchun maydon
- `upload_to='users/'` - rasmlar `media/users/` papkasiga yuklanadi
- `blank=True, null=True` - rasm majburiy emas

### 4-qadam: Standart rasm tayyorlash

Agar foydalanuvchi rasm yuklamagan bo'lsa, standart rasm ko'rsatish uchun:

1. `static/images/` papkasida `default-user.png` yoki `no-avatar.png` rasmini joylashtiring
2. Yoki internetdan bepul avatar rasmini yuklab oling

Rasm hajmi: taxminan 200x200 piksel yoki 300x300 piksel

### 5-qadam: Profile sahifasini yaratish

Endi profil sahifasini yaratamiz. Avval view'ni yozamiz:

```python
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm

@login_required
def profile_view(request):
    """Foydalanuvchi profil sahifasi"""
    # Profilni olish yoki yaratish
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    """Profilni tahrirlash sahifasi"""
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES,  # Rasm yuklash uchun
            instance=profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_edit.html', context)
```

**Tushuntirish:**
- `profile_view` - profilni ko'rsatish uchun
- `profile_edit` - profilni tahrirlash uchun
- `request.FILES` - yuklangan fayllarni qabul qilish uchun kerak
- `get_or_create()` - profil yo'q bo'lsa, yangi yaratadi

### 6-qadam: URL'larni sozlash

```python
# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('password-change/', views.password_change, name='password_change'),
]
```

### 7-qadam: Profile sahifasi template'ini yaratish

```html
<!-- templates/accounts/profile.html -->

{% extends 'base.html' %}
{% load static %}

{% block title %}{{ user.username }} - Profil{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-4">
            <!-- Profil rasmi -->
            <div class="card">
                <div class="card-body text-center">
                    {% if profile.photo %}
                        <img src="{{ profile.photo.url }}" 
                             alt="{{ user.username }}" 
                             class="img-fluid rounded-circle mb-3"
                             style="width: 200px; height: 200px; object-fit: cover;">
                    {% else %}
                        <img src="{% static 'images/default-user.png' %}" 
                             alt="Default avatar" 
                             class="img-fluid rounded-circle mb-3"
                             style="width: 200px; height: 200px; object-fit: cover;">
                    {% endif %}
                    
                    <h4>{{ user.get_full_name|default:user.username }}</h4>
                    <p class="text-muted">@{{ user.username }}</p>
                    
                    <a href="{% url 'profile_edit' %}" class="btn btn-primary btn-block">
                        <i class="fas fa-edit"></i> Profilni tahrirlash
                    </a>
                </div>
            </div>
        </div>
        
        <div class="col-md-8">
            <!-- Profil ma'lumotlari -->
            <div class="card">
                <div class="card-header">
                    <h5><i class="fas fa-user"></i> Profil ma'lumotlari</h5>
                </div>
                <div class="card-body">
                    <table class="table table-borderless">
                        <tbody>
                            <tr>
                                <th style="width: 200px;">Ism:</th>
                                <td>{{ user.first_name|default:"Kiritilmagan" }}</td>
                            </tr>
                            <tr>
                                <th>Familiya:</th>
                                <td>{{ user.last_name|default:"Kiritilmagan" }}</td>
                            </tr>
                            <tr>
                                <th>Email:</th>
                                <td>{{ user.email|default:"Kiritilmagan" }}</td>
                            </tr>
                            <tr>
                                <th>Tug'ilgan sana:</th>
                                <td>{{ profile.date_of_birth|date:"d.m.Y"|default:"Kiritilmagan" }}</td>
                            </tr>
                            <tr>
                                <th>Bio:</th>
                                <td>{{ profile.bio|default:"Kiritilmagan"|linebreaks }}</td>
                            </tr>
                            <tr>
                                <th>Ro'yxatdan o'tgan:</th>
                                <td>{{ user.date_joined|date:"d.m.Y H:i" }}</td>
                            </tr>
                            <tr>
                                <th>Oxirgi kirish:</th>
                                <td>{{ user.last_login|date:"d.m.Y H:i" }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Parolni o'zgartirish -->
            <div class="card mt-3">
                <div class="card-header">
                    <h5><i class="fas fa-lock"></i> Xavfsizlik</h5>
                </div>
                <div class="card-body">
                    <a href="{% url 'password_change' %}" class="btn btn-warning">
                        <i class="fas fa-key"></i> Parolni o'zgartirish
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**Tushuntirish:**
- `{% if profile.photo %}` - rasm mavjudligini tekshirish
- `{{ profile.photo.url }}` - rasmning URL manzili
- `{% static 'images/default-user.png' %}` - standart rasm
- `rounded-circle` - rasmni dumaloq qilish (Bootstrap)
- `object-fit: cover` - rasmni to'g'ri o'lchamda ko'rsatish
- `|default:"Kiritilmagan"` - bo'sh bo'lsa, matn ko'rsatish
- `|linebreaks` - bio'dagi satr ko'chirishlarni saqlab qolish

### 8-qadam: Profilni tahrirlash template'ini yaratish

```html
<!-- templates/accounts/profile_edit.html -->

{% extends 'base.html' %}
{% load static %}

{% block title %}Profilni tahrirlash{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4><i class="fas fa-edit"></i> Profilni tahrirlash</h4>
                </div>
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <h5 class="mb-3">Foydalanuvchi ma'lumotlari</h5>
                        
                        <!-- Username -->
                        <div class="form-group">
                            <label>{{ user_form.username.label }}</label>
                            {{ user_form.username }}
                            {% if user_form.username.errors %}
                                <div class="text-danger">
                                    {{ user_form.username.errors }}
                                </div>
                            {% endif %}
                        </div>
                        
                        <!-- First name -->
                        <div class="form-group">
                            <label>{{ user_form.first_name.label }}</label>
                            {{ user_form.first_name }}
                        </div>
                        
                        <!-- Last name -->
                        <div class="form-group">
                            <label>{{ user_form.last_name.label }}</label>
                            {{ user_form.last_name }}
                        </div>
                        
                        <!-- Email -->
                        <div class="form-group">
                            <label>{{ user_form.email.label }}</label>
                            {{ user_form.email }}
                        </div>
                        
                        <hr class="my-4">
                        
                        <h5 class="mb-3">Profil ma'lumotlari</h5>
                        
                        <!-- Joriy rasm -->
                        {% if profile_form.instance.photo %}
                        <div class="form-group">
                            <label>Joriy rasm:</label><br>
                            <img src="{{ profile_form.instance.photo.url }}" 
                                 alt="Profil rasmi" 
                                 class="img-thumbnail mb-2"
                                 style="max-width: 200px;">
                        </div>
                        {% endif %}
                        
                        <!-- Yangi rasm yuklash -->
                        <div class="form-group">
                            <label>{{ profile_form.photo.label }}</label>
                            {{ profile_form.photo }}
                            <small class="form-text text-muted">
                                JPG, PNG formatida, maksimal 5MB
                            </small>
                            {% if profile_form.photo.errors %}
                                <div class="text-danger">
                                    {{ profile_form.photo.errors }}
                                </div>
                            {% endif %}
                        </div>
                        
                        <!-- Bio -->
                        <div class="form-group">
                            <label>{{ profile_form.bio.label }}</label>
                            {{ profile_form.bio }}
                            <small class="form-text text-muted">
                                O'zingiz haqingizda qisqacha ma'lumot
                            </small>
                        </div>
                        
                        <!-- Tug'ilgan sana -->
                        <div class="form-group">
                            <label>{{ profile_form.date_of_birth.label }}</label>
                            {{ profile_form.date_of_birth }}
                            <small class="form-text text-muted">
                                Format: YYYY-MM-DD (masalan: 1990-01-15)
                            </small>
                        </div>
                        
                        <hr class="my-4">
                        
                        <!-- Tugmalar -->
                        <div class="form-group">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Saqlash
                            </button>
                            <a href="{% url 'profile' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Bekor qilish
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .form-control, .form-control-file {
        margin-bottom: 10px;
    }
</style>
{% endblock %}
```

**Tushuntirish:**
- `enctype="multipart/form-data"` - fayllarni yuklash uchun MAJBURIY
- `{{ profile_form.instance.photo }}` - joriy rasmga murojaat
- `img-thumbnail` - rasmni chiroyli ko'rsatish (Bootstrap)

### 9-qadam: Forms.py faylini yangilash

```python
# accounts/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    """Foydalanuvchi ma'lumotlarini yangilash formasi"""
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username kiriting'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingizni kiriting'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiyangizni kiriting'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email kiriting'
            }),
        }
        labels = {
            'username': 'Foydalanuvchi nomi',
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email manzil',
        }


class ProfileUpdateForm(forms.ModelForm):
    """Profil ma'lumotlarini yangilash formasi"""
    
    class Meta:
        model = Profile
        fields = ['photo', 'bio', 'date_of_birth']
        widgets = {
            'photo': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'O\'zingiz haqingizda yozing...'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'photo': 'Profil rasmi',
            'bio': 'Bio (O\'zingiz haqingizda)',
            'date_of_birth': 'Tug\'ilgan sana',
        }
```

**Tushuntirish:**
- `UserUpdateForm` - User modelini yangilash uchun
- `ProfileUpdateForm` - Profile modelini yangilash uchun
- `accept='image/*'` - faqat rasm fayllarini qabul qilish
- `type='date'` - sana tanlash uchun input

### 10-qadam: Navigatsiyaga profil havolasini qo'shish

```html
<!-- templates/base.html yoki navigation.html -->

{% if user.is_authenticated %}
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" 
           role="button" data-toggle="dropdown">
            {% if user.profile.photo %}
                <img src="{{ user.profile.photo.url }}" 
                     alt="{{ user.username }}"
                     style="width: 30px; height: 30px; border-radius: 50%;">
            {% endif %}
            {{ user.username }}
        </a>
        <div class="dropdown-menu">
            <a class="dropdown-item" href="{% url 'profile' %}">
                <i class="fas fa-user"></i> Profilim
            </a>
            <a class="dropdown-item" href="{% url 'profile_edit' %}">
                <i class="fas fa-edit"></i> Profilni tahrirlash
            </a>
            <a class="dropdown-item" href="{% url 'password_change' %}">
                <i class="fas fa-key"></i> Parolni o'zgartirish
            </a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="{% url 'logout' %}">
                <i class="fas fa-sign-out-alt"></i> Chiqish
            </a>
        </div>
    </li>
{% else %}
    <li class="nav-item">
        <a class="nav-link" href="{% url 'login' %}">Kirish</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="{% url 'signup' %}">Ro'yxatdan o'tish</a>
    </li>
{% endif %}
```

### 11-qadam: Rasm o'lchamini cheklash (ixtiyoriy)

Katta hajmdagi rasmlarni yuklashni oldini olish uchun:

```python
# accounts/forms.py

from django import forms
from django.core.exceptions import ValidationError

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'bio', 'date_of_birth']
        # ... (widgets va labels)
    
    def clean_photo(self):
        """Rasm hajmini tekshirish"""
        photo = self.cleaned_data.get('photo')
        
        if photo:
            # 5MB dan katta bo'lmasligini tekshirish
            if photo.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('Rasm hajmi 5MB dan oshmasligi kerak!')
            
            # Fayl turini tekshirish
            if not photo.content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                raise ValidationError('Faqat JPG va PNG formatdagi rasmlar qabul qilinadi!')
        
        return photo
```

**Tushuntirish:**
- `clean_photo()` - photo maydonini validatsiya qilish
- `photo.size` - fayl hajmi baytlarda
- `photo.content_type` - fayl turi (MIME type)

## Natijani tekshirish

1. **Serverni ishga tushiring:**
```bash
python manage.py runserver
```

2. **Profilga kiring:**
   - `http://127.0.0.1:8000/accounts/profile/` - profilni ko'rish
   - `http://127.0.0.1:8000/accounts/profile/edit/` - profilni tahrirlash

3. **Rasm yuklang va saqlang**

4. **Profilda rasm to'g'ri ko'rinishini tekshiring**

## Keng tarqalgan xatolar va yechimlar

### Xato 1: Rasm ko'rinmayapti

**Sabab:** `MEDIA_URL` va `MEDIA_ROOT` to'g'ri sozlanmagan

**Yechim:** 
- `settings.py` da sozlamalarni tekshiring
- `urls.py` da `static()` funksiyasi qo'shilganligini tekshiring

### Xato 2: "No such file or directory"

**Sabab:** `media` papkasi yaratilmagan

**Yechim:**
```bash
mkdir media
mkdir media/users
```

### Xato 3: Rasm yuklanmayapti

**Sabab:** Form'da `enctype="multipart/form-data"` qo'shilmagan

**Yechim:**
```html
<form method="post" enctype="multipart/form-data">
```

### Xato 4: Profile obyekti yo'q

**Sabab:** Foydalanuvchi uchun profil yaratilmagan

**Yechim:**
```python
profile, created = Profile.objects.get_or_create(user=request.user)
```

## Qo'shimcha imkoniyatlar

### 1. Rasmni avtomatik kichiklashtirish

```python
# accounts/models.py

from django.db import models
from PIL import Image

class Profile(models.Model):
    # ... boshqa maydonlar ...
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.photo:
            img = Image.open(self.photo.path)
            
            # Agar rasm 300x300 dan katta bo'lsa, kichiklashtirish
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.path)
```

**E'tibor bering:** `Pillow` kutubxonasi o'rnatilgan bo'lishi kerak:
```bash
pip install Pillow
```

### 2. Eski rasmni o'chirish

Yangi rasm yuklanganda eski rasmni o'chirish:

```python
# accounts/models.py

from django.db import models
import os

class Profile(models.Model):
    # ... boshqa maydonlar ...
    
    def save(self, *args, **kwargs):
        try:
            # Eski profil obyektini olish
            old_profile = Profile.objects.get(id=self.id)
            # Agar yangi rasm yuklangan bo'lsa va eski rasm bor bo'lsa
            if old_profile.photo and old_profile.photo != self.photo:
                # Eski rasmni o'chirish
                if os.path.isfile(old_profile.photo.path):
                    os.remove(old_profile.photo.path)
        except Profile.DoesNotExist:
            pass
        
        super().save(*args, **kwargs)
```

### 3. Rasm yuklashda progress bar

```html
<!-- jQuery va Bootstrap kerak -->
<script>
$('form').on('submit', function(e) {
    var fileInput = $('#id_photo')[0];
    if (fileInput.files.length > 0) {
        $('.progress').show();
        // Progress animatsiya
    }
});
</script>
```

## Best Practice - Eng yaxshi amaliyotlar

### 1. Rasm formatlari
- Foydalanuvchi rasmlarini JPEG formatida saqlash (hajmi kichik)
- PNG formatini faqat shaffof fon kerak bo'lganda ishlatish

### 2. Xavfsizlik
- Fayllarni serverga yuklashdan oldin validatsiya qiling
- Fayl turini va hajmini doim tekshiring
- Executable fayllar (.exe, .sh) ni rad eting

### 3. Performance (unumdorlik)
- Rasmlarni avtomatik kichiklashtiring
- Thumbnail (kichik versiya) yarating
- CDN (Content Delivery Network) dan foydalaning

### 4. Foydalanuvchi tajribasi
- Yuklash jarayonida loading indikator ko'rsating
- Rasm hajmi va formatini aniq ko'rsating
- Xato xabarlarini tushunarli qiling

### 5. Kod tashkiloti
- Media fayllar uchun alohida papkalar yarating
- Model, Form, View'larni mantiqiy ravishda ajrating
- Qayta ishlatiladigan komponentlar yarating

## Xulosa

Ushbu darsda biz quyidagilarni o'rgandik:

✅ Media fayllar bilan ishlash asoslari  
✅ `MEDIA_URL` va `MEDIA_ROOT` sozlamalari  
✅ Profil sahifasida rasm ko'rsatish  
✅ Standart rasm qo'llash  
✅ Rasm yuklash va validatsiya qilish  
✅ Profilni chiroyli ko'rinishda joylashtirish  
✅ Xatoliklarni bartaraf etish  

Keyingi darsda **Login_required dekoratori va LoginRequiredMixin** mavzusini o'rganamiz va sahifalarni himoya qilishni o'rgatamiz!

## Qo'shimcha o'qish uchun

- [Django Media Files Documentation](https://docs.djangoproject.com/en/stable/topics/files/)
- [Pillow Library Documentation](https://pillow.readthedocs.io/)
- [Django File Uploads](https://docs.djangoproject.com/en/stable/topics/http/file-uploads/)