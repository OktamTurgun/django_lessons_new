# Lesson 44: Practice - Django'da izoh qoldirish. Views qismini yozish

## Amaliyot maqsadi

Ushbu amaliyotda siz:
- NewsDetailView ichida izoh qo'shish funksiyasini yozasiz
- POST so'rovlarni to'g'ri qayta ishlashni o'rganasiz
- Form validatsiyasi va xatolarni boshqarishni amalda qo'llaysiz
- Xavfsizlik choralari va best practices bilan ishlaysiz

---

## Boshlang'ich holatni tekshirish

Oldingi darsda yaratgan modellarimiz va formalarimiz tayyor bo'lishi kerak:

### 1. Comment modeli (`news/models.py`)
```python
from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.news.title[:30]}"
```

### 2. CommentForm (`news/forms.py`)
```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Izohingizni yozing...'
            })
        }
        labels = {
            'body': 'Izoh'
        }
```

---

## Amaliy topshiriqlar

### Topshiriq 1: Joriy NewsDetailView ni ko'rib chiqish ⭐

**Maqsad:** Hozirgi NewsDetailView qanday ishlayotganini tushunish

**1.1. Joriy kodni ochish**

`news/views.py` faylini oching va NewsDetailView ni toping:

```python
from django.views.generic import DetailView
from .models import News

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
```

**Savol:** Bu view faqat nima qiladi?
<details>
<summary>Javob</summary>
Bu view faqat GET so'rovlarni qabul qiladi va yangilik ma'lumotlarini ko'rsatadi. POST so'rovlarni (masalan, forma yuborish) qabul qilmaydi.
</details>

---

### Topshiriq 2: get_context_data metodini qo'shish ⭐⭐

**Maqsad:** Template uchun izohlar va formani tayyorlash

**2.1. Importlarni qo'shish**

`news/views.py` faylining boshiga qo'shing:

```python
from django.views.generic import DetailView
from django.shortcuts import redirect
from django.contrib import messages
from .models import News, Comment
from .forms import CommentForm
```

**2.2. get_context_data metodini yozish**

NewsDetailView ichiga qo'shing:

```python
class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # TODO: Faol izohlarni oling
        # TODO: Izohlar sonini hisoblang
        # TODO: Bo'sh formani qo'shing
        
        return context
```

**Topshiriq:** TODO qatorlarini to'ldiring

<details>
<summary>Yechim</summary>

```python
def get_context_data(self, **kwargs):
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
```
</details>

**2.3. Tekshirish**

Terminal'da:
```bash
python manage.py runserver
```

Brauzerda yangilik sahifasiga kiring va Django Debug Toolbar yoki `{{ debug }}` orqali contextni tekshiring.

---

### Topshiriq 3: POST metodini qo'shish (oddiy versiya) ⭐⭐

**Maqsad:** POST so'rovlarni qabul qilish va formani saqlash

**3.1. Oddiy post metodini yozish**

```python
def post(self, request, *args, **kwargs):
    # 1. Yangilikni olish
    self.object = self.get_object()
    
    # 2. Formani to'ldirish
    form = CommentForm(request.POST)
    
    # 3. Validatsiya
    if form.is_valid():
        # 4. Formani saqlash
        comment = form.save(commit=False)
        
        # TODO: news va user ni qo'shing
        
        # 5. Bazaga saqlash
        comment.save()
        
        # 6. Redirect qilish
        return redirect('news_detail', pk=self.object.pk)
    
    # Agar forma xato bo'lsa
    context = self.get_context_data()
    context['comment_form'] = form
    return self.render_to_response(context)
```

**Topshiriq:** TODO qismini to'ldiring

<details>
<summary>Yechim</summary>

```python
# Qo'shimcha ma'lumotlarni qo'shamiz
comment.news = self.object
comment.user = request.user
```
</details>

**3.2. Xato yuz beradi!**

Agar siz formani yuborib ko'rsangiz, qanday xato yuz beradi?

<details>
<summary>Javob</summary>
`IntegrityError: NOT NULL constraint failed: news_comment.user_id`

Sabab: Foydalanuvchi tizimga kirmaganligini tekshirmadik!
</details>

---

### Topshiriq 4: Autentifikatsiya tekshiruvi qo'shish ⭐⭐⭐

**Maqsad:** Faqat tizimga kirgan foydalanuvchilar izoh qoldirishini ta'minlash

**4.1. Tekshiruv qo'shish**

`post` metodining boshiga qo'shing:

```python
def post(self, request, *args, **kwargs):
    # Foydalanuvchi tizimga kirganmi?
    if not request.user.is_authenticated:
        # TODO: Warning message qo'shing
        # TODO: Login sahifasiga yo'naltiring
        pass
    
    # ... qolgan kod
```

**Topshiriq:** TODO qismlarini to'ldiring

<details>
<summary>Yechim</summary>

```python
if not request.user.is_authenticated:
    messages.warning(request, "Izoh qoldirish uchun avval tizimga kiring!")
    return redirect('login')
```
</details>

**4.2. Tekshirish**

1. Brauzerdan chiqing (logout qiling)
2. Yangilik sahifasiga kiring
3. Izoh yozib, yuborib ko'ring
4. Login sahifasiga yo'naltirilishingiz kerak

---

### Topshiriq 5: Success message qo'shish ⭐⭐

**Maqsad:** Foydalanuvchiga muvaffaqiyatli xabar ko'rsatish

**5.1. Message qo'shish**

`post` metodida `comment.save()` dan keyin:

```python
comment.save()

# TODO: Success message qo'shing

messages.success(request, "Rahmat! Izohingiz muvaffaqiyatli qo'shildi.")
```

**5.2. Base template'da message'larni ko'rsatish**

`templates/base.html` faylini oching va `{% block content %}` dan oldin qo'shing:

```html
<!-- Messages -->
{% if messages %}
    <div class="container mt-3">
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    </div>
{% endif %}

{% block content %}
{% endblock %}
```

**5.3. Message tags'ni sozlash (optional)**

`config/settings.py` ga qo'shing:

```python
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}
```

---

### Topshiriq 6: Formadagi xatolarni ko'rsatish ⭐⭐⭐

**Maqsad:** Agar forma noto'g'ri to'ldirilsa, xatolarni ko'rsatish

**6.1. Xato holatini qayta ishlash**

`post` metodining oxirida:

```python
# Agar forma xato bo'lsa
if not form.is_valid():
    messages.error(request, "Formada xatolar bor. Iltimos, qaytadan tekshiring.")
    
context = self.get_context_data()
context['comment_form'] = form  # Xatolar bilan forma
return self.render_to_response(context)
```

**6.2. Test qilish**

Bo'sh izoh yozib ko'ring - xato xabari ko'rinishi kerak.

---

### Topshiriq 7: Qo'shimcha validatsiya qo'shish ⭐⭐⭐⭐

**Maqsad:** Spam va keraksiz izohlarni oldini olish

**7.1. Minimum uzunlik tekshiruvi**

```python
if form.is_valid():
    comment = form.save(commit=False)
    
    # Minimum uzunlik tekshiruvi
    if len(comment.body.strip()) < 10:
        messages.error(request, "Izoh kamida 10 ta belgidan iborat bo'lishi kerak!")
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)
    
    comment.news = self.object
    comment.user = request.user
    comment.save()
    # ...
```

**7.2. Spam so'zlarni tekshirish**

```python
# Spam so'zlar ro'yxati
SPAM_WORDS = ['spam', 'viagra', 'casino', 'betting', 'loan']

if form.is_valid():
    comment = form.save(commit=False)
    
    # Spam tekshiruvi
    comment_lower = comment.body.lower()
    if any(word in comment_lower for word in SPAM_WORDS):
        messages.error(request, "Sizning izohingizda taqiqlangan so'zlar mavjud!")
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)
    
    # ... davom etadi
```

---

### Topshiriq 8: Rate limiting qo'shish ⭐⭐⭐⭐⭐

**Maqsad:** Bir foydalanuvchining juda ko'p izoh qoldirmasligini ta'minlash

**8.1. Import qo'shish**

```python
from django.utils import timezone
from datetime import timedelta
```

**8.2. Rate limiting logikasi**

```python
def post(self, request, *args, **kwargs):
    # ... autentifikatsiya tekshiruvi
    
    # Oxirgi 1 daqiqada qoldirgan izohlarni sanash
    recent_comments = Comment.objects.filter(
        user=request.user,
        created_at__gte=timezone.now() - timedelta(minutes=1)
    ).count()
    
    if recent_comments >= 3:
        messages.warning(
            request, 
            "Siz juda ko'p izoh qoldirmoqdasiz. Iltimos, 1 daqiqa kutib turing."
        )
        return redirect('news_detail', pk=self.object.pk)
    
    # ... qolgan kod
```

**8.3. Test qilish**

Bir yangilikka ketma-ket 4 ta izoh yozib ko'ring - 4-chisi ruxsat berilmasligi kerak.

---

### Topshiriq 9: To'liq kod yozish ⭐⭐⭐⭐⭐

**Maqsad:** Barcha funksiyalarni birlashtirib, to'liq view yaratish

**9.1. To'liq NewsDetailView**

```python
# news/views.py
from django.views.generic import DetailView
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import News, Comment
from .forms import CommentForm

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        """Template uchun ma'lumotlarni tayyorlaymiz"""
        context = super().get_context_data(**kwargs)
        
        # Faol izohlarni olamiz
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
        
        # 1. Autentifikatsiya tekshiruvi
        if not request.user.is_authenticated:
            messages.warning(request, "Izoh qoldirish uchun avval tizimga kiring!")
            return redirect('login')
        
        # 2. Yangilikni olamiz
        self.object = self.get_object()
        
        # 3. Rate limiting
        recent_comments = Comment.objects.filter(
            user=request.user,
            created_at__gte=timezone.now() - timedelta(minutes=1)
        ).count()
        
        if recent_comments >= 3:
            messages.warning(
                request, 
                "Siz juda ko'p izoh qoldirmoqdasiz. 1 daqiqa kutib turing."
            )
            return redirect('news_detail', pk=self.object.pk)
        
        # 4. Formani to'ldiramiz
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            
            # 5. Uzunlik tekshiruvi
            if len(comment.body.strip()) < 10:
                messages.error(request, "Izoh kamida 10 ta belgidan iborat bo'lishi kerak!")
                context = self.get_context_data()
                context['comment_form'] = form
                return self.render_to_response(context)
            
            # 6. Spam tekshiruvi
            spam_words = ['spam', 'viagra', 'casino']
            if any(word in comment.body.lower() for word in spam_words):
                messages.error(request, "Izohingizda taqiqlangan so'zlar mavjud!")
                context = self.get_context_data()
                context['comment_form'] = form
                return self.render_to_response(context)
            
            # 7. Ma'lumotlarni qo'shamiz
            comment.news = self.object
            comment.user = request.user
            
            # 8. Bazaga saqlaymiz
            comment.save()
            
            # 9. Success message
            messages.success(request, "Rahmat! Izohingiz muvaffaqiyatli qo'shildi.")
            
            # 10. Sahifani yangilaymiz
            return redirect('news_detail', pk=self.object.pk)
        
        # Agar forma xato bo'lsa
        messages.error(request, "Formada xatolar bor. Qaytadan tekshiring.")
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)
```

---

### Topshiriq 10: URLs ni tekshirish ⭐

**Maqsad:** URL configuration to'g'ri ishlashini ta'minlash

**10.1. news/urls.py**

```python
from django.urls import path
from . import views

urlpatterns = [
    # ... boshqa URL'lar
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='news_detail'),
]
```

**10.2. Asosiy config/urls.py**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    # ... boshqa URL'lar
]
```

---

## Mustaqil vazifa

### Vazifa 1: Izohni tahrirlash funksiyasi ⭐⭐⭐⭐⭐

Foydalanuvchi o'z izohini tahrirlashi mumkin bo'lgan funksiya yarating.

**Qadamlar:**

1. `news/views.py` da yangi view yarating:
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # Faqat o'z izohini tahrirlashi mumkin
    if comment.user != request.user:
        messages.error(request, "Siz bu izohni tahrirlay olmaysiz!")
        return redirect('news_detail', pk=comment.news.pk)
    
    # TODO: POST so'rovni qayta ishlang
    # TODO: Formani ko'rsating
    
    pass
```

2. URL qo'shing:
```python
path('comment/<int:pk>/edit/', views.edit_comment, name='edit_comment'),
```

3. Template yarating: `templates/news/edit_comment.html`

<details>
<summary>To'liq yechim</summary>

```python
@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # Faqat o'z izohini tahrirlashi mumkin
    if comment.user != request.user:
        messages.error(request, "Siz bu izohni tahrirlay olmaysiz!")
        return redirect('news_detail', pk=comment.news.pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Izohingiz tahrirlandi!")
            return redirect('news_detail', pk=comment.news.pk)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment
    }
    return render(request, 'news/edit_comment.html', context)
```
</details>

---

### Vazifa 2: Izohni o'chirish funksiyasi ⭐⭐⭐⭐

Foydalanuvchi o'z izohini o'chirishi mumkin bo'lgan funksiya yarating.

**Ko'rsatma:**
- `@login_required` dekoratoridan foydalaning
- Foydalanuvchi faqat o'z izohini o'chirishi mumkin
- POST metodida o'chirish amalga oshiriladi
- Success message ko'rsating

<details>
<summary>Yechim</summary>

```python
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    
    # Faqat o'z izohini o'chirishi mumkin
    if comment.user != request.user:
        messages.error(request, "Siz bu izohni o'chira olmaysiz!")
        return redirect('news_detail', pk=comment.news.pk)
    
    if request.method == 'POST':
        news_pk = comment.news.pk
        comment.delete()
        messages.success(request, "Izohingiz o'chirildi!")
        return redirect('news_detail', pk=news_pk)
    
    return render(request, 'news/delete_comment.html', {'comment': comment})
```

URL:
```python
path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
```
</details>

---

### Vazifa 3: Izohga javob berish (nested comments) ⭐⭐⭐⭐⭐

Izohga izoh qoldirish funksiyasini yarating (optional, qiyin).

**Qadamlar:**

1. Comment modeliga `parent` maydoni qo'shing:
```python
class Comment(models.Model):
    # ... boshqa fieldlar
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE,
        related_name='replies'
    )
```

2. Migration yarating va ishga tushiring

3. View'ni yangilang

4. Template'da nested izohlarni ko'rsating

---

## Tekshirish ro'yxati (Checklist)

Quyidagi barcha funksiyalar ishlashini tekshiring:

- [ ] Yangilik sahifasi ochiladi
- [ ] Izohlar ko'rinadi (agar mavjud bo'lsa)
- [ ] Izoh formasini ko'rish mumkin
- [ ] Tizimga kirmagan foydalanuvchi izoh yoza olmaydi
- [ ] Tizimga kirgan foydalanuvchi izoh yozishi mumkin
- [ ] Izoh yozilgandan keyin success message ko'rinadi
- [ ] Yangi izoh darhol ko'rinadi
- [ ] Bo'sh izoh yozib bo'lmaydi
- [ ] 10 ta belgidan kam izoh yozib bo'lmaydi
- [ ] Spam so'zli izoh qabul qilinmaydi
- [ ] 1 daqiqada 3 ta izohdan ko'p yozib bo'lmaydi
- [ ] Forma xatolari to'g'ri ko'rinadi
- [ ] CSRF token ishlaydi

---

## Umumiy xatolar va yechimlar

### Xato 1: `'User' object has no attribute 'comments'`

**Sabab:** Comment modelida `related_name` noto'g'ri yoki yo'q

**Yechim:**
```python
news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments')
```

---

### Xato 2: `CSRF verification failed`

**Sabab:** Template'da `{% csrf_token %}` yo'q

**Yechim:**
```html
<form method="post">
    {% csrf_token %}
    ...
</form>
```

---

### Xato 3: `IntegrityError: NOT NULL constraint failed`

**Sabab:** `user` yoki `news` fieldi berilmagan

**Yechim:**
```python
comment = form.save(commit=False)
comment.news = self.object
comment.user = request.user
comment.save()
```

---

### Xato 4: Messages ko'rinmayapti

**Sabab:** Base template'da message block yo'q

**Yechim:**
```html
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

---

## Qo'shimcha maslahatlar

### 💡 Maslahat 1: Code organization
Agar `post` metodi juda uzun bo'lib qolsa, alohida metodlarga bo'ling:

```python
def post(self, request, *args, **kwargs):
    if not self._is_authenticated(request):
        return self._redirect_to_login()
    
    if self._is_rate_limited(request):
        return self._show_rate_limit_message()
    
    # ... davom etadi
```

### 💡 Maslahat 2: Testing
View'ni test qilish uchun:

```python
# news/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import News, Comment

class CommentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='12345')
        self.news = News.objects.create(title='Test', body='Test body')
    
    def test_add_comment_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            f'/news/{self.news.pk}/',
            {'body': 'Test comment'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)
```

### 💡 Maslahat 3: Logging
Muhim harakatlarni log qiling:

```python
import logging

logger = logging.getLogger(__name__)

def post(self, request, *args, **kwargs):
    # ...
    if form.is_valid():
        comment.save()
        logger.info(f"New comment added by {request.user.username} on news {self.object.pk}")
```

---

## Yakuniy natija

Ushbu amaliyotni tugatganingizdan so'ng:
- ✅ To'liq ishlaydigan izoh tizimiga ega bo'lasiz
- ✅ POST so'rovlarni qayta ishlashni bilasiz
- ✅ Form validatsiyasi va xatolarni boshqarishni o'rganasiz
- ✅ Xavfsizlik choralari (CSRF, autentifikatsiya, rate limiting) qo'llashni bilasiz
- ✅ Django messages framework bilan ishlashni o'rganasiz

Keyingi darsda **template qismini** yozamiz va izohlarni chiroyli ko'rinishda chiqaramiz!

**Omad yor bo'lsin! 🚀**