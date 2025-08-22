# Lesson 06: Django qismlari bilan tanishish

## Maqsad

Ushbu darsda biz **Django loyihasining asosiy qismlari** bilan tanishamiz:  
`models`, `views`, `templates`, `urls` va boshqa muhim komponentlar.  

**Maqsad** — Django MVC (Model–View–Controller) arxitekturasi qanday ishlashini tushunish.

---

## 1. Django MVC/MVT arxitekturasi

Django’da klassik **MVC modeli** biroz o‘zgarib, **MVT (Model–View–Template)** deb ataladi:

- **Model** → ma’lumotlar bazasi qismi (ORM orqali ishlaydi).
- **View** → foydalanuvchidan kelgan so‘rovlarni qabul qiladi va javob qaytaradi.
- **Template** → foydalanuvchiga ko‘rinadigan HTML sahifalar.
- **URLconf (urls.py)** → kelgan so‘rovni to‘g‘ri view’ga yo‘naltiradi.

 **Oddiy oqim**:

```
User → URL → View → Model → View → Template → User
```

---

## 2. Django loyihasining asosiy fayllari

```
blog_project/
├─ blog_project/
│  ├─ settings.py   # Umumiy sozlamalar
│  ├─ urls.py       # URL yo‘llash
│  ├─ wsgi.py       # Deploy uchun
│  └─ asgi.py       # Async server uchun
├─ blog/
│  ├─ models.py     # Ma’lumotlar modeli
│  ├─ views.py      # View funksiyalar
│  ├─ urls.py       # Blog URL konfiguratsiyasi
│  ├─ templates/    # HTML fayllar
│  └─ admin.py      # Admin panelga modelni ulash
├─ manage.py        # Asosiy boshqaruv fayli
```

---

## 3. Django qismlari bilan tanishish

### 3.1. `manage.py`

Loyihani boshqarish uchun ishlatiladi:

```bash
python manage.py runserver       # serverni ishga tushirish
python manage.py makemigrations  # migratsiya yaratish
python manage.py migrate         # bazani yangilash
python manage.py createsuperuser # admin yaratish
```

---

### 3.2. `settings.py`

Loyiha sozlamalari shu faylda bo‘ladi.  
Masalan, `blog` ilovasini ulash uchun:

```python
INSTALLED_APPS = [
    ...
    'blog',
]
```

---

### 3.3. `urls.py`

So‘rovlarni tegishli view’ga bog‘laydi:

**blog_project/urls.py:**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # blog ilovasiga yo‘naltirish
]
```

**blog/urls.py:**

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # asosiy sahifa
]
```

---

### 3.4. `views.py`

Foydalanuvchi so‘rovini qabul qilib, javob qaytaradi:

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Salom, bu blogning asosiy sahifasi!")
```

Agar `http://127.0.0.1:8000/` ga kirsangiz, shu matn chiqadi.

---

### 3.5. `models.py`

Ma’lumotlar bazasi tuzilmasini aniqlash uchun ishlatiladi:

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)   # sarlavha
    content = models.TextField()               # matn
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

Model yaratgach:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 3.6. `templates/`

HTML fayllar shu yerda bo‘ladi.  

**blog/templates/home.html:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>Blog</title>
</head>
<body>
    <h1>Salom, Blog sahifasiga xush kelibsiz!</h1>
</body>
</html>
```

**views.py da foydalanish:**

```python
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
```

---

### 3.7. `admin.py`

Modelni admin panelga ulash:

```python
from django.contrib import admin
from .models import Post

admin.site.register(Post)
```

Keyin:

```bash
python manage.py createsuperuser
```

`/admin/` sahifasiga kirsangiz, `Post` modelini ko‘rasiz.

---

## 4. MVT oqim jarayoni (request → response)

1. Foydalanuvchi brauzerdan **URL kiritadi**.  
2. Django **urls.py** orqali qaysi view chaqirilishini aniqlaydi.  
3. View **modeldan ma’lumot oladi** yoki hisob-kitob qiladi.  
4. **Template** orqali HTML hosil qiladi.  
5. Foydalanuvchiga tayyor javob yuboriladi.  

---

## Xulosa

- Django **MVT arxitekturasi** asosida ishlaydi.  
- Har bir qismning vazifasi:  
  - **Model** — ma’lumotlar,  
  - **View** — logika,  
  - **Template** — ko‘rinish.  
- **urls.py** esa qismlarni bog‘lovchi **ko‘prik**.  

👉 **Keyingi dars (Lesson 07):** Blog Modelini yaratish va ishlatish.
