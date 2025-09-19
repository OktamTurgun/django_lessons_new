# Dars 30: Saytga yangilik qo'shish: CreateView

## Dars maqsadi
Bu darsda siz Django'ning Class-Based Views (CBV) dan foydalanib, saytga yangi yangilik qo'shish funksiyasini yaratishni o'rganasiz. CreateView yordamida foydalanuvchilar uchun yangilik yaratish sahifasini tuzamiz.

## Nazariy qism

### CreateView nima?
`CreateView` - Django'ning Class-Based View'laridan biri bo'lib, modelga yangi obyekt yaratish uchun maxsus ishlab chiqilgan. Bu view avtomatik ravishda:
- GET so'rovida - bo'sh forma ko'rsatadi
- POST so'rovida - formani validatsiya qiladi va saqlaydi
- Muvaffaqiyatli saqlangandan keyin belgilangan sahifaga yo'naltiradi

### CreateView'ning afzalliklari:
1. **Kod qisqartirilishi** - Oz kod bilan ko'p ishni bajaradi
2. **Avtomatik validatsiya** - Form tekshiruvini o'zi bajaradi
3. **CSRF himoyasi** - Avtomatik himoya
4. **Xatolarni boshqarish** - Xatolarni avtomatik ko'rsatadi

## Amaliy qism

### 1-bosqich: CreateView import qilish

Avval kerakli kutubxonalarni import qilamiz:

```python
# news/views.py
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import News
from .forms import NewsForm  # Buni keyinroq yaratamiz
```

**Izoh**: `reverse_lazy` - URL nomini kech hisoblash uchun ishlatiladi.

### 2-bosqich: NewsForm yaratish

Yangilik yaratish uchun forma kerak:

```python
# news/forms.py
from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    """Yangilik yaratish va tahrirlash formasi"""
    
    class Meta:
        model = News
        fields = ['title', 'slug', 'body', 'category', 'image', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Yangilik sarlavhasini kiriting'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL uchun slug (majburiy emas)'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Yangilik matnini kiriting'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def clean_title(self):
        """Sarlavhani validatsiya qilish"""
        title = self.cleaned_data['title']
        if len(title) < 10:
            raise forms.ValidationError("Sarlavha kamida 10 ta belgidan iborat bo'lishi kerak")
        return title
```

**Izoh**: `widgets` - formaning HTML ko'rinishini sozlash uchun ishlatiladi.

### 3-bosqich: CreateView yaratish

Endi asosiy CreateView'ni yaratamiz:

```python
# news/views.py
class NewsCreateView(CreateView):
    """Yangi yangilik yaratish view'si"""
    model = News
    form_class = NewsForm
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('news:list')
    
    def form_valid(self, form):
        """Forma to'g'ri to'ldirilganda ishlaydigan metod"""
        # Muallifni avtomatik o'rnatish (agar foydalanuvchi tizimga kirgan bo'lsa)
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
        
        # Muvaffaqiyat xabarini qo'shish
        messages.success(self.request, "Yangilik muvaffaqiyatli yaratildi!")
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Forma noto'g'ri to'ldirilganda ishlaydigan metod"""
        messages.error(self.request, "Formada xatolar mavjud. Iltimos, qaytadan tekshiring.")
        return super().form_invalid(form)
```

**Muhim tushuntirishlar**:
- `model` - qaysi model bilan ishlashni ko'rsatadi
- `form_class` - qaysi formadan foydalanishni belgilaydi
- `template_name` - qaysi template ishlatilishini ko'rsatadi
- `success_url` - muvaffaqiyatli saqlangandan keyin qayerga yo'naltirishni belgilaydi

### 4-bosqich: Template yaratish

Yangilik yaratish uchun template:

```html
<!-- templates/news/news_create.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Yangi yangilik qo'shish{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-md-8 mx-auto">
            <div class="card">
                <div class="card-header">
                    <h3><i class="fas fa-plus"></i> Yangi yangilik qo'shish</h3>
                </div>
                <div class="card-body">
                    <!-- Xatolar ko'rsatish -->
                    {% if form.errors %}
                        <div class="alert alert-danger">
                            <strong>Xatolar:</strong>
                            {{ form.errors }}
                        </div>
                    {% endif %}
                    
                    <!-- Forma -->
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        <div class="mb-3">
                            <label for="{{ form.title.id_for_label }}" class="form-label">Sarlavha *</label>
                            {{ form.title }}
                            {% if form.title.errors %}
                                <div class="text-danger">{{ form.title.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.slug.id_for_label }}" class="form-label">Slug</label>
                            {{ form.slug }}
                            <small class="form-text text-muted">Bo'sh qoldirilsa, avtomatik yaratiladi</small>
                            {% if form.slug.errors %}
                                <div class="text-danger">{{ form.slug.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.category.id_for_label }}" class="form-label">Kategoriya *</label>
                            {{ form.category }}
                            {% if form.category.errors %}
                                <div class="text-danger">{{ form.category.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.image.id_for_label }}" class="form-label">Rasm</label>
                            {{ form.image }}
                            {% if form.image.errors %}
                                <div class="text-danger">{{ form.image.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.body.id_for_label }}" class="form-label">Yangilik matni *</label>
                            {{ form.body }}
                            {% if form.body.errors %}
                                <div class="text-danger">{{ form.body.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="mb-3">
                            <label for="{{ form.status.id_for_label }}" class="form-label">Holati</label>
                            {{ form.status }}
                            {% if form.status.errors %}
                                <div class="text-danger">{{ form.status.errors }}</div>
                            {% endif %}
                        </div>
                        
                        <div class="d-flex justify-content-between">
                            <a href="{% url 'news:list' %}" class="btn btn-secondary">
                                <i class="fas fa-arrow-left"></i> Orqaga
                            </a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> Saqlash
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**Muhim elementlar**:
- `enctype="multipart/form-data"` - fayl yuklash uchun zarur
- `{% csrf_token %}` - xavfsizlik uchun
- Har bir maydon uchun xatolarni ko'rsatish

### 5-bosqich: URL sozlash

URL'larni sozlaymiz:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Boshqa URL'lar...
    path('create/', views.NewsCreateView.as_view(), name='create'),
    # ...
]
```

### 6-bosqich: Navigatsiyaga link qo'shish

Asosiy templatega yangilik yaratish linkini qo'shamiz:

```html
<!-- base.html ichida nav qismida -->
<li class="nav-item">
    <a class="nav-link" href="{% url 'news:create' %}">
        <i class="fas fa-plus"></i> Yangilik qo'shish
    </a>
</li>
```

### 7-bosqich: Model'ni yaxshilash

Model'da `save` metodini yaxshilaymiz:

```python
# news/models.py
from django.utils.text import slugify

class News(models.Model):
    # mavjud fieldlar...
    
    def save(self, *args, **kwargs):
        """Saqlashdan oldin slug yaratish"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

## Xatolarni bartaraf etish

### Keng uchraydigan xatolar:

1. **Template topilmaydi**
   ```
   Xato: TemplateDoesNotExist
   Yechim: Template yo'lini tekshiring
   ```

2. **CSRF xatosi**
   ```
   Xato: CSRF verification failed
   Yechim: {% csrf_token %} qo'shishni unutmang
   ```

3. **Forma validatsiya xatosi**
   ```
   Xato: Form is not valid
   Yechim: form.errors'ni tekshiring
   ```

## Qo'shimcha imkoniyatlar

### 1. Faqat login qilgan foydalanuvchilar uchun:

```python
from django.contrib.auth.mixins import LoginRequiredMixin

class NewsCreateView(LoginRequiredMixin, CreateView):
    # davomida...
    login_url = '/accounts/login/'  # login sahifasi URL'i
```

### 2. Faqat admin foydalanuvchilar uchun:

```python
from django.contrib.auth.mixins import UserPassesTestMixin

class NewsCreateView(UserPassesTestMixin, CreateView):
    # davomida...
    
    def test_func(self):
        return self.request.user.is_staff
```

### 3. Ajax bilan yuklash:

```python
from django.http import JsonResponse

class NewsCreateView(CreateView):
    # davomida...
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'Yangilik yaratildi'})
        return response
```

## Best Practices (Eng yaxshi amaliyotlar)

### 1. **Xavfsizlik**
- Har doim CSRF tokendan foydalaning
- Foydalanuvchi huquqlarini tekshiring
- Kiruvchi ma'lumotlarni validatsiya qiling

### 2. **Kod tashkil etish**
- Form'larni alohida fayllarda saqlang
- View'larni mantiqiy guruhlang
- Template'larni qayta ishlatishga mo'ljallang

### 3. **Foydalanuvchi tajribasi**
- Tushunarli xato xabarlarini bering
- Loading holatini ko'rsating
- Muvaffaqiyat xabarlarini qo'shing

### 4. **Optimizatsiya**
- Zarur fieldlarni belgilang
- Fayllarni to'g'ri nomlang
- Cache'dan foydalaning (kerak bo'lsa)

### 5. **Test yozish**
```python
# news/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import News

class NewsCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_create_news_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('news:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_news_post(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'title': 'Test yangilik sarlavhasi',
            'body': 'Test yangilik matni',
            'status': 'DF'
        }
        response = self.client.post(reverse('news:create'), data)
        self.assertEqual(response.status_code, 302)  # redirect
        self.assertTrue(News.objects.filter(title='Test yangilik sarlavhasi').exists())
```

## Maslahatlar

1. **Dastlabki ma'lumotlar**: Form'da dastlabki qiymatlarni o'rnating
2. **Fayl yuklash**: Fayl o'lchamini cheklang va formatini tekshiring
3. **SEO**: Meta ma'lumotlarni qo'shing
4. **Responsive**: Mobil qurilmalarda yaxshi ko'rinishini ta'minlang
5. **Backup**: Ma'lumotlarni zaxiralashni unutmang

Bu dars bilan siz Django'da CreateView yordamida yangilik qo'shish funksiyasini to'liq o'rgandingiz. Keyingi darsda yangilikni tahrirlash (UpdateView) va o'chirish (DeleteView) funksiyalarini o'rganasiz.