# Lesson 33: Foydalanuvchi parolini o'zgartirish

## Dars maqsadi
Bu darsda Django'da foydalanuvchilarning parollarini o'zgartirish funksiyasini qanday amalga oshirishni o'rganamiz. Django'ning o'rnatilgan PasswordChangeView va PasswordChangeDoneView'laridan foydalanib, xavfsiz parol o'zgartirish tizimini yaratamiz.

## Nazariy qism

### Django'da parol o'zgartirish
Django authentication tizimi parollarni o'zgartirish uchun tayyor class-based view'larni taqdim etadi:

- **PasswordChangeView** - parolni o'zgartirish formasini ko'rsatadi
- **PasswordChangeDoneView** - parol muvaffaqiyatli o'zgartirilganidan keyin ko'rsatiladigan sahifa

### Parol o'zgartirish jarayoni
1. Foydalanuvchi joriy parolini kiritadi
2. Yangi parolni ikki marta kiritadi (tasdiqlash uchun)
3. Django parolni xesh qiladi va saqlaydi
4. Muvaffaqiyat sahifasiga yo'naltiradi

## Amaliy qism

### 1-bosqich: URLs sozlash

Avval `accounts` app'imizda URL'larni sozlaymiz:

```python
# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Parol o'zgartirish URL'lari
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change_form.html',
             success_url='/accounts/password_change/done/'
         ), 
         name='password_change'),
    
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'
         ),
         name='password_change_done'),
]
```

**Kod tushuntiruvi:**
- `PasswordChangeView` - parol o'zgartirish formasini boshqaradi
- `template_name` - ishlatilayotgan template nomini belgilaydi
- `success_url` - muvaffaqiyatli o'zgartirishdan keyin yo'naltirilayotgan URL
- `PasswordChangeDoneView` - muvaffaqiyat sahifasini ko'rsatadi

### 2-bosqich: Parol o'zgartirish template yaratish

```html
<!-- templates/registration/password_change_form.html -->
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}Parolni o'zgartirish{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title mb-0">
                        <i class="fas fa-key"></i> Parolni o'zgartirish
                    </h3>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        {% if form.errors %}
                            <div class="alert alert-danger">
                                <strong>Xatolik yuz berdi:</strong>
                                {{ form.errors }}
                            </div>
                        {% endif %}

                        <div class="mb-3">
                            <label for="{{ form.old_password.id_for_label }}" class="form-label">
                                Joriy parol
                            </label>
                            {{ form.old_password|add_class:"form-control" }}
                            {% if form.old_password.help_text %}
                                <small class="form-text text-muted">{{ form.old_password.help_text }}</small>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.new_password1.id_for_label }}" class="form-label">
                                Yangi parol
                            </label>
                            {{ form.new_password1|add_class:"form-control" }}
                            {% if form.new_password1.help_text %}
                                <small class="form-text text-muted">{{ form.new_password1.help_text }}</small>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.new_password2.id_for_label }}" class="form-label">
                                Yangi parolni tasdiqlang
                            </label>
                            {{ form.new_password2|add_class:"form-control" }}
                            {% if form.new_password2.help_text %}
                                <small class="form-text text-muted">{{ form.new_password2.help_text }}</small>
                            {% endif %}
                        </div>

                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Parolni o'zgartirish
                            </button>
                        </div>
                    </form>
                </div>
                <div class="card-footer text-center">
                    <a href="{% url 'news:home' %}" class="btn btn-link">
                        <i class="fas fa-arrow-left"></i> Bosh sahifaga qaytish
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**Template tushuntiruvi:**
- `old_password` - joriy parolni kiritish maydoni
- `new_password1` - yangi parolni kiritish maydoni  
- `new_password2` - yangi parolni tasdiqlash maydoni
- Bootstrap CSS classlari bilan chiroyli dizayn
- Xatolik xabarlarini ko'rsatish

### 3-bosqich: Muvaffaqiyat sahifasi template

```html
<!-- templates/registration/password_change_done.html -->
{% extends 'base.html' %}

{% block title %}Parol o'zgartirildi{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-success">
                <div class="card-header bg-success text-white">
                    <h3 class="card-title mb-0">
                        <i class="fas fa-check-circle"></i> Muvaffaqiyat!
                    </h3>
                </div>
                <div class="card-body text-center">
                    <div class="mb-4">
                        <i class="fas fa-shield-alt text-success" style="font-size: 4rem;"></i>
                    </div>
                    <h4 class="text-success mb-3">Parolingiz muvaffaqiyatli o'zgartirildi!</h4>
                    <p class="text-muted mb-4">
                        Yangi parolingiz xavfsiz tarzda saqlandi. Endi yangi parol bilan 
                        tizimga kirishingiz mumkin.
                    </p>
                    
                    <div class="d-grid gap-2">
                        <a href="{% url 'news:home' %}" class="btn btn-primary">
                            <i class="fas fa-home"></i> Bosh sahifaga o'tish
                        </a>
                        <a href="{% url 'accounts:logout' %}" class="btn btn-outline-secondary">
                            <i class="fas fa-sign-out-alt"></i> Tizimdan chiqish
                        </a>
                    </div>
                </div>
                <div class="card-footer text-center text-muted">
                    <small>
                        <i class="fas fa-info-circle"></i> 
                        Xavfsizlik uchun vaqti-vaqti bilan parolingizni o'zgartiring
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 4-bosqich: Navigation menyuga parol o'zgartirish linkini qo'shish

```html
<!-- templates/base.html ning navbar qismiga qo'shamiz -->
{% if user.is_authenticated %}
    <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" 
           role="button" data-bs-toggle="dropdown">
            <i class="fas fa-user"></i> {{ user.username }}
        </a>
        <ul class="dropdown-menu">
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
    </li>
{% endif %}
```

### 5-bosqich: Custom PasswordChangeView yaratish (ixtiyoriy)

Agar ko'proq nazorat kerak bo'lsa, custom view yaratishimiz mumkin:

```python
# accounts/views.py
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

class CustomPasswordChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')
    success_message = "Parolingiz muvaffaqiyatli o'zgartirildi!"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Parolni o'zgartirish'
        return context
```

**Custom view tushuntiruvi:**
- `LoginRequiredMixin` - faqat tizimga kirgan foydalanuvchilar kirishi mumkin
- `SuccessMessageMixin` - muvaffaqiyat xabarini ko'rsatadi
- `get_context_data` - template'ga qo'shimcha ma'lumot yuboradi

### 6-bosqich: Parol validatsiyasini sozlash

```python
# settings.py
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
```

**Validator tushuntiruvi:**
- `UserAttributeSimilarityValidator` - parol foydalanuvchi ma'lumotlariga o'xshamasligi
- `MinimumLengthValidator` - minimal uzunlik (8 belgi)
- `CommonPasswordValidator` - umumiy parollarni taqiqlash
- `NumericPasswordValidator` - faqat raqamlardan iborat parolni taqiqlash

### 7-bosqich: Settings.py'da asosiy sozlamalar

```python
# settings.py
# Login va logout yo'nalishlari
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Session xavfsizligi
SESSION_COOKIE_AGE = 86400  # 24 soat
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # HTTPS uchun

# Parol hashlash
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]
```

## Test qilish

### 1. URL'larni tekshirish:
```bash
python manage.py shell
from django.urls import reverse
print(reverse('accounts:password_change'))
print(reverse('accounts:password_change_done'))
```

### 2. Parol o'zgartirish jarayonini sinab ko'rish:
1. Tizimga kiring
2. Parol o'zgartirish sahifasiga o'ting
3. Joriy parolni kiriting
4. Yangi parolni ikki marta kiriting  
5. Formani yuboring
6. Muvaffaqiyat sahifasini tekshiring

## Xavfsizlik masalalari

### 1. HTTPS ishlatish
```python
# settings.py (production uchun)
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### 2. CSRF himoyasi
Template'larda doimo `{% csrf_token %}` ishlatish.

### 3. Rate limiting
```python
# Parol o'zgartirish uchun rate limiting
from django.contrib.auth.decorators import ratelimit

@ratelimit(key='ip', rate='5/h', method='POST')
def password_change_view(request):
    # view logic
    pass
```

## Best Practices

### 1. Parol talablari
- Kamida 8 belgi uzunlik
- Katta va kichik harflar
- Raqamlar va maxsus belgilar
- Umumiy parollarni taqiqlash

### 2. Xavfsizlik
- HTTPS protocol ishlatish
- Session'larni xavfsiz saqlash
- Parollarni hech qachon plain textda saqlamaslik

### 3. Foydalanuvchi tajribasi
- Aniq xato xabarlar
- Parol kuchini ko'rsatish
- Muvaffaqiyat haqida xabar berish

### 4. Logging
```python
import logging

logger = logging.getLogger(__name__)

class CustomPasswordChangeView(PasswordChangeView):
    def form_valid(self, form):
        logger.info(f"Password changed for user: {self.request.user.username}")
        return super().form_valid(form)
```

## Xulosa
Bu darsda biz Django'da parol o'zgartirish funksiyasini to'liq amalga oshirdik. Foydalanuvchilar endi xavfsiz tarzda parollarini o'zgartirishi mumkin. Keyingi darsda parolni qayta tiklash funksiyasini o'rganamiz.

**Keyingi dars:**

34-darsda Foydalanuvchi parolni qayta tiklash (1-qism) ni o'rganamiz.