# Dars 27: Amaliyot - Yangiliklar sayti sahifalarini yaratish

## Amaliyot maqsadi
Bu amaliyotda siz nazariy qismda o'rgangan barcha bilimlaringizni qo'llab, to'liq funksional yangiliklar saytini yaratishingiz kerak. Har bir bosqichni diqqat bilan bajaring va kodni test qiling.

## Bosqichma-bosqich amaliyot

### 1-bosqich: Loyihani tayyorlash

#### 1.1 Virtual muhitni faollashtiring
```bash
# Virtual muhitni faollashtirish
pipenv shell

# Yoki venv ishlatgan bo'lsangiz:
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows
```

#### 1.2 Kerakli papkalarni yarating
```bash
# Template papkalarini yarating
mkdir -p templates/news
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images
```

### 2-bosqich: URL'larni sozlash

#### 2.1 Asosiy urls.py faylini yangilang
**mysite/urls.py** faylini quyidagicha o'zgartiring:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls', namespace='news')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### 2.2 News ilovasi uchun urls.py yarating
**news/urls.py** faylini yarating:

```python
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # TO DO: Bu yerga barcha URL'larni qo'shing
    # Masalan: path('', views.HomePageView.as_view(), name='home'),
]
```

**Vazifa:** Darsda ko'rsatilgan barcha URL'larni qo'shing.

### 3-bosqich: View'larni yaratish

#### 3.1 Kerakli import'larni qo'shing
**news/views.py** faylining boshiga:

```python
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.db.models import Q, Count
# TO DO: Qolgan import'larni qo'shing
```

#### 3.2 HomePageView yarating
```python
class HomePageView(TemplateView):
    template_name = 'news/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # TO DO: Context ma'lumotlarini qo'shing
        return context
```

**Vazifa:** 
- Kategoriyalar bo'yicha yangiliklarni oling
- So'nggi 5 ta yangiliklarni qo'shing
- Mashhur yangiliklarni qo'shing

#### 3.3 NewsListView yarating
```python
class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    # TO DO: Qolgan xususiyatlarni qo'shing
```

**Vazifa:**
- Sahifalashni qo'shing (6 ta yangilik)
- Filtrlash va saralashni amalga oshiring
- Context'ga kategoriyalarni qo'shing

#### 3.4 Qolgan view'larni yarating
**Vazifa:** Darsda ko'rsatilgan barcha view'larni yarating:
- NewsDetailView
- CategoryNewsView  
- SearchView
- ContactView
- AboutView

### 4-bosqich: Forms yaratish

#### 4.1 Forms.py faylini yarating
**news/forms.py:**

```python
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        # TO DO: Widget'larni qo'shing
```

**Vazifa:**
- Widget'larga CSS klasslarini qo'shing
- Validation'larni qo'shing
- SearchForm yarating

### 5-bosqich: Models yaratish/yangilash

#### 5.1 Contact modelini qo'shing
**news/models.py ga qo'shing:**

```python
class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    # TO DO: Qolgan fieldlarni qo'shing
    
    class Meta:
        # TO DO: Meta ma'lumotlarini qo'shing
        pass
        
    def __str__(self):
        # TO DO: __str__ metodini yozing
        pass
```

#### 5.2 Migration'larni yarating
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6-bosqich: Template'lar yaratish

#### 6.1 Base template yarating
**templates/base.html:**

```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <!-- TO DO: Meta teglarni qo'shing -->
    <title>{% block title %}Yangiliklar Sayti{% endblock %}</title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- TO DO: Static CSS faylini qo'shing -->
</head>
<body>
    <!-- TO DO: Navbar, main content va footer qo'shing -->
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### 6.2 Home sahifa template'ini yarating
**templates/news/home.html:**

```html
{% extends 'base.html' %}
{% load static %}

{% block title %}Bosh sahifa - Yangiliklar{% endblock %}

{% block content %}
<div class="container">
    <!-- TO DO: Hero section qo'shing -->
    
    <!-- TO DO: Kategoriyalar bo'yicha yangiliklarni ko'rsating -->
    
    <!-- TO DO: Sidebar qo'shing -->
</div>
{% endblock %}
```

**Vazifa:** Darsda ko'rsatilgan barcha template'larni yarating:
- news_list.html
- news_detail.html
- category_news.html
- search.html
- contact.html
- about.html

### 7-bosqich: Admin panelini sozlash

#### 7.1 Contact modelini admin'ga qo'shing
**news/admin.py:**

```python
from .models import Category, News, Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # TO DO: Admin sozlamalarini qo'shing
    pass
```

### 8-bosqich: Static fayllar qo'shish

#### 8.1 CSS faylini yarating
**static/css/style.css:**

```css
/* TO DO: Asosiy stillarni qo'shing */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* TO DO: Navbar stillarini qo'shing */

/* TO DO: Card stillarini qo'shing */

/* TO DO: Responsive stillarni qo'shing */
```

### 9-bosqich: Test qilish

#### 9.1 Development server'ni ishga tushiring
```bash
python manage.py runserver
```

#### 9.2 Sahifalarni test qiling
Quyidagi sahifalarni tekshiring:
- [ ] Bosh sahifa (`/`)
- [ ] Yangiliklar ro'yxati (`/news/`)
- [ ] Yangilik batafsil (`/news/slug/`)
- [ ] Kategoriya sahifasi (`/category/slug/`)
- [ ] Qidiruv (`/search/`)
- [ ] Kontakt (`/contact/`)
- [ ] About (`/about/`)

### 10-bosqich: Ma'lumot qo'shish

#### 10.1 Admin panelga kiring
```
http://127.0.0.1:8000/admin/
```

#### 10.2 Test ma'lumotlari qo'shing
- 3-4 ta kategoriya yarating
- Har kategoriyada 5-6 ta yangilik qo'shing
- Yangiliklarga rasm qo'shing

### 11-bosqich: Xatoliklarni tuzatish

#### 11.1 Keng uchraydigan xatoliklar:

**Xato 1:** `NoReverseMatch` - URL nom xatosi
```python
# Noto'g'ri:
path('news/<slug>/', views.NewsDetailView.as_view(), name='detail'),

# To'g'ri:
path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
```

**Xato 2:** Template topilmadi
```python
# views.py da template nomini tekshiring:
template_name = 'news/home.html'  # To'g'ri yo'l
```

**Xato 3:** Context xatosi
```python
# Context'da kalit nomlarini tekshiring:
context['news_list'] = news_list  # Template'da news_list ishlatilgan
```

### 12-bosqich: Qo'shimcha funksiyalar (Ixtiyoriy)

#### 12.1 Ko'rishlar sonini oshirish
NewsDetailView'da:
```python
def get_object(self, queryset=None):
    obj = super().get_object(queryset)
    # TO DO: Views fieldini oshiring
    return obj
```

#### 12.2 Qidiruv algoritmini yaxshilash
```python
def get_queryset(self):
    query = self.request.GET.get('q')
    if query:
        # TO DO: Title va body bo'yicha qidiring
        pass
```

#### 12.3 Pagination'ni sozlash
```python
class NewsListView(ListView):
    paginate_by = 6  # Har sahifada 6 ta
    # TO DO: Pagination'ni template'da ko'rsating
```

## Yakuniy tekshirish

### ✅ Tekshirish ro'yxati:

- [ ] Barcha URL'lar ishlaydi
- [ ] Template'lar to'g'ri ko'rsatiladi  
- [ ] Form'lar ishlaydi
- [ ] Ma'lumotlar to'g'ri ko'rsatiladi
- [ ] Responsive design ishlaydi
- [ ] Admin panel to'g'ri sozlangan
- [ ] Static fayllar yuklanyapti
- [ ] Xatolik sahifalari mavjud

### Maslahatlar:

1. **Dastlab oddiy variant yarating** - murakkab design'dan keyin
2. **Har bosqichni test qiling** - keyingi bosqichga o'tmaydi
3. **Xatoliklarni yozib boring** - keyinroq tuzatish uchun
4. **Code'ni izohlab yozing** - o'zingiz va boshqalar uchun
5. **Git'da saqlang** - har muhim o'zgarishni commit qiling

## Qo'shimcha vazifalar

### Oson daraja:
1. 404 va 500 xatolik sahifalarini yarating
2. Breadcrumb navigation qo'shing  
3. Social media share tugmalarini qo'shing

### O'rta daraja:
1. AJAX bilan ko'proq yangiliklar yuklash
2. Tag'lar funksiyasini qo'shing
3. Comment tizimini yarating

### Qiyin daraja:
1. Elasticsearch bilan qidiruvni yaxshilash
2. Redis bilan caching qo'shish
3. API yaratish (REST/GraphQL)

## Xulosa

Bu amaliyotni tamomlaganingizdan keyin sizda to'liq funksional yangiliklar sayti bo'ladi. Siz o'rgangan asosiy kontseptsiyalar:

### 📚 O'rgangan bilimlar:
- **URL routing** - sayt navigatsiyasini boshqarish
- **Class-based views** - kodni tashkil qilish
- **Template inheritance** - kodni qayta ishlatish
- **Form handling** - foydalanuvchi ma'lumotlarini qabul qilish
- **Database queries** - ma'lumotlar bilan ishlash
- **Pagination** - katta ro'yxatlarni bo'lish
- **Static files** - CSS, JS va rasm fayllar bilan ishlash

### 🎯 Keyingi maqsadlar:
1. **Performance optimization** - sayt tezligini oshirish
2. **User authentication** - foydalanuvchi tizimi
3. **Advanced features** - qo'shimcha funksiyalar
4. **Deployment** - saytni internetga joylashtirish

### 💡 Best Practice'lar:

#### 1. Code Organization
```python
# View'larni mantiqiy guruhlarga ajrating
class NewsViews:
    # Barcha news bilan bog'liq view'lar
    pass

class UserViews:
    # Foydalanuvchi view'lari
    pass
```

#### 2. Template Structure
```
templates/
├── base.html
├── includes/
│   ├── navbar.html
│   ├── footer.html
│   └── sidebar.html
└── news/
    ├── home.html
    ├── news_list.html
    └── news_detail.html
```

#### 3. URL Naming
```python
# Konsistent nomlardan foydalaning
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    # news_ prefix bilan
]
```

#### 4. Model Methods
```python
class News(models.Model):
    # ...
    
    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'slug': self.slug})
    
    def get_excerpt(self, word_count=20):
        return truncatewords(self.body, word_count)
    
    @property
    def reading_time(self):
        word_count = len(self.body.split())
        return max(1, word_count // 200)  # 200 so'z/daqiqa
```

#### 5. Security Best Practices
```python
# Form validation
def clean_title(self):
    title = self.cleaned_data.get('title')
    if len(title) < 5:
        raise ValidationError('Sarlavha juda qisqa')
    return title

# SQL injection prevention
# Har doim ORM ishlatiladi, raw SQL emas
queryset = News.objects.filter(title__icontains=search_term)
```

### 🔧 Troubleshooting Guide

#### Keng uchraydigan muammolar va yechimlari:

**1. Template topilmadi xatosi**
```python
# Xato:
template_name = 'home.html'

# To'g'ri:
template_name = 'news/home.html'

# settings.py da TEMPLATES sozlamalarini tekshiring
```

**2. Static fayllar yuklanmayapti**
```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# URL'larda:
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**3. Media fayllar ko'rinmayapti**
```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# urls.py
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**4. Pagination ishlamayapti**
```html
<!-- Template'da -->
{% if is_paginated %}
    <!-- Pagination kodlari -->
    {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
{% endif %}
```

**5. Form validation xatolari**
```python
# views.py
def form_invalid(self, form):
    messages.error(self.request, 'Formada xatoliklar mavjud!')
    return super().form_invalid(form)

# Template'da
{% if form.errors %}
    {% for error in form.errors %}
        <div class="alert alert-danger">{{ error }}</div>
    {% endfor %}
{% endif %}
```

### 📊 Performance Tips

#### 1. Database Optimization
```python
# Select related ishlatish
class NewsListView(ListView):
    def get_queryset(self):
        return News.objects.select_related('category', 'author')

# Prefetch related
class CategoryNewsView(ListView):
    def get_queryset(self):
        return News.objects.prefetch_related('tags')
```

#### 2. Caching
```python
# views.py
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@method_decorator(cache_page(60 * 15), name='get')  # 15 daqiqa
class HomePageView(TemplateView):
    # ...
```

#### 3. Image Optimization
```python
# models.py
def get_resized_image_url(self, width=300, height=200):
    if self.photo:
        # Pillow yordamida rasmni o'lchamini o'zgartirish
        pass
```

### 🚀 Deployment Checklist

#### Production'ga tayyorlanish:
- [ ] `DEBUG = False` qo'yish
- [ ] `ALLOWED_HOSTS` to'ldirish
- [ ] Database'ni production'ga o'tkazish
- [ ] Static fayllarni to'plash (`collectstatic`)
- [ ] HTTPS sozlash
- [ ] Security settings qo'shish
- [ ] Error logging sozlash

#### Environment Variables
```python
# .env fayl yarating
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=postgres://...

# settings.py
import os
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

### 📝 Code Review Checklist

Kodni tekshirish uchun:

**✅ Functionality**
- [ ] Barcha sahifalar to'g'ri ishlaydi
- [ ] Form'lar validatsiyani o'taydi  
- [ ] Database queries optimallashgan
- [ ] Error handling mavjud

**✅ Code Quality**
- [ ] DRY principle bajarilgan
- [ ] Functions va classlar aniq vazifaga ega
- [ ] Izohlar yozilgan
- [ ] Naming convention'lar bir xil

**✅ Security**
- [ ] CSRF protection faol
- [ ] SQL injection'dan himoyalangan
- [ ] User input validation qilingan
- [ ] Sensitive ma'lumotlar yashirilgan

**✅ Performance**
- [ ] Database query'lari optimallashgan
- [ ] Caching qo'llanilgan (kerak bo'lsa)
- [ ] Static fayllar minimized
- [ ] Images optimized

### 🎓 Keyingi darslar uchun tayyorgarlik

Bu loyiha tugagandan keyin siz quyidagilarni o'rganishingiz mumkin:

1. **Django REST Framework** - API yaratish
2. **Celery** - background task'lar
3. **Docker** - containerization
4. **Testing** - unit va integration testlar
5. **CI/CD** - automated deployment

### 📞 Yordam olish

Qiynalgan holatda:

1. **Django documentation** - https://docs.djangoproject.com/
2. **Stack Overflow** - konkret muammolar uchun
3. **Django community** - forum va chat'lar
4. **GitHub repositories** - o'xshash loyihalar
5. **Video tutorials** - vizual o'rganish uchun

### 🎉 Tabriklaymiz!

Siz Django bilan to'liq funksional web-sayt yaratdingiz! Bu katta yutuq va web development sohasidagi muhim qadam. Davom eting va yangi texnologiyalarni o'rganing!

---
