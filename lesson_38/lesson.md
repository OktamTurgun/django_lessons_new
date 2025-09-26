# Lesson 38: Profil modelini yaratish va tahrirlash

## Dars maqsadi
Ushbu darsda biz foydalanuvchi uchun qo'shimcha ma'lumotlarni saqlash uchun Profile modeli yaratamiz va uni tahrirlash imkoniyatini qo'shamiz. Django'ning User modelini kengaytirish, One-to-One relationship, va profile update funksiyalarini o'rganamiz.

## Mavzu bo'yicha nazariy ma'lumot

### Django User modelini kengaytirish usullari
Django'da User modelini kengaytirish uchun asosan uchta usul mavjud:

1. **Profile Model (One-to-One)** - bu darsda o'rganamiz
2. **Custom User Model (AbstractUser)**
3. **Custom User Model (AbstractBaseUser)**

### Profile Model nima?
Profile model - bu Django'ning standart User modeli bilan One-to-One bog'lanishga ega bo'lgan alohida model. Bu modelda foydalanuvchining qo'shimcha ma'lumotlari saqlanadi.

### Profile modelining afzalliklari
- **Mavjud loyihani buzmaydi** - User model o'zgartirilmaydi
- **Moslashuvchanlik** - kerak bo'lganda oson kengaytiriladi
- **Modularity** - profil ma'lumotlari alohida boshqariladi
- **Database normalizatsiya** - ma'lumotlar to'g'ri taqsimlanadi

## Amaliy qism

### 1-bosqich: Profile modelini yaratish

**accounts/models.py** faylida Profile modelini yaratamiz:

```python
# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Profile(models.Model):
    """Foydalanuvchi profil modeli"""
    
    # User modeli bilan One-to-One bog'lanish
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Foydalanuvchi"
    )
    
    # Qo'shimcha maydonlar
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        verbose_name="Bio",
        help_text="O'zingiz haqingizda qisqacha ma'lumot"
    )
    
    birth_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Tug'ilgan sana"
    )
    
    location = models.CharField(
        max_length=30, 
        blank=True, 
        verbose_name="Manzil"
    )
    
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        verbose_name="Telefon raqami",
        help_text="Masalan: +998901234567"
    )
    
    website = models.URLField(
        blank=True, 
        verbose_name="Veb-sayt",
        help_text="Shaxsiy veb-saytingiz havolasi"
    )
    
    avatar = models.ImageField(
        default='profile_pics/default.jpg',
        upload_to='profile_pics/',
        verbose_name="Profil rasmi"
    )
    
    # Qo'shimcha sozlamalar
    is_private = models.BooleanField(
        default=False,
        verbose_name="Shaxsiy profil",
        help_text="Profilingizni faqat siz ko'ra olasiz"
    )
    
    receive_notifications = models.BooleanField(
        default=True,
        verbose_name="Bildirishnomalarni olish"
    )
    
    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaratilgan sana"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Yangilangan sana"
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profillar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} profili"
    
    def get_absolute_url(self):
        """Profil sahifasining URL manzili"""
        return reverse('accounts:profile', kwargs={'pk': self.user.pk})
    
    def save(self, *args, **kwargs):
        """Rasmni saqlashda o'lchamini kichraytirish"""
        super().save(*args, **kwargs)
        
        # Rasm mavjud bo'lsa, o'lchamini tekshirish
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.avatar.path)
    
    def get_full_name(self):
        """To'liq ismni qaytarish"""
        full_name = f"{self.user.first_name} {self.user.last_name}"
        return full_name.strip() or self.user.username
    
    def get_age(self):
        """Yoshni hisoblash"""
        if self.birth_date:
            from datetime import date
            today = date.today()
            age = today.year - self.birth_date.year
            if today.month < self.birth_date.month or \
               (today.month == self.birth_date.month and today.day < self.birth_date.day):
                age -= 1
            return age
        return None
```

### 2-bosqich: Profile yaratish uchun signal qo'shish

**accounts/signals.py** faylini yaratamiz:

```python
# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Yangi User yaratilganda avtomatik Profile yaratish"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """User saqlanganda Profile ham saqlash"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # Agar profile mavjud bo'lmasa, yaratish
        Profile.objects.create(user=instance)
```

### 3-bosqich: Signal'ni faollashtirish

**accounts/apps.py** faylini yangilaymiz:

```python
# accounts/apps.py
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        """Signal'larni yuklash"""
        import accounts.signals
```

### 4-bosqich: Admin panelni sozlash

**accounts/admin.py** faylini yangilaymiz:

```python
# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    """User admin sahifasida Profile'ni ko'rsatish"""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil'


class UserAdmin(BaseUserAdmin):
    """User modelini Profile bilan birga boshqarish"""
    inlines = (ProfileInline,)
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_location')
    list_filter = BaseUserAdmin.list_filter + ('profile__location',)
    
    def get_location(self, obj):
        return obj.profile.location if hasattr(obj, 'profile') else ''
    get_location.short_description = 'Manzil'


# User modelini qayta ro'yxatga olish
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model uchun admin interface"""
    list_display = ('user', 'location', 'birth_date', 'is_private', 'created_at')
    list_filter = ('is_private', 'location', 'created_at')
    search_fields = ('user__username', 'user__email', 'location', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Asosiy ma'lumotlar', {
            'fields': ('user', 'bio', 'avatar')
        }),
        ('Shaxsiy ma'lumotlar', {
            'fields': ('birth_date', 'location', 'phone_number', 'website')
        }),
        ('Sozlamalar', {
            'fields': ('is_private', 'receive_notifications')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

### 5-bosqich: Profile tahrirlash form'ini yaratish

**accounts/forms.py** faylini yangilaymiz:

```python
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    # Mavjud kod...
    pass


class UserUpdateForm(forms.ModelForm):
    """User ma'lumotlarini yangilash uchun form"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email manzilingizni kiriting'
        })
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingizni kiriting'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Familiyangizni kiriting'
            }),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Profile ma'lumotlarini yangilash uchun form"""
    
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False
    )
    
    class Meta:
        model = Profile
        fields = [
            'bio', 'birth_date', 'location', 'phone_number', 
            'website', 'avatar', 'is_private', 'receive_notifications'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'O\'zingiz haqingizda qisqacha yozing...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Manzilingizni kiriting'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998901234567'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'receive_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def clean_phone_number(self):
        """Telefon raqami formatini tekshirish"""
        phone = self.cleaned_data.get('phone_number')
        if phone and not phone.startswith('+'):
            raise forms.ValidationError("Telefon raqami '+' belgisi bilan boshlanishi kerak.")
        return phone

    def clean_avatar(self):
        """Rasm o'lchamini tekshirish"""
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            # Fayl o'lchami (2MB dan kichik bo'lishi kerak)
            if avatar.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Rasm hajmi 2MB dan oshmasligi kerak.")
            
            # Fayl formati
            if not avatar.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise forms.ValidationError("Faqat PNG, JPG, JPEG, GIF formatdagi rasmlarni yuklash mumkin.")
        
        return avatar
```

### 6-bosqich: Profile view'larini yaratish

**accounts/views.py** faylini yangilaymiz:

```python
# accounts/views.py
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


class SignUpView(CreateView):
    # Mavjud kod...
    pass


class ProfileDetailView(DetailView):
    """Profil ko'rish sahifasi"""
    model = Profile
    template_name = 'registration/profile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self):
        """URL'dagi user_id asosida profile'ni olish"""
        user_id = self.kwargs.get('user_id')
        if user_id:
            user = User.objects.get(id=user_id)
            return user.profile
        else:
            # Agar user_id berilmagan bo'lsa, joriy foydalanuvchi profili
            return self.request.user.profile


@login_required
def profile_update_view(request):
    """Profil tahrirlash sahifasi (Function-based view)"""
    
    if request.method == 'POST':
        # Ikkala formni ham POST ma'lumotlari bilan yaratish
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profilingiz muvaffaqiyatli yangilandi!')
            return redirect('accounts:profile_detail')
        else:
            messages.error(request, 'Tahrirlashda xatolik yuz berdi. Iltimos, ma\'lumotlarni tekshiring.')
    
    else:
        # GET so'rovi - bo'sh formlarni yaratish
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'registration/profile_update.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Profil tahrirlash sahifasi (Class-based view)"""
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'registration/profile_update_cbv.html'
    
    def get_object(self):
        """Joriy foydalanuvchi profilini olish"""
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        """Template'ga qo'shimcha context qo'shish"""
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['user_form'] = UserUpdateForm(
                self.request.POST, 
                instance=self.request.user
            )
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context
    
    def form_valid(self, form):
        """Form to'g'ri to'ldirilganda"""
        # User form'ini ham tekshirish
        user_form = UserUpdateForm(
            self.request.POST, 
            instance=self.request.user
        )
        
        if user_form.is_valid():
            user_form.save()
            messages.success(
                self.request, 
                'Profilingiz muvaffaqiyatli yangilandi!'
            )
            return super().form_valid(form)
        else:
            # User form noto'g'ri bo'lsa, xato ko'rsatish
            messages.error(
                self.request, 
                'User ma\'lumotlarida xatolik bor.'
            )
            return self.form_invalid(form)
    
    def get_success_url(self):
        """Muvaffaqiyatli tahrirlashdan keyin qayerga yo'naltirish"""
        return reverse_lazy('accounts:profile_detail')
```

### 7-bosqich: URL marshrutlarini yangilash

**accounts/urls.py** faylini yangilaymiz:

```python
# accounts/urls.py
from django.urls import path
from .views import (
    SignUpView, 
    ProfileDetailView, 
    profile_update_view,
    ProfileUpdateView
)

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    
    # Profile URL'lari
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<int:user_id>/', ProfileDetailView.as_view(), name='profile_detail_user'),
    
    # Profile update - Function-based view
    path('profile/edit/', profile_update_view, name='profile_update'),
    
    # Profile update - Class-based view (alternative)
    path('profile/edit-cbv/', ProfileUpdateView.as_view(), name='profile_update_cbv'),
]
```

### 8-bosqich: Template'larni yaratish

#### Profile detail template

**templates/registration/profile_detail.html** faylini yaratamiz:

```html
<!-- templates/registration/profile_detail.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ profile.get_full_name }} - Profil{% endblock title %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <!-- Profile rasmi va asosiy ma'lumotlar -->
        <div class="col-md-4">
            <div class="card">
                <div class="card-body text-center">
                    <img src="{{ profile.avatar.url }}" 
                         alt="Profile picture" 
                         class="rounded-circle mb-3"
                         style="width: 150px; height: 150px; object-fit: cover;">
                    
                    <h4>{{ profile.get_full_name }}</h4>
                    <p class="text-muted">@{{ profile.user.username }}</p>
                    
                    {% if profile.location %}
                        <p><i class="fas fa-map-marker-alt"></i> {{ profile.location }}</p>
                    {% endif %}
                    
                    {% if profile.get_age %}
                        <p><i class="fas fa-birthday-cake"></i> {{ profile.get_age }} yosh</p>
                    {% endif %}
                    
                    {% if request.user == profile.user %}
                        <a href="{% url 'accounts:profile_update' %}" 
                           class="btn btn-primary btn-sm">
                            <i class="fas fa-edit"></i> Tahrirlash
                        </a>
                    {% endif %}
                </div>
            </div>
            
            <!-- Qo'shimcha ma'lumotlar -->
            <div class="card mt-3">
                <div class="card-header">
                    <h5>Ma'lumotlar</h5>
                </div>
                <div class="card-body">
                    {% if profile.phone_number %}
                        <p><strong>Telefon:</strong> {{ profile.phone_number }}</p>
                    {% endif %}
                    
                    {% if profile.user.email %}
                        <p><strong>Email:</strong> {{ profile.user.email }}</p>
                    {% endif %}
                    
                    {% if profile.website %}
                        <p><strong>Veb-sayt:</strong> 
                            <a href="{{ profile.website }}" target="_blank">{{ profile.website }}</a>
                        </p>
                    {% endif %}
                    
                    <p><strong>Ro'yxatdan o'tgan:</strong> {{ profile.user.date_joined|date:"d M Y" }}</p>
                </div>
            </div>
        </div>
        
        <!-- Bio va qo'shimcha kontent -->
        <div class="col-md-8">
            {% if profile.bio %}
                <div class="card">
                    <div class="card-header">
                        <h5>Bio</h5>
                    </div>
                    <div class="card-body">
                        <p>{{ profile.bio|linebreaks }}</p>
                    </div>
                </div>
            {% endif %}
            
            <!-- Foydalanuvchi yangiliklari (kelgusida qo'shiladi) -->
            <div class="card mt-3">
                <div class="card-header">
                    <h5>{{ profile.get_full_name }} ning yangiliklari</h5>
                </div>
                <div class="card-body">
                    <p class="text-muted">Hozircha yangiliklaringiz yo'q.</p>
                    {% if request.user == profile.user %}
                        <a href="#" class="btn btn-success">Yangilik yozish</a>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

#### Profile update template

**templates/registration/profile_update.html** faylini yaratamiz:

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
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                                {{ message }}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endfor %}
                    {% endif %}
                    
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <!-- User ma'lumotlari -->
                        <h5 class="mb-3">Shaxsiy ma'lumotlar</h5>
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="{{ user_form.first_name.id_for_label }}" class="form-label">Ism</label>
                                {{ user_form.first_name }}
                                {% if user_form.first_name.errors %}
                                    <div class="text-danger">
                                        {% for error in user_form.first_name.errors %}
                                            <small>{{ error }}</small>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="{{ user_form.last_name.id_for_label }}" class="form-label">Familiya</label>
                                {{ user_form.last_name }}
                                {% if user_form.last_name.errors %}
                                    <div class="text-danger">
                                        {% for error in user_form.last_name.errors %}
                                            <small>{{ error }}</small>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ user_form.email.id_for_label }}" class="form-label">Email</label>
                            {{ user_form.email }}
                            {% if user_form.email.errors %}
                                <div class="text-danger">
                                    {% for error in user_form.email.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <hr>
                        
                        <!-- Profile ma'lumotlari -->
                        <h5 class="mb-3">Profil ma'lumotlari</h5>
                        
                        <div class="mb-3">
                            <label for="{{ profile_form.avatar.id_for_label }}" class="form-label">Profil rasmi</label>
                            {% if request.user.profile.avatar %}
                                <div class="mb-2">
                                    <img src="{{ request.user.profile.avatar.url }}" 
                                         alt="Current avatar" 
                                         class="rounded-circle"
                                         style="width: 60px; height: 60px; object-fit: cover;">
                                </div>
                            {% endif %}
                            {{ profile_form.avatar }}
                            {% if profile_form.avatar.errors %}
                                <div class="text-danger">
                                    {% for error in profile_form.avatar.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ profile_form.bio.id_for_label }}" class="form-label">Bio</label>
                            {{ profile_form.bio }}
                            {% if profile_form.bio.errors %}
                                <div class="text-danger">
                                    {% for error in profile_form.bio.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="{{ profile_form.birth_date.id_for_label }}" class="form-label">Tug'ilgan sana</label>
                                {{ profile_form.birth_date }}
                                {% if profile_form.birth_date.errors %}
                                    <div class="text-danger">
                                        {% for error in profile_form.birth_date.errors %}
                                            <small>{{ error }}</small>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="{{ profile_form.location.id_for_label }}" class="form-label">Manzil</label>
                                {{ profile_form.location }}
                                {% if profile_form.location.errors %}
                                    <div class="text-danger">
                                        {% for error in profile_form.location.errors %}
                                            <small>{{ error }}</small>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="{{ profile_form.phone_number.id_for_label }}" class="form-label">Telefon raqami</label>
                                {{ profile_form.phone_number }}
                                {% if profile_form.phone_number.errors %}
                                    <div class="text-danger">
                                        {% for error in profile_form.phone_number.errors %}
                                            <small>{{ error }}</small>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                            <div class="col-md-6 mb-3">
                                <label for="{{ profile_form.website.id_for_label }}" class="form-label">Veb-sayt</label>
                                {{ profile_form.website }}
                                {% if profile_form.website.errors %}
                                    <div class="text-danger">
                                        {% for error in profile_form.website.errors %}
                                            <small>{{ error }}</small>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        
                        <hr>
                        
                        <!-- Sozlamalar -->
                        <h5 class="mb-3">Sozlamalar</h5>
                        
                        <div class="form-check mb-3">
                            {{ profile_form.is_private }}
                            <label class="form-check-label" for="{{ profile_form.is_private.id_for_label }}">
                                Shaxsiy profil (faqat siz ko'ra olasiz)
                            </label>
                        </div>
                        
                        <div class="form-check mb-3">
                            {{ profile_form.receive_notifications }}
                            <label class="form-check-label" for="{{ profile_form.receive_notifications.id_for_label }}">
                                Bildirishnomalarni olish
                            </label>
                        </div>
                        
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'accounts:profile_detail' %}" class="btn btn-secondary">
                                <i class="fas fa-arrow-left"></i> Orqaga
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Saqlash
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

### 9-bosqich: Navbar'ga profil linkini qo'shish

**templates/base.html** faylida navbar'ni yangilaymiz:

```html
<!-- templates/base.html -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{% url 'news:home' %}">Yangiliklar sayti</a>
        
        <div class="navbar-nav ms-auto">
            {% if user.is_authenticated %}
                <!-- Profile dropdown -->
                <div class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle d-flex align-items-center" 
                       href="#" 
                       id="navbarDropdown" 
                       role="button" 
                       data-bs-toggle="dropdown">
                        {% if user.profile.avatar %}
                            <img src="{{ user.profile.avatar.url }}" 
                                 alt="Profile" 
                                 class="rounded-circle me-2"
                                 style="width: 30px; height: 30px; object-fit: cover;">
                        {% endif %}
                        {{ user.profile.get_full_name }}
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                        <li>
                            <a class="dropdown-item" href="{% url 'accounts:profile_detail' %}">
                                <i class="fas fa-user"></i> Mening profilim
                            </a>
                        </li>
                        <li>
                            <a class="dropdown-item" href="{% url 'accounts:profile_update' %}">
                                <i class="fas fa-edit"></i> Profilni tahrirlash
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item" href="{% url 'password_change' %}">
                                <i class="fas fa-key"></i> Parolni o'zgartirish
                            </a>
                        </li>
                        <li><hr class="dropdown-divider"></li>
                        <li>
                            <a class="dropdown-item" href="{% url 'logout' %}">
                                <i class="fas fa-sign-out-alt"></i> Chiqish
                            </a>
                        </li>
                    </ul>
                </div>
            {% else %}
                <a class="nav-link" href="{% url 'login' %}">Kirish</a>
                <a class="nav-link" href="{% url 'accounts:signup' %}">Ro'yxatdan o'tish</a>
            {% endif %}
        </div>
    </div>
</nav>
```

### 10-bosqich: Media fayllar uchun sozlamalar

**config/settings.py** faylini yangilaymiz:

```python
# config/settings.py
import os

# Media files uchun sozlamalar
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Pillow kutubxonasi uchun
INSTALLED_APPS = [
    # ...
    'PIL',  # Agar kerak bo'lsa
]
```

**config/urls.py** faylida media URL'larini qo'shamiz:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

# Development rejimida media fayllarni serve qilish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 11-bosqich: Default profil rasmini qo'shish

**media/profile_pics/** papkasini yarating va **default.jpg** faylini joylashtiring.

## Migration va testlash

### 1. Migration yaratish va qo'llash

```bash
# Pillow o'rnatish (rasm ishlash uchun)
pip install Pillow

# Migration yaratish
python manage.py makemigrations accounts

# Migration qo'llash
python manage.py migrate

# Superuser yaratish (agar mavjud bo'lmasa)
python manage.py createsuperuser

# Server ishga tushirish
python manage.py runserver
```

### 2. Mavjud foydalanuvchilar uchun profile yaratish

Agar loyihada allaqachon foydalanuvchilar mavjud bo'lsa, ularni profile yaratish:

```bash
python manage.py shell
```

```python
# Django shell'da
from django.contrib.auth.models import User
from accounts.models import Profile

# Barcha foydalanuvchilar uchun profile yaratish
for user in User.objects.all():
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
        print(f"Profile yaratildi: {user.username}")
```

## Kengaytirilgan funksiyalar

### 1. Profile qidirish funksiyasi

**accounts/views.py** ga qidirish view'ini qo'shish:

```python
# accounts/views.py ga qo'shimcha
from django.db.models import Q

class ProfileSearchView(ListView):
    """Profil qidirish sahifasi"""
    model = Profile
    template_name = 'registration/profile_search.html'
    context_object_name = 'profiles'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Profile.objects.filter(
                Q(user__username__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(location__icontains=query),
                is_private=False
            ).select_related('user')
        return Profile.objects.filter(is_private=False).select_related('user')
```

### 2. Profile statistikalari

**accounts/models.py** ga qo'shimcha metodlar:

```python
# Profile modeliga qo'shimcha metodlar
def get_news_count(self):
    """Foydalanuvchi yangiliklarining sonini olish"""
    return self.user.news_set.count() if hasattr(self.user, 'news_set') else 0

def get_comments_count(self):
    """Foydalanuvchi izohlarining sonini olish"""
    return self.user.comment_set.count() if hasattr(self.user, 'comment_set') else 0
```

### 3. Profile activity feed

**accounts/views.py** ga activity feed view'ini qo'shish:

```python
# accounts/views.py ga qo'shimcha
class ProfileActivityView(LoginRequiredMixin, TemplateView):
    """Foydalanuvchi faoliyati sahifasi"""
    template_name = 'registration/profile_activity.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # So'nggi yangililar
        context['recent_news'] = user.news_set.all()[:5] if hasattr(user, 'news_set') else []
        
        # So'nggi izohlar
        context['recent_comments'] = user.comment_set.all()[:5] if hasattr(user, 'comment_set') else []
        
        return context
```

## Best Practices va maslahatlar

### 1. Performance optimizatsiya

```python
# views.py'da select_related va prefetch_related ishlatish
class ProfileDetailView(DetailView):
    model = Profile
    
    def get_queryset(self):
        return Profile.objects.select_related('user')
```

### 2. Security

```python
# Profile ko'rish huquqini tekshirish
def get_object(self):
    profile = super().get_object()
    
    # Shaxsiy profil tekshiruvi
    if profile.is_private and profile.user != self.request.user:
        raise Http404("Profil topilmadi")
    
    return profile
```

### 3. Image optimization

```python
# models.py'da save metodini optimallashtirish
def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    
    if self.avatar:
        img = Image.open(self.avatar.path)
        
        # Format tekshirish
        if img.format not in ['JPEG', 'PNG']:
            img = img.convert('RGB')
        
        # O'lcham optimizatsiya
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size, Image.Resampling.LANCZOS)
            img.save(self.avatar.path, optimize=True, quality=85)
```

### 4. Form validation

```python
# forms.py'da kengaytirilgan validation
def clean_bio(self):
    bio = self.cleaned_data.get('bio')
    if bio and len(bio) < 10:
        raise forms.ValidationError("Bio kamida 10 ta belgidan iborat bo'lishi kerak.")
    return bio
```

### 5. Template optimization

```html
<!-- Lazy loading rasm uchun -->
<img src="{{ profile.avatar.url }}" 
     alt="Profile picture" 
     class="rounded-circle"
     loading="lazy"
     style="width: 150px; height: 150px; object-fit: cover;">
```

## Xatolar va ularning yechimlari

### 1. OneToOneField xatosi
```
RelatedObjectDoesNotExist: User has no profile
```
**Yechimi:** Signal yaratish yoki migration'da profile yaratish

### 2. ImageField xatosi
```
AttributeError: 'ImageFieldFile' object has no attribute 'url'
```
**Yechimi:** Rasmni tekshirish:
```python
{% if profile.avatar %}
    <img src="{{ profile.avatar.url }}">
{% endif %}
```

### 3. Migration xatosi
```
ValueError: The field 'Profile.user' was declared with a lazy reference
```
**Yechimi:** Import'larni to'g'ri yozish

## Xulosa

Ushbu darsda biz Django'da to'liq Profile tizimini yaratdik. Asosiy o'rgangan narsalar:

1. **Profile Model yaratish** - One-to-One relationship
2. **Signal'lar** - avtomatik profile yaratish
3. **File upload** - rasm yuklash va optimizatsiya
4. **Form handling** - murakkab formlar bilan ishlash
5. **Template'lar** - professional UI yaratish
6. **Admin integration** - admin panelni sozlash
7. **Security** - profil ruxsatlarini boshqarish

Keyingi darsda login_required dekoratori va LoginRequiredMixin haqida batafsil o'rganamiz.