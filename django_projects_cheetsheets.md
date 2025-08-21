# Pipenv bilan Django Loyiha Yaratish - To'liq Qadamlar Ketma-ketligi

---

## 1. Muhitni tayyorlash

### Pipenv o‘rnatish (agar hali bo‘lmasa)
```bash
pip install pipenv
```
### Yangi loyiha papkasi yaratish

```bash
mkdir myproject
cd myproject
```

### Django ni o‘rnatish va virtual environment yaratish

```bash
pipenv install django
```

### Virtual environment ni faollashtirish

```bash
pipenv shell
```

### Django versiyasini tekshirish

```bash
python -m django --version
```
## 2. Django loyiha yaratish

### Yangi loyiha yaratish
```text
django-admin startproject config .

```
Natija: config papkasi yaratiladi:

config/
├── __init__.py
├── settings.py
├── urls.py
├── asgi.py
└── wsgi.py
manage.py
Pipfile
Pipfile.lock

### Loyihani sinab ko‘rish

```bash
python manage.py runserver
```
👉 Brauzerda: http://127.0.0.1:8000/



## 3. App yaratish
### Yangi app yaratish (masalan: blog)

```bash
python manage.py startapp blog
```

### Natija: blog papkasi yaratiladi:

blog/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
├── urls.py
└── views.py

## 4. App ni loyihaga qo‘shish
### Fayl: config/settings.py

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # Qo‘shing
]
```

## 5. Model yaratish
### Fayl: blog/models.py

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    content = models.TextField(verbose_name="Matn")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
```

## 6. Migratsiya qilish

```bash
python manage.py makemigrations
python manage.py migrate
```

## 7. Superuser yaratish

```bash
python manage.py createsuperuser
```

## 8. Admin panelga model qo‘shish
### Fayl: blog/admin.py

```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_published']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
```

## 9. URL sozlash
### Fayl: config/urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
```
### Fayl: blog/urls.py

```python
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
]

```
## 10. View yaratish
### Fayl: blog/views.py

```python
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    posts = Post.objects.filter(is_published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

```
## 11. Template yaratish

```bash
mkdir -p blog/templates/blog
```

### Fayl: blog/templates/blog/post_list.html

```html
<h1>Blog postlar</h1>
{% for post in posts %}
    <h2><a href="{% url 'blog:post_detail' post.pk %}">{{ post.title }}</a></h2>
    <p>{{ post.content|truncatewords:20 }}</p>
{% empty %}
    <p>Hozircha postlar yo‘q.</p>
{% endfor %}
```

### Fayl: blog/templates/blog/post_detail.html

```html
<h1>{{ post.title }}</h1>
<p>{{ post.content }}</p>
<a href="{% url 'blog:post_list' %}">← Orqaga</a>
```

## 12. Loyihani test qilish

```bash
python manage.py runserver
```

Test:
- [Admin panel](http://127.0.0.1:8000/admin/)
- [Blog sahifasi](http://127.0.0.1:8000/blog/)


## Yakuniy loyiha tuzilishi

myproject/
├── Pipfile
├── Pipfile.lock
├── db.sqlite3
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── blog/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    └── templates/
        └── blog/
            ├── post_list.html
            └── post_detail.html

## Foydali Pipenv buyruqlar
```bash

# Virtual muhitga kirish
pipenv shell

# Virtual muhitdan chiqish
exit

# Yangi paket o‘rnatish
pipenv install djangorestframework

# Faqat development uchun paket o‘rnatish
pipenv install black --dev

# Paketlar ro‘yxatini ko‘rish
pipenv graph

# Barcha paketlarni qayta o‘rnatish
pipenv install --ignore-pipfile
```
---

## Tekshirish ro‘yxati
 - **Pipenv o‘rnatildi**

 - **Django o‘rnatildi**

 - **Loyiha yaratildi**

 - **App yaratildi**

 - **Model yozildi**

 - **Migratsiya qilindi**

 - **Superuser yaratildi**

 - **Admin panel sozlandi**

 - **URL qo‘shildi**

 - **View yozildi**

 - **Template yaratildi**

 - **Loyiha test qilindi**

---

**Bu cheatsheet har safar yangi Django loyihasini pipenv yordamida yaratishda sizga yo‘l-yo‘riq bo‘ladi!**