# Lesson 08: Blog loyihasi — Views va Templates bilan ishlash

## Maqsad
Ushbu darsda biz Django loyihamizda **views** va **templates** bilan ishlashni o‘rganamiz. Siz foydalanuvchiga ma’lumot ko‘rsatish, URL’larni boshqarish va dinamik sahifalar yaratishni amalda ko‘rib chiqasiz.

---

## 1 Views nima?
Django’da **view** — bu foydalanuvchi so‘roviga javob qaytaruvchi funksiya yoki klassdir.  
Oddiy qilib aytganda: **URL → View → Response** oqimi mavjud.

### Function-Based Views (FBV)
```python
# blog/views.py
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Salom, bu birinchi view!")
```

### Class-Based Views (CBV)
```python
# blog/views.py
from django.views import View
from django.http import HttpResponse

class HelloView(View):
    def get(self, request):
        return HttpResponse("Salom, bu Class-Based View!")
```

---

## 2 urls.py bilan ishlash
Har bir view URL bilan bog‘lanishi kerak.

```python
# blog/urls.py
from django.urls import path
from . import views
from .views import HelloView

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('cbv/', HelloView.as_view(), name='hello_cbv'),
]
```

**Asosiy urls.py** ichiga qo‘shamiz:
```python
# blog_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
]
```

---

## 3 Templates bilan ishlash
Template — bu HTML fayl bo‘lib, u foydalanuvchiga ko‘rinadigan sahifani shakllantiradi.

**Misol:**
```python
# blog/views.py
from django.shortcuts import render

def home(request):
    return render(request, 'blog/home.html', {"name": "Ali"})
```

```html
<!-- blog/templates/blog/home.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Blog</title>
</head>
<body>
    <h1>Salom, {{ name }}!</h1>
    <p>Bu mening birinchi template sahifam.</p>
</body>
</html>
```

Natija: Brauzerda `http://127.0.0.1:8000/` ga kirganda **Salom, Ali!** chiqadi.

---

## 4 Context orqali ma’lumot uzatish
```python
# blog/views.py
def about(request):
    context = {
        "title": "Haqida sahifa",
        "description": "Bu sahifada loyiha haqida ma’lumot bor."
    }
    return render(request, 'blog/about.html', context)
```

```html
<!-- blog/templates/blog/about.html -->
<h1>{{ title }}</h1>
<p>{{ description }}</p>
```

---

## 5 Dynamic URL’lar va get_object_or_404
```python
# blog/views.py
from django.shortcuts import render, get_object_or_404
from .models import Post

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {"post": post})
```

```python
# blog/urls.py
urlpatterns = [
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
]
```

```html
<!-- blog/templates/blog/post_detail.html -->
<h2>{{ post.title }}</h2>
<p>{{ post.content }}</p>
<small>Muallif: {{ post.author }}</small>
```

Natija: `http://127.0.0.1:8000/post/1/` ga kirganda **id=1** bo‘lgan post chiqadi.

---

## Muhim eslatmalar va maslahatlar
- **FBV** kichik va oddiy loyihalar uchun qulay, lekin **CBV** yirik loyihalarda qayta foydalanishga ancha mos.
- Har bir app ichida `templates/<app_name>/` strukturasini saqlash best practice hisoblanadi.
- Har doim **get_object_or_404** ishlatish tavsiya qilinadi — bu xatoliklarni foydalanuvchi uchun toza ko‘rsatadi.
- Template ichida murakkab logikani emas, balki faqat ma’lumotni ko‘rsatishni ishlating.
- Kodni DRY (Don't Repeat Yourself) qoidasi asosida yozing.

---

## Yakun
Endi siz Django’da:
- Views (FBV & CBV) yozishni
- URL’larni boshqarishni
- Templates bilan ishlashni
- Context orqali ma’lumot uzatishni
- Dinamik sahifalar yaratishni

o‘rgandingiz.

**Keyingi dars:**
9-dars: Blog loyihasi. BlogDetail. Funksiyaga asoslangan View.