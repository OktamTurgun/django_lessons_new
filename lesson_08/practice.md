# Lesson 08 Practice: Views va Templates bilan ishlash

Ushbu amaliy mashqlar orqali siz Django’da **views**, **urls** va **templates** bilan ishlashni amalda o‘rganasiz. Har bir bosqichni ketma-ket bajaring.

---

## 1 Oddiy view yozish
Vazifa: `blog/views.py` ichida quyidagini yozing:

```python
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Salom! Bu mening birinchi view’im.")
```

So‘ngra `blog/urls.py` faylida view’ni ro‘yxatdan o‘tkazing:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
]
```

Brauzerda `http://127.0.0.1:8000/hello/` ni ochib tekshirib ko‘ring.

---

## 2 Template bilan ishlash
Vazifa: `templates/blog/home.html` faylini yarating:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Blog Home</title>
</head>
<body>
    <h1>Salom, Blog sahifasiga xush kelibsiz!</h1>
    <p>Bugun: {{ date }}</p>
</body>
</html>
```

`views.py` ichida:

```python
from django.shortcuts import render
import datetime

def home(request):
    context = {
        "date": datetime.date.today()
    }
    return render(request, "blog/home.html", context)
```

Brauzerda asosiy sahifada hozirgi sana chiqishini ko‘ring.

---

## 3 Dynamic URL va parametrlar
Vazifa: View yozing:

```python
from django.http import HttpResponse

def greet(request, name):
    return HttpResponse(f"Salom, {name.title()}!")
```

`urls.py` ichiga qo‘shing:

```python
path('greet/<str:name>/', views.greet, name='greet'),
```

`http://127.0.0.1:8000/greet/ali/` manziliga kirsangiz → “Salom, Ali!” chiqadi.

---

## 4 Blog postlar ro‘yxati
Vazifa: Avvalgi darsdagi `Post` modelidan foydalanib, postlarni chiqaruvchi view yozing:

```python
from .models import Post

def post_list(request):
    posts = Post.objects.all()
    return render(request, "blog/post_list.html", {"posts": posts})
```

Template (`templates/blog/post_list.html`):

```html
<h1>Blog Postlar</h1>
<ul>
  {% for post in posts %}
    <li>{{ post.title }} - {{ post.author }}</li>
  {% endfor %}
</ul>
```

Brauzerda barcha postlar chiqishini ko‘ring.

---

## 5 Bitta postni ko‘rsatish (detail view)
Vazifa: Dynamic URL orqali bitta postni ko‘rsatish.

`views.py` ichida:

```python
from django.shortcuts import get_object_or_404

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})
```

`urls.py` ichiga qo‘shing:

```python
path('post/<int:pk>/', views.post_detail, name='post_detail'),
```

Template (`templates/blog/post_detail.html`):

```html
<h1>{{ post.title }}</h1>
<p><b>Author:</b> {{ post.author }}</p>
<p>{{ post.content }}</p>
<p><i>Yaratilgan: {{ post.created_at }}</i></p>
```

`http://127.0.0.1:8000/post/1/` manzilida birinchi post chiqadi.

---

## Yakuniy mashq
- `home`, `post_list`, va `post_detail` sahifalarini navigatsiya orqali bog‘lab qo‘ying.  
- Har bir sahifaga havola (`<a href="...">`) joylang.  
- Sahifalararo o‘tishni tekshirib ko‘ring.

---

##  Muhim eslatmalar
- `render()` funksiyasi HTML faylga context yuboradi.  
- `get_object_or_404` mavjud bo‘lmagan obyektlarda 404 sahifasini qaytaradi.  
- Templates’da `for` va `if` kabi **Django template tag**lardan foydalaniladi.  
- Katta loyihalarda views uchun **Class-Based Views (CBV)** ishlatish tavsiya etiladi.

---

Shu bilan siz Django’da **views** va **templates** bilan ishlashni amalda o‘rgandingiz!
