# Lesson 40: Amaliyot - Profilda rasm va boshqa ma'lumotlarni chiqarish

## Loyiha maqsadi

Ushbu amaliyotda biz yangiliklar saytimiz uchun to'liq funksional profil tizimini yaratamiz. Foydalanuvchilar o'z profillariga rasm yuklashi, ma'lumotlarini tahrirlashi va profilini ko'rishi mumkin bo'ladi.

## Amaliyot rejasi

1. Media fayllar tizimini sozlash
2. Standart avatar rasmini tayyorlash
3. Profile modelini yaratish va migratsiya qilish
4. Profile view'larini yozish
5. Profile template'larini yaratish
6. Rasm validatsiyasini qo'shish
7. Profilni navigatsiyaga integratsiya qilish
8. Qo'shimcha funksiyalar
9. Testlar yozish
10. Production uchun tayyorlash

---

## 1-bosqich: Media fayllar tizimini sozlash

### 1.1. Settings.py faylini yangilash

`config/settings.py` faylini oching va oxiriga quyidagilarni qo'shing:

```python
# config/settings.py

# Static files sozlamalari
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Media files sozlamalari
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Tushuntirish:**
- `MEDIA_URL` - brauzerda media fayllarni ochish uchun URL
- `MEDIA_ROOT` - media fayllar saqlanadigan papka

### 1.2. Asosiy URLs.py faylini yangilash

`config/urls.py` faylini oching va media fayllarni xizmat qilish uchun quyidagilarni qo'shing:

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

**Eslatma:** Bu kod faqat `DEBUG=True` bo'lganda ishlaydi (development rejimida).

### 1.3. Media papkalarini yaratish

Terminal orqali quyidagi buyruqlarni bajaring:

```bash
# Loyiha ildiz papkasida
mkdir media
mkdir media/users
```

Yoki Windows'da:
```cmd
md media
md media\users
```

---

## 2-bosqich: Standart avatar rasmini tayyorlash

### 2.1. Standart rasm yuklab olish

1. [Unsplash](https://unsplash.com) yoki [Flaticon](https://www.flaticon.com) dan bepul avatar rasmini yuklab oling
2. Yoki oddiy default avatar yarating (Paint yoki boshqa dasturda)

### 2.2. Rasmni joylash

1. `static/images/` papkasini yarating (agar yo'q bo'lsa)
2. Rasmni `default-avatar.png` nomi bilan saqlang

```bash
# Loyiha strukturasi
project/
  ├── static/
  │   └── images/
  │       └── default-avatar.png
  ├── media/
  │   └── users/
  └── ...
```

---

## 3-bosqich: Profile modelini yaratish

### 3.1. Accounts app yaratish (agar yo'q bo'lsa)

```bash
python manage.py startapp accounts
```

### 3.2. Settings.py'ga qo'shish

```python
# config/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Local apps
    'news.apps.NewsConfig',
    'accounts.apps.AccountsConfig',  # Qo'shish
]
```

### 3.3. Profile modelini yozish

`accounts/models.py` faylini oching va quyidagini yozing:

```python
# accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
import os


class Profile(models.Model):
    """Foydalanuvchi profili modeli"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='Profil rasmi')
    bio = models.TextField(blank=True, null=True, verbose_name='Bio')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Tug\'ilgan sana')
    
    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profillar'
    
    def __str__(self):
        return f"{self.user.username} profili"
    
    def get_photo_url(self):
        """Profil rasmini qaytarish yoki standart rasmni ko'rsatish"""
        if self.photo:
            return self.photo.url
        return '/static/images/default-avatar.png'
    
    def save(self, *args, **kwargs):
        """Eski rasmni o'chirish va yangi rasmni kichiklashtirish"""
        try:
            # Bazada mavjud profilni olish
            old_profile = Profile.objects.get(id=self.id)
            # Agar yangi rasm yuklangan va eski rasm bor bo'lsa
            if old_profile.photo and old_profile.photo != self.photo:
                # Eski rasmni o'chirish
                if os.path.isfile(old_profile.photo.path):
                    os.remove(old_profile.photo.path)
        except Profile.DoesNotExist:
            pass
        
        super().save(*args, **kwargs)
        
        # Yangi rasmni kichiklashtirish
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.photo.path)


# Signal: Yangi user yaratilganda avtomatik profil yaratish
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """User yaratilganda avtomatik Profile yaratish"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """User saqlanganida Profile'ni ham saqlash"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
```

**Tushuntirish:**
- `OneToOneField` - har bir user uchun bitta profil
- `upload_to='users/'` - rasmlar `media/users/` papkasiga yuklanadi
- `blank=True, null=True` - majburiy emas
- `get_photo_url()` - rasm yo'q bo'lsa standart rasmni qaytaradi
- `save()` metodi - eski rasmni o'chiradi va yangi rasmni kichiklashtiradi
- Signallar - yangi user yaratilganda avtomatik profil yaratadi

### 3.4. Pillow kutubxonasini o'rnatish

```bash
pip install Pillow
```

### 3.5. Migratsiya qilish

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3.6. Admin panelga qo'shish

`accounts/admin.py` faylini oching:

```python
# accounts/admin.py

from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']
    list_filter = ['date_of_birth']
    search_fields = ['user__username', 'user__email']
```

---

## 4-bosqich: Forms yaratish

### 4.1. Forms.py faylini yaratish

`accounts/forms.py` faylini yarating:

```python
# accounts/forms.py

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserUpdateForm(forms.ModelForm):
    """Foydalanuvchi asosiy ma'lumotlarini yangilash"""
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ism'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiya'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email manzil'
            }),
        }
        labels = {
            'username': 'Foydalanuvchi nomi',
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Email',
        }
    
    def clean_email(self):
        """Email'ni validatsiya qilish"""
        email = self.cleaned_data.get('email')
        if email:
            # Boshqa userlarning emailini tekshirish
            qs = User.objects.filter(email=email).exclude(id=self.instance.id)
            if qs.exists():
                raise ValidationError('Bu email allaqachon ishlatilmoqda!')
        return email


class ProfileUpdateForm(forms.ModelForm):
    """Profil qo'shimcha ma'lumotlarini yangilash"""
    
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
                'placeholder': 'O\'zingiz haqingizda qisqacha yozing...'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'photo': 'Profil rasmi',
            'bio': 'Bio',
            'date_of_birth': 'Tug\'ilgan sana',
        }
    
    def clean_photo(self):
        """Rasm faylini validatsiya qilish"""
        photo = self.cleaned_data.get('photo')
        
        if photo:
            # Fayl hajmini tekshirish (5MB)
            if photo.size > 5 * 1024 * 1024:
                raise ValidationError('Rasm hajmi 5MB dan oshmasligi kerak!')
            
            # Fayl turini tekshirish
            allowed_types = ['image/jpeg', 'image/png', 'image/jpg']
            if photo.content_type not in allowed_types:
                raise ValidationError('Faqat JPG va PNG formatdagi rasmlar qabul qilinadi!')
        
        return photo
```

**Tushuntirish:**
- `UserUpdateForm` - User modelini tahrirlash uchun
- `ProfileUpdateForm` - Profile modelini tahrirlash uchun
- `clean_email()` - email takrorlanmasligini tekshirish
- `clean_photo()` - rasm hajmi va turini tekshirish

---

## 5-bosqich: Views yaratish

### 5.1. Profile view'larini yozish

`accounts/views.py` faylini oching:

```python
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm


@login_required
def profile_view(request):
    """Foydalanuvchi profil sahifasi"""
    # Profilni olish yoki yaratish
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    """Profilni tahrirlash sahifasi"""
    # Profilni olish yoki yaratish
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
            messages.success(request, 'Profil muvaffaqiyatli yangilandi!')
            return redirect('profile')
        else:
            messages.error(request, 'Iltimos, xatolarni tuzating!')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'accounts/profile_edit.html', context)
```

**Muhim:** 
- `@login_required` - faqat login qilgan userlar kirishi mumkin
- `request.FILES` - yuklangan fayllarni qabul qilish uchun
- `get_or_create()` - profil yo'q bo'lsa yaratadi

---

## 6-bosqich: URL'larni sozlash

### 6.1. Accounts URLs yaratish

`accounts/urls.py` faylini yarating:

```python
# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]
```

---

## 7-bosqich: Template'lar yaratish

### 7.1. Base template yaratish (agar yo'q bo'lsa)

`templates/base.html`:

```html
<!-- templates/base.html -->

{% load static %}
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar sayti{% endblock %}
```

---

## 8-bosqich: Test qilish

### 8.1. Serverni ishga tushirish

```bash
python manage.py runserver
```

### 8.2. Superuser yaratish (agar yo'q bo'lsa)

```bash
python manage.py createsuperuser
```

### 8.3. Test qilish

1. Brauzerda `http://127.0.0.1:8000/accounts/profile/` ochish
2. Profilni tahrirlashga o'tish: `/accounts/profile/edit/`
3. Rasm yuklash va saqlash
4. Profil sahifasida rasm ko'rinishini tekshirish
5. Navbar'da profil rasmini tekshirish

---

## 9-bosqich: Qo'shimcha funksiyalar (Advanced)

### 9.1. Profil to'ldirilganlik foizi

`accounts/models.py` ga qo'shing:

```python
# accounts/models.py

class Profile(models.Model):
    # ... oldingi kodlar ...
    
    def get_completion_percentage(self):
        """Profil to'ldirilganlik foizini hisoblash"""
        score = 0
        if self.user.first_name: score += 20
        if self.user.last_name: score += 20
        if self.user.email: score += 20
        if self.photo: score += 20
        if self.bio: score += 20
        return score
```

Profile template'ida ko'rsatish:

```html
<!-- templates/accounts/profile.html -->

{% block content %}
<div class="container mt-5">
    <!-- Progress bar -->
    <div class="alert alert-info">
        <h6>Profil to'ldirilganlik: {{ profile.get_completion_percentage }}%</h6>
        <div class="progress">
            <div class="progress-bar" role="progressbar" 
                 style="width: {{ profile.get_completion_percentage }}%">
                {{ profile.get_completion_percentage }}%
            </div>
        </div>
    </div>
    
    <!-- ... qolgan kod ... -->
</div>
{% endblock %}
```

### 9.2. Avatar galereya funksiyasi

`accounts/views.py` ga qo'shing:

```python
# accounts/views.py

import shutil
from django.conf import settings

@login_required
def select_avatar(request):
    """Tayyor avatardan tanlash"""
    if request.method == 'POST':
        avatar_name = request.POST.get('avatar')
        if avatar_name:
            profile = request.user.profile
            
            # Tayyor avatarni profile papkasiga nusxalash
            source = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 
                                 'avatars', avatar_name)
            destination = os.path.join(settings.MEDIA_ROOT, 'users', 
                                      f'{request.user.id}_{avatar_name}')
            
            shutil.copy(source, destination)
            profile.photo = f'users/{request.user.id}_{avatar_name}'
            profile.save()
            
            messages.success(request, 'Avatar muvaffaqiyatli o\'zgartirildi!')
            return redirect('profile')
    
    # Tayyor avatarlar ro'yxati
    avatars_dir = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 'avatars')
    avatars = os.listdir(avatars_dir) if os.path.exists(avatars_dir) else []
    
    return render(request, 'accounts/select_avatar.html', {'avatars': avatars})
```

Template yaratish:

```html
<!-- templates/accounts/select_avatar.html -->

{% extends 'base.html' %}
{% load static %}

{% block title %}Avatar tanlash{% endblock %}

{% block content %}
<div class="container mt-5">
    <h3 class="mb-4">Tayyor avatardan tanlang</h3>
    
    <form method="post">
        {% csrf_token %}
        <div class="row">
            {% for avatar in avatars %}
            <div class="col-md-2 col-sm-4 col-6 mb-3">
                <div class="card text-center">
                    <img src="{% static 'avatars/'|add:avatar %}" 
                         class="card-img-top" 
                         alt="Avatar"
                         style="cursor: pointer; height: 150px; object-fit: cover;"
                         onclick="selectAvatar('{{ avatar }}')">
                    <div class="card-body p-2">
                        <input type="radio" name="avatar" value="{{ avatar }}" id="avatar_{{ forloop.counter }}">
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <button type="submit" class="btn btn-primary mt-3">
            <i class="fas fa-check"></i> Tanlash
        </button>
        <a href="{% url 'profile_edit' %}" class="btn btn-secondary mt-3">
            <i class="fas fa-arrow-left"></i> Orqaga
        </a>
    </form>
</div>

<script>
function selectAvatar(name) {
    document.querySelector(`input[value="${name}"]`).checked = true;
}
</script>
{% endblock %}
```

URL qo'shish:

```python
# accounts/urls.py

urlpatterns = [
    # ... oldingi URL'lar ...
    path('profile/select-avatar/', views.select_avatar, name='select_avatar'),
]
```

---

## 10-bosqich: Testlar yozish

### 10.1. Profile model testlari

`accounts/tests.py` yarating:

```python
# accounts/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile


class ProfileModelTest(TestCase):
    """Profile modeli uchun testlar"""
    
    def setUp(self):
        """Test uchun foydalanuvchi yaratish"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_creation(self):
        """Yangi user yaratilganda avtomatik profil yaratilishini tekshirish"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
    
    def test_profile_str(self):
        """Profile __str__ metodini tekshirish"""
        expected_str = f"{self.user.username} profili"
        self.assertEqual(str(self.user.profile), expected_str)
    
    def test_get_photo_url_without_photo(self):
        """Rasm yo'q bo'lganda standart rasm qaytarilishini tekshirish"""
        default_url = '/static/images/default-avatar.png'
        self.assertEqual(self.user.profile.get_photo_url(), default_url)
    
    def test_get_completion_percentage_empty(self):
        """Bo'sh profil uchun 0% qaytarilishini tekshirish"""
        self.assertEqual(self.user.profile.get_completion_percentage(), 0)
    
    def test_get_completion_percentage_full(self):
        """To'liq profil uchun 100% qaytarilishini tekshirish"""
        self.user.first_name = 'Test'
        self.user.last_name = 'User'
        self.user.email = 'test@example.com'
        self.user.save()
        
        self.user.profile.bio = 'Test bio'
        # photo'ni test qilish uchun mock ishlatish kerak
        self.user.profile.save()
        
        # Email, first_name, last_name, bio = 80%
        self.assertEqual(self.user.profile.get_completion_percentage(), 80)
```

### 10.2. Profile view testlari

```python
# accounts/tests.py (davomi)

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class ProfileViewTest(TestCase):
    """Profile view testlari"""
    
    def setUp(self):
        """Test uchun foydalanuvchi va client yaratish"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.profile_url = reverse('profile')
        self.edit_url = reverse('profile_edit')
    
    def test_profile_view_requires_login(self):
        """Profil sahifasi login talab qilishini tekshirish"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertIn('/login/', response.url)
    
    def test_profile_view_for_logged_in_user(self):
        """Login qilgan user profilni ko'ra olishini tekshirish"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
    
    def test_profile_edit_get(self):
        """Profil tahrirlash sahifasini GET request bilan olish"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profilni tahrirlash')
    
    def test_profile_edit_post_valid(self):
        """Profil tahrirlashni POST request bilan test qilish"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'bio': 'Test bio',
        }
        response = self.client.post(self.edit_url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Ma'lumotlar yangilanganini tekshirish
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')


class ProfileFormTest(TestCase):
    """Profile form testlari"""
    
    def test_user_update_form_valid(self):
        """UserUpdateForm validatsiyasi"""
        from .forms import UserUpdateForm
        
        user = User.objects.create_user(username='testuser', password='test123')
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=user)
        self.assertTrue(form.is_valid())
    
    def test_profile_update_form_photo_validation(self):
        """ProfileUpdateForm rasm validatsiyasi"""
        from .forms import ProfileUpdateForm
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        # Juda katta fayl (6MB)
        large_file = SimpleUploadedFile(
            "test.jpg", 
            b"x" * (6 * 1024 * 1024),  # 6MB
            content_type="image/jpeg"
        )
        
        form_data = {'bio': 'Test bio'}
        form_files = {'photo': large_file}
        
        user = User.objects.create_user(username='test', password='test123')
        form = ProfileUpdateForm(data=form_data, files=form_files, instance=user.profile)
        
        self.assertFalse(form.is_valid())
        self.assertIn('photo', form.errors)
```

### 10.3. Testlarni ishga tushirish

```bash
# Barcha testlarni ishga tushirish
python manage.py test accounts

# Verbose rejimda
python manage.py test accounts --verbosity=2

# Coverage bilan
pip install coverage
coverage run --source='.' manage.py test accounts
coverage report
coverage html  # HTML report yaratish
```

---

## 11-bosqich: Troubleshooting (Muammolarni hal qilish)

### Muammo 1: Rasm ko'rinmayapti

**Sabab:** MEDIA sozlamalari noto'g'ri yoki URL pattern yo'q

**Yechim:**
```python
# settings.py tekshirish
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# urls.py tekshirish
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Muammo 2: "No such file or directory: 'media/users/...'"

**Sabab:** Media papka yaratilmagan

**Yechim:**
```bash
mkdir -p media/users
# yoki Windows'da
md media\users
```

### Muammo 3: Rasm yuklanmayapti

**Sabab:** Form'da `enctype` atributi yo'q

**Yechim:**
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    ...
</form>
```

### Muammo 4: Profile.DoesNotExist xatosi

**Sabab:** Foydalanuvchi uchun profil yaratilmagan

**Yechim:**
```python
# View'da get_or_create ishlatish
profile, created = Profile.objects.get_or_create(user=request.user)
```

### Muammo 5: "Cannot identify image file"

**Sabab:** Pillow kutubxonasi o'rnatilmagan yoki buzilgan rasm fayli

**Yechim:**
```bash
pip install --upgrade Pillow
```

### Muammo 6: Signal ishlamayapti

**Sabab:** Signal import qilinmagan

**Yechim:**
```python
# accounts/apps.py

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    def ready(self):
        import accounts.signals  # Signal'larni import qilish
```

---

## 12-bosqich: Production uchun tayyorlash

### 12.1. Media fayllarni production'da xizmat qilish

Production'da (masalan, Nginx bilan) media fayllar to'g'ridan-to'g'ri web-server orqali xizmat qilinadi:

```nginx
# nginx.conf

server {
    listen 80;
    server_name yourdomain.com;
    
    location /media/ {
        alias /path/to/your/project/media/;
    }
    
    location /static/ {
        alias /path/to/your/project/static/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 12.2. AWS S3 bilan integratsiya (Ixtiyoriy)

Katta loyihalarda media fayllarni AWS S3'ga yuklash yaxshiroq:

```bash
pip install django-storages boto3
```

```python
# settings.py

# AWS S3 sozlamalari
AWS_ACCESS_KEY_ID = 'your-access-key'
AWS_SECRET_ACCESS_KEY = 'your-secret-key'
AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Media fayllar uchun S3 ishlatish
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### 12.3. Security best practices

```python
# settings.py (Production)

# CSRF
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Session
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# File upload
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

---

## Best Practices - Eng yaxshi amaliyotlar

### 1. Xavfsizlik

✅ **Fayllarni doim validatsiya qiling:**
- Fayl hajmini cheklang (masalan, 5MB)
- Faqat ruxsat etilgan formatlarni qabul qiling (JPG, PNG)
- Fayl nomlarini sanitize qiling

✅ **Executable fayllarni rad eting:**
```python
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif']

def validate_image_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
```

✅ **Login talab qiling:**
```python
@login_required  # Har doim
def profile_view(request):
    ...
```

### 2. Performance

✅ **Rasmlarni kichiklashtiring:**
- Thumbnail versiyalar yarating
- Image optimization ishlatiling (Pillow)
- Lazy loading qo'shing

✅ **Caching ishlatiling:**
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # 15 daqiqa
def profile_view(request):
    ...
```

✅ **Database query optimization:**
```python
# select_related ishlatish
users = User.objects.select_related('profile').all()

# Prefetch ishlatish
from django.db.models import Prefetch
users = User.objects.prefetch_related('profile').all()
```

### 3. User Experience

✅ **Loading indikatorlar:**
```html
<button type="submit" id="submitBtn">
    <span id="btnText">Saqlash</span>
    <span id="loader" class="d-none">
        <i class="fas fa-spinner fa-spin"></i>
    </span>
</button>

<script>
document.getElementById('profileForm').addEventListener('submit', function() {
    document.getElementById('btnText').classList.add('d-none');
    document.getElementById('loader').classList.remove('d-none');
});
</script>
```

✅ **Success/Error messages:**
```python
from django.contrib import messages

messages.success(request, 'Profil muvaffaqiyatli yangilandi!')
messages.error(request, 'Xatolik yuz berdi!')
messages.warning(request, 'Ogohlantirish!')
messages.info(request, 'Ma\'lumot!')
```

✅ **Form validatsiya xabarlari:**
- Tushunarli xato xabarlari
- Real-time validatsiya (JavaScript)
- Field-level va form-level validation

### 4. Kod tashkiloti

✅ **DRY (Don't Repeat Yourself):**
```python
# utils.py yaratish
def get_user_profile(user):
    profile, created = Profile.objects.get_or_create(user=user)
    return profile

def handle_uploaded_file(file, user):
    # Fayl yuklash logikasi
    pass
```

✅ **Signals ishlatish:**
- Avtomatik profil yaratish
- Rasmlarni avtomatik optimizatsiya qilish
- Email yuborish

✅ **Custom managers:**
```python
class ProfileManager(models.Manager):
    def with_photo(self):
        return self.exclude(photo='')
    
    def completed(self):
        return self.filter(
            user__first_name__isnull=False,
            user__last_name__isnull=False,
            photo__isnull=False
        )

class Profile(models.Model):
    # ...
    objects = ProfileManager()
```

### 5. Testing

✅ **Testlar yozing:**
- Model testlari
- View testlari
- Form testlari
- Integration testlari

✅ **Coverage tekshiring:**
```bash
pip install coverage
coverage run --source='.' manage.py test accounts
coverage report
coverage html  # HTML report
```

✅ **CI/CD sozlash:**
```yaml
# .github/workflows/django.yml
name: Django CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python manage.py test
```

---

## Qo'shimcha vazifalar (Homework)

### Vazifa 1: Avatar galereya (Bajarildi ✅)

Foydalanuvchiga tayyor avatar rasmlaridan birini tanlash imkoniyati qo'shing.

**Talablar:**
- `static/avatars/` papkasida 10ta tayyor avatar
- Radio button yoki grid tarzida ko'rsatish
- Tanlangan avatarni profil rasmi sifatida saqlash

### Vazifa 2: Profil to'ldirilganlik foizi (Bajarildi ✅)

Profil sahifasida to'ldirilganlik foizini ko'rsating.

**Talablar:**
- Ism, familiya, email, rasm, bio - har biri 20%
- Progress bar bilan vizualizatsiya
- Bo'sh field'lar uchun hint berish

### Vazifa 3: Rasm crop funksiyasi

Rasm yuklashda crop (kesish) imkoniyati qo'shing.

**Talablar:**
- [Cropper.js](https://fengyuanchen.github.io/cropperjs/) kutubxonasidan foydalaning
- Foydalanuvchi rasmni kerakli o'lchamga kesishi mumkin
- Crop qilingan rasmni saqlash

**Yordam:**
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.12/cropper.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/cropperjs/1.5.12/cropper.min.css">
```

### Vazifa 4: Social media havolalar

Profilga ijtimoiy tarmoq havolalarini qo'shing.

**Talablar:**
- Facebook, Twitter, Instagram, LinkedIn
- Icon'lar bilan ko'rsatish
- URLField validatsiyasi

**Model:**
```python
class Profile(models.Model):
    # ... oldingi fieldlar ...
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
```

### Vazifa 5: Profil privacy sozlamalari

Profil uchun privacy sozlamalarini qo'shing.

**Talablar:**
- Profilni hammaga ko'rsatish/yashirish
- Email ko'rinishini boshqarish
- Tug'ilgan sanani yashirish

---

## Xulosa

Ushbu amaliyotda biz quyidagilarni amalga oshirdik:

✅ Media fayllar tizimini sozladik  
✅ Profile modelini yaratdik  
✅ Profil sahifasini yaratdik  
✅ Profil tahrirlash funksiyasini qo'shdik  
✅ Rasm yuklash va validatsiya qildik  
✅ Standart avatar rasmini qo'lladik  
✅ Navigatsiyaga profil menyusini qo'shdik  
✅ Qo'shimcha funksiyalar qo'shdik (avatar galereya, completion %)  
✅ Testlar yozdik  
✅ Best practice'larni qo'lladik  
✅ Production uchun tayyorladik  

**Keyingi dars:** Login_required dekoratori va LoginRequiredMixin - sahifalarni himoya qilish!

---

## Foydali havolalar

### Django
- [Django Media Files](https://docs.djangoproject.com/en/stable/topics/files/)
- [Django Forms](https://docs.djangoproject.com/en/stable/topics/forms/)
- [Django Signals](https://docs.djangoproject.com/en/stable/topics/signals/)
- [Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)

### Kutubxonalar
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Django Storages (AWS S3)](https://django-storages.readthedocs.io/)
- [Cropper.js](https://fengyuanchen.github.io/cropperjs/)

### Frontend
- [Bootstrap 4 Components](https://getbootstrap.com/docs/4.6/components/)
- [Font Awesome Icons](https://fontawesome.com/icons)

### Deployment
- [Nginx Configuration](https://nginx.org/en/docs/)
- [Gunicorn](https://gunicorn.org/)
- [AWS S3](https://aws.amazon.com/s3/)

---

## Requirements.txt

Loyiha uchun kerakli kutubxonalar:

```txt
Django==4.2.7
Pillow==10.1.0
django-storages==1.14.2  # AWS S3 uchun (ixtiyoriy)
boto3==1.29.7  # AWS S3 uchun (ixtiyoriy)
coverage==7.3.2  # Testing uchun (ixtiyoriy)
```

O'rnatish:
```bash
pip install -r requirements.txt
```

---

## Git ignore

`.gitignore` fayliga qo'shish kerak:

```gitignore
# Media files
media/

# Database
*.sqlite3
db.sqlite3

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# Django
*.log
local_settings.py

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Loyiha strukturasi (Final)

```
news_project/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── news/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── models.py
│   └── views.py
├── templates/
│   ├── base.html
│   └── accounts/
│       ├── profile.html
│       ├── profile_edit.html
│       └── select_avatar.html
├── static/
│   ├── images/
│   │   └── default-avatar.png
│   └── avatars/
│       ├── avatar1.png
│       ├── avatar2.png
│       └── ...
├── media/
│   └── users/
│       └── (yuklangan rasmlar)
├── .gitignore
├── requirements.txt
├── manage.py
└── db.sqlite3
```

---

## Yakuniy tekshirish ro'yxati (Checklist)

### Kod
- [ ] Settings.py to'g'ri sozlangan (MEDIA_URL, MEDIA_ROOT)
- [ ] Profile modeli yaratilgan va migratsiya qilingan
- [ ] Forms validatsiya bilan
- [ ] Views @login_required decorator bilan
- [ ] URL patterns to'g'ri
- [ ] Template'lar tayyor
- [ ] Signals ishlayapti

### Fayllar
- [ ] media/users/ papkasi yaratilgan
- [ ] static/images/default-avatar.png mavjud
- [ ] .gitignore to'g'ri sozlangan
- [ ] requirements.txt yaratilgan

### Funksionallik
- [ ] Profil ko'rinishi ishlayapti
- [ ] Profil tahrirlash ishlayapti
- [ ] Rasm yuklash ishlayapti
- [ ] Rasm kichiklashtiriladi
- [ ] Navbar'da profil rasmi ko'rinadi
- [ ] Messages ko'rsatiladi

### Testing
- [ ] Model testlari yozilgan
- [ ] View testlari yozilgan
- [ ] Form testlari yozilgan
- [ ] Barcha testlar o'tayapti

### Security
- [ ] Rasm validatsiyasi ishlayapti
- [ ] Login talab qilinadi
- [ ] CSRF protection yoqilgan
- [ ] Fayl hajmi cheklangan

---

## Tez-tez beriladigan savollar (FAQ)

**S: Pillow o'rnatganda xato chiqyapti?**  
J: `pip install --upgrade pip` keyin qayta urinib ko'ring.

**S: Media fayllar production'da ko'rinmayapti?**  
J: Nginx yoki Apache orqali static va media fayllarni xizmat qilish kerak.

**S: Rasm yuklanganda xotira tugayapti?**  
J: `FILE_UPLOAD_MAX_MEMORY_SIZE` sozlamasini pasaytiring yoki chunk upload ishlatilng.

**S: Signal ishlamayapti?**  
J: `apps.py` da `ready()` metodini tekshiring va signal import qilinganini tasdiqlang.

**S: Avatar galereya ishlmayapti?**  
J: `static/avatars/` papkasi yaratilganini va rasmlar mavjudligini tekshiring.

---

## Muallif haqida

Bu dars Django asoslarda profil tizimini yaratish bo'yicha to'liq amaliy qo'llanma. 

**Darsning maqsadi:**
- Django media files bilan ishlashni o'rganish
- Model signals va form validation
- User profile CRUD operatsiyalari
- Image processing va optimization
- Testing va best practices

**Keyingi darslar:**
- Lesson 41: Login required dekoratori
- Lesson 42: Class-based views
- Lesson 43: Django REST Framework
- Lesson 44: WebSocket va real-time features

---

**Omad! 🚀 Keyingi darsda ko'rishamiz!**
