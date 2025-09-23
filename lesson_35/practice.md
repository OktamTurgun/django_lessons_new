# Lesson 35: Amaliyot - Foydalanuvchi parolini qayta tiklash (2-qism)

## Amaliy mashg'ulot maqsadi

Bu amaliyotda lesson_34 da boshlanган parol qayta tiklash jarayonini yakunlaymiz va to'liq funksional qilib tayyorlaymiz.

## Boshlash shartlari

- Lesson_34 muvaffaqiyatli bajarilgan
- `password_reset_form.html` va `password_reset_done.html` templatelar tayyor
- Email backend sozlangan (console yoki SMTP)
- Django server ishlaydi

## 1-qadam: Qolgan templatelarni yaratish

### Password Reset Confirm template yaratish

`templates/registration/password_reset_confirm.html` faylini yarating:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Yangi parol o'rnatish{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h4 class="text-center mb-0">
                        <i class="fas fa-key me-2"></i>
                        Yangi parol o'rnatish
                    </h4>
                </div>
                <div class="card-body p-4">
                    {% if validlink %}
                        <!-- Token to'g'ri bo'lsa -->
                        <div class="alert alert-info">
                            <i class="fas fa-info-circle me-2"></i>
                            Xavfsizlik uchun yangi parolingizni ikki marta kiriting.
                        </div>
                        
                        <form method="post" id="passwordResetForm">
                            {% csrf_token %}
                            
                            {% if form.non_field_errors %}
                                <div class="alert alert-danger">
                                    <i class="fas fa-exclamation-triangle me-2"></i>
                                    {{ form.non_field_errors }}
                                </div>
                            {% endif %}
                            
                            <div class="mb-3">
                                <label for="{{ form.new_password1.id_for_label }}" class="form-label">
                                    <i class="fas fa-lock me-1"></i>
                                    Yangi parol
                                </label>
                                <div class="input-group">
                                    <input type="password" 
                                           class="form-control {% if form.new_password1.errors %}is-invalid{% endif %}" 
                                           id="{{ form.new_password1.id_for_label }}"
                                           name="{{ form.new_password1.name }}"
                                           placeholder="Yangi parolingizni kiriting"
                                           required>
                                    <button class="btn btn-outline-secondary" type="button" onclick="togglePassword('{{ form.new_password1.id_for_label }}')">
                                        <i class="fas fa-eye" id="toggleIcon1"></i>
                                    </button>
                                </div>
                                {% if form.new_password1.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ form.new_password1.errors }}
                                    </div>
                                {% endif %}
                                <div class="form-text">
                                    <small>
                                        <i class="fas fa-shield-alt me-1"></i>
                                        Parol kamida 8 ta belgi bo'lishi va faqat raqamlardan iborat bo'lmasligi kerak.
                                    </small>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <label for="{{ form.new_password2.id_for_label }}" class="form-label">
                                    <i class="fas fa-lock me-1"></i>
                                    Parolni takrorlang
                                </label>
                                <div class="input-group">
                                    <input type="password" 
                                           class="form-control {% if form.new_password2.errors %}is-invalid{% endif %}" 
                                           id="{{ form.new_password2.id_for_label }}"
                                           name="{{ form.new_password2.name }}"
                                           placeholder="Parolni qayta kiriting"
                                           required>
                                    <button class="btn btn-outline-secondary" type="button" onclick="togglePassword('{{ form.new_password2.id_for_label }}')">
                                        <i class="fas fa-eye" id="toggleIcon2"></i>
                                    </button>
                                </div>
                                {% if form.new_password2.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ form.new_password2.errors }}
                                    </div>
                                {% endif %}
                            </div>
                            
                            <!-- Password strength indicator -->
                            <div class="mb-3">
                                <div class="progress" style="height: 5px;">
                                    <div class="progress-bar" id="passwordStrength" role="progressbar" style="width: 0%"></div>
                                </div>
                                <small id="strengthText" class="text-muted">Parol kuchini ko'rsatish</small>
                            </div>
                            
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary btn-lg" id="submitBtn">
                                    <i class="fas fa-save me-2"></i>
                                    Parolni o'rnatish
                                </button>
                            </div>
                        </form>
                    {% else %}
                        <!-- Token noto'g'ri yoki muddati tugagan -->
                        <div class="text-center">
                            <div class="mb-4">
                                <i class="fas fa-exclamation-triangle fa-4x text-danger"></i>
                            </div>
                            
                            <div class="alert alert-danger">
                                <h5 class="alert-heading">
                                    <i class="fas fa-times-circle me-2"></i>
                                    Yaroqsiz havola
                                </h5>
                                <p class="mb-0">
                                    Parol qayta tiklash havolasi yaroqsiz yoki muddati tugagan bo'lishi mumkin.
                                </p>
                            </div>
                            
                            <div class="mt-4">
                                <a href="{% url 'accounts:password_reset' %}" class="btn btn-primary">
                                    <i class="fas fa-redo me-2"></i>
                                    Qaytadan so'rash
                                </a>
                                <a href="{% url 'accounts:login' %}" class="btn btn-outline-secondary ms-2">
                                    <i class="fas fa-sign-in-alt me-2"></i>
                                    Kirish sahifasi
                                </a>
                            </div>
                        </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>

<!-- JavaScript -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Password visibility toggle
    window.togglePassword = function(fieldId) {
        const field = document.getElementById(fieldId);
        const icon = document.querySelector(`button[onclick="togglePassword('${fieldId}')"] i`);
        
        if (field.type === "password") {
            field.type = "text";
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
        } else {
            field.type = "password";
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
        }
    };
    
    // Password strength checker
    const password1 = document.getElementById('{{ form.new_password1.id_for_label }}');
    const strengthBar = document.getElementById('passwordStrength');
    const strengthText = document.getElementById('strengthText');
    
    if (password1) {
        password1.addEventListener('input', function() {
            const password = this.value;
            const strength = calculatePasswordStrength(password);
            updateStrengthUI(strength);
        });
    }
    
    function calculatePasswordStrength(password) {
        let strength = 0;
        
        if (password.length >= 8) strength += 25;
        if (password.match(/[a-z]/)) strength += 25;
        if (password.match(/[A-Z]/)) strength += 25;
        if (password.match(/[0-9]/)) strength += 25;
        if (password.match(/[^a-zA-Z0-9]/)) strength += 25; // Special characters
        
        return Math.min(strength, 100);
    }
    
    function updateStrengthUI(strength) {
        strengthBar.style.width = strength + '%';
        
        if (strength < 25) {
            strengthBar.className = 'progress-bar bg-danger';
            strengthText.textContent = 'Juda zaif';
            strengthText.className = 'text-danger';
        } else if (strength < 50) {
            strengthBar.className = 'progress-bar bg-warning';
            strengthText.textContent = 'Zaif';
            strengthText.className = 'text-warning';
        } else if (strength < 75) {
            strengthBar.className = 'progress-bar bg-info';
            strengthText.textContent = 'O\'rtacha';
            strengthText.className = 'text-info';
        } else {
            strengthBar.className = 'progress-bar bg-success';
            strengthText.textContent = 'Kuchli';
            strengthText.className = 'text-success';
        }
    }
    
    // Form submission
    const form = document.getElementById('passwordResetForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = document.getElementById('submitBtn');
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saqlanmoqda...';
            submitBtn.disabled = true;
        });
    }
});
</script>
{% endblock %}
```

### Password Reset Complete template yaratish

`templates/registration/password_reset_complete.html` faylini yarating:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Parol muvaffaqiyatli o'zgartirildi{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-header bg-success text-white text-center">
                    <h4 class="mb-0">
                        <i class="fas fa-check-circle me-2"></i>
                        Muvaffaqiyat!
                    </h4>
                </div>
                <div class="card-body p-4 text-center">
                    <div class="mb-4">
                        <i class="fas fa-shield-check fa-5x text-success animate__animated animate__bounceIn"></i>
                    </div>
                    
                    <h5 class="card-title text-success mb-3">
                        Parolingiz muvaffaqiyatli o'zgartirildi
                    </h5>
                    
                    <p class="card-text lead mb-4">
                        Tabriklaymiz! Endi yangi parolingiz bilan hisobingizga xavfsiz kirishingiz mumkin.
                    </p>
                    
                    <div class="alert alert-info">
                        <i class="fas fa-lightbulb me-2"></i>
                        <strong>Maslahat:</strong> Parolingizni xavfsiz joyda saqlang va hech kimga aytmang.
                    </div>
                    
                    <div class="mt-4">
                        <a href="{% url 'accounts:login' %}" class="btn btn-success btn-lg me-2">
                            <i class="fas fa-sign-in-alt me-2"></i>
                            Hisobga kirish
                        </a>
                        <a href="{% url 'home' %}" class="btn btn-outline-primary">
                            <i class="fas fa-home me-2"></i>
                            Bosh sahifa
                        </a>
                    </div>
                </div>
                <div class="card-footer bg-light text-center">
                    <small class="text-muted">
                        <i class="fas fa-clock me-1"></i>
                        {{ "now"|date:"d.m.Y H:i" }} da yangilandi
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Success sound (ixtiyoriy) -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Success animation
    setTimeout(function() {
        const icon = document.querySelector('.fa-shield-check');
        if (icon) {
            icon.classList.add('animate__animated', 'animate__pulse');
        }
    }, 1000);
    
    // Auto redirect (ixtiyoriy)
    let countdown = 10;
    const loginBtn = document.querySelector('a[href*="login"]');
    
    if (loginBtn) {
        const interval = setInterval(function() {
            countdown--;
            if (countdown > 0) {
                loginBtn.innerHTML = `<i class="fas fa-sign-in-alt me-2"></i>Hisobga kirish (${countdown})`;
            } else {
                clearInterval(interval);
                // Uncomment quyidagi qatorni auto-redirect uchun
                // window.location.href = loginBtn.href;
            }
        }, 1000);
    }
});
</script>
{% endblock %}
```

## 2-qadam: Custom Email Template yaratish

### HTML Email template

`templates/registration/password_reset_email.html` faylini yarating:

```html
{% load i18n %}
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="utf-8">
    <title>Parol qayta tiklash</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .email-container {
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .header {
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        .content {
            padding: 30px 20px;
        }
        .button {
            display: inline-block;
            padding: 15px 30px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            margin: 20px 0;
            text-align: center;
            transition: background-color 0.3s;
        }
        .button:hover {
            background: #0056b3;
            color: white;
        }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
            border-top: 1px solid #e9ecef;
        }
        .warning {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            color: #856404;
            padding: 15px;
            border-radius: 0 5px 5px 0;
            margin: 15px 0;
        }
        .link-box {
            background: #f8f9fa;
            border: 2px dashed #007bff;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            word-break: break-all;
            font-family: monospace;
            font-size: 12px;
        }
        .info-box {
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 15px;
            margin: 15px 0;
            border-radius: 0 5px 5px 0;
        }
        h1, h2, h3 {
            margin-top: 0;
        }
        .emoji {
            font-size: 1.2em;
        }
    </style>
</head>
<body>
    {% autoescape off %}
    <div class="email-container">
        <div class="header">
            <h1 style="margin: 0;">🔐 {{ site_name }}</h1>
            <p style="margin: 10px 0 0 0; font-size: 18px;">Parol qayta tiklash so'rovi</p>
        </div>
        
        <div class="content">
            <h2>Salom, {{ user.get_username }}!</h2>
            
            <p>Sizning <strong>{{ site_name }}</strong> saytidagi hisobingiz uchun parol qayta tiklash so'rovi yuborildi.</p>
            
            <div class="info-box">
                <p><strong>📋 So'rov ma'lumotlari:</strong></p>
                <ul style="margin: 10px 0;">
                    <li><strong>Foydalanuvchi:</strong> {{ user.get_username }}</li>
                    <li><strong>Email:</strong> {{ user.email }}</li>
                    <li><strong>Vaqt:</strong> {{ "now"|date:"d.m.Y H:i" }}</li>
                </ul>
            </div>
            
            <p>Parolingizni qayta tiklash uchun quyidagi tugmaga bosing:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{{ protocol }}://{{ domain }}{% url 'accounts:password_reset_confirm' uidb64=uid token=token %}" class="button">
                    🔑 Parolni qayta tiklash
                </a>
            </div>
            
            <div class="warning">
                <p><strong>⚠️ Muhim ma'lumot:</strong></p>
                <ul style="margin: 10px 0;">
                    <li>Bu havola faqat <strong>1 soat</strong> davomida amal qiladi</li>
                    <li>Havola faqat bir marta ishlatilishi mumkin</li>
                    <li>Yangi parol o'rnatgandan keyin eski tokenlar ishlamaydi</li>
                </ul>
            </div>
            
            <p><strong>Agar tugma ishlamasa</strong>, quyidagi havolani nusxalab brauzeringizga qo'ying:</p>
            
            <div class="link-box">
                {{ protocol }}://{{ domain }}{% url 'accounts:password_reset_confirm' uidb64=uid token=token %}
            </div>
            
            <div class="info-box">
                <p><strong>🛡️ Xavfsizlik maslahatlar:</strong></p>
                <ul>
                    <li>Kuchli parol tanlang (kamida 8 belgi, harflar, raqamlar, belgilar)</li>
                    <li>Parolni boshqa hech qayerda ishlatmang</li>
                    <li>Parolni muntazam o'zgartirib turing</li>
                </ul>
            </div>
            
            <p><strong>❌ Agar bu so'rovni siz yubormasangiz:</strong></p>
            <ul>
                <li>Bu xabarni e'tiborsiz qoldiring</li>
                <li>Sizning hisobingiz xavfsiz</li>
                <li>Hech qanday harakat talab qilinmaydi</li>
                <li>Agar shubha bo'lsa, bizga murojaat qiling</li>
            </ul>
        </div>
        
        <div class="footer">
            <p><strong>{{ site_name }} jamoasi</strong></p>
            <p>📧 Bu avtomatik xabar. Iltimos javob bermang.</p>
            <p>🌐 <a href="{{ protocol }}://{{ domain }}" style="color: #007bff;">{{ domain }}</a></p>
            <p>© {{ "now"|date:"Y" }} {{ site_name }}. Barcha huquqlar himoyalangan.</p>
        </div>
    </div>
    {% endautoescape %}
</body>
</html>
```

### Email Subject

`templates/registration/password_reset_subject.txt` faylini yangilang:

```
🔐 {{ site_name }} - Parol qayta tiklash so'rovi ({{ user.get_username }})
```

## 3-qadam: SMTP Email sozlamalarini o'rnatish

### Development uchun Gmail SMTP

`settings.py` faylingizni yangilang:

```python
# settings.py

# Email sozlamalari
if DEBUG:
    # Development - Console backend
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # Production - SMTP backend
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Email manzillari
DEFAULT_FROM_EMAIL = f'Django Sayt <{EMAIL_HOST_USER or "noreply@example.com"}>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# Parol qayta tiklash sozlamalari
PASSWORD_RESET_TIMEOUT = 3600  # 1 soat (sekundlarda)

# Site sozlamalari (ixtiyoriy)
SITE_NAME = 'Django Sayt'
```

### Environment Variables o'rnatish

Loyihangiz ildizida `.env` fayl yarating:

```bash
# .env
EMAIL_HOST_USER=sizning_email@gmail.com
EMAIL_HOST_PASSWORD=sizning_gmail_app_password
DEBUG=True
SECRET_KEY=sizning_secret_key
```

### Django-decouple o'rnatish

```bash
pip install python-decouple
```

Settings.py da ishlatish:

```python
# settings.py
from decouple import config
import os

# Gmail orqali email yuborish uchun
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
```

## 4-qadam: Gmail App Password olish

### Gmail 2-Factor Authentication yoqish

1. Gmail hisobingizga kiring
2. **Google Account** > **Security**
3. **2-Step Verification** ni yoqing
4. Telefon raqami bilan tasdiqlash

### App Password yaratish

1. **Google Account** > **Security** > **2-Step Verification**
2. **App passwords** ni tanlang
3. **Select app** > **Mail**
4. **Select device** > **Other** (Django loyiha nomi)
5. **Generate** tugmasini bosing
6. Hosil bo'lgan 16 raqamli parolni `.env` ga qo'ying

## 5-qadam: To'liq test qilish

### 1. Console Backend bilan test

```bash
# Virtual environment faollashtirish
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows

# Server ishga tushirish
python manage.py runserver
```

### 2. Parol qayta tiklash jarayoni test

1. **Form test**: `http://127.0.0.1:8000/accounts/password-reset/`
2. Mavjud email manzilini kiriting
3. **Done page** ko'rinishini tekshiring
4. **Terminal da email** ni ko'ring
5. **Emaildagi havolaga** bosing
6. **Password reset confirm** sahifasini test qiling
7. Yangi parol kiriting
8. **Complete page** ko'rinishini tekshiring

### 3. Login bilan test

1. Yangi parol bilan login qiling
2. Muvaffaqiyatli kirish mumkinligini tekshiring

## 6-qadam: Production uchun SMTP test

### Settings.py ni o'zgartirish

```python
# Test uchun vaqtincha
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

### SMTP xatolarini bartaraf etish

#### 1. Authentication xatosi

```python
# Gmail App Password to'g'ri kiritilganini tekshiring
# Oddiy Gmail parol ishlamaydi, faqat App Password
```

#### 2. Connection xatosi

```python
# Internet connection va firewall tekshiring
# Gmail SMTP: smtp.gmail.com:587
```

#### 3. TLS xatosi

```python
EMAIL_USE_TLS = True  # Gmail uchun True bo'lishi kerak
# EMAIL_USE_SSL = False  # TLS bilan ishlatilmaydi
```

## 7-qadam: Custom Forms yaratish (Qo'shimcha)

### Custom Password Reset Form

`accounts/forms.py` yarating:

```python
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
import re

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
            # Xavfsizlik uchun haqiqiy xatolikni ko'rsatmang
            pass  # Har doim success qaytaradi
        return email

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Yangi parol",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kamida 8 ta belgi',
            'autocomplete': 'new-password'
        }),
    )
    new_password2 = forms.CharField(
        label="Parolni tasdiqlash",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni qayta kiriting',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )
    
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        
        # Custom validations
        if len(password) < 8:
            raise forms.ValidationError("Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
        
        if password.isdigit():
            raise forms.ValidationError("Parol faqat raqamlardan iborat bo'lmasligi kerak.")
        
        if not re.search(r'[A-Za-z]', password):
            raise forms.ValidationError("Parolda kamida bitta harf bo'lishi kerak.")
        
        return password
```

### URLs da custom form ishlatish

```python
# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm

app_name = 'accounts'

urlpatterns = [
    # Custom forms bilan
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             form_class=CustomPasswordResetForm,
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt'
         ),
         name='password_reset'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             form_class=CustomSetPasswordForm
         ),
         name='password_reset_confirm'),
    
    # Qolgan URLlar...
]
```

## 8-qadam: JavaScript yaxshilashlari

### Static fayllar yaratish

`static/js/password-reset.js` yarating:

```javascript
// static/js/password-reset.js
document.addEventListener('DOMContentLoaded', function() {
    // Password strength calculator
    function calculatePasswordStrength(password) {
        let score = 0;
        
        // Length check
        if (password.length >= 8) score += 25;
        if (password.length >= 12) score += 25;
        
        // Character variety
        if (/[a-z]/.test(password)) score += 10;
        if (/[A-Z]/.test(password)) score += 10;
        if (/[0-9]/.test(password)) score += 10;
        if (/[^A-Za-z0-9]/.test(password)) score += 20;
        
        return Math.min(score, 100);
    }
    
    // Real-time password validation
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(field => {
        field.addEventListener('input', function() {
            validatePasswordRealTime(this);
        });
    });
    
    function validatePasswordRealTime(field) {
        const password = field.value;
        const feedbackDiv = field.parentNode.querySelector('.invalid-feedback') || 
                           field.parentNode.parentNode.querySelector('.invalid-feedback');
        
        // Remove existing classes
        field.classList.remove('is-valid', 'is-invalid');
        
        if (password.length === 0) return;
        
        const strength = calculatePasswordStrength(password);
        
        if (strength < 50) {
            field.classList.add('is-invalid');
            if (feedbackDiv) {
                feedbackDiv.textContent = 'Parol juda zaif. Yanada kuchli parol tanlang.';
                feedbackDiv.style.display = 'block';
            }
        } else {
            field.classList.add('is-valid');
            if (feedbackDiv) {
                feedbackDiv.style.display = 'none';
            }
        }
    }
    
    // Password match validation
    const password1 = document.querySelector('input[name="new_password1"]');
    const password2 = document.querySelector('input[name="new_password2"]');
    
    if (password1 && password2) {
        password2.addEventListener('input', function() {
            if (this.value && password1.value !== this.value) {
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
            } else if (this.value && password1.value === this.value) {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    }
    
    // Form submission protection
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saqlanmoqda...';
                
                // Agar 5 soniyadan keyin response kelmasa, button ni qayta yoq
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 5000);
            }
        });
    });
});
```

### CSS yaxshilashlari

`static/css/password-reset.css` yarating:

```css
/* static/css/password-reset.css */
.password-reset-container {
    min-height: 100vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
}

.password-reset-card {
    border: none;
    border-radius: 15px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    background: rgba(255, 255, 255, 0.95);
}

.password-reset-header {
    border-top-left-radius: 15px !important;
    border-top-right-radius: 15px !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.strength-indicator {
    height: 6px;
    background: #e9ecef;
    border-radius: 3px;
    overflow: hidden;
    margin-top: 5px;
}

.strength-bar {
    height: 100%;
    transition: all 0.3s ease;
}

.strength-weak { background: #dc3545; }
.strength-medium { background: #ffc107; }
.strength-good { background: #20c997; }
.strength-strong { background: #28a745; }

.form-control:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.animated-icon {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

/* Toast notifications */
.toast {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 1050;
}
```

## 9-qadam: Logging va Monitoring

### Logging sozlash

`settings.py` ga logging qo'shing:

```python
# settings.py

import os

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {name} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'password_reset.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.core.mail': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'accounts': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Logs papkasini yaratish
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
```

### Custom logging views

`accounts/views.py` yarating:

```python
# accounts/views.py
import logging
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

logger = logging.getLogger('accounts')

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email, is_active=True)
            logger.info(f'Password reset requested for user: {user.username} ({email})')
        except User.DoesNotExist:
            logger.warning(f'Password reset attempted for non-existent email: {email}')
        
        return super().form_valid(form)

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    
    def form_valid(self, form):
        user = form.user
        logger.info(f'Password successfully reset for user: {user.username} ({user.email})')
        return super().form_valid(form)
```

## 10-qadam: Rate Limiting qo'shish

### Django-ratelimit o'rnatish

```bash
pip install django-ratelimit
```

### Rate limiting qo'llash

```python
# accounts/views.py
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

@method_decorator(ratelimit(key='ip', rate='3/h', method='POST', block=True), name='post')
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        # Rate limit exceededni handle qilish
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.warning(f'Rate limit exceeded for IP: {request.META.get("REMOTE_ADDR")}')
            return self.render_to_response(self.get_context_data(
                form=self.get_form(),
                rate_limited=True
            ))
```

### Template da rate limiting xabarini ko'rsatish

`password_reset_form.html` ga qo'shing:

```html
{% if rate_limited %}
<div class="alert alert-warning">
    <i class="fas fa-exclamation-triangle me-2"></i>
    <strong>Juda ko'p urinish!</strong> 
    Iltimos, 1 soat kutib turing va qaytadan urinib ko'ring.
</div>
{% endif %}
```

## 11-qadam: Unit Testing

### Test faylini yaratish

`accounts/tests.py` yarating:

```python
# accounts/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpassword123'
        )
        self.reset_url = reverse('accounts:password_reset')
    
    def test_password_reset_form_display(self):
        """Password reset formasi to'g'ri ko'rsatilishini test qilish"""
        response = self.client.get(self.reset_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Parolni qayta tiklash')
        self.assertContains(response, 'email')
    
    def test_password_reset_valid_email(self):
        """Mavjud email bilan parol qayta tiklashni test qilish"""
        response = self.client.post(self.reset_url, {
            'email': 'test@example.com'
        })
        
        # Redirectni tekshirish
        self.assertEqual(response.status_code, 302)
        
        # Email yuborilganligini tekshirish
        self.assertEqual(len(mail.outbox), 1)
        
        # Email mazmunini tekshirish
        email = mail.outbox[0]
        self.assertIn('Parol qayta tiklash', email.subject)
        self.assertIn('testuser', email.body)
    
    def test_password_reset_invalid_email(self):
        """Mavjud bo'lmagan email bilan test qilish"""
        response = self.client.post(self.reset_url, {
            'email': 'nonexistent@example.com'
        })
        
        # Django xavfsizlik sababli har doim success qaytaradi
        self.assertEqual(response.status_code, 302)
        
        # Ammo email yuborilmasligi kerak
        self.assertEqual(len(mail.outbox), 0)
    
    def test_password_reset_confirm_valid_token(self):
        """To'g'ri token bilan parol o'zgartirishni test qilish"""
        # Token va uidb64 yaratish
        token = default_token_generator.make_token(self.user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        # Password reset confirm URL
        confirm_url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': uidb64,
            'token': token
        })
        
        # GET request - formani ko'rsatish
        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yangi parol')
        
        # POST request - parolni o'zgartirish
        response = self.client.post(confirm_url, {
            'new_password1': 'newstrongpassword123',
            'new_password2': 'newstrongpassword123'
        })
        
        # Muvaffaqiyatli o'zgartirishdan keyin redirect
        self.assertEqual(response.status_code, 302)
        
        # Parol o'zgarganligini tekshirish
        updated_user = User.objects.get(pk=self.user.pk)
        self.assertTrue(updated_user.check_password('newstrongpassword123'))
        self.assertFalse(updated_user.check_password('oldpassword123'))
    
    def test_password_reset_confirm_invalid_token(self):
        """Noto'g'ri token bilan test qilish"""
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        invalid_token = 'invalid-token-123'
        
        confirm_url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': uidb64,
            'token': invalid_token
        })
        
        response = self.client.get(confirm_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yaroqsiz havola')
    
    def test_password_mismatch(self):
        """Parollar mos kelmasligi holatini test qilish"""
        token = default_token_generator.make_token(self.user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        confirm_url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': uidb64,
            'token': token
        })
        
        response = self.client.post(confirm_url, {
            'new_password1': 'password123',
            'new_password2': 'differentpassword123'
        })
        
        # Form xatolik bilan qaytarilishi kerak
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'mos kelmadi')  # Error message
    
    def test_weak_password_validation(self):
        """Zaif parol validatsiyasini test qilish"""
        token = default_token_generator.make_token(self.user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        confirm_url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': uidb64,
            'token': token
        })
        
        # Juda qisqa parol
        response = self.client.post(confirm_url, {
            'new_password1': '123',
            'new_password2': '123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'new_password2', 
                           'This password is too short. It must contain at least 8 characters.')
```

### Testlarni ishga tushirish

```bash
# Barcha testlar
python manage.py test

# Faqat accounts app testlari
python manage.py test accounts

# Ma'lum bir test class
python manage.py test accounts.tests.PasswordResetTestCase

# Verbose output bilan
python manage.py test accounts --verbosity=2
```

## 12-qadam: Performance Optimization

### Database indexing

```python
# accounts/models.py (agar custom user model bo'lsa)
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)  # Index qo'shish
    
    class Meta:
        indexes = [
            models.Index(fields=['email', 'is_active']),  # Composite index
            models.Index(fields=['date_joined']),
        ]
```

### Caching

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# Email rate limiting uchun cache
from django.core.cache import cache

def check_email_rate_limit(email):
    key = f'password_reset_{email}'
    attempts = cache.get(key, 0)
    if attempts >= 3:
        return False
    cache.set(key, attempts + 1, timeout=3600)  # 1 soat
    return True
```

## 13-qadam: Security Headers

### Django Security Middleware

```python
# settings.py (Production uchun)

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000  # 1 yil
SECURE_REDIRECT_EXEMPT = []
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_SSL_REDIRECT = True

# CSP Headers
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net")
```

## 14-qadam: Yakuniy tekshiruv

### Barcha funksiyalarni test qiling:

1. **Password Reset Form** ✅
   - [ ] Form ko'rinadi
   - [ ] Email validation ishlaydi
   - [ ] CSRF token bor
   - [ ] Success redirect ishlaydi

2. **Email Functionality** ✅
   - [ ] Console/SMTP backend ishlaydi
   - [ ] Email template to'g'ri render qilinadi
   - [ ] Subject to'g'ri
   - [ ] Havola to'g'ri yaratiladi

3. **Password Reset Confirm** ✅
   - [ ] Valid token bilan form ochiladi
   - [ ] Invalid token da error ko'rsatiladi
   - [ ] Password strength indicator ishlaydi
   - [ ] Password visibility toggle ishlaydi

4. **Password Reset Complete** ✅
   - [ ] Success message ko'rsatiladi
   - [ ] Login havolasi ishlaydi
   - [ ] Auto-redirect ishlaydi (agar yoqilgan bo'lsa)

5. **Security Features** ✅
   - [ ] Rate limiting ishlaydi
   - [ ] HTTPS redirect (production)
   - [ ] Secure headers o'rnatilgan
   - [ ] Token timeout ishlaydi

### Browser compatibility test

```javascript
// Browser compatibility check
function checkBrowserSupport() {
    const features = {
        fetch: 'fetch' in window,
        promises: 'Promise' in window,
        es6: (() => {
            try {
                eval('class TestClass {}');
                return true;
            } catch (e) {
                return false;
            }
        })()
    };
    
    console.log('Browser support:', features);
}
```

## 15-qadam: Deployment Checklist

### Production uchun tayyorgarlik

```python
# settings/production.py
import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Static Files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
```

### Environment variables (.env production)

```bash
# Production .env
DEBUG=False
SECRET_KEY=your-super-secret-production-key
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-app-password
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```

## Xulosa

Tabriklaymiz! Siz Django'da to'liq parol qayta tiklash tizimini muvaffaqiyatli yaratdingiz. 

### Nima amalga oshirdik:

1. ✅ **To'liq 4-bosqichli parol qayta tiklash**
2. ✅ **Professional email template**  
3. ✅ **SMTP email yuborish**
4. ✅ **Custom forms va validation**
5. ✅ **JavaScript interaktivlik**
6. ✅ **Security features**
7. ✅ **Unit testing**
8. ✅ **Performance optimization**
9. ✅ **Production deployment**

### Keyingi qadam

Keyingi darsda (lesson_36) biz **Signup** funksiyasini yaratamiz:
- Custom user registration
- Email verification  
- Account activation
- User profile setup

**Ajoyib ish!** Endi foydalanuvchilar parollarini xavfsiz tarzda qayta tiklay oladilar.