# Lesson 37: Signup. Class View orqali ro'yxatdan o'tish

## Dars maqsadi
Ushbu darsda biz Django'da Class-Based View (CBV) yordamida foydalanuvchilar ro'yxatdan o'tishi uchun signup funksiyasini yaratamiz. `UserCreationForm` va `CreateView` dan foydalanib professional darajada ro'yxatdan o'tish tizimini qo'llash usullarini o'rganamiz.

## Mavzu bo'yicha nazariy ma'lumot

### Django'da Signup jarayoni
Django'da foydalanuvchi ro'yxatdan o'tishi uchun asosan ikki yondashuv mavjud:
1. **Function-Based View (FBV)** - oddiy funksiyalar orqali
2. **Class-Based View (CBV)** - klasslar orqali (bu darsda o'rganamiz)

### Class-Based View afzalliklari
- **Kod qayta ishlatish** - bir marta yozib, ko'p joyda ishlatish
- **Mixin'lar** - qo'shimcha funksionallikni osongina qo'shish
- **DRY prinsipi** - "Don't Repeat Yourself"
- **Django konvensiyalari** - Django'ning standart yondashuvlari

### Django'ning built-in form va view'lari
- `UserCreationForm` - foydalanuvchi yaratish uchun tayyor form
- `CreateView` - yangi obyekt yaratish uchun umumiy view
- `LoginView` - kirish jarayoni uchun

## Amaliy qism

### 1-bosqich: accounts app yaratish

Avval alohida accounts app yaratamiz:

```bash
python manage.py startapp accounts
```

**settings.py** faylida app'ni ro'yxatga qo'shamiz:

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
    'accounts.apps.AccountsConfig',  # Yangi qo'shildi
]
```

### 2-bosqich: Custom SignUpForm yaratish

**accounts/forms.py** faylini yaratib, custom form yaratamiz:

```python
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Ro'yxatdan o'tish uchun maxsus form"""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ismingizni kiriting'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Familiyangizni kiriting'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email manzilingizni kiriting'
        })
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Foydalanuvchi nomini kiriting'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni kiriting'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Parolni takrorlang'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        """Foydalanuvchini saqlashda qo'shimcha ma'lumotlarni ham saqlash"""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user
```

### 3-bosqich: SignUpView yaratish

**accounts/views.py** faylini yaratamiz:

```python
# accounts/views.py
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from .forms import SignUpForm


class SignUpView(CreateView):
    """Class-based view orqali ro'yxatdan o'tish"""
    
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('news:home')  # Muvaffaqiyatli ro'yxatdan o'tgandan keyin bosh sahifaga yo'naltirish
    
    def form_valid(self, form):
        """Form to'g'ri to'ldirilganda ishlaydigan method"""
        # Avval foydalanuvchini saqlaymiz
        response = super().form_valid(form)
        
        # Keyin avtomatik tizimga kiritamiz
        user = form.save()
        login(self.request, user)
        
        # Muvaffaqiyat xabarini qo'shamiz
        messages.success(
            self.request, 
            f"Xush kelibsiz, {user.first_name}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz."
        )
        
        return response
    
    def form_invalid(self, form):
        """Form noto'g'ri to'ldirilganda ishlaydigan method"""
        messages.error(
            self.request, 
            "Ro'yxatdan o'tishda xatolik yuz berdi. Iltimos, ma'lumotlarni tekshiring."
        )
        return super().form_invalid(form)
```

### 4-bosqich: URL marshrutlarini sozlash

**accounts/urls.py** faylini yaratamiz:

```python
# accounts/urls.py
from django.urls import path
from .views import SignUpView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
```

**config/urls.py** faylida accounts URL'larini qo'shamiz:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('accounts.urls')),  # Yangi qo'shildi
    path('accounts/', include('django.contrib.auth.urls')),  # Login, logout uchun
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 5-bosqich: Signup template yaratish

**templates/registration/signup.html** faylini yaratamiz:

```html
<!-- templates/registration/signup.html -->
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}Ro'yxatdan o'tish{% endblock title %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-center">Ro'yxatdan o'tish</h3>
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
                    
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="{{ form.first_name.id_for_label }}" class="form-label">Ism</label>
                            {{ form.first_name }}
                            {% if form.first_name.errors %}
                                <div class="text-danger">
                                    {% for error in form.first_name.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.last_name.id_for_label }}" class="form-label">Familiya</label>
                            {{ form.last_name }}
                            {% if form.last_name.errors %}
                                <div class="text-danger">
                                    {% for error in form.last_name.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.email.id_for_label }}" class="form-label">Email</label>
                            {{ form.email }}
                            {% if form.email.errors %}
                                <div class="text-danger">
                                    {% for error in form.email.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.username.id_for_label }}" class="form-label">Foydalanuvchi nomi</label>
                            {{ form.username }}
                            {% if form.username.errors %}
                                <div class="text-danger">
                                    {% for error in form.username.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.password1.id_for_label }}" class="form-label">Parol</label>
                            {{ form.password1 }}
                            {% if form.password1.errors %}
                                <div class="text-danger">
                                    {% for error in form.password1.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.password2.id_for_label }}" class="form-label">Parolni takrorlang</label>
                            {{ form.password2 }}
                            {% if form.password2.errors %}
                                <div class="text-danger">
                                    {% for error in form.password2.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">
                                Ro'yxatdan o'tish
                            </button>
                        </div>
                    </form>
                    
                    <div class="text-center mt-3">
                        <p>Akkauntingiz bormi? <a href="{% url 'login' %}">Kirish</a></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

### 6-bosqich: Navigation'ga signup linkini qo'shish

**templates/base.html** faylida navbar'ga signup linkini qo'shamiz:

```html
<!-- templates/base.html ichidagi navbar qismi -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{% url 'news:home' %}">Yangiliklar sayti</a>
        
        <div class="navbar-nav ms-auto">
            {% if user.is_authenticated %}
                <span class="navbar-text me-3">
                    Salom, {{ user.first_name|default:user.username }}!
                </span>
                <a class="nav-link" href="{% url 'logout' %}">Chiqish</a>
            {% else %}
                <a class="nav-link" href="{% url 'login' %}">Kirish</a>
                <a class="nav-link" href="{% url 'accounts:signup' %}">Ro'yxatdan o'tish</a>
            {% endif %}
        </div>
    </div>
</nav>
```

### 7-bosqich: Login sahifasini yangilash

**templates/registration/login.html** faylini yangilab, signup linkini qo'shamiz:

```html
<!-- templates/registration/login.html -->
{% extends 'base.html' %}

{% block title %}Kirish{% endblock title %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h3 class="text-center">Tizimga kirish</h3>
                </div>
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="{{ form.username.id_for_label }}" class="form-label">
                                Foydalanuvchi nomi
                            </label>
                            <input type="text" 
                                   name="username" 
                                   class="form-control"
                                   placeholder="Foydalanuvchi nomini kiriting"
                                   required>
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.password.id_for_label }}" class="form-label">
                                Parol
                            </label>
                            <input type="password" 
                                   name="password" 
                                   class="form-control"
                                   placeholder="Parolni kiriting"
                                   required>
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">
                                Kirish
                            </button>
                        </div>
                    </form>
                    
                    <div class="text-center mt-3">
                        <p>Akkauntingiz yo'qmi? 
                            <a href="{% url 'accounts:signup' %}">Ro'yxatdan o'ting</a>
                        </p>
                        <p><a href="#">Parolni unutdingizmi?</a></p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

## Kengaytirilgan funksiyalar

### 1. Email tasdiqlash funksiyasi qo'shish

**accounts/forms.py** faylida email mavjudligini tekshirish:

```python
# accounts/forms.py ga qo'shimcha
def clean_email(self):
    """Email mavjudligini tekshirish"""
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
        raise forms.ValidationError("Bu email manzil allaqachon ishlatilmoqda.")
    return email
```

### 2. Custom redirect funksiyasi

**accounts/views.py** da `get_success_url` methodini override qilish:

```python
# accounts/views.py ga qo'shimcha
def get_success_url(self):
    """Signup dan keyin qayerga yo'naltirish"""
    next_page = self.request.GET.get('next')
    if next_page:
        return next_page
    return reverse_lazy('news:home')
```

### 3. User Profile sahifasi yaratish

**accounts/views.py** ga profile view qo'shish:

```python
# accounts/views.py ga qo'shimcha
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class ProfileView(LoginRequiredMixin, TemplateView):
    """Foydalanuvchi profil sahifasi"""
    template_name = 'registration/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
```

## Testlash

### 1. Funktsiyani sinab ko'rish
```bash
python manage.py runserver
```

Brauzerda quyidagi URL'larga kiring:
- `http://127.0.0.1:8000/accounts/signup/` - Ro'yxatdan o'tish
- `http://127.0.0.1:8000/accounts/login/` - Kirish

### 2. Django shell orqali tekshirish
```python
python manage.py shell

# Foydalanuvchilar ro'yxatini ko'rish
from django.contrib.auth.models import User
users = User.objects.all()
print(users)

# Eng oxirgi foydalanuvchini ko'rish
last_user = User.objects.last()
print(f"Ism: {last_user.first_name}")
print(f"Email: {last_user.email}")
```

## Xato va ularni hal qilish

### 1. Template topilmayapti xatosi
```
TemplateDoesNotExist: registration/signup.html
```
**Yechi:** `templates/registration/` papkasini to'g'ri yarating

### 2. URL pattern xatosi
```
NoReverseMatch: Reverse for 'signup' not found
```
**Yechi:** URL nomlarini to'g'ri yozing va namespace'dan foydalaning

### 3. Form validation xatosi
**Yechi:** Custom form metodlarida `super()` ni to'g'ri chaqiring

## Best Practices va maslahatlar

### 1. Security
- **CSRF tokenlarini** doimo ishlating
- **Parol murakkabligini** tekshiring
- **Email validatsiyasi** qo'shing

### 2. User Experience
- **Clear error messages** - aniq xato xabarlari
- **Success messages** - muvaffaqiyat xabarlari  
- **Responsive design** - barcha qurilmalar uchun

### 3. Code Organization
- **Separate concerns** - har bir fayl o'z vazifasini bajarsin
- **Reusable components** - qayta ishlatiluvchi komponentlar
- **Consistent naming** - izchil nomlash

### 4. Performance
- **Database queries optimizatsiyasi**
- **Form validation client-side** ham qo'shing
- **Caching strategiyalari** o'ylang

### 5. Testing
```python
# accounts/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class SignUpTest(TestCase):
    def test_signup_view_success(self):
        """Signup sahifasi to'g'ri ishlaydimi"""
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ro'yxatdan o'tish")
    
    def test_signup_form_valid_data(self):
        """To'g'ri ma'lumotlar bilan signup"""
        form_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(reverse('accounts:signup'), form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='testuser').exists())
```

## Xulosa

Ushbu darsda biz Django'da Class-Based View yordamida professional signup tizimini yaratdik. Asosiy o'rgangan narsalar:

1. **Custom SignUpForm** yaratish
2. **CreateView** dan foydalanish  
3. **Automatic login** after signup
4. **Messages framework** bilan ishlash
5. **Template'larda form handling**
6. **URL routing** va namespace'lar
7. **Security best practices**

Keyingi darsda foydalanuvchi profil modelini yaratish va tahrirlash usullarini o'rganamiz.