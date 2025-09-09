# Dars 19: Formalar bilan ishlash. Contact form

## Kirish

Django'da formalar veb-ilovalarimizda foydalanuvchi bilan o'zaro muloqot qilishning asosiy vositalaridan biridir. Contact form (aloqa formasi) deyarli har bir veb-saytda mavjud bo'lgan muhim komponentdir. Ushbu darsda Django'ning form tizimi bilan tanishib, contact form yaratishni o'rganamiz.

## Django Forms nima?

Django Forms - bu HTML formalarini yaratish, validatsiya qilish va qayta ishlash uchun mo'ljallangan Django'ning ichki tizimi. Django Forms quyidagi afzalliklarga ega:

- Xavfsizlik (CSRF himoyasi)
- Avtomatik validatsiya
- HTML generatsiya qilish
- Ma'lumotlarni tozalash (cleaning)
- Xatolarni boshqarish

## Contact Form yaratish

### 1-bosqich: forms.py faylini yaratish

Birinchi navbatda, loyihangizning asosiy papkasida `forms.py` fayli yaratamiz:

```python
# forms.py
from django import forms

class ContactForm(forms.Form):
    # Ism maydon
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ismingizni kiriting'
        })
    )
    
    # Email maydon
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email manzilingiz'
        })
    )
    
    # Telefon maydon (ixtiyoriy)
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998 90 123 45 67'
        })
    )
    
    # Mavzu maydon
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xabar mavzusi'
        })
    )
    
    # Xabar matni
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Xabaringizni yozing...'
        })
    )
```

### Kod tushuntirishi:

- `forms.CharField()` - matn kiritish maydonini yaratadi
- `forms.EmailField()` - email validatsiyasi bilan maydon
- `max_length` - maksimal belgilar soni
- `required=False` - maydon to'ldirilishi majburiy emas
- `widget` - HTML input turini va atributlarini belgilaydi
- `attrs` - HTML atributlarini qo'shish (class, placeholder, va boshqalar)

### 2-bosqich: View yaratish

`views.py` faylida contact form uchun view yaratamiz:

```python
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Formadan ma'lumotlarni olish
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data.get('phone', '')
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Email yuborish (ixtiyoriy)
            try:
                full_message = f"""
                Ism: {name}
                Email: {email}
                Telefon: {phone}
                
                Xabar:
                {message}
                """
                
                send_mail(
                    subject=f'Contact Form: {subject}',
                    message=full_message,
                    from_email=email,
                    recipient_list=['your-email@example.com'],
                    fail_silently=False,
                )
                
                # Muvaffaqiyatli xabar
                messages.success(request, 'Xabaringiz muvaffaqiyatli yuborildi!')
                
            except Exception as e:
                # Xato xabari
                messages.error(request, 'Xatolik yuz berdi. Qaytadan urinib ko\'ring.')
            
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)
```

### Kod tushuntirishi:

- `request.method == 'POST'` - form yuborilganmi tekshirish
- `form.is_valid()` - form validatsiyasini tekshirish
- `form.cleaned_data` - tozalangan va validatsiya qilingan ma'lumotlar
- `messages.success()` - muvaffaqiyat xabari
- `redirect()` - sahifani qayta yo'naltirish

### 3-bosqich: Template yaratish

`templates` papkasida `contact.html` fayli yaratamiz:

```html
<!-- contact.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Biz bilan bog'lanish{% endblock %}

{% block content %}
<div class="container my-5">
    <div class="row">
        <div class="col-md-8 mx-auto">
            <h2 class="text-center mb-4">Biz bilan bog'lanish</h2>
            
            <!-- Xabarlar ko'rsatish -->
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
            
            <div class="card shadow">
                <div class="card-body p-4">
                    <form method="post">
                        {% csrf_token %}
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="{{ form.name.id_for_label }}" class="form-label">Ism *</label>
                                {{ form.name }}
                                {% if form.name.errors %}
                                    <div class="text-danger mt-1">
                                        {% for error in form.name.errors %}
                                            <small>{{ error }}</small>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label for="{{ form.email.id_for_label }}" class="form-label">Email *</label>
                                {{ form.email }}
                                {% if form.email.errors %}
                                    <div class="text-danger mt-1">
                                        {% for error in form.email.errors %}
                                            <small>{{ error }}</small>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label for="{{ form.phone.id_for_label }}" class="form-label">Telefon</label>
                                {{ form.phone }}
                                {% if form.phone.errors %}
                                    <div class="text-danger mt-1">
                                        {% for error in form.phone.errors %}
                                            <small>{{ error }}</small>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label for="{{ form.subject.id_for_label }}" class="form-label">Mavzu *</label>
                                {{ form.subject }}
                                {% if form.subject.errors %}
                                    <div class="text-danger mt-1">
                                        {% for error in form.subject.errors %}
                                            <small>{{ error }}</small>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.message.id_for_label }}" class="form-label">Xabar *</label>
                            {{ form.message }}
                            {% if form.message.errors %}
                                <div class="text-danger mt-1">
                                    {% for error in form.message.errors %}
                                        <small>{{ error }}</small>
                                    {% endfor %}
                                </div>
                            {% endif %}
                        </div>
                        
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-lg">
                                <i class="fas fa-paper-plane me-2"></i>Yuborish
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- Qo'shimcha ma'lumotlar -->
            <div class="row mt-5">
                <div class="col-md-4 text-center mb-3">
                    <div class="card border-0">
                        <div class="card-body">
                            <i class="fas fa-map-marker-alt fa-3x text-primary mb-3"></i>
                            <h5>Manzil</h5>
                            <p>Toshkent shahri<br>Chilonzor tumani</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4 text-center mb-3">
                    <div class="card border-0">
                        <div class="card-body">
                            <i class="fas fa-phone fa-3x text-primary mb-3"></i>
                            <h5>Telefon</h5>
                            <p>+998 90 123 45 67<br>+998 71 123 45 67</p>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-4 text-center mb-3">
                    <div class="card border-0">
                        <div class="card-body">
                            <i class="fas fa-envelope fa-3x text-primary mb-3"></i>
                            <h5>Email</h5>
                            <p>info@example.com<br>support@example.com</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Template tushuntirishi:

- `{% csrf_token %}` - CSRF himoyasi (majburiy)
- `{{ form.name }}` - form maydonini chiqarish
- `form.name.errors` - maydon xatolarini ko'rsatish
- `messages` - xabarlarni ko'rsatish (success, error)
- Bootstrap classlari - chiroyli ko'rinish uchun

### 4-bosqich: URL konfiguratsiyasi

`urls.py` faylida URL qo'shamiz:

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Boshqa URL'lar
    path('contact/', views.contact_view, name='contact'),
]
```

## Form Validatsiyasi

Django formalarida maxsus validatsiya qo'shish mumkin:

```python
# forms.py
from django import forms
from django.core.exceptions import ValidationError
import re

class ContactForm(forms.Form):
    # ... boshqa maydonlar ...
    
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+998 90 123 45 67'
        })
    )
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Telefon raqam formatini tekshirish
            pattern = r'^\+998\s?\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$'
            if not re.match(pattern, phone):
                raise ValidationError('Telefon raqam +998 XX XXX XX XX formatida bo\'lishi kerak')
        return phone
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            # Ismda faqat harflar bo'lishi kerak
            if not name.replace(' ', '').isalpha():
                raise ValidationError('Ismda faqat harflar bo\'lishi mumkin')
        return name
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        
        # Email yoki telefon kamida bittasi bo'lishi kerak
        if not email and not phone:
            raise ValidationError('Email yoki telefon raqam kamida bittasi kiritilishi kerak')
        
        return cleaned_data
```

## Email sozlamalari

Email yuborish uchun `settings.py` faylida sozlamalar:

```python
# settings.py

# Gmail uchun
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # App password

# Yoki console uchun (test)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Xulosa

Ushbu darsda biz Django'da contact form yaratishni o'rgandik. Asosiy e'tibor berilgan masalalar:

1. **Django Forms** - formalar yaratish va validatsiya
2. **Form maydonlari** - turli xil input turlari
3. **Form ishlov berish** - POST so'rovlarni qayta ishlash
4. **Template renderlash** - formani HTML'da ko'rsatish
5. **Xatolarni boshqarish** - validatsiya xatolari va xabarlar
6. **Email yuborish** - contact form orqali email yuborish

**Keyingi dars:**
Keyingi darsda biz Class-based view (FormView) bilan ishlay olishni o'rganamiz, bu esa kod yozishni yanada sodda va tezroq qiladi.