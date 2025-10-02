# Lesson 44: Django'da izoh qoldirish. Views qismini yozish (2-qism)

## Kirish

Assalomu alaykum! Oldingi darsda biz Comment modelini va CommentForm formasini yaratgan edik. Endi esa **views qismini** yozamiz - ya'ni foydalanuvchi izoh qoldirganda, bu izohni qanday qilib qabul qilish, saqlash va qayta ko'rsatishni amalga oshiramiz.

Bu darsda quyidagilarni o'rganamiz:
- Function-based view yordamida izoh qo'shish
- Form validatsiyasi va xatolarni qaytarish
- Redirect va success message
- News detail sahifasida izohlarni ko'rsatish

---

## 1. Joriy holat: News detail view

Avval `news/views.py` faylimizdagi `NewsDetailView`ni ko'rib chiqamiz:

```python
# news/views.py
from django.views.generic import DetailView
from .models import News

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
```

Bu juda oddiy DetailView. Endi biz bu sahifaga izoh qoldirish funksiyasini qo'shamiz.

---

## 2. Function-based view bilan izoh qo'shish

### 2.1. Viewni yaratish

`news/views.py` faylida yangi function yaratamiz:

```python
# news/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import News, Comment
from .forms import CommentForm

@login_required
def add_comment(request, pk):
    """Yangilikga izoh qo'shish"""
    # Yangilikni topamiz
    news = get_object_or_404(News, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Formani saqlaymiz, lekin hali DB ga yozmaymiz
            comment = form.save(commit=False)
            # Qo'shimcha ma'lumotlarni qo'shamiz
            comment.news = news
            comment.user = request.user
            # Endi DB ga saqlaymiz
            comment.save()
            
            messages.success(request, "Izohingiz muvaffaqiyatli qo'shildi!")
            return redirect('news_detail', pk=news.pk)
    else:
        form = CommentForm()
    
    context = {
        'form': form,
        'news': news
    }
    return render(request, 'news/add_comment.html', context)
```

### 2.2. Kod tushuntirilishi

Keling, har bir qismni batafsil ko'rib chiqamiz:

#### a) `@login_required` dekoratori
```python
@login_required
def add_comment(request, pk):
```
- Bu dekorator foydalanuvchi tizimga kirganligini tekshiradi
- Agar kirmagan bo'lsa, login sahifasiga yo'naltiradi
- Settings.py da `LOGIN_URL = 'login'` bo'lishi kerak

#### b) Yangilikni topish
```python
news = get_object_or_404(News, pk=pk)
```
- URL dan kelgan `pk` orqali yangilikni qidiramiz
- Agar topilmasa, 404 xatosi qaytaradi

#### c) POST so'rovni qayta ishlash
```python
if request.method == 'POST':
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.news = news
        comment.user = request.user
        comment.save()
```

**`commit=False` nima?**
- Bu formani saqlaymiz, lekin hali bazaga yozmaymiz
- Avval qo'shimcha ma'lumotlarni qo'shishimiz kerak (news va user)
- Keyin `.save()` bilan bazaga saqlaymiz

#### d) Success message va redirect
```python
messages.success(request, "Izohingiz muvaffaqiyatli qo'shildi!")
return redirect('news_detail', pk=news.pk)
```
- Muvaffaqiyatli xabar ko'rsatamiz
- Yangilik sahifasiga qaytaramiz

---

## 3. Alternative: DetailView ichida izoh qo'shish

Yana bir yondashuv - DetailView ichida formani qayta ishlash:

```python
# news/views.py
from django.views.generic import DetailView
from django.shortcuts import redirect
from django.contrib import messages
from .models import News, Comment
from .forms import CommentForm

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Yangilikka tegishli izohlarni olamiz
        context['comments'] = self.object.comments.all().order_by('-created_at')
        # Bo'sh formani qo'shamiz
        context['comment_form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        """POST so'rovni qayta ishlaymiz"""
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = self.object
            comment.user = request.user
            comment.save()
            
            messages.success(request, "Izohingiz qo'shildi!")
            return redirect('news_detail', pk=self.object.pk)
        
        # Agar form noto'g'ri bo'lsa
        context = self.get_context_data()
        context['comment_form'] = form  # Xatolar bilan formani qaytaramiz
        return self.render_to_response(context)
```

### 3.1. Bu yondashuvning afzalliklari

✅ Bitta view - bitta sahifa uchun
✅ Formani shu yerda ko'rsatamiz va qayta ishlaymiz
✅ Kodlar bir joyda
✅ Qo'shimcha URL kerak emas

### 3.2. Kod tushuntirilishi

#### a) `get_context_data` metodi
```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['comments'] = self.object.comments.all().order_by('-created_at')
    context['comment_form'] = CommentForm()
    return context
```
- Template uchun qo'shimcha ma'lumotlar tayyorlaymiz
- `self.object` - joriy yangilik obyekti
- `.comments.all()` - bu yangilikning barcha izohlarini olamiz
- `order_by('-created_at')` - eng yangi izohlar yuqorida

#### b) `post` metodi
```python
def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form = CommentForm(request.POST)
```
- DetailView avtomatik ravishda faqat GET so'rovlarni qabul qiladi
- POST so'rovlarni qayta ishlash uchun `post` metodini yozamiz

---

## 4. URLs ni sozlash

### 4.1. Birinchi yondashuv uchun (alohida view)

```python
# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... boshqa URL'lar
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    path('news/<int:pk>/comment/', views.add_comment, name='add_comment'),
]
```

### 4.2. Ikkinchi yondashuv uchun (DetailView ichida)

```python
# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # ... boshqa URL'lar
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
    # Qo'shimcha URL kerak emas!
]
```

---

## 5. Login required qo'shish (DetailView uchun)

Agar DetailView yondashuvini tanlasak, login required qo'shishimiz kerak:

### 5.1. Mixin bilan

```python
# news/views.py
from django.contrib.auth.mixins import LoginRequiredMixin

class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    # ... qolgan kod
```

**Muammo:** Bu butun sahifani himoya qiladi. Ya'ni foydalanuvchi tizimga kirmagan bo'lsa, yangilikni ham ko'ra olmaydi!

### 5.2. Yaxshiroq yechim: Faqat POST uchun tekshirish

```python
# news/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        # Foydalanuvchi tizimga kirganmi?
        if not request.user.is_authenticated:
            messages.warning(request, "Izoh qoldirish uchun tizimga kiring!")
            return redirect('login')
        
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = self.object
            comment.user = request.user
            comment.save()
            
            messages.success(request, "Izohingiz qo'shildi!")
            return redirect('news_detail', pk=self.object.pk)
        
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)
```

---

## 6. Izohlarni sanab ko'rsatish

Izohlarni ko'rsatish uchun `get_context_data` metodida izohlarni contextga qo'shamiz:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    # Barcha izohlar
    context['comments'] = self.object.comments.filter(active=True).order_by('-created_at')
    
    # Izohlar soni
    context['comments_count'] = context['comments'].count()
    
    # Forma
    context['comment_form'] = CommentForm()
    
    return context
```

### Tushuntirish:
- `.filter(active=True)` - faqat faol izohlarni olamiz
- `.order_by('-created_at')` - eng yangi izohlar birinchi
- `.count()` - jami izohlar soni

---

## 7. To'liq kod namunasi

### news/views.py (tavsiya etilgan yondashuv)

```python
from django.views.generic import DetailView
from django.shortcuts import redirect
from django.contrib import messages
from .models import News, Comment
from .forms import CommentForm

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        """Template uchun ma'lumotlarni tayyorlaymiz"""
        context = super().get_context_data(**kwargs)
        
        # Faol izohlarni olamiz (eng yangisi yuqorida)
        context['comments'] = self.object.comments.filter(
            active=True
        ).order_by('-created_at')
        
        # Izohlar sonini hisoblaymiz
        context['comments_count'] = context['comments'].count()
        
        # Bo'sh formani qo'shamiz
        context['comment_form'] = CommentForm()
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Izoh qo'shish uchun POST so'rovni qayta ishlaymiz"""
        
        # Foydalanuvchi autentifikatsiya qilinganmi?
        if not request.user.is_authenticated:
            messages.warning(request, "Izoh qoldirish uchun avval tizimga kiring!")
            return redirect('login')
        
        # Yangilikni olamiz
        self.object = self.get_object()
        
        # Formani to'ldiramiz
        form = CommentForm(request.POST)
        
        if form.is_valid():
            # Formani saqlaymiz (hali DB ga emas)
            comment = form.save(commit=False)
            
            # Qo'shimcha ma'lumotlarni qo'shamiz
            comment.news = self.object
            comment.user = request.user
            
            # Endi DB ga saqlaymiz
            comment.save()
            
            # Success message
            messages.success(request, "Rahmat! Izohingiz muvaffaqiyatli qo'shildi.")
            
            # Sahifani yangilaymiz
            return redirect('news_detail', pk=self.object.pk)
        
        # Agar forma xato bo'lsa
        context = self.get_context_data()
        context['comment_form'] = form  # Xatolar bilan forma
        return self.render_to_response(context)
```

### news/urls.py

```python
from django.urls import path
from . import views

urlpatterns = [
    # Boshqa URL'lar...
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
]
```

---

## 8. Xavfsizlik masalalari

### 8.1. CSRF himoyasi

Django avtomatik ravishda CSRF token tekshiradi. Template'da:

```html
<form method="post">
    {% csrf_token %}
    {{ comment_form.as_p }}
    <button type="submit">Izoh qoldirish</button>
</form>
```

`{% csrf_token %}` - bu juda muhim! Uni unutmang.

### 8.2. XSS (Cross-Site Scripting) dan himoya

Comment modelida `body` maydonini sanitize qilish:

```python
# news/models.py
from django.utils.html import escape

class Comment(models.Model):
    # ... boshqa fieldlar
    
    def save(self, *args, **kwargs):
        # HTML teglarni escape qilamiz
        self.body = escape(self.body)
        super().save(*args, **kwargs)
```

Yoki template'da:

```html
{{ comment.body|linebreaks }}  <!-- Avtomatik escape qiladi -->
```

---

## 9. Best Practices

### ✅ 1. Qaysi yondashuvni tanlash?

**DetailView ichida (tavsiya etiladi):**
- Oddiy holatlarda
- Forma va sahifa bir-biriga bog'liq bo'lsa
- Kodlar bir joyda bo'lishini xohlasangiz

**Alohida function-based view:**
- Murakkab logika bo'lsa
- Bir nechta formalar bo'lsa
- View'ni qayta ishlatish kerak bo'lsa

### ✅ 2. Validation

```python
def post(self, request, *args, **kwargs):
    # ...
    form = CommentForm(request.POST)
    
    if form.is_valid():
        # Qo'shimcha tekshiruvlar
        comment = form.save(commit=False)
        
        # Masalan: spam so'zlarni tekshirish
        spam_words = ['spam', 'viagra', 'casino']
        if any(word in comment.body.lower() for word in spam_words):
            messages.error(request, "Sizning izohingizda taqiqlangan so'zlar bor!")
            return redirect('news_detail', pk=self.object.pk)
        
        comment.news = self.object
        comment.user = request.user
        comment.save()
        # ...
```

### ✅ 3. Rate limiting

Bir foydalanuvchining juda ko'p izoh qoldirmasligini ta'minlash:

```python
from django.utils import timezone
from datetime import timedelta

def post(self, request, *args, **kwargs):
    # ...
    
    # Oxirgi 1 daqiqada qoldirgan izohlarni sanash
    recent_comments = Comment.objects.filter(
        user=request.user,
        created_at__gte=timezone.now() - timedelta(minutes=1)
    ).count()
    
    if recent_comments >= 3:
        messages.warning(request, "Iltimos, 1 daqiqa kutib turing.")
        return redirect('news_detail', pk=self.object.pk)
    
    # ... davom etadi
```

### ✅ 4. Success message'larni ko'rsatish

Settings.py da:

```python
# settings.py
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
```

Base template'da:

```html
<!-- templates/base.html -->
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
            {{ message }}
            <button type="button" class="close" data-dismiss="alert">&times;</button>
        </div>
    {% endfor %}
{% endif %}
```

---

## 10. Xatolarni tekshirish

### Umumiy xatolar:

**1. "RelatedObjectDoesNotExist" xatosi**
```python
# Xato:
comment.user  # Agar user yo'q bo'lsa

# To'g'ri:
if hasattr(comment, 'user') and comment.user:
    print(comment.user.username)
```

**2. "IntegrityError: NOT NULL constraint failed"**
```python
# Xato: user yoki news berilmagan
comment = form.save()  # ❌

# To'g'ri:
comment = form.save(commit=False)
comment.user = request.user
comment.news = self.object
comment.save()  # ✅
```

**3. CSRF verification failed**
- Template'da `{% csrf_token %}` borligini tekshiring
- Forma `method="post"` bo'lishi kerak

---

## Xulosa

Bu darsda biz:
- ✅ DetailView ichida POST so'rovlarni qayta ishlashni o'rgandik
- ✅ Comment qo'shish funksiyasini yozdik
- ✅ Form validatsiyasi va xatolarni ko'rsatishni o'rnatdik
- ✅ Xavfsizlik masalalari bilan tanishdik
- ✅ Best practices'larni ko'rib chiqdik

Keyingi darsda **template qismini** yozamiz va izohlarni chiroyli ko'rinishda chiqaramiz!

---

## Qo'shimcha o'qish uchun

- Django Messages Framework: https://docs.djangoproject.com/en/4.2/ref/contrib/messages/
- Form Validation: https://docs.djangoproject.com/en/4.2/ref/forms/validation/
- Class-based Views: https://docs.djangoproject.com/en/4.2/topics/class-based-views/