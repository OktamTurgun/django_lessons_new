# Lesson 36: Signup - Roʻyxatdan oʻtish

## Dars maqsadi
Ushbu darsda biz Django'da yangi foydalanuvchilarning ro'yxatdan o'tish (signup) funksiyasini yaratamiz. Foydalanuvchilar saytga o'z akkauntlarini yarata olishadi.

## Mavzu bo'yicha bilimlar

### 1. Django User Model
Django'da foydalanuvchilar bilan ishlash uchun `django.contrib.auth.models.User` modeli mavjud. Bu model quyidagi asosiy maydonlarga ega:
- `username` - foydalanuvchi nomi
- `email` - elektron pochta manzili  
- `first_name` - ism
- `last_name` - familiya
- `password` - parol (hashlangan holda)

### 2. UserCreationForm
Django'da signup uchun tayyor `UserCreationForm` mavjud. Bu forma quyidagi maydonlarni o'z ichiga oladi:
- `username` - foydalanuvchi nomi
- `password1` - parol
- `password2` - parolni takrorlash

## Amaliy qism

### 1-bosqich: accounts app yaratish

Avval foydalanuvchilar bilan bog'liq barcha funksiyalar uchun alohida app yaratamiz:

```bash
python manage.py startapp accounts
```

### 2-bosqich: settings.py da app ni ro'yxatga olish

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
    'news_app',
    'accounts',  # Yangi qo'shildi
]
```

### 3-bosqich: Signup view yaratish

```python
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Yangi foydalanuvchini yaratish
            user = form.save()
            
            # Foydalanuvchini avtomatik login qilish
            login(request, user)
            
            # Muvaffaqiyatli xabar
            messages.success(request, f"Salom {user.username}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.")
            
            # Bosh sahifaga yo'naltirish
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form
    }
    return render(request, 'registration/signup.html', context)
```

**Kod izohli:**
- `request.method == 'POST'` - agar forma yuborilgan bo'lsa
- `form.is_valid()` - forma to'g'ri to'ldirilganligini tekshirish
- `form.save()` - yangi foydalanuvchini bazaga saqlash
- `login(request, user)` - foydalanuvchini avtomatik login qilish
- `messages.success()` - muvaffaqiyatli xabar chiqarish
- `redirect('home')` - bosh sahifaga yo'naltirish

### 4-bosqich: URL konfiguratsiyasi

```python
# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
]
```

```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_app.urls')),
    path('accounts/', include('accounts.urls')),  # Yangi qo'shildi
]
```

### 5-bosqich: Signup template yaratish

Avval `templates/registration` papkasini yarating va ichiga `signup.html` faylini yarating:

```html
<!-- templates/registration/signup.html -->

{% extends '_base.html' %}
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
                    <!-- Xato xabarlari -->
                    {% if form.errors %}
                        <div class="alert alert-danger">
                            {{ form.errors }}
                        </div>
                    {% endif %}
                    
                    <!-- Signup forma -->
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="{{ form.username.id_for_label }}" class="form-label">
                                Foydalanuvchi nomi
                            </label>
                            {{ form.username }}
                            {% if form.username.help_text %}
                                <div class="form-text">{{ form.username.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.password1.id_for_label }}" class="form-label">
                                Parol
                            </label>
                            {{ form.password1 }}
                            {% if form.password1.help_text %}
                                <div class="form-text">{{ form.password1.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.password2.id_for_label }}" class="form-label">
                                Parolni takrorlang
                            </label>
                            {{ form.password2 }}
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary">
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

### 6-bosqich: Navigation da signup linkini qo'shish

```html
<!-- templates/_base.html -->

<!-- Navbar ichida, login tugmasidan oldin -->
{% if user.is_authenticated %}
    <li class="nav-item">
        <a class="nav-link" href="#">Salom, {{ user.username }}!</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="{% url 'logout' %}">Chiqish</a>
    </li>
{% else %}
    <li class="nav-item">
        <a class="nav-link" href="{% url 'accounts:signup' %}">Ro'yxatdan o'tish</a>
    </li>
    <li class="nav-item">
        <a class="nav-link" href="{% url 'login' %}">Kirish</a>
    </li>
{% endif %}
```

## Yaxshilangan Signup View (Class-based)

Function-based view o'rniga class-based view ham ishlatishimiz mumkin:

```python
# accounts/views.py

from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib import messages

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        # Formani saqlash
        response = super().form_valid(form)
        
        # Yangi yaratilgan foydalanuvchini avtomatik login qilish
        login(self.request, self.object)
        
        # Muvaffaqiyatli xabar
        messages.success(self.request, f"Salom {self.object.username}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz.")
        
        return response
```

**URLs.py ni yangilash:**
```python
# accounts/urls.py

from django.urls import path
from .views import SignupView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
]
```

## Custom Signup Form yaratish

Agar qo'shimcha maydonlar kerak bo'lsa, o'z formamizni yarata olamiz:

```python
# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Haqiqiy email manzilini kiriting")
    first_name = forms.CharField(max_length=30, required=True, help_text="Ismingizni kiriting")
    last_name = forms.CharField(max_length=30, required=True, help_text="Familiyangizni kiriting")
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user
```

**View da custom formani ishlatish:**
```python
# accounts/views.py

from .forms import CustomSignupForm

class SignupView(CreateView):
    form_class = CustomSignupForm  # UserCreationForm o'rniga
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    
    # Qolgan kod bir xil...
```

## Xatoliklar bilan ishlash

Signup jarayonida yuzaga kelishi mumkin bo'lgan xatoliklar:

1. **Username allaqachon mavjud**
2. **Parollar mos kelmaydi**
3. **Parol juda oddiy**
4. **Email noto'g'ri formatda**

Bu xatoliklar avtomatik ravishda formada ko'rsatiladi.

## Testlash

Signup funksiyasini sinab ko'ring:

1. `http://127.0.0.1:8000/accounts/signup/` ga boring
2. Forma maydonlarini to'ldiring
3. Ro'yxatdan o'tish tugmasini bosing
4. Muvaffaqiyatli bo'lsa, bosh sahifaga yo'naltirilishingiz kerak

## Maslahatlar va Best Practices

### 1. Xavfsizlik maslahatlar
- Parol talablarini kuchaytiring
- Email tasdiqlashni qo'shing
- CAPTCHA qo'shing (spam oldini olish uchun)

### 2. Foydalanuvchi tajribasi
- Forma xatolarini aniq ko'rsating
- Muvaffaqiyatli xabarlar chiqaring
- Mobile-friendly dizayn qiling

### 3. Kod tashkiloti
- Foydalanuvchi bilan bog'liq barcha funksiyalarni `accounts` appida saqlang
- Custom formalarni alohida `forms.py` faylida yarating
- View'larni mantiqiy ravishda guruhlang

### 4. Kelajakda qo'shish mumkin
- Email tasdiqlash
- Social media orqali ro'yxatdan o'tish
- Profil rasmi yuklash
- Foydalanuvchi profilini kengaytirish

## Xulosa

Ushbu darsda biz Django'da signup (ro'yxatdan o'tish) funksiyasini yaratdik. Bu orqali yangi foydalanuvchilar saytga o'z akkauntlarini yarata olishadi. Keyingi darslarda biz foydalanuvchi profilini yaratish va tahrirlash bilan shug'ullanamiz.