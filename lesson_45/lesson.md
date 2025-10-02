# Lesson 45: Django'da izoh qoldirish. Template qismini yozish (3-qism)

## Kirish

Assalomu alaykum! Oldingi ikki darsda biz Comment modelini, formasini va views qismini yaratdik. Endi esa eng muhim qism - **template qismini** yozamiz. Bu darsda izohlarni chiroyli va funksional ko'rinishda chiqarishni o'rganamiz.

Bu darsda quyidagilarni o'rganamiz:
- Izoh formasini template'da ko'rsatish
- Izohlar ro'yxatini chiroyli chiqarish
- Bootstrap bilan dizayn qilish
- Foydalanuvchi uchun qulay interfeys yaratish
- Xatolarni chiroyli ko'rsatish

---

## 1. Joriy news_detail.html shabloni

Avval joriy template'imizni ko'rib chiqamiz. Odatda `templates/news/news_detail.html` faylimiz quyidagicha bo'lishi mumkin:

```html
{% extends 'base.html' %}

{% block title %}{{ news.title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <article>
        <h1>{{ news.title }}</h1>
        
        <div class="text-muted mb-3">
            <small>
                <i class="bi bi-person"></i> {{ news.author.get_full_name }}
                <i class="bi bi-calendar ms-3"></i> {{ news.publish_time|date:"d.m.Y H:i" }}
                <i class="bi bi-folder ms-3"></i> {{ news.category.name }}
            </small>
        </div>
        
        {% if news.photo %}
            <img src="{{ news.photo.url }}" class="img-fluid mb-3" alt="{{ news.title }}">
        {% endif %}
        
        <div class="news-body">
            {{ news.body|safe }}
        </div>
    </article>
</div>
{% endblock %}
```

Endi bu template'ga izohlar qismini qo'shamiz.

---

## 2. Izohlar sonini ko'rsatish

Dastlab, yangilik ostida izohlar sonini ko'rsatamiz:

```html
{% extends 'base.html' %}

{% block title %}{{ news.title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <article>
        <h1>{{ news.title }}</h1>
        
        <div class="text-muted mb-3">
            <small>
                <i class="bi bi-person"></i> {{ news.author.get_full_name }}
                <i class="bi bi-calendar ms-3"></i> {{ news.publish_time|date:"d.m.Y H:i" }}
                <i class="bi bi-folder ms-3"></i> {{ news.category.name }}
                <!-- Izohlar soni -->
                <i class="bi bi-chat-dots ms-3"></i> {{ comments_count }} ta izoh
            </small>
        </div>
        
        {% if news.photo %}
            <img src="{{ news.photo.url }}" class="img-fluid mb-3" alt="{{ news.title }}">
        {% endif %}
        
        <div class="news-body">
            {{ news.body|safe }}
        </div>
    </article>
    
    <hr class="my-5">
    
    <!-- IZOHLAR QISMI SHU YERDA BO'LADI -->
    
</div>
{% endblock %}
```

### Tushuntirish:
- `comments_count` - ViewsDA `get_context_data` metodida qo'shgan o'zgaruvchi
- Bootstrap Icons (`bi-chat-dots`) - chiroyli ikonka
- `<hr>` - ajratuvchi chiziq

---

## 3. Izoh qoldirish formasini qo'shish

### 3.1. Oddiy forma

```html
<!-- IZOHLAR BO'LIMI -->
<div class="comments-section">
    <h3 class="mb-4">Izohlar ({{ comments_count }})</h3>
    
    <!-- IZOH QOLDIRISH FORMASI -->
    {% if user.is_authenticated %}
        <div class="card mb-4">
            <div class="card-body">
                <h5 class="card-title">Izoh qoldirish</h5>
                <form method="post">
                    {% csrf_token %}
                    {{ comment_form.as_p }}
                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-send"></i> Yuborish
                    </button>
                </form>
            </div>
        </div>
    {% else %}
        <div class="alert alert-info">
            Izoh qoldirish uchun 
            <a href="{% url 'login' %}?next={{ request.path }}">tizimga kiring</a> 
            yoki 
            <a href="{% url 'signup' %}">ro'yxatdan o'ting</a>.
        </div>
    {% endif %}
</div>
```

### 3.2. Kod tushuntirilishi

#### a) Foydalanuvchi tekshiruvi
```html
{% if user.is_authenticated %}
    <!-- Forma -->
{% else %}
    <!-- Login taklifi -->
{% endif %}
```

Bu yerda:
- `user.is_authenticated` - foydalanuvchi tizimga kirganmi?
- Agar kirmagan bo'lsa - login sahifasiga havola beramiz
- `?next={{ request.path }}` - login qilgandan keyin qaytib kelish uchun

#### b) Form elementlari
```html
<form method="post">
    {% csrf_token %}
    {{ comment_form.as_p }}
    <button type="submit">Yuborish</button>
</form>
```

- `{% csrf_token %}` - xavfsizlik uchun
- `{{ comment_form.as_p }}` - formani paragraf ko'rinishida
- `as_p` - har bir field `<p>` tegida

---

## 4. Formani chiroyliroq qilish

### 4.1. Django Crispy Forms bilan (tavsiya etiladi)

Dastlab o'rnatish:
```bash
pip install django-crispy-forms crispy-bootstrap5
```

Settings.py ga qo'shish:
```python
# settings.py
INSTALLED_APPS = [
    # ...
    'crispy_forms',
    'crispy_bootstrap5',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

Template'da ishlatish:
```html
{% load crispy_forms_tags %}

<form method="post">
    {% csrf_token %}
    {{ comment_form|crispy }}
    <button type="submit" class="btn btn-primary">
        <i class="bi bi-send"></i> Yuborish
    </button>
</form>
```

### 4.2. Qo'lda formani chiroyli qilish (crispy forms'siz)

```html
<form method="post">
    {% csrf_token %}
    
    <!-- Formadagi xatolarni ko'rsatish -->
    {% if comment_form.errors %}
        <div class="alert alert-danger">
            <strong>Xatoliklar:</strong>
            <ul class="mb-0">
                {% for field in comment_form %}
                    {% for error in field.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                {% endfor %}
            </ul>
        </div>
    {% endif %}
    
    <div class="mb-3">
        <label for="{{ comment_form.body.id_for_label }}" class="form-label">
            {{ comment_form.body.label }}
        </label>
        {{ comment_form.body }}
        {% if comment_form.body.help_text %}
            <div class="form-text">{{ comment_form.body.help_text }}</div>
        {% endif %}
    </div>
    
    <button type="submit" class="btn btn-primary">
        <i class="bi bi-send"></i> Yuborish
    </button>
</form>
```

### 4.3. Kod tushuntirilishi

#### Xatolarni ko'rsatish
```html
{% if comment_form.errors %}
    <div class="alert alert-danger">
        {% for field in comment_form %}
            {% for error in field.errors %}
                <li>{{ error }}</li>
            {% endfor %}
        {% endfor %}
    </div>
{% endif %}
```

Bu kod:
- Barcha form xatolarini aylanadi
- Har bir xatoni `<li>` da ko'rsatadi
- Bootstrap `alert-danger` classi bilan qizil rangda

---

## 5. Izohlar ro'yxatini ko'rsatish

### 5.1. Oddiy ro'yxat

```html
<!-- IZOHLAR RO'YXATI -->
<div class="comments-list mt-5">
    <h4 class="mb-4">Barcha izohlar</h4>
    
    {% if comments %}
        {% for comment in comments %}
            <div class="card mb-3">
                <div class="card-body">
                    <div class="d-flex align-items-start">
                        <!-- Foydalanuvchi rasmi -->
                        <div class="me-3">
                            {% if comment.user.profile.photo %}
                                <img src="{{ comment.user.profile.photo.url }}" 
                                     class="rounded-circle" 
                                     width="50" height="50"
                                     alt="{{ comment.user.username }}">
                            {% else %}
                                <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" 
                                     style="width: 50px; height: 50px;">
                                    <span class="fs-5">{{ comment.user.username|first|upper }}</span>
                                </div>
                            {% endif %}
                        </div>
                        
                        <!-- Izoh matni -->
                        <div class="flex-grow-1">
                            <h6 class="mb-1">
                                {{ comment.user.get_full_name|default:comment.user.username }}
                            </h6>
                            <small class="text-muted">
                                <i class="bi bi-clock"></i> 
                                {{ comment.created_at|timesince }} oldin
                            </small>
                            <p class="mt-2 mb-0">{{ comment.body|linebreaks }}</p>
                        </div>
                    </div>
                </div>
            </div>
        {% endfor %}
    {% else %}
        <div class="alert alert-info">
            <i class="bi bi-info-circle"></i> 
            Hali hech kim izoh qoldirmagan. Birinchi bo'ling!
        </div>
    {% endif %}
</div>
```

### 5.2. Kod tushuntirilishi

#### a) Foydalanuvchi rasmi
```html
{% if comment.user.profile.photo %}
    <img src="{{ comment.user.profile.photo.url }}" 
         class="rounded-circle" 
         width="50" height="50">
{% else %}
    <!-- Avatar harfi -->
    <div class="rounded-circle bg-secondary">
        <span>{{ comment.user.username|first|upper }}</span>
    </div>
{% endif %}
```

- Agar rasm bo'lsa - rasmni ko'rsatadi
- Yo'q bo'lsa - ismning birinchi harfini ko'rsatadi
- `rounded-circle` - doira shakli

#### b) Vaqtni ko'rsatish
```html
{{ comment.created_at|timesince }} oldin
```

- `timesince` - necha vaqt o'tganini ko'rsatadi
- Masalan: "5 daqiqa oldin", "2 soat oldin"

#### c) Matnni formatlash
```html
{{ comment.body|linebreaks }}
```

- `linebreaks` - matnda yangi qatorlarni `<br>` ga o'zgartiradi
- HTML teglarni avtomatik escape qiladi (XSS dan himoya)

---

## 6. Izohlarni tahrirlash va o'chirish tugmalari

Agar foydalanuvchi o'z izohini ko'rayotgan bo'lsa, tahrirlash va o'chirish tugmalarini ko'rsatamiz:

```html
{% for comment in comments %}
    <div class="card mb-3">
        <div class="card-body">
            <div class="d-flex align-items-start">
                <!-- Avatar -->
                <div class="me-3">
                    {% if comment.user.profile.photo %}
                        <img src="{{ comment.user.profile.photo.url }}" 
                             class="rounded-circle" 
                             width="50" height="50">
                    {% else %}
                        <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" 
                             style="width: 50px; height: 50px;">
                            <span class="fs-5">{{ comment.user.username|first|upper }}</span>
                        </div>
                    {% endif %}
                </div>
                
                <!-- Izoh matni -->
                <div class="flex-grow-1">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h6 class="mb-1">
                                {{ comment.user.get_full_name|default:comment.user.username }}
                                {% if comment.user == news.author %}
                                    <span class="badge bg-primary">Muallif</span>
                                {% endif %}
                            </h6>
                            <small class="text-muted">
                                <i class="bi bi-clock"></i> 
                                {{ comment.created_at|timesince }} oldin
                            </small>
                        </div>
                        
                        <!-- Tahrirlash tugmalari -->
                        {% if comment.user == user %}
                            <div class="dropdown">
                                <button class="btn btn-sm btn-link text-muted" 
                                        type="button" 
                                        data-bs-toggle="dropdown">
                                    <i class="bi bi-three-dots-vertical"></i>
                                </button>
                                <ul class="dropdown-menu">
                                    <li>
                                        <a class="dropdown-item" 
                                           href="{% url 'edit_comment' comment.pk %}">
                                            <i class="bi bi-pencil"></i> Tahrirlash
                                        </a>
                                    </li>
                                    <li>
                                        <a class="dropdown-item text-danger" 
                                           href="{% url 'delete_comment' comment.pk %}">
                                            <i class="bi bi-trash"></i> O'chirish
                                        </a>
                                    </li>
                                </ul>
                            </div>
                        {% endif %}
                    </div>
                    
                    <p class="mt-2 mb-0">{{ comment.body|linebreaks }}</p>
                </div>
            </div>
        </div>
    </div>
{% endfor %}
```

### Tushuntirish:

#### Muallif belgisi
```html
{% if comment.user == news.author %}
    <span class="badge bg-primary">Muallif</span>
{% endif %}
```
- Agar izoh yozuvchi yangilik muallifi bo'lsa, "Muallif" belgisi ko'rsatiladi

#### Dropdown menyu
```html
{% if comment.user == user %}
    <div class="dropdown">
        <button data-bs-toggle="dropdown">...</button>
        <ul class="dropdown-menu">
            <li><a href="{% url 'edit_comment' comment.pk %}">Tahrirlash</a></li>
            <li><a href="{% url 'delete_comment' comment.pk %}">O'chirish</a></li>
        </ul>
    </div>
{% endif %}
```
- Faqat o'z izohida ko'rinadi
- Bootstrap dropdown komponenti
- Uchta nuqta tugmasi

---

## 7. To'liq template kodi

Endi barcha qismlarni birlashtirgan to'liq template:

```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block title %}{{ news.title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- YANGILIK QISMI -->
    <article class="mb-5">
        <h1 class="mb-3">{{ news.title }}</h1>
        
        <div class="text-muted mb-3">
            <small>
                <i class="bi bi-person"></i> {{ news.author.get_full_name }}
                <i class="bi bi-calendar ms-3"></i> {{ news.publish_time|date:"d.m.Y H:i" }}
                <i class="bi bi-folder ms-3"></i> {{ news.category.name }}
                <i class="bi bi-chat-dots ms-3"></i> {{ comments_count }} ta izoh
            </small>
        </div>
        
        {% if news.photo %}
            <img src="{{ news.photo.url }}" 
                 class="img-fluid rounded mb-4" 
                 alt="{{ news.title }}">
        {% endif %}
        
        <div class="news-body">
            {{ news.body|safe }}
        </div>
    </article>
    
    <hr class="my-5">
    
    <!-- IZOHLAR BO'LIMI -->
    <div class="comments-section">
        <h3 class="mb-4">
            <i class="bi bi-chat-dots"></i> 
            Izohlar ({{ comments_count }})
        </h3>
        
        <!-- IZOH QOLDIRISH FORMASI -->
        {% if user.is_authenticated %}
            <div class="card mb-5 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title mb-3">
                        <i class="bi bi-pencil-square"></i> 
                        Izoh qoldirish
                    </h5>
                    <form method="post">
                        {% csrf_token %}
                        {{ comment_form|crispy }}
                        <button type="submit" class="btn btn-primary">
                            <i class="bi bi-send"></i> Yuborish
                        </button>
                    </form>
                </div>
            </div>
        {% else %}
            <div class="alert alert-info">
                <i class="bi bi-info-circle"></i> 
                Izoh qoldirish uchun 
                <a href="{% url 'login' %}?next={{ request.path }}" class="alert-link">
                    tizimga kiring
                </a> 
                yoki 
                <a href="{% url 'signup' %}" class="alert-link">
                    ro'yxatdan o'ting
                </a>.
            </div>
        {% endif %}
        
        <!-- IZOHLAR RO'YXATI -->
        <div class="comments-list mt-5">
            {% if comments %}
                {% for comment in comments %}
                    <div class="card mb-3 shadow-sm">
                        <div class="card-body">
                            <div class="d-flex align-items-start">
                                <!-- Avatar -->
                                <div class="me-3">
                                    {% if comment.user.profile.photo %}
                                        <img src="{{ comment.user.profile.photo.url }}" 
                                             class="rounded-circle" 
                                             width="50" 
                                             height="50"
                                             alt="{{ comment.user.username }}">
                                    {% else %}
                                        <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" 
                                             style="width: 50px; height: 50px;">
                                            <span class="fs-5 fw-bold">
                                                {{ comment.user.username|first|upper }}
                                            </span>
                                        </div>
                                    {% endif %}
                                </div>
                                
                                <!-- Izoh matni -->
                                <div class="flex-grow-1">
                                    <div class="d-flex justify-content-between align-items-start">
                                        <div>
                                            <h6 class="mb-1">
                                                {{ comment.user.get_full_name|default:comment.user.username }}
                                                {% if comment.user == news.author %}
                                                    <span class="badge bg-primary">Muallif</span>
                                                {% endif %}
                                            </h6>
                                            <small class="text-muted">
                                                <i class="bi bi-clock"></i> 
                                                {{ comment.created_at|timesince }} oldin
                                            </small>
                                        </div>
                                        
                                        <!-- Tahrirlash tugmalari -->
                                        {% if comment.user == user %}
                                            <div class="dropdown">
                                                <button class="btn btn-sm btn-link text-muted" 
                                                        type="button" 
                                                        data-bs-toggle="dropdown"
                                                        aria-expanded="false">
                                                    <i class="bi bi-three-dots-vertical"></i>
                                                </button>
                                                <ul class="dropdown-menu dropdown-menu-end">
                                                    <li>
                                                        <a class="dropdown-item" 
                                                           href="{% url 'edit_comment' comment.pk %}">
                                                            <i class="bi bi-pencil"></i> Tahrirlash
                                                        </a>
                                                    </li>
                                                    <li><hr class="dropdown-divider"></li>
                                                    <li>
                                                        <a class="dropdown-item text-danger" 
                                                           href="{% url 'delete_comment' comment.pk %}">
                                                            <i class="bi bi-trash"></i> O'chirish
                                                        </a>
                                                    </li>
                                                </ul>
                                            </div>
                                        {% endif %}
                                    </div>
                                    
                                    <p class="mt-2 mb-0">{{ comment.body|linebreaks }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            {% else %}
                <div class="alert alert-light border text-center py-5">
                    <i class="bi bi-chat-dots fs-1 text-muted d-block mb-3"></i>
                    <p class="mb-0 text-muted">
                        Hali hech kim izoh qoldirmagan. Birinchi bo'ling!
                    </p>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
```

---

## 8. Qo'shimcha funksiyalar

### 8.1. Javob berish tugmasi (Reply)

Har bir izohga javob berish imkoniyatini qo'shamiz:

```html
<p class="mt-2 mb-2">{{ comment.body|linebreaks }}</p>

<!-- Javob berish tugmasi -->
<button class="btn btn-sm btn-outline-secondary" 
        type="button"
        data-bs-toggle="collapse" 
        data-bs-target="#reply-{{ comment.pk }}">
    <i class="bi bi-reply"></i> Javob berish
</button>

<!-- Javob formasi (yashirin) -->
<div class="collapse mt-3" id="reply-{{ comment.pk }}">
    <form method="post" action="{% url 'add_comment' news.pk %}">
        {% csrf_token %}
        <input type="hidden" name="parent" value="{{ comment.pk }}">
        <div class="mb-2">
            <textarea name="body" 
                      class="form-control form-control-sm" 
                      rows="2" 
                      placeholder="Javob yozing..."></textarea>
        </div>
        <button type="submit" class="btn btn-sm btn-primary">
            <i class="bi bi-send"></i> Yuborish
        </button>
    </form>
</div>
```

### 8.2. Like/Dislike tugmalari

```html
<div class="mt-2">
    <button class="btn btn-sm btn-outline-primary" 
            onclick="likeComment({{ comment.pk }})">
        <i class="bi bi-hand-thumbs-up"></i> 
        <span id="likes-{{ comment.pk }}">{{ comment.likes_count }}</span>
    </button>
    <button class="btn btn-sm btn-outline-danger ms-2" 
            onclick="dislikeComment({{ comment.pk }})">
        <i class="bi bi-hand-thumbs-down"></i>
        <span id="dislikes-{{ comment.pk }}">{{ comment.dislikes_count }}</span>
    </button>
</div>

<script>
function likeComment(commentId) {
    fetch(`/comments/${commentId}/like/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById(`likes-${commentId}`).textContent = data.likes;
    });
}
</script>
```

### 8.3. Izohlarni sahifalash (Pagination)

Agar izohlar ko'p bo'lsa, sahifalash qo'shish kerak:

**views.py:**
```python
from django.core.paginator import Paginator

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Barcha izohlar
    comments = self.object.comments.filter(active=True).order_by('-created_at')
    
    # Sahifalash
    paginator = Paginator(comments, 10)  # Har sahifada 10 ta
    page_number = self.request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['comments'] = page_obj
    context['comments_count'] = comments.count()
    context['comment_form'] = CommentForm()
    
    return context
```

**Template:**
```html
<!-- Izohlar ro'yxati -->
{% for comment in comments %}
    <!-- ... -->
{% endfor %}

<!-- Pagination -->
{% if comments.has_other_pages %}
    <nav aria-label="Comments pagination">
        <ul class="pagination justify-content-center mt-4">
            {% if comments.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1">Birinchi</a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ comments.previous_page_number }}">
                        Oldingi
                    </a>
                </li>
            {% endif %}
            
            <li class="page-item active">
                <span class="page-link">
                    {{ comments.number }} / {{ comments.paginator.num_pages }}
                </span>
            </li>
            
            {% if comments.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ comments.next_page_number }}">
                        Keyingi
                    </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ comments.paginator.num_pages }}">
                        Oxirgi
                    </a>
                </li>
            {% endif %}
        </ul>
    </nav>
{% endif %}
```

---

## 9. Custom template tags yaratish

Izohlar uchun maxsus template tag yaratamiz.

### 9.1. Templatetags katalogini yaratish

```
news/
├── templatetags/
│   ├── __init__.py
│   └── comment_tags.py
```

### 9.2. comment_tags.py

```python
# news/templatetags/comment_tags.py
from django import template
from django.utils.timesince import timesince
from django.utils import timezone

register = template.Library()

@register.filter
def time_ago(date):
    """Vaqtni 'oldin' shaklida qaytaradi"""
    if not date:
        return ''
    
    now = timezone.now()
    diff = now - date
    
    if diff.days == 0:
        if diff.seconds < 60:
            return 'Hozirgina'
        elif diff.seconds < 3600:
            minutes = diff.seconds // 60
            return f'{minutes} daqiqa oldin'
        else:
            hours = diff.seconds // 3600
            return f'{hours} soat oldin'
    elif diff.days == 1:
        return 'Kecha'
    elif diff.days < 7:
        return f'{diff.days} kun oldin'
    else:
        return date.strftime('%d.%m.%Y')

@register.simple_tag
def get_comment_class(comment, user):
    """Izoh uchun CSS class qaytaradi"""
    if comment.user == user:
        return 'border-primary'
    return ''

@register.inclusion_tag('news/comment_item.html')
def render_comment(comment, user, news):
    """Bitta izohni render qiladi"""
    return {
        'comment': comment,
        'user': user,
        'news': news,
    }
```

### 9.3. Template'da ishlatish

```html
{% load comment_tags %}

<!-- Time ago filter -->
{{ comment.created_at|time_ago }}

<!-- CSS class -->
<div class="card {{ comment|get_comment_class:user }}">
    ...
</div>

<!-- Inclusion tag -->
{% render_comment comment user news %}
```

---

## 10. Mobile responsive dizayn

Mobile qurilmalar uchun moslashuvchan dizayn:

```html
{% block extra_css %}
<style>
/* Mobile uchun optimizatsiya */
@media (max-width: 768px) {
    .comments-section h3 {
        font-size: 1.5rem;
    }
    
    .card-body {
        padding: 1rem;
    }
    
    /* Avatar kichikroq */
    .comments-list .rounded-circle {
        width: 40px !important;
        height: 40px !important;
    }
    
    /* Izoh matni */
    .comments-list .card-body p {
        font-size: 0.9rem;
    }
    
    /* Dropdown tugma */
    .dropdown-toggle {
        padding: 0.25rem;
    }
    
    /* Form */
    .comment-form textarea {
        font-size: 0.9rem;
    }
}

/* Qorong'u rejim uchun */
@media (prefers-color-scheme: dark) {
    .card {
        background-color: #2d3748;
        border-color: #4a5568;
        color: #e2e8f0;
    }
    
    .text-muted {
        color: #a0aec0 !important;
    }
}
</style>
{% endblock %}
```

### Template'da responsive classlar:

```html
<!-- Desktop va mobile uchun turli xil ko'rinish -->
<div class="d-none d-md-flex align-items-start">
    <!-- Desktop versiya -->
    <div class="me-3">
        <img src="..." width="50" height="50">
    </div>
    <div class="flex-grow-1">
        <!-- Izoh matni -->
    </div>
</div>

<div class="d-flex d-md-none flex-column">
    <!-- Mobile versiya -->
    <div class="d-flex align-items-center mb-2">
        <img src="..." width="40" height="40" class="me-2">
        <h6 class="mb-0">{{ comment.user.username }}</h6>
    </div>
    <p>{{ comment.body }}</p>
</div>
```

---

## 11. JavaScript bilan interaktivlik

### 11.1. Real-time izoh qo'shish (AJAX bilan)

**Template:**
```html
<form id="comment-form" method="post">
    {% csrf_token %}
    {{ comment_form|crispy }}
    <button type="submit" class="btn btn-primary">
        <span class="spinner-border spinner-border-sm d-none" id="submit-spinner"></span>
        <span id="submit-text">Yuborish</span>
    </button>
</form>

<script>
document.getElementById('comment-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const form = this;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"]');
    const spinner = document.getElementById('submit-spinner');
    const submitText = document.getElementById('submit-text');
    
    // Loading holatini ko'rsatish
    spinner.classList.remove('d-none');
    submitText.textContent = 'Yuklanmoqda...';
    submitBtn.disabled = true;
    
    fetch(form.action || window.location.href, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Formani tozalash
            form.reset();
            
            // Yangi izohni qo'shish
            const commentsList = document.querySelector('.comments-list');
            const newComment = createCommentElement(data.comment);
            commentsList.insertBefore(newComment, commentsList.firstChild);
            
            // Success xabari
            showMessage('success', 'Izohingiz qo\'shildi!');
            
            // Izohlar sonini yangilash
            updateCommentsCount(data.comments_count);
        } else {
            showMessage('danger', 'Xatolik yuz berdi!');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showMessage('danger', 'Xatolik yuz berdi!');
    })
    .finally(() => {
        // Loading holatini o'chirish
        spinner.classList.add('d-none');
        submitText.textContent = 'Yuborish';
        submitBtn.disabled = false;
    });
});

function createCommentElement(comment) {
    const div = document.createElement('div');
    div.className = 'card mb-3 shadow-sm';
    div.innerHTML = `
        <div class="card-body">
            <div class="d-flex align-items-start">
                <div class="me-3">
                    <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" 
                         style="width: 50px; height: 50px;">
                        <span class="fs-5 fw-bold">${comment.user.username.charAt(0).toUpperCase()}</span>
                    </div>
                </div>
                <div class="flex-grow-1">
                    <h6 class="mb-1">${comment.user.full_name || comment.user.username}</h6>
                    <small class="text-muted">
                        <i class="bi bi-clock"></i> Hozirgina
                    </small>
                    <p class="mt-2 mb-0">${comment.body}</p>
                </div>
            </div>
        </div>
    `;
    return div;
}

function showMessage(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // 5 sekunddan keyin o'chirish
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function updateCommentsCount(count) {
    document.querySelectorAll('.comments-count').forEach(el => {
        el.textContent = `${count} ta izoh`;
    });
}
</script>
```

**Views.py (JSON response):**
```python
from django.http import JsonResponse

def post(self, request, *args, **kwargs):
    # AJAX so'rov ekanligini tekshirish
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # ... autentifikatsiya va validatsiya
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.news = self.object
        comment.user = request.user
        comment.save()
        
        if is_ajax:
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.pk,
                    'body': comment.body,
                    'user': {
                        'username': comment.user.username,
                        'full_name': comment.user.get_full_name(),
                    },
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                },
                'comments_count': self.object.comments.filter(active=True).count(),
            })
        
        messages.success(request, "Izohingiz qo'shildi!")
        return redirect('news_detail', pk=self.object.pk)
    
    if is_ajax:
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)
    
    # ... oddiy response
```

### 11.2. Izohni o'chirish (confirmation)

```html
<a href="#" 
   class="dropdown-item text-danger" 
   onclick="confirmDelete(event, {{ comment.pk }})">
    <i class="bi bi-trash"></i> O'chirish
</a>

<script>
function confirmDelete(event, commentId) {
    event.preventDefault();
    
    if (confirm('Izohni o\'chirmoqchimisiz?')) {
        fetch(`/comments/${commentId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Izohni DOM dan o'chirish
                document.querySelector(`#comment-${commentId}`).remove();
                showMessage('success', 'Izoh o\'chirildi!');
                updateCommentsCount(data.comments_count);
            }
        });
    }
}
</script>
```

---

## 12. Xavfsizlik va best practices

### 12.1. XSS (Cross-Site Scripting) dan himoya

**Template'da:**
```html
<!-- XATO: HTML teglarni qabul qiladi -->
{{ comment.body|safe }}

<!-- TO'G'RI: Avtomatik escape qiladi -->
{{ comment.body|linebreaks }}

<!-- Yoki faqat ruxsat etilgan teglar -->
{{ comment.body|escape|urlize|linebreaks }}
```

**Model'da:**
```python
from django.utils.html import escape

class Comment(models.Model):
    # ...
    
    def save(self, *args, **kwargs):
        # HTML teglarni olib tashlash
        self.body = escape(self.body)
        super().save(*args, **kwargs)
```

### 12.2. CSRF himoyasi

```html
<!-- Har bir forma uchun -->
<form method="post">
    {% csrf_token %}
    <!-- ... -->
</form>

<!-- AJAX so'rovlarda -->
<script>
fetch(url, {
    method: 'POST',
    headers: {
        'X-CSRFToken': getCookie('csrftoken'),
    }
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
</script>
```

### 12.3. Rate limiting (frontend)

```html
<script>
let lastCommentTime = 0;
const RATE_LIMIT_SECONDS = 60;

document.getElementById('comment-form').addEventListener('submit', function(e) {
    const now = Date.now();
    const timeSinceLastComment = (now - lastCommentTime) / 1000;
    
    if (timeSinceLastComment < RATE_LIMIT_SECONDS) {
        e.preventDefault();
        const remainingTime = Math.ceil(RATE_LIMIT_SECONDS - timeSinceLastComment);
        showMessage('warning', `Iltimos, ${remainingTime} sekund kutib turing.`);
        return;
    }
    
    lastCommentTime = now;
});
</script>
```

---

## 13. SEO optimizatsiya

### 13.1. Structured data (Schema.org)

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ news.title }}",
  "datePublished": "{{ news.publish_time|date:'c' }}",
  "author": {
    "@type": "Person",
    "name": "{{ news.author.get_full_name }}"
  },
  "commentCount": {{ comments_count }},
  "comment": [
    {% for comment in comments %}
    {
      "@type": "Comment",
      "text": "{{ comment.body|escape }}",
      "dateCreated": "{{ comment.created_at|date:'c' }}",
      "author": {
        "@type": "Person",
        "name": "{{ comment.user.get_full_name|default:comment.user.username }}"
      }
    }{% if not forloop.last %},{% endif %}
    {% endfor %}
  ]
}
</script>
```

### 13.2. Meta teglar

```html
{% block meta %}
<meta name="description" content="{{ news.title }} - {{ comments_count }} ta izoh">
<meta property="og:title" content="{{ news.title }}">
<meta property="og:description" content="{{ news.body|striptags|truncatewords:30 }}">
<meta property="og:type" content="article">
<meta property="og:url" content="{{ request.build_absolute_uri }}">
{% if news.photo %}
<meta property="og:image" content="{{ request.scheme }}://{{ request.get_host }}{{ news.photo.url }}">
{% endif %}
{% endblock %}
```

---

## 14. Accessibility (A11y)

### 14.1. ARIA atributlari

```html
<!-- Forma -->
<form method="post" aria-label="Izoh qoldirish formasi">
    {% csrf_token %}
    <label for="id_body" class="form-label">Izohingiz</label>
    <textarea id="id_body" 
              name="body" 
              class="form-control"
              aria-describedby="bodyHelp"
              aria-required="true"></textarea>
    <small id="bodyHelp" class="form-text">
        Kamida 10 ta belgi kiriting
    </small>
    <button type="submit" aria-label="Izohni yuborish">
        Yuborish
    </button>
</form>

<!-- Izohlar ro'yxati -->
<section aria-label="Izohlar ro'yxati">
    {% for comment in comments %}
        <article class="card mb-3" aria-label="Izoh: {{ comment.user.username }}">
            <!-- ... -->
        </article>
    {% endfor %}
</section>
```

### 14.2. Keyboard navigation

```html
<style>
/* Focus holatlarini ko'rsatish */
.btn:focus,
.form-control:focus {
    outline: 2px solid #0d6efd;
    outline-offset: 2px;
}

/* Skip to comments link */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #0d6efd;
    color: white;
    padding: 8px;
    text-decoration: none;
    z-index: 100;
}

.skip-link:focus {
    top: 0;
}
</style>

<a href="#comments" class="skip-link">Izohlarga o'tish</a>

<section id="comments" tabindex="-1">
    <!-- Izohlar -->
</section>
```

---

## 15. Performance optimizatsiya

### 15.1. Lazy loading images

```html
{% if comment.user.profile.photo %}
    <img src="{{ comment.user.profile.photo.url }}" 
         class="rounded-circle" 
         width="50" 
         height="50"
         loading="lazy"
         alt="{{ comment.user.username }}">
{% endif %}
```

### 15.2. Izohlarni async yuklash

```html
<div id="comments-container">
    <div class="text-center">
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Yuklanmoqda...</span>
        </div>
    </div>
</div>

<script>
// Sahifa yuklangandan keyin izohlarni yuklash
document.addEventListener('DOMContentLoaded', function() {
    fetch('{% url "load_comments" news.pk %}')
        .then(response => response.text())
        .then(html => {
            document.getElementById('comments-container').innerHTML = html;
        });
});
</script>
```

**views.py:**
```python
from django.template.loader import render_to_string

def load_comments(request, pk):
    news = get_object_or_404(News, pk=pk)
    comments = news.comments.filter(active=True).order_by('-created_at')[:10]
    
    html = render_to_string('news/comments_list.html', {
        'comments': comments,
        'user': request.user,
        'news': news,
    })
    
    return HttpResponse(html)
```

---

## 16. Testing template

### 16.1. Template tag testlari

```python
# news/tests/test_template_tags.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from news.templatetags.comment_tags import time_ago
from news.models import News, Comment

class CommentTagsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', password='test')
        self.news = News.objects.create(title='Test', body='Test')
    
    def test_time_ago_just_now(self):
        comment = Comment.objects.create(
            news=self.news,
            user=self.user,
            body='Test'
        )
        result = time_ago(comment.created_at)
        self.assertEqual(result, 'Hozirgina')
    
    def test_time_ago_minutes(self):
        time = timezone.now() - timedelta(minutes=5)
        result = time_ago(time)
        self.assertEqual(result, '5 daqiqa oldin')
```

### 16.2. Template rendering testi

```python
# news/tests/test_templates.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from news.models import News, Comment

class CommentTemplateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('test', password='test')
        self.news = News.objects.create(title='Test', body='Test')
    
    def test_comment_form_visible_for_authenticated(self):
        self.client.login(username='test', password='test')
        response = self.client.get(f'/news/{self.news.pk}/')
        self.assertContains(response, 'Izoh qoldirish')
        self.assertContains(response, 'csrf_token')
    
    def test_comment_form_hidden_for_anonymous(self):
        response = self.client.get(f'/news/{self.news.pk}/')
        self.assertContains(response, 'tizimga kiring')
        self.assertNotContains(response, 'Izoh qoldirish')
    
    def test_comments_list_displayed(self):
        Comment.objects.create(
            news=self.news,
            user=self.user,
            body='Test comment'
        )
        response = self.client.get(f'/news/{self.news.pk}/')
        self.assertContains(response, 'Test comment')
```

---

## 17. Best Practices

### ✅ 1. Template tuzilishi

```
templates/
├── base.html
├── news/
│   ├── news_detail.html          # Asosiy sahifa
│   ├── includes/
│   │   ├── comment_form.html     # Forma qismi
│   │   ├── comment_item.html     # Bitta izoh
│   │   └── comments_list.html    # Izohlar ro'yxati
```

**Foydalanish:**
```html
<!-- news_detail.html -->
{% include 'news/includes/comment_form.html' %}
{% include 'news/includes/comments_list.html' %}
```

### ✅ 2. CSS classlarni to'g'ri nomlash

```html
<!-- BEM (Block Element Modifier) metodologiyasi -->
<div class="comment">
    <div class="comment__header">
        <img class="comment__avatar" src="...">
        <h6 class="comment__author">...</h6>
    </div>
    <div class="comment__body">...</div>
    <div class="comment__footer">
        <button class="comment__action comment__action--like">Like</button>
    </div>
</div>
```

### ✅ 3. JavaScript'ni alohida faylda saqlash

```html
{% block extra_js %}
<script src="{% static 'js/comments.js' %}"></script>
{% endblock %}
```

### ✅ 4. Loading states

```html
<button type="submit" class="btn btn-primary" id="submit-btn">
    <span class="spinner-border spinner-border-sm d-none"></span>
    <span class="btn-text">Yuborish</span>
</button>

<script>
const btn = document.getElementById('submit-btn');
const spinner = btn.querySelector('.spinner-border');
const text = btn.querySelector('.btn-text');

// Loading holatiga o'tish
function setLoading(isLoading) {
    if (isLoading) {
        spinner.classList.remove('d-none');
        text.textContent = 'Yuklanmoqda...';
        btn.disabled = true;
    } else {
        spinner.classList.add('d-none');
        text.textContent = 'Yuborish';
        btn.disabled = false;
    }
}
</script>
```

### ✅ 5. Error handling

```html
{% if comment_form.errors %}
    <div class="alert alert-danger alert-dismissible">
        <strong>Xatolar:</strong>
        <ul class="mb-0">
            {% for field, errors in comment_form.errors.items %}
                {% for error in errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            {% endfor %}
        </ul>
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
{% endif %}
```

---

## Xulosa

Bu darsda biz:
- ✅ Izoh qoldirish formasini template'da yaratdik
- ✅ Izohlar ro'yxatini chiroyli qilib chiqardik
- ✅ Bootstrap bilan responsive dizayn qildik
- ✅ JavaScript bilan interaktivlik qo'shdik
- ✅ Xavfsizlik va accessibility'ga e'tibor berdik
- ✅ Performance optimizatsiya qildik
- ✅ Best practices bilan tanishdik

Keyingi darsda **yangiliklarni izlash funksiyasini** yaratamiz!

---

## Qo'shimcha o'qish uchun

- Bootstrap Components: https://getbootstrap.com/docs/5.3/components/
- Django Templates: https://docs.djangoproject.com/en/4.2/topics/templates/
- ARIA: https://www.w3.org/WAI/ARIA/apg/
- Web Accessibility: https://www.w3.org/WAI/fundamentals/accessibility-intro/