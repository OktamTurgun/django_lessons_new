# Dars 20: Class bilan Form View yaratish

## Dars maqsadi
Bu darsda siz Class-based Views (CBV) yordamida formalar bilan ishlashni o'rganasiz. FormView klassidan foydalanib, Contact sahifasini yaratish va forma ma'lumotlarini qayta ishlash jarayonini o'rganasiz.

## Nazariy qism

### Class-based Views (CBV) nima?
Class-based Views - Django'da view'larni sinf (class) ko'rinishida yozish usuli. Function-based view'larga nisbatan ko'proq imkoniyatlar beradi va kodni qayta ishlatishni osonlashtiradi.

**CBV afzalliklari:**
- Kodni qayta ishlatish imkoniyati
- Inheritance (meros) mexanizmini ishlatish
- Django'ning tayyor sinflarini ishlatish
- Kodni tashkil qilish osonroq

### FormView nima?
FormView - Django'ning tayyor sinfi bo'lib, formalar bilan ishlash uchun mo'ljallangan. Bu sinf quyidagi imkoniyatlarni beradi:

- Formani ko'rsatish (GET so'rov)
- Forma ma'lumotlarini qabul qilish (POST so'rov)
- Forma validatsiyasini tekshirish
- Muvaffaqiyatli jo'natilgandan keyin boshqa sahifaga yo'naltirish

## Amaliy qism

### 1. Contact sahifasini yaratish

Avval Contact sahifasi uchun forma yaratamiz:

```python
# forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ismingizni kiriting'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email manzilingizni kiriting'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xabar mavzusini kiriting'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Xabaringizni yozing...'
        })
    )
```

**Kod tushuntirishi:**
- `CharField` - matn maydonlari uchun
- `EmailField` - email validatsiyasi bilan
- `widget` - HTML elementlarini sozlash uchun
- `attrs` - HTML atributlarini qo'shish uchun

### 2. Function-based view (FBV) usuli

Avval oddiy funksiya ko'rinishidagi view'ni ko'ramiz:

```python
# views.py (FBV usuli)
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Forma ma'lumotlarini olish
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Bu yerda email jo'natish yoki ma'lumotlarni saqlash
            # Hozircha faqat xabar ko'rsatamiz
            messages.success(request, 'Xabaringiz muvaffaqiyatli jo\'natildi!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
```

### 3. Class-based view (CBV) usuli

Endi xuddi shu funksiyani Class-based view yordamida yozamiz:

```python
# views.py (CBV usuli)
from django.views.generic import FormView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import ContactForm

class ContactView(FormView):
    template_name = 'contact.html'  # Template fayli nomi
    form_class = ContactForm        # Foydalaniladigan forma
    success_url = reverse_lazy('contact')  # Muvaffaqiyatli jo'natilganda yo'naltirish
    
    def form_valid(self, form):
        """Forma to'g'ri to'ldirilganda ishlaydigan metod"""
        # Forma ma'lumotlarini olish
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        
        # Bu yerda email jo'natish yoki ma'lumotlarni saqlash
        # Hozircha faqat xabar ko'rsatamiz
        messages.success(self.request, 'Xabaringiz muvaffaqiyatli jo\'natildi!')
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Forma noto'g'ri to'ldirilganda ishlaydigan metod"""
        messages.error(self.request, 'Formada xatolik bor. Iltimos, qaytadan tekshiring.')
        return super().form_invalid(form)
```

**Kod tushuntirishi:**
- `template_name` - ishlatilaidigan template fayli
- `form_class` - ishlatilaidigan forma sinfi
- `success_url` - muvaffaqiyatli jo'natilganda yo'naltiriladigan URL
- `form_valid()` - forma to'g'ri validatsiyadan o'tganda chaqiriladigan metod
- `form_invalid()` - forma validatsiyadan o'tmagan holatda chaqiriladigan metod
- `reverse_lazy()` - URL'ni kechiktirib aniqlash uchun

### 4. URLs.py da ro'yxatdan o'tkazish

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Function-based view uchun
    # path('contact/', views.contact_view, name='contact'),
    
    # Class-based view uchun
    path('contact/', views.ContactView.as_view(), name='contact'),
]
```

**Eslatma:** CBV'ni ishlatish uchun `.as_view()` metodini chaqirish kerak.

### 5. Template yaratish

```html
<!-- templates/contact.html -->
{% extends 'base.html' %}

{% block title %}Biz bilan bog'lanish{% endblock %}

{% block content %}
<div class="container mt-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <h2>Biz bilan bog'lanish</h2>
            
            <!-- Xabarlarni ko'rsatish -->
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
                    <label for="{{ form.name.id_for_label }}" class="form-label">Ism</label>
                    {{ form.name }}
                    {% if form.name.errors %}
                        <div class="text-danger">
                            {% for error in form.name.errors %}
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
                    <label for="{{ form.subject.id_for_label }}" class="form-label">Mavzu</label>
                    {{ form.subject }}
                    {% if form.subject.errors %}
                        <div class="text-danger">
                            {% for error in form.subject.errors %}
                                <small>{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <div class="mb-3">
                    <label for="{{ form.message.id_for_label }}" class="form-label">Xabar</label>
                    {{ form.message }}
                    {% if form.message.errors %}
                        <div class="text-danger">
                            {% for error in form.message.errors %}
                                <small>{{ error }}</small>
                            {% endfor %}
                        </div>
                    {% endif %}
                </div>
                
                <button type="submit" class="btn btn-primary">Xabarni jo'natish</button>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### 6. FormView'ning boshqa metodlari

```python
class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    
    def get_context_data(self, **kwargs):
        """Template'ga qo'shimcha ma'lumot jo'natish"""
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Biz bilan bog\'lanish'
        context['company_name'] = 'MyCompany'
        return context
    
    def get_form_kwargs(self):
        """Forma yaratish uchun qo'shimcha parametrlar"""
        kwargs = super().get_form_kwargs()
        # Masalan, foydalanuvchi tizimga kirgan bo'lsa
        if self.request.user.is_authenticated:
            kwargs['initial'] = {
                'name': self.request.user.get_full_name(),
                'email': self.request.user.email,
            }
        return kwargs
    
    def get_success_url(self):
        """Success URL'ni dinamik ravishda aniqlash"""
        messages.success(self.request, 'Rahmat! Xabaringiz jo\'natildi.')
        return reverse_lazy('contact')
```

## FormView vs Function-based view

| Xususiyat | Function-based View | FormView |
|-----------|-------------------|----------|
| Kod miqdori | Ko'proq | Kamroq |
| Qayta ishlatish | Qiyin | Oson |
| Sozlash | To'liq nazorat | Cheklangan |
| O'rganish | Oson | Qiyinroq |
| Django metodlari | Qo'lda yozish | Tayyor |

## Xulosa

Class-based FormView quyidagi hollarda foydali:
- Standart formalar bilan ishlashda
- Kodni qayta ishlatish kerak bo'lganda
- Django'ning tayyor funksiyalaridan foydalanishda
- Katta loyihalarda tartib-intizom kerak bo'lganda

Function-based view'lar quyidagi hollarda yaxshi:
- Oddiy formalar uchun
- Maxsus logika kerak bo'lganda
- To'liq nazorat kerak bo'lganda
- Boshlang'ich o'rganish jarayonida

**Keyingi dars:**

Keyingi darsda ModelForm va oddiy Form o'rtasidagi farqlarni o'rganamiz va ma'lumotlar bazasi bilan bog'langan formalar yaratamiz.