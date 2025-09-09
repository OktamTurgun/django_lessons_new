# Dars 20 - Amaliyot: Class bilan Form View yaratish

## Maqsad
Bu amaliyotda siz Contact sahifasini Class-based FormView yordamida yaratib, forma bilan ishlashni o'rganasiz.

## Bosqichma-bosqich amaliyot

### 1-bosqich: Forma yaratish

`forms.py` faylini yarating va Contact formasini qo'shing:

```python
# forms.py
from django import forms

class ContactForm(forms.Form):
    """Bog'lanish uchun forma"""
    
    name = forms.CharField(
        max_length=100,
        label='Ism-familiya',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ism-familiyangizni kiriting',
            'required': True
        })
    )
    
    email = forms.EmailField(
        label='Email manzil',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com',
            'required': True
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        label='Telefon raqam',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998 90 123 45 67'
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        label='Xabar mavzusi',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Qisqacha mavzuni kiriting'
        })
    )
    
    message = forms.CharField(
        label='Xabar matni',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Xabaringizni batafsil yozing...'
        })
    )
    
    def clean_phone(self):
        """Telefon raqamini validatsiya qilish"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Faqat raqam va + belgisi bo'lishi kerak
            cleaned_phone = ''.join(filter(lambda x: x.isdigit() or x == '+', phone))
            if len(cleaned_phone) < 9:
                raise forms.ValidationError('Telefon raqam juda qisqa')
            return cleaned_phone
        return phone
    
    def clean_message(self):
        """Xabar uzunligini tekshirish"""
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Xabar kamida 10 ta belgi bo\'lishi kerak')
        return message
```

### 2-bosqich: Home sahifasi uchun FormView

Avval Home sahifasini oddiy TemplateView bilan yaratamiz:

```python
# views.py
from django.views.generic import TemplateView, FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ContactForm

class HomeView(TemplateView):
    """Bosh sahifa"""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Bosh sahifa'
        context['welcome_message'] = 'Xush kelibsiz!'
        return context
```

### 3-bosqich: Contact sahifasi uchun FormView

```python
# views.py ga qo'shish
class ContactView(FormView):
    """Bog'lanish sahifasi"""
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    
    def get_context_data(self, **kwargs):
        """Template'ga qo'shimcha ma'lumot jo'natish"""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Biz bilan bog\'lanish'
        context['company_info'] = {
            'name': 'IT Academy',
            'address': 'Toshkent shahar, Yunusobod tumani',
            'phone': '+998 71 123 45 67',
            'email': 'info@itacademy.uz'
        }
        return context
    
    def get_initial(self):
        """Formaning boshlang'ich qiymatlarini o'rnatish"""
        initial = super().get_initial()
        # Agar foydalanuvchi tizimga kirgan bo'lsa
        if self.request.user.is_authenticated:
            initial.update({
                'name': self.request.user.get_full_name() or self.request.user.username,
                'email': self.request.user.email,
            })
        return initial
    
    def form_valid(self, form):
        """Forma to'g'ri to'ldirilganda ishlaydigan metod"""
        # Forma ma'lumotlarini olish
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        
        # Bu yerda xabarni email orqali jo'natish yoki DB'ga saqlash
        # Hozircha console'ga chiqaramiz
        print("=== YANGI XABAR ===")
        print(f"Ism: {name}")
        print(f"Email: {email}")
        print(f"Telefon: {phone}")
        print(f"Mavzu: {subject}")
        print(f"Xabar: {message}")
        print("==================")
        
        # Muvaffaqiyat xabarini ko'rsatish
        messages.success(
            self.request, 
            f'Rahmat {name}! Xabaringiz muvaffaqiyatli jo\'natildi. '
            'Tez orada javob beramiz.'
        )
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Forma noto'g'ri to'ldirilganda ishlaydigan metod"""
        messages.error(
            self.request, 
            'Formada ba\'zi xatoliklar mavjud. Iltimos, qaytadan tekshiring.'
        )
        return super().form_invalid(form)
```

### 4-bosqich: URLs.py sozlash

```python
# urls.py
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
]
```

**Eslatma:** `.as_view()` metodini unutmang!

### 5-bosqich: Template'larni yaratish

#### Base template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}IT Academy{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'main:home' %}">IT Academy</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{% url 'main:home' %}">Bosh sahifa</a>
                <a class="nav-link" href="{% url 'main:contact' %}">Bog'lanish</a>
            </div>
        </div>
    </nav>

    <!-- Content -->
    <main class="py-4">
        {% block content %}
        {% endblock %}
    </main>

    <!-- Scripts -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### Home sahifasi template

```html
<!-- templates/home.html -->
{% extends 'base.html' %}

{% block title %}{{ page_title }} - IT Academy{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-12 text-center">
            <h1 class="display-4">{{ welcome_message }}</h1>
            <p class="lead">IT sohasidagi eng so'nggi yangiliklar va ma'lumotlar</p>
            <a href="{% url 'main:contact' %}" class="btn btn-primary btn-lg">
                Biz bilan bog'lanish
            </a>
        </div>
    </div>
</div>
{% endblock %}
```

#### Contact sahifasi template

```html
<!-- templates/contact.html -->
{% extends 'base.html' %}

{% block title %}{{ page_title }} - IT Academy{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <!-- Forma qismi -->
        <div class="col-md-8">
            <h2>{{ page_title }}</h2>
            
            <!-- Xabarlarni ko'rsatish -->
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
            
            <form method="post" novalidate>
                {% csrf_token %}
                
                <div class="mb-3">
                    <label for="{{ form.name.id_for_label }}" class="form-label">
                        {{ form.name.label }}
                    </label>
                    {{ form.name }}
                    {% if form.name.errors %}
                        <div class="text-danger">
                            {% for error in form.name.errors %}
                                <small class="d-block">{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="{{ form.email.id_for_label }}" class="form-label">
                                {{ form.email.label }}
                            </label>
                            {{ form.email }}
                            {% if form.email.errors %}
                                <div class="text-danger">
                                    {% for error in form.email.errors %}
                                        <small class="d-block">{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="{{ form.phone.id_for_label }}" class="form-label">
                                {{ form.phone.label }} (ixtiyoriy)
                            </label>
                            {{ form.phone }}
                            {% if form.phone.errors %}
                                <div class="text-danger">
                                    {% for error in form.phone.errors %}
                                        <small class="d-block">{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                
                <div class="mb-3">
                    <label for="{{ form.subject.id_for_label }}" class="form-label">
                        {{ form.subject.label }}
                    </label>
                    {{ form.subject }}
                    {% if form.subject.errors %}
                        <div class="text-danger">
                            {% for error in form.subject.errors %}
                                <small class="d-block">{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <div class="mb-3">
                    <label for="{{ form.message.id_for_label }}" class="form-label">
                        {{ form.message.label }}
                    </label>
                    {{ form.message }}
                    {% if form.message.errors %}
                        <div class="text-danger">
                            {% for error in form.message.errors %}
                                <small class="d-block">{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <button type="submit" class="btn btn-primary btn-lg">
                    <i class="fas fa-paper-plane"></i> Xabarni jo'natish
                </button>
            </form>
        </div>
        
        <!-- Kompaniya ma'lumotlari -->
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5>{{ company_info.name }}</h5>
                </div>
                <div class="card-body">
                    <p><strong>Manzil:</strong><br>{{ company_info.address }}</p>
                    <p><strong>Telefon:</strong><br>{{ company_info.phone }}</p>
                    <p><strong>Email:</strong><br>{{ company_info.email }}</p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 6-bosqich: Sinov qilish

1. Serverni ishga tushiring:
```bash
python manage.py runserver
```

2. Brauzerda `/` sahifasiga kiring
3. "Biz bilan bog'lanish" tugmasini bosing
4. Formani to'ldiring va jo'nating
5. Konsol (terminal) da xabar ko'rinishini tekshiring

### 7-bosqich: Qo'shimcha funksiyalar

Email jo'natish uchun real funksiya qo'shing:

```python
# views.py ga qo'shish
from django.core.mail import send_mail
from django.conf import settings

class ContactView(FormView):
    # ... oldingi kodlar ...
    
    def form_valid(self, form):
        # Forma ma'lumotlarini olish
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        
        # Email jo'natish
        try:
            email_subject = f"Yangi xabar: {subject}"
            email_message = f"""
            Yangi xabar keldi:
            
            Ism: {name}
            Email: {email}
            Telefon: {phone or 'Ko\'rsatilmagan'}
            
            Xabar:
            {message}
            """
            
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                ['admin@itacademy.uz'],
                fail_silently=False,
            )
            
            messages.success(
                self.request,
                f'Rahmat {name}! Xabaringiz muvaffaqiyatli jo\'natildi.'
            )
        except Exception as e:
            messages.error(
                self.request,
                'Xabar jo\'natishda xatolik yuz berdi. Keyinroq urinib ko\'ring.'
            )
            print(f"Email jo'natishda xato: {e}")
        
        return super().form_valid(form)
```

## Topshiriq

1. **Asosiy topshiriq:** Feedback sahifasini yarating
   - FeedbackForm yarating (name, email, rating, comment)
   - FeedbackView yarating (FormView inheritance)
   - Template yarating
   - URL qo'shing

2. **Qo'shimcha topshiriq:** Newsletter subscription qo'shing
   - NewsletterForm yarating (email, preferences)
   - Checkbox'lar bilan kategoriya tanlash imkonini qo'shing
   - AJAX bilan forma jo'natishni amalga oshiring

3. **Murakkab topshiriq:** File upload qo'shing
   - Contact formaga file maydonini qo'shing
   - Fayl o'lchamini cheklang (maksimal 5MB)
   - Faqat ma'lum formatlarni qabul qiling (pdf, doc, txt)

## Best Practices

1. **Forma validatsiyasi:** Har doim server-side validatsiya qiling
2. **Xavfsizlik:** CSRF token ishlatishni unutmang
3. **Foydalanuvchi tajribasi:** Loading spinner va success/error xabarlarini ko'rsating
4. **Kodni tashkil qilish:** Formalarni alohida forms.py faylida saqlang
5. **Email sozlamalari:** Production'da real SMTP sozlamalarini ishlating

## Xulosa

Siz muvaffaqiyatli Class-based FormView yordamida Contact sahifasini yaratdingiz. Bu usul kodni qayta ishlatish va Django'ning tayyor funksiyalaridan foydalanish imkonini beradi.