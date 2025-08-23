# Lesson 07: Blog Model qismi

## Maqsad

Ushbu darsda biz **Django Model** tushunchasi bilan chuqur tanishamiz.  
Blog ilovamiz uchun **Post modeli** yaratiladi, ma’lumotlar bazasi bilan ishlashni ko‘ramiz va amaliy misollar orqali mustahkamlaymiz.

---

## 1. Model nima?

- Django’da **Model** — bu ma’lumotlar bazasi jadvallarini ifodalaydigan **Python class**.
- Har bir model `django.db.models.Model` dan meros oladi.
- **Django ORM** (Object Relational Mapper) orqali SQL yozmasdan, Python kodida ma’lumotlar bilan ishlashimiz mumkin.

---

## 2. Blog uchun Post modeli yaratish

`blog/models.py` faylini ochamiz va quyidagicha yozamiz:

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)  # Post sarlavhasi
    content = models.TextField()  # Post matni
    created_at = models.DateTimeField(auto_now_add=True)  # Avtomatik sana
    updated_at = models.DateTimeField(auto_now=True)  # Har tahrirlanganda yangilanadi
    is_published = models.BooleanField(default=True)  # Post ko‘rinishi

    def __str__(self):
        return self.title
```

📌 **Izohlar**:
- `CharField` → qisqa matn (title kabi).
- `TextField` → uzun matn (kontent uchun).
- `DateTimeField(auto_now_add=True)` → obyekt yaratilganda avtomatik sana.
- `DateTimeField(auto_now=True)` → obyekt yangilanganda sana avtomatik yangilanadi.
- `BooleanField` → ha/yo‘q qiymati (True/False).
- `__str__` → admin panel va konsolda obyekt qanday ko‘rinishini belgilaydi.

---

## 3. Migratsiyalar

Model qo‘shilgandan keyin migratsiya qilish kerak:

```bash
python manage.py makemigrations
python manage.py migrate
```

 Bu amallar **Post modelini ma’lumotlar bazasida jadval sifatida yaratadi**.

---

## 4. Admin panelga qo‘shish

`blog/admin.py` faylini ochamiz:

```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
```

📌 **Izohlar**:
- `list_display` → admin jadvalda ko‘rsatiladigan ustunlar.
- `list_filter` → yon paneldagi filtrlar.
- `search_fields` → qidirish uchun maydonlar.

---

## 5. Model bilan ishlash (Django ORM)

Django shell orqali modelni sinab ko‘ramiz:

```bash
python manage.py shell
```

```python
from blog.models import Post

# Yangi post yaratish
post = Post.objects.create(title="Birinchi post", content="Bu mening birinchi blog postim!")

# Barcha postlarni olish
Post.objects.all()

# Bitta post topish
Post.objects.get(id=1)

# Filtrlash
Post.objects.filter(is_published=True)

# Yangilash
post.title = "Yangilangan post"
post.save()

# O‘chirish
post.delete()
```

📌 **Best Practice**:
- `.create()` → yangi obyekt yaratadi va saqlaydi.
- `.save()` → mavjud obyektni yangilaydi.
- `.filter()` va `.get()` → ma’lumotlarni izlash uchun.

---

## 6. Template orqali postlarni chiqarish

### 6.1 View yozamiz (`views.py`):

```python
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})
```

📌 **Izoh**:
- `filter(is_published=True)` → faqat ko‘rinadigan postlarni olish.
- `order_by('-created_at')` → yangilarini oldinda chiqarish.

---

### 6.2 URL sozlash (`urls.py`):

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
]
```

---

### 6.3 Template yaratish (`templates/blog/post_list.html`):

```html
<!DOCTYPE html>
<html>
<head>
    <title>Blog Postlari</title>
</head>
<body>
    <h1>📘 Blog Postlari</h1>
    {% for post in posts %}
        <h2>{{ post.title }}</h2>
        <p>{{ post.content|truncatechars:100 }}</p>
        <small>📅 {{ post.created_at }}</small>
        <hr>
    {% empty %}
        <p>Hozircha post yo‘q.</p>
    {% endfor %}
</body>
</html>
```

📌 **Izoh**:
- `truncatechars:100` → matnni 100 belgidan keyin qisqartiradi.
- `{% empty %}` → agar post bo‘lmasa, xabar ko‘rsatadi.

---

## 7. Maslahatlar va Best Practice

- Model maydonlarini ilojini boricha aniq tiplarda belgilang (`CharField`, `TextField`, `BooleanField`, `DateField` va h.k.).
- `__str__` metodini har doim yozing → debugging va admin panelda ko‘rish qulay bo‘ladi.
- `Meta` klassidan foydalaning:

```python
class Post(models.Model):
    ...
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Postlar"
```

- Admin panelda `list_display`, `search_fields`, `list_filter` larni sozlab boring.
- ORM’dan foydalanish SQL yozishni yengillashtiradi, lekin query sonini minimallashtirishga e’tibor bering.

---

## Xulosa

- **Model** — bu ma’lumotlar bazasidagi jadvalning Python classdagi ifodasi.  
- Biz **Post modelini** yaratdik, migratsiya qildik, admin panelga qo‘shdik va ORM orqali ishlashni o‘rgandik.  
- **Template orqali postlarni ro‘yxat ko‘rinishida chiqarishni** o‘rgandik.  

👉 Endi sizda Blog uchun tayyor **Model qismi** mavjud. Keyingi darslarda bu modelni foydalanuvchi bilan integratsiya qilishni o‘rganamiz.

**Keyingi dars:**
8-dars: Blog loyihasi: Views va templates bilan ishlash