# Amaliyot 19: Contact form yaratish

## Maqsad
Ushbu amaliyotda siz to'liq ishlaydigan contact form yaratib, Django'ning forms tizimi bilan amaliy tajriba orttirasiz.

## Bosqichma-bosqich amaliyot

### 1-bosqich: Loyihani tayyorlash

Avvalo, mavjud Django loyihangizni ishga tushiring:

```bash
# Virtual muhitni faollashtiring
pipenv shell

# Django serverni ishga tushiring
python manage.py runserver
```

### 2-bosqich: Forms faylini yaratish

Loyihangizning asosiy papkasida (loyiha nomi bilan) `forms.py` fayli yarating:

```python
# news/forms.py (yoki sizning app nomingiz)
from django import forms
from django.core.exceptions import ValidationError

class ContactForm(forms.Form):
    # To'liq ism
    full_name = forms.CharField(
        label="To'liq ism",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "Ismingiz va familiyangizni kiriting"
        })
    )
    
    # Email manzil
    email = forms.EmailField(
        label="Email manzil",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@gmail.com'
        })
    )
    
    # Telefon raqam
    phone_number = forms.CharField(
        label="Telefon raqam",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998 90 123 45 67'
        })
    )
    
    # Kompaniya/tashkilot
    organization = forms.CharField(
        label="Kompaniya/Tashkilot",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kompaniya nomi (ixtiyoriy)'
        })
    )
    
    # Xabar turi
    MESSAGE_TYPES = [
        ('general', 'Umumiy savol'),
        ('support', 'Texnik yordam'),
        ('business', 'Biznes takliflar'),
        ('complaint', 'Shikoyat'),
        ('other', 'Boshqa'),
    ]
    
    message_type = forms.ChoiceField(
        label="Xabar turi",
        choices=MESSAGE_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    # Mavzu
    subject = forms.CharField(
        label="Mavzu",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xabar mavzusi'
        })
    )
    
    # Xabar matni
    message = forms.CharField(
        label="Xabar",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Xabaringizni batafsil yozing...'
        })
    )
    
    # Roziylik
    agreement = forms.BooleanField(
        label="Men shaxsiy ma'lumotlarimni qayta ishlashga rozilik beraman",
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    # Custom validatsiya metodlari
    def clean_full_name(self):
        name = self.cleaned_data.get('full_name')
        if name:
            # Kamida 2 ta so'z bo'lishi kerak
            words = name.strip().split()
            if len(words) < 2:
                raise ValidationError("Ism va familiyani to'liq kiriting")
            
            # Faqat harflar va bo'shliq
            if not all(word.replace('-', '').isalpha() for word in words):
                raise ValidationError("Ism va familiyada faqat harflar bo'lishi mumkin")
        
        return name
    
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone:
            # Telefon raqam formatini tekshirish
            import re
            # O'zbekiston raqamlari uchun
            pattern = r'^\+998\s?[0-9]{2}\s?[0-9]{3}\s?[0-9]{2}\s?[0-9]{2}$'
            if not re.match(pattern, phone.replace('-', ' ')):
                raise ValidationError(
                    "Telefon raqam +998 XX XXX XX XX formatida bo'lishi kerak"
                )
        return phone
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if message:
            # Minimum 10 ta belgi
            if len(message.strip()) < 10:
                raise ValidationError("Xabar kamida 10 ta belgidan iborat bo'lishi kerak")
            
            # Maksimum 1000 ta belgi
            if len(message) > 1000:
                raise ValidationError("Xabar 1000 ta belgidan ko'p bo'lmasligi kerak")
        
        return message
```

### 3-bosqich: View yaratish

`views.py` faylida contact view yaratamiz:

```python
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse
from .forms import ContactForm
import logging

# Logger yaratish
logger = logging.getLogger(__name__)

def contact_view(request):
    """Contact form view"""
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            try:
                # Form ma'lumotlarini olish
                full_name = form.cleaned_data['full_name']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data.get('phone_number', '')
                organization = form.cleaned_data.get('organization', '')
                message_type = form.cleaned_data['message_type']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                
                # Xabar turi nomini olish
                message_type_display = dict(form.MESSAGE_TYPES)[message_type]
                
                # Email matnini yaratish
                email_subject = f"[{message_type_display}] {subject}"
                email_message = f"""
Yangi xabar keldi!

Yuboruvchi ma'lumotlari:
- Ism: {full_name}
- Email: {email}
- Telefon: {phone_number or 'Kiritilmagan'}
- Tashkilot: {organization or 'Kiritilmagan'}
- Xabar turi: {message_type_display}

Xabar matni:
{message}

---
Bu xabar avtomatik ravishda yuborilgan.
                """
                
                # Email yuborish
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=email,  # Yuboruvchi email
                    recipient_list=['admin@yoursite.com'],  # Qabul qiluvchi
                    fail_silently=False,
                )
                
                # Muvaffaqiyat xabari
                messages.success(
                    request, 
                    f"Hurmatli {full_name}, xabaringiz muvaffaqiyatli yuborildi! "
                    "Tez orada siz bilan bog'lanamiz."
                )
                
                # Logga yozish
                logger.info(f"Contact form submitted by {full_name} ({email})")
                
                return redirect('contact')
                
            except BadHeaderError:
                messages.error(request, "Xatolik: Noto'g'ri email header")
                logger.error("Bad header error in contact form")
                
            except Exception as e:
                messages.error(
                    request, 
                    "Xatolik yuz berdi. Iltimos qaytadan urinib ko'ring yoki "
                    "to'g'ridan-to'g'ri email orqali murojaat qiling."
                )
                logger.error(f"Error sending contact form: {str(e)}")
        
        else:
            # Form validatsiya xatolari
            messages.error(
                request, 
                "Iltimos, barcha maydonlarni to'g'ri to'ldiring."
            )
    
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'page_title': 'Biz bilan bog\'lanish'
    }
    
    return render(request, 'contact.html', context)
```

### 4-bosqich: Template yaratish

`templates` papkasida `contact.html` fayli yaratamiz:

```html
<!-- templates/contact.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ page_title }}{% endblock %}

{% block extra_css %}
<style>
    .contact-section {
        padding: 60px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .contact-form-wrapper {
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    .form-header {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 2rem;
        text-align: center;
    }
    
    .contact-info {
        background: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .info-item {
        text-align: center;
        padding: 1.5rem;
        border-radius: 10px;
        transition: transform 0.3s;
    }
    
    .info-item:hover {
        transform: translateY(-5px);
    }
    
    .form-control:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    .btn-contact {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        padding: 12px 40px;
        border-radius: 25px;
        transition: all 0.3s;
    }
    
    .btn-contact:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
{% endblock %}

{% block content %}
<div class="contact-section">
    <div class="container">
        <div class="row">
            <div class="col-lg-12">
                <div class="contact-form-wrapper">
                    <!-- Form header -->
                    <div class="form-header">
                        <h2><i class="fas fa-envelope me-3"></i>Biz bilan bog'lanish</h2>
                        <p>Savol va takliflaringizni bizga yuboring</p>
                    </div>
                    
                    <div class="p-4">
                        <!-- Xabarlar -->
                        {% if messages %}
                            {% for message in messages %}
                                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                                    <strong>
                                        {% if message.tags == 'success' %}
                                            <i class="fas fa-check-circle me-2"></i>
                                        {% elif message.tags == 'error' %}
                                            <i class="fas fa-exclamation-circle me-2"></i>
                                        {% endif %}
                                    </strong>
                                    {{ message }}
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                </div>
                            {% endfor %}
                        {% endif %}
                        
                        <!-- Aloqa ma'lumotlari -->
                        <div class="contact-info mb-4">
                            <div class="row">
                                <div class="col-md-4">
                                    <div class="info-item">
                                        <i class="fas fa-map-marker-alt fa-2x text-primary mb-3"></i>
                                        <h5>Manzil</h5>
                                        <p>Toshkent shahri, Chilonzor tumani, Bunyodkor ko'chasi</p>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="info-item">
                                        <i class="fas fa-phone fa-2x text-primary mb-3"></i>
                                        <h5>Telefon</h5>
                                        <p>+998 90 123 45 67<br>+998 71 123 45 67</p>
                                    </div>
                                </div>
                                <div class="col-md-4">
                                    <div class="info-item">
                                        <i class="fas fa-envelope fa-2x text-primary mb-3"></i>
                                        <h5>Email</h5>
                                        <p>info@example.com<br>support@example.com</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Contact form -->
                        <form method="post" id="contact-form" novalidate>
                            {% csrf_token %}
                            
                            <div class="row">
                                <!-- To'liq ism -->
                                <div class="col-md-6 mb-3">
                                    <label for="{{ form.full_name.id_for_label }}" class="form-label">
                                        {{ form.full_name.label }} <span class="text-danger">*</span>
                                    </label>
                                    {{ form.full_name }}
                                    {% if form.full_name.errors %}
                                        <div class="text-danger mt-1">
                                            {% for error in form.full_name.errors %}
                                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small><br>
                                            {% endfor %}
                                        </div>
                                    {% endif %}
                                </div>
                                
                                <!-- Email -->
                                <div class="col-md-6 mb-3">
                                    <label for="{{ form.email.id_for_label }}" class="form-label">
                                        {{ form.email.label }} <span class="text-danger">*</span>
                                    </label>
                                    {{ form.email }}
                                    {% if form.email.errors %}
                                        <div class="text-danger mt-1">
                                            {% for error in form.email.errors %}
                                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small><br>
                                            {% endfor %}
                                        </div>
                                    {% endif %}
                                </div>
                            </div>
                            
                            <div class="row">
                                <!-- Telefon -->
                                <div class="col-md-6 mb-3">
                                    <label for="{{ form.phone_number.id_for_label }}" class="form-label">
                                        {{ form.phone_number.label }}
                                    </label>
                                    {{ form.phone_number }}
                                    {% if form.phone_number.errors %}
                                        <div class="text-danger mt-1">
                                            {% for error in form.phone_number.errors %}
                                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small><br>
                                            {% endfor %}
                                        </div>
                                    {% endif %}
                                </div>
                                
                                <!-- Tashkilot -->
                                <div class="col-md-6 mb-3">
                                    <label for="{{ form.organization.id_for_label }}" class="form-label">
                                        {{ form.organization.label }}
                                    </label>
                                    {{ form.organization }}
                                    {% if form.organization.errors %}
                                        <div class="text-danger mt-1">
                                            {% for error in form.organization.errors %}
                                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small><br>
                                            {% endfor %}
                                        </div>
                                    {% endif %}
                                </div>
                            </div>
                            
                            <div class="row">
                                <!-- Xabar turi -->
                                <div class="col-md-6 mb-3">
                                    <label for="{{ form.message_type.id_for_label }}" class="form-label">
                                        {{ form.message_type.label }} <span class="text-danger">*</span>
                                    </label>
                                    {{ form.message_type }}
                                    {% if form.message_type.errors %}
                                        <div class="text-danger mt-1">
                                            {% for error in form.message_type.errors %}
                                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small><br>
                                            {% endfor %}
                                        </div>
                                    {% endif %}
                                </div>
                                
                                <!-- Mavzu -->
                                <div class="col-md-6 mb-3">
                                    <label for="{{ form.subject.id_for_label }}" class="form-label">
                                        {{ form.subject.label }} <span class="text-danger">*</span>
                                    </label>
                                    {{ form.subject }}
                                    {% if form.subject.errors %}
                                        <div class="text-danger mt-1">
                                            {% for error in form.subject.errors %}
                                                <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small><br>
                                            {% endfor %}
                                        </div>
                                    {% endif %}
                                </div>
                            </div>
                            
                            <!-- Xabar matni -->
                            <div class="mb-3">
                                <label for="{{ form.message.id_for_label }}" class="form-label">
                                    {{ form.message.label }} <span class="text-danger">*</span>
                                </label>
                                {{ form.message }}
                                {% if form.message.errors %}
                                    <div class="text-danger mt-1">
                                        {% for error in form.message.errors %}
                                            <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small><br>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                                <div class="form-text">Kamida 10 ta belgi kiritish talab etiladi</div>
                            </div>
                            
                            <!-- Roziylik -->
                            <div class="mb-4">
                                <div class="form-check">
                                    {{ form.agreement }}
                                    <label class="form-check-label" for="{{ form.agreement.id_for_label }}">
                                        {{ form.agreement.label }} <span class="text-danger">*</span>
                                    </label>
                                </div>
                                {% if form.agreement.errors %}
                                    <div class="text-danger mt-1">
                                        {% for error in form.agreement.errors %}
                                            <small><i class="fas fa-exclamation-triangle me-1"></i>{{ error }}</small><br>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                            
                            <!-- Submit tugma -->
                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary btn-contact btn-lg">
                                    <i class="fas fa-paper-plane me-2"></i>Xabar yuborish
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Xarita qismi (ixtiyoriy) -->
<div class="py-5 bg-light">
    <div class="container">
        <div class="row">
            <div class="col-lg-12 text-center">
                <h3 class="mb-4">Bizning joylashuvimiz</h3>
                <div class="map-container" style="height: 300px; background: #e9ecef; border-radius: 10px; display: flex; align-items: center; justify-content: center;">
                    <p class="text-muted">
                        <i class="fas fa-map-marked-alt fa-3x mb-3"></i><br>
                        Bu yerda xarita bo'ladi<br>
                        <small>Google Maps yoki boshqa xarita xizmatlari</small>
                    </p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Form validatsiyasi uchun JavaScript
    document.addEventListener('DOMContentLoaded', function() {
        const form = document.querySelector('#contact-form');
        const phoneInput = document.querySelector('#id_phone_number');
        
        // Telefon raqam formatini avtomatik to'g'rilash
        if (phoneInput) {
            phoneInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                if (value.startsWith('998')) {
                    value = '+' + value;
                    // Formatni to'g'rilash: +998 XX XXX XX XX
                    if (value.length > 4) {
                        value = value.slice(0, 4) + ' ' + value.slice(4);
                    }
                    if (value.length > 7) {
                        value = value.slice(0, 7) + ' ' + value.slice(7);
                    }
                    if (value.length > 11) {
                        value = value.slice(0, 11) + ' ' + value.slice(11);
                    }
                    if (value.length > 14) {
                        value = value.slice(0, 14) + ' ' + value.slice(14);
                    }
                    e.target.value = value.slice(0, 17); // Maksimum uzunlik
                }
            });
        }
        
        // Form yuborilganida loading ko'rsatish
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Yuborilmoqda...';
            submitBtn.disabled = true;
            
            // 10 soniyadan keyin qayta tiklash (xatolik bo'lsa)
            setTimeout(function() {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 10000);
        });
    });
</script>
{% endblock %}
```

### 5-bosqich: URL konfiguratsiyasi

`urls.py` faylida URL qo'shing:

```python
# urls.py (app level)
from django.urls import path
from . import views

urlpatterns = [
    # Boshqa URL'lar
    path('contact/', views.contact_view, name='contact'),
]
```

Agar asosiy `urls.py` faylida app URL'lari ulanmagan bo'lsa:

```python
# myproject/urls.py (project level)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # yoki sizning app nomingiz
]
```

### 6-bosqich: Email sozlamalari

`settings.py` faylida email sozlamalarini qo'shing:

```python
# settings.py

# Test uchun console backend (email console'da ko'rinadi)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Yoki haqiqiy email yuborish uchun (Gmail)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'your-email@gmail.com'
# EMAIL_HOST_PASSWORD = 'your-app-password'

# Default from email
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

# Logging sozlamalari
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'contact_form.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'news.views': {  # yoki sizning app nomingiz
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

### 7-bosqich: Navigation menusiga qo'shish

Agar `base.html` yoki navigation faylingiz mavjud bo'lsa, contact sahifasiga link qo'shing:

```html
<!-- base.html yoki navigation qismida -->
<nav class="navbar navbar-expand-lg">
    <div class="container">
        <!-- Boshqa menu elementlari -->
        <ul class="navbar-nav">
            <li class="nav-item">
                <a class="nav-link" href="{% url 'home' %}">Bosh sahifa</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="{% url 'news:list' %}">Yangiliklar</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="{% url 'contact' %}">Aloqa</a>
            </li>
        </ul>
    </div>
</nav>
```

### 8-bosqich: Test qilish

1. Serverni ishga tushiring:
```bash
python manage.py runserver
```

2. Brauzerda `http://127.0.0.1:8000/contact/` sahifasini oching

3. Formani to'ldirib test qiling:
   - Barcha majburiy maydonlarni to'ldiring
   - Telefon raqamni noto'g'ri formatda kiritib ko'ring
   - Bo'sh form yuborib ko'ring
   - To'g'ri ma'lumotlar bilan yuborib ko'ring

### 9-bosqich: Qo'shimcha funksiyalar (ixtiyoriy)

#### A) Contact model yaratish (ma'lumotlarni bazada saqlash):

```python
# models.py
from django.db import models

class ContactMessage(models.Model):
    MESSAGE_TYPES = [
        ('general', 'Umumiy savol'),
        ('support', 'Texnik yordam'),
        ('business', 'Biznes takliflar'),
        ('complaint', 'Shikoyat'),
        ('other', 'Boshqa'),
    ]
    
    full_name = models.CharField(max_length=100, verbose_name="To'liq ism")
    email = models.EmailField(verbose_name="Email")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    organization = models.CharField(max_length=150, blank=True, verbose_name="Tashkilot")
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, verbose_name="Xabar turi")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    is_read = models.BooleanField(default=False, verbose_name="O'qilgan")
    
    class Meta:
        verbose_name = "Aloqa xabari"
        verbose_name_plural = "Aloqa xabarlari"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.full_name}"
```

Migration yarating:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### B) Admin interfeysida ko'rish:

```python
# admin.py
from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'full_name', 'email', 'message_type', 'created_at', 'is_read']
    list_filter = ['message_type', 'is_read', 'created_at']
    search_fields = ['full_name', 'email', 'subject']
    readonly_fields = ['created_at']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "O'qilgan deb belgilash"
    
    actions = [mark_as_read]
```

#### C) Ajax orqali form yuborish:

```html
<!-- Template'ga qo'shimcha JavaScript -->
<script>
// Ajax form submission
document.getElementById('contact-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const submitBtn = this.querySelector('button[type="submit"]');
    
    // Loading holatini ko'rsatish
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Yuborilmoqda...';
    submitBtn.disabled = true;
    
    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Muvaffaqiyat xabari
            showAlert('success', data.message);
            this.reset();
        } else {
            // Xatolik xabari
            showAlert('error', 'Xatolik yuz berdi!');
        }
    })
    .catch(error => {
        showAlert('error', 'Tarmoq xatoligi!');
    })
    .finally(() => {
        // Tugmani qayta tiklash
        submitBtn.innerHTML = '<i class="fas fa-paper-plane me-2"></i>Xabar yuborish';
        submitBtn.disabled = false;
    });
});

function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.querySelector('.contact-form-wrapper .p-4').insertBefore(
        alertDiv, 
        document.querySelector('form')
    );
}
</script>
```

## Maslahatlar va Best Practices

### 1. Xavfsizlik
- **CSRF himoyasi**: Har doim `{% csrf_token %}` ishlatish
- **Input validatsiyasi**: Barcha kiruvchi ma'lumotlarni tekshirish
- **Email header injection**: BadHeaderError dan himoya
- **Rate limiting**: Spam xujumlardan himoya
- **Sanitization**: HTML va JavaScript injection oldini olish

### 2. Foydalanuvchi tajribasi (UX)
- **Loading indikatorlari**: Form yuborilayotganini ko'rsatish
- **Aniq xato xabarlar**: Foydalanuvchiga tushunarli
- **Form qiymatlarini saqlash**: Xato bo'lganda qayta kiritmaslik
- **Responsive dizayn**: Barcha qurilmalarda ishlash
- **Accessibility**: Screen reader'lar uchun label'lar

### 3. Kod sifati
- **DRY prinsipi**: Kod takrorlanishini oldini olish
- **Separation of concerns**: Logic va presentation ajratish
- **Error handling**: Barcha xatoliklarni tutish
- **Logging**: Muhim hodisalarni yozib qo'yish
- **Comments**: Kodga izohlar yozish

### 4. Performance
- **Database optimizatsiyasi**: Keraksiz so'rovlarni kamaytirish
- **Email queue**: Ko'p email yuborishda queue ishlatish
- **Caching**: Static ma'lumotlarni keshlash
- **Asset optimization**: CSS/JS fayllarni siqish
- **CDN**: Static fayllar uchun CDN ishlatish

### 5. Monitoring va Analytics
- **Form statistikalari**: Yuborilgan formalar soni
- **Success rate**: Muvaffaqiyatli yuborilgan foiz
- **Error tracking**: Xatoliklarni kuzatish
- **Response time**: Formaning javob berish vaqti
- **User behavior**: Foydalanuvchi harakatlari

## Keng tarqalgan xatoliklar va yechimlari

### 1. CSRF token xatoligi
```python
# Xato: CSRF token yo'q
# Yechim: Template'da {% csrf_token %} qo'shish
```

### 2. Email yuborilmaydi
```python
# Xato: EMAIL_BACKEND noto'g'ri sozlangan
# Yechim: settings.py da to'g'ri sozlash
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Test uchun
```

### 3. Form validatsiya ishlamaydi
```python
# Xato: clean_* metodlar noto'g'ri
# Yechim: Methodlar to'g'ri nomlanishi kerak
def clean_phone_number(self):  # To'g'ri
    # kod
```

### 4. Static fayllar yuklanmaydi
```python
# Xato: STATIC_URL yoki STATICFILES_DIRS noto'g'ri
# Yechim: settings.py da to'g'ri sozlash
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

## Keyingi qadamlar

### 1. Asosiy funksiyani test qiling
- Formani to'ldiring va yuborib ko'ring
- Barcha validatsiyalarni tekshiring
- Email kelishini tekshiring (console yoki email'da)

### 2. Dizaynni sozlang
- O'z loyihangizga mos ranglar qo'llang
- Logo va branding qo'shing
- Font va ikonkalarni o'zgartiring

### 3. Qo'shimcha xususiyatlar qo'shing
- **File upload**: Fayl yuklash imkoniyati
- **reCAPTCHA**: Bot himoyasi
- **Multiple recipients**: Turli bo'limlarga yuborish
- **Auto-response**: Avtomatik javob email

### 4. Monitoring o'rnating
- **Google Analytics**: Form submission tracking
- **Error tracking**: Sentry yoki boshqa servis
- **Performance monitoring**: Response time kuzatish

### 5. Testing yozing
```python
# tests.py
from django.test import TestCase, Client
from django.urls import reverse

class ContactFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_contact_form_display(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        
    def test_valid_form_submission(self):
        data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content',
            'message_type': 'general',
            'agreement': True
        }
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
```

### 6. Production uchun tayyorlash
- **HTTPS** sozlang
- **Environment variables** ishlatng
- **Database backup** tizimini o'rnating
- **Load balancing** uchun tayyorlang

## Troubleshooting (Muammolarni hal qilish)

### Form yuborilmaydi
1. CSRF token mavjudligini tekshiring
2. Form action URL'ini tekshiring
3. Method="POST" borligini tekshiring
4. JavaScript xatolarini console'da tekshiring

### Email yuborilmaydi
1. EMAIL_BACKEND sozlamalarini tekshiring
2. SMTP sozlamalarini tekshiring (agar real email ishlatilsa)
3. Internet ulanishini tekshiring
4. Gmail uchun App Password ishlatganingizni tekshiring

### Validatsiya ishlamaydi
1. Form class'ida clean_* metodlar to'g'ri yozilganini tekshiring
2. ValidationError import qilinganini tekshiring
3. Form.is_valid() chaqirilganini tekshiring

### CSS/JavaScript ishlamaydi
1. STATIC_URL va STATICFILES_DIRS sozlangan bo'lishini tekshiring
2. {% load static %} template'da mavjudligini tekshiring
3. Fayllar to'g'ri yo'lda turganini tekshiring

## Qo'shimcha resurslar

### Django Documentation
- [Django Forms](https://docs.djangoproject.com/en/stable/topics/forms/)
- [Form validation](https://docs.djangoproject.com/en/stable/ref/forms/validation/)
- [Email backends](https://docs.djangoproject.com/en/stable/topics/email/)

### Frontend kutubxonalar
- [Bootstrap](https://getbootstrap.com/) - CSS framework
- [Font Awesome](https://fontawesome.com/) - Ikonkalar
- [jQuery Validation](https://jqueryvalidation.org/) - Form validation

### Email xizmatlar
- **Gmail SMTP**: Bepul, lekin limitlangan
- **SendGrid**: Professional email xizmat
- **Mailgun**: Developer-friendly email API
- **Amazon SES**: AWS email xizmati

## Xulosa

Bu amaliyot orqali siz Django'da professional darajadagi contact form yaratishni o'rgandingiz. Form faqat ma'lumot to'plash emas, balki foydalanuvchi bilan sifatli muloqot vositasi bo'lishi kerak.

### Asosiy natijalar:
- ✅ To'liq ishlaydigan contact form
- ✅ Custom validatsiya
- ✅ Email yuborish funksiyasi
- ✅ Professional dizayn
- ✅ JavaScript interaktivligi
- ✅ Error handling
- ✅ Security best practices

### Esda tutingki:
- **Xavfsizlik** har doim birinchi o'rinda
- **Foydalanuvchi tajribasi** muhim
- **Kod sifati** maintainability uchun zarur
- **Testing** ishonchli loyiha uchun kerak
- **Monitoring** doimiy yaxshilash uchun muhim

Keyingi darsda biz Class-based FormView bilan tanishamiz va yanada ilg'or Django form texnikalarini o'rganamiz!