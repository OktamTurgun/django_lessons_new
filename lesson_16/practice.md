# 16-dars: News list va detail page - Amaliyot

## Amaliyot maqsadi
Ushbu amaliyotda siz nazariy bilimlarni qo'llab, to'liq ishlaydigan yangiliklar ro'yxati va detail sahifalarini yaratasiz.

## Boshlash uchun tayyorgarlik

### 1-qadam: Loyihangizni tekshiring

```bash
# Virtual muhitni faollashtiring
pipenv shell

# Server ishlab turganligini tekshiring
python manage.py runserver
```

Agar xatolik bo'lsa, avvalgi darslarni qarab chiqing.

### 2-qadam: Ma'lumotlar bazasida yangiliklar bor-yo'qligini tekshiring

```bash
python manage.py shell
```

```python
from news.models import News, Category
from django.contrib.auth.models import User

# Yangiliklar sonini tekshirish
print(f"Yangiliklar soni: {News.objects.count()}")
print(f"Kategoriyalar soni: {Category.objects.count()}")

# Agar ma'lumot yo'q bo'lsa, qo'shamiz
if News.objects.count() == 0:
    # Kategoriya yaratish
    tech_cat = Category.objects.create(name="Texnologiya", slug="tech")
    sport_cat = Category.objects.create(name="Sport", slug="sport")
    
    # User yaratish
    user = User.objects.create_user('admin', 'admin@example.com', 'admin123')
    
    # Yangiliklar yaratish
    News.objects.create(
        title="Yangi iPhone chiqa boshladi",
        slug="yangi-iphone",
        content="Apple kompaniyasi yangi iPhone modelini taqdim etdi...",
        author=user,
        category=tech_cat
    )
    
    News.objects.create(
        title="O'zbekiston futbol jamoasi g'alaba qozondi",
        slug="uzbekiston-futbol",
        content="Milliy jamoamiz kuchli raqibni mag'lub etdi...",
        author=user,
        category=sport_cat
    )

exit()
```

## Amaliy ishlar

### Amaliy ish 1: Asosiy Views yaratish

**Vazifa:** news/views.py faylini yarating va asosiy views funksiyalarini yozing.

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import News, Category

def news_list(request):
    """
    TODO: Bu yerda siz o'zingiz kod yozishingiz kerak
    
    Nima qilish kerak:
    1. Barcha is_published=True yangiliklar olish
    2. Kategoriya filtri qo'shish
    3. Pagination qo'shish (har sahifada 6 ta)
    4. Template'ga context yuborish
    """
    pass

def news_detail(request, slug):
    """
    TODO: Bu yerda siz o'zingiz kod yozishingiz kerak
    
    Nima qilish kerak:
    1. Slug bo'yicha yangilik topish
    2. 404 xatolik handle qilish
    3. O'xshash yangiliklar topish
    4. Template'ga context yuborish
    """
    pass
```

**Yechim:**

<details>
<summary>Yechimni ko'rish</summary>

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import News, Category

def news_list(request):
    # 1. Barcha nashr etilgan yangiliklarni olamiz
    news_list = News.objects.filter(is_published=True).select_related('author', 'category')
    
    # 2. Kategoriya bo'yicha filtrlash
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        news_list = news_list.filter(category=category)
    
    # 3. Sahifalash
    paginator = Paginator(news_list, 6)
    page_number = request.GET.get('page')
    news = paginator.get_page(page_number)
    
    # 4. Kategoriyalar ro'yxati
    categories = Category.objects.all()
    
    context = {
        'news': news,
        'categories': categories,
        'current_category': category_slug,
    }
    return render(request, 'news/list.html', context)

def news_detail(request, slug):
    # 1. Yangilikni topish
    news = get_object_or_404(
        News.objects.select_related('author', 'category'),
        slug=slug, 
        is_published=True
    )
    
    # 2. O'xshash yangiliklar
    related_news = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id)[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    return render(request, 'news/detail.html', context)
```

</details>

### Amaliy ish 2: URLs yaratish

**Vazifa:** news/urls.py fayl yarating va URL pattern'larni belgilang.

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),
    path('<slug:slug>/', views.news_detail, name='detail'),
]
```

</details>

### Amaliy ish 3: Base template yaratish

**Vazifa:** templates/base.html fayl yarating.

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <!-- TODO: Head qismini to'ldiring -->
</head>
<body>
    <!-- TODO: Navigation va content qismini yozing -->
</body>
</html>
```

**Yechim:**

<details>
<summary>Yechimni ko'rish</summary>

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar sayti{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="{% url 'news:list' %}">📰 Yangiliklar</a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <div class="navbar-nav ms-auto">
                    <a class="nav-link" href="{% url 'news:list' %}">Bosh sahifa</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="container mt-4">
        {% block content %}
        {% endblock %}
    </main>

    <footer class="bg-light mt-5 py-4">
        <div class="container text-center">
            <p>&copy; 2025 Yangiliklar sayti. Barcha huquqlar himoyalangan.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

</details>

### Amaliy ish 4: News List template

**Vazifa:** news/templates/news/list.html fayl yarating.

**Talab:** 
- Kategoriyalar sidebar
- Qidiruv funksiyasi
- Yangiliklar grid layout
- Pagination

```html
<!-- news/templates/news/list.html -->
{% extends 'base.html' %}

{% block title %}Yangiliklar ro'yxati{% endblock %}

{% block content %}
<!-- TODO: Sahifa tarkibini yozing -->
{% endblock %}
```

**Yechim:**

<details>
<summary>Yechimni ko'rish</summary>

```html
<!-- news/templates/news/list.html -->
{% extends 'base.html' %}

{% block title %}Yangiliklar ro'yxati{% endblock %}

{% block content %}
<div class="row">
    <!-- Sidebar - Kategoriyalar -->
    <div class="col-lg-3 col-md-4 mb-4">
        <!-- Qidiruv -->
        <div class="card mb-3">
            <div class="card-header">
                <h6 class="mb-0">🔍 Qidiruv</h6>
            </div>
            <div class="card-body">
                <form method="GET">
                    <div class="input-group">
                        <input type="text" name="q" class="form-control form-control-sm" 
                               placeholder="Qidiring..." 
                               value="{{ search_query }}">
                        {% if current_category %}
                        <input type="hidden" name="category" value="{{ current_category }}">
                        {% endif %}
                        <button type="submit" class="btn btn-primary btn-sm">
                            Qidiruv
                        </button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- Kategoriyalar -->
        <div class="card">
            <div class="card-header">
                <h6 class="mb-0">📂 Kategoriyalar</h6>
            </div>
            <div class="card-body">
                <div class="d-grid gap-2">
                    <a href="{% url 'news:list' %}" 
                       class="btn btn-outline-primary btn-sm {% if not current_category %}active{% endif %}">
                        🏠 Barchasi
                    </a>
                    
                    {% for category in categories %}
                    <a href="{% url 'news:list' %}?category={{ category.slug }}" 
                       class="btn btn-outline-primary btn-sm {% if current_category == category.slug %}active{% endif %}">
                        {{ category.name }}
                    </a>
                    {% endfor %}
                </div>
            </div>
        </div>
    </div>
    
    <!-- Asosiy mazmun -->
    <div class="col-lg-9 col-md-8">
        <!-- Header -->
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>
                {% if current_category %}
                    {% for category in categories %}
                        {% if category.slug == current_category %}
                            {{ category.name }} yangiliklari
                        {% endif %}
                    {% endfor %}
                {% elif search_query %}
                    "{{ search_query }}" bo'yicha qidiruv
                {% else %}
                    So'nggi yangiliklar
                {% endif %}
            </h2>
            
            {% if news %}
            <small class="text-muted">
                Jami: {{ news.paginator.count }} ta yangilik
            </small>
            {% endif %}
        </div>
        
        <!-- Yangiliklar ro'yxati -->
        {% if news %}
        <div class="row">
            {% for item in news %}
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card h-100 shadow-sm">
                    {% if item.image %}
                    <div style="height: 200px; overflow: hidden;">
                        <img src="{{ item.image.url }}" class="card-img-top w-100 h-100" 
                             alt="{{ item.title }}" style="object-fit: cover;">
                    </div>
                    {% else %}
                    <div class="bg-light d-flex align-items-center justify-content-center" style="height: 200px;">
                        <span class="text-muted">📰 Rasm yo'q</span>
                    </div>
                    {% endif %}
                    
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">{{ item.title }}</h5>
                        <p class="card-text flex-grow-1">{{ item.content|truncatewords:15 }}</p>
                        
                        <div class="mt-auto">
                            <div class="d-flex justify-content-between align-items-center">
                                <small class="text-muted">
                                    <i class="fas fa-calendar"></i> {{ item.created_at|date:"d M, Y" }}
                                </small>
                                <span class="badge bg-secondary">{{ item.category.name }}</span>
                            </div>
                            
                            <a href="{% url 'news:detail' item.slug %}" 
                               class="btn btn-primary btn-sm mt-2 w-100">
                                📖 Batafsil o'qish
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        <!-- Pagination -->
        {% if news.has_other_pages %}
        <nav aria-label="Sahifalar" class="mt-4">
            <ul class="pagination justify-content-center">
                {% if news.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1{% if current_category %}&category={{ current_category }}{% endif %}{% if search_query %}&q={{ search_query }}{% endif %}">
                        &laquo; Birinchi
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ news.previous_page_number }}{% if current_category %}&category={{ current_category }}{% endif %}{% if search_query %}&q={{ search_query }}{% endif %}">
                        Avvalgi
                    </a>
                </li>
                {% endif %}
                
                <!-- Sahifa raqamlari -->
                {% for num in news.paginator.page_range %}
                    {% if news.number|add:'-3' <= num <= news.number|add:'3' %}
                    <li class="page-item {% if news.number == num %}active{% endif %}">
                        <a class="page-link" href="?page={{ num }}{% if current_category %}&category={{ current_category }}{% endif %}{% if search_query %}&q={{ search_query }}{% endif %}">
                            {{ num }}
                        </a>
                    </li>
                    {% endif %}
                {% endfor %}
                
                {% if news.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ news.next_page_number }}{% if current_category %}&category={{ current_category }}{% endif %}{% if search_query %}&q={{ search_query }}{% endif %}">
                        Keyingi
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ news.paginator.num_pages }}{% if current_category %}&category={{ current_category }}{% endif %}{% if search_query %}&q={{ search_query }}{% endif %}">
                        Oxirgi &raquo;
                    </a>
                </li>
                {% endif %}
            </ul>
        </nav>
        {% endif %}
        
        {% else %}
        <!-- Bo'sh holat -->
        <div class="text-center py-5">
            <div class="mb-4">
                <i class="fas fa-newspaper fa-5x text-muted"></i>
            </div>
            
            {% if search_query %}
            <h4>Qidiruv natijasi topilmadi</h4>
            <p class="text-muted">"{{ search_query }}" bo'yicha hech narsa topilmadi</p>
            <a href="{% url 'news:list' %}" class="btn btn-primary">Barchasi</a>
            {% elif current_category %}
            <h4>Bu kategoriyada yangilik yo'q</h4>
            <p class="text-muted">Tez orada yangiliklar qo'shiladi</p>
            <a href="{% url 'news:list' %}" class="btn btn-primary">Barchasi</a>
            {% else %}
            <h4>Hozircha yangiliklar yo'q</h4>
            <p class="text-muted">Tez orada birinchi yangiliklar paydo bo'ladi</p>
            {% endif %}
        </div>
        {% endif %}
    </div>
</div>
{% endblock %}
```

</details>

### Amaliy ish 5: News Detail template

**Vazifa:** news/templates/news/detail.html fayl yarating.

**Talab:**
- Yangilik to'liq mazmuni
- Muallif va sana ma'lumotlari
- O'xshash yangiliklar
- Orqaga qaytish tugmasi

<details>
<summary>Template yechimi</summary>

```html
<!-- news/templates/news/detail.html -->
{% extends 'base.html' %}

{% block title %}{{ news.title }} - Yangiliklar sayti{% endblock %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <!-- Asosiy yangilik -->
        <article>
            <!-- Breadcrumb -->
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item">
                        <a href="{% url 'news:list' %}">Yangiliklar</a>
                    </li>
                    <li class="breadcrumb-item">
                        <a href="{% url 'news:list' %}?category={{ news.category.slug }}">
                            {{ news.category.name }}
                        </a>
                    </li>
                    <li class="breadcrumb-item active">{{ news.title|truncatechars:30 }}</li>
                </ol>
            </nav>
            
            <!-- Yangilik sarlavhasi -->
            <h1 class="mb-3">{{ news.title }}</h1>
            
            <!-- Meta ma'lumotlar -->
            <div class="row mb-4">
                <div class="col">
                    <div class="d-flex flex-wrap align-items-center text-muted">
                        <span class="me-3">
                            <i class="fas fa-user"></i>
                            <strong>{{ news.author.get_full_name|default:news.author.username }}</strong>
                        </span>
                        <span class="me-3">
                            <i class="fas fa-calendar"></i>
                            {{ news.created_at|date:"d M, Y H:i" }}
                        </span>
                        <span class="me-3">
                            <i class="fas fa-folder"></i>
                            <a href="{% url 'news:list' %}?category={{ news.category.slug }}" 
                               class="text-decoration-none">
                                {{ news.category.name }}
                            </a>
                        </span>
                        {% if news.updated_at != news.created_at %}
                        <span>
                            <i class="fas fa-edit"></i>
                            <small>O'zgartirilgan: {{ news.updated_at|date:"d M, Y H:i" }}</small>
                        </span>
                        {% endif %}
                    </div>
                </div>
            </div>
            
            <!-- Asosiy rasm -->
            {% if news.image %}
            <div class="mb-4">
                <img src="{{ news.image.url }}" class="img-fluid rounded shadow" alt="{{ news.title }}">
            </div>
            {% endif %}
            
            <!-- Yangilik mazmuni -->
            <div class="content">
                {{ news.content|linebreaks }}
            </div>
            
            <!-- Action tugmalari -->
            <div class="mt-4 pt-3 border-top">
                <div class="row">
                    <div class="col">
                        <a href="{% url 'news:list' %}" class="btn btn-outline-secondary">
                            <i class="fas fa-arrow-left"></i> Orqaga
                        </a>
                        
                        <a href="{% url 'news:list' %}?category={{ news.category.slug }}" 
                           class="btn btn-outline-primary">
                            <i class="fas fa-folder"></i> {{ news.category.name }} yangiliklari
                        </a>
                    </div>
                    
                    <div class="col-auto">
                        <!-- Share tugmalari (ixtiyoriy) -->
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-outline-success btn-sm" 
                                    onclick="shareToWhatsApp()">
                                <i class="fab fa-whatsapp"></i>
                            </button>
                            <button type="button" class="btn btn-outline-info btn-sm" 
                                    onclick="shareToTelegram()">
                                <i class="fab fa-telegram"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </article>
    </div>
    
    <!-- Sidebar - O'xshash yangiliklar -->
    <div class="col-lg-4">
        {% if related_news %}
        <div class="card">
            <div class="card-header">
                <h6 class="mb-0">📰 O'xshash yangiliklar</h6>
            </div>
            <div class="card-body">
                {% for item in related_news %}
                <div class="row mb-3 {% if not forloop.last %}border-bottom pb-3{% endif %}">
                    {% if item.image %}
                    <div class="col-4">
                        <img src="{{ item.image.url }}" class="img-fluid rounded" 
                             alt="{{ item.title }}" style="height: 80px; object-fit: cover;">
                    </div>
                    <div class="col-8">
                    {% else %}
                    <div class="col-12">
                    {% endif %}
                        <h6 class="mb-1">
                            <a href="{% url 'news:detail' item.slug %}" class="text-decoration-none">
                                {{ item.title|truncatechars:60 }}
                            </a>
                        </h6>
                        <small class="text-muted">
                            <i class="fas fa-calendar"></i> {{ item.created_at|date:"d M, Y" }}
                        </small>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        
        <!-- Kategoriya haqida ma'lumot -->
        <div class="card mt-3">
            <div class="card-header">
                <h6 class="mb-0">ℹ️ Kategoriya haqida</h6>
            </div>
            <div class="card-body">
                <h6>{{ news.category.name }}</h6>
                <p class="small text-muted mb-2">
                    Ushbu kategoriyada jami 
                    <strong>{{ news.category.news_set.filter.is_published.count }}</strong> ta yangilik mavjud
                </p>
                <a href="{% url 'news:list' %}?category={{ news.category.slug }}" 
                   class="btn btn-outline-primary btn-sm">
                    Barchasini ko'rish
                </a>
            </div>
        </div>
    </div>
</div>

<!-- Share script -->
<script>
function shareToWhatsApp() {
    const url = window.location.href;
    const text = "{{ news.title|escapejs }}";
    window.open(`https://wa.me/?text=${encodeURIComponent(text + ' ' + url)}`, '_blank');
}

function shareToTelegram() {
    const url = window.location.href;
    const text = "{{ news.title|escapejs }}";
    window.open(`https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(text)}`, '_blank');
}
</script>
{% endblock %}
```

</details>

### Amaliy ish 6: Qo'shimcha funksiyalar qo'shish

**Vazifa:** Views'ga qidiruv funksiyasini qo'shing va sinab ko'ring.

**1. Qidiruv funksiyasini views'ga qo'shish:**

```python
# news/views.py'ga qo'shing
def news_list(request):
    news_list = News.objects.filter(is_published=True).select_related('author', 'category')
    
    # Qidiruv qo'shish
    search_query = request.GET.get('q')
    if search_query:
        news_list = news_list.filter(
            title__icontains=search_query
        )
    
    # Qolgan kod...
    
    context = {
        'news': news,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,  # Bu qatorni qo'shing
    }
    return render(request, 'news/list.html', context)
```

**2. Ko'proq ma'lumot qo'shish:**

```python
# news/models.py'ga qo'shimcha metodlar
class News(models.Model):
    # mavjud maydonlar...
    
    def get_reading_time(self):
        """Matnni o'qish uchun taxminiy vaqt (daqiqalarda)"""
        word_count = len(self.content.split())
        reading_time = word_count / 200  # Daqiqada 200 so'z
        return max(1, round(reading_time))
    
    def get_short_content(self, words=30):
        """Qisqartirilgan mazmun"""
        return ' '.join(self.content.split()[:words]) + '...'
```

Template'da ishlatish:

```html
<!-- news/templates/news/list.html ichida -->
<p class="card-text">{{ item.get_short_content:20 }}</p>
<small class="text-muted">
    📖 {{ item.get_reading_time }} daqiqa o'qish
</small>
```

### Amaliy ish 7: Testlash va debug qilish

**1. Views'larni sinab ko'ring:**

```bash
# Server ishga tushiring
python manage.py runserver

# Brauzerda ochib ko'ring:
# http://127.0.0.1:8000/news/
# http://127.0.0.1:8000/news/yangilik-slug/
```

**2. Xatoliklarni topish:**

```python
# news/views.py'da debug qo'shish
def news_list(request):
    print(f"Request GET parameters: {request.GET}")  # Debug
    
    news_list = News.objects.filter(is_published=True)
    print(f"Total news count: {news_list.count()}")  # Debug
    
    # Qolgan kod...
```

### Amaliy ish 8: Performance yaxshilash

**Vazifa:** Ma'lumotlar bazasiga kamroq so'rov yuborish uchun optimizatsiya qiling.

```python
# news/views.py - optimizatsiya qilingan versiya
def news_list(request):
    # select_related va prefetch_related ishlatish
    news_list = News.objects.filter(
        is_published=True
    ).select_related(
        'author', 'category'
    ).only(
        'title', 'slug', 'content', 'image', 'created_at',
        'author__username', 'author__first_name', 'author__last_name',
        'category__name', 'category__slug'
    )
    
    # Qolgan kod bir xil...

def news_detail(request, slug):
    # Faqat kerakli maydonlarni olish
    news = get_object_or_404(
        News.objects.select_related('author', 'category'),
        slug=slug, 
        is_published=True
    )
    
    # O'xshash yangiliklar uchun ham optimizatsiya
    related_news = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id).select_related('category').only(
        'title', 'slug', 'image', 'created_at', 'category__name'
    )[:3]
    
    # Qolgan kod...
```

## Sinovlar yozish

### Test faylini yaratish

```python
# news/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import News, Category

class NewsViewsTest(TestCase):
    def setUp(self):
        """Har bir test uchun ma'lumot tayyorlash"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test kategoriya',
            slug='test-cat'
        )
        self.news = News.objects.create(
            title='Test yangilik',
            slug='test-yangilik',
            content='Bu test uchun yangilik matni',
            author=self.user,
            category=self.category,
            is_published=True
        )
    
    def test_news_list_view(self):
        """News list sahifasi to'g'ri ishlayotganini tekshirish"""
        response = self.client.get(reverse('news:list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test yangilik')
        self.assertContains(response, 'Test kategoriya')
    
    def test_news_detail_view(self):
        """News detail sahifasi to'g'ri ishlayotganini tekshirish"""
        response = self.client.get(reverse('news:detail', kwargs={'slug': 'test-yangilik'}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test yangilik')
        self.assertContains(response, 'Bu test uchun yangilik matni')
    
    def test_news_detail_404(self):
        """Mavjud bo'lmagan yangilik uchun 404 qaytarish"""
        response = self.client.get(reverse('news:detail', kwargs={'slug': 'mavjud-emas'}))
        self.assertEqual(response.status_code, 404)
    
    def test_category_filter(self):
        """Kategoriya bo'yicha filtrlash"""
        response = self.client.get(reverse('news:list') + '?category=test-cat')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test yangilik')
    
    def test_search_functionality(self):
        """Qidiruv funksiyasi"""
        response = self.client.get(reverse('news:list') + '?q=test')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test yangilik')
```

**Testlarni ishga tushirish:**

```bash
python manage.py test news.tests.NewsViewsTest
```

## Vazifalar o'zingiz uchun

### 1-vazifa: Like/Unlike funksiyasi

News modeliga like system qo'shing:

```python
# news/models.py'ga qo'shing
class NewsLike(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('news', 'user')
```

### 2-vazifa: Comments system

Yangiliklarga izoh qoldirish imkonini qo'shing.

### 3-vazifa: Advanced search

Qidiruvni kengaytiring - mazmun, muallif, kategoriya bo'yicha qidiruv.

### 4-vazifa: Social sharing

Facebook, Twitter kabi ijtimoiy tarmoqlarga ulashish tugmalarini qo'shing.

## Keng tarqalgan xatoliklar va yechimlar

### 1. Template topilmaydi

**Xato:** `TemplateDoesNotExist at /news/`

**Yechim:** 
- `TEMPLATES` settings'da `news` app qo'shilganligini tekshiring
- Template fayl yo'li to'g'ri ekanligini tekshiring

### 2. Static fayllar yuklanmaydi

**Xato:** CSS/JS fayllar ishlamaydi

**Yechim:**
```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# urls.py'da
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

### 3. Media fayllar ko'rinmaydi

**Yechim:**
```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# urls.py'da
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 4. Pagination ishlamaydi

**Yechim:** GET parametrlarini to'g'ri uzatganligini tekshiring:

```html
<!-- To'g'ri usul -->
<a href="?page={{ num }}{% if current_category %}&category={{ current_category }}{% endif %}">

<!-- Noto'g'ri usul -->
<a href="?page={{ num }}">
```

## Qo'shimcha maslahatlar

### 1. URL pattern'larda tartib muhim

```python
# To'g'ri tartib
urlpatterns = [
    path('', views.news_list, name='list'),           # /news/
    path('search/', views.news_search, name='search'), # /news/search/
    path('<slug:slug>/', views.news_detail, name='detail'), # /news/some-slug/
]

# Noto'g'ri tartib - detail pattern search'ni "tutib oladi"
urlpatterns = [
    path('<slug:slug>/', views.news_detail, name='detail'),
    path('search/', views.news_search, name='search'), # Bu ishlamaydi!
]
```

### 2. Template'da xavfsizlik

```html
<!-- Foydalanuvchi ma'lumotlarini escape qiling -->
<h1>{{ news.title }}</h1>  <!-- Safe -->
<div>{{ news.content|linebreaks }}</div>  <!-- Safe -->

<!-- Raw HTML ishlatishdan saqlaning -->
<div>{{ news.content|safe }}</div>  <!-- Xavfli, faqat ishonchli ma'lumot uchun -->
```

### 3. Performance monitoring

```python
# news/views.py'da debugging
import time
from django.db import connection

def news_list(request):
    start_time = time.time()
    
    # Sizning kodingiz...
    
    # Debug ma'lumotlari
    if settings.DEBUG:
        print(f"View execution time: {time.time() - start_time:.3f}s")
        print(f"Database queries: {len(connection.queries)}")
    
    return render(request, 'news/list.html', context)
```

## Mustaqil loyiha

### Topshiriq: Mahalliy yangiliklar sayti

Quyidagi talablar bo'yicha o'z yangiliklar saytingizni yarating:

**Funksional talablar:**
1. **Kategoriyalar:**
   - Mahalliy yangiliklar
   - Sport
   - Madaniyat
   - Iqtisodiyot

2. **Yangiliklar ro'yxati:**
   - Eng so'nggisi yuqorida
   - Kategoriya bo'yicha filtrlash
   - Qidiruv funksiyasi
   - Har sahifada 9 ta yangilik

3. **Detail sahifa:**
   - To'liq matn
   - O'xshash yangiliklar (3 ta)
   - Ijtimoiy tarmoqlarga ulashish
   - Breadcrumb navigation

4. **Qo'shimcha:**
   - Responsive dizayn
   - Loading states
   - Empty states
   - Error handling

**Texnik talablar:**
- Function-based views ishlatish
- Bootstrap 5 ishlatish
- Pagination qo'shish
- SEO friendly URL'lar
- Performance optimizatsiya

### Bosqichma-bosqich bajarish:

**1-bosqich:** Models yaratish va admin sozlash
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

**2-bosqich:** Admin orqali test ma'lumotlari qo'shish
- 4 ta kategoriya yarating
- Har kategoriyada kamida 3 ta yangilik qo'shing
- Rasmlar yuklang

**3-bosqich:** Views va URLs yaratish
- news_list funksiyasi
- news_detail funksiyasi
- URL patterns

**4-bosqich:** Templates yaratish
- base.html
- news/list.html
- news/detail.html

**5-bosqich:** Test qilish va xatoliklarni tuzatish

## Baholash mezonlari

**A'lo (5):**
- Barcha funksiyalar ishlaydi
- Responsive dizayn
- Performance optimizatsiya
- Error handling
- Clean code

**Yaxshi (4):**
- Asosiy funksiyalar ishlaydi
- Oddiy dizayn
- Biroz optimizatsiya

**Qoniqarli (3):**
- Asosiy sahifalar ishlaydi
- Minimal dizayn

## Ko'mak va manba

### Foydali linklar:
- [Django Pagination](https://docs.djangoproject.com/en/4.2/topics/pagination/)
- [Django Generic Views](https://docs.djangoproject.com/en/4.2/ref/class-based-views/)
- [Bootstrap 5 Components](https://getbootstrap.com/docs/5.1/components/)

### Debug qilish:

```python
# Shell'da test qilish
python manage.py shell

from news.models import News
print(News.objects.all())
print(News.objects.filter(is_published=True).count())
```

### Umumiy xatoliklar:

1. **NoReverseMatch xatosi** - URL name'lari noto'g'ri
2. **TemplateDoesNotExist** - Template fayl yo'li xato
3. **AttributeError** - Model methodlari noto'g'ri
4. **ImportError** - Import'lar noto'g'ri

## Keyingi bosqich

Ushbu amaliyotni muvaffaqiyatli bajarib bo'lgach, keyingi darsda:
- Template'lar va static fayllar bilan chuqurroq ishlash
- Custom CSS va JavaScript qo'shish
- Responsive dizayn yaratish
- Advanced frontend funksiyalar

## Yakuniy tekshiruv

Quyidagi barcha nuqtalar ishlayotganligini tekshiring:

- [ ] `/news/` sahifasi ochiladi
- [ ] Yangiliklar ko'rinadi
- [ ] Kategoriya filtri ishlaydi
- [ ] Qidiruv ishlaydi
- [ ] Pagination ishlaydi
- [ ] Detail sahifa ochiladi
- [ ] O'xshash yangiliklar ko'rinadi
- [ ] Orqaga qaytish tugmasi ishlaydi
- [ ] Mobile'da yaxshi ko'rinadi

Barcha nuqtalar ✅ bo'lsa, siz darsni muvaffaqiyatli tugallang! 🎉

## Best Practice'lar

### 1. **DRY (Don't Repeat Yourself)**
```python
# Yomon usul - kod takrorlash
def news_list(request):
    news_list = News.objects.filter(is_published=True).select_related('author', 'category')
    # ...

def news_by_category(request, category_slug):
    news_list = News.objects.filter(is_published=True).select_related('author', 'category')
    # Bir xil kod takrorlanmoqda...

# Yaxshi usul - umumiy queryset
class NewsManager(models.Manager):
    def published(self):
        return self.filter(is_published=True).select_related('author', 'category')

# models.py'da
class News(models.Model):
    # maydonlar...
    objects = NewsManager()
```

### 2. **Consistent naming**
```python
# Template name'lar
'news/list.html'     # ✅ Aniq
'news/detail.html'   # ✅ Aniq

'news/show.html'     # ❌ Noaniq
'news/view.html'     # ❌ Noaniq
```

### 3. **Template inheritance**
```html
<!-- ✅ To'g'ri struktura -->
base.html
├── news/
│   ├── list.html (extends base.html)
│   └── detail.html (extends base.html)

<!-- ❌ Noto'g'ri - kodni takrorlash -->
news/list.html (to'liq HTML)
news/detail.html (to'liq HTML)
```

### 4. **URL naming convention**
```python
# ✅ To'g'ri
app_name = 'news'
urlpatterns = [
    path('', views.news_list, name='list'),
    path('<slug:slug>/', views.news_detail, name='detail'),
]

# Template'da: {% url 'news:list' %}

# ❌ Noto'g'ri
urlpatterns = [
    path('', views.news_list, name='news_list_view'),
    path('<slug:slug>/', views.news_detail, name='show_news_detail'),
]
```

### 5. **Context data optimization**
```python
# ✅ Optimal - faqat kerakli ma'lumot
context = {
    'news': news,
    'categories': categories,
    'current_category': category_slug,
}

# ❌ Keraksiz ma'lumot
context = {
    'news': news,
    'categories': categories,
    'all_users': User.objects.all(),  # Nima uchun?
    'all_news': News.objects.all(),   # Keraksiz
}
```

Muvaffaqiyat tilaymiz! 🚀  'news'

urlpatterns = [
    # TODO: URL pattern'larni yozing
]
```

**Yechim:**

<details>
<summary>Yechimni ko'rish</summary>

```python
# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_list, name='list'),
    path('<slug:slug>/', views.news_detail, name='detail'),
]
```

</details>

### Amaliy ish 3: Settings'da TEMPLATES sozlash

**Vazifa:** settings.py faylida templates sozlamalarini tekshiring.

```python
# myproject/settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Bu qator muhim!
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Amaliy ish 4: Folder struktura yaratish

**Vazifa:** Kerakli folder'lar va fayllar yarating.

```
myproject/
├── news/
│   ├── templates/
│   │   └── news/
│   │       ├── list.html
│   │       └── detail.html
│   ├── views.py
│   ├── urls.py
│   └── models.py
├── templates/
│   └── base.html
└── media/
    └── news/
```

**Terminal commandalari:**

```bash
# Folder'lar yaratish
mkdir -p news/templates/news
mkdir -p templates
mkdir -p media/news

# Fayllar yaratish
touch news/templates/news/list.html
touch news/templates/news/detail.html
touch templates/base.html
```

### Amaliy ish 5: Views'larni to'liq yozish

**Vazifa:** news/views.py faylini to'liq yakunlang.

**Sizning vazifangiz:**
1. news_list funksiyasini yozing
2. news_detail funksiyasini yozing  
3. Qidiruv funksiyasini qo'shing
4. Error handling qo'shing

```python
# news/views.py - boshlang'ich shablon
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import News, Category

def news_list(request):
    # 1. Sizning kodingiz - yangiliklar ro'yxatini olish
    
    # 2. Sizning kodingiz - qidiruv qo'shish
    
    # 3. Sizning kodingiz - kategoriya filtri
    
    # 4. Sizning kodingiz - pagination
    
    # 5. Sizning kodingiz - context tayyorlash
    
    pass

def news_detail(request, slug):
    # 1. Sizning kodingiz - yangilikni topish
    
    # 2. Sizning kodingiz - o'xshash yangiliklar
    
    # 3. Sizning kodingiz - context tayyorlash
    
    pass
```

**Yechim - faqat kerak bo'lganda oching:**

<details>
<summary>To'liq views.py yechimi</summary>

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import News, Category

def news_list(request):
    """Yangiliklar ro'yxati sahifasi"""
    
    # 1. Asosiy queryset
    news_list = News.objects.filter(is_published=True).select_related('author', 'category')
    
    # 2. Qidiruv funksiyasi
    search_query = request.GET.get('q', '').strip()
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    # 3. Kategoriya bo'yicha filtrlash
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        try:
            selected_category = Category.objects.get(slug=category_slug)
            news_list = news_list.filter(category=selected_category)
        except Category.DoesNotExist:
            pass
    
    # 4. Pagination
    paginator = Paginator(news_list, 6)
    page_number = request.GET.get('page', 1)
    
    try:
        news = paginator.page(page_number)
    except:
        news = paginator.page(1)
    
    # 5. Barcha kategoriyalar
    categories = Category.objects.all()
    
    # 6. Context tayyorlash
    context = {
        'news': news,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'selected_category': selected_category,
        'total_count': paginator.count,
    }
    
    return render(request, 'news/list.html', context)

def news_detail(request, slug):
    """Yangilik detail sahifasi"""
    
    # 1. Yangilikni topish (404 xatosi bilan)
    news = get_object_or_404(
        News.objects.select_related('author', 'category'),
        slug=slug,
        is_published=True
    )
    
    # 2. O'xshash yangiliklar (bir xil kategoriyadan)
    related_news = News.objects.filter(
        category=news.category,
        is_published=True
    ).exclude(id=news.id).select_related('category')[:4]
    
    # 3. Kategoriyadan boshqa yangiliklar soni
    category_news_count = News.objects.filter(
        category=news.category,
        is_published=True
    ).count()
    
    # 4. Context
    context = {
        'news': news,
        'related_news': related_news,
        'category_news_count': category_news_count,
    }
    
    return render(request, 'news/detail.html', context)
```

</details>

### Amaliy ish 6: Template fayllarini yozish

**6.1. Base template yaratish**

```html
<!-- templates/base.html - O'zingiz to'ldiring -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <!-- TODO: Meta taglar qo'shing -->
    <!-- TODO: Bootstrap CSS qo'shing -->
    <!-- TODO: Title block yarating -->
</head>
<body>
    <!-- TODO: Navigation yarating -->
    <!-- TODO: Main content block -->
    <!-- TODO: Footer qo'shing -->
    <!-- TODO: Bootstrap JS qo'shing -->
</body>
</html>
```

**6.2. List template yaratish**

O'zingiz `news/templates/news/list.html` faylini yozib ko'ring. Kerakli elementlar:
- Qidiruv forma
- Kategoriyalar sidebar  
- Yangiliklar grid (3 ustun)
- Pagination
- Empty state

**6.3. Detail template yaratish**

O'zingiz `news/templates/news/detail.html` faylini yozib ko'ring. Kerakli elementlar:
- Breadcrumb navigation
- Yangilik to'liq matni
- Meta ma'lumotlar (muallif, sana)
- O'xshash yangiliklar sidebar
- Orqaga qaytish tugmasi

### Amaliy ish 7: Test ma'lumotlari qo'shish

**Vazifa:** Admin panel orqali test ma'lumotlari qo'shing.

```bash
# Superuser yarating
python manage.py createsuperuser

# Admin panelga kiring: http://127.0.0.1:8000/admin/
```

**Admin panelda:**
1. **3-4 ta kategoriya** yarating (Texnologiya, Sport, Siyosat, Madaniyat)
2. **Har kategoriyada 5-6 ta yangilik** qo'shing
3. **Rasmlar yuklang** (internet'dan test rasmlari)
4. **Yangiliklar mazmunini** uzoq qiling (kamida 200-300 so'z)

### Amaliy ish 8: Sinov va tuzatish

**8.1. Asosiy funksiyalarni sinang:**

```
1. Yangiliklar ro'yxati: http://127.0.0.1:8000/news/
2. Kategoriya filtri: http://127.0.0.1:8000/news/?category=tech
3. Qidiruv: http://127.0.0.1:8000/news/?q=test
4. Pagination: http://127.0.0.1:8000/news/?page=2
5. Detail sahifa: http://127.0.0.1:8000/news/yangilik-slug/
```

**8.2. Mobile'da sinash:**

Browser'da F12 bosing va mobile view'da sahifalarni tekshiring.

**8.3. Xatoliklarni tuzating:**

Agar sahifa ishlamasa:
```bash
# Debug mode'da xatolikni ko'ring
python manage.py runserver

# Log'larga qarang
tail -f /var/log/django.log  # agar mavjud bo'lsa
```

### Amaliy ish 9: Performance test qilish

**Vazifa:** Sahifalar tezligini o'lchang va yaxshilang.

```python
# news/views.py'ga qo'shing
import time
from django.db import connection

def news_list(request):
    start_time = time.time()
    query_count_start = len(connection.queries)
    
    # Sizning kodingiz...
    
    # Performance ma'lumotlari
    end_time = time.time()
    query_count_end = len(connection.queries)
    
    print(f"⏱️  Sahifa yuklash vaqti: {end_time - start_time:.3f} soniya")
    print(f"🗃️  Database so'rovlar soni: {query_count_end - query_count_start}")
    
    return render(request, 'news/list.html', context)
```

**Maqsad:** 
- Sahifa 1 soniyadan kam vaqtda yuklanishi
- Database so'rovlar 10 tadan kam bo'lishi

### Amaliy ish 10: Class-based Views'ga o'tish (Ixtiyoriy)

**Vazifa:** Function-based views o'rniga Class-based views yozing.

```python
# news/views.py'ga qo'shing
from django.views.generic import ListView, DetailView

class NewsListView(ListView):
    # TODO: Bu klassni to'ldiring
    pass

class NewsDetailView(DetailView):  
    # TODO: Bu klassni to'ldiring
    pass
```

**Yechim:**

<details>
<summary>CBV yechimi</summary>

```python
from django.views.generic import ListView, DetailView
from django.db.models import Q

class NewsListView(ListView):
    model = News
    template_name = 'news/list.html'
    context_object_name = 'news'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = News.objects.filter(is_published=True).select_related('author', 'category')
        
        # Qidiruv
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        # Kategoriya
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('author', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # O'xshash yangiliklar
        context['related_news'] = News.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id).select_related('category')[:4]
        
        return context
```

URL'larda o'zgarish:
```python
# news/urls.py
urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
]
```

</details>

## Loyiha yakunlash

### Final tekshiruv

Quyidagi ro'yxatni to'liq bajaring:

**✅ Texnik tekshiruv:**
- [ ] Models to'g'ri yaratilgan va migration bajarilgan
- [ ] Admin panel ishlamoqda va ma'lumotlar qo'shilgan
- [ ] URLs to'g'ri konfiguratsiya qilingan
- [ ] Views yozilgan va xatoliksiz
- [ ] Templates yaratilgan va to'g'ri joylashtirilgan

**✅ Funksional tekshiruv:**
- [ ] Yangiliklar ro'yxati sahifasi ochiladi
- [ ] Kategoriya bo'yicha filtrlash ishlaydi
- [ ] Qidiruv funksiyasi ishlaydi
- [ ] Pagination to'g'ri ishlaydi
- [ ] Detail sahifa ochiladi va to'liq matn ko'rsatiladi
- [ ] O'xshash yangiliklar ko'rsatiladi
- [ ] Navigation (orqaga qaytish) ishlaydi

**✅ Dizayn tekshiruv:**
- [ ] Sahifa mobile'da yaxshi ko'rinadi
- [ ] Bootstrap componentlari to'g'ri ishlaydi
- [ ] Rasmlar to'g'ri ko'rsatiladi
- [ ] Loading va empty state'lar mavjud

**✅ Performance tekshiruv:**
- [ ] Sahifa 2 soniyadan kam vaqtda yuklaydi
- [ ] Rasmlar optimizatsiya qilingan
- [ ] Database so'rovlar minimallashtirilgan

### Xatoliklarni tuzatish

**Agar sahifa ochilmasa:**

1. **URL xatosi tekshirish:**
```bash
python manage.py shell
>>> from django.urls import reverse
>>> reverse('news:list')
'/news/'
>>> reverse('news:detail', kwargs={'slug': 'test'})
'/news/test/'
```

2. **Template xatosi:**
```bash
# Django'da template debug
# settings.py'da
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True
```

3. **Ma'lumotlar bazasi xatosi:**
```bash
python manage.py shell
>>> from news.models import News
>>> News.objects.all()
>>> News.objects.filter(is_published=True)
```

### Bonus vazifalar (Qo'shimcha ball uchun)

**Bonus 1: Ajax qidiruv**
JavaScript orqali real-time qidiruv qo'shing.

**Bonus 2: Infinite scroll**
Pagination o'rniga infinite scroll qo'shing.

**Bonus 3: Dark mode**
Qorong'u rejim qo'shing.

**Bonus 4: Reading progress**
Detail sahifada o'qish jarayonini ko'rsatish.

## Yakuniy loyiha topshirish

### Topshirish talablari:

1. **Code sifati:**
   - Clean code yozilgan
   - Izohlar qo'shilgan
   - PEP 8 standartiga rioya qilingan

2. **Funksiyalar:**
   - Barcha asosiy funksiyalar ishlaydi
   - Error handling qo'shilgan
   - Performance optimizatsiya qilingan

3. **Dizayn:**
   - Professional ko'rinish
   - Responsive dizayn
   - User-friendly interface

### Topshirish format:

```
news_project_[ISMINGIZ]/
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── news/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── templates/
│   └── migrations/
├── templates/
│   └── base.html
├── media/
├── requirements.txt
└── README.md
```

### README.md fayli yozing:

```markdown
# Yangiliklar sayti - 16-dars loyihasi

## Loyiha haqida
Django framework'ida yaratilgan yangiliklar sayti.

## Funksiyalar
- Yangiliklar ro'yxati
- Kategoriya bo'yicha filtrlash  
- Qidiruv funksiyasi
- Pagination
- Detail sahifa
- O'xshash yangiliklar

## O'rnatish
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Muallif
[Sizning ismingiz]
```

## Dars xulosasi

Ushbu amaliyotda siz o'rgandingiz:

### 🎯 **Asosiy bilimlar:**
- Django Views yaratish (Function-based)
- URL routing va naming
- Template inheritance
- Context data bilan ishlash
- Pagination qo'shish

### 🔧 **Texnik ko'nikmalar:**
- Database optimizatsiya (select_related)
- Error handling (404, empty states)
- Form handling (GET parameters)
- Performance monitoring
- Testing views

### 🎨 **Frontend skills:**
- Bootstrap grid system
- Responsive design
- Card layouts
- Navigation systems
- User experience design

### 📈 **Professional skills:**
- Code organization
- Best practices
- Clean code writing
- Project structure
- Documentation writing

## Keyingi darsga tayyorgarlik

17-darsda **"Template va static fayllar bilan ishlash"** o'tamiz. Tayyorgarlik:

1. Ushbu darsni to'liq bajaring
2. Loyihangiz ishlayotganligini tekshiring
3. Static fayllar uchun CSS/JS haqida o'ylang
4. Qanday dizayn qilmoqchi ekanligingizni rejalashtiring

## Muvaffaqiyat belgisi 🏆

Agar quyidagilarni bajara olsangiz, darsni muvaffaqiyatli o'zlatdingiz:

- ✅ Yangiliklar sahifasi to'liq ishlaydi
- ✅ Detail sahifa professional ko'rinishda
- ✅ Qidiruv va filtrlash funksiyalar mavjud
- ✅ Mobile'da ham yaxshi ishlaydi
- ✅ Code clean va tushunarlı yozilgan

**Tabriklaymiz! 🎉 16-darsni muvaffaqiyatli yakunladingiz!**