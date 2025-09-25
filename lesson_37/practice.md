# Lesson 37 Practice: Signup funksiyasini amaliy qo'llash

## Amaliyot maqsadi
Bu amaliyot darsida siz o'rgangan Class-Based View yordamida signup funksiyasini to'liq amalga oshirasiz va turli xil stsenariylarni sinab ko'rasiz.

## Vazifa 1: Asosiy signup tizimini yaratish

### 1.1 Loyiha tuzilmasi
Quyidagi papka tuzilmasini yarating:

```
myproject/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── news/
│   └── ...
├── accounts/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── templates/
    ├── base.html
    └── registration/
        ├── login.html
        └── signup.html
```

### 1.2 Accounts app yaratish va sozlash

**Terminalde bajarilishi kerak:**
```bash
# 1. Accounts app yaratish
python manage.py startapp accounts

# 2. Migratsiya qilish
python manage.py makemigrations
python manage.py migrate

# 3. Serverni ishga tushirish
python manage.py runserver
```

### 1.3 Settings.py ni yangilash

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
    'accounts.apps.AccountsConfig',  # Bu qatorni qo'shing
]

# Login/Logout redirects
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
```

## Vazifa 2: SignUpForm yaratish va sozlash

### 2.1 Basic form yaratish

**accounts/forms.py** faylini yarating:

```python
# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    # TODO: Quyidagi maydonlarni to'ldiring
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            # TODO: CSS klasslar va placeholder qo'shing
        })
    )
    
    # TODO: last_name, email maydonlarini qo'shing
    # TODO: username, password1, password2 maydonlariga CSS qo'shing
    
    class Meta:
        model = User
        fields = (
            # TODO: Maydon nomlarini yozing
        )
    
    def save(self, commit=True):
        # TODO: Custom save metodini yozing
        pass
```

**Sizning vazifangiz:**
1. Barcha `TODO` qismlarini to'ldiring
2. CSS klasslar va placeholder'larni qo'shing
3. `save` metodini to'g'ri yozing

### 2.2 Form validation qo'shish

Form'ga quyidagi validation'larni qo'shing:

```python
# accounts/forms.py ga qo'shimcha metodlar

def clean_email(self):
    """Email takrorlanmasligini tekshirish"""
    # TODO: Email mavjudligini tekshiring
    pass

def clean_username(self):
    """Username'ning uzunligini tekshirish"""
    # TODO: Username kamida 3 ta belgidan iborat bo'lishini tekshiring
    pass
```

## Vazifa 3: SignUpView yaratish

### 3.1 Basic view yaratish

**accounts/views.py** faylini to'ldiring:

```python
# accounts/views.py
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = # TODO: Form klassini yozing
    template_name = # TODO: Template nomini yozing
    success_url = # TODO: Muvaffaqiyatli ro'yxatdan o'tgandan keyin qayerga yo'naltirish
    
    def form_valid(self, form):
        # TODO: Form valid bo'lganda bajariladigan amallar
        # 1. Super metodini chaqiring
        # 2. Foydalanuvchini login qiling
        # 3. Success message qo'shing
        pass
    
    def form_invalid(self, form):
        # TODO: Form invalid bo'lganda xato xabarini qo'shing
        pass
```

### 3.2 URL marshrutlarini sozlash

**accounts/urls.py** faylini yarating:

```python
# accounts/urls.py
from django.urls import path
from .views import # TODO: View'ni import qiling

app_name = 'accounts'

urlpatterns = [
    # TODO: signup URL'ini qo'shing
]
```

**config/urls.py** ni yangilang:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    # TODO: accounts URL'larini qo'shing
    # TODO: django auth URL'larini qo'shing
]
```

## Vazifa 4: Template'larni yaratish

### 4.1 Base template yangilash

**templates/base.html** faylida navbar'ni yangilang:

```html
<!-- templates/base.html -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{% url 'news:home' %}">Yangiliklar</a>
        
        <div class="navbar-nav ms-auto">
            {% if user.is_authenticated %}
                <!-- TODO: Authenticated user uchun interfeys -->
            {% else %}
                <!-- TODO: Anonymous user uchun login va signup linklari -->
            {% endif %}
        </div>
    </div>
</nav>
```

### 4.2 Signup template yaratish

**templates/registration/signup.html** faylini yarating:

```html
{% extends 'base.html' %}

{% block title %}Ro'yxatdan o'tish{% endblock title %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header">
                    <!-- TODO: Card header qo'shing -->
                </div>
                <div class="card-body">
                    <!-- TODO: Messages'larni ko'rsating -->
                    
                    <form method="post">
                        {% csrf_token %}
                        
                        <!-- TODO: Har bir form field uchun div yarating -->
                        <!-- first_name, last_name, email, username, password1, password2 -->
                        
                        <div class="d-grid">
                            <!-- TODO: Submit button qo'shing -->
                        </div>
                    </form>
                    
                    <div class="text-center mt-3">
                        <!-- TODO: Login sahifasiga link qo'shing -->
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

## Vazifa 5: Testlash va debugging

### 5.1 Manual testing

Quyidagi test stsenariylarini bajaring:

1. **Signup sahifasini ochish:**
   - `http://127.0.0.1:8000/accounts/signup/` ga kiring
   - Sahifa to'g'ri yuklanayotganini tekshiring

2. **Valid ma'lumotlar bilan test:**
   ```
   Ism: Ali
   Familiya: Valiyev
   Email: ali@example.com
   Username: alivaliyev
   Parol: mypassword123
   Parolni takrorlang: mypassword123
   ```

3. **Invalid ma'lumotlar bilan test:**
   ```
   - Bo'sh maydonlar bilan
   - Takrorlanuvchi email bilan
   - Qisqa username bilan
   - Mos kelmaydigan parollar bilan
   ```

4. **Auto-login testlash:**
   - Signup dan keyin avtomatik login qilinganini tekshiring
   - Navbar'da foydalanuvchi nomi ko'rinishini tekshiring

### 5.2 Django shell orqali testing

```python
# Terminal'da
python manage.py shell

# Foydalanuvchilarni tekshirish
from django.contrib.auth.models import User

# Barcha foydalanuvchilar
users = User.objects.all()
for user in users:
    print(f"Username: {user.username}, Email: {user.email}")

# Ma'lum bir foydalanuvchini topish
try:
    user = User.objects.get(username='alivaliyev')
    print(f"Ism: {user.first_name}, Familiya: {user.last_name}")
except User.DoesNotExist:
    print("Foydalanuvchi topilmadi")
```

### 5.3 Automated testing yaratish

**accounts/tests.py** faylini to'ldiring:

```python
# accounts/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('accounts:signup')
    
    def test_signup_page_loads(self):
        """Signup sahifasi to'g'ri yuklanayotganini test qilish"""
        # TODO: GET so'rovi yuborib, status code tekshiring
        pass
    
    def test_signup_with_valid_data(self):
        """To'g'ri ma'lumotlar bilan signup test qilish"""
        data = {
            # TODO: Test uchun ma'lumotlarni yozing
        }
        # TODO: POST so'rovi yuborib, redirect va user yaratilishini tekshiring
        pass
    
    def test_signup_with_invalid_data(self):
        """Noto'g'ri ma'lumotlar bilan signup test qilish"""
        data = {
            # TODO: Noto'g'ri ma'lumotlarni yozing
        }
        # TODO: Form xatolarini tekshiring
        pass
```

**Test'larni ishga tushirish:**
```bash
python manage.py test accounts
```

## Vazifa 6: Kengaytirilgan funksiyalar

### 6.1 Profile sahifasi qo'shish

**accounts/views.py** ga ProfileView qo'shing:

```python
# accounts/views.py ga qo'shimcha
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'
    
    def get_context_data(self, **kwargs):
        # TODO: Context'ga user ma'lumotlarini qo'shing
        pass
```

**templates/registration/profile.html** yarating:

```html
<!-- templates/registration/profile.html -->
{% extends 'base.html' %}

{% block title %}Profil{% endblock title %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">
                    <h4>Mening profilim</h4>
                </div>
                <div class="card-body">
                    <!-- TODO: User ma'lumotlarini ko'rsating -->
                    <p><strong>Ism:</strong> {{ user.first_name }}</p>
                    <!-- TODO: Qolgan ma'lumotlarni qo'shing -->
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

### 6.2 Email verification qo'shish

**accounts/forms.py** ga email verification logic qo'shing:

```python
# accounts/forms.py ga qo'shimcha
def clean_email(self):
    """Email formatini va mavjudligini tekshirish"""
    email = self.cleaned_data.get('email')
    
    # TODO: Email formati to'g'ri ekanligini tekshiring
    # TODO: Bu email allaqachon ishlatilmaganligini tekshiring
    
    return email
```

### 6.3 Success message'larni sozlash

**accounts/views.py** da turli xil message'lar qo'shing:

```python
# accounts/views.py da form_valid metodini yangilang
def form_valid(self, form):
    response = super().form_valid(form)
    user = form.save()
    login(self.request, user)
    
    # TODO: Turli xil success message'lar qo'shing
    messages.success(
        self.request, 
        f"Tabriklaymiz {user.first_name}! Siz muvaffaqiyatli ro'yxatdan o'tdingiz."
    )
    
    return response
```

## Vazifa 7: Error handling va debugging

### 7.1 Common errors va ularning yechimlari

**Error 1: TemplateDoesNotExist**
```
TemplateDoesNotExist at /accounts/signup/
registration/signup.html
```
**Yechimi:** `templates/registration/` papkasini yaratganingizni tekshiring

**Error 2: NoReverseMatch**
```
NoReverseMatch: Reverse for 'signup' not found
```
**Yechimi:** URL pattern'lar va namespace'lar to'g'ri yozilganligini tekshiring

**Error 3: Form validation error**
```
ValidationError: Username allaqachon mavjud
```
**Yechimi:** Form'dagi `clean_username` metodini tekshiring

### 7.2 Debug qilish usullari

**Debug print'lar qo'yish:**
```python
# views.py da
def form_valid(self, form):
    print(f"Form data: {form.cleaned_data}")  # Debug
    response = super().form_valid(form)
    print(f"User created: {form.save()}")      # Debug
    return response
```

**Django debug toolbar o'rnatish:**
```bash
pip install django-debug-toolbar
```

## Vazifa 8: Security va best practices

### 8.1 Security checklist

- [ ] CSRF token'lar ishlatilgan
- [ ] Input validation qo'shilgan
- [ ] SQL injection'dan himoyalangan
- [ ] Password complexity tekshirilgan
- [ ] Email duplication tekshirilgan

### 8.2 Performance optimizatsiya

**Database query'larini optimizatsiya qilish:**
```python
# views.py da
from django.db.models import Q

# Efficient user lookup
def get_user_by_email_or_username(email_or_username):
    return User.objects.filter(
        Q(email=email_or_username) | Q(username=email_or_username)
    ).first()
```

### 8.3 User experience yaxshilash

**Loading animation qo'shish:**
```html
<!-- signup.html'ga JavaScript qo'shing -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const submitBtn = document.querySelector('button[type="submit"]');
    
    form.addEventListener('submit', function() {
        submitBtn.innerHTML = 'Yuklanmoqda...';
        submitBtn.disabled = true;
    });
});
</script>
```

## Yakuniy tekshirish

### Muvaffaqiyatli yakunlash uchun checklist:

- [ ] Accounts app yaratilgan va settings'da qo'shilgan
- [ ] SignUpForm to'liq yozilgan va validation qo'shilgan
- [ ] SignUpView to'g'ri ishlayapti
- [ ] URL routing to'g'ri sozlangan
- [ ] Template'lar yaratilgan va to'g'ri ishlayapti
- [ ] Navbar'da login/signup linklari ko'rinayapti
- [ ] Auto-login signup'dan keyin ishlayapti
- [ ] Messages framework ishlayapti
- [ ] Test'lar yozilgan va o'tayapti
- [ ] Error handling qo'shilgan
- [ ] Security measures qo'llangan

### Final test scenariosi:

1. Serverni ishga tushiring: `python manage.py runserver`
2. `/accounts/signup/` sahifasiga kiring
3. To'g'ri ma'lumotlarni kiriting va submit qiling
4. Avtomatik login bo'lganligini tekshiring
5. Profil sahifasiga kiring
6. Logout qiling va login qiling
7. Barcha funksiyalar ishlaganligini tasdiqlang

## Qo'shimcha vazifalar (ixtiyoriy)

### 1. AJAX signup
jQuery yoki JavaScript bilan AJAX orqali signup jarayonini amalga oshiring

### 2. Social media signup
Google yoki Facebook orqali signup qo'shing

### 3. Email activation
Signup'dan keyin email activation talab qiling

### 4. Custom user model
AbstractUser'dan meros olib custom user model yarating

### 5. reCAPTCHA integration
Spam'dan himoya uchun Google reCAPTCHA qo'shing

Bu amaliyot darsini tugallagandan so'ng, siz Django'da professional darajada signup tizimini yarata olasiz!