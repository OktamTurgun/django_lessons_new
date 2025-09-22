# Lesson 34: Amaliyot - Foydalanuvchi parolini qayta tiklash (1-qism)

## Amaliy mashg'ulot maqsadi

Bu amaliyotda siz o'z loyihangizdagi parol qayta tiklash funksiyasini ishga tushirasiz va test qilasiz.

## Boshlash shartlari

- Django loyihangiz tayyor
- User authentication tizimi ishlamoqda
- Login/Logout funksiyalari ishlaydi

## 1-qadam: Loyihani tayyorlash

### Folder strukturasini tekshirish

```
myproject/
├── accounts/
│   ├── urls.py
│   ├── views.py
│   └── ...
├── templates/
│   └── registration/
│       ├── login.html
│       └── ... (yangi fayllar qo'shiladi)
└── manage.py
```

### Virtual muhitni faollashtirish

```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

## 2-qadam: URLs konfiguratsiyasi

### accounts/urls.py faylini yangilash

Mavjud `accounts/urls.py` faylingizga quyidagi URLlarni qo'shing:

```python
# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Mavjud URLlaringiz (login, logout, va boshqalar)
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # YANGI: Parol qayta tiklash URLlari
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html'
         ),
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
```

### URL test qilish

Serverni ishga tushiring va URLlarni tekshiring:

```bash
python manage.py runserver
```

Quyidagi URLlarga kiring:
- `http://127.0.0.1:8000/accounts/password-reset/`

Agar xatolik chiqsa, URL konfiguratsiyasini qaytadan tekshiring.

## 3-qadam: Email sozlamalarini o'rnatish

### settings.py faylini yangilash

Loyihangizning `settings.py` fayliga quyidagilarni qo'shing:

```python
# settings.py ning oxirida

# Email sozlamalari (development uchun)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Parol qayta tiklash sozlamalari
PASSWORD_RESET_TIMEOUT = 3600  # 1 soat

# Email manzili
DEFAULT_FROM_EMAIL = 'admin@saytingiz.uz'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
```

### Settings.py ni test qilish

Django shell orqali email sozlamalarini tekshiring:

```bash
python manage.py shell
```

Shell ichida:

```python
from django.conf import settings
print(settings.EMAIL_BACKEND)
print(settings.PASSWORD_RESET_TIMEOUT)
```

## 4-qadam: Template fayllarini yaratish

### Registration papkasini yaratish

```bash
mkdir templates/registration
```

### 1. Password Reset Form templatei

`templates/registration/password_reset_form.html` yarating:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Parolni qayta tiklash{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0 text-center">
                        <i class="fas fa-key me-2"></i>
                        Parolni qayta tiklash
                    </h4>
                </div>
                <div class="card-body p-4">
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        Parolingizni unutdingizmi? Email manzilingizni kiriting va biz sizga 
                        yangi parol o'rnatish uchun havola yuboramiz.
                    </div>
                    
                    <form method="post">
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                            <div class="alert alert-danger">
                                <i class="fas fa-exclamation-triangle me-2"></i>
                                {{ form.non_field_errors }}
                            </div>
                        {% endif %}
                        
                        <div class="mb-3">
                            <label for="{{ form.email.id_for_label }}" class="form-label">
                                <i class="fas fa-envelope me-1"></i>
                                Email manzili
                            </label>
                            <input type="email" 
                                   class="form-control {% if form.email.errors %}is-invalid{% endif %}" 
                                   id="{{ form.email.id_for_label }}"
                                   name="{{ form.email.name }}"
                                   placeholder="email@example.com"
                                   required>
                            {% if form.email.errors %}
                                <div class="invalid-feedback">
                                    {{ form.email.errors }}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="d-grid gap-2">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-paper-plane me-2"></i>
                                Parolni qayta tiklash
                            </button>
                        </div>
                    </form>
                </div>
                <div class="card-footer text-center bg-light">
                    <small class="text-muted">
                        Hisobingizni eslaysizmi? 
                        <a href="{% url 'accounts:login' %}" class="text-decoration-none">
                            Bu yerga bosing
                        </a>
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 2. Password Reset Done templatei

`templates/registration/password_reset_done.html` yarating:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Email yuborildi{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-header bg-success text-white text-center">
                    <h4 class="mb-0">
                        <i class="fas fa-check-circle me-2"></i>
                        Email muvaffaqiyatli yuborildi!
                    </h4>
                </div>
                <div class="card-body p-4 text-center">
                    <div class="mb-4">
                        <i class="fas fa-envelope fa-4x text-success"></i>
                    </div>
                    
                    <h5 class="card-title">Ko'rsatmalar yuborildi</h5>
                    <p class="card-text lead">
                        Parolni qayta tiklash bo'yicha ko'rsatmalar sizning 
                        email manzilingizga yuborildi.
                    </p>
                    
                    <div class="alert alert-warning">
                        <i class="fas fa-exclamation-triangle me-2"></i>
                        <strong>Muhim:</strong> Email kelmagan bo'lsa, 
                        spam papkasini tekshiring!
                    </div>
                    
                    <div class="mt-4">
                        <a href="{% url 'accounts:login' %}" class="btn btn-outline-primary me-2">
                            <i class="fas fa-sign-in-alt me-2"></i>
                            Kirish sahifasi
                        </a>
                        <a href="{% url 'home' %}" class="btn btn-outline-secondary">
                            <i class="fas fa-home me-2"></i>
                            Bosh sahifa
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 5-qadam: Login templateini yangilash

Mavjud `templates/registration/login.html` faylingizga "Parolni unutdingizmi?" havolasini qo'shing:

Login formasining pastida quyidagini qo'shing:

```html
<!-- Login formasi oxirida -->
<div class="text-center mt-3">
    <p class="mb-1">
        <a href="{% url 'accounts:password_reset' %}" class="text-decoration-none">
            <i class="fas fa-question-circle me-1"></i>
            Parolni unutdingizmi?
        </a>
    </p>
</div>
```

## 6-qadam: Email template yaratish (ixtiyoriy)

### Custom email template

`templates/registration/password_reset_email.html` yarating:

```html
{% load i18n %}
{% autoescape off %}
Salom {{ user.get_username }},

Sizning {{ site_name }} saytidagi hisobingiz uchun parol qayta tiklash so'rovi keldi.

Parolni qayta tiklash uchun quyidagi havolaga bosing:
{{ protocol }}://{{ domain }}{% url 'accounts:password_reset_confirm' uidb64=uid token=token %}

Bu havola {{ timeout }} soat davomida amal qiladi.

Agar bu so'rovni siz yubormasangiz, bu xabarni e'tiborsiz qoldiring.

Hurmat bilan,
{{ site_name }} jamoasi

---
Bu avtomatik xabar. Javob bermang.
{% endautoescape %}
```

### Email subject

`templates/registration/password_reset_subject.txt` yarating:

```
{{ site_name }} - Parolni qayta tiklash so'rovi
```

## 7-qadam: Test qilish

### 1. Superuser yaratish (agar yo'q bo'lsa)

```bash
python manage.py createsuperuser
```

### 2. Serverni ishga tushirish

```bash
python manage.py runserver
```

### 3. Parol qayta tiklashni test qilish

1. `http://127.0.0.1:8000/accounts/login/` ga o'ting
2. "Parolni unutdingizmi?" havolasiga bosing
3. Mavjud foydalanuvchining email manzilini kiriting
4. "Parolni qayta tiklash" tugmasini bosing
5. Terminal/console da email matnini ko'ring

### 4. Console outputni tekshirish

Terminal da quyidagicha ko'rinishi kerak:

```
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit
Subject: Saytingiz - Parolni qayta tiklash so'rovi
From: admin@saytingiz.uz
To: user@example.com
Date: ...

Salom username,

Sizning sayt nomi saytidagi hisobingiz uchun parol qayta tiklash so'rovi keldi.

Parolni qayta tiklash uchun quyidagi havolaga bosing:
http://127.0.0.1:8000/accounts/password-reset-confirm/...
```

## 8-qadam: Xatoliklarni bartaraf etish

### 1. Template topilmadi xatosi

**Xato:** `TemplateDoesNotExist`

**Yechim:**
```python
# settings.py da TEMPLATES sozlamasini tekshiring
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],  # Bu qator bor ekanligini tekshiring
        # ...
    }
]
```

### 2. URL xatosi

**Xato:** `NoReverseMatch`

**Yechim:**
- URL nomlarini tekshiring
- `app_name = 'accounts'` qo'shilganligini tekshiring

### 3. Email yuborilmaydi

**Xato:** Email terminal da ko'rinmaydi

**Yechim:**
```python
# settings.py da
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## 9-qadam: Custom Form yaratish (qo'shimcha)

Agar standart form sizga mos kelmasa, o'z formangizni yarating:

### accounts/forms.py

```python
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="Email manzili",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sizning email manzilingiz',
            'autocomplete': 'email'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email, is_active=True).exists():
            raise forms.ValidationError("Bu email manzili bilan foydalanuvchi topilmadi.")
        return email
```

### URLs da custom form ishlatish

```python
# accounts/urls.py
from .forms import CustomPasswordResetForm

path('password-reset/', 
     auth_views.PasswordResetView.as_view(
         template_name='registration/password_reset_form.html',
         form_class=CustomPasswordResetForm  # Custom form qo'shish
     ),
     name='password_reset'),
```

## Natija

Ushbu amaliyotni bajarib bo'lgandan keyin sizda:

1. ✅ Parol qayta tiklash formasi ishlaydi
2. ✅ Email yuborish funksiyasi faol
3. ✅ Foydalanuvchi-do'st interfeys tayyor
4. ✅ Xavfsizlik tadbirlari amalga oshirilgan

## Keyingi qadam

Keyingi darsda (lesson_35) biz:
- Email orqali kelgan havolani qayta ishlashni o'rganamiz
- Yangi parol o'rnatish formasini yaratamiz
- To'liq parol qayta tiklash jarayonini yakunlaymiz

## Takrorlash savollari

1. **Django'da parol qayta tiklash necha bosqichdan iborat?**
   - Javob: 4 bosqich (Form, Done, Confirm, Complete)

2. **EMAIL_BACKEND ning Console va SMTP o'rtasidagi farq nima?**
   - Console: Development uchun, emailni terminalda ko'rsatadi
   - SMTP: Production uchun, haqiqiy email yuboradi

3. **`<uidb64>` va `<token>` URL parametrlari nima uchun ishlatiladi?**
   - uidb64: Foydalanuvchi ID sining base64 kodlanishi
   - token: Xavfsizlik uchun maxsus token

4. **PASSWORD_RESET_TIMEOUT nima vazifani bajaradi?**
   - Parol qayta tiklash havolasining amal qilish muddatini belgilaydi

## Qo'shimcha mashqlar

### Mashq 1: CSS Styling yaxshilash

Login va Password Reset sahifalariga qo'shimcha styling qo'shing:

```css
/* static/css/auth.css */
.auth-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
}

.auth-card {
    border: none;
    border-radius: 15px;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.auth-header {
    border-top-left-radius: 15px !important;
    border-top-right-radius: 15px !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.form-control:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}
```

### Mashq 2: Email template ni yaxshilash

Email templatega HTML format qo'shing:

```html
<!-- templates/registration/password_reset_email.html -->
{% load i18n %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Parol qayta tiklash</title>
    <style>
        .email-container {
            max-width: 600px;
            margin: 0 auto;
            font-family: Arial, sans-serif;
            line-height: 1.6;
        }
        .header {
            background-color: #007bff;
            color: white;
            padding: 20px;
            text-align: center;
        }
        .content {
            padding: 20px;
            background-color: #f8f9fa;
        }
        .button {
            display: inline-block;
            padding: 12px 24px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }
        .footer {
            padding: 20px;
            text-align: center;
            color: #666;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h2>{{ site_name }} - Parol qayta tiklash</h2>
        </div>
        <div class="content">
            <h3>Salom {{ user.get_username }}!</h3>
            <p>Sizning hisobingiz uchun parol qayta tiklash so'rovi keldi.</p>
            <p>Parolni qayta tiklash uchun quyidagi tugmaga bosing:</p>
            <div style="text-align: center;">
                <a href="{{ protocol }}://{{ domain }}{% url 'accounts:password_reset_confirm' uidb64=uid token=token %}" 
                   class="button">Parolni qayta tiklash</a>
            </div>
            <p><strong>Muhim:</strong> Bu havola {{ timeout }} soat davomida amal qiladi.</p>
            <p>Agar bu so'rovni siz yubormasangiz, bu xabarni e'tiborsiz qoldiring.</p>
        </div>
        <div class="footer">
            <p>Bu avtomatik xabar. Javob bermang.</p>
            <p>© {{ site_name }}. Barcha huquqlar himoyalangan.</p>
        </div>
    </div>
</body>
</html>
```

### Mashq 3: JavaScript validatsiyasi

Form validatsiyasini yaxshilash uchun JavaScript qo'shing:

```html
<!-- password_reset_form.html ga qo'shing -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const emailInput = document.querySelector('input[type="email"]');
    const submitBtn = document.querySelector('button[type="submit"]');
    
    // Email validation
    emailInput.addEventListener('input', function() {
        const email = this.value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (email && !emailRegex.test(email)) {
            this.classList.add('is-invalid');
            this.classList.remove('is-valid');
        } else if (email) {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        } else {
            this.classList.remove('is-invalid', 'is-valid');
        }
    });
    
    // Form submission
    form.addEventListener('submit', function(e) {
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Yuborilmoqda...';
        submitBtn.disabled = true;
    });
});
</script>
```

## Production uchun maslahatlar

### 1. SMTP konfiguratsiyasi

Production da haqiqiy email yuborish uchun:

```python
# settings.py (production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # yoki boshqa SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@saytingiz.com'
EMAIL_HOST_PASSWORD = 'app_password'  # Gmail uchun App Password

# Email manzillari
DEFAULT_FROM_EMAIL = 'noreply@saytingiz.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
```

### 2. Environment variables

Sensitive ma'lumotlarni environment variable sifatida saqlang:

```python
import os
from decouple import config

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

### 3. Rate limiting

Parol qayta tiklash so'rovlarini cheklash uchun:

```python
# accounts/views.py
from django.contrib.auth.decorators import ratelimit
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key='ip', rate='3/h', method='POST'), name='post')
class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
```

## Xatolarni debug qilish

### 1. Django Debug Toolbar

Development da email ni track qilish uchun:

```bash
pip install django-debug-toolbar
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]
```

### 2. Logging sozlash

Email yuborish jarayonini log qilish:

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'email.log',
        },
    },
    'loggers': {
        'django.core.mail': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Xavfsizlik bo'yicha maslahatlar

### 1. Email enumeration xujumlarini oldini olish

Foydalanuvchi mavjudligini tekshirmaslik uchun:

```python
# accounts/forms.py
class SecurePasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        # Har doim muvaffaqiyat xabarini ko'rsating
        # Haqiqiy email bor yoki yo'qligini aytmang
        return email
```

### 2. HTTPS ni majburiy qilish

```python
# settings.py (production)
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### 3. Token xavfsizligini oshirish

```python
# settings.py
PASSWORD_RESET_TIMEOUT = 1800  # 30 daqiqa (standart 3600)
```

## Test case yozish

### Unit test

```python
# accounts/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail

class PasswordResetTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_password_reset_form_display(self):
        response = self.client.get(reverse('accounts:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Parolni qayta tiklash')
    
    def test_password_reset_email_sent(self):
        response = self.client.post(reverse('accounts:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Parol qayta tiklash', mail.outbox[0].subject)
```

## Yakuniy tekshiruv ro'yxati

- [ ] URLs to'g'ri ishlaydi
- [ ] Template fayllar mavjud va to'g'ri
- [ ] Email backend sozlangan
- [ ] Login sahifasida "Parolni unutdingizmi?" havolasi bor
- [ ] Form validatsiyasi ishlaydi
- [ ] Email yuboriladi va terminlada ko'rinadi
- [ ] Password reset done sahifasi ko'rsatiladi
- [ ] Xatolik holatlarida to'g'ri xabarlar chiqadi
- [ ] CSS styling qo'llangan
- [ ] Mobile responsive dizayn

## Keyingi darsga tayyorgarlik

Lesson 35 uchun tayyorgarlik:
1. Email orqali kelgan havolani test qiling
2. Token va uidb64 parametrlarini tushunib oling
3. Yangi parol o'rnatish jarayoni haqida o'ylang

**Muvaffaqiyat!** Siz Django'da parol qayta tiklashning birinchi qismini muvaffaqiyatli amalga oshirdingiz.