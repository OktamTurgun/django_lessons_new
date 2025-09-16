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

# Media fayllar uchun (development rejimida)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### 2.2 News ilovasi uchun urls.py yarating
**news/urls.py** faylini yarating va quyidagi kodlarni yozing:

```python
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Bosh sahifa
    path('', views.HomePageView.as_view(), name='home'),
    
    # Yangiliklar ro'yxati
    path('news/', views.NewsListView.as_view(), name='news_list'),
    
    # Yangilik batafsil
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    
    # Kategoriya bo'yicha yangiliklar
    path('category/<slug:category_slug>/', views.CategoryNewsView.as_view(), name='category_news'),
    
    # Qidiruv
    path('search/', views.SearchView.as_view(), name='search'),
    
    # Kontakt sahifasi
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # About sahifasi
    path('about/', views.AboutView.as_view(), name='about'),
]
```

### 3-bosqich: View'larni yaratish

#### 3.1 Kerakli import'larni qo'shing
**news/views.py** faylining boshiga quyidagi import'larni qo'shing:

```python
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import News, Category
from .forms import ContactForm
```

#### 3.2 HomePageView yarating
```python
class HomePageView(TemplateView):
    """Bosh sahifa view'i"""
    template_name = 'news/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Kategoriyalar bo'yicha yangiliklar
        categories = Category.objects.all()
        news_by_category = {}
        
        for category in categories[:4]:  # Faqat 4 ta kategoriya
            news_list = News.published.filter(category=category)[:3]  # Har kategoriyadan 3 ta
            if news_list:
                news_by_category[category] = news_list
        
        # So'nggi yangiliklar
        latest_news = News.published.order_by('-publish_time')[:5]
        
        # Mashhur yangiliklar (ko'p ko'rilgan)
        popular_news = News.published.order_by('-views')[:5]
        
        context.update({
            'news_by_category': news_by_category,
            'latest_news': latest_news,
            'popular_news': popular_news,
            'categories': categories,
        })
        
        return context
```

#### 3.3 NewsListView yarating
```python
class NewsListView(ListView):
    """Barcha yangiliklar sahifasi"""
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 6  # Har sahifada 6 ta yangilik
    
    def get_queryset(self):
        queryset = News.published.select_related('category', 'author')
        
        # Kategoriya bo'yicha filtrlash
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        
        # Saralash
        sort_by = self.request.GET.get('sort', '-publish_time')
        queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
```

#### 3.4 NewsDetailView yarating
```python
class NewsDetailView(DetailView):
    """Yangilik batafsil sahifasi"""
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_queryset(self):
        return News.published.select_related('category', 'author')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Ko'rishlar sonini oshirish
        obj.views += 1
        obj.save(update_fields=['views'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news = self.object
        
        # O'xshash yangiliklar (bir xil kategoriyadan)
        related_news = News.published.filter(
            category=news.category
        ).exclude(id=news.id)[:4]
        
        context['related_news'] = related_news
        return context
```

#### 3.5 CategoryNewsView yarating
```python
class CategoryNewsView(ListView):
    """Kategoriya bo'yicha yangiliklar"""
    model = News
    template_name = 'news/category_news.html'
    context_object_name = 'news_list'
    paginate_by = 8
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return News.published.filter(category=self.category).select_related('author')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['news_count'] = self.get_queryset().count()
        return context
```

#### 3.6 SearchView yarating
```python
class SearchView(ListView):
    """Qidiruv sahifasi"""
    model = News
    template_name = 'news/search.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return News.published.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            ).select_related('category', 'author')
        return News.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['total_results'] = self.get_queryset().count()
        return context
```

#### 3.7 ContactView yarating
```python
class ContactView(FormView):
    """Kontakt sahifasi"""
    template_name = 'news/contact.html'
    form_class = ContactForm
    success_url = '/contact/'
    
    def form_valid(self, form):
        # Formani saqlash
        form.save()
        messages.success(self.request, 'Xabaringiz muvaffaqiyatli yuborildi!')
        return super().form_valid(form)
```

#### 3.8 AboutView yarating
```python
class AboutView(TemplateView):
    """Biz haqimizda sahifasi"""
    template_name = 'news/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Statistika ma'lumotlari
        context['total_news'] = News.published.count()
        context['total_categories'] = Category.objects.count()
        return context
```

### 4-bosqich: Forms yaratish

#### 4.1 Forms.py faylini yarating
**news/forms.py:**

```python
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    """Kontakt formasi"""
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ismingizni kiriting'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email manzilingizni kiriting'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Xabar mavzusi'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Xabaringizni yozing'
            }),
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('Ism kamida 2 ta belgidan iborat bo\'lishi kerak.')
        return name
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Xabar kamida 10 ta belgidan iborat bo\'lishi kerak.')
        return message

class SearchForm(forms.Form):
    """Qidiruv formasi"""
    q = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Qidirish...',
            'required': True,
        })
    )
```

### 5-bosqich: Models yaratish/yangilash

#### 5.1 Contact modelini qo'shing
**news/models.py ga quyidagi Contact modelini qo'shing:**

```python
class Contact(models.Model):
    """Kontakt formasi modeli"""
    name = models.CharField(max_length=100, verbose_name="Ism")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Mavzu")
    message = models.TextField(verbose_name="Xabar")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    
    class Meta:
        verbose_name = "Kontakt xabari"
        verbose_name_plural = "Kontakt xabarlari"
        ordering = ['-created_time']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
```

#### 5.2 Migration'larni yarating va qo'llang
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
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar Sayti{% endblock %}</title>
    {% load static %}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <!-- Header -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'news:home' %}">Yangiliklar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:home' %}">Bosh sahifa</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:news_list' %}">Yangiliklar</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:about' %}">Biz haqimizda</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'news:contact' %}">Aloqa</a>
                    </li>
                </ul>
                <form class="d-flex" method="get" action="{% url 'news:search' %}">
                    <input class="form-control me-2" type="search" name="q" 
                           placeholder="Qidirish..." value="{{ request.GET.q }}">
                    <button class="btn btn-outline-light" type="submit">Qidirish</button>
                </form>
            </div>
        </div>
    </nav>

    <!-- Messages -->
    {% if messages %}
    <div class="container mt-3">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Main Content -->
    <main class="py-4">
        {% block content %}
        {% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <h5>Yangiliklar Sayti</h5>
                    <p>Eng so'nggi va dolzarb yangiliklar bilan tanishing.</p>
                </div>
                <div class="col-md-6">
                    <h5>Kategoriyalar</h5>
                    <ul class="list-unstyled">
                        {% for category in categories %}
                        <li><a href="{% url 'news:category_news' category.slug %}" class="text-light">{{ category.name }}</a></li>
                        {% endfor %}
                    </ul>
                </div>
            </div>
            <hr>
            <div class="text-center">
                <p>&copy; 2024 Yangiliklar Sayti. Barcha huquqlar himoyalangan.</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

#### 6.2 Home sahifa template'ini yarating
**templates/news/home.html:** (Lesson.md dagi to'liq kodni oling)

#### 6.3 Qolgan template'larni yarating
Lesson.md dagi kodni ishlatib quyidagi template'larni yarating:
- **templates/news/news_list.html**
- **templates/news/news_detail.html** 
- **templates/news/category_news.html**
- **templates/news/search.html**
- **templates/news/contact.html**
- **templates/news/about.html**

### 7-bosqich: Admin panelini sozlash

#### 7.1 Contact modelini admin'ga qo'shing
**news/admin.py ga qo'shing:**

```python
from django.contrib import admin
from .models import Category, News, Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_time']
    list_filter = ['created_time']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['created_time']
    
    def has_add_permission(self, request):
        return False  # Admin paneldan qo'shishni cheklash
```

### 8-bosqich: Static fayllar qo'shish

#### 8.1 CSS faylini yarating
**static/css/style.css:** (Lesson.md dagi to'liq CSS kodini oling)

### 9-bosqich: Test qilish

#### 9.1 Development server'ni ishga tushiring
```bash
python manage.py runserver
```

#### 9.2 Sahifalarni test qiling
Quyidagi sahifalarni tekshiring:
- [ ] Bosh sahifa (`http://127.0.0.1:8000/`)
- [ ] Yangiliklar ro'yxati (`http://127.0.0.1:8000/news/`)
- [ ] Qidiruv (`http://127.0.0.1:8000/search/`)
- [ ] Kontakt (`http://127.0.0.1:8000/contact/`)
- [ ] About (`http://127.0.0.1:8000/about/`)

### 10-bosqich: Ma'lumot qo'shish

#### 10.1 Admin panelga kiring
```
http://127.0.0.1:8000/admin/
```

#### 10.2 Test ma'lumotlari qo'shing
- 3-4 ta kategoriya yarating
- Har kategoriyada 5-6 ta yangilik qo'shing
- Yangiliklarga rasm qo'shing
- Slug fieldlarni to'ldiring

### 11-bosqich: Xatoliklarni tuzatish

#### 11.1 Keng uchraydigan xatoliklar:

**Xato 1:** `NoReverseMatch` - URL nom xatosi
```python
# Template'da to'g'ri URL nomlarini ishlatganingizni tekshiring
{% url 'news:news_detail' news.slug %}
```

**Xato 2:** Template topilmadi
```python
# views.py da template yo'llarini tekshiring:
template_name = 'news/home.html'  # templates papka ichida news/home.html
```

**Xato 3:** Static fayllar yuklanmayapti
```python
# settings.py da STATIC_URL va STATICFILES_DIRS to'g'ri sozlanganini tekshiring
```

**Xato 4:** Context variable topilmadi
```html
<!-- Template'da context variable nomlarini to'g'ri ishlatganingizni tekshiring -->
{{ news_list }} <!-- views.py da context_object_name bilan mos kelishi kerak -->
```

## Yakuniy tekshirish

### ✅ Tekshirish ro'yxati:

- [ ] Barcha URL'lar ishlaydi va to'g'ri sahifalarga olib boradi
- [ ] Template'lar to'g'ri ko'rsatiladi  
- [ ] Kontakt formasi ishlaydi va ma'lumotlar saqlanadi
- [ ] Qidiruv funksiyasi ishlaydi
- [ ] Pagination ko'rsatiladi (6+ yangilik bo'lsa)
- [ ] Ma'lumotlar to'g'ri ko'rsatiladi (sarlavha, matn, sana)
- [ ] Responsive design ishlaydi (mobil qurilmalarda test qiling)
- [ ] Admin panel to'g'ri sozlangan
- [ ] Static fayllar (CSS) yuklanyapti
- [ ] Rasm fayllar ko'rsatiladi

### Maslahatlar:

1. **Har bosqichni ketma-ket bajaring** - bir bosqichni tugatmasdan keyingisiga o'tmang
2. **Xatoliklarni darhol tuzating** - kichik xatolar katta muammolarga aylanishi mumkin  
3. **Browser console'ni tekshiring** - JavaScript xatolari bo'lishi mumkin
4. **Django error sahifalarini o'qing** - aniq xato ma'lumotlari beradi
5. **Code'ni izohlab yozing** - keyinroq tushunish uchun

## Qo'shimcha vazifalar (Ixtiyoriy)

### Oson daraja:
1. 404 va 500 xatolik sahifalarini yarating
2. Breadcrumb navigation qo'shing  
3. Footer'ga social media linklar qo'shing

### O'rta daraja:
1. Ko'rishlar soni (views count) funksiyasini qo'shing
2. O'xshash yangiliklar ko'rsatish
3. Kategoriya bo'yicha yangiliklar soni

### Qiyin daraja:
1. AJAX bilan ko'proq yangiliklar yuklash
2. Tag'lar funksiyasini qo'shing
3. Comment tizimini yarating

## Yakuniy loyiha strukturasi

```
mysite/
├── mysite/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── news/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── templates/
│   ├── base.html
│   └── news/
│       ├── home.html
│       ├── news_list.html
│       ├── news_detail.html
│       ├── category_news.html
│       ├── search.html
│       ├── contact.html
│       └── about.html
├── static/
│   └── css/
│       └── style.css
├── media/
│   └── news/
└── manage.py
```

## Debug maslahatlar

**1. Server ishlamayapti:**
```bash
# Virtual environment faollashtirilganini tekshiring
# Kerakli paketlar o'rnatilganini tekshiring
pip list
```

**2. Template topilmayapti:**
```python
# settings.py da TEMPLATES sozlamalarini tekshiring
'DIRS': [BASE_DIR / 'templates'],
```

**3. Static fayllar ishlamayapti:**
```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# urls.py (development uchun)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**4. Ma'lumotlar ko'rinmayapti:**
```python
# Admin paneldan ma'lumotlar mavjudligini tekshiring
# Models da published manager to'g'ri ishlayotganini tekshiring
```

Bu amaliyotni muvaffaqiyatli tugatganingizdan keyin sizda to'liq funksional yangiliklar sayti bo'ladi!