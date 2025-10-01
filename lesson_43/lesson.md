# Django'da Izoh Qoldirish: Izoh Modeli va Formasini Yaratish (1-qism)

## Kirish

Zamonaviy veb-saytlarning aksariyatida foydalanuvchilar o'z fikr-mulohazalarini bildirish imkoniyatiga ega bo'ladilar. Izohlar (comments) - bu foydalanuvchilar va kontent o'rtasidagi muhim aloqa vositasidir. Bu darsda biz yangiliklar saytimizga izoh qoldirish funksiyasini qo'shamiz.

Izoh tizimini qurish uchun biz uch bosqichdan o'tamiz:
1. **Izoh modelini yaratish** (1-qism - bu dars)
2. **Views qismini yozish** (2-qism)
3. **Template qismini yozish** (3-qism)

Bu darsda biz birinchi bosqichni - izoh modeli va formasini yaratishni o'rganamiz.

---

## Izoh Modeli Haqida

Izoh modeli quyidagi ma'lumotlarni saqlashi kerak:
- Qaysi yangilikga izoh qoldirilgani
- Kimning izoh qoldirishi (foydalanuvchi)
- Izoh matni
- Izoh qoldirilgan vaqt
- Izoh faol/faol emasligini belgilash (moderatsiya uchun)

---

## 1-Bosqich: Izoh Modelini Yaratish

`news` ilovamizning `models.py` fayliga yangi `Comment` modelini qo'shamiz.

### models.py

```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Mavjud News modeli...

class Comment(models.Model):
    """
    Izohlar modeli - foydalanuvchilar yangiliklariga izoh qoldirishlari uchun
    """
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
    body = models.TextField(
        verbose_name='Izoh matni'
    )
    created_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Yaratilgan vaqt'
    )
    active = models.BooleanField(
        default=True,
        verbose_name='Faolmi?'
    )

    class Meta:
        ordering = ['-created_time']
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'

    def __str__(self):
        return f"{self.user.username} - {self.news.title[:30]}"
```

### Model Maydonlarini Tushuntirish

**1. news (ForeignKey)**
```python
news = models.ForeignKey(
    News,
    on_delete=models.CASCADE,
    related_name='comments',
    verbose_name='Yangilik'
)
```
- **ForeignKey** - Bu izoh qaysi yangilikga tegishli ekanligini ko'rsatadi
- **on_delete=models.CASCADE** - Agar yangilik o'chirilsa, unga tegishli barcha izohlar ham o'chiriladi
- **related_name='comments'** - Bu juda muhim! News modelidan izohlarni olish uchun ishlatamiz: `news.comments.all()`

**2. user (ForeignKey)**
```python
user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name='Foydalanuvchi'
)
```
- Izoh qoldirgan foydalanuvchini belgilaydi
- Agar foydalanuvchi o'chirilsa, uning barcha izohlar ham o'chiriladi

**3. body (TextField)**
```python
body = models.TextField(
    verbose_name='Izoh matni'
)
```
- Izohning asosiy matni
- TextField - uzun matnlar uchun ishlatiladi

**4. created_time (DateTimeField)**
```python
created_time = models.DateTimeField(
    auto_now_add=True,
    verbose_name='Yaratilgan vaqt'
)
```
- **auto_now_add=True** - Izoh birinchi marta yaratilganda avtomatik vaqt qo'shiladi
- Foydalanuvchiga "3 soat oldin", "2 kun oldin" kabi ko'rsatish uchun ishlatiladi

**5. active (BooleanField)**
```python
active = models.BooleanField(
    default=True,
    verbose_name='Faolmi?'
)
```
- Izohni moderatsiya qilish uchun
- Admin izohni yashirishi mumkin (active=False qilish orqali)

### Meta Class Tushuntirish

```python
class Meta:
    ordering = ['-created_time']
    verbose_name = 'Izoh'
    verbose_name_plural = 'Izohlar'
```

- **ordering = ['-created_time']** - Izohlar eng yangisilari birinchi bo'lib chiqadi
- **verbose_name** - Admin panelda yagonalik shakli
- **verbose_name_plural** - Admin panelda ko'plik shakli

---

## 2-Bosqich: Migratsiya Qilish

Model yaratganimizdan keyin uni ma'lumotlar bazasiga qo'shishimiz kerak.

### Terminal

```bash
python manage.py makemigrations
```

Natija:
```
Migrations for 'news':
  news/migrations/0003_comment.py
    - Create model Comment
```

Keyin migratsiyani amalga oshiramiz:

```bash
python manage.py migrate
```

Natija:
```
Running migrations:
  Applying news.0003_comment... OK
```

---

## 3-Bosqich: Admin Panelda Izohlarni Ko'rsatish

Izohlarni admin panelda boshqarish uchun `admin.py` faylini yangilaymiz.

### admin.py

```python
from django.contrib import admin
from .models import News, Category, Comment

# Mavjud admin classlari...

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user__username', 'body']
    actions = ['activate_comments', 'deactivate_comments']

    def activate_comments(self, request, queryset):
        """Tanlangan izohlarni faollashtirish"""
        queryset.update(active=True)
        self.message_user(request, 'Tanlangan izohlar faollashtirildi.')
    activate_comments.short_description = 'Tanlangan izohlarni faollashtirish'

    def deactivate_comments(self, request, queryset):
        """Tanlangan izohlarni faolsizlantirish"""
        queryset.update(active=False)
        self.message_user(request, 'Tanlangan izohlar faolsizlantirildi.')
    deactivate_comments.short_description = 'Tanlangan izohlarni faolsizlantirish'
```

### Admin Class Tushuntirish

**list_display**
```python
list_display = ['user', 'news', 'created_time', 'active']
```
- Admin panelda jadvalda ko'rsatiladigan ustunlar
- Foydalanuvchi, yangilik, vaqt va holat ko'rinadi

**list_filter**
```python
list_filter = ['active', 'created_time']
```
- O'ng tomonda filtrlash panelini qo'shadi
- Faol/faol emas va sana bo'yicha filtrlash mumkin

**search_fields**
```python
search_fields = ['user__username', 'body']
```
- Qidiruv maydonini qo'shadi
- **user__username** - ForeignKey orqali bog'langan maydon
- **body** - Izoh matni ichidan qidirish

**Custom Actions (Maxsus Harakatlar)**
```python
def activate_comments(self, request, queryset):
    queryset.update(active=True)
    self.message_user(request, 'Tanlangan izohlar faollashtirildi.')
```
- Admin bir nechta izohni birdan faol/faolsiz qilishi mumkin
- `queryset.update()` - tanlangan barcha izohlarni yangilaydi
- `self.message_user()` - foydalanuvchiga xabar ko'rsatadi

---

## 4-Bosqich: Izoh Formasini Yaratish

Foydalanuvchilar izoh qoldirishi uchun forma kerak. `news` ilovasida yangi `forms.py` fayl yaratamiz.

### news/forms.py (yangi fayl)

```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    """
    Izoh qoldirish formasi
    """
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

### Forma Tushuntirish

**ModelForm**
```python
class CommentForm(forms.ModelForm):
```
- **ModelForm** - Model asosida forma yaratadi
- Avtomatik validatsiya qo'shadi
- Modelga ma'lumotlarni saqlashni osonlashtiradi

**Meta Class**
```python
class Meta:
    model = Comment
    fields = ['body']
```
- **model = Comment** - Qaysi model uchun forma ekanligini ko'rsatadi
- **fields = ['body']** - Faqat izoh matni maydonini ko'rsatamiz
- `user` va `news` maydonlarini kodda avtomatik to'ldiramiz

**Widgets (Vizual Ko'rinish)**
```python
widgets = {
    'body': forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Izohingizni yozing...',
        'rows': 4
    })
}
```
- **forms.Textarea** - Ko'p qatorli matn maydoni
- **attrs** - HTML atributlarini qo'shish
- **class** - Bootstrap uchun CSS class
- **placeholder** - Foydalanuvchiga maslahat matni
- **rows** - Maydon balandligi (qatorlar soni)

**Labels (Yorliqlar)**
```python
labels = {
    'body': 'Sizning izohingiz'
}
```
- Maydon nomini o'zbek tilida ko'rsatadi

---

## 5-Bosqich: Test Ma'lumotlar Qo'shish

Admin panelga kirib, bir nechta test izohlar qo'shib ko'ramiz.

### Admin panelda test

1. Serverni ishga tushiring:
```bash
python manage.py runserver
```

2. Brauzerda `http://127.0.0.1:8000/admin/` ga o'ting

3. **Comments** bo'limiga o'ting va **Add comment** tugmasini bosing

4. Test izoh qo'shing:
   - **News:** Biron yangilikni tanlang
   - **User:** O'zingizni tanlang
   - **Body:** "Bu juda qiziq yangilik! Davomini kutamiz."
   - **Active:** belgilangan holda qoldiring

5. **Save** tugmasini bosing

6. Yana 2-3 ta test izoh qo'shing, turli yangiliklariga

---

## Izohlar Bilan Ishlashning Amaliy Misoli

Keling, Django shell orqali izohlar bilan qanday ishlashni ko'rib chiqamiz.

### Terminal (Django Shell)

```bash
python manage.py shell
```

### 1. Barcha izohlarni olish

```python
from news.models import Comment

# Barcha izohlar
comments = Comment.objects.all()
print(comments)

# Faol izohlar
active_comments = Comment.objects.filter(active=True)
print(f"Faol izohlar soni: {active_comments.count()}")
```

### 2. Bitta yangilikka tegishli izohlarni olish

```python
from news.models import News

# Birinchi yangilikni olamiz
news = News.objects.first()

# Unga tegishli barcha izohlar (related_name='comments' ishlatamiz)
news_comments = news.comments.all()
print(f"{news.title} yangiligiga {news_comments.count()} ta izoh")

# Faqat faol izohlar
active_news_comments = news.comments.filter(active=True)
for comment in active_news_comments:
    print(f"{comment.user.username}: {comment.body[:50]}")
```

### 3. Foydalanuvchi izohlarini olish

```python
from django.contrib.auth.models import User

# Birinchi foydalanuvchini olamiz
user = User.objects.first()

# Foydalanuvchi qoldirgan barcha izohlar
user_comments = Comment.objects.filter(user=user)
print(f"{user.username} {user_comments.count()} ta izoh qoldirgan")
```

### 4. Yangi izoh qo'shish

```python
from news.models import News, Comment
from django.contrib.auth.models import User

# Kerakli ma'lumotlarni olamiz
news = News.objects.first()
user = User.objects.first()

# Yangi izoh yaratamiz
new_comment = Comment.objects.create(
    news=news,
    user=user,
    body="Bu Django shell orqali qo'shilgan izoh!",
    active=True
)

print(f"Izoh yaratildi: {new_comment}")
```

---

## Model Metodlarini Qo'shish (Qo'shimcha)

Izoh modeliga foydali metodlar qo'shishimiz mumkin.

### models.py (Comment modeliga qo'shamiz)

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
        """
        Qisqartirilgan izoh matni (admin panel uchun)
        """
        if len(self.body) > 50:
            return f"{self.body[:50]}..."
        return self.body
    
    def get_user_full_name(self):
        """
        Foydalanuvchining to'liq ismi
        """
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
```

### Metodlarni Tushuntirish

**get_short_body()**
```python
def get_short_body(self):
    if len(self.body) > 50:
        return f"{self.body[:50]}..."
    return self.body
```
- Uzun izohlarni qisqartiradi
- Template'da yoki admin panelda ishlatish uchun qulay

**get_user_full_name()**
```python
def get_user_full_name(self):
    if self.user.first_name and self.user.last_name:
        return f"{self.user.first_name} {self.user.last_name}"
    return self.user.username
```
- Agar foydalanuvchi ism-familiyasini kiritgan bo'lsa, uni ko'rsatadi
- Aks holda username'ni qaytaradi

---

## Admin Panelni Yanada Yaxshilash

Admin panelda yangi metodlarni ishlatamiz.

### admin.py (yangilangan)

```python
from django.contrib import admin
from .models import News, Category, Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_user_name', 'get_news_title', 'get_short_comment', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user__username', 'body', 'news__title']
    actions = ['activate_comments', 'deactivate_comments']
    readonly_fields = ['created_time']

    def get_user_name(self, obj):
        """Foydalanuvchi ismi"""
        return obj.get_user_full_name()
    get_user_name.short_description = 'Foydalanuvchi'

    def get_news_title(self, obj):
        """Yangilik sarlavhasi (qisqartirilgan)"""
        if len(obj.news.title) > 40:
            return f"{obj.news.title[:40]}..."
        return obj.news.title
    get_news_title.short_description = 'Yangilik'

    def get_short_comment(self, obj):
        """Qisqartirilgan izoh"""
        return obj.get_short_body()
    get_short_comment.short_description = 'Izoh'

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

### Yangi Admin Metodlar Tushuntirish

**get_user_name()**
```python
def get_user_name(self, obj):
    return obj.get_user_full_name()
get_user_name.short_description = 'Foydalanuvchi'
```
- `obj` - Comment obyekti
- Model metodini chaqiradi
- `short_description` - ustun nomini belgilaydi

**readonly_fields**
```python
readonly_fields = ['created_time']
```
- Admin formada faqat o'qish uchun maydonlar
- Vaqtni o'zgartirish mumkin emas

---

## Formani Turli Xil Variantlarda Yaratish

### 1. Oddiy Variant (minimal)

```python
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
```

### 2. Batafsil Variant (CSS klasslar bilan)

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
                'placeholder': 'Izohingizni yozing...',
                'rows': 4,
                'style': 'resize: none;'  # O'lchamini o'zgartirish imkonini o'chirish
            })
        }
        
        labels = {
            'body': 'Sizning izohingiz'
        }
        
        help_texts = {
            'body': 'Iltimos, odobli tilda yozing.'
        }
```

### 3. Validatsiya bilan Variant

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
                'placeholder': 'Izohingizni yozing...',
                'rows': 4
            })
        }
        
        labels = {
            'body': 'Sizning izohingiz'
        }
    
    def clean_body(self):
        """
        Izoh matnini tekshirish
        """
        body = self.cleaned_data.get('body')
        
        # Minimal uzunlik tekshiruvi
        if len(body) < 10:
            raise forms.ValidationError(
                'Izoh kamida 10 ta belgidan iborat bo\'lishi kerak.'
            )
        
        # Maksimal uzunlik tekshiruvi
        if len(body) > 500:
            raise forms.ValidationError(
                'Izoh 500 ta belgidan oshmasligi kerak.'
            )
        
        # Taqiqlangan so'zlarni tekshirish (misol)
        forbidden_words = ['spam', 'reklama']
        for word in forbidden_words:
            if word.lower() in body.lower():
                raise forms.ValidationError(
                    f'Izohda taqiqlangan so\'z ishlatilgan: "{word}"'
                )
        
        return body
```

### Validatsiya Metodini Tushuntirish

**clean_body()**
```python
def clean_body(self):
    body = self.cleaned_data.get('body')
```
- Django avtomatik chaqiradi
- Maydon nomidan keyin `clean_` prefiksini qo'shish kerak

**ValidationError**
```python
raise forms.ValidationError('Xato xabari')
```
- Validatsiya muvaffaqiyatsiz bo'lsa, xato ko'rsatadi
- Forma saqlanmaydi

---

## Xulosa

Bu darsda biz quyidagilarni o'rgandik:

### ✅ Bajardik:
1. **Comment modelini yaratdik** - izohlar uchun ma'lumotlar bazasi strukturasi
2. **Migratsiya qildik** - modelni ma'lumotlar bazasiga qo'shdik
3. **Admin panelni sozladik** - izohlarni boshqarish uchun
4. **CommentForm yaratdik** - foydalanuvchilar izoh qoldirishi uchun
5. **Model metodlarini qo'shdik** - qulaylik uchun
6. **Validatsiya qo'shdik** - izohlarni tekshirish uchun

### 📌 Muhim Tushunchalar:

**ForeignKey maydonlar:**
```python
news = models.ForeignKey(News, related_name='comments', ...)
```
- `related_name` - teskari aloqa uchun
- Bir yangilikda ko'p izohlar bo'lishi mumkin

**ModelForm:**
```python
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
```
- Model asosida forma yaratadi
- Avtomatik validatsiya qo'shadi

**Admin Custom Actions:**
```python
def activate_comments(self, request, queryset):
    queryset.update(active=True)
```
- Bir nechta obyektni birdan o'zgartirish

### 🎯 Keyingi Qadamlar:

Keyingi darsda biz:
- Views qismini yozamiz
- Izoh qoldirish funksiyasini ishga tushiramiz
- AJAX orqali yangilash qo'shamiz (ixtiyoriy)

---

## Maslahatlar va Best Practice

### 1. Model Dizayni
```python
# ✅ Yaxshi
class Comment(models.Model):
    news = models.ForeignKey(News, related_name='comments', ...)
    # related_name orqali news.comments.all() ishlatish oson

# ❌ Yomon
class Comment(models.Model):
    news = models.ForeignKey(News, ...)
    # related_name yo'q, news.comment_set.all() ishlatish kerak
```

### 2. Validatsiya
```python
# ✅ Yaxshi - Model va Formada validatsiya
class Comment(models.Model):
    body = models.TextField(max_length=500)

class CommentForm(forms.ModelForm):
    def clean_body(self):
        # Qo'shimcha tekshiruv
        pass

# ❌ Yomon - Validatsiya yo'q
class Comment(models.Model):
    body = models.TextField()  # Cheksiz uzunlik
```

### 3. Admin Panel
```python
# ✅ Yaxshi - To'liq sozlangan
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'created_time', 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user__username', 'body']

# ❌ Yomon - Oddiy ro'yxatdan o'tkazish
admin.site.register(Comment)
```

### 4. Forma Widgetlari
```python
# ✅ Yaxshi - User-friendly
widgets = {
    'body': forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Izohingizni yozing...',
        'rows': 4
    })
}

# ❌ Yomon - Oddiy HTML input
widgets = {
    'body': forms.Textarea()
}
```

### 5. Xavfsizlik
```python
# ✅ Yaxshi - Moderatsiya imkoniyati
class Comment(models.Model):
    active = models.BooleanField(default=True)

# Template'da:
comments = news.comments.filter(active=True)

# ❌ Yomon - Barcha izohlarni ko'rsatish
comments = news.comments.all()  # Spam ham ko'rinadi
```

### 6. Performance (Tezlik)
```python
# ✅ Yaxshi - select_related ishlatish
comments = Comment.objects.select_related('user', 'news').all()

# ❌ Yomon - Har bir izoh uchun alohida so'rov
comments = Comment.objects.all()
for comment in comments:
    print(comment.user.username)  # Har safar yangi so'rov!
```

---

## Qo'shimcha Ma'lumotlar

### Izohlar Sonini Olish

```python
# News modeliga qo'shish mumkin
class News(models.Model):
    # ... mavjud maydonlar ...
    
    def get_comments_count(self):
        """Faol izohlar soni"""
        return self.comments.filter(active=True).count()
    
    def get_all_comments_count(self):
        """Barcha izohlar soni"""
        return self.comments.count()
```

### Izohlarni Vaqt Bo'yicha Guruhlash

```python
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

# Oxirgi 7 kundagi izohlar
week_ago = timezone.now() - timedelta(days=7)
recent_comments = Comment.objects.filter(
    created_time__gte=week_ago,
    active=True
)

# Eng ko'p izohli yangiliklar
popular_news = News.objects.annotate(
    comment_count=Count('comments')
).order_by('-comment_count')[:5]
```

### Foydalanuvchi Faolligi

```python
# Eng faol foydalanuvchilar (ko'p izoh qoldirgan)
from django.db.models import Count

active_users = User.objects.annotate(
    comment_count=Count('comment')
).order_by('-comment_count')[:10]

for user in active_users:
    print(f"{user.username}: {user.comment_count} ta izoh")
```

---

Bu darsda biz izoh tizimining asosini yaratdik. Keyingi darsda biz views va template qismlarini yozib, to'liq ishlaydigan izoh tizimini yaratamiz!

**Davomi:** lesson_44 - Views qismini yozish (2-qism)