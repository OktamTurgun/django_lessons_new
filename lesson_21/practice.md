# Dars 21 - Amaliyot: ModelForm vs Form

## Maqsad
Bu amaliyotda siz Form va ModelForm o'rtasidagi farqlarni amaliy ravishda ko'rasiz va ikki xil yondashuvni qiyoslaysiz.

## Loyiha tuzilmasi
```
news_project/
  ├── models.py
  ├── forms.py
  ├── views.py
  ├── urls.py
  └── templates/
      ├── base.html
      ├── contact_form.html      # Oddiy Form
      ├── contact_modelform.html # ModelForm
      ├── search.html            # Search Form
      └── news_form.html         # News ModelForm
```

## 1-bosqich: Modellarni yaratish

```python
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Category(models.Model):
    """Yangilik kategoriyalari"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Kategoriya nomi')
    slug = models.SlugField(unique=True, verbose_name='URL nomi')
    description = models.TextField(blank=True, verbose_name='Tavsif')
    
    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class News(models.Model):
    """Yangiliklar modeli"""
    title = models.CharField(max_length=200, verbose_name='Sarlavha')
    slug = models.SlugField(unique=True, verbose_name='URL nomi')
    content = models.TextField(verbose_name='Matn')
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Muallif'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        verbose_name='Kategoriya'
    )
    image = models.ImageField(
        upload_to='news/%Y/%m/', 
        blank=True, 
        verbose_name='Rasm'
    )
    published = models.BooleanField(default=False, verbose_name='Nashr etilsinmi')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Yangilangan')
    
    class Meta:
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Contact(models.Model):
    """Bog'lanish ma'lumotlari - ModelForm uchun"""
    name = models.CharField(max_length=100, verbose_name='Ism-familiya')
    email = models.EmailField(verbose_name='Email manzil')
    phone = models.CharField(
        max_length=20,
        verbose_name='Telefon raqam',
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Telefon raqam formati: +998901234567'
        )],
        blank=True
    )
    subject = models.CharField(max_length=200, verbose_name='Mavzu')
    message = models.TextField(verbose_name='Xabar')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Qabul qilingan')
    is_read = models.BooleanField(default=False, verbose_name='O\'qilganmi')
    
    class Meta:
        verbose_name = 'Bog\'lanish'
        verbose_name_plural = 'Bog\'lanishlar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
```

## 2-bosqich: Formalarni yaratish

```python
# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import News, Category, Contact

# ============= ODDIY FORMALAR =============

class ContactForm(forms.Form):
    """Oddiy Contact Form - ma'lumotni saqlamaydi"""
    name = forms.CharField(
        max_length=100,
        label='Ism-familiya',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ism-familiyangizni kiriting'
        })
    )
    email = forms.EmailField(
        label='Email manzil',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
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
            'placeholder': 'Qisqacha mavzu kiriting'
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
        """Telefon raqam validatsiyasi"""
        phone = self.cleaned_data.get('phone')
        if phone:
            import re
            if not re.match(r'^\+?1?\d{9,15}$', phone):
                raise forms.ValidationError('Telefon raqam formati noto\'g\'ri')
        return phone
    
    def clean_message(self):
        """Xabar uzunligi validatsiyasi"""
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Xabar kamida 10 ta belgi bo\'lishi kerak')
        return message
    
    def send_notification(self):
        """Email jo'natish (oddiy form'da qo'lda yoziladi)"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        try:
            send_mail(
                f"Yangi xabar: {self.cleaned_data['subject']}",
                f"Ism: {self.cleaned_data['name']}\n"
                f"Email: {self.cleaned_data['email']}\n"
                f"Telefon: {self.cleaned_data['phone'] or 'Ko\'rsatilmagan'}\n\n"
                f"Xabar:\n{self.cleaned_data['message']}",
                settings.DEFAULT_FROM_EMAIL,
                ['admin@example.com'],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Email jo'natishda xato: {e}")
            return False

class SearchForm(forms.Form):
    """Qidiruv formasi - ma'lumotni saqlamaydi"""
    query = forms.CharField(
        max_length=200,
        label='Qidiruv so\'zi',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nima qidiryapsiz?'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='Barcha kategoriyalar',
        label='Kategoriya',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        label='Sanadan',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        label='Sanagacha',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    def clean(self):
        """Sanalar validatsiyasi"""
        cleaned_data = super().clean()
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise forms.ValidationError('Boshlanish sanasi tugash sanasidan kichik bo\'lishi kerak')
        
        return cleaned_data

# ============= MODEL FORMALAR =============

class ContactModelForm(forms.ModelForm):
    """Contact modeli uchun ModelForm"""
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ism-familiyangizni kiriting'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+998 90 123 45 67'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Qisqacha mavzu kiriting'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Xabaringizni batafsil yozing...'
            })
        }
        labels = {
            'name': 'Ism-familiya',
            'email': 'Email manzil',
            'phone': 'Telefon raqam (ixtiyoriy)',
            'subject': 'Xabar mavzusi',
            'message': 'Xabar matni'
        }
    
    def clean_message(self):
        """Qo'shimcha validatsiya"""
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Xabar kamida 10 ta belgi bo\'lishi kerak')
        return message
    
    def save(self, commit=True):
        """Saqlashda qo'shimcha amallar"""
        contact = super().save(commit=False)
        
        # Ismni formatlash
        contact.name = contact.name.title()
        
        if commit:
            contact.save()
            
            # Email jo'natish (ModelForm'da ham qilish mumkin)
            self.send_notification(contact)
        
        return contact
    
    def send_notification(self, contact):
        """Email jo'natish"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        try:
            send_mail(
                f"Yangi xabar: {contact.subject}",
                f"Ism: {contact.name}\n"
                f"Email: {contact.email}\n"
                f"Telefon: {contact.phone or 'Ko\'rsatilmagan'}\n\n"
                f"Xabar:\n{contact.message}",
                settings.DEFAULT_FROM_EMAIL,
                ['admin@example.com'],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email jo'natishda xato: {e}")

class NewsModelForm(forms.ModelForm):
    """Yangilik yaratish uchun ModelForm"""
    
    class Meta:
        model = News
        fields = ['title', 'content', 'category', 'image', 'published']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Yangilik sarlavhasini kiriting'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Yangilik matnini kiriting...'
            }),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Sarlavha',
            'content': 'Matn',
            'category': 'Kategoriya',
            'image': 'Rasm (ixtiyoriy)',
            'published': 'Darhol nashr etish'
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_title(self):
        """Sarlavha validatsiyasi"""
        title = self.cleaned_data.get('title')
        if News.objects.filter(title__iexact=title).exists():
            raise forms.ValidationError('Bunday sarlavha allaqachon mavjud')
        return title
    
    def save(self, commit=True):
        """Muallif bilan saqlash"""
        news = super().save(commit=False)
        if self.user:
            news.author = self.user
        
        # Slug yaratish
        from django.utils.text import slugify
        import uuid
        base_slug = slugify(news.title)
        news.slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
        
        if commit:
            news.save()
        
        return news
```

## 3-bosqich: View'larni yaratish

```python
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, CreateView, ListView, TemplateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import (
    ContactForm, 
    ContactModelForm, 
    SearchForm, 
    NewsModelForm
)
from .models import News, Contact, Category

# ============= ODDIY FORM VIEWS =============

class ContactFormView(FormView):
    """Oddiy Form bilan Contact sahifasi"""
    template_name = 'contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_form')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'Oddiy Form'
        context['description'] = 'Bu oddiy Form yordamida yaratilgan. Ma\'lumotlar DB\'ga saqlanmaydi.'
        return context
    
    def form_valid(self, form):
        """Form to'g'ri to'ldirilganda"""
        # Email jo'natish
        if form.send_notification():
            messages.success(
                self.request,
                f"Rahmat {form.cleaned_data['name']}! "
                "Xabaringiz jo'natildi. Tez orada javob beramiz."
            )
        else:
            messages.error(
                self.request,
                "Xabar jo'natishda xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring."
            )
        
        # Console'ga chiqarish
        print("=== ODDIY FORM MA'LUMOTLARI ===")
        print(f"Ism: {form.cleaned_data['name']}")
        print(f"Email: {form.cleaned_data['email']}")
        print(f"Telefon: {form.cleaned_data['phone']}")
        print(f"Mavzu: {form.cleaned_data['subject']}")
        print(f"Xabar: {form.cleaned_data['message']}")
        print("================================")
        
        return super().form_valid(form)

class SearchView(FormView):
    """Qidiruv sahifasi - Oddiy Form"""
    template_name = 'search.html'
    form_class = SearchForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Agar forma jo'natilgan bo'lsa, qidiruv natijalarini ko'rsatish
        if self.request.method == 'GET' and 'query' in self.request.GET:
            form = SearchForm(self.request.GET)
            if form.is_valid():
                context['results'] = self.search_news(form.cleaned_data)
                context['search_performed'] = True
        
        return context
    
    def search_news(self, cleaned_data):
        """Yangiliklar qidirish"""
        query = cleaned_data.get('query', '')
        category = cleaned_data.get('category')
        date_from = cleaned_data.get('date_from')
        date_to = cleaned_data.get('date_to')
        
        news_list = News.objects.filter(published=True)
        
        if query:
            news_list = news_list.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        
        if category:
            news_list = news_list.filter(category=category)
        
        if date_from:
            news_list = news_list.filter(created_at__date__gte=date_from)
        
        if date_to:
            news_list = news_list.filter(created_at__date__lte=date_to)
        
        return news_list[:20]  # Faqat 20 ta natija

# ============= MODEL FORM VIEWS =============

class ContactModelFormView(CreateView):
    """ModelForm bilan Contact sahifasi"""
    model = Contact
    form_class = ContactModelForm
    template_name = 'contact_modelform.html'
    success_url = reverse_lazy('contact_modelform')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_type'] = 'ModelForm'
        context['description'] = 'Bu ModelForm yordamida yaratilgan. Ma\'lumotlar DB\'ga saqlanadi.'
        return context
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f"Rahmat {form.cleaned_data['name']}! "
            "Xabaringiz saqlandi va jo'natildi."
        )
        return super().form_valid(form)

class NewsCreateView(LoginRequiredMixin, CreateView):
    """Yangilik yaratish - ModelForm"""
    model = News
    form_class = NewsModelForm
    template_name = 'news_form.html'
    success_url = reverse_lazy('news_list')
    
    def get_form_kwargs(self):
        """Form'ga user'ni uzatish"""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        messages.success(
            self.request,
            f"Yangilik '{form.cleaned_data['title']}' muvaffaqiyatli yaratildi!"
        )
        return super().form_valid(form)

class NewsListView(ListView):
    """Yangiliklar ro'yxati"""
    model = News
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        return News.objects.filter(published=True).select_related('author', 'category')

class ComparisonView(TemplateView):
    """Form vs ModelForm taqqoslash sahifasi"""
    template_name = 'comparison.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts_count'] = Contact.objects.count()
        context['recent_contacts'] = Contact.objects.order_by('-created_at')[:5]
        return context
```

## 4-bosqich: URL konfiguratsiyasi

```python
# urls.py
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Oddiy Form'lar
    path('contact-form/', views.ContactFormView.as_view(), name='contact_form'),
    path('search/', views.SearchView.as_view(), name='search'),
    
    # ModelForm'lar
    path('contact-modelform/', views.ContactModelFormView.as_view(), name='contact_modelform'),
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    
    # Taqqoslash
    path('comparison/', views.ComparisonView.as_view(), name='comparison'),
]
```

## 5-bosqich: Template'larni yaratish

### Base template

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Form vs ModelForm{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'main:comparison' %}">
                <i class="fas fa-code"></i> Django Forms
            </a>
            
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
                            Oddiy Form
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="{% url 'main:contact_form' %}">Contact Form</a></li>
                            <li><a class="dropdown-item" href="{% url 'main:search' %}">Search Form</a></li>
                        </ul>
                    </li>
                    
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">
                            ModelForm
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="{% url 'main:contact_modelform' %}">Contact ModelForm</a></li>
                            <li><a class="dropdown-item" href="{% url 'main:news_create' %}">News Create</a></li>
                        </ul>
                    </li>
                    
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'main:news_list' %}">Yangiliklar</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Messages -->
    {% if messages %}
        <div class="container mt-3">
            {% for message in messages %}
                <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                    <i class="fas fa-info-circle"></i> {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            {% endfor %}
        </div>
    {% endif %}

    <!-- Content -->
    <main class="container my-4">
        {% block content %}
        {% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container text-center">
            <p>&copy; 2024 Django Forms Tutorial. Form vs ModelForm</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Contact Form template (oddiy)

```html
<!-- templates/contact_form.html -->
{% extends 'base.html' %}

{% block title %}{{ form_type }} - Contact{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header bg-info text-white">
                <h4><i class="fas fa-envelope"></i> {{ form_type }} - Bog'lanish</h4>
                <small>{{ description }}</small>
            </div>
            <div class="card-body">
                <form method="post" novalidate>
                    {% csrf_token %}
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">{{ form.name.label }}</label>
                                {{ form.name }}
                                {% if form.name.errors %}
                                    <div class="text-danger">
                                        {% for error in form.name.errors %}
                                            <small>{{ error }}</small><br>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">{{ form.email.label }}</label>
                                {{ form.email }}
                                {% if form.email.errors %}
                                    <div class="text-danger">
                                        {% for error in form.email.errors %}
                                            <small>{{ error }}</small><br>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">{{ form.phone.label }}</label>
                                {{ form.phone }}
                                {% if form.phone.errors %}
                                    <div class="text-danger">
                                        {% for error in form.phone.errors %}
                                            <small>{{ error }}</small><br>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">{{ form.subject.label }}</label>
                                {{ form.subject }}
                                {% if form.subject.errors %}
                                    <div class="text-danger">
                                        {% for error in form.subject.errors %}
                                            <small>{{ error }}</small><br>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">{{ form.message.label }}</label>
                        {{ form.message }}
                        {% if form.message.errors %}
                            <div class="text-danger">
                                {% for error in form.message.errors %}
                                    <small>{{ error }}</small><br>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    
                    <button type="submit" class="btn btn-info btn-lg">
                        <i class="fas fa-paper-plane"></i> Jo'natish (Form)
                    </button>
                </form>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-info-circle"></i> Oddiy Form</h5>
            </div>
            <div class="card-body">
                <h6>Xususiyatlari:</h6>
                <ul class="list-unstyled">
                    <li><i class="fas fa-times text-danger"></i> DB'ga saqlanmaydi</li>
                    <li><i class="fas fa-check text-success"></i> Email jo'natadi</li>
                    <li><i class="fas fa-check text-success"></i> Custom validatsiya</li>
                    <li><i class="fas fa-check text-success"></i> To'liq nazorat</li>
                </ul>
                
                <hr>
                <a href="{% url 'main:contact_modelform' %}" class="btn btn-success">
                    ModelForm'ni sinab ko'ring
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### Contact ModelForm template

```html
<!-- templates/contact_modelform.html -->
{% extends 'base.html' %}

{% block title %}{{ form_type }} - Contact{% endblock %}

{% block content %}
<div class="row">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header bg-success text-white">
                <h4><i class="fas fa-database"></i> {{ form_type }} - Bog'lanish</h4>
                <small>{{ description }}</small>
            </div>
            <div class="card-body">
                <form method="post" novalidate>
                    {% csrf_token %}
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">{{ form.name.label }}</label>
                                {{ form.name }}
                                {% if form.name.errors %}
                                    <div class="text-danger">
                                        {% for error in form.name.errors %}
                                            <small>{{ error }}</small><br>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">{{ form.email.label }}</label>
                                {{ form.email }}
                                {% if form.email.errors %}
                                    <div class="text-danger">
                                        {% for error in form.email.errors %}
                                            <small>{{ error }}</small><br>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">{{ form.phone.label }}</label>
                                {{ form.phone }}
                                {% if form.phone.errors %}
                                    <div class="text-danger">
                                        {% for error in form.phone.errors %}
                                            <small>{{ error }}</small><br>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-3">
                                <label class="form-label">{{ form.subject.label }}</label>
                                {{ form.subject }}
                                {% if form.subject.errors %}
                                    <div class="text-danger">
                                        {% for error in form.subject.errors %}
                                            <small>{{ error }}</small><br>
                                        {% endfor %}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                    </div>
                    
                    <div class="mb-3">
                        <label class="form-label">{{ form.message.label }}</label>
                        {{ form.message }}
                        {% if form.message.errors %}
                            <div class="text-danger">
                                {% for error in form.message.errors %}
                                    <small>{{ error }}</small><br>
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                    
                    <button type="submit" class="btn btn-success btn-lg">
                        <i class="fas fa-save"></i> Saqlash (ModelForm)
                    </button>
                </form>
            </div>
        </div>
    </div>
    
    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-database"></i> ModelForm</h5>
            </div>
            <div class="card-body">
                <h6>Xususiyatlari:</h6>
                <ul class="list-unstyled">
                    <li><i class="fas fa-check text-success"></i> DB'ga saqlanadi</li>
                    <li><i class="fas fa-check text-success"></i> Model validatsiyasi</li>
                    <li><i class="fas fa-check text-success"></i> Kamroq kod</li>
                    <li><i class="fas fa-check text-success"></i> save() metodi</li>
                </ul>
                
                <hr>
                <a href="{% url 'main:comparison' %}" class="btn btn-primary">
                    Taqqoslashni ko'ring
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 6-bosqich: Qiyoslash sahifasi

```html
<!-- templates/comparison.html -->
{% extends 'base.html' %}

{% block title %}Form vs ModelForm Taqqoslash{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <h1 class="text-center mb-4">
            <i class="fas fa-balance-scale"></i> Form vs ModelForm
        </h1>
    </div>
</div>

<div class="row">
    <div class="col-md-6">
        <div class="card border-info">
            <div class="card-header bg-info text-white">
                <h4><i class="fas fa-code"></i> Oddiy Form</h4>
            </div>
            <div class="card-body">
                <h6>Afzalliklari:</h6>
                <ul class="text-success">
                    <li>To'liq nazorat</li>
                    <li>Murakkab validatsiya</li>
                    <li>Bir nechta model bilan ishlash</li>
                    <li>Ma'lumotni saqlamaslik</li>
                </ul>
                
                <h6>Kamchiliklari:</h6>
                <ul class="text-danger">
                    <li>Ko'proq kod yozish</li>
                    <li>Qo'lda validatsiya</li>
                    <li>Model bilan bog'lanmagan</li>
                </ul>
                
                <hr>
                <div class="d-grid gap-2">
                    <a href="{% url 'main:contact_form' %}" class="btn btn-info">
                        Contact Form
                    </a>
                    <a href="{% url 'main:search' %}" class="btn btn-outline-info">
                        Search Form
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-6">
        <div class="card border-success">
            <div class="card-header bg-success text-white">
                <h4><i class="fas fa-database"></i> ModelForm</h4>
            </div>
            <div class="card-body">
                <h6>Afzalliklari:</h6>
                <ul class="text-success">
                    <li>Kamroq kod</li>
                    <li>Model asosida validatsiya</li>
                    <li>Avtomatik save()</li>
                    <li>DRY prinsipi</li>
                </ul>
                
                <h6>Kamchiliklari:</h6>
                <ul class="text-danger">
                    <li>Cheklangan nazorat</li>
                    <li>Faqat bitta model</li>
                    <li>Murakkab logika qiyin</li>
                </ul>
                
                <hr>
                <div class="d-grid gap-2">
                    <a href="{% url 'main:contact_modelform' %}" class="btn btn-success">
                        Contact ModelForm
                    </a>
                    <a href="{% url 'main:news_create' %}" class="btn btn-outline-success">
                        News Create
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-bar"></i> Statistika</h5>
            </div>
            <div class="card-body">
                <div class="row text-center">
                    <div class="col-md-4">
                        <h3 class="text-primary">{{ contacts_count }}</h3>
                        <p>Jami kontaktlar (ModelForm)</p>
                    </div>
                    <div class="col-md-4">
                        <h3 class="text-info">∞</h3>
                        <p>Email jo'natildi (Form)</p>
                    </div>
                    <div class="col-md-4">
                        <h3 class="text-success">100%</h3>
                        <p>Muvaffaqiyat darajasi</p>
                    </div>
                </div>
                
                {% if recent_contacts %}
                <hr>
                <h6>So'nggi kontaktlar (ModelForm):</h6>
                <div class="list-group">
                    {% for contact in recent_contacts %}
                    <div class="list-group-item">
                        <div class="d-flex w-100 justify-content-between">
                            <h6 class="mb-1">{{ contact.name }}</h6>
                            <small>{{ contact.created_at|date:"d.m.Y H:i" }}</small>
                        </div>
                        <p class="mb-1">{{ contact.subject }}</p>
                        <small>{{ contact.email }}</small>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

## 7-bosqich: Migration va test

```bash
# Migration yaratish
python manage.py makemigrations
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Server ishga tushirish
python manage.py runserver
```

## Topshiriqlar

### 1. Asosiy topshiriq: Newsletter Form vs ModelForm
- Newsletter modeli yarating (email, subscribed_at, is_active)
- Oddiy Form va ModelForm yozib taqqoslang

### 2. Qo'shimcha: Feedback sistema
- Rating bilan feedback form yarating
- Har ikkala usulda ham amalga oshiring

### 3. Murakkab: User Registration
- User registration'ni Form va ModelForm bilan yozing
- Password confirmation validatsiyasi qo'shing

## Best Practices

1. **Form tanlash:**
   - DB'ga saqlanmaydi → Form
   - CRUD operatsiyalari → ModelForm

2. **Validatsiya:**
   - Form: clean() metodlari
   - ModelForm: Model + qo'shimcha clean()

3. **Xavfsizlik:**
   - Har doim CSRF token
   - Server-side validatsiya

4. **Performance:**
   - ModelForm'da select_related() ishlating
   - Faqat kerakli maydonlarni ko'rsating

## Xulosa

Bu amaliyotda siz Form va ModelForm o'rtasidagi farqlarni amaliy ko'rdingiz:

- **Form** - to'liq nazorat, murakkab logika
- **ModelForm** - kamroq kod, model bilan integratsiya

Keyingi darsda bosh sahifada yangiliklarni kategoriya bo'yicha ko'rsatishni o'rganamiz.