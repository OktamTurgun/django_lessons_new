# Lesson 36: Practice - Signup Amaliyoti

## Amaliyot maqsadi
Ushbu amaliyotda siz o'z loyihangizda to'liq signup (ro'yxatdan o'tish) funksiyasini yaratib, uni sinab ko'rasiz.

## Bosqichma-bosqich amaliyot

### 1-amaliyot: accounts app yaratish va sozlash

**1.1. Yangi app yarating:**
```bash
python manage.py startapp accounts
```

**1.2. settings.py da ro'yxatga oling:**
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
    'accounts',  # Bu qatorni qo'shing
]
```

**Tekshirish:** Server ishlaganligini tekshiring:
```bash
python manage.py runserver
```

### 2-amaliyot: Asosiy signup view yaratish

**2.1. accounts/views.py faylini yarating:**
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
            # Foydalanuvchini yaratish va saqlash
            user = form.save()
            
            # Avtomatik login qilish
            login(request, user)
            
            # Muvaffaqiyat xabari
            messages.success(request, f"Xush kelibsiz {user.username}! Ro'yxatdan o'tish muvaffaqiyatli yakunlandi.")
            
            # Home sahifaga yo'naltirish
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})
```

**2.2. accounts/urls.py yarating:**
```python
# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
]
```

**2.3. Asosiy urls.py ni yangilang:**
```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news_app.urls')),
    path('accounts/', include('accounts.urls')),  # Bu qatorni qo'shing
]
```

### 3-amaliyot: Signup template yaratish

**3.1. templates/registration papkasini yarating:**
```bash
mkdir -p templates/registration
```

**3.2. signup.html faylini yarating:**
```html
<!-- templates/registration/signup.html -->

{% extends '_base.html' %}

{% block title %}Ro'yxatdan o'tish{% endblock title %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-primary text-white">
                    <h3 class="text-center mb-0">Ro'yxatdan o'tish</h3>
                </div>
                <div class="card-body">
                    <!-- Messages -->
                    {% if messages %}
                        {% for message in messages %}
                            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                                {{ message }}
                                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                            </div>
                        {% endfor %}
                    {% endif %}
                    
                    <!-- Form errors -->
                    {% if form.non_field_errors %}
                        <div class="alert alert-danger">
                            {% for error in form.non_field_errors %}
                                <p>{{ error }}</p>
                            {% endfor %}
                        </div>
                    {% endif %}
                    
                    <!-- Signup Form -->
                    <form method="post">
                        {% csrf_token %}
                        
                        <!-- Username -->
                        <div class="mb-3">
                            <label for="{{ form.username.id_for_label }}" class="form-label">
                                Foydalanuvchi nomi *
                            </label>
                            <input type="text" 
                                   class="form-control {% if form.username.errors %}is-invalid{% endif %}"
                                   id="{{ form.username.id_for_label }}"
                                   name="{{ form.username.name }}"
                                   value="{{ form.username.value|default:'' }}">
                            
                            {% if form.username.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.username.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                            
                            {% if form.username.help_text %}
                                <div class="form-text">{{ form.username.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <!-- Password 1 -->
                        <div class="mb-3">
                            <label for="{{ form.password1.id_for_label }}" class="form-label">
                                Parol *
                            </label>
                            <input type="password" 
                                   class="form-control {% if form.password1.errors %}is-invalid{% endif %}"
                                   id="{{ form.password1.id_for_label }}"
                                   name="{{ form.password1.name }}">
                            
                            {% if form.password1.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.password1.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                            
                            {% if form.password1.help_text %}
                                <div class="form-text">{{ form.password1.help_text }}</div>
                            {% endif %}
                        </div>
                        
                        <!-- Password 2 -->
                        <div class="mb-3">
                            <label for="{{ form.password2.id_for_label }}" class="form-label">
                                Parolni takrorlang *
                            </label>
                            <input type="password" 
                                   class="form-control {% if form.password2.errors %}is-invalid{% endif %}"
                                   id="{{ form.password2.id_for_label }}"
                                   name="{{ form.password2.name }}">
                            
                            {% if form.password2.errors %}
                                <div class="invalid-feedback">
                                    {% for error in form.password2.errors %}
                                        {{ error }}
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <!-- Submit button -->
                        <div class="d-grid mb-3">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-user-plus"></i> Ro'yxatdan o'tish
                            </button>
                        </div>
                    </form>
                    
                    <!-- Login link -->
                    <div class="text-center">
                        <p class="mb-0">Akkauntingiz bormi? 
                            <a href="{% url 'login' %}" class="text-decoration-none">Bu yerda kiring</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

### 4-amaliyot: Navigation'ga signup linkini qo'shish

**4.1. _base.html faylini yangilang:**
```html
<!-- templates/_base.html ichida navbar qismini topib, yangilang -->

<div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav me-auto">
        <li class="nav-item">
            <a class="nav-link" href="{% url 'home' %}">Bosh sahifa</a>
        </li>
        <!-- Boshqa menu itemlar -->
    </ul>
    
    <!-- User menu -->
    <ul class="navbar-nav">
        {% if user.is_authenticated %}
            <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" 
                   data-bs-toggle="dropdown">
                    <i class="fas fa-user"></i> {{ user.username }}
                </a>
                <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#">Profil</a></li>
                    <li><hr class="dropdown-divider"></li>
                    <li><a class="dropdown-item" href="{% url 'logout' %}">
                        <i class="fas fa-sign-out-alt"></i> Chiqish
                    </a></li>
                </ul>
            </li>
        {% else %}
            <li class="nav-item">
                <a class="nav-link" href="{% url 'accounts:signup' %}">
                    <i class="fas fa-user-plus"></i> Ro'yxatdan o'tish
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="{% url 'login' %}">
                    <i class="fas fa-sign-in-alt"></i> Kirish
                </a>
            </li>
        {% endif %}
    </ul>
</div>
```

### 5-amaliyot: Custom Signup Form yaratish

**5.1. accounts/forms.py yarating:**
```python
# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email manzilingiz'
        }),
        help_text='Haqiqiy email manzilini kiriting'
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ismingiz'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Familiyangiz'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Barcha fieldlarga CSS class qo'shish
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user
```

**5.2. views.py ni yangilang:**
```python
# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomSignupForm  # Import qo'shing

def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)  # CustomSignupForm ishlatamiz
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 
                f"Xush kelibsiz {user.first_name} {user.last_name}! Ro'yxatdan o'tish muvaffaqiyatli yakunlandi.")
            return redirect('home')
    else:
        form = CustomSignupForm()
    
    return render(request, 'registration/signup.html', {'form': form})
```

### 6-amaliyot: Template'ni yangilash (custom form uchun)

**6.1. signup.html ni yangilang:**
```html
<!-- templates/registration/signup.html -->
<!-- Faqat form qismini yangilaymiz -->

<form method="post">
    {% csrf_token %}
    
    <!-- Username -->
    <div class="mb-3">
        <label for="{{ form.username.id_for_label }}" class="form-label">
            Foydalanuvchi nomi *
        </label>
        {{ form.username }}
        {% if form.username.errors %}
            <div class="text-danger small">
                {% for error in form.username.errors %}
                    {{ error }}
                {% endfor %}
            </div>
        {% endif %}
        {% if form.username.help_text %}
            <div class="form-text">{{ form.username.help_text }}</div>
        {% endif %}
    </div>
    
    <!-- First Name -->
    <div class="mb-3">
        <label for="{{ form.first_name.id_for_label }}" class="form-label">
            Ism *
        </label>
        {{ form.first_name }}
        {% if form.first_name.errors %}
            <div class="text-danger small">
                {% for error in form.first_name.errors %}
                    {{ error }}
                {% endfor %}
            </div>
        {% endif %}
    </div>
    
    <!-- Last Name -->
    <div class="mb-3">
        <label for="{{ form.last_name.id_for_label }}" class="form-label">
            Familiya *
        </label>
        {{ form.last_name }}
        {% if form.last_name.errors %}
            <div class="text-danger small">
                {% for error in form.last_name.errors %}
                    {{ error }}
                {% endfor %}
            </div>
        {% endif %}
    </div>
    
    <!-- Email -->
    <div class="mb-3">
        <label for="{{ form.email.id_for_label }}" class="form-label">
            Email *
        </label>
        {{ form.email }}
        {% if form.email.errors %}
            <div class="text-danger small">
                {% for error in form.email.errors %}
                    {{ error }}
                {% endfor %}
            </div>
        {% endif %}
        {% if form.email.help_text %}
            <div class="form-text">{{ form.email.help_text }}</div>
        {% endif %}
    </div>
    
    <!-- Password 1 -->
    <div class="mb-3">
        <label for="{{ form.password1.id_for_label }}" class="form-label">
            Parol *
        </label>
        {{ form.password1 }}
        {% if form.password1.errors %}
            <div class="text-danger small">
                {% for error in form.password1.errors %}
                    {{ error }}
                {% endfor %}
            </div>
        {% endif %}
        {% if form.password1.help_text %}
            <div class="form-text">{{ form.password1.help_text }}</div>
        {% endif %}
    </div>
    
    <!-- Password 2 -->
    <div class="mb-3">
        <label for="{{ form.password2.id_for_label }}" class="form-label">
            Parolni takrorlang *
        </label>
        {{ form.password2 }}
        {% if form.password2.errors %}
            <div class="text-danger small">
                {% for error in form.password2.errors %}
                    {{ error }}
                {% endfor %}
            </div>
        {% endif %}
    </div>
    
    <!-- Submit button -->
    <div class="d-grid mb-3">
        <button type="submit" class="btn btn-primary btn-lg">
            <i class="fas fa-user-plus"></i> Ro'yxatdan o'tish
        </button>
    </div>
</form>
```

### 7-amaliyot: Testlash va Debug

**7.1. Migratsiyalarni tekshiring:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**7.2. Serverni ishga tushiring:**
```bash
python manage.py runserver
```

**7.3. Signup sahifasini sinang:**
- `http://127.0.0.1:8000/accounts/signup/` ga boring
- Barcha maydonlarni to'ldiring
- Formani yuborib ko'ring

**7.4. Xatoliklarni sinab ko'ring:**
- Bo'sh maydonlar bilan forma yuboring
- Parollarni turli xil kiritib ko'ring
- Mavjud username bilan ro'yxatdan o'tishga harakat qiling

### 8-amaliyot: Class-based View ga o'tish

**8.1. accounts/views.py ni yangilang:**
```python
# accounts/views.py

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomSignupForm

class SignupView(CreateView):
    form_class = CustomSignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        # Formani saqlash
        response = super().form_valid(form)
        
        # Yangi foydalanuvchini avtomatik login qilish
        login(self.request, self.object)
        
        # Muvaffaqiyatli xabar
        messages.success(self.request, 
            f"Xush kelibsiz {self.object.first_name} {self.object.last_name}! "
            f"Ro'yxatdan o'tish muvaffaqiyatli yakunlandi.")
        
        return response

# Eski function-based view ni comment qilish mumkin
# def signup_view(request):
#     ...
```

**8.2. accounts/urls.py ni yangilang:**
```python
# accounts/urls.py

from django.urls import path
from .views import SignupView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
]
```

### 9-amaliyot: Email validation qo'shish

**9.1. forms.py ga email validation qo'shish:**
```python
# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email manzilingiz'
        }),
        help_text='Haqiqiy email manzilini kiriting'
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ismingiz'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Familiyangiz'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    def clean_email(self):
        """Email unique ekanligini tekshirish"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Bu email manzili allaqachon ro'yxatdan o'tgan.")
        return email
        
    def clean_first_name(self):
        """Ism faqat harflardan iborat bo'lishini tekshirish"""
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise ValidationError("Ism faqat harflardan iborat bo'lishi kerak.")
        return first_name.title()  # Birinchi harfni katta qilish
        
    def clean_last_name(self):
        """Familiya faqat harflardan iborat bo'lishini tekshirish"""
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise ValidationError("Familiya faqat harflardan iborat bo'lishi kerak.")
        return last_name.title()  # Birinchi harfni katta qilish
            
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user
```

### 10-amaliyot: Success sahifasi yaratish

**10.1. templates/registration/signup_success.html yarating:**
```html
<!-- templates/registration/signup_success.html -->

{% extends '_base.html' %}

{% block title %}Ro'yxatdan o'tish muvaffaqiyatli{% endblock title %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card border-success">
                <div class="card-header bg-success text-white">
                    <h3 class="text-center mb-0">
                        <i class="fas fa-check-circle"></i> Tabriklaymiz!
                    </h3>
                </div>
                <div class="card-body text-center">
                    <div class="alert alert-success">
                        <h4>Ro'yxatdan o'tish muvaffaqiyatli yakunlandi!</h4>
                        <p class="mb-0">Siz endi saytning to'liq imkoniyatlaridan foydalanishingiz mumkin.</p>
                    </div>
                    
                    <div class="row mt-4">
                        <div class="col-md-4 mb-3">
                            <div class="card h-100">
                                <div class="card-body">
                                    <i class="fas fa-newspaper fa-3x text-primary mb-3"></i>
                                    <h5>Yangiliklar</h5>
                                    <p class="small">So'nggi yangiliklar bilan tanishib boring</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-4 mb-3">
                            <div class="card h-100">
                                <div class="card-body">
                                    <i class="fas fa-user-edit fa-3x text-info mb-3"></i>
                                    <h5>Profil</h5>
                                    <p class="small">O'z profilingizni tahrirlang</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="col-md-4 mb-3">
                            <div class="card h-100">
                                <div class="card-body">
                                    <i class="fas fa-comments fa-3x text-warning mb-3"></i>
                                    <h5>Izohlar</h5>
                                    <p class="small">Yangiliklarni izoh qoldiring</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-4">
                        <a href="{% url 'home' %}" class="btn btn-primary btn-lg me-2">
                            <i class="fas fa-home"></i> Bosh sahifa
                        </a>
                        <a href="#" class="btn btn-outline-secondary btn-lg">
                            <i class="fas fa-user"></i> Profilim
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock content %}
```

### 11-amaliyot: Final testing va optimizatsiya

**11.1. Barcha funksiyalarni sinab ko'ring:**

1. **Asosiy test holatlari:**
   - To'g'ri ma'lumotlar bilan ro'yxatdan o'tish
   - Noto'g'ri ma'lumotlar bilan test qilish
   - Mavjud email bilan test qilish
   - Parollar mos kelmaydigan holat

2. **Test ma'lumotlari:**
   ```
   Username: testuser123
   Ism: Akmal
   Familiya: Karimov
   Email: akmal@example.com
   Parol: mypassword123
   ```

**11.2. Xatoliklarni tekshiring:**
```bash
# Django loglarini ko'ring
python manage.py check
```

**11.3. CSS styling qo'shish:**
```css
/* static/css/style.css ga qo'shing */

.signup-card {
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
    border: none;
}

.form-control:focus {
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.btn-primary {
    background-color: #0d6efd;
    border-color: #0d6efd;
}

.btn-primary:hover {
    background-color: #0b5ed7;
    border-color: #0a58ca;
}

.alert-success {
    border-color: #d4edda;
    background-color: #d1e7dd;
    color: #0f5132;
}
```

### 12-amaliyot: Qo'shimcha xususiyatlar

**12.1. Password strength checker qo'shish:**
```javascript
// templates/registration/signup.html ichiga script qo'shing

<script>
function checkPasswordStrength() {
    const password = document.getElementById('id_password1').value;
    const strengthBar = document.getElementById('password-strength');
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    const strengthText = ['Juda zaif', 'Zaif', 'O\'rta', 'Kuchli', 'Juda kuchli'];
    const strengthColors = ['danger', 'warning', 'info', 'success', 'success'];
    
    if (password.length > 0) {
        strengthBar.innerHTML = `
            <div class="progress mt-2">
                <div class="progress-bar bg-${strengthColors[strength-1]}" 
                     style="width: ${strength * 20}%">${strengthText[strength-1]}</div>
            </div>
        `;
    } else {
        strengthBar.innerHTML = '';
    }
}

document.getElementById('id_password1').addEventListener('input', checkPasswordStrength);
</script>

<!-- Password field dan keyin qo'shing -->
<div id="password-strength"></div>
```

## Yakuniy testlash va natijalar

### Muvaffaqiyat mezonlari:
- ✅ Signup sahifasi to'g'ri ishlaydi
- ✅ Form validation ishlaydi
- ✅ Foydalanuvchi avtomatik login qilinadi
- ✅ Xabarlar to'g'ri ko'rsatiladi
- ✅ Navigation linklar ishlaydi
- ✅ Responsive dizayn

### Keyingi qadamlar:
1. Email verification qo'shish
2. Social media login qo'shish
3. CAPTCHA qo'shish
4. Password reset functionality
5. User profile yaratish

## Qo'shimcha vazifalar

### Mustaqil amaliyot:

**Vazifa 1: Telefon raqam qo'shish**
```python
# accounts/forms.py ga qo'shing
phone = forms.CharField(
    max_length=15,
    required=False,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+998901234567'
    }),
    help_text='Format: +998901234567'
)

def clean_phone(self):
    phone = self.cleaned_data.get('phone')
    if phone and not phone.startswith('+998'):
        raise ValidationError("Telefon raqam +998 bilan boshlanishi kerak")
    return phone
```

**Vazifa 2: Terms and Conditions checkbox**
```python
# accounts/forms.py ga qo'shing
agree_terms = forms.BooleanField(
    required=True,
    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    error_messages={'required': 'Shartlarga rozilik berish majburiy'}
)
```

**Vazifa 3: Template'da yangi maydonlarni ko'rsatish**
```html
<!-- Telefon raqam -->
<div class="mb-3">
    <label for="{{ form.phone.id_for_label }}" class="form-label">
        Telefon raqam
    </label>
    {{ form.phone }}
    {% if form.phone.help_text %}
        <div class="form-text">{{ form.phone.help_text }}</div>
    {% endif %}
</div>

<!-- Terms checkbox -->
<div class="mb-3 form-check">
    {{ form.agree_terms }}
    <label class="form-check-label" for="{{ form.agree_terms.id_for_label }}">
        Men <a href="#" target="_blank">foydalanish shartlari</a>ga roziman
    </label>
    {% if form.agree_terms.errors %}
        <div class="text-danger small">
            {% for error in form.agree_terms.errors %}
                {{ error }}
            {% endfor %}
        </div>
    {% endif %}
</div>
```

## Xulosa va natijalar

### O'rganganimiz:
✅ Django'da signup tizimini yaratish
✅ Custom form yaratish va validation
✅ Function-based va Class-based View'lar
✅ Template yaratish va styling
✅ Form xatolarini boshqarish
✅ User authentication workflow

### Amaliy natijalar:
- To'liq ishlaydigan ro'yxatdan o'tish tizimi
- Professional ko'rinishdagi form
- Xavfsiz validation sistemasi
- Responsive dizayn
- User-friendly interface

### Keyingi darslarda:
- **Lesson 37**: Email verification
- **Lesson 38**: User profile yaratish
- **Lesson 39**: Password reset funksiyasi
- **Lesson 40**: Social media login

### Yakuniy Git comandalari:
```bash
# Barcha o'zgarishlarni saqlash
git add .
git status
git commit -m "feat: Add complete signup functionality

- Create accounts app
- Add custom signup form with validation
- Implement class-based and function-based views
- Create responsive signup template
- Add email and name validation
- Implement automatic login after signup
- Add success messages and error handling"

git push origin main
```

### Debug va troubleshooting:
Agar muammolar yuzaga kelsa:

1. **Server ishlamayotgan bo'lsa:**
   ```bash
   python manage.py check
   python manage.py migrate
   python manage.py runserver
   ```

2. **Template topilmayotgan bo'lsa:**
   - `templates/registration/` papkasi mavjudligini tekshiring
   - `settings.py` da TEMPLATES sozlamalarini ko'ring

3. **CSS ishlamayotgan bo'lsa:**
   - Static files yo'lini tekshiring
   - `python manage.py collectstatic` ishga tushiring

4. **Form ishlamayotgan bo'lsa:**
   - CSRF token borligini tekshiring
   - Form fieldlarining nomlari to'g'riligini tekshiring

### Performance va xavfsizlik:
- Parol kuchliligini tekshirish
- CAPTCHA qo'shishni o'ylang
- Rate limiting qo'shing
- Email verification qo'shing

Bu bilan **Lesson 36 Practice** to'liq yakunlandi! Siz endi professional darajada signup tizimini yaratishni bilasiz.