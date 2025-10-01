# Django Izoh Tizimi - Amaliyot Mashqlari

Bu amaliyot mashqlarida siz darsda o'rgangan barcha narsalarni qo'llab ishlab chiqasiz va qo'shimcha funksiyalar qo'shasiz.

---

## Mashq 1: Comment Modelini Yaratish

### Vazifa
Yangiliklar saytingizga izoh (Comment) modelini qo'shing va uni to'liq sozlang.

### Bosqichma-bosqich yo'riqnoma:

#### 1-Qadam: models.py faylini ochish
`news/models.py` faylini oching va Comment modelini qo'shing.

#### 2-Qadam: Comment modelini yozish
```python
from django.db import models
from django.contrib.auth.models import User

class Comment(models.Model):
    """Izohlar modeli"""
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Yangilik'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Foydalanuvchi'
    )
    body = models.TextField(verbose_name='Izoh matni')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    active = models.BooleanField(default=True, verbose_name='Faolmi?')

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'

    def __str__(self):
        return f"{self.user.username} - {self.news.title[:30]}"
```

#### 3-Qadam: Migratsiya qilish
Terminal'da quyidagi buyruqlarni bajaring:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 4-Qadam: Tekshirish
```bash
python manage.py shell
```

Shell'da:
```python
from news.models import Comment
print(Comment.objects.all())
```

### ✅ Natija
Agar xato chiqmasa - to'g'ri bajarilgan!

---

## Mashq 2: Admin Panelni Sozlash

### Vazifa
Admin panelda izohlarni boshqarish uchun to'liq interfeys yarating.

### Bosqichma-bosqich yo'riqnoma:

#### 1-Qadam: admin.py faylini yangilash
```python
from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'news', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user__username', 'body', 'news__title']
    list_per_page = 20
```

#### 2-Qadam: Serverni ishga tushirish
```bash
python manage.py runserver
```

#### 3-Qadam: Admin panelga kirish
Brauzerda: `http://127.0.0.1:8000/admin/`

#### 4-Qadam: Test izoh qo'shish
- Comments bo'limiga o'ting
- "Add comment" tugmasini bosing
- Barcha maydonlarni to'ldiring
- Save tugmasini bosing

### ✅ Tekshirish
- Admin panelda Comments bo'limi ko'rinishi kerak
- Izohlarni qo'shish, o'zgartirish, o'chirish ishlashi kerak
- Qidiruv va filtrlash ishlashi kerak

---

## Mashq 3: Custom Admin Actions Qo'shish

### Vazifa
Admin panelda bir nechta izohni birdan faollashtirish/faolsizlantirish funksiyasini qo'shing.

### Bosqichma-bosqich yo'riqnoma:

#### Kod:
```python
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'news', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user__username', 'body', 'news__title']
    actions = ['activate_comments', 'deactivate_comments']

    def activate_comments(self, request, queryset):
        """Tanlangan izohlarni faollashtirish"""
        count = queryset.update(active=True)
        self.message_user(request, f'{count} ta izoh faollashtirildi.')
    activate_comments.short_description = 'Tanlangan izohlarni faollashtirish'

    def deactivate_comments(self, request, queryset):
        """Tanlangan izohlarni faolsizlantirish"""
        count = queryset.update(active=False)
        self.message_user(request, f'{count} ta izoh faolsizlantirildi.')
    deactivate_comments.short_description = 'Tanlangan izohlarni faolsizlantirish'
```

#### Tekshirish:
1. Admin panelda bir nechta izoh qo'shing
2. Checkboxlar orqali bir nechta izohni tanlang
3. "Action" dropdown dan "Tanlangan izohlarni faolsizlantirish" tanlang
4. "Go" tugmasini bosing
5. Izohlar faolsizlanishi kerak (active=False)

### ✅ Natija
Bir bosishda ko'p izohlarni boshqarish imkoniyati paydo bo'ladi.

---

## Mashq 4: CommentForm Yaratish

### Vazifa
Foydalanuvchilar izoh qoldirishi uchun forma yarating.

### Bosqichma-bosqich yo'riqnoma:

#### 1-Qadam: forms.py fayl yaratish
`news/forms.py` faylini yarating (agar yo'q bo'lsa).

#### 2-Qadam: Formani yozish
```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """Izoh qoldirish formasi"""
    
    class Meta:
        model = Comment
        fields = ['body']
        
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Izohingizni yozing...',
                'rows': 4
            })
        }
        
        labels = {
            'body': 'Sizning izohingiz'
        }
```

#### 3-Qadam: Django shell'da tekshirish
```bash
python manage.py shell
```

```python
from news.forms import CommentForm

# Bo'sh forma
form = CommentForm()
print(form.as_p())

# Ma'lumot bilan forma
form = CommentForm(data={'body': 'Test izoh'})
print(form.is_valid())  # True bo'lishi kerak
```

### ✅ Natija
Forma yaratilgan va ishlayotgan bo'lishi kerak.

---

## Mashq 5: Validatsiya Qo'shish

### Vazifa
Formaga maxsus validatsiya qoidalarini qo'shing.

### Bosqichma-bosqich yo'riqnoma:

#### Kod:
```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """Validatsiya bilan izoh formasi"""
    
    class Meta:
        model = Comment
        fields = ['body']
        
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Izohingizni yozing...',
                'rows': 4
            })
        }
        
        labels = {
            'body': 'Sizning izohingiz'
        }
    
    def clean_body(self):
        """Izoh matnini tekshirish"""
        body = self.cleaned_data.get('body')
        
        # Minimal uzunlik
        if len(body) < 10:
            raise forms.ValidationError(
                'Izoh kamida 10 ta belgidan iborat bo\'lishi kerak.'
            )
        
        # Maksimal uzunlik
        if len(body) > 500:
            raise forms.ValidationError(
                'Izoh 500 ta belgidan oshmasligi kerak.'
            )
        
        # Bo'sh joy tekshiruvi
        if body.strip() == '':
            raise forms.ValidationError(
                'Izoh bo\'sh bo\'lishi mumkin emas.'
            )
        
        return body
```

#### Tekshirish:
```python
from news.forms import CommentForm

# Juda qisqa izoh (xato bo'lishi kerak)
form1 = CommentForm(data={'body': 'Test'})
print(form1.is_valid())  # False
print(form1.errors)

# To'g'ri izoh
form2 = CommentForm(data={'body': 'Bu juda yaxshi yangilik. Rahmat!'})
print(form2.is_valid())  # True

# Juda uzun izoh (xato bo'lishi kerak)
long_text = 'a' * 501
form3 = CommentForm(data={'body': long_text})
print(form3.is_valid())  # False
print(form3.errors)
```

### ✅ Natija
Validatsiya ishlayotgan bo'lishi va xatolarni to'g'ri ko'rsatishi kerak.

---

## Mashq 6: Model Metodlarini Qo'shish

### Vazifa
Comment modeliga foydali metodlar qo'shing.

### Bosqichma-bosqich yo'riqnoma:

#### Kod:
```python
class Comment(models.Model):
    # ... mavjud maydonlar ...

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'

    def __str__(self):
        return f"{self.user.username} - {self.news.title[:30]}"
    
    def get_short_body(self):
        """Qisqartirilgan izoh matni"""
        if len(self.body) > 50:
            return f"{self.body[:50]}..."
        return self.body
    
    def get_user_full_name(self):
        """Foydalanuvchining to'liq ismi"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    
    def get_created_time_formatted(self):
        """Formatlangan vaqt"""
        return self.created_time.strftime('%d.%m.%Y %H:%M')
```

#### Tekshirish:
```bash
python manage.py shell
```

```python
from news.models import Comment

comment = Comment.objects.first()

# Metodlarni sinash
print(comment.get_short_body())
print(comment.get_user_full_name())
print(comment.get_created_time_formatted())
```

### ✅ Natija
Barcha metodlar ishlashi kerak.

---

## Mashq 7: Admin Panelda Custom Metodlarni Ko'rsatish

### Vazifa
Admin panelda model metodlarini ustunlar sifatida ko'rsating.

### Bosqichma-bosqich yo'riqnoma:

#### Kod:
```python
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'get_user_display', 
        'get_news_display', 
        'get_short_comment', 
        'created_time', 
        'active'
    ]
    list_filter = ['active', 'created_time']
    search_fields = ['user__username', 'body', 'news__title']
    actions = ['activate_comments', 'deactivate_comments']
    readonly_fields = ['created_time']

    def get_user_display(self, obj):
        """Foydalanuvchi nomi"""
        return obj.get_user_full_name()
    get_user_display.short_description = 'Foydalanuvchi'

    def get_news_display(self, obj):
        """Yangilik sarlavhasi"""
        if len(obj.news.title) > 40:
            return f"{obj.news.title[:40]}..."
        return obj.news.title
    get_news_display.short_description = 'Yangilik'

    def get_short_comment(self, obj):
        """Qisqartirilgan izoh"""
        return obj.get_short_body()
    get_short_comment.short_description = 'Izoh'

    # ... activate va deactivate metodlari ...
```

#### Tekshirish:
Admin panelda Comments bo'limini oching va yangi ustunlarni ko'ring.

### ✅ Natija
Admin jadvalida to'liq va qisqartirilgan ma'lumotlar ko'rinadi.

---

## Mashq 8: Django Shell bilan Ishlash

### Vazifa
Django shell orqali izohlar bilan turli amallarni bajaring.

### Bosqichma-bosqich yo'riqnoma:

```bash
python manage.py shell
```

#### 1. Barcha izohlarni olish
```python
from news.models import Comment

comments = Comment.objects.all()
print(f"Jami izohlar: {comments.count()}")
```

#### 2. Faol izohlarni olish
```python
active_comments = Comment.objects.filter(active=True)
print(f"Faol izohlar: {active_comments.count()}")
```

#### 3. Bitta yangilikka tegishli izohlar
```python
from news.models import News

news = News.objects.first()
news_comments = news.comments.all()
print(f"{news.title} - {news_comments.count()} ta izoh")

# Har bir izohni ko'rsatish
for comment in news_comments:
    print(f"  {comment.user.username}: {comment.get_short_body()}")
```

#### 4. Foydalanuvchi izohlari
```python
from django.contrib.auth.models import User

user = User.objects.first()
user_comments = Comment.objects.filter(user=user)
print(f"{user.username} - {user_comments.count()} ta izoh")
```

#### 5. Yangi izoh yaratish
```python
new_comment = Comment.objects.create(
    news=News.objects.first(),
    user=User.objects.first(),
    body="Django shell orqali qo'shilgan izoh!",
    active=True
)
print(f"Yangi izoh yaratildi: {new_comment}")
```

#### 6. Izohni yangilash
```python
comment = Comment.objects.first()
comment.body = "Yangilangan izoh matni"
comment.save()
print("Izoh yangilandi!")
```

#### 7. Izohni o'chirish
```python
comment = Comment.objects.last()
comment.delete()
print("Izoh o'chirildi!")
```

### ✅ Natija
Barcha buyruqlar ishlashi va tegishli natijalarni qaytarishi kerak.

---

## Mashq 9: Advanced Queries (Murakkab So'rovlar)

### Vazifa
Ma'lumotlar bazasidan murakkab so'rovlar yordamida ma'lumot oling.

### Bosqichma-bosqich yo'riqnoma:

```bash
python manage.py shell
```

#### 1. Eng ko'p izohli yangiliklar
```python
from django.db.models import Count
from news.models import News

popular_news = News.objects.annotate(
    comment_count=Count('comments')
).order_by('-comment_count')[:5]

for news in popular_news:
    print(f"{news.title}: {news.comment_count} ta izoh")
```

#### 2. Oxirgi 7 kundagi izohlar
```python
from django.utils import timezone
from datetime import timedelta
from news.models import Comment

week_ago = timezone.now() - timedelta(days=7)
recent_comments = Comment.objects.filter(
    created_time__gte=week_ago,
    active=True
)

print(f"Oxirgi 7 kunda: {recent_comments.count()} ta izoh")
```

#### 3. Eng faol foydalanuvchilar
```python
from django.contrib.auth.models import User
from django.db.models import Count

active_users = User.objects.annotate(
    comment_count=Count('comment')
).filter(comment_count__gt=0).order_by('-comment_count')[:10]

for user in active_users:
    print(f"{user.username}: {user.comment_count} ta izoh")
```

#### 4. Bugungi izohlar
```python
from django.utils import timezone

today = timezone.now().date()
today_comments = Comment.objects.filter(
    created_time__date=today,
    active=True
)

print(f"Bugun: {today_comments.count()} ta izoh")
```

#### 5. Izohsiz yangiliklar
```python
news_without_comments = News.objects.annotate(
    comment_count=Count('comments')
).filter(comment_count=0)

print(f"Izohsiz yangiliklar: {news_without_comments.count()} ta")
```

### ✅ Natija
Barcha murakkab so'rovlar to'g'ri natija qaytarishi kerak.

---

## Mashq 10: Test Ma'lumotlar Yaratish

### Vazifa
Bir nechta test izohlar yarating va ularni tekshiring.

### Bosqichma-bosqich yo'riqnoma:

```bash
python manage.py shell
```

```python
from news.models import News, Comment
from django.contrib.auth.models import User

# Foydalanuvchi va yangilik
user = User.objects.first()
news = News.objects.first()

# 10 ta test izoh
test_comments = [
    "Bu juda qiziq yangilik!",
    "Davomini kutamiz.",
    "Juda foydali ma'lumot, rahmat!",
    "Interesting article, thank you!",
    "Bunday yangiliklarni ko'proq joylashtiring.",
    "Men bu haqda bilmaganman, rahmat!",
    "Qiziq, lekin qo'shimcha tushuntirish kerak.",
    "Ajoyib yozilgan!",
    "Bu mavzuda ko'proq yozing iltimos.",
    "Foydali bo'ldi, saqlab qo'yaman."
]

# Izohlarni yaratish
for i, body in enumerate(test_comments, 1):
    Comment.objects.create(
        news=news,
        user=user,
        body=body,
        active=True
    )
    print(f"{i}. Izoh yaratildi")

print(f"\nJami: {Comment.objects.count()} ta izoh")
```

### ✅ Natija
10 ta test izoh yaratilgan bo'lishi kerak.

---

## Qo'shimcha Vazifalar (Mustaqil Ishlash Uchun)

### Vazifa 11: Like/Dislike Funksiyasi
Comment modeliga `likes` va `dislikes` maydonlarini qo'shing.

**Maslahat:**
```python
class Comment(models.Model):
    # ... mavjud maydonlar ...
    likes = models.PositiveIntegerField(default=0, verbose_name='Yoqdi')
    dislikes = models.PositiveIntegerField(default=0, verbose_name='Yoqmadi')
```

### Vazifa 12: Parent-Child Comment (Javob berish)
Izohga javob berish imkoniyatini qo'shing.

**Maslahat:**
```python
class Comment(models.Model):
    # ... mavjud maydonlar ...
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Asosiy izoh'
    )
```

### Vazifa 13: Email Bildirishnoma
Yangi izoh qoldirilganda yangilik muallifiga email yuborish.

**Maslahat:**
```python
from django.core.mail import send_mail

def send_comment_notification(comment):
    send_mail(
        subject='Yangilikingizga izoh qoldirildi',
        message=f'{comment.user.username} sizning yangilikingizga izoh qoldirdi.',
        from_email='noreply@yoursite.com',
        recipient_list=[comment.news.author.email],
    )
```

### Vazifa 14: Izoh Statistikasi
Har bir foydalanuvchi uchun izoh statistikasini yarating.

**Maslahat:**
```python
def get_user_comment_stats(user):
    total_comments = Comment.objects.filter(user=user).count()
    active_comments = Comment.objects.filter(user=user, active=True).count()
    
    return {
        'total': total_comments,
        'active': active_comments,
        'inactive': total_comments - active_comments
    }
```

### Vazifa 15: Spam Filtri
Taqiqlangan so'zlarni tekshiruvchi funksiya yarating.

**Maslahat:**
```python
FORBIDDEN_WORDS = ['spam', 'reklama', 'click here']

def clean_body(self):
    body = self.cleaned_data.get('body')
    
    for word in FORBIDDEN_WORDS:
        if word.lower() in body.lower():
            raise forms.ValidationError(
                f'Taqiqlangan so\'z: "{word}"'
            )
    
    return body
```

---

## Umumiy Xatolar va Ularning Yechimlari

### Xato 1: "Comment object has no attribute 'comments'"
**Sabab:** related_name noto'g'ri ishlatilgan.

**Yechim:**
```python
# models.py da
news = models.ForeignKey(News, related_name='comments', ...)

# Keyin ishlatish:
news.comments.all()  # To'g'ri
news.comment_set.all()  # Xato
```

### Xato 2: "Cannot resolve keyword 'user__username'"
**Sabab:** Search field noto'g'ri yozilgan.

**Yechim:**
```python
# admin.py da
search_fields = ['user__username', 'body']  # To'g'ri
search_fields = ['user.username', 'body']   # Xato (nuqta emas, ikki underscore)
```

### Xato 3: "ValidationError not raised"
**Sabab:** clean_ metodida return qilmagan.

**Yechim:**
```python
def clean_body(self):
    body = self.cleaned_data.get('body')
    
    if len(body) < 10:
        raise forms.ValidationError('Juda qisqa')
    
    return body  # Bu juda muhim!
```

### Xato 4: "Related objects not saved"
**Sabab:** CASCADE to'g'ri sozlanmagan.

**Yechim:**
```python
# models.py da
news = models.ForeignKey(News, on_delete=models.CASCADE, ...)  # To'g'ri
news = models.ForeignKey(News, ...)  # Xato (on_delete majburiy)
```

---

## Tekshirish Ro'yxati

Barcha mashqlarni bajarib bo'lgandan keyin tekshiring:

- [ ] Comment modeli yaratilgan va migratsiya qilingan
- [ ] Admin panelda izohlarni ko'rish va boshqarish ishlaydi
- [ ] Custom actions (activate/deactivate) ishlaydi
- [ ] CommentForm yaratilgan va validatsiya ishlaydi
- [ ] Model metodlari qo'shilgan va ishlaydi
- [ ] Admin panelda custom metodlar ko'rinadi
- [ ] Django shell orqali barcha amallar bajariladi
- [ ] Murakkab so'rovlar (annotate, filter) ishlaydi
- [ ] Test ma'lumotlar yaratilgan
- [ ] Barcha xatolar to'g'rilangan

---

## Keyingi Qadamlar

Agar barcha mashqlarni muvaffaqiyatli bajardingiz:

1. **lesson_44** - Views qismini yozish
2. **lesson_45** - Template qismini yozish
3. **lesson_46** - AJAX bilan izoh qo'shish

---

## Foydali Maslahatlar

### 1. Ma'lumotlar Bazasini Tozalash
Agar test ma'lumotlarni o'chirmoqchi bo'lsangiz:

```python
# Shell'da
Comment.objects.all().delete()
```

### 2. Backup Olish
Muhim ma'lumotlar oldidan backup oling:

```bash
python manage.py dumpdata news.Comment > comments_backup.json
```

### 3. Backup'dan Qayta Yuklash
```bash
python manage.py loaddata comments_backup.json
```

### 4. Performanceni Tekshirish
```python
from django.db import connection

# So'rovlar sonini ko'rish
print(len(connection.queries))
```

### 5. Debug Rejimi
development'da debugging uchun:

```python
# settings.py
DEBUG = True
```

---

**Eslatma:** Bu amaliyot mashqlari darsda o'rgangan nazariy bilimlarni mustahkamlash uchun mo'ljallangan. Har bir mashqni o'zingiz bajaring va natijalarni tekshiring.

**Omad tilaymiz!** 🚀