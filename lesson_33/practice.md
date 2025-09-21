# Lesson 33 Practice: Foydalanuvchi parolini o'zgartirish amaliyoti

## Amaliyot maqsadi
Bu amaliyotda biz Django loyihamizda to'liq parol o'zgartirish tizimini yaratamiz. Barcha bosqichlarni amalda bajarib, professional darajadagi parol o'zgartirish funksiyasini ishga tushiramiz.

## Bosqichma-bosqich amaliyot

### 1-bosqich: Loyihani tayyorlash

Avval loyihada `accounts` app mavjudligini tekshiramiz:

```bash
# Agar accounts app mavjud bo'lmasa
python manage.py startapp accounts

# settings.py ga qo'shish
# INSTALLED_APPS ro'yxatiga 'accounts' qo'shing
```

**Tekshirish:** `accounts` papkasi loyiha ichida yaratilganini tasdiqlang.

### 2-bosqich: URLs.py fayllarini sozlash

#### Asosiy urls.py
```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),  # news app URL'lari
    path('accounts/', include('accounts.urls')),  # accounts app URL'lari
]
```

#### Accounts app URLs
```python
# accounts/urls.py (yangi fayl yaratamiz)
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Login/Logout
    path('login/', 
         auth_views.LoginView.as_view(template_name='registration/login.html'), 
         name='login'),
    
    path('logout/', 
         auth_views.LogoutView.as_view(), 
         name='logout'),
    
    # Parol o'zgartirish
    path('password-change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change_form.html',
             success_url='/accounts/password-change/done/'
         ), 
         name='password_change'),
    
    path('password-change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'
         ),
         name='password_change_done'),
]
```

**Tekshirish:** Server ishga tushiring va URL'larni browser'da sinab ko'ring.

### 3-bosqich: Template'lar papkasini yaratish

```bash
# Loyiha root papkasida templates papkasini yaratamiz
mkdir templates
mkdir templates/registration
```

**Papka tuzilmasi:**
```
myproject/
├── templates/
│   ├── base.html
│   └── registration/
│       ├── login.html
│       ├── password_change_form.html
│       └── password_change_done.html
```

### 4-bosqich: Base template yaratish

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangilikhlar sayti{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    
    <style>
        body { padding-top: 70px; }
        .navbar-brand { font-weight: bold; }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
        <div class="container">
            <a class="navbar-brand" href="{% url 'news:home' %}">
                <i class="fas fa-newspaper"></i> News Site
            </a>
            
            <div class="navbar-nav ms-auto">
                {% if user.is_authenticated %}
                    <div class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" id="userDropdown" 
                           role="button" data-bs-toggle="dropdown">
                            <i class="fas fa-user"></i> {{ user.username }}
                        </a>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li>
                                <a class="dropdown-item" href="{% url 'accounts:password_change' %}">
                                    <i class="fas fa-key"></i> Parolni o'zgartirish
                                </a>
                            </li>
                            <li><hr class="dropdown-divider"></li>
                            <li>
                                <a class="dropdown-item" href="{% url 'accounts:logout' %}">
                                    <i class="fas fa-sign-out-alt"></i> Chiqish
                                </a>
                            </li>
                        </ul>
                    </div>
                {% else %}
                    <a class="nav-link" href="{% url 'accounts:login' %}">
                        <i class="fas fa-sign-in-alt"></i> Kirish
                    </a>
                {% endif %}
            </div>
        </div>
    </nav>

    <!-- Messages -->
    {% if messages %}
        <div class="container mt-3">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <!-- Main Content -->
    {% block content %}
    {% endblock %}

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 5-bosqich: Login template yaratish

```html
<!-- templates/registration/login.html -->
{% extends 'base.html' %}

{% block title %}Tizimga kirish{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h4><i class="fas fa-sign-in-alt"></i> Tizimga kirish</h4>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="{{ form.username.id_for_label }}" class="form-label">
                                Foydalanuvchi nomi
                            </label>
                            {{ form.username }}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.password.id_for_label }}" class="form-label">
                                Parol
                            </label>
                            {{ form.password }}
                        </div>
                        
                        <button type="submit" class="btn btn-primary w-100">
                            <i class="fas fa-sign-in-alt"></i> Kirish
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 6-bosqich: Parol o'zgartirish formasini yaratish

```html
<!-- templates/registration/password_change_form.html -->
{% extends 'base.html' %}

{% block title %}Parolni o'zgartirish{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        <i class="fas fa-key"></i> Parolni o'zgartirish
                    </h4>
                </div>
                <div class="card-body">
                    
                    <!-- Xatoliklar -->
                    {% if form.errors %}
                        <div class="alert alert-danger">
                            <strong>Xatoliklar:</strong>
                            {% for field, errors in form.errors.items %}
                                <ul class="mb-0">
                                    {% for error in errors %}
                                        <li>{{ error }}</li>
                                    {% endfor %}
                                </ul>
                            {% endfor %}
                        </div>
                    {% endif %}

                    <form method="post">
                        {% csrf_token %}
                        
                        <!-- Joriy parol -->
                        <div class="mb-3">
                            <label for="{{ form.old_password.id_for_label }}" class="form-label">
                                <i class="fas fa-lock"></i> Joriy parol
                            </label>
                            <input type="password" 
                                   name="{{ form.old_password.name }}" 
                                   class="form-control" 
                                   id="{{ form.old_password.id_for_label }}"
                                   required>
                        </div>

                        <!-- Yangi parol -->
                        <div class="mb-3">
                            <label for="{{ form.new_password1.id_for_label }}" class="form-label">
                                <i class="fas fa-key"></i> Yangi parol
                            </label>
                            <input type="password" 
                                   name="{{ form.new_password1.name }}" 
                                   class="form-control" 
                                   id="{{ form.new_password1.id_for_label }}"
                                   required>
                            {% if form.new_password1.help_text %}
                                <div class="form-text text-muted">
                                    {{ form.new_password1.help_text|safe }}
                                </div>
                            {% endif %}
                        </div>

                        <!-- Yangi parolni tasdiqlash -->
                        <div class="mb-3">
                            <label for="{{ form.new_password2.id_for_label }}" class="form-label">
                                <i class="fas fa-shield-alt"></i> Yangi parolni tasdiqlash
                            </label>
                            <input type="password" 
                                   name="{{ form.new_password2.name }}" 
                                   class="form-control" 
                                   id="{{ form.new_password2.id_for_label }}"
                                   required>
                        </div>

                        <!-- Submit button -->
                        <div class="d-grid">
                            <button type="submit" class="btn btn-success btn-lg">
                                <i class="fas fa-save"></i> Parolni o'zgartirish
                            </button>
                        </div>
                    </form>
                </div>
                
                <div class="card-footer text-center">
                    <a href="{% url 'news:home' %}" class="btn btn-link">
                        <i class="fas fa-arrow-left"></i> Bekor qilish
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 7-bosqich: Muvaffaqiyat sahifasini yaratish

```html
<!-- templates/registration/password_change_done.html -->
{% extends 'base.html' %}

{% block title %}Parol o'zgartirildi{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-success">
                <div class="card-header bg-success text-white text-center">
                    <h3 class="mb-0">
                        <i class="fas fa-check-circle"></i> Muvaffaqiyat!
                    </h3>
                </div>
                <div class="card-body text-center">
                    
                    <!-- Success icon -->
                    <div class="mb-4">
                        <i class="fas fa-shield-check text-success" style="font-size: 5rem;"></i>
                    </div>
                    
                    <h4 class="text-success mb-3">Parolingiz muvaffaqiyatli o'zgartirildi!</h4>
                    
                    <p class="text-muted mb-4">
                        Yangi parolingiz xavfsiz tarzda saqlandi. Endi yangitdan tizimga kirishingiz mumkin.
                    </p>
                    
                    <!-- Action buttons -->
                    <div class="d-grid gap-2 d-md-flex justify-content-md-center">
                        <a href="{% url 'news:home' %}" class="btn btn-primary">
                            <i class="fas fa-home"></i> Bosh sahifa
                        </a>
                        <a href="{% url 'accounts:logout' %}" class="btn btn-outline-secondary">
                            <i class="fas fa-sign-out-alt"></i> Tizimdan chiqish
                        </a>
                    </div>
                </div>
                
                <div class="card-footer text-center text-muted">
                    <small>
                        <i class="fas fa-info-circle"></i> 
                        Xavfsizlik uchun parolni muntazam o'zgartiring
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 8-bosqich: Settings.py ni sozlash

```python
# settings.py
import os

# Templates sozlamasi
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Template papkasini qo'shamiz
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Login va logout yo'nalishlari
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Parol validatsiyasi
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Session xavfsizligi
SESSION_COOKIE_AGE = 86400  # 24 soat
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

**Tekshirish:** `python manage.py check` buyrug'i bilan xatolik yo'qligini tekshiring.

### 9-bosqich: Superuser yaratish va test

```bash
# Agar superuser mavjud bo'lmasa
python manage.py createsuperuser

# Test foydalanuvchi yaratish
python manage.py shell
```

```python
# Shell ichida
from django.contrib.auth.models import User

# Test foydalanuvchi yaratish
user = User.objects.create_user(
    username='testuser',
    password='testpass123',
    email='test@example.com'
)
print(f"Foydalanuvchi yaratildi: {user.username}")
```

### 10-bosqich: Serverni ishga tushirish va test qilish

```bash
# Server ishga tushirish
python manage.py runserver
```

**Test qilish bosqichlari:**

1. **Login test:**
   - `http://127.0.0.1:8000/accounts/login/` ga boring
   - Test foydalanuvchi bilan kirish

2. **Parol o'zgartirish test:**
   - Tizimga kirgandan keyin navbar'dagi dropdown menyuni oching
   - "Parolni o'zgartirish" tugmasini bosing
   - Form to'ldiring va yuboring

3. **URL'lar test:**
   ```
   http://127.0.0.1:8000/accounts/password-change/
   http://127.0.0.1:8000/accounts/password-change/done/
   ```

### 11-bosqich: Parol kuchini ko'rsatish (qo'shimcha)

```html
<!-- password_change_form.html ga qo'shamiz -->
<script>
function checkPasswordStrength() {
    const password = document.getElementById('id_new_password1').value;
    const strengthBar = document.getElementById('password-strength');
    const strengthText = document.getElementById('strength-text');
    
    let strength = 0;
    let text = '';
    
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    switch(strength) {
        case 0:
        case 1:
            strengthBar.className = 'progress-bar bg-danger';
            strengthBar.style.width = '20%';
            text = 'Juda zaif';
            break;
        case 2:
            strengthBar.className = 'progress-bar bg-warning';
            strengthBar.style.width = '40%';
            text = 'Zaif';
            break;
        case 3:
            strengthBar.className = 'progress-bar bg-info';
            strengthBar.style.width = '60%';
            text = 'O\'rtacha';
            break;
        case 4:
            strengthBar.className = 'progress-bar bg-success';
            strengthBar.style.width = '80%';
            text = 'Kuchli';
            break;
        case 5:
            strengthBar.className = 'progress-bar bg-success';
            strengthBar.style.width = '100%';
            text = 'Juda kuchli';
            break;
    }
    
    strengthText.textContent = text;
}

document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('id_new_password1');
    if (passwordField) {
        passwordField.addEventListener('input', checkPasswordStrength);
    }
});
</script>

<!-- Form ichiga qo'shamiz -->
<div class="mb-3">
    <label for="{{ form.new_password1.id_for_label }}" class="form-label">
        <i class="fas fa-key"></i> Yangi parol
    </label>
    <input type="password" 
           name="{{ form.new_password1.name }}" 
           class="form-control" 
           id="{{ form.new_password1.id_for_label }}"
           onkeyup="checkPasswordStrength()"
           required>
    
    <!-- Parol kuchi ko'rsatkichi -->
    <div class="mt-2">
        <div class="progress" style="height: 5px;">
            <div id="password-strength" class="progress-bar" style="width: 0%"></div>
        </div>
        <small id="strength-text" class="form-text"></small>
    </div>
    
    {% if form.new_password1.help_text %}
        <div class="form-text text-muted">
            {{ form.new_password1.help_text|safe }}
        </div>
    {% endif %}
</div>
```

### 12-bosqich: Custom views yaratish (qo'shimcha)

```python
# accounts/views.py
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages

class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')
    
    def form_valid(self, form):
        messages.success(self.request, 'Parolingiz muvaffaqiyatli o\'zgartirildi!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Parolni o\'zgartirish'
        return context

class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Parol o\'zgartirildi'
        return context
```

### 13-bosqich: Error handling va logging

```python
# accounts/views.py ga qo'shamiz
import logging

logger = logging.getLogger(__name__)

class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    # ... oldingi kodlar
    
    def form_invalid(self, form):
        logger.warning(f"Password change failed for user: {self.request.user.username}")
        messages.error(self.request, 'Parol o\'zgartirishda xatolik yuz berdi. Qaytadan urinib ko\'ring.')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        logger.info(f"Password changed successfully for user: {self.request.user.username}")
        messages.success(self.request, 'Parolingiz muvaffaqiyatli o\'zgartirildi!')
        return super().form_valid(form)
```

### 14-bosqich: Yakuniy test va debugging

```bash
# Serverni qayta ishga tushiring
python manage.py runserver

# Test checklist:
```

**Test ro'yxati:**

- [ ] Login sahifasi to'g'ri ishlaydi
- [ ] Navbar'da parol o'zgartirish link'i mavjud
- [ ] Parol o'zgartirish sahifasi ochiladi
- [ ] Form validation ishlaydi
- [ ] Noto'g'ri joriy parol uchun xato ko'rsatiladi
- [ ] Parol validatsiya qoidalari ishlaydi
- [ ] Muvaffaqiyat sahifasi ko'rsatiladi
- [ ] Yangi parol bilan kirish mumkin

### 15-bosqich: Troubleshooting

**Keng uchraydi xatoliklar:**

1. **Template not found xatosi:**
   ```python
   # settings.py da DIRS to'g'ri sozlanganini tekshiring
   'DIRS': [BASE_DIR / 'templates'],
   ```

2. **CSRF token xatosi:**
   ```html
   <!-- Form ichida {% csrf_token %} borligini tekshiring -->
   ```

3. **URL xatosi:**
   ```python
   # urls.py da app_name va URL name'lar to'g'ri ekanini tekshiring
   ```

4. **Migration xatosi:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Qo'shimcha vazifalar

1. **Email orqali parol o'zgartirish haqida xabar yuborish**
2. **Parol tarixi saqlab, takrorlanishni oldini olish** 
3. **2FA (Two-Factor Authentication) qo'shish**
4. **Password strength meter'ni yaxshilash**
5. **Rate limiting qo'shish**

### Xulosa

Bu amaliyotda biz:
- To'liq parol o'zgartirish tizimini yaratdik
- Bootstrap bilan chiroyli interfeys yaratdik  
- Xavfsizlik validatsiyalarini sozladik
- Error handling va logging qo'shdik
- Professional darajadagi user experience yaratdik

**Keyingi qadam:** Parolni unutgan foydalanuvchilar uchun parolni qayta tiklash tizimini yaratish.