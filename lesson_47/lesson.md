# Lesson 47: Ko'rishlar sonini aniqlash

## Kirish

Ushbu darsda biz yangiliklar saytimizga **ko'rishlar sonini aniqlash** (views count) funksiyasini qo'shamiz. Bu funksiya har bir yangilik sahifasi necha marta ko'rilganini hisoblab beradi va bu ma'lumot orqali eng mashhur yangiliklarni aniqlashimiz mumkin bo'ladi.

## Maqsad

- News modeliga `views_count` maydonini qo'shish
- Har safar yangilik ochilganda ko'rishlar sonini avtomatik oshirish
- Session orqali bir foydalanuvchi tomonidan takroriy ko'rishlarni oldini olish
- Admin panelda ko'rishlar sonini ko'rsatish

---

## 1-bosqich: News modeliga `views_count` maydonini qo'shish

Birinchi navbatda, News modelimizga yangilik necha marta ko'rilganini saqlaydigan maydon qo'shishimiz kerak.

### `news/models.py` faylini yangilash

```python
from django.db import models
from django.urls import reverse
from django.utils import timezone

class News(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    body = models.TextField()
    image = models.ImageField(upload_to='news/images', blank=True, null=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='news'
    )
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_choices=2,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT
    )
    
    # Yangi maydon: Ko'rishlar soni
    views_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-publish_time']
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news_detail', args=[self.slug])
```

### Tushuntirish:

- `views_count = models.IntegerField(default=0)` - Bu maydon yangilik ko'rishlar sonini saqlaydi
- `default=0` - Yangi yangilik yaratilganda ko'rishlar soni 0 dan boshlanadi
- `IntegerField` - Butun son tipidagi maydon (1, 2, 3...)

---

## 2-bosqich: Migratsiya yaratish va ishga tushirish

Model o'zgarganligi uchun migratsiya yaratishimiz va uni ishga tushirishimiz kerak.

### Terminal buyruqlari:

```bash
# Migratsiya faylini yaratish
python manage.py makemigrations

# Migratsiyani ishga tushirish
python manage.py migrate
```

### Natija:

```
Migrations for 'news':
  news/migrations/0005_news_views_count.py
    - Add field views_count to news

Running migrations:
  Applying news.0005_news_views_count... OK
```

---

## 3-bosqich: Admin panelda ko'rishlar sonini ko'rsatish

Admin panelda yangiliklar ro'yxatida ko'rishlar sonini ko'rsatamiz.

### `news/admin.py` faylini yangilash

```python
from django.contrib import admin
from .models import News, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'status', 'views_count', 'publish_time']
    list_filter = ['status', 'category', 'publish_time']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    ordering = ['-publish_time', '-views_count']
    readonly_fields = ['views_count']  # Admindan o'zgartirib bo'lmaydigan qilish
```

### Tushuntirish:

- `list_display` ro'yxatiga `'views_count'` qo'shdik - endi jadvalda ko'rsatiladi
- `readonly_fields = ['views_count']` - Bu maydonni admin panelda faqat o'qish uchun qildik, chunki u avtomatik hisoblanadi
- `ordering` ga `'-views_count'` qo'shdik - eng ko'p ko'rilgan yangiliklar birinchi chiqadi

---

## 4-bosqich: Views qismida ko'rishlar sonini oshirish

Yangilik sahifasi ochilganda ko'rishlar sonini oshirishimiz kerak. Buni `NewsDetailView` da amalga oshiramiz.

### `news/views.py` faylini yangilash

```python
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

from .models import News, Category
from .forms import ContactForm, CommentForm

# ... boshqa viewlar ...

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_object(self, queryset=None):
        """
        Yangilikni olish va ko'rishlar sonini oshirish
        """
        # Yangilikni slug orqali olish
        obj = get_object_or_404(News, slug=self.kwargs['slug'], status=News.StatusChoices.PUBLISHED)
        
        # Session'da bu yangilik ko'rilganmi tekshirish
        session_key = f'viewed_news_{obj.pk}'
        
        if not self.request.session.get(session_key, False):
            # Agar ko'rilmagan bo'lsa, ko'rishlar sonini oshirish
            obj.views_count += 1
            obj.save(update_fields=['views_count'])
            
            # Session'ga belgi qo'yish
            self.request.session[session_key] = True
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(active=True)
        return context
```

### Tushuntirish:

#### `get_object()` metodini override qildik:

1. **Yangilikni olish:**
   ```python
   obj = get_object_or_404(News, slug=self.kwargs['slug'], status=News.StatusChoices.PUBLISHED)
   ```
   - Slug orqali yangilikni topamiz
   - Faqat published holatdagi yangiliklarni ko'rsatamiz

2. **Session kalitini yaratish:**
   ```python
   session_key = f'viewed_news_{obj.pk}'
   ```
   - Har bir yangilik uchun noyob session kaliti yaratiladi
   - Masalan: `viewed_news_5` (5 - yangilik ID si)

3. **Takroriy ko'rishlarni oldini olish:**
   ```python
   if not self.request.session.get(session_key, False):
   ```
   - Session'da bu yangilik ko'rilganmi tekshiramiz
   - Agar ko'rilmagan bo'lsa (False), ko'rishlar sonini oshiramiz

4. **Ko'rishlar sonini oshirish:**
   ```python
   obj.views_count += 1
   obj.save(update_fields=['views_count'])
   ```
   - `+=` operatori bilan sonni 1 ga oshiramiz
   - `update_fields=['views_count']` - faqat shu maydonni yangilaydi (tezroq ishlaydi)

5. **Session'ga belgi qo'yish:**
   ```python
   self.request.session[session_key] = True
   ```
   - Foydalanuvchi ushbu yangilikni ko'rganini session'ga saqlaymiz
   - Keyingi marta yana kirsa, ko'rishlar soni oshmaydI

---

## 5-bosqich: Session sozlamalari

Session ishlashi uchun Django settings.py da session middleware yoqilgan bo'lishi kerak (odatda default holatda yoqilgan).

### `config/settings.py` faylini tekshirish

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Bu yoqilgan bo'lishi kerak
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Session sozlamalari (ixtiyoriy)
SESSION_COOKIE_AGE = 86400  # 1 kun (sekundlarda)
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
```

### Tushuntirish:

- `SESSION_COOKIE_AGE = 86400` - Session 1 kun davom etadi (24 * 60 * 60 sekund)
- `SESSION_SAVE_EVERY_REQUEST = False` - Har bir so'rovda session saqlanmaydi (tezroq ishlaydi)
- `SESSION_EXPIRE_AT_BROWSER_CLOSE = False` - Brauzer yopilganda session o'chmaydI

---

## 6-bosqich: Test qilish

### 1. Admin panelda tekshirish:

1. Admin panelga kiring: `http://127.0.0.1:8000/admin/`
2. News bo'limiga o'ting
3. Ko'rishlar soni ustunini ko'rasiz (hamma 0 bo'ladi)

### 2. Yangilik sahifasida test qilish:

1. Biror yangilik sahifasini oching: `http://127.0.0.1:8000/news/yangilik-slug/`
2. Admin panelga qaytib, yangilikni tekshiring - ko'rishlar soni 1 ga oshgan bo'lishi kerak
3. Sahifani yangilang (F5) - ko'rishlar soni o'zgarmaydi (session ishlayapti)
4. Brauzerni yoping va qayta oching - ko'rishlar soni yana 1 ga oshadi

---

## Session haqida qo'shimcha ma'lumot

### Session nima?

Session - bu foydalanuvchi haqidagi ma'lumotlarni serverda saqlaydigan mexanizm. Har bir foydalanuvchiga noyob session ID beriladi va bu ID cookie orqali saqlanadi.

### Session qanday ishlaydi?

```
1. Foydalanuvchi saytga kiradi
   → Django unga session ID beradi
   
2. Session ID cookie'da saqlanadi
   → Brauzer har bir so'rovda bu ID ni yuboradi
   
3. Django session ID orqali foydalanuvchini taniydi
   → Session ma'lumotlarini oladi
   
4. Biz session'ga ma'lumot yozamiz
   → viewed_news_5 = True
   
5. Keyingi safar foydalanuvchi kirganda
   → Django session'dan ma'lumotni o'qiydi
   → Ko'rishlar sonini oshirmaydi
```

### Session afzalliklari:

- ✅ Har bir foydalanuvchi uchun alohida
- ✅ Serverda xavfsiz saqlanadi
- ✅ Vaqtinchalik ma'lumotlarni saqlash uchun ideal
- ✅ Autentifikatsiya uchun ishlatiladi

### Session kamchiliklari:

- ❌ Server xotirasini band qiladi
- ❌ Ko'p foydalanuvchilar bo'lsa ko'p joy oladi
- ❌ Brauzer cookie'larini o'chirsa, session yo'qoladi

---

## Muqobil yondashuvlar

### 1. IP address orqali kuzatish

```python
def get_client_ip(request):
    """Foydalanuvchi IP addressini olish"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class NewsDetailView(DetailView):
    # ...
    
    def get_object(self, queryset=None):
        obj = get_object_or_404(News, slug=self.kwargs['slug'])
        
        # IP address orqali tekshirish
        ip_address = get_client_ip(self.request)
        session_key = f'viewed_news_{obj.pk}_{ip_address}'
        
        if not self.request.session.get(session_key, False):
            obj.views_count += 1
            obj.save(update_fields=['views_count'])
            self.request.session[session_key] = True
        
        return obj
```

**Afzalligi:** Brauzer cookie o'chirilsa ham ishlaydi
**Kamchiligi:** Bir IP'dan ko'p foydalanuvchi bo'lishi mumkin

### 2. Alohida ViewLog modeli yaratish

```python
# models.py
class NewsViewLog(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Ko\'rish tarixi'
        verbose_name_plural = 'Ko\'rish tarixi'
```

**Afzalligi:** To'liq statistika, kim, qachon ko'rgan
**Kamchiligi:** Ma'lumotlar bazasi tez to'ladi

---

## Xulosa

Ushbu darsda biz:

1. ✅ News modeliga `views_count` maydonini qo'shdik
2. ✅ Migratsiya yaratdik va ishga tushirdik
3. ✅ Admin panelda ko'rishlar sonini ko'rsatdik
4. ✅ `get_object()` metodini override qilib, ko'rishlar sonini oshirdik
5. ✅ Session orqali takroriy ko'rishlarni oldini oldik
6. ✅ Session sozlamalarini o'rganib chiqdik

Keyingi darsda ko'rishlar sonini template'da chiqarishni o'rganamiz!

---

## Best Practices

### ✅ To'g'ri yondashuv:

1. **update_fields ishlatish:**
   ```python
   obj.save(update_fields=['views_count'])  # Tezroq
   ```

2. **Session'dan to'g'ri foydalanish:**
   ```python
   if not self.request.session.get(session_key, False):
       # Ko'rishlar sonini oshirish
   ```

3. **readonly_fields ishlatish:**
   ```python
   readonly_fields = ['views_count']  # Admin'dan o'zgartirilmasin
   ```

### ❌ Xato yondashuvlar:

1. **Har safar save() chaqirish:**
   ```python
   obj.save()  # Barcha maydonlar yangilanadi (sekinroq)
   ```

2. **Session tekshirmasdan oshirish:**
   ```python
   obj.views_count += 1  # Har safar oshadi (xato)
   ```

3. **views_count'ni admin'dan o'zgartirish:**
   ```python
   # Admin panelda qo'lda o'zgartirish noto'g'ri
   ```

---

## Maslahatlar

💡 **Performance uchun:** Ko'p foydalanuvchilar bo'lsa, Redis yoki Memcached ishlatish yaxshiroq

💡 **Analytics uchun:** Google Analytics yoki Yandex Metrica integratsiya qilish mumkin

💡 **Testing uchun:** Session'ni tozalash: `python manage.py clearsessions`

💡 **Production'da:** Session'ni database'da emas, cache'da saqlash tezroq