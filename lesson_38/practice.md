# Foydalanuvchi profil tizimi yaratish

## Amaliyot maqsadi
Bu amaliyot darsida siz foydalanuvchi profil tizimini to'liq yaratib, uning barcha funksiyalarini sinab ko'rasiz. One-to-One relationship, signal'lar, file upload va complex form'lar bilan amaliy ishlashni o'rganasiz.

## Tayyorgarlik

### 1. Kerakli kutubxonalarni o'rnatish

```bash
# Pillow kutubxonasini o'rnatish (rasm ishlash uchun)
pip install Pillow

# requirements.txt faylini yangilash
pip freeze > requirements.txt
```

### 2. Media sozlamalarini tekshirish

**config/settings.py** faylida:

```python
# Media files
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Vazifa 1: Profile modelini yaratish

### 1.1 Model yaratish

**accounts/models.py** faylini to'ldiring:

```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Profile(models.Model):
    # TODO: One-to-One field yaratish
    user = models.OneToOneField(
        # TODO: To'ldiring
    )
    
    # TODO: Quyidagi maydonlarni yarating:
    # - bio (TextField, max_length=500, blank=True)
    # - birth_date (DateField, null=True, blank=True)
    # - location (CharField, max_length=30, blank=True)
    # - phone_number (CharField, max_length=15, blank=True)
    # - website (URLField, blank=True)
    # - avatar (ImageField, default='profile_pics/default.jpg', upload_to='profile_pics/')
    # - is_private (BooleanField, default=False)
    # - receive_notifications (BooleanField, default=True)
    # - created_at (DateTimeField, auto_now_add=True)
    # - updated_at (DateTimeField, auto_now=True)

    class Meta:
        # TODO: verbose_name va ordering qo'shing
        pass

    def __str__(self):
        # TODO: String representation yozing
        pass
    
    def get_absolute_url(self):
        # TODO: Profile URL'ini qaytaring
        pass
    
    def save(self, *args, **kwargs):
        # TODO: Rasm o'lchamini kichraytirish logikasini yozing
        pass
    
    def get_full_name(self):
        # TODO: To'liq ismni qaytarish metodini yozing
        pass
    
    def get_age(self):
        # TODO: Yosh hisoblash metodini yozing
        pass
```

**Sizning vazifangiz:**
1. Barcha TODO qismlarini to'ldiring
2. Maydonlarga `verbose_name` qo'shing
3. `help_text` qo'shing
4. Metodlarni to'g'ri yozing

### 1.2 Test qilish

Profile modelini test qilish uchun kod yozing:

```python
# Test kodini yozing
# python manage.py shell

from accounts.models import Profile
from django.contrib.auth.models import User

# Test user yaratish
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    first_name='Test',
    last_name='User'
)

# Profile yaratish
profile = Profile.objects.create(
    user=user,
    bio='Bu test profili',
    location='Toshkent'
)

print(profile.get_full_name())
print(profile.__str__())
```

## Vazifa 2: Signal'larni sozlash

### 2.1 Signal yaratish

**accounts/signals.py** faylini yarating:

```python
# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # TODO: Yangi User yaratilganda Profile yaratish
    pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # TODO: User saqlanganda Profile ham saqlash
    pass
```

### 2.2 Signal'ni faollashtirish

**accounts/apps.py** faylini yangilang:

```python
# accounts/apps.py
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        # TODO: Signal'larni import qiling
        pass
```

### 2.3 Signal'ni testlash

```bash
# Terminal'da
python manage.py shell
```

```python
# Shell'da test qilish
from django.contrib.auth.models import User

# Yangi user yaratish
new_user = User.objects.create_user(
    username='signaltest',
    email='signal@test.com'
)

# Profile avtomatik yaratildimi tekshirish
print(hasattr(new_user, 'profile'))
print(new_user.profile)
```

## Vazifa 3: Admin panelni sozlash

### 3.1 ProfileAdmin yaratish

**accounts/admin.py** faylini to'ldiring:

```python
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    # TODO: Profile inline yaratish
    pass


class UserAdmin(BaseUserAdmin):
    # TODO: User admin'ni Profile bilan birlashtirish
    # inlines, list_display, list_filter qo'shing
    pass


# TODO: User'ni qayta ro'yxatga olish
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # TODO: Profile admin interface yaratish
    # list_display, list_filter, search_fields, fieldsets qo'shing
    pass
```

### 3.2 Admin panelni testlash

```bash
# Superuser yaratish
python manage.py createsuperuser

# Server ishga tushirish
python manage.py runserver

# Admin panelga kirish: http://127.0.0.1:8000/admin/
```

## Vazifa 4: Profile form'larini yaratish

### 4.1 Form'larni yaratish

**accounts/forms.py** faylini yangilang:

```python
# accounts/forms.py (mavjud kod ustiga qo'shing)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

# Mavjud SignUpForm...

class UserUpdateForm(forms.ModelForm):
    """User ma'lumotlarini yangilash uchun form"""
    
    # TODO: email maydonini yarating
    
    class Meta:
        model = # TODO: Model ko'rsating
        fields = # TODO: Maydonlarni ko'rsating
        widgets = {
            # TODO: Widget'larni qo'shing
        }


class ProfileUpdateForm(forms.ModelForm):
    """Profile ma'lumotlarini yangilash uchun form"""
    
    # TODO: birth_date uchun DateInput widget yarating
    
    class Meta:
        model = # TODO: Model ko'rsating
        fields = [
            # TODO: Barcha kerakli maydonlarni qo'shing
        ]
        widgets = {
            # TODO: Har bir maydon uchun widget yarating
        }

    def clean_phone_number(self):
        # TODO: Telefon raqami validatsiyasini yozing
        pass

    def clean_avatar(self):
        # TODO: Avatar validatsiyasini yozing (hajmi, format)
        pass
```

### 4.2 Form validatsiyasini test qilish

Form'larni test qilish uchun kod:

```python
# python manage.py shell
from accounts.forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User

# Test data
user = User.objects.first()
form_data = {
    'first_name': 'Yangi',
    'last_name': 'Ism',
    'email': 'yangi@email.com'
}

form = UserUpdateForm(data=form_data, instance=user)
print(form.is_valid())
print(form.errors)
```

## Vazifa 5: View'larni yaratish

### 5.1 Profile detail view yaratish

**accounts/views.py** faylini yangilang:

```python
# accounts/views.py (mavjud kod ustiga qo'shing)
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm

# Mavjud SignUpView...


class ProfileDetailView(DetailView):
    """Profil ko'rish sahifasi"""
    model = # TODO: Model ko'rsating
    template_name = # TODO: Template nomini yozing
    context_object_name = # TODO: Context nomini yozing
    
    def get_object(self):
        # TODO: URL'dagi user_id asosida profile'ni olish yoki
        # agar user_id yo'q bo'lsa, joriy foydalanuvchi profili
        pass


@login_required
def profile_update_view(request):
    """Profil tahrirlash sahifasi (Function-based view)"""
    
    if request.method == 'POST':
        # TODO: POST ma'lumotlari bilan form yaratish
        # TODO: Ikkala form ham valid bo'lsa saqlash
        # TODO: Success message va redirect
        pass
    else:
        # TODO: GET so'rovi - bo'sh form yaratish
        pass
    
    context = {
        # TODO: Context yaratish
    }
    
    return render(request, 'registration/profile_update.html', context)
```

### 5.2 URL'larni sozlash

**accounts/urls.py** faylini yangilang:

```python
# accounts/urls.py
from django.urls import path
from .views import (
    SignUpView, 
    ProfileDetailView, 
    profile_update_view
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # TODO: Profile URL'larini qo'shing
    # profile/ - joriy foydalanuvchi profili
    # profile/<int:user_id>/ - ma'lum bir foydalanuvchi profili
    # profile/edit/ - profil tahrirlash
]
```

## Vazifa 6: Template'larni yaratish

### 6.1 Profile detail template yaratish

**templates/registration/profile_detail.html** faylini yarating:

```html
<!-- templates/registration/profile_detail.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ profile.get_full_name }} - Profil{% endblock title %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <!-- Chap tomon: Avatar va asosiy ma'lumotlar -->
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    <!-- TODO: Avatar rasmini ko'rsating -->
                    <!-- TODO: To'liq ismni ko'rsating -->
                    <!-- TODO: Username'ni ko'rsating -->
                    <!-- TODO: Location va yosh (agar mavjud bo'lsa) -->
                    
                    <!-- TODO: Agar joriy foydalanuvchi o'zining profili bo'lsa, tahrirlash tugmasi -->
                </div>
            </div>
            
            <!-- Qo'shimcha ma'lumotlar card -->
            <div class="card mt-3">
                <div class="card-header">
                    <h5>Ma'lumotlar</h5>
                </div>
                <div class="card-body">
                    <!-- TODO: Telefon, email, website, ro'yxatdan o'tgan sana -->
                </div>
            </div>
        </div>
        
        <!-- O'ng tomon: Bio va kontent -->
        <div class="col-md-8">
            <!-- TODO: Bio card (agar mavjud bo'lsa) -->
            
            <!-- TODO: Foydalanuvchi yangiliklarini ko'rsatish card -->
        </div>
    </div>
</div>
{% endblock content %}
```

### 6.2 Profile update template yaratish

**templates/registration/profile_update.html** faylini yarating:

```html
<!-- templates/registration/profile_update.html -->
{% extends 'base.html' %}

{% block title %}Profilni tahrirlash{% endblock title %}

{% block content %}
<div class="container mt-4">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4><i class="fas fa-user-edit"></i> Profilni tahrirlash</h4>
                </div>
                <div class="card-body">
                    <!-- TODO: Messages'larni ko'rsating -->
                    
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <!-- TODO: User ma'lumotlari bo'limi -->
                        <!-- first_name, last_name, email -->
                        
                        <hr>
                        
                        <!-- TODO: Profile ma'lumotlari bo'limi -->
                        <!-- avatar, bio, birth_date, location, phone_number, website -->
                        
                        <hr>
                        
                        <!-- TODO: Sozlamalar bo'limi -->
                        <!-- is_private, receive_notifications -->
                        
                        <!-- TODO: Tugmalar (Orqaga, Saqlash) -->
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

### 6.3 Navbar'ni yangilash

**templates/base.html** faylida navbar'ga profile dropdown qo'shing:

```html
<!-- templates/base.html -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{% url 'news:home' %}">Yangiliklar</a>
        
        <div class="navbar-nav ms-auto">
            {% if user.is_authenticated %}
                <!-- TODO: Profile dropdown yarating -->
                <!-- Avatar, ism, profil, tahrirlash, parol o'zgartirish, chiqish -->
            {% else %}
                <!-- TODO: Login va signup linklari -->
            {% endif %}
        </div>
    </div>
</nav>
```

## Vazifa 7: Migration va testlash

### 7.1 Migration jarayoni

```bash
# 1. Migration yaratish
python manage.py makemigrations accounts

# 2. Migration qo'llash
python manage.py migrate

# 3. Mavjud foydalanuvchilar uchun profile yaratish
python manage.py shell
```

```python
# Shell'da
from django.contrib.auth.models import User
from accounts.models import Profile

for user in User.objects.all():
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
        print(f"Profile yaratildi: {user.username}")
```

### 7.2 Media fayl tuzilmasi yaratish

```bash
# Media papkalarini yaratish
mkdir -p media/profile_pics

# Default rasm qo'yish (ixtiyoriy)
# default.jpg faylini media/profile_pics/ papkasiga qo'ying
```

### 7.3 Funksionalni testlash

**Test scenariosi:**
1. Server ishga tushiring: `python manage.py runserver`
2. Yangi foydalanuvchi ro'yxatdan o'ting
3. Profile avtomatik yaratilganini tekshiring
4. Profil sahifasiga kiring
5. Profilni tahrirlang:
   - Avatar yuklay
   - Bio yozing
   - Ma'lumotlarni to'ldiring
6. O'zgarishlar saqlangandini tekshiring
7. Boshqa foydalanuvchi profilini ko'rishga urining

## Vazifa 8: Kengaytirilgan funksiyalar

### 8.1 Profile qidirish

**accounts/views.py** ga qidirish view'ini qo'shing:

```python
# accounts/views.py ga qo'shimcha
from django.db.models import Q
from django.views.generic import ListView

class ProfileSearchView(ListView):
    """Profil qidirish sahifasi"""
    model = Profile
    template_name = 'registration/profile_search.html'
    context_object_name = 'profiles'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        # TODO: Query asosida profil qidirish logikasini yozing
        # Username, ism, familiya, location bo'yicha qidirish
        # Faqat ochiq (is_private=False) profillarni ko'rsatish
        pass
```

### 8.2 Profile statistika

**accounts/models.py** da Profile modeliga qo'shimcha metodlar qo'shing:

```python
# Profile modeliga qo'shimcha
def get_news_count(self):
    """Foydalanuvchi yangiliklarining sonini olish"""
    # TODO: User'ning yangiliklar sonini qaytaring
    # return self.user.news_set.count() if hasattr(self.user, 'news_set') else 0
    pass

def get_comments_count(self):
    """Foydalanuvchi izohlarining sonini olish"""
    # TODO: User'ning izohlar sonini qaytaring
    # return self.user.comment_set.count() if hasattr(self.user, 'comment_set') else 0
    pass

def is_online(self):
    """Foydalanuvchi online ekanligini tekshirish"""
    # TODO: So'nggi faoliyat vaqti asosida online holatini aniqlash
    from datetime import datetime, timedelta
    # last_activity = self.user.last_login
    # if last_activity:
    #     return datetime.now() - last_activity < timedelta(minutes=15)
    # return False
    pass
```

### 8.3 Avatar resize funksiyasini yaxshilash

**accounts/models.py** da save metodini kengaytiring:

```python
def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    if self.avatar:
        img = Image.open(self.avatar.path)
        
        # TODO: Quyidagi funksiyalarni qo'shing:
        # 1. Rasm formatini tekshirish
        if img.format not in ['JPEG', 'PNG']:
            img = img.convert('RGB')
        
        # 2. O'lchamni optimizatsiya qilish
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size, Image.Resampling.LANCZOS)
        
        # 3. Sifatni sozlash va faylni siqish
        img.save(self.avatar.path, optimize=True, quality=85)
```

### 8.4 Profile privacy settings

**accounts/views.py** da privacy check qo'shing:

```python
from django.http import Http404

class ProfileDetailView(DetailView):
    # Mavjud kod...
    
    def get_object(self):
        profile = super().get_object()
        
        # TODO: Shaxsiy profil tekshiruvi
        # Agar profil private bo'lsa va joriy user owner bo'lmasa, 404
        if profile.is_private and profile.user != self.request.user:
            if not self.request.user.is_authenticated:
                raise Http404("Profil topilmadi")
            raise Http404("Bu profil shaxsiy")
        
        return profile
```

## Vazifa 9: Testing

### 9.1 Unit test'lar yozish

**accounts/tests.py** faylini yarating:

```python
# accounts/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
from .models import Profile
from .forms import ProfileUpdateForm


class ProfileModelTest(TestCase):
    def setUp(self):
        """Test uchun user va profile yaratish"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        # Profile signal orqali avtomatik yaratiladi
    
    def test_profile_creation(self):
        """Profile to'g'ri yaratilganini test qilish"""
        # TODO: Profile yaratilganligi va string representation'i
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(str(self.user.profile), f"{self.user.username} profili")
    
    def test_get_full_name(self):
        """get_full_name metodi test qilish"""
        # TODO: To'liq ism qaytarilishi
        expected_name = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(self.user.profile.get_full_name(), expected_name)
    
    def test_get_age(self):
        """get_age metodi test qilish"""
        # TODO: Yosh to'g'ri hisoblanishi
        self.user.profile.birth_date = date(1990, 1, 1)
        self.user.profile.save()
        age = self.user.profile.get_age()
        self.assertIsNotNone(age)
        self.assertGreater(age, 20)  # 1990 yildan keyin tug'ilgan


class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # TODO: Test user'ni login qilish
        self.client.login(username='testuser', password='testpass123')
    
    def test_profile_detail_view(self):
        """Profile detail view test qilish"""
        # TODO: Profil sahifasi to'g'ri yuklanishi
        response = self.client.get(reverse('accounts:profile_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)
    
    def test_profile_update_view_get(self):
        """Profile update GET so'rovi test qilish"""
        # TODO: Update sahifasi to'g'ri yuklanishi
        response = self.client.get(reverse('accounts:profile_update'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profilni tahrirlash')
    
    def test_profile_update_view_post(self):
        """Profile update POST so'rovi test qilish"""
        # TODO: Ma'lumot yangilanishi
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'bio': 'Updated bio text',
            'location': 'Toshkent',
            'is_private': False,
            'receive_notifications': True
        }
        response = self.client.post(reverse('accounts:profile_update'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        
        # Profile updated bo'lganini tekshirish
        self.user.refresh_from_db()
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.profile.bio, 'Updated bio text')


class ProfileFormTest(TestCase):
    def test_profile_form_valid_data(self):
        """To'g'ri ma'lumotlar bilan form test qilish"""
        # TODO: Valid form
        form_data = {
            'bio': 'Test bio mazmuni',
            'birth_date': '1990-01-01',
            'location': 'Toshkent',
            'phone_number': '+998901234567',
            'website': 'https://example.com',
            'is_private': False,
            'receive_notifications': True
        }
        form = ProfileUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_profile_form_invalid_data(self):
        """Noto'g'ri ma'lumotlar bilan form test qilish"""
        # TODO: Invalid form
        form_data = {
            'phone_number': 'invalid_phone',  # + belgisi yo'q
            'website': 'invalid_url',  # To'g'ri URL emas
        }
        form = ProfileUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)


class ProfileSignalTest(TestCase):
    def test_profile_created_on_user_creation(self):
        """User yaratilganda Profile avtomatik yaratilishini test qilish"""
        user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpass123'
        )
        # Signal orqali profile yaratilishi kerak
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)
```

### 9.2 Test'larni ishga tushirish

```bash
# Barcha test'larni ishga tushirish
python manage.py test accounts

# Ma'lum bir test klasini ishga tushirish
python manage.py test accounts.tests.ProfileModelTest

# Verbose output bilan
python manage.py test accounts --verbosity=2

# Coverage bilan test qilish (ixtiyoriy)
pip install coverage
coverage run --source='.' manage.py test accounts
coverage report
coverage html  # HTML hisobot yaratish
```

### 9.3 Manual testing checklist

**Profile yaratish:**
- [ ] Yangi user ro'yxatdan o'tganda profile avtomatik yaratiladi
- [ ] Signal to'g'ri ishlaydi
- [ ] Default qiymatlar o'rnatiladi
- [ ] Admin panelda profile ko'rinadi

**Profile ko'rish:**
- [ ] O'z profilini ko'rish mumkin
- [ ] Boshqa foydalanuvchi profilini ko'rish mumkin
- [ ] Shaxsiy profil faqat owner'ga ko'rinadi
- [ ] Avatar to'g'ri ko'rsatiladi
- [ ] URL'lar to'g'ri ishlaydi

**Profile tahrirlash:**
- [ ] Form to'g'ri yuklanadi
- [ ] Ma'lumotlar saqlaydi
- [ ] Avatar yuklash ishlaydi
- [ ] Rasm avtomatik resize bo'ladi
- [ ] Validation'lar ishlaydi
- [ ] Error message'lar ko'rsatiladi
- [ ] Success message ko'rsatiladi

**Security:**
- [ ] Faqat login foydalanuvchi o'z profilini tahrirlaydi
- [ ] File upload xavfsiz
- [ ] Form validation ishlaydi
- [ ] Private profile'lar himoyalangan

## Vazifa 10: Performance va Security

### 10.1 Database optimizatsiya

**Query optimizatsiya:**

```python
# views.py da
class ProfileDetailView(DetailView):
    model = Profile
    
    def get_queryset(self):
        # TODO: select_related dan foydalaning
        return Profile.objects.select_related('user')

class ProfileSearchView(ListView):
    def get_queryset(self):
        # TODO: Efficient query yozing
        query = self.request.GET.get('q')
        if query:
            return Profile.objects.filter(
                Q(user__username__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(location__icontains=query),
                is_private=False
            ).select_related('user')
        return Profile.objects.filter(
            is_private=False
        ).select_related('user')
```

### 10.2 Security checklist

```python
# views.py da security measures
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    def get_object(self):
        # TODO: Faqat owner o'z profilini tahrirlashi mumkin
        obj = super().get_object()
        if obj.user != self.request.user:
            raise Http404("Ruxsat berilmagan")
        return obj

# File upload security
def clean_avatar(self):
    avatar = self.cleaned_data.get('avatar')
    if avatar:
        # TODO: File size check (max 2MB)
        if avatar.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Fayl hajmi 2MB dan oshmasligi kerak")
        
        # TODO: File type check
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        if avatar.content_type not in allowed_types:
            raise forms.ValidationError("Faqat JPG, PNG, GIF formatdagi fayllarni yuklash mumkin")
    
    return avatar
```

### 10.3 Performance optimizatsiya

```python
# models.py da caching
from django.core.cache import cache

class Profile(models.Model):
    # ... mavjud kodlar
    
    def get_full_name(self):
        # TODO: Cache'dan foydalanish
        cache_key = f"user_full_name_{self.user.id}"
        full_name = cache.get(cache_key)
        
        if full_name is None:
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            if not full_name:
                full_name = self.user.username
            cache.set(cache_key, full_name, 3600)  # 1 soat cache
        
        return full_name
```

### 10.4 Final checklist

**Development checklist:**
- [ ] Model to'g'ri yaratilgan va migration qilingan
- [ ] Signal'lar ishlayapti
- [ ] Admin panel sozlangan
- [ ] Form'lar validation bilan
- [ ] View'lar security check bilan
- [ ] Template'lar responsive
- [ ] URL'lar to'g'ri sozlangan
- [ ] Media fayllar handle qilinayapti

**Security checklist:**
- [ ] Login required decorators
- [ ] File upload validation
- [ ] Privacy settings working
- [ ] CSRF protection enabled
- [ ] SQL injection himoyasi
- [ ] XSS himoyasi

**Performance checklist:**
- [ ] Database query optimizatsiya
- [ ] Image resize working
- [ ] Caching implemented (ixtiyoriy)
- [ ] Pagination implemented (katta dataset uchun)

**Testing checklist:**
- [ ] Unit test'lar yozilgan
- [ ] Manual testing o'tkazilgan
- [ ] Edge case'lar test qilingan
- [ ] Error handling test qilingan

## Yakuniy loyiha sinovlari

### Full workflow test:

1. **Yangi foydalanuvchi ro'yxatdan o'tish:**
   - Signup form to'ldirish
   - Profile avtomatik yaratilganligi
   - Login bo'lganligi

2. **Profile detail sahifasiga kirish:**
   - Profil ma'lumotlari to'g'ri ko'rsatilganligi
   - Avatar default rasm bilan ko'rsatilganligi

3. **Profile tahrirlash:**
   - Tahrirlash sahifasiga kirish
   - Barcha maydonlarni to'ldirish
   - Avatar yuklash
   - Saqlash va redirect

4. **O'zgarishlarni tekshirish:**
   - Profile detail sahifasida yangi ma'lumotlar
   - Avatar o'zgargan va resize bo'lgan

5. **Privacy test:**
   - Profile'ni private qilish
   - Boshqa foydalanuvchi tomondan ko'rishga urinish
   - 404 error qaytarish

Bu amaliyot darsini muvaffaqiyatli yakunlasangiz, siz Django'da to'liq profil tizimini yaratishni o'rgangan bo'lasiz!