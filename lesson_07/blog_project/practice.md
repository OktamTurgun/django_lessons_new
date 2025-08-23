# Lesson 07 Practice: Blog Model qismi

Bu amaliyotda siz **Blog ilovasi uchun model yaratish, migratsiya qilish, admin panelga ulash va ORM orqali CRUD amallarini bajarishni** mashq qilasiz. Har bir bosqichda kod va izohlar berilgan.

**Old shartlar**: `blog` nomli app mavjud va `settings.py` ichidagi `INSTALLED_APPS` ga qo‘shilgan bo‘lishi kerak.

---

## 1 Post modelini yaratish

📌 **Vazifa**: `blog/models.py` faylida quyidagi modelni yozing:

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200, help_text="Post sarlavhasi (200 belgigacha)")
    content = models.TextField(help_text="Post matni (HTML/oddiy matn)")
    is_published = models.BooleanField(default=True, help_text="Post saytga ko‘rinadimi?")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Yaratilgan vaqt (auto)")
    updated_at = models.DateTimeField(auto_now=True, help_text="So‘nggi tahrir vaqti (auto)")

    def __str__(self):
        # Admin va konsolda chiroyli ko‘rinishi uchun
        return self.title

    class Meta:
        ordering = ["-created_at"]  # Eng yangi postlar birinchi
        verbose_name = "Post"
        verbose_name_plural = "Postlar"
```

📌 **Nima uchun shunday?**
- `auto_now_add` obyekt yaratilganda sana/vaqtni avtomatik yozadi.
- `auto_now` obyekt saqlanganda (update qilinsa) sanani yangilaydi.
- `ordering` bilan global tartibni belgilab, `Post.objects.all()` doim bir xil tartibda keladi.

---

## 2 Migratsiya yaratish va bazaga qo‘llash

**Buyruqlar**:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Kutilgan natija**: yangi `blog_post` jadvali bazada yaratiladi.

📌 **Eslatma**: Har safar model tuzilmasini o‘zgartirsangiz, `makemigrations → migrate` ketma-ketligini bajaring.

---

## 3 Admin panelga ulash

📌 **Vazifa**: `blog/admin.py` faylida Post modelini ro‘yxatdan o‘tkazing va qulay ro‘yxat ko‘rinishi yarating.

```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "content")
```

**Tekshirish**:
1. `python manage.py createsuperuser` bilan admin yarating (agar hali bo‘lmasa).
2. `runserver` qiling va `http://127.0.0.1:8000/admin/` ga kiring.
3. Post qo‘shib ko‘ring.

---

## 4 Django shell orqali CRUD (yaratish/o‘qish/yangilash/o‘chirish)

**Shell ochish**:

```bash
python manage.py shell
```

**Obyekt yaratish va o‘qish**:

```python
from blog.models import Post

# Yaratish (create)
p1 = Post.objects.create(title="Birinchi post", content="Salom, bu birinchi post!", is_published=True)
p2 = Post.objects.create(title="Ikkinchi post", content="Bu ikkinchi post...", is_published=False)

# O‘qish (read)
all_posts = Post.objects.all()              # hammasi
published = Post.objects.filter(is_published=True)  # faqat ko‘rinadiganlar
latest_five = Post.objects.all()[:5]        # slicing
```

**Qidiruv va filtrlash (field lookups)**:

```python
Post.objects.filter(title__icontains="post")   # sarlavhasida 'post' so‘zi bor
Post.objects.filter(created_at__date__gte="2025-01-01")  # 2025-yildan keyin yaratilganlar
Post.objects.exclude(is_published=True)        # ko‘rinmaydiganlar
```

**Yangilash va saqlash**:

```python
p1.title = "Yangilangan sarlavha"
p1.save()  # bitta obyektni saqlash
```

**O‘chirish**:

```python
p2.delete()    # bitta obyektni o‘chirish
# yoki
Post.objects.filter(is_published=False).delete()  # ko‘p obyektni bir yo‘la o‘chirish (ehtiyot bo‘ling!)
```

**Qo‘shimcha foydali metodlar**:

```python
Post.objects.count()
Post.objects.exists()
Post.objects.values("title", "is_published")          # dictlar
Post.objects.values_list("title", flat=True)[:10]     # faqat sarlavhalar
```

---

## 5 get_absolute_url (ixtiyoriy, lekin tavsiya etiladi)

Keyinchalik detail sahifa yaratishda yordam beradi.

```python
from django.urls import reverse

class Post(models.Model):
    # ... yuqoridagi maydonlar ...
    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])
```

📌 **Eslatma**: `urls.py` da `path("posts/<int:pk>/", views.post_detail, name="post_detail")` bo‘lsa, `obj.get_absolute_url()` to‘g‘ri manzilni chiqaradi.

---

## 6 Qo‘shimcha model: Comment (ForeignKey bilan munosabat)

📌 **Vazifa**: Comment modelini qo‘shing va Post bilan 1-to-ko‘p aloqani o‘rnating.

```python
# blog/models.py

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author}: {self.text[:30]}"
```

**Keyin**:

```bash
python manage.py makemigrations
python manage.py migrate
```

**Admin**:

```python
# blog/admin.py
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")
    search_fields = ("author", "text")
    list_filter = ("created_at",)
```

**Reverse relation (post → comments) bilan ishlash**:

```python
post = Post.objects.first()
post_comments = post.comments.all()  # related_name = "comments" sababli
```

---

## 7 Bonus: slug maydoni (SEO uchun)

📌 **Vazifa (ixtiyoriy)**: Post ga slug qo‘shing va uni sarlavhadan avtomatik hosil qiling.

```python
# models.py
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    content = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
```

📌 **Eslatma**: bir xil sarlavha ko‘p bo‘lsa `unique=True` xatoga olib keladi — real loyihada unikal qilish uchun slugga `-id` yoki random suffix qo‘shish tavsiya etiladi.

---

## 8 Tez-tez uchraydigan xatolar va yechimlar

- **No installed app with label 'blog'** → `settings.py` → `INSTALLED_APPS` ichiga `blog` qo‘shilganini tekshiring.
- **You have unapplied migrations** → `makemigrations` va `migrate` ni bajaring.
- **Admin’da model ko‘rinmayapti** → `admin.py` da ro‘yxatdan o‘tganini va serverni qayta ishga tushirganingizni tekshiring.
- **IntegrityError (unique constraint)** → slug yoki unique maydonlar takrorlanmaganini tekshiring.

---

## Yakuniy tekshiruv ro‘yxati (Checklist)

- [x] Post modeli yaratildi (`title`, `content`, `is_published`, `created_at`, `updated_at`, `__str__`, `Meta.ordering`).
- [x] Migratsiyalar bajarildi (`makemigrations → migrate`).
- [x] Admin panelga Post (va Comment) ulandi.
- [x] Shell orqali create/read/update/delete amallari ishladi.
- [x] (Bonus) `get_absolute_url` va `slug` sinab ko‘rildi.

---

## Best practices

- Har bir model uchun `__str__` yozing — debugging va admin uchun qulay.
- `Meta.ordering` bilan default tartibni belgilang (odatda `-created_at`).
- Katta matnlar uchun `TextField`, qisqa sarlavha uchun `CharField` ishlating.
- Ko‘p o‘qiladigan query’larda indeks (masalan `db_index=True`) qo‘llashni o‘ylang.
- `bulk_delete`/`bulk_update` kabi amallardan oldin backup yoki ehtiyot choralarini ko‘ring.
- `ForeignKey` lar uchun `related_name` yozish keyinchalik kodingizni soddalashtiradi.

---

## Yakuniy challenge

`Post` ga quyidagi maydonni qo‘shing:

```python
views_count = models.PositiveIntegerField(default=0)
```

- Har safar post detail ko‘rilganda `views_count += 1` bo‘lsin (view funksiyada).

- Eng ko‘p ko‘rilgan 5 ta postni ORM orqali oling:

```python
Post.objects.order_by('-views_count')[:5]
```

---

Shu bilan siz **Blog Model qismi bo‘yicha amaliy ko‘nikmalarga ega bo‘lasiz.**
