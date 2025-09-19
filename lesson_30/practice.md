# Amaliyot: Saytga yangilik qo'shish - CreateView

Bu amaliyotda siz o'zingizning yangiliklar saytingizga yangilik qo'shish funksiyasini bosqichma-bosqich yaratib chiqasiz.

## Boshlash oldidan tekshirish

Quyidagi fayllar mavjudligini tekshiring:
- `news/models.py` - News modeli
- `news/views.py` - mavjud view'lar
- `templates/` papkasi
- Virtual muhit faollashtirilgan

## 1-bosqich: Form yaratish

### 1.1. news/forms.py faylini yarating

```bash
touch news/forms.py
```

### 1.2. NewsForm klassini yozing

`news/forms.py` fayliga quyidagi kodni yozing:

```python
from django import forms
from .models import News, Category

class NewsForm(forms.ModelForm):
    """Yangilik yaratish formasi"""
    
    class Meta:
        model = News
        fields = ['title', 'slug', 'body', 'category', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Yangilik sarlavhasini kiriting',
                'required': True
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL uchun slug (ixtiyoriy)'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Yangilik matnini batafsil yozing...',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Sarlavha',
            'slug': 'URL manzili (Slug)',
            'body': 'Yangilik matni',
            'category': 'Kategoriya',
            'image': 'Rasm',
            'status': 'Holati',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Kategoriya tanlang"
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title) < 10:
            raise forms.ValidationError("Sarlavha kamida 10 ta belgidan iborat bo'lishi kerak")
        return title
    
    def clean_body(self):
        body = self.cleaned_data.get('body')
        if body and len(body) < 50:
            raise forms.ValidationError("Yangilik matni kamida 50 ta belgidan iborat bo'lishi kerak")
        return body
```

**Izoh**: Bu formada barcha kerakli validatsiyalar va CSS klasslar qo'shilgan.

## 2-bosqich: CreateView yaratish

### 2.1. news/views.py fayliga import qo'shish

Fayl boshiga quyidagi import'larni qo'shing:

```python
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import NewsForm
```

### 2.2. NewsCreateView klassini yaratish

`news/views.py` faylining oxiriga qo'shing:

```python
class NewsCreateView(LoginRequiredMixin, CreateView):
    """Yangi yangilik yaratish view'si"""
    model = News
    form_class = NewsForm
    template_name = 'news/news_create.html'
    login_url = '/admin/'  # Login sahifasi URL'i
    
    def form_valid(self, form):
        """Forma muvaffaqiyatli yuborilganda"""
        # Muallifni avtomatik o'rnatish
        form.instance.author = self.request.user
        
        # Muvaffaqiyat xabarini qo'shish
        messages.success(
            self.request, 
            f"'{form.instance.title}' yanglig muvaffaqiyatli yaratildi!"
        )
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Forma noto'g'ri bo'lganda"""
        messages.error(
            self.request, 
            "Formada xatolar mavjud. Iltimos, qaytadan tekshiring."
        )
        return super().form_invalid(form)
    
    def get_success_url(self):
        """Muvaffaqiyatli saqlangandan keyin qayerga yo'naltirish"""
        return reverse_lazy('news:detail', kwargs={'slug': self.object.slug})
```

**Muhim**: `LoginRequiredMixin` faqat login qilgan foydalanuvchilarga ruxsat beradi.

## 3-bosqich: Template yaratish

### 3.1. Template papkasini yarating

```bash
mkdir -p templates/news
```

### 3.2. news_create.html faylini yarating

`templates/news/news_create.html` fayliga quyidagi kodni yozing:

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Yangi yangilik qo'shish - {{ block.super }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-lg-8 mx-auto">
            <!-- Sahifa sarlavhasi -->
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2><i class="fas fa-plus-circle text-primary"></i> Yangi yangilik qo'shish</h2>
                <a href="{% url 'news:list' %}" class="btn btn-outline-secondary">
                    <i class="fas fa-arrow-left"></i> Orqaga
                </a>
            </div>
            
            <!-- Asosiy forma kartasi -->
            <div class="card shadow">
                <div class="card-header bg-primary text-white">
                    <h5 class="card-title mb-0">
                        <i class="fas fa-edit"></i> Yangilik ma'lumotlari
                    </h5>
                </div>
                <div class="card-body">
                    
                    <!-- Form xatolarini ko'rsatish -->
                    {% if form.non_field_errors %}
                        <div class="alert alert-danger alert-dismissible fade show" role="alert">
                            {{ form.non_field_errors }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endif %}
                    
                    <!-- Asosiy forma -->
                    <form method="post" enctype="multipart/form-data" novalidate>
                        {% csrf_token %}
                        
                        <div class="row">
                            <!-- Sarlavha -->
                            <div class="col-12 mb-3">
                                <label for="{{ form.title.id_for_label }}" class="form-label fw-bold">
                                    {{ form.title.label }} <span class="text-danger">*</span>
                                </label>
                                {{ form.title }}
                                {% if form.title.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ form.title.errors|first }}
                                    </div>
                                {% endif %}
                                <small class="form-text text-muted">Diqqat tortuvchi sarlavha yozing</small>
                            </div>
                            
                            <!-- Slug -->
                            <div class="col-md-6 mb-3">
                                <label for="{{ form.slug.id_for_label }}" class="form-label fw-bold">
                                    {{ form.slug.label }}
                                </label>
                                {{ form.slug }}
                                {% if form.slug.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ form.slug.errors|first }}
                                    </div>
                                {% endif %}
                                <small class="form-text text-muted">Bo'sh qoldirilsa, avtomatik yaratiladi</small>
                            </div>
                            
                            <!-- Kategoriya -->
                            <div class="col-md-6 mb-3">
                                <label for="{{ form.category.id_for_label }}" class="form-label fw-bold">
                                    {{ form.category.label }} <span class="text-danger">*</span>
                                </label>
                                {{ form.category }}
                                {% if form.category.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ form.category.errors|first }}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        
                        <div class="row">
                            <!-- Rasm -->
                            <div class="col-md-6 mb-3">
                                <label for="{{ form.image.id_for_label }}" class="form-label fw-bold">
                                    {{ form.image.label }}
                                </label>
                                {{ form.image }}
                                {% if form.image.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ form.image.errors|first }}
                                    </div>
                                {% endif %}
                                <small class="form-text text-muted">JPG, PNG formatida (maksimal 5MB)</small>
                            </div>
                            
                            <!-- Holati -->
                            <div class="col-md-6 mb-3">
                                <label for="{{ form.status.id_for_label }}" class="form-label fw-bold">
                                    {{ form.status.label }}
                                </label>
                                {{ form.status }}
                                {% if form.status.errors %}
                                    <div class="invalid-feedback d-block">
                                        {{ form.status.errors|first }}
                                    </div>
                                {% endif %}
                            </div>
                        </div>
                        
                        <!-- Yangilik matni -->
                        <div class="mb-4">
                            <label for="{{ form.body.id_for_label }}" class="form-label fw-bold">
                                {{ form.body.label }} <span class="text-danger">*</span>
                            </label>
                            {{ form.body }}
                            {% if form.body.errors %}
                                <div class="invalid-feedback d-block">
                                    {{ form.body.errors|first }}
                                </div>
                            {% endif %}
                            <small class="form-text text-muted">To'liq va batafsil ma'lumot yozing</small>
                        </div>
                        
                        <!-- Tugmalar -->
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'news:list' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Bekor qilish
                            </a>
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-save"></i> Saqlash
                            </button>
                        </div>
                    </form>
                </div>
            </div>
            
            <!-- Yordam ma'lumotlari -->
            <div class="card mt-3">
                <div class="card-body">
                    <h6 class="card-title"><i class="fas fa-info-circle text-info"></i> Maslahatlar:</h6>
                    <ul class="list-unstyled mb-0 small">
                        <li>• <span class="text-danger">*</span> belgilangan maydonlar majburiy</li>
                        <li>• Sarlavhani qisqa va tushunarli qiling</li>
                        <li>• Rasm yuklash ixtiyoriy, lekin tavsiya etiladi</li>
                        <li>• "Qoralama" holatida saqlangan yangiliklar ommaga ko'rinmaydi</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Sarlavhadan avtomatik slug yaratish
    document.getElementById('{{ form.title.id_for_label }}').addEventListener('input', function() {
        const title = this.value;
        const slug = title.toLowerCase()
                         .replace(/[^\w\s-]/g, '') // maxsus belgilarni olib tashlash
                         .replace(/\s+/g, '-')     // bo'shliqlarni - ga almashtirish
                         .trim();
        document.getElementById('{{ form.slug.id_for_label }}').value = slug;
    });
    
    // Fayl yuklash preview
    document.getElementById('{{ form.image.id_for_label }}').addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                // Preview yaratish (agar kerak bo'lsa)
                console.log('Fayl tanlandi:', file.name);
            };
            reader.readAsDataURL(file);
        }
    });
</script>
{% endblock %}
```

## 4-bosqich: URL sozlash

### 4.1. news/urls.py fayliga URL qo'shish

```python
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Mavjud URL'lar...
    path('create/', views.NewsCreateView.as_view(), name='create'),
    # ...
]
```

## 5-bosqich: Navigation va linklar qo'shish

### 5.1. base.html ga yangilik qo'shish linkini qo'shing

`templates/base.html` faylidagi navigation qismiga:

```html
<!-- Navbar ichida -->
<li class="nav-item">
    <a class="nav-link" href="{% url 'news:create' %}">
        <i class="fas fa-plus"></i> Yangilik qo'shish
    </a>
</li>
```

### 5.2. Yangiliklar list sahifasiga tugma qo'shish

`templates/news/news_list.html` fayliga sahifa boshida:

```html
<div class="d-flex justify-content-between align-items-center mb-4">
    <h2>Barcha yangiliklar</h2>
    <a href="{% url 'news:create' %}" class="btn btn-primary">
        <i class="fas fa-plus"></i> Yangi yangilik
    </a>
</div>
```

## 6-bosqich: Model'ni yaxshilash

### 6.1. news/models.py da slug avtomatik yaratish

`News` modelining `save` metodini qo'shing yoki yangilang:

```python
from django.utils.text import slugify
import uuid

class News(models.Model):
    # Mavjud fieldlar...
    
    def save(self, *args, **kwargs):
        """Saqlashdan oldin slug yaratish"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Takrorlanmaydigan slug yaratish
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Yangilik sahifasiga URL"""
        return reverse('news:detail', kwargs={'slug': self.slug})
```

## 7-bosqich: Testlash va debug

### 7.1. Django shell'da test qilish

```bash
python manage.py shell
```

```python
# Shell ichida
from news.forms import NewsForm
from news.models import Category

# Kategoriya yaratish (agar yo'q bo'lsa)
category = Category.objects.create(name='Test kategoriya')

# Forma test qilish
form_data = {
    'title': 'Test yangilik sarlavhasi',
    'body': 'Bu test uchun yozilgan yangilik matni. Kamida 50 ta belgi bo'lishi kerak.',
    'category': category.id,
    'status': 'PB'
}

form = NewsForm(data=form_data)
print("Forma valid:", form.is_valid())
if not form.is_valid():
    print("Xatolar:", form.errors)
```

### 7.2. Browser'da test qilish

1. Serverni ishga tushiring:
```bash
python manage.py runserver
```

2. Browserda quyidagi URL'ga o'ting:
```
http://127.0.0.1:8000/news/create/
```

3. Formani to'ldiring va test qiling

## 8-bosqich: Xatolarni tuzatish

### 8.1. Template topilmasa

**Xato**: `TemplateDoesNotExist at /news/create/`

**Yechim**:
```python
# settings.py da TEMPLATES bo'limini tekshiring
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Bu qator to'g'ri bo'lishi kerak
        # ...
    },
]
```

### 8.2. CSRF xatosi

**Xato**: `CSRF verification failed`

**Yechim**: Template'da `{% csrf_token %}` borligini tekshiring

### 8.3. Import xatosi

**Xato**: `ImportError: cannot import name 'NewsForm'`

**Yechim**: `news/forms.py` fayli yaratilganligini va import to'g'riligini tekshiring

### 8.4. Login talab qilinsa

**Xato**: Login sahifasiga yo'naltiriladi

**Yechim**: 
```python
# Admin yaratish
python manage.py createsuperuser

# Yoki LoginRequiredMixin'ni olib tashlash
class NewsCreateView(CreateView):  # LoginRequiredMixin'siz
    # ...
```

## 9-bosqich: Qo'shimcha funksiyalar

### 9.1. Ajax bilan yuborish

`templates/news/news_create.html` ga JavaScript qo'shing:

```html
{% block extra_js %}
{{ block.super }}
<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function(e) {
        // Loading indikatorini ko'rsatish
        const submitBtn = document.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saqlanmoqda...';
        
        // Form yuborilganda loading'ni qaytarish (Ajax bo'lmasa)
        setTimeout(function() {
            if (!form.dataset.ajaxSubmitted) {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }
        }, 5000);
    });
});
</script>
{% endblock %}
```

### 9.2. Rich text editor qo'shish

CKEditor qo'shish uchun:

```bash
pip install django-ckeditor
```

`settings.py` da:

```python
INSTALLED_APPS = [
    # ...
    'ckeditor',
    'ckeditor_uploader',
]

# CKEditor sozlamalari
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 300,
        'width': '100%',
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"
```

`news/forms.py` da:

```python
from ckeditor.widgets import CKEditorWidget

class NewsForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    # ...
```

### 9.3. Media fayllar sozlash

`settings.py` da:

```python
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

`urls.py` da (asosiy loyiha):

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 10-bosqich: Test yozish

### 10.1. news/tests.py fayliga testlar qo'shing

```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import News, Category
from .forms import NewsForm

class NewsCreateViewTest(TestCase):
    def setUp(self):
        """Test uchun dastlabki ma'lumotlar"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Test kategoriya')
        self.url = reverse('news:create')
    
    def test_create_view_get_without_login(self):
        """Login qilmagan foydalanuvchi uchun"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Login sahifasiga yo'naltiradi
    
    def test_create_view_get_with_login(self):
        """Login qilgan foydalanuvchi uchun GET so'rov"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Yangi yangilik qo\'shish')
    
    def test_create_news_post_valid_data(self):
        """To'g'ri ma'lumotlar bilan POST so'rov"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Test yangilik sarlavhasi uchun uzun matn',
            'body': 'Bu test uchun yozilgan yangilik matni. Kamida 50 ta belgi bo\'lishi kerak uchun uzunroq yozamiz.',
            'category': self.category.id,
            'status': 'PB'
        }
        response = self.client.post(self.url, data)
        
        # Yangilik yaratilganini tekshirish
        self.assertTrue(News.objects.filter(title=data['title']).exists())
        
        # Redirect qilinganini tekshirish
        news = News.objects.get(title=data['title'])
        self.assertRedirects(response, news.get_absolute_url())
    
    def test_create_news_post_invalid_data(self):
        """Noto'g'ri ma'lumotlar bilan POST so'rov"""
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Qisqa',  # Juda qisqa sarlavha
            'body': 'Qisqa matn',  # Juda qisqa matn
            'category': self.category.id,
            'status': 'PB'
        }
        response = self.client.post(self.url, data)
        
        # Form xatolari borligini tekshirish
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Formada xatolar mavjud')
        
        # Yangilik yaratilmaganini tekshirish
        self.assertFalse(News.objects.filter(title=data['title']).exists())

class NewsFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test kategoriya')
    
    def test_valid_form(self):
        """To'g'ri forma"""
        data = {
            'title': 'Test yangilik sarlavhasi uchun uzun matn',
            'body': 'Bu test uchun yozilgan yangilik matni. Kamida 50 ta belgi bo\'lishi kerak.',
            'category': self.category.id,
            'status': 'PB'
        }
        form = NewsForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_short_title(self):
        """Qisqa sarlavha bilan"""
        data = {
            'title': 'Qisqa',
            'body': 'Bu test uchun yozilgan yangilik matni. Kamida 50 ta belgi bo\'lishi kerak.',
            'category': self.category.id,
            'status': 'PB'
        }
        form = NewsForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
```

### 10.2. Testlarni ishga tushirish

```bash
# Barcha testlar
python manage.py test

# Faqat news app testlari
python manage.py test news

# Bitta test klassi
python manage.py test news.tests.NewsCreateViewTest

# Batafsil natijalar bilan
python manage.py test --verbosity=2
```

## 11-bosqich: Production uchun tayyorlash

### 11.1. Media fayllar uchun papka yaratish

```bash
mkdir media
mkdir media/news_images
```

### 11.2. settings.py da production sozlamalari

```python
# Media fayllar
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Fayl yuklash cheklovlari
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024  # 5MB
```

### 11.3. Nginx sozlamalari (production server uchun)

```nginx
# /etc/nginx/sites-available/your_site
server {
    # ...
    
    location /media/ {
        alias /path/to/your/project/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

## 12-bosqich: Debugging va logging

### 12.1. Debug uchun logging qo'shish

`news/views.py` da:

```python
import logging

logger = logging.getLogger(__name__)

class NewsCreateView(LoginRequiredMixin, CreateView):
    # ...
    
    def form_valid(self, form):
        logger.info(f"Yangi yangilik yaratildi: {form.instance.title}")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        logger.warning(f"Forma xatolari: {form.errors}")
        return super().form_invalid(form)
```

### 12.2. settings.py da logging sozlash

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'news': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## Yakuniy tekshirish

Bu amaliyotni tugallashdan oldin quyidagilarni tekshiring:

### ✅ Texnik tekshiruvlar:
- [ ] Forma to'g'ri ishlaydi
- [ ] Validation xatolari ko'rsatiladi  
- [ ] Slug avtomatik yaratiladi
- [ ] Login talab qilinadi
- [ ] Rasm yuklash ishlaydi
- [ ] URL'lar to'g'ri sozlangan

### ✅ Foydalanuvchi tajribasi:
- [ ] Responsive design
- [ ] Loading indikatorlar
- [ ] Tushunarli xato xabarlari
- [ ] Muvaffaqiyat xabarlari
- [ ] Intuitiv interfeys

### ✅ Xavfsizlik:
- [ ] CSRF himoyasi
- [ ] Foydalanuvchi autentifikatsiyasi
- [ ] Fayl yuklash xavfsizligi
- [ ] Ma'lumotlar validatsiyasi

### ✅ Testlar:
- [ ] Unit testlar yozilgan
- [ ] View testlari ishlaydi
- [ ] Form testlari o'tadi
- [ ] Edge case'lar tekshirilgan

## Maslahatlar

1. **Xatolarni bartaraf etish**: Har doim Django debug toolbar'dan foydalaning
2. **Ma'lumotlar bazasi**: Migration'larni unutmang
3. **Static fayllar**: `python manage.py collectstatic` ishlatishni unutmang
4. **Backup**: Muhim ma'lumotlarni zaxiralang
5. **Documentation**: Kod izohlarini yozing

Tabriklaymiz! 🎉 Siz Django CreateView yordamida yangilik qo'shish funksiyasini muvaffaqiyatli yaratdingiz. Keyingi darsda yangilikni tahrirlash (UpdateView) va o'chirish (DeleteView) bilan tanishasiz.