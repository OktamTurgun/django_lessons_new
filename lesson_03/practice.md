# Lesson 03 – Amaliyot  
**Mavzu:** Django arxitekturasi va ishlash tamoyili  

---

## 🎯 Maqsad
- Django MTV arxitekturasi bilan tanishish  
- Django’da **model**, **view** va **template** lar qanday ishlashini amaliy misolda ko‘rish  

---

## 1-qadam: Yangi Django loyihasi yaratish
```bash
django-admin startproject lesson_03_project
cd lesson_03_project
python manage.py startapp blog
```

## 2-qadam: settings.py faylida app ni ro‘yxatga olish

```python
INSTALLED_APPS = [
    ...,
    'blog',
]

```

## 3-qadam: Model yaratish (blog/models.py)

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

```

So‘ngra migratsiyalarni bajaring:

```bash
python manage.py makemigrations
python manage.py migrate

```
## 4-qadam: View yozish (blog/views.py)

```python
from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})

```

## 5-qadam: Template yaratish (blog/templates/blog/home.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Blog</title>
</head>
<body>
    <h1>Postlar ro‘yxati</h1>
    <ul>
        {% for post in posts %}
            <li>
                <h2>{{ post.title }}</h2>
                <p>{{ post.content }}</p>
            </li>
        {% endfor %}
    </ul>
</body>
</html>

```

## 6-qadam: URL sozlash
blog/urls.py fayli:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]

```

## lesson_03_project/urls.py fayliga qo‘shish:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]

```

**Natija:**
Brauzerda **http://127.0.0.1:8000/** ga kirsangiz, Post lar ro‘yxati chiqadi.

Siz endi **Model** → **View** → **Template** oqimini amalda ko‘rdingiz.
