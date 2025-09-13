# 25-dars: Template teglari. Loyihani to'ldirish

## Dars maqsadi
Ushbu darsda Django template teglarini o'rganamiz va yangiliklar loyihasini to'liq funksional qilamiz. Template teglari yordamida sahifalarni dinamik qilib, foydalanuvchilarga yaxshiroq tajriba taqdim etamiz.

## Nazariy qism

### Template teglari nima?

Django template teglari - bu template ichida mantiqiy amallarni bajarish uchun ishlatiladigan maxsus sintaksisdir. Ular `{% %}` belgilar orasida yoziladi va sahifaga dinamik kontent qo'shish imkonini beradi.

### Asosiy template teglari

#### 1. `{% for %}` - Takrorlash tegi
Bu teg ro'yxat yoki boshqa iterable obyektlar bo'ylab aylanish uchun ishlatiladi.

```django
{% for yangilik in yangiliklar %}
    <h3>{{ yangilik.sarlavha }}</h3>
    <p>{{ yangilik.matn }}</p>
{% endfor %}
```

#### 2. `{% if %}` - Shartli teg
Ma'lum shart bajarilganda kontent ko'rsatish uchun.

```django
{% if user.is_authenticated %}
    <p>Xush kelibsiz, {{ user.username }}!</p>
{% else %}
    <p>Iltimos, tizimga kiring</p>
{% endif %}
```

#### 3. `{% url %}` - URL yaratish tegi
View nomiga asoslanib URL manzilini yaratadi.

```django
<a href="{% url 'news:detail' yangilik.id %}">Batafsil</a>
```

#### 4. `{% static %}` - Statik fayllar tegi
CSS, JavaScript va rasmlar kabi statik fayllarga yo'l ko'rsatadi.

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

## Amaliy qism: Yangiliklar loyihasini to'ldirish

### 1-bosqich: Base template yaratish

Avvalo asosiy shablon yaratamiz (`base.html`):

```html
<!-- templates/base.html -->
{% load static %}
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Yangiliklar sayti{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="{% url 'news:home' %}">Yangiliklar</a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{% url 'news:home' %}">Bosh sahifa</a>
                <a class="nav-link" href="{% url 'news:all_news' %}">Barcha yangiliklar</a>
                <a class="nav-link" href="{% url 'news:contact' %}">Aloqa</a>
            </div>
        </div>
    </nav>

    <!-- Main content -->
    <main class="container mt-4">
        {% block content %}
        {% endblock %}
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-light mt-5 py-4">
        <div class="container text-center">
            <p>&copy; 2024 Yangiliklar sayti. Barcha huquqlar himoyalangan.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### 2-bosqich: Bosh sahifani to'ldirish

`home.html` templateni yangilaymiz:

```html
<!-- templates/news/home.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Bosh sahifa - Yangiliklar sayti{% endblock %}

{% block content %}
<!-- Hero section -->
<div class="jumbotron bg-primary text-white p-5 rounded mb-4">
    <h1 class="display-4">Yangiliklar sayti</h1>
    <p class="lead">Eng so'nggi yangiliklar va ma'lumotlar bilan tanishing</p>
</div>

<!-- Featured news -->
{% if featured_news %}
<section class="mb-5">
    <h2 class="mb-4">Asosiy yangiliklar</h2>
    <div class="row">
        {% for yangilik in featured_news %}
        <div class="col-md-6 mb-4">
            <div class="card h-100">
                {% if yangilik.rasm %}
                    <img src="{{ yangilik.rasm.url }}" class="card-img-top" alt="{{ yangilik.sarlavha }}" style="height: 200px; object-fit: cover;">
                {% endif %}
                <div class="card-body">
                    <span class="badge bg-secondary">{{ yangilik.kategoriya.nom }}</span>
                    <h5 class="card-title mt-2">{{ yangilik.sarlavha }}</h5>
                    <p class="card-text">{{ yangilik.qisqa_mazmun|truncatewords:20 }}</p>
                    <small class="text-muted">{{ yangilik.yaratilgan_sana|date:"d M, Y" }}</small>
                </div>
                <div class="card-footer">
                    <a href="{% url 'news:detail' yangilik.pk %}" class="btn btn-primary">Batafsil o'qish</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</section>
{% endif %}

<!-- News by categories -->
<section>
    <h2 class="mb-4">Kategoriyalar bo'yicha yangiliklar</h2>
    
    {% for kategoriya, yangiliklar in yangiliklar_by_category.items %}
    {% if yangiliklar %}
    <div class="mb-5">
        <h3 class="h4 mb-3">
            <span class="badge bg-info">{{ kategoriya.nom }}</span>
        </h3>
        <div class="row">
            {% for yangilik in yangiliklar %}
            <div class="col-md-4 mb-3">
                <div class="card h-100">
                    {% if yangilik.rasm %}
                        <img src="{{ yangilik.rasm.url }}" class="card-img-top" alt="{{ yangilik.sarlavha }}" style="height: 150px; object-fit: cover;">
                    {% endif %}
                    <div class="card-body">
                        <h6 class="card-title">{{ yangilik.sarlavha }}</h6>
                        <p class="card-text small">{{ yangilik.qisqa_mazmun|truncatewords:10 }}</p>
                        <small class="text-muted">{{ yangilik.yaratilgan_sana|date:"d M" }}</small>
                    </div>
                    <div class="card-footer p-2">
                        <a href="{% url 'news:detail' yangilik.pk %}" class="btn btn-sm btn-outline-primary">O'qish</a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        
        {% if yangiliklar|length >= 3 %}
        <div class="text-center">
            <a href="{% url 'news:category' kategoriya.slug %}" class="btn btn-outline-secondary">
                {{ kategoriya.nom }} kategoriyasidagi barcha yangiliklar
            </a>
        </div>
        {% endif %}
    </div>
    {% endif %}
    {% empty %}
    <div class="alert alert-info">
        <h4>Hozircha yangilik yo'q</h4>
        <p>Tez orada yangi yangiliklar qo'shiladi.</p>
    </div>
    {% endfor %}
</section>
{% endblock %}
```

### 3-bosqich: Yangilik batafsil sahifasini yaratish

`detail.html` templateni to'liq ishlab chiqamiz:

```html
<!-- templates/news/detail.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}{{ yangilik.sarlavha }} - Yangiliklar sayti{% endblock %}

{% block content %}
<article>
    <!-- Breadcrumb -->
    <nav aria-label="breadcrumb">
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="{% url 'news:home' %}">Bosh sahifa</a></li>
            <li class="breadcrumb-item">
                <a href="{% url 'news:category' yangilik.kategoriya.slug %}">{{ yangilik.kategoriya.nom }}</a>
            </li>
            <li class="breadcrumb-item active">{{ yangilik.sarlavha|truncatewords:5 }}</li>
        </ol>
    </nav>

    <!-- Article header -->
    <header class="mb-4">
        <span class="badge bg-primary">{{ yangilik.kategoriya.nom }}</span>
        <h1 class="mt-2">{{ yangilik.sarlavha }}</h1>
        
        <div class="d-flex justify-content-between align-items-center text-muted mb-3">
            <div>
                <i class="fas fa-calendar"></i> {{ yangilik.yaratilgan_sana|date:"d F, Y" }}
                <i class="fas fa-user ms-3"></i> {{ yangilik.muallif.get_full_name|default:yangilik.muallif.username }}
            </div>
            <div>
                <i class="fas fa-eye"></i> {{ yangilik.ko'rishlar_soni }} marta ko'rilgan
            </div>
        </div>
        
        {% if yangilik.rasm %}
        <img src="{{ yangilik.rasm.url }}" class="img-fluid rounded mb-4" alt="{{ yangilik.sarlavha }}">
        {% endif %}
        
        {% if yangilik.qisqa_mazmun %}
        <div class="alert alert-info">
            <strong>Qisqacha:</strong> {{ yangilik.qisqa_mazmun }}
        </div>
        {% endif %}
    </header>

    <!-- Article content -->
    <div class="article-content">
        {{ yangilik.matn|linebreaks }}
    </div>

    <!-- Tags -->
    {% if yangilik.teglar.all %}
    <div class="mt-4">
        <strong>Teglar:</strong>
        {% for teg in yangilik.teglar.all %}
            <span class="badge bg-secondary me-1">{{ teg.nom }}</span>
        {% endfor %}
    </div>
    {% endif %}

    <!-- Social sharing -->
    <div class="mt-4 pt-4 border-top">
        <h5>Ulashing:</h5>
        <div class="d-flex gap-2">
            <a href="#" class="btn btn-sm btn-primary">Facebook</a>
            <a href="#" class="btn btn-sm btn-info">Twitter</a>
            <a href="#" class="btn btn-sm btn-success">WhatsApp</a>
        </div>
    </div>
</article>

<!-- Related articles -->
{% if tegdosh_yangiliklar %}
<section class="mt-5">
    <h3>Shunga o'xshash yangiliklar</h3>
    <div class="row">
        {% for yangilik in tegdosh_yangiliklar %}
        <div class="col-md-4 mb-3">
            <div class="card">
                {% if yangilik.rasm %}
                    <img src="{{ yangilik.rasm.url }}" class="card-img-top" style="height: 150px; object-fit: cover;">
                {% endif %}
                <div class="card-body">
                    <h6 class="card-title">{{ yangilik.sarlavha }}</h6>
                    <p class="card-text small">{{ yangilik.qisqa_mazmun|truncatewords:15 }}</p>
                    <a href="{% url 'news:detail' yangilik.pk %}" class="btn btn-sm btn-primary">O'qish</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</section>
{% endif %}
{% endblock %}
```

### 4-bosqich: Kategoriya sahifasini yaratish

`category.html` templateni yaratamiz:

```html
<!-- templates/news/category.html -->
{% extends 'base.html' %}

{% block title %}{{ kategoriya.nom }} - Yangiliklar sayti{% endblock %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1>{{ kategoriya.nom }} kategoriyasi</h1>
    <span class="badge bg-primary">{{ yangiliklar.count }} ta yangilik</span>
</div>

{% if kategoriya.tavsif %}
<p class="lead">{{ kategoriya.tavsif }}</p>
{% endif %}

<div class="row">
    {% for yangilik in yangiliklar %}
    <div class="col-md-6 col-lg-4 mb-4">
        <div class="card h-100">
            {% if yangilik.rasm %}
                <img src="{{ yangilik.rasm.url }}" class="card-img-top" style="height: 200px; object-fit: cover;">
            {% endif %}
            <div class="card-body">
                <h5 class="card-title">{{ yangilik.sarlavha }}</h5>
                <p class="card-text">{{ yangilik.qisqa_mazmun|truncatewords:15 }}</p>
                <small class="text-muted">{{ yangilik.yaratilgan_sana|date:"d M, Y" }}</small>
            </div>
            <div class="card-footer">
                <a href="{% url 'news:detail' yangilik.pk %}" class="btn btn-primary btn-sm">Batafsil</a>
            </div>
        </div>
    </div>
    {% empty %}
    <div class="col-12">
        <div class="alert alert-info">
            Ushbu kategoriyada hozircha yangilik yo'q.
        </div>
    </div>
    {% endfor %}
</div>

<!-- Pagination -->
{% if is_paginated %}
<nav>
    <ul class="pagination justify-content-center">
        {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Oldingi</a>
            </li>
        {% endif %}
        
        <li class="page-item active">
            <span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span>
        </li>
        
        {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}">Keyingi</a>
            </li>
        {% endif %}
    </ul>
</nav>
{% endif %}
{% endblock %}
```

### 5-bosqich: Views.py faylini yangilash

Template teglarini to'liq ishlatish uchun views ni ham yangilashimiz kerak:

```python
# news/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Count
from .models import Yangilik, Kategoriya

class HomeView(ListView):
    model = Yangilik
    template_name = 'news/home.html'
    context_object_name = 'yangiliklar'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Asosiy yangiliklar (eng ko'p ko'rilgan)
        context['featured_news'] = Yangilik.objects.filter(
            nashr_etilgan=True
        ).order_by('-ko\'rishlar_soni')[:4]
        
        # Kategoriyalar bo'yicha yangiliklar
        kategoriyalar = Kategoriya.objects.all()
        yangiliklar_by_category = {}
        
        for kategoriya in kategoriyalar:
            yangiliklar = Yangilik.objects.filter(
                kategoriya=kategoriya,
                nashr_etilgan=True
            ).order_by('-yaratilgan_sana')[:3]
            
            if yangiliklar.exists():
                yangiliklar_by_category[kategoriya] = yangiliklar
        
        context['yangiliklar_by_category'] = yangiliklar_by_category
        return context

class YangiliklarDetailView(DetailView):
    model = Yangilik
    template_name = 'news/detail.html'
    context_object_name = 'yangilik'
    
    def get_object(self):
        # Ko'rishlar sonini oshirish
        obj = super().get_object()
        obj.ko_rishlar_soni += 1
        obj.save()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        yangilik = self.get_object()
        
        # Tegdosh yangiliklar
        context['tegdosh_yangiliklar'] = Yangilik.objects.filter(
            kategoriya=yangilik.kategoriya,
            nashr_etilgan=True
        ).exclude(id=yangilik.id)[:3]
        
        return context

class KategoriyaView(ListView):
    model = Yangilik
    template_name = 'news/category.html'
    context_object_name = 'yangiliklar'
    paginate_by = 6
    
    def get_queryset(self):
        self.kategoriya = get_object_or_404(Kategoriya, slug=self.kwargs['slug'])
        return Yangilik.objects.filter(
            kategoriya=self.kategoriya,
            nashr_etilgan=True
        ).order_by('-yaratilgan_sana')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategoriya'] = self.kategoriya
        return context
```

## Template filtrlari

Django template teglaridan tashqari filtrlar ham mavjud. Ular `|` belgisi bilan ishlatiladi:

```django
{{ yangilik.sarlavha|title }}           # Har bir so'zning birinchi harfini katta qiladi
{{ yangilik.yaratilgan_sana|date:"d M, Y" }}  # Sanani formatlaydi
{{ yangilik.matn|truncatewords:20 }}    # 20 so'zgacha qisqartiradi
{{ yangilik.matn|linebreaks }}          # Matnda qator uzilishlarini HTML'ga aylantiradi
```

## Xulosa

Ushbu darsda biz:
- Django template teglarining asoslarini o'rgandik
- `{% for %}`, `{% if %}`, `{% url %}` kabi asosiy teglarni ishlatdik
- Yangiliklar loyihasini to'liq funksional template bilan ta'minladik
- Base template yaratib, kodlarni qayta ishlatish tamoyilini qo'lladik
- Template filtrlarini o'rgandik

Template teglari Django'ning eng kuchli xususiyatlaridan biri bo'lib, ular orqali dinamik va foydalanuvchi-do'st veb sahifalar yaratish mumkin.

**Keyingi dars:**

26-darsda URL'larni slug bilan ishlash va `get_absolute_url` metodini o'rganamiz.