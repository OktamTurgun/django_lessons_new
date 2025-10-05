# Lesson 47: Ko'rishlar sonini aniqlash - Amaliy mashg'ulot

## Vazifalar ro'yxati

Ushbu amaliy mashg'ulotda siz quyidagi vazifalarni bajarasiz:

1. ✅ News modeliga views_count maydonini qo'shish
2. ✅ Migratsiya yaratish va ishga tushirish
3. ✅ Admin panelni sozlash
4. ✅ NewsDetailView'da ko'rishlar sonini oshirish
5. ✅ Session orqali takroriy ko'rishlarni oldini olish
6. ✅ Test qilish va natijalarni tekshirish

---

## Vazifa 1: News modelini yangilash

### 1.1. `news/models.py` faylini oching

### 1.2. News modeliga views_count maydonini qo'shing:

```python
class News(models.Model):
    # Mavjud maydonlar...
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    body = models.TextField()
    # ... boshqa maydonlar ...
    
    # Yangi maydon qo'shing
    views_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-publish_time']
    
    def __str__(self):
        return self.title
```

### 1.3. Faylni saqlang (Ctrl+S yoki Cmd+S)

### ✅ Tekshirish:
- `views_count` maydoni to'g'ri yozilganmi?
- `default=0` qo'yilganmi?
- `IntegerField` ishlatilganmi?

---

## Vazifa 2: Migratsiya yaratish

### 2.1. Terminal oching (VS Code'da: Ctrl+` yoki View → Terminal)

### 2.2. Migratsiya faylini yarating:

```bash
python manage.py makemigrations
```

### 2.3. Natijani o'qing:

```
Migrations for 'news':
  news/migrations/0005_news_views_count.py
    - Add field views_count to news
```

### 2.4. Migratsiyani ishga tushiring:

```bash
python manage.py migrate
```

### 2.5. Natijani tekshiring:

```
Running migrations:
  Applying news.0005_news_views_count... OK
```

### ✅ Tekshirish:
- Migratsiya fayli yaratildimi? (`news/migrations/` papkasida)
- Xatolik bo'lmadimi?
- Database yangilandimi?

---

## Vazifa 3: Admin panelni sozlash

### 3.1. `news/admin.py` faylini oching

### 3.2. NewsAdmin klassini yangilang:

```python
from django.contrib import admin
from .models import News, Category

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'status', 'views_count', 'publish_time']
    list_filter = ['status', 'category', 'publish_time']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    ordering = ['-publish_time', '-views_count']
    readonly_fields = ['views_count']  # Bu qatorni qo'shing
```

### 3.3. Faylni saqlang

### 3.4. Admin panelni tekshiring:

1. Serverni ishga tushiring:
   ```bash
   python manage.py runserver
   ```

2. Admin panelga kiring: `http://127.0.0.1:8000/admin/`

3. News bo'limiga o'ting va yangiliklar ro'yxatini ko'ring

### ✅ Tekshirish:
- `views_count` ustuni ko'rinmoqdami?
- Barcha yangiliklar uchun 0 qiymat ko'rsatilganmi?
- Yangilikni tahrirlashda `views_count` o'zgartirish mumkin emasmi?

---

## Vazifa 4: NewsDetailView'ni yangilash

### 4.1. `news/views.py` faylini oching

### 4.2. NewsDetailView klassini to'liq yangilang:

```python
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    
    def get_object(self, queryset=None):
        """
        Yangilikni olish va ko'rishlar sonini oshirish
        """
        # 1. Yangilikni slug orqali olish
        obj = get_object_or_404(
            News, 
            slug=self.kwargs['slug'], 
            status=News.StatusChoices.PUBLISHED
        )
        
        # 2. Session kalitini yaratish
        session_key = f'viewed_news_{obj.pk}'
        
        # 3. Session'da bu yangilik ko'rilganmi tekshirish
        if not self.request.session.get(session_key, False):
            # 4. Ko'rishlar sonini oshirish
            obj.views_count += 1
            obj.save(update_fields=['views_count'])
            
            # 5. Session'ga belgi qo'yish
            self.request.session[session_key] = True
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # Izohlar uchun context (agar mavjud bo'lsa)
        if hasattr(self, 'object') and hasattr(self.object, 'comments'):
            context['comments'] = self.object.comments.filter(active=True)
        return context
```

### 4.3. Faylni saqlang

### ✅ Tekshirish:
- `get_object()` metodi to'g'ri override qilindimi?
- Barcha 5 ta qadam yozilganmi?
- `update_fields=['views_count']` ishlatildimi?

---

## Vazifa 5: Test qilish

### 5.1. Birinchi test: Admin paneldan tekshirish

1. Admin panelga o'ting: `http://127.0.0.1:8000/admin/news/news/`
2. Birinchi yangilikni toping va uning ko'rishlar sonini yozing (masalan: 0)
3. Yangilik slug'ini yozing (masalan: "python-dasturlash")

### 5.2. Ikkinchi test: Yangilik sahifasiga kirish

1. Yangilik sahifasini oching: `http://127.0.0.1:8000/news/python-dasturlash/`
2. Sahifa to'liq ochilganini tekshiring

### 5.3. Uchinchi test: Ko'rishlar sonini tekshirish

1. Admin panelga qaytiq
2. News ro'yxatini yangilang (F5)
3. Ko'rishlar soni 1 ga oshganini tekshiring

### 5.4. To'rtinchi test: Session ishlashini tekshirish

1. Yangilik sahifasini yana oching (F5)
2. Admin panelni tekshiring
3. Ko'rishlar soni o'zgarmaganini tekshiring (hali 1 bo'lishi kerak)

### 5.5. Beshinchi test: Yangi session

1. Brauzerni yoping (butunlay)
2. Brauzerni qayta oching
3. Yangilik sahifasini oching
4. Admin panelni tekshiring - ko'rishlar soni 2 ga oshgan bo'lishi kerak

### ✅ Tekshirish natijalari:

Test | Kutilayotgan natija | Sizning natijangiz
-----|---------------------|-------------------
Birinchi kirish | views_count = 1 | 
Sahifani yangilash | views_count = 1 (o'zgarmaydi) | 
Brauzer yopilgandan keyin | views_count = 2 | 

---

## Vazifa 6: Boshqa yangiliklarni test qilish

### 6.1. Ikkinchi yangilikni toping

Admin panelda boshqa yangilikni tanlang

### 6.2. Test qiling:

1. Yangilik sahifasini oching
2. Ko'rishlar soni 1 ga oshganini tekshiring
3. Sahifani yangilang - ko'rishlar soni o'zgarmaydi

### 6.3. Bir necha yangiliklarni test qiling:

- Kamida 3 ta yangilikni oching
- Har birining ko'rishlar soni alohida hisoblanishini tekshiring

---

## Vazifa 7: Session sozlamalarini tekshirish (Qo'shimcha)

### 7.1. `config/settings.py` faylini oching

### 7.2. MIDDLEWARE ro'yxatini toping va tekshiring:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Bu bo'lishi kerak
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

### 7.3. Session sozlamalarini qo'shing (agar yo'q bo'lsa):

```python
# Session sozlamalari
SESSION_COOKIE_AGE = 86400  # 1 kun
SESSION_SAVE_EVERY_REQUEST = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
```

### ✅ Tekshirish:
- SessionMiddleware yoqilganmi?
- Session sozlamalari mavjudmi?

---

## Vazifa 8: Shell orqali test qilish (Qo'shimcha)

### 8.1. Django shell'ni oching:

```bash
python manage.py shell
```

### 8.2. Yangiliklarni tekshiring:

```python
from news.models import News

# Barcha yangiliklar ko'rishlar sonini ko'rish
news_list = News.objects.all()
for news in news_list:
    print(f"{news.title}: {news.views_count} ko'rishlar")
```

### 8.3. Ko'rishlar sonini qo'lda o'zgartirish:

```python
# Birinchi yangilikni olish
news = News.objects.first()
print(f"Avvalgi qiymat: {news.views_count}")

# Ko'rishlar sonini oshirish
news.views_count += 5
news.save(update_fields=['views_count'])

print(f"Yangi qiymat: {news.views_count}")
```

### 8.4. Shell'dan chiqing:

```python
exit()
```

---

## Vazifa 9: Muammolarni hal qilish

### Agar ko'rishlar soni oshmaydigan bo'lsa:

#### 9.1. get_object() metodini tekshiring

```python
# Bu kod views.py'da to'g'ri joylashganmi?
def get_object(self, queryset=None):
    obj = get_object_or_404(News, slug=self.kwargs['slug'])
    # ...
```

#### 9.2. Session ishlayotganini tekshiring

```python
# Shell'da:
from django.contrib.sessions.models import Session

# Barcha sessionlar
sessions = Session.objects.all()
print(f"Jami sessionlar: {sessions.count()}")
```

#### 9.3. Migratsiya to'g'ri bajarilganini tekshiring

```bash
python manage.py showmigrations news
```

Natija:
```
news
 [X] 0001_initial
 [X] 0002_category
 [X] 0003_news_category
 [X] 0004_alter_news_status
 [X] 0005_news_views_count  # Bu bo'lishi kerak
```

#### 9.4. Database'ni tekshiring

```bash
python manage.py dbshell
```

```sql
-- SQLite uchun:
PRAGMA table_info(news_news);

-- views_count ustuni bormi?
```

### Agar har safar ko'rishlar soni oshib ketsa:

#### 9.5. Session tekshiruvini qo'shing

```python
# views.py'da
def get_object(self, queryset=None):
    obj = get_object_or_404(News, slug=self.kwargs['slug'])
    
    session_key = f'viewed_news_{obj.pk}'
    
    # Debug uchun
    print(f"Session key: {session_key}")
    print(f"Session'da mavjudmi: {self.request.session.get(session_key, False)}")
    
    if not self.request.session.get(session_key, False):
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        self.request.session[session_key] = True
        print("Ko'rishlar soni oshirildi!")
    else:
        print("Allaqachon ko'rilgan")
    
    return obj
```

---

## Vazifa 10: Qo'shimcha funksiyalar (Ixtiyoriy)

### 10.1. Eng ko'p ko'rilgan yangiliklar

#### `news/views.py` faylida yangi view yarating:

```python
from django.views.generic import ListView

class PopularNewsListView(ListView):
    model = News
    template_name = 'news/popular_news.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        return News.objects.filter(
            status=News.StatusChoices.PUBLISHED
        ).order_by('-views_count')[:10]  # Eng ko'p ko'rilgan 10 ta
```

#### `news/urls.py` ga URL qo'shing:

```python
from .views import PopularNewsListView

urlpatterns = [
    # ... mavjud URL'lar
    path('popular/', PopularNewsListView.as_view(), name='popular_news'),
]
```

#### Template yarating `templates/news/popular_news.html`:

```html
{% extends 'base.html' %}

{% block content %}
<div class="container mt-4">
    <h2>Eng Ko'p O'qilgan Yangiliklar</h2>
    
    <div class="row">
        {% for news in news_list %}
        <div class="col-md-6 mb-4">
            <div class="card">
                {% if news.image %}
                <img src="{{ news.image.url }}" class="card-img-top" alt="{{ news.title }}">
                {% endif %}
                <div class="card-body">
                    <h5 class="card-title">{{ news.title }}</h5>
                    <p class="card-text">{{ news.body|truncatewords:20 }}</p>
                    <p class="text-muted">
                        <small>
                            👁️ {{ news.views_count }} ko'rishlar | 
                            📅 {{ news.publish_time|date:"d.m.Y" }}
                        </small>
                    </p>
                    <a href="{{ news.get_absolute_url }}" class="btn btn-primary">Batafsil</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

#### Test qiling:

1. Brauzerni oching: `http://127.0.0.1:8000/news/popular/`
2. Eng ko'p ko'rilgan yangiliklar ko'rsatilishini tekshiring

---

### 10.2. Ko'rishlar sonini template context'ga qo'shish

#### `news/context_processors.py` faylini yarating (agar yo'q bo'lsa):

```python
from .models import News

def stats_context(request):
    """
    Global statistika ma'lumotlari
    """
    total_views = sum(news.views_count for news in News.objects.all())
    most_viewed = News.objects.filter(
        status=News.StatusChoices.PUBLISHED
    ).order_by('-views_count').first()
    
    return {
        'total_news_views': total_views,
        'most_viewed_news': most_viewed,
    }
```

#### `config/settings.py` ga context processor qo'shing:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'news.context_processors.stats_context',  # Qo'shing
            ],
        },
    },
]
```

#### Template'da ishlatish:

```html
<!-- base.html yoki boshqa template'da -->
<footer>
    <p>Jami ko'rishlar: {{ total_news_views }}</p>
    {% if most_viewed_news %}
    <p>Eng mashhur: 
        <a href="{{ most_viewed_news.get_absolute_url }}">
            {{ most_viewed_news.title }} ({{ most_viewed_news.views_count }} ko'rishlar)
        </a>
    </p>
    {% endif %}
</footer>
```

---

### 10.3. Admin panelda filtrlash va saralash

#### `news/admin.py` ni yanada yaxshilang:

```python
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'title', 
        'category', 
        'status', 
        'views_count', 
        'publish_time',
        'colored_views'  # Rangdagi ko'rishlar
    ]
    list_filter = ['status', 'category', 'publish_time']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish_time'
    ordering = ['-views_count']  # Eng ko'p ko'rilganlar birinchi
    readonly_fields = ['views_count', 'created_time', 'updated_time']
    
    def colored_views(self, obj):
        """Ko'rishlar sonini rangda ko'rsatish"""
        from django.utils.html import format_html
        
        if obj.views_count > 100:
            color = 'green'
        elif obj.views_count > 50:
            color = 'orange'
        else:
            color = 'red'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.views_count
        )
    
    colored_views.short_description = 'Ko\'rishlar (rangda)'
```

---

## Vazifa 11: Test natijalarini tahlil qilish

### 11.1. Ma'lumotlar to'plash

Kamida 5 ta yangilikni test qiling va natijalarni yozing:

| № | Yangilik nomi | Birinchi kirish | Ikkinchi kirish | Uchinchi kirish |
|---|---------------|-----------------|-----------------|-----------------|
| 1 | Python dasturlash | 1 | 1 | 2 |
| 2 | Django framework | 1 | 1 | 2 |
| 3 | ... | ... | ... | ... |

### 11.2. Tahlil savollari:

1. **Session ishlayaptimi?**
   - Ha / Yo'q
   - Dalil: _______________

2. **Ko'rishlar soni to'g'ri hisoblanmoqdami?**
   - Ha / Yo'q
   - Qaysi holatda xato yuz berdi: _______________

3. **Admin panelda to'g'ri ko'rsatilmoqdami?**
   - Ha / Yo'q
   - Qanday muammo bor: _______________

---

## Vazifa 12: Code review (O'z kodingizni tekshirish)

### 12.1. Models.py tekshiruvi

- [ ] `views_count = models.IntegerField(default=0)` mavjudmi?
- [ ] Maydon nomi to'g'ri yozilganmi? (views_count, views_counter emas)
- [ ] Default qiymat 0 mi?

### 12.2. Views.py tekshiruvi

- [ ] `get_object()` metodi override qilinganmi?
- [ ] `session_key` to'g'ri yaratilganmi?
- [ ] Session tekshiruvi bormi?
- [ ] `update_fields=['views_count']` ishlatilganmi?
- [ ] Session'ga belgi qo'yilganmi?

### 12.3. Admin.py tekshiruvi

- [ ] `list_display` da `views_count` bormi?
- [ ] `readonly_fields` da `views_count` bormi?
- [ ] `ordering` da `-views_count` bormi?

### 12.4. Migratsiya tekshiruvi

- [ ] Migratsiya fayli yaratilganmi?
- [ ] Migratsiya to'g'ri nomlangan mi? (0005_news_views_count.py)
- [ ] Migratsiya ishga tushirilganmi?

---

## Vazifa 13: Xatolarni tuzatish

### Xato 1: "views_count" attribute mavjud emas

**Xato xabari:**
```
'News' object has no attribute 'views_count'
```

**Yechim:**
```bash
# Migratsiya qilishni unutgansiz
python manage.py makemigrations
python manage.py migrate
```

### Xato 2: Ko'rishlar soni har doim oshib ketadi

**Sabab:** Session tekshiruvi ishlamayapti

**Yechim:**
```python
# views.py'da session_key to'g'ri yaratilganini tekshiring
session_key = f'viewed_news_{obj.pk}'  # obj.id emas, obj.pk

# Session middleware yoqilganini tekshiring
# settings.py da SessionMiddleware bormi?
```

### Xato 3: Admin panelda views_count ko'rinmaydi

**Sabab:** list_display yangilanmagan

**Yechim:**
```python
# admin.py da
list_display = ['id', 'title', 'views_count']  # views_count qo'shing
```

### Xato 4: Migratsiya xatoligi

**Xato xabari:**
```
You are trying to add a non-nullable field 'views_count' to news without a default
```

**Yechim:**
```python
# models.py da default qo'shing
views_count = models.IntegerField(default=0)  # default=0 muhim
```

---

## Vazifa 14: Yakuniy test

### 14.1. Barcha funksiyalarni test qiling:

1. **Model test:**
   - [ ] views_count maydoni mavjud
   - [ ] Default qiymat 0

2. **Admin test:**
   - [ ] Ko'rishlar soni ko'rsatiladi
   - [ ] Readonly qilingan
   - [ ] Saralash ishlaydi

3. **View test:**
   - [ ] Birinchi kirish: +1
   - [ ] Takror kirish: +0
   - [ ] Brauzer yopilgandan keyin: +1

4. **Session test:**
   - [ ] Session saqlanadi
   - [ ] Takror kirish oldini oladi
   - [ ] Har xil yangiliklar uchun alohida ishlaydi

### 14.2. Screenshot oling:

- Admin panelda ko'rishlar soni ko'rsatilgan screenshot
- Yangilik sahifasi screenshot
- Shell'da views_count qiymatlari screenshot

---

## Qo'shimcha mashqlar (Challenge)

### Challenge 1: Haftalik statistika

Ko'rishlar sonini oxirgi 7 kun uchun filter qiling:

```python
from django.utils import timezone
from datetime import timedelta

# Oxirgi 7 kun ichida eng ko'p ko'rilgan
week_ago = timezone.now() - timedelta(days=7)
popular_this_week = News.objects.filter(
    publish_time__gte=week_ago
).order_by('-views_count')[:5]
```

### Challenge 2: Foydalanuvchi uchun statistika

Foydalanuvchi qancha yangilik ko'rganini hisoblang:

```python
def user_stats(request):
    """Foydalanuvchi ko'rgan yangiliklar soni"""
    viewed_count = 0
    for key in request.session.keys():
        if key.startswith('viewed_news_'):
            viewed_count += 1
    return viewed_count
```

### Challenge 3: API endpoint yaratish

Ko'rishlar sonini JSON formatda qaytaring:

```python
from django.http import JsonResponse

def news_stats_api(request):
    news_list = News.objects.all().values('id', 'title', 'views_count')
    return JsonResponse(list(news_list), safe=False)
```

---

## Yakuniy Checklist

Vazifani yakunlashdan oldin tekshiring:

### Kod sifati:
- [ ] Barcha fayllar saqlangan
- [ ] Kod tozalangan (debug print() lar o'chirilgan)
- [ ] Izohlar yozilgan (zarur joylarda)

### Funksionallik:
- [ ] Ko'rishlar soni to'g'ri hisoblanadi
- [ ] Session ishlaydi
- [ ] Admin panelda ko'rsatiladi
- [ ] Xatoliksiz ishlaydi

### Testlar:
- [ ] Kamida 5 ta yangilikda test qilindi
- [ ] Turli senariylarda tekshirildi
- [ ] Natijalar to'g'ri

### Dokumentatsiya:
- [ ] Code izohlar yozildi
- [ ] README'ga ma'lumot qo'shildi (agar kerak bo'lsa)

---

## Keyingi qadamlar

Ushbu darsni tugatgandan so'ng:

1. ✅ **Lesson 48** - Ko'rishlar sonini template'da aks ettirish
2. ✅ **Lesson 49** - Izohlar sonini template'dan chiqarish
3. ✅ **GitHub** - O'zgarishlarni saqlash

---

## Yordam va qo'llab-quvvatlash

### Agar muammo yuzaga kelsa:

1. **Xatoni o'qing:** Terminal'dagi xato xabarini diqqat bilan o'qing
2. **Google qiling:** Xato xabarini Google'da qidiring
3. **Dokumentatsiyani o'qing:** Django docs'ni tekshiring
4. **Savol bering:** Stack Overflow yoki Django forumda

### Foydali havolalar:

- Django Sessions: https://docs.djangoproject.com/en/stable/topics/http/sessions/
- Django Models: https://docs.djangoproject.com/en/stable/topics/db/models/
- Django Admin: https://docs.djangoproject.com/en/stable/ref/contrib/admin/

---

Endi yangiliklaringiz qancha mashhurligini bilib olasiz va eng ko'p o'qilgan maqolalarni ajratib ko'rsatishingiz mumkin.

**Keyingi darsda ko'rishlar sonini template'da chiroyli qilib ko'rsatishni o'rganamiz!** 