# Lesson 45: Practice - Django'da izoh qoldirish. Template qismini yozish

## Amaliyot maqsadi

Ushbu amaliyotda siz:
- Izoh qoldirish formasini template'da yaratishni o'rganasiz
- Izohlar ro'yxatini chiroyli ko'rinishda chiqarasiz
- Bootstrap bilan responsive dizayn qilasiz
- JavaScript yordamida interaktiv funksiyalar qo'shasiz
- Foydalanuvchi uchun qulay interfeys yaratishni o'rganasiz

---

## Boshlang'ich tayyorgarlik

### 1. Kerakli fayllar

Quyidagi fayllar tayyor bo'lishi kerak:
- ✅ `news/models.py` - Comment modeli
- ✅ `news/forms.py` - CommentForm
- ✅ `news/views.py` - NewsDetailView (post metodi bilan)
- ✅ `templates/base.html` - asosiy shablon

### 2. Bootstrap va Icons

`base.html` da Bootstrap va Bootstrap Icons mavjudligini tekshiring:

```html
<!-- templates/base.html -->
<head>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bootstrap Icons -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
</head>
<body>
    <!-- Content -->
    
    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
```

---

## Topshiriqlar

### Topshiriq 1: Asosiy template tuzilmasini yaratish ⭐

**Maqsad:** `news_detail.html` faylida izohlar bo'limi uchun joy ajratish

**1.1. Joriy template'ni ochish**

`templates/news/news_detail.html` faylini oching.

**1.2. Izohlar bo'limini qo'shish**

Yangilik matni ostiga quyidagini qo'shing:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <!-- YANGILIK QISMI -->
    <article class="mb-5">
        <h1>{{ news.title }}</h1>
        <div class="news-body">
            {{ news.body|safe }}
        </div>
    </article>
    
    <hr class="my-5">
    
    <!-- TODO: IZOHLAR BO'LIMI SHU YERDA -->
    <div class="comments-section">
        <h3>Izohlar</h3>
        <!-- Keyingi qadamlarda to'ldiramiz -->
    </div>
    
</div>
{% endblock %}
```

**1.3. Sahifani tekshirish**

Brauzerda yangilik sahifasini oching va "Izohlar" sarlavhasi ko'rinishini tekshiring.

---

### Topshiriq 2: Izohlar sonini ko'rsatish ⭐

**Maqsad:** Izohlar sonini chiroyli ko'rinishda chiqarish

**2.1. Sarlavhaga izohlar sonini qo'shish**

```html
<div class="comments-section">
    <h3 class="mb-4">
        <i class="bi bi-chat-dots"></i> 
        Izohlar ({{ comments_count }})
    </h3>
</div>
```

**2.2. Yangilik ma'lumotlarida ham ko'rsatish**

Yangilik sarlavhasi ostiga qo'shing:

```html
<div class="text-muted mb-3">
    <small>
        <i class="bi bi-person"></i> {{ news.author.get_full_name }}
        <i class="bi bi-calendar ms-3"></i> {{ news.publish_time|date:"d.m.Y H:i" }}
        <!-- TODO: Izohlar sonini qo'shing -->
    </small>
</div>
```

<details>
<summary>Yechim</summary>

```html
<i class="bi bi-chat-dots ms-3"></i> {{ comments_count }} ta izoh
```
</details>

---

### Topshiriq 3: Izoh qoldirish formasini yaratish ⭐⭐

**Maqsad:** Foydalanuvchi uchun izoh qoldirish formasi

**3.1. Foydalanuvchi autentifikatsiyasini tekshirish**

```html
<div class="comments-section">
    <h3 class="mb-4">
        <i class="bi bi-chat-dots"></i> 
        Izohlar ({{ comments_count }})
    </h3>
    
    <!-- TODO: Agar foydalanuvchi tizimga kirgan bo'lsa - forma -->
    <!-- TODO: Aks holda - login taklifi -->
</div>
```

**Topshiriq:** `{% if user.is_authenticated %}` dan foydalanib, ikki holatni yarating.

<details>
<summary>Yechim</summary>

```html
{% if user.is_authenticated %}
    <div class="card mb-5 shadow-sm">
        <div class="card-body">
            <h5 class="card-title mb-3">
                <i class="bi bi-pencil-square"></i> 
                Izoh qoldirish
            </h5>
            <!-- Forma shu yerda -->
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
```
</details>

**3.2. Formani qo'shish**

Card body ichiga qo'shing:

```html
<form method="post">
    {% csrf_token %}
    {{ comment_form.as_p }}
    <button type="submit" class="btn btn-primary">
        <i class="bi bi-send"></i> Yuborish
    </button>
</form>
```

**3.3. Tekshirish**

1. Tizimga kirmasdan - login taklifi ko'rinishi kerak
2. Tizimga kirib - forma ko'rinishi kerak
3. Formani yuborib ko'ring

---

### Topshiriq 4: Django Crispy Forms o'rnatish va ishlatish ⭐⭐

**Maqsad:** Formani chiroyliroq qilish

**4.1. O'rnatish**

Terminal'da:

```bash
pip install django-crispy-forms crispy-bootstrap5
```

**4.2. Settings.py ga qo'shish**

```python
# config/settings.py

INSTALLED_APPS = [
    # ...
    'crispy_forms',
    'crispy_bootstrap5',
]

# Crispy Forms sozlamalari
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
```

**4.3. Template'da ishlatish**

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

**4.4. Tekshirish**

Forma endi chiroyliroq va Bootstrap stilida bo'lishi kerak.

---

### Topshiriq 5: Izohlar ro'yxatini ko'rsatish ⭐⭐⭐

**Maqsad:** Barcha izohlarni chiroyli ko'rinishda chiqarish

**5.1. Bo'sh holat**

Avval izohlar yo'q holatini yaratamiz:

```html
<!-- Formadan keyin -->
<div class="comments-list mt-5">
    <h4 class="mb-4">Barcha izohlar</h4>
    
    {% if comments %}
        <!-- TODO: Izohlar ro'yxati -->
    {% else %}
        <div class="alert alert-light border text-center py-5">
            <i class="bi bi-chat-dots fs-1 text-muted d-block mb-3"></i>
            <p class="mb-0 text-muted">
                Hali hech kim izoh qoldirmagan. Birinchi bo'ling!
            </p>
        </div>
    {% endif %}
</div>
```

**5.2. Bitta izoh template'ini yaratish**

```html
{% if comments %}
    {% for comment in comments %}
        <div class="card mb-3 shadow-sm">
            <div class="card-body">
                <!-- TODO: Izoh mazmuni -->
            </div>
        </div>
    {% endfor %}
{% else %}
    <!-- ... -->
{% endif %}
```

**5.3. Izoh mazmunini to'ldirish**

**Topshiriq:** Quyidagi elementlarni qo'shing:
- Foydalanuvchi avatari (50x50)
- Foydalanuvchi ismi
- Vaqt (timesince bilan)
- Izoh matni

<details>
<summary>Yechim</summary>

```html
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
```
</details>

**5.4. Test ma'lumotlari qo'shish**

Admin paneldan yoki Django shell orqali bir nechta test izohlar qo'shing:

```python
python manage.py shell

from news.models import News, Comment
from django.contrib.auth.models import User

user = User.objects.first()
news = News.objects.first()

Comment.objects.create(
    news=news,
    user=user,
    body="Bu test izohi"
)
```

---

### Topshiriq 6: "Muallif" belgisini qo'shish ⭐⭐

**Maqsad:** Agar izoh yozuvchi yangilik muallifi bo'lsa, belgisini ko'rsatish

**6.1. Belgini qo'shish**

Foydalanuvchi ismi yoniga:

```html
<h6 class="mb-1">
    {{ comment.user.get_full_name|default:comment.user.username }}
    <!-- TODO: Agar muallif bo'lsa, badge qo'shing -->
</h6>
```

<details>
<summary>Yechim</summary>

```html
<h6 class="mb-1">
    {{ comment.user.get_full_name|default:comment.user.username }}
    {% if comment.user == news.author %}
        <span class="badge bg-primary">Muallif</span>
    {% endif %}
</h6>
```
</details>

**6.2. Tekshirish**

Yangilik muallifining izohida "Muallif" belgisi ko'rinishi kerak.

---

### Topshiriq 7: Tahrirlash va o'chirish tugmalarini qo'shish ⭐⭐⭐

**Maqsad:** Foydalanuvchi o'z izohini tahrirlashi va o'chirishi mumkin

**7.1. Dropdown menyu qo'shish**

Izoh mazmunida:

```html
<div class="d-flex justify-content-between align-items-start">
    <div>
        <h6 class="mb-1">
            {{ comment.user.get_full_name|default:comment.user.username }}
        </h6>
        <small class="text-muted">
            <i class="bi bi-clock"></i> 
            {{ comment.created_at|timesince }} oldin
        </small>
    </div>
    
    <!-- TODO: Agar o'z izohi bo'lsa, dropdown qo'shing -->
</div>

<p class="mt-2 mb-0">{{ comment.body|linebreaks }}</p>
```

**Topshiriq:** Bootstrap dropdown komponenti yarating.

<details>
<summary>Yechim</summary>

```html
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
```
</details>

**7.2. Tekshirish**

1. Boshqa foydalanuvchining izohida - tugmalar ko'rinmasligi kerak
2. O'z izohingizda - uchta nuqta tugmasi ko'rinishi kerak
3. Tugmani bosganda - menyu ochilishi kerak

---

### Topshiriq 8: Form xatolarini ko'rsatish ⭐⭐⭐

**Maqsad:** Forma xato bo'lsa, xatolarni chiroyli ko'rsatish

**8.1. Xatolar blokini qo'shish**

Forma ustiga:

```html
<form method="post">
    {% csrf_token %}
    
    <!-- Xatolarni ko'rsatish -->
    {% if comment_form.errors %}
        <div class="alert alert-danger alert-dismissible fade show" role="alert">
            <strong><i class="bi bi-exclamation-triangle"></i> Xatoliklar:</strong>
            <ul class="mb-0 mt-2">
                {% for field in comment_form %}
                    {% for error in field.errors %}
                        <li>{{ error }}</li>
                    {% endfor %}
                {% endfor %}
            </ul>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    {% endif %}
    
    {{ comment_form|crispy }}
    <button type="submit" class="btn btn-primary">
        <i class="bi bi-send"></i> Yuborish
    </button>
</form>
```

**8.2. Test qilish**

Bo'sh forma yuborib ko'ring - xato xabari ko'rinishi kerak.

---

### Topshiriq 9: Mobile responsive qilish ⭐⭐⭐

**Maqsad:** Mobil qurilmalarda ham chiroyli ko'rinishi

**9.1. Custom CSS qo'shish**

Template boshiga:

```html
{% block extra_css %}
<style>
/* Mobile optimizatsiya */
@media (max-width: 768px) {
    .comments-section h3 {
        font-size: 1.5rem;
    }
    
    .comments-list .rounded-circle {
        width: 40px !important;
        height: 40px !important;
    }
    
    .comments-list .card-body {
        padding: 0.75rem;
    }
    
    .comments-list p {
        font-size: 0.9rem;
    }
}
</style>
{% endblock %}
```

**9.2. Responsive classlardan foydalanish**

Avatar qismini yangilang:

```html
<!-- Desktop: 50x50, Mobile: 40x40 -->
<div class="me-2 me-md-3">
    {% if comment.user.profile.photo %}
        <img src="{{ comment.user.profile.photo.url }}" 
             class="rounded-circle" 
             width="50" 
             height="50"
             style="width: 40px; height: 40px;"
             alt="{{ comment.user.username }}">
    {% else %}
        <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" 
             style="width: 40px; height: 40px;">
            <span class="fs-6 fw-bold">
                {{ comment.user.username|first|upper }}
            </span>
        </div>
    {% endif %}
</div>
```

**9.3. Tekshirish**

Brauzer derazasini kichiklashtiring yoki mobil rejimda ko'ring (F12 → Device toolbar).

---

### Topshiriq 10: JavaScript interaktivlik qo'shish ⭐⭐⭐⭐

**Maqsad:** AJAX bilan izoh qo'shish (sahifa yangilanmasdan)

**10.1. Form ID qo'shish**

```html
<form method="post" id="comment-form">
    {% csrf_token %}
    {{ comment_form|crispy }}
    <button type="submit" class="btn btn-primary" id="submit-btn">
        <span class="spinner-border spinner-border-sm d-none" id="submit-spinner"></span>
        <span id="submit-text"><i class="bi bi-send"></i> Yuborish</span>
    </button>
</form>
```

**10.2. JavaScript kodi qo'shish**

Template oxirida:

```html
{% block extra_js %}
<script>
document.getElementById('comment-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const form = this;
    const formData = new FormData(form);
    const submitBtn = document.getElementById('submit-btn');
    const spinner = document.getElementById('submit-spinner');
    const submitText = document.getElementById('submit-text');
    
    // Loading holatini ko'rsatish
    spinner.classList.remove('d-none');
    submitText.innerHTML = 'Yuklanmoqda...';
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
            
            // Success xabari
            showMessage('success', 'Izohingiz qo\'shildi!');
            
            // Sahifani yangilash (vaqtinchalik)
            setTimeout(() => {
                window.location.reload();
            }, 1000);
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
        submitText.innerHTML = '<i class="bi bi-send"></i> Yuborish';
        submitBtn.disabled = false;
    });
});

function showMessage(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // 3 sekunddan keyin o'chirish
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}
</script>
{% endblock %}
```

**10.3. Views.py ni yangilash**

`news/views.py` da JSON response qo'shing:

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
                'message': 'Izohingiz qo\'shildi!',
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

**10.4. Tekshirish**

Izoh yozib, yuborib ko'ring - sahifa yangilanmay, xabar ko'rinishi kerak.

---

## Mustaqil vazifalar

### Vazifa 1: Izohlarni include bilan ajratish ⭐⭐⭐

**Maqsad:** Template kodini tartibli qilish

**Qadamlar:**

1. `templates/news/includes/` papkasini yarating
2. Quyidagi fayllarni yarating:
   - `comment_form.html` - forma qismi
   - `comment_item.html` - bitta izoh
   - `comments_list.html` - izohlar ro'yxati

3. Asosiy template'da include qiling:

```html
{% include 'news/includes/comment_form.html' %}
{% include 'news/includes/comments_list.html' %}
```

<details>
<summary>comment_item.html namunasi</summary>

```html
<!-- templates/news/includes/comment_item.html -->
<div class="card mb-3 shadow-sm">
    <div class="card-body">
        <div class="d-flex align-items-start">
            <div class="me-3">
                {% if comment.user.profile.photo %}
                    <img src="{{ comment.user.profile.photo.url }}" 
                         class="rounded-circle" 
                         width="50" height="50">
                {% else %}
                    <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" 
                         style="width: 50px; height: 50px;">
                        <span class="fs-5 fw-bold">
                            {{ comment.user.username|first|upper }}
                        </span>
                    </div>
                {% endif %}
            </div>
            
            <div class="flex-grow-1">
                <div class="d-flex justify-content-between">
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
                    
                    {% if comment.user == user %}
                        <div class="dropdown">
                            <button class="btn btn-sm btn-link text-muted" 
                                    data-bs-toggle="dropdown">
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
```

comments_list.html'da:
```html
<!-- templates/news/includes/comments_list.html -->
<div class="comments-list mt-5">
    <h4 class="mb-4">Barcha izohlar</h4>
    
    {% if comments %}
        {% for comment in comments %}
            {% include 'news/includes/comment_item.html' %}
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
```
</details>

---

### Vazifa 2: Custom template tag yaratish ⭐⭐⭐⭐

**Maqsad:** Vaqtni "oldin" shaklida ko'rsatish uchun template tag

**Qadamlar:**

1. `news/templatetags/` papkasini yarating
2. `__init__.py` va `comment_tags.py` fayllarini yarating

3. `comment_tags.py`:

```python
from django import template
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
```

4. Template'da ishlatish:

```html
{% load comment_tags %}

<small class="text-muted">
    <i class="bi bi-clock"></i> 
    {{ comment.created_at|time_ago }}
</small>
```

---

### Vazifa 3: Sahifalash (Pagination) qo'shish ⭐⭐⭐⭐

**Maqsad:** Agar izohlar ko'p bo'lsa, sahifalarga bo'lish

**Qadamlar:**

1. `views.py` da paginator qo'shing:

```python
from django.core.paginator import Paginator

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    comments = self.object.comments.filter(active=True).order_by('-created_at')
    
    # Sahifalash
    paginator = Paginator(comments, 5)  # Har sahifada 5 ta
    page_number = self.request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context['comments'] = page_obj
    context['comments_count'] = comments.count()
    context['comment_form'] = CommentForm()
    
    return context
```

2. Template'da pagination qo'shing:

```html
<!-- Izohlar ro'yxatidan keyin -->
{% if comments.has_other_pages %}
    <nav aria-label="Comments pagination">
        <ul class="pagination justify-content-center mt-4">
            {% if comments.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1">Birinchi</a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ comments.previous_page_number }}">
                        <i class="bi bi-chevron-left"></i>
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
                        <i class="bi bi-chevron-right"></i>
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

### Vazifa 4: Like/Dislike funksiyasi ⭐⭐⭐⭐⭐

**Maqsad:** Izohlarga like va dislike qo'yish

**Qadamlar:**

1. Model'ga qo'shimcha fieldlar qo'shing:

```python
# news/models.py
class Comment(models.Model):
    # ... mavjud fieldlar
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comment_dislikes', blank=True)
    
    def total_likes(self):
        return self.likes.count()
    
    def total_dislikes(self):
        return self.dislikes.count()
```

2. Migration qiling:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. View yarating:

```python
# news/views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.likes.filter(id=request.user.id).exists():
        # Agar allaqachon like bosgan bo'lsa, like ni olib tashlash
        comment.likes.remove(request.user)
        liked = False
    else:
        # Like qo'shish va dislike ni olib tashlash
        comment.likes.add(request.user)
        comment.dislikes.remove(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': comment.total_likes(),
        'dislikes_count': comment.total_dislikes(),
    })

@login_required
def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    if comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)
        disliked = False
    else:
        comment.dislikes.add(request.user)
        comment.likes.remove(request.user)
        disliked = True
    
    return JsonResponse({
        'disliked': disliked,
        'likes_count': comment.total_likes(),
        'dislikes_count': comment.total_dislikes(),
    })
```

4. URL qo'shing:

```python
# news/urls.py
urlpatterns = [
    # ...
    path('comment/<int:pk>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:pk>/dislike/', views.dislike_comment, name='dislike_comment'),
]
```

5. Template'ga tugmalar qo'shing:

```html
<div class="mt-2">
    <button class="btn btn-sm btn-outline-primary like-btn" 
            data-comment-id="{{ comment.pk }}"
            data-action="like">
        <i class="bi bi-hand-thumbs-up"></i> 
        <span class="likes-count">{{ comment.total_likes }}</span>
    </button>
    <button class="btn btn-sm btn-outline-danger ms-2 dislike-btn" 
            data-comment-id="{{ comment.pk }}"
            data-action="dislike">
        <i class="bi bi-hand-thumbs-down"></i>
        <span class="dislikes-count">{{ comment.total_dislikes }}</span>
    </button>
</div>
```

6. JavaScript qo'shing:

```html
<script>
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

document.querySelectorAll('.like-btn, .dislike-btn').forEach(button => {
    button.addEventListener('click', function() {
        const commentId = this.dataset.commentId;
        const action = this.dataset.action;
        const url = `/comment/${commentId}/${action}/`;
        
        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            // Sonlarni yangilash
            const card = this.closest('.card');
            card.querySelector('.likes-count').textContent = data.likes_count;
            card.querySelector('.dislikes-count').textContent = data.dislikes_count;
            
            // Tugma rangini o'zgartirish
            if (action === 'like') {
                this.classList.toggle('btn-primary');
                this.classList.toggle('btn-outline-primary');
            } else {
                this.classList.toggle('btn-danger');
                this.classList.toggle('btn-outline-danger');
            }
        });
    });
});
</script>
```

---

### Vazifa 5: Izohga javob berish (Reply) ⭐⭐⭐⭐⭐

**Maqsad:** Izohga izoh qoldirish (nested comments)

**Qadamlar:**

1. Model'ga parent field qo'shing:

```python
# news/models.py
class Comment(models.Model):
    # ... mavjud fieldlar
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )
    
    def get_replies(self):
        return Comment.objects.filter(parent=self, active=True).order_by('created_at')
```

2. Migration:

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Template'ga reply tugmasi qo'shing:

```html
<p class="mt-2 mb-2">{{ comment.body|linebreaks }}</p>

<button class="btn btn-sm btn-link text-muted p-0" 
        type="button"
        data-bs-toggle="collapse" 
        data-bs-target="#reply-{{ comment.pk }}">
    <i class="bi bi-reply"></i> Javob berish
</button>

<!-- Javob formasi (yashirin) -->
<div class="collapse mt-3" id="reply-{{ comment.pk }}">
    <form method="post" class="reply-form">
        {% csrf_token %}
        <input type="hidden" name="parent" value="{{ comment.pk }}">
        <div class="input-group">
            <textarea name="body" 
                      class="form-control form-control-sm" 
                      rows="2" 
                      placeholder="Javob yozing..."
                      required></textarea>
            <button type="submit" class="btn btn-primary btn-sm">
                <i class="bi bi-send"></i>
            </button>
        </div>
    </form>
</div>

<!-- Javoblarni ko'rsatish -->
{% if comment.get_replies %}
    <div class="ms-4 mt-3 border-start border-2 ps-3">
        {% for reply in comment.get_replies %}
            <div class="mb-3">
                <div class="d-flex">
                    <div class="me-2">
                        <div class="rounded-circle bg-secondary text-white d-flex align-items-center justify-content-center" 
                             style="width: 30px; height: 30px;">
                            <span class="small">{{ reply.user.username|first|upper }}</span>
                        </div>
                    </div>
                    <div class="flex-grow-1">
                        <h6 class="mb-0 small">
                            {{ reply.user.get_full_name|default:reply.user.username }}
                        </h6>
                        <small class="text-muted">{{ reply.created_at|timesince }} oldin</small>
                        <p class="mb-0 mt-1">{{ reply.body|linebreaks }}</p>
                    </div>
                </div>
            </div>
        {% endfor %}
    </div>
{% endif %}
```

4. View'ni yangilang:

```python
def post(self, request, *args, **kwargs):
    # ...
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.news = self.object
        comment.user = request.user
        
        # Parent izohni tekshirish
        parent_id = request.POST.get('parent')
        if parent_id:
            parent_comment = Comment.objects.get(pk=parent_id)
            comment.parent = parent_comment
        
        comment.save()
        # ...
```

5. Context'da faqat parent izohlarni ko'rsatish:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Faqat parent izohlar (javoblar emas)
    context['comments'] = self.object.comments.filter(
        active=True,
        parent__isnull=True
    ).order_by('-created_at')
    
    context['comments_count'] = self.object.comments.filter(active=True).count()
    context['comment_form'] = CommentForm()
    
    return context
```

---

## Tekshirish ro'yxati (Checklist)

Template to'liq ishlashini tekshiring:

### Asosiy funksiyalar
- [ ] Izohlar soni to'g'ri ko'rinadi
- [ ] Forma faqat tizimga kirgan foydalanuvchilarga ko'rinadi
- [ ] Forma yordamida izoh qo'shish mumkin
- [ ] Izohlar ro'yxati to'g'ri ko'rinadi
- [ ] Avatar yoki harf avatari ko'rinadi
- [ ] Vaqt "oldin" shaklida ko'rinadi
- [ ] Izoh matni to'g'ri formatlangan

### Ruxsatnomalar
- [ ] Faqat o'z izohida tahrirlash tugmasi ko'rinadi
- [ ] Boshqa foydalanuvchining izohida tugmalar yo'q
- [ ] Yangilik muallifida "Muallif" belgisi ko'rinadi

### Dizayn va UX
- [ ] Bootstrap stillar to'g'ri qo'llanilgan
- [ ] Mobile qurilmalarda yaxshi ko'rinadi
- [ ] Xato xabarlari to'g'ri ko'rinadi
- [ ] Success xabarlari ko'rinadi
- [ ] Loading holatlar mavjud

### Xavfsizlik
- [ ] CSRF token barcha formalarda bor
- [ ] HTML teglar escape qilingan
- [ ] XSS hujumlaridan himoyalangan

### Qo'shimcha
- [ ] Pagination ishlaydi (agar qo'shilgan bo'lsa)
- [ ] Like/Dislike ishlaydi (agar qo'shilgan bo'lsa)
- [ ] Reply funksiyasi ishlaydi (agar qo'shilgan bo'lsa)

---

## Umumiy xatolar va yechimlar

### Xato 1: Izohlar ko'rinmayapti

**Sabab:** Context'da `comments` yo'q yoki noto'g'ri

**Yechim:**
```python
# views.py da
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['comments'] = self.object.comments.filter(active=True)
    return context
```

---

### Xato 2: Avatar ko'rinmayapti

**Sabab:** Profile modeli yo'q yoki photo field yo'q

**Yechim:**
```html
{% if comment.user.profile.photo %}
    <img src="{{ comment.user.profile.photo.url }}" ...>
{% else %}
    <!-- Harf avatarini ko'rsatish -->
{% endif %}
```

---

### Xato 3: Forma yuborilganda 404 xatosi

**Sabab:** POST metodi view'da yo'q yoki URL noto'g'ri

**Yechim:**
```python
# views.py da
def post(self, request, *args, **kwargs):
    # POST metodini qo'shing
    pass
```

---

### Xato 4: Dropdown menyu ishlamayapti

**Sabab:** Bootstrap JS yuklanmagan

**Yechim:**
```html
<!-- base.html da -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

---

### Xato 5: AJAX ishlamayapti

**Sabab:** View JSON qaytarmayapti

**Yechim:**
```python
from django.http import JsonResponse

def post(self, request, *args, **kwargs):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # ...
    
    if is_ajax:
        return JsonResponse({'success': True})
```

---

## Performance maslahatlar

### 💡 Maslahat 1: Select_related va prefetch_related

```python
# views.py
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Bir marta DB ga murojaat
    context['comments'] = self.object.comments.filter(
        active=True
    ).select_related('user', 'user__profile').order_by('-created_at')
    
    return context
```

### 💡 Maslahat 2: Lazy loading images

```html
<img src="{{ comment.user.profile.photo.url }}" 
     loading="lazy"
     alt="{{ comment.user.username }}">
```

### 💡 Maslahat 3: Cache ishlatish

```python
from django.views.decorators.cache import cache_page

# URL'da
path('news/<int:pk>/', cache_page(60 * 5)(NewsDetailView.as_view())),
```

### 💡 Maslahat 4: Static fayllarni minify qilish

```bash
# CSS va JS fayllarni minify qiling
# Production'da collectstatic ishlatilganda
python manage.py collectstatic
```

---

## Qo'shimcha resurslar

### Bootstrap komponentlari
- Cards: https://getbootstrap.com/docs/5.3/components/card/
- Forms: https://getbootstrap.com/docs/5.3/forms/overview/
- Buttons: https://getbootstrap.com/docs/5.3/components/buttons/
- Alerts: https://getbootstrap.com/docs/5.3/components/alerts/

### Django template dokumentatsiyasi
- Built-in filters: https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#built-in-filter-reference
- Template tags: https://docs.djangoproject.com/en/4.2/ref/templates/builtins/#built-in-tag-reference

### JavaScript
- Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API
- DOM manipulation: https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model

---

## Yakuniy natija

Ushbu amaliyotni tugatganingizdan so'ng:
- ✅ To'liq funksional izohlar tizimini yaratdingiz
- ✅ Bootstrap bilan chiroyli dizayn qildingiz
- ✅ JavaScript bilan interaktivlik qo'shdingiz
- ✅ Mobile-friendly interfeys yaratdingiz
- ✅ Best practices'larni qo'lladingiz

**Tabriklaymiz! Izohlar tizimi tayyor! 🎉**

Keyingi darsda **yangiliklarni izlash funksiyasini** yaratamiz!

**Omad yor bo'lsin! 🚀**