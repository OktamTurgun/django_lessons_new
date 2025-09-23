# Lesson 35: Foydalanuvchi parolini qayta tiklash (2-qism)

## Kirish

Lesson_34 da biz parol qayta tiklash jarayonining birinchi qismini - form va email yuborishni amalga oshirdik. Endi ikkinchi qismda email orqali kelgan havolani qayta ishlash va yangi parol o'rnatish jarayonini yakunlaymiz.

Bu darsda o'rganadigan mavzular:
- Password Reset Confirm templateni yaratish
- Password Reset Complete templateni yaratish
- Email orqali kelgan token va uidb64 parametrlarini tushunish
- Production muhitda SMTP email sozlamalari
- Custom email templatelarini yaratish
- Xavfsizlik va best practice'lar

## Django parol qayta tiklash jarayonining davomi

Lesson_34 da biz 4 bosqichning birinchi 2 tasini bajargan edik:

1. ✅ **Password Reset Form** - Foydalanuvchi email kiritadi
2. ✅ **Password Reset Done** - Email yuborildi xabari
3. 🔄 **Password Reset Confirm** - Yangi parol o'rnatish (bu darsda)
4. 🔄 **Password Reset Complete** - Muvaffaqiyat xabari (bu darsda)

## 1-bosqich: Password Reset Confirm Template

Bu template email orqali kelgan havola bosilganda ochiladi va yangi parol o'rnatish formasini ko'rsatadi.

**templates/registration/password_reset_confirm.html**:

```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yangi parol o'rnatish</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-light">
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
                            
                            <form method="post">
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
                                
                                <div class="d-grid gap-2">
                                    <button type="submit" class="btn btn-primary btn-lg">
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

    <!-- JavaScript for password visibility toggle -->
    <script>
        function togglePassword(fieldId) {
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
        }
    </script>
</body>
</html>
```

### Template tushuntirishlari:

#### validlink o'zgaruvchisi
Django avtomatik ravishda `validlink` o'zgaruvchisini template'ga yuboradi:
- `True` - Token to'g'ri va muddati tugamagan
- `False` - Token noto'g'ri yoki muddati tugagan

#### Form fields
- `form.new_password1` - Yangi parol
- `form.new_password2` - Parolni tasdiqlash

## 2-bosqich: Password Reset Complete Template

Bu template parol muvaffaqiyatli o'zgartirilganda ko'rsatiladi.

**templates/registration/password_reset_complete.html**:

```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parol muvaffaqiyatli o'zgartirildi</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-light">
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
                            <i class="fas fa-shield-check fa-5x text-success"></i>
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
</body>
</html>
```

## 3-bosqich: Custom Email Template yaratish

Django'ning standart email templatei oddiy. Biz uni yaxshiroq qilamiz.

**templates/registration/password_reset_email.html**:

```html
{% load i18n %}
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="utf-8">
    <title>Parol qayta tiklash</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            padding: 30px 20px;
            text-align: center;
            border-radius: 10px 10px 0 0;
        }
        .content {
            background: #f8f9fa;
            padding: 30px 20px;
            border-left: 1px solid #dee2e6;
            border-right: 1px solid #dee2e6;
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
        }
        .button:hover {
            background: #0056b3;
            color: white;
        }
        .footer {
            background: #e9ecef;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 14px;
            border-radius: 0 0 10px 10px;
            border: 1px solid #dee2e6;
        }
        .warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }
        .link-box {
            background: white;
            border: 2px dashed #007bff;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            word-break: break-all;
        }
    </style>
</head>
<body>
    {% autoescape off %}
    <div class="header">
        <h2 style="margin: 0;">🔐 {{ site_name }}</h2>
        <p style="margin: 10px 0 0 0;">Parol qayta tiklash so'rovi</p>
    </div>
    
    <div class="content">
        <h3>Salom, {{ user.get_username }}!</h3>
        
        <p>Sizning <strong>{{ site_name }}</strong> saytidagi hisobingiz uchun parol qayta tiklash so'rovi yuborildi.</p>
        
        <p>Parolingizni qayta tiklash uchun quyidagi tugmaga bosing:</p>
        
        <div style="text-align: center;">
            <a href="{{ protocol }}://{{ domain }}{% url 'accounts:password_reset_confirm' uidb64=uid token=token %}" class="button">
                🔑 Parolni qayta tiklash
            </a>
        </div>
        
        <div class="warning">
            <strong>⚠️ Muhim ma'lumot:</strong>
            <ul style="margin: 10px 0;">
                <li>Bu havola faqat <strong>{{ timeout }} soat</strong> davomida amal qiladi</li>
                <li>Havola faqat bir marta ishlatilishi mumkin</li>
                <li>Agar tugma ishlamasa, quyidagi havolani nusxalab brauzeringizga qo'ying</li>
            </ul>
        </div>
        
        <div class="link-box">
            <strong>To'liq havola:</strong><br>
            {{ protocol }}://{{ domain }}{% url 'accounts:password_reset_confirm' uidb64=uid token=token %}
        </div>
        
        <p><strong>Agar bu so'rovni siz yubormasangiz:</strong></p>
        <ul>
            <li>Bu xabarni e'tiborsiz qoldiring</li>
            <li>Sizning hisobingiz xavfsiz</li>
            <li>Hech qanday harakat talab qilinmaydi</li>
        </ul>
    </div>
    
    <div class="footer">
        <p><strong>{{ site_name }} jamoasi</strong></p>
        <p>📧 Bu avtomatik xabar. Iltimos javob bermang.</p>
        <p>© {{ "now"|date:"Y" }} {{ site_name }}. Barcha huquqlar himoyalangan.</p>
    </div>
    {% endautoescape %}
</body>
</html>
```

### Email subject template

**templates/registration/password_reset_subject.txt**:

```
🔐 {{ site_name }} - Parol qayta tiklash so'rovi
```

## 4-bosqich: Production uchun SMTP sozlamalari

Development da console backend ishlatgan edik. Production uchun haqiqiy email yuborish kerak.

### Gmail SMTP sozlamalari

**settings.py**:

```python
# Email sozlamalari (Production)
import os
from decouple import config

# SMTP Backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Gmail SMTP sozlamalari
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')  # Environment variable
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')  # App Password

# Email manzillari
DEFAULT_FROM_EMAIL = f'{config("SITE_NAME", default="Django Site")} <{EMAIL_HOST_USER}>'
SERVER_EMAIL = EMAIL_HOST_USER

# Parol qayta tiklash sozlamalari
PASSWORD_RESET_TIMEOUT = 3600  # 1 soat (sekundlarda)

# Site sozlamalari
SITE_ID = 1
SITE_NAME = config('SITE_NAME', default='Django Sayt')
```

### Environment Variables (.env file)

Loyihangiz ildizida `.env` fayl yarating:

```bash
# .env
EMAIL_HOST_USER=sizning_email@gmail.com
EMAIL_HOST_PASSWORD=sizning_app_parolingiz
SITE_NAME=Mening Web Saytim
```

### Gmail App Password olish

1. Google hisobingizga kiring
2. **Google Account** > **Security** > **2-Step Verification**
3. **App passwords** ni tanlang
4. Yangi app password yarating
5. Bu parolni `.env` faylda ishlatting

### Boshqa email providerlar

#### Yandex SMTP:
```python
EMAIL_HOST = 'smtp.yandex.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

#### Mail.ru SMTP:
```python
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

#### Custom SMTP:
```python
EMAIL_HOST = 'your-smtp-server.com'
EMAIL_PORT = 587  # yoki 465 SSL uchun
EMAIL_USE_TLS = True  # yoki EMAIL_USE_SSL = True
```

## 5-bosqich: Token va uidb64 tushuntirish

Django parol qayta tiklash uchun 2 ta parameter ishlatadi:

### uidb64
- Foydalanuvchi ID sining base64 kodlanishi
- Misol: `user.pk = 5` → `uidb64 = "NQ"`

```python
# Django ichida qanday ishlaydi:
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

user_id = 5
uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
print(uidb64)  # "NQ"
```

### token
- Foydalanuvchi va vaqt asosida yaratilgan xavfsizlik token
- Har bir so'rov uchun noyob
- Muayyan vaqtdan keyin amal qilmaydi

```python
# Django ichida token yaratish:
from django.contrib.auth.tokens import default_token_generator

token = default_token_generator.make_token(user)
print(token)  # "5z8-a4f2c8d1e9b7f3a6"
```

### URL structure
```
/accounts/password-reset-confirm/NQ/5z8-a4f2c8d1e9b7f3a6/
                                ↑    ↑
                            uidb64  token
```

## 6-bosqich: Xavfsizlik masalalari

### 1. Token xavfsizligi
- Token foydalanuvchi parolidan yasaladi
- Parol o'zgartirilsa, eski tokenlar ishlamaydi
- Vaqt chegarasi bor (default: 3 kun)

### 2. Brute Force hujumlari oldini olish

**Rate limiting qo'shish:**

```python
# accounts/views.py
from django.contrib.auth.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.contrib.auth import views as auth_views

@method_decorator(ratelimit(key='ip', rate='3/h', method='POST'), name='post')
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
```

### 3. Email enumeration hujumlar

Attackerlar email mavjudligini tekshirishi mumkin. Buni oldini olish uchun:

```python
# accounts/forms.py
from django.contrib.auth.forms import PasswordResetForm

class SecurePasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        # Har doim success ko'rsating, email bor yoki yo'q
        return email
```

### 4. HTTPS majburiy qilish

```python
# settings.py (Production)
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

## 7-bosqich: Custom Views yaratish

Agar Django'ning standart viewlari kifoya qilmasa:

```python
# accounts/views.py
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.template.loader import render_to_string

class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')
    
    def form_valid(self, form):
        # Custom logic qo'shish
        response = super().form_valid(form)
        
        # Log yaratish
        email = form.cleaned_data['email']
        logger.info(f'Password reset requested for: {email}')
        
        return response

class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Parol o'zgartirilgandan keyin log
        user = form.user
        logger.info(f'Password successfully changed for user: {user.username}')
        
        return response
```

## 8-bosqich: Testing

### Functional test

```python
# accounts/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpassword123'
        )
    
    def test_complete_password_reset_flow(self):
        # 1. Parol qayta tiklash so'rovi
        response = self.client.post(reverse('accounts:password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        
        # 2. Email ma'lumotlarini olish
        email = mail.outbox[0]
        self.assertIn('Parol qayta tiklash', email.subject)
        
        # 3. Token va uidb64 yaratish
        token = default_token_generator.make_token(self.user)
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        
        # 4. Password reset confirm sahifasini test qilish
        reset_url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': uidb64, 'token': token
        })
        response = self.client.get(reset_url)
        self.assertEqual(response.status_code, 200)
        
        # 5. Yangi parol o'rnatish
        response = self.client.post(reset_url, {
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        
        # 6. Parol o'zgarganini tekshirish
        user = User.objects.get(pk=self.user.pk)
        self.assertTrue(user.check_password('newpassword123'))
```

## Xatoliklarni bartaraf etish

### 1. Email yuborilmaydi
```python
# settings.py da EMAIL_BACKEND ni tekshiring
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Gmail uchun App Password ishlatganingizni tekshiring
```

### 2. Template topilmaydi
```python
# TEMPLATES da DIRS sozlamasi
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        # ...
    }
]
```

### 3. SMTP xatosi
```python
# Gmail uchun 2-factor authentication yoqish kerak
# App Password olish kerak (oddiy parol ishlamaydi)
```

### 4. Token muddati tugagan
```python
# settings.py da
PASSWORD_RESET_TIMEOUT = 3600  # 1 soat (sekundlarda)
```

## Best Practices

### 1. Email xavfsizligi
- HTML email ishlatish
- SSL/TLS bilan shifrlash
- SPF, DKIM, DMARC sozlash

### 2. Form validatsiyasi
- Parol kuchi tekshiruvi
- Rate limiting
- CSRF himoyasi

### 3. User Experience
- Loading animatsiyalari
- Progress indicatorlar
- Clear error messages
- Mobile responsive design

### 4. Monitoring
- Email yuborish loglarini saqlash
- Failed attempts ni track qilish
- Performance monitoring

## Xulosa

Bu darsda biz Django'da parol qayta tiklash funksiyasini to'liq yakunladik:

1. **Password Reset Confirm template** - Token tekshiruvi va yangi parol formasi
2. **Password Reset Complete template** - Muvaffaqiyat xabari
3. **Custom email template** - Professional ko'rinish
4. **Production SMTP sozlamalari** - Haqiqiy email yuborish
5. **Xavfsizlik** - Rate limiting, HTTPS, token himoyasi
6. **Testing** - To'liq funksional testlar

Endi foydalanuvchilar parollarini unutganda xavfsiz va professional tarzda qayta tiklay oladilar.

## Keyingi dars

Keyingi darsda (lesson_36) biz:
- Signup: Foydalanuvchilarni ro'yxatdan o'tkazish
- Custom user registration form
- Email verification
- User activation jarayoni