# Dars 26: URLni slug'ga o'zgartirish va get_absolute_url

## Dars maqsadi
Ushbu darsda siz quyidagi mavzularni o'rganasiz:
- Slug nima va nima uchun kerak
- URL'larni slug bilan SEO-friendly qilish
- `get_absolute_url()` metodining ahamiyati
- Slug yaratish va ishlatishning eng yaxshi usullari

## Slug nima?

**Slug** - bu URL'da ishlatilish uchun mo'ljallangan matn bo'lagi bo'lib, odatda faqat harflar, raqamlar va chiziqchalardan iborat bo'ladi.

### Slug'ning afzalliklari:
- **SEO-friendly**: Qidiruv tizimlari uchun tushunarli
- **Foydalanuvchi uchun qulay**: URL manzili o'qilishi oson
- **Xavfsiz**: Maxsus belgilar yo'q

### Misollar:
```
Yomon URL: /news/15/
Yaxshi URL: /news/django-bilan-web-sayt-yaratish/
```

## Model'ga Slug qo'shish

Avval `models.py` faylimizga slug maydonini qo'shamiz:

```python
# models.py
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class News(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    body = models.TextField()
    photo = models.ImageField(upload_to='news/photos/')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        # Agar slug bo'sh bo'lsa, title'dan avtomatik yaratamiz
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
```

### Kodni tushuntirish:

1. **slug maydon**: `SlugField` maxsus maydon turi
   - `max_length=250`: Maksimal uzunlik
   - `unique=True`: Har bir slug noyob bo'lishi kerak
   - `blank=True`: Admin panelda bo'sh qoldirilishi mumkin

2. **save() metodi**: Obyekt saqlanayotganda ishga tushadi
   - `slugify()` funksiyasi matnni slug formatiga o'zgartiradi
   - Faqat slug bo'sh bo'lgandagina yaratadi

3. **get_absolute_url()** metodi: Obyektning to'liq URL manzilini qaytaradi

## URLs.py faylini yangilash

URL pattern'larini slug bilan ishlash uchun o'zgartiramiz:

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    # Eski variant: path('<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    # Yangi variant:
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
]
```

### URL pattern tushuntirish:
- `<slug:slug>`: URL'dan slug qiymatini oladi
- `slug` - parameter nomi (view'da ishlatiladi)
- `slug:` - Django'ga bu slug ekanligini bildiradi

## Views.py faylini yangilash

DetailView'ni slug bilan ishlash uchun sozlaymiz:

```python
# views.py
from django.views.generic import ListView, DetailView
from .models import News

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    
    def get_queryset(self):
        return News.objects.filter(status=True)

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    # Slug bo'yicha qidirish uchun
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
```

### View parametrlari tushuntirish:
- `slug_field`: Model'dagi slug maydon nomi
- `slug_url_kwarg`: URL'dan keladigan parametr nomi

## Template'larda foydalanish

Template fayllarida slug'li URL'larni ishlatamiz:

```html
<!-- news/news_list.html -->
<div class="news-list">
    {% for news in news_list %}
        <article class="news-item">
            <h2>
                <a href="{{ news.get_absolute_url }}">{{ news.title }}</a>
            </h2>
            <p class="excerpt">{{ news.body|truncatewords:20 }}</p>
            <div class="meta">
                <time>{{ news.created_time|date:"d.m.Y" }}</time>
            </div>
        </article>
    {% endfor %}
</div>
```

```html
<!-- news/news_detail.html -->
<article class="news-detail">
    <h1>{{ news.title }}</h1>
    <div class="meta">
        <time>{{ news.created_time|date:"d F Y" }}</time>
    </div>
    <div class="content">
        {{ news.body|linebreaks }}
    </div>
    <a href="{% url 'news:news_list' %}" class="back-link">← Barcha yangiliklar</a>
</article>
```

## Mavjud ma'lumotlarga slug qo'shish

Agar loyihangizda allaqachon ma'lumotlar bor bo'lsa, ularga slug qo'shish uchun management command yaratamiz:

```python
# management/commands/add_slugs.py
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from news.models import News

class Command(BaseCommand):
    help = 'Add slugs to existing news'
    
    def handle(self, *args, **options):
        news_list = News.objects.filter(slug='')
        
        for news in news_list:
            news.slug = slugify(news.title)
            news.save()
            self.stdout.write(f'Slug qo\'shildi: {news.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'{news_list.count()} ta yangilikka slug qo\'shildi')
        )
```

Komandani ishga tushirish:
```bash
python manage.py add_slugs
```

## Migration yaratish va ishga tushirish

Model o'zgargach, migration yaratamiz:

```bash
python manage.py makemigrations
python manage.py migrate
```

## get_absolute_url() metodining afzalliklari

### 1. Markazlashtirish
URL yaratish mantiq bir joyda to'plangan:
```python
# Yaxshi usul
<a href="{{ news.get_absolute_url }}">{{ news.title }}</a>

# Yomon usul
<a href="{% url 'news:news_detail' slug=news.slug %}">{{ news.title }}</a>
```

### 2. Django Admin panelida "View on site" tugmasi
```python
class News(models.Model):
    # ...
    
    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'slug': self.slug})
```

### 3. Redirectlarda foydalanish
```python
# views.py
from django.shortcuts import redirect

def some_view(request):
    news = News.objects.get(id=1)
    return redirect(news)  # get_absolute_url() ni ishlatadi
```

## Slug bilan ishlashning Best Practices

### 1. Noyoblik ta'minlash
```python
from django.utils.text import slugify
import uuid

def save(self, *args, **kwargs):
    if not self.slug:
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        
        # Agar bunday slug mavjud bo'lsa, raqam qo'shamiz
        while News.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            
        self.slug = slug
    super().save(*args, **kwargs)
```

### 2. Kirill harflarini to'g'ri qayta ishlash
```python
from django.utils.text import slugify
from transliterate import translit

def save(self, *args, **kwargs):
    if not self.slug:
        # Kirill harflarini lotin harflariga o'giramiz
        transliterated = translit(self.title, 'ru', reversed=True)
        self.slug = slugify(transliterated)
    super().save(*args, **kwargs)
```

### 3. Slug uzunligini cheklash
```python
def save(self, *args, **kwargs):
    if not self.slug:
        base_slug = slugify(self.title)[:50]  # 50 ta belgigacha
        self.slug = base_slug
    super().save(*args, **kwargs)
```

## Xatolarni hal qilish

### 1. "DoesNotExist" xatosi
```python
# views.py
from django.shortcuts import get_object_or_404

class NewsDetailView(DetailView):
    def get_object(self):
        return get_object_or_404(
            News, 
            slug=self.kwargs['slug'], 
            status=True
        )
```

### 2. Slug bo'sh bo'lgan holat
```python
def get_absolute_url(self):
    if self.slug:
        return reverse('news:news_detail', kwargs={'slug': self.slug})
    return reverse('news:news_detail', kwargs={'pk': self.pk})
```

## Dars yakuniy natijasi

Ushbu darsdan so'ng sizda:
- **SEO-friendly** URL'lar bor bo'ladi
- Foydalanuvchilar uchun **tushunarli** manzillar
- **get_absolute_url()** metodini to'g'ri ishlatish ko'nikmasi
- Slug bilan ishlashning eng yaxshi usullari

**Keyingi dars:**

27-darsda biz Yangiliklar sayti sahifasini yaratishni o'rganamaiz.