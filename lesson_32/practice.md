# Dars 32: Amaliyot - Foydalanuvchi profilini yaratish

## Amaliyot maqsadi
Bu amaliyotda Django loyihasida foydalanuvchi profili yaratish, uni ko'rsatish va tahrirlash imkoniyatlarini qo'shamiz. Barcha bosqichlarni ketma-ket bajarib chiqamiz.

## Boshlash

Ishni boshlashdan oldin loyiha virtual muhitini faollashtiring:

```bash
# Loyiha katalogiga o'ting
cd django_loyiha_nomi

# Virtual muhitni faollashtiiring
pipenv shell

# Yoki venv uchun
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate     # Windows
```

## Amaliyot 1: Users app yaratish

### 1.1 Yangi app yaratamiz
```bash
python manage.py startapp users
```

### 1.2 Settings.py ga qo'shamiz
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
    'users.apps.UsersConfig',  # Bu qatorni qo'shing
]
```

### 1.3 Pillow kutubxonasini o'rnatamiz
```bash
pip install Pillow
```

## Amaliyot 2: Profile modelini yaratish

### 2.1 users/models.py fayliga quyidagini yozing:
```python
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

**Test qiling:** Modelni to'g'ri yazdingizmi?

## Amaliyot 3: Media sozlamalarini qo'shish

### 3.1 config/settings.py fayliga qo'shing:
```python
import os

# Faylning oxiriga qo'shing
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 3.2 config/urls.py ni yangilang:
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('users/', include('users.urls')),  # Bu qatorni qo'shing
]

# Bu qismni qo'shing
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3.3 Default rasm qo'shing
Loyiha katalogida:
1. `media` papka yarating
2. `media` ichida `profile_pics` papka yarating  
3. `profile_pics` ga `default.jpg` rasm qo'ying (kichik o'lchamli rasm)

**Test qiling:** Papkalar to'g'ri yaratilganmi?

## Amaliyot 4: Signal qo'shish

### 4.1 users/signals.py yarating:
```python
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

### 4.2 users/apps.py ni yangilang:
```python
from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self):
        import users.signals
```

**Test qiling:** Signal to'g'ri ulanganmi?

## Amaliyot 5: Migration qilish

```bash
python manage.py makemigrations users
python manage.py migrate
```

**Natija:** Users_profile jadvali yaratildi.

## Amaliyot 6: Forms yaratish

### 6.1 users/forms.py yarating:
```python
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

**Test qiling:** Formalar to'g'ri yaratilganmi?

## Amaliyot 7: Views yaratish

### 7.1 users/views.py ga quyidagini yozing:
```python
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
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

**Test qiling:** Views funksiyalari xatosiz yozilganmi?

## Amaliyot 8: URLs yaratish

### 8.1 users/urls.py yarating:
```python
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
]
```

**Test qiling:** URL patterns to'g'ri yozilganmi?

## Amaliyot 9: Template papkalarini yaratish

```bash
# users app ichida
mkdir -p users/templates/users
```

## Amaliyot 10: Profile template yaratish

### 10.1 users/templates/users/profile.html yarating:
```html
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

**Test qiling:** Template xatosiz yozilganmi?

## Amaliyot 11: Profile Update template yaratish

### 11.1 users/templates/users/profile_update.html yarating:
```html
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
                            </div>
                            
                            <div class="mb-3">
                                <label for="{{ p_form.bio.id_for_label }}" class="form-label">Bio</label>
                                {{ p_form.bio }}
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

## Amaliyot 12: Admin qismini sozlash

### 12.1 users/admin.py ni yangilang:
```python
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'location', 'created']
    list_filter = ['created', 'updated']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created', 'updated']
```

## Amaliyot 13: Navbar ga profil havolasini qo'shish

### 13.1 templates/base.html fayldagi navbar qismini yangilang:

Agar login qilgan foydalanuvchi uchun dropdown menyu mavjud bo'lsa, unga profil havolalarini qo'shing:

```html
<!-- Navbar ichida -->
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
            <li><a class="dropdown-item" href="{% url 'admin:index' %}">Admin</a></li>
            <li><a class="dropdown-item" href="{% url 'account_logout' %}">Chiqish</a></li>
        </ul>
    </li>
{% endif %}
```

## Amaliyot 14: Test qilish

### 14.1 Serverni ishga tushiring:
```bash
python manage.py runserver
```

### 14.2 Test bosqichlari:

1. **Admin orqali superuser yarating** (agar yo'q bo'lsa):
   ```bash
   python manage.py createsuperuser
   ```

2. **Saytga kiring:** http://127.0.0.1:8000/

3. **Login qiling** va navbar'da "Mening profilim" havolasini bosing

4. **Profil sahifasini tekshiring:**
   - Default rasm ko'rinishi kerak
   - "Profilni tahrirlash" tugmasi ishlashi kerak

5. **Profil tahrirlash sahifasini tekshiring:**
   - Barcha maydonlar ko'rinishi kerak
   - Rasm yuklash ishlashi kerak
   - Saqlash tugmasi ishlashi kerak

6. **Admin sahifasini tekshiring:**
   - http://127.0.0.1:8000/admin/
   - Profiles bo'limida profillar ko'rinishi kerak

### 14.3 Xatoliklarni tuzatish:

**Agar rasm ko'rinmasa:**
- `MEDIA_URL` va `MEDIA_ROOT` to'g'ri sozlanganmi?
- `default.jpg` fayli mavjudmi?
- `urls.py` da media static sozlamasi qo'shilganmi?

**Agar profil yaratilmasa:**
- Signal to'g'ri ulanganmi?
- Migration bajarilganmi?

**Agar form saqlanmasa:**
- `enctype="multipart/form-data"` qo'shilganmi?
- CSRF token mavjudmi?

## Amaliyot 15: Qo'shimcha funksiyalar

### 15.1 Profile'da statistika qo'shish

`users/models.py` ga method qo'shing:

```python
def get_news_count(self):
    """Foydalanuvchi yozgan yangiliklarni sanash"""
    return self.user.news_set.count() if hasattr(self.user, 'news_set') else 0
```

Template'da ishlatish:
```html
<p><strong>Yangiliklarim soni:</strong> {{ profile.get_news_count }}</p>
```

### 15.2 Social Media linklari qo'shish

`users/models.py` ga maydonlar qo'shing:

```python
facebook = models.URLField(blank=True, verbose_name="Facebook")
twitter = models.URLField(blank=True, verbose_name="Twitter") 
linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
instagram = models.URLField(blank=True, verbose_name="Instagram")
```

Migration qiling:
```bash
python manage.py makemigrations users
python manage.py migrate
```

## Yakuniy Test

### Barcha funksiyalarni tekshiring:
1. ✅ Profil sahifasi ochiladi
2. ✅ Profil tahrirlash ishlaydi  
3. ✅ Rasm yuklash ishlaydi
4. ✅ Ma'lumotlar saqlanydi
5. ✅ Admin sahifasida ko'rinadi
6. ✅ Navbar'da havolalar ishlaydi

## Amaliyot tugadi! 🎉

Siz muvaffaqiyatli foydalanuvchi profili yaratdingiz. Endi foydalanuvchilar:
- O'z profillarini ko'ra oladilar
- Profil rasmini yuklashi mumkin
- Shaxsiy ma'lumotlarni tahrirlaydi
- Bio, telefon, manzil va boshqalarini qo'sha oladilar

**Keyingi dars:** 

33-darsda Foydalanuvchui parolini o'zgartirish