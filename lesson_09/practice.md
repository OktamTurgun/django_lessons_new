# Practice 09: Blog loyihasi. BlogDetail - Amaliy mashqlar

## Mashq maqsadi
Ushbu amaliy mashqlarda siz Django blog loyihasida BlogDetail view bilan ishlash ko'nikmalarini mustahkamlaysiz.

## Vazifa ro'yxati

### Asosiy vazifalar

#### 1. Vazifa: BlogDetail view yaratish
**Maqsad:** Post detail sahifasini yaratish

**Bajarilishi kerak:**
```python
# blog/views.py
def post_detail(request, year, month, day, slug):
    # Postni topish va 404 xatoligini qaytarish
    # Template bilan render qilish
    pass
```

**Tekshirish:** URL orqali individual postga kirish mumkin bo'lishi kerak.

---

#### 2. Vazifa: URL pattern sozlash
**Maqsad:** Post detail uchun URL pattern yaratish

**Bajarilishi kerak:**
```python
# blog/urls.py
# <int:year>/<int:month>/<int:day>/<slug:slug>/ formatida URL
```

**Tekshirish:** URL `blog/2025/03/15/my-post/` formatida ishlashi kerak.

---

#### 3. Vazifa: Template yaratish
**Maqsad:** Post detail template yaratish

**Bajarilishi kerak:**
- Post title, content, author, publish date ko'rsatish
- Base template dan extend qilish
- Back link qo'shish

**Tekshirish:** Sahifa to'liq ma'lumotlar bilan ko'rsatilishi kerak.

---

### O'rta daraja vazifalar

#### 4. Vazifa: SEO optimizatsiyasi
**Maqsad:** Meta tags va SEO elementlar qo'shish

**Bajarilishi kerak:**
```html
<!-- post_detail.html -->
<meta name="description" content="...">
<meta name="author" content="...">
<meta property="og:title" content="...">
<!-- va boshqalar -->
```

**Tekshirish:** Page source da meta taglar ko'rinishi kerak.

---

#### 5. Vazifa: Error handling
**Maqsad:** 404 sahifasini yaratish va error handling

**Bajarilishi kerak:**
- Custom 404.html template
- get_object_or_404 ishlatish
- Friendly error messages

**Tekshirish:** Mavjud bo'lmagan URL ga kirganda 404 sahifa ko'rsatilishi.

---

#### 6. Vazifa: Template filterlari
**Maqsad:** Custom template filter yaratish

**Bajarilishi kerak:**
```python
# blog/templatetags/blog_tags.py
@register.filter
def reading_time(text):
    # O'qish vaqtini hisoblash (250 so'z/daqiqa)
    pass
```

**Tekshirish:** Template da `{{ post.body|reading_time }}` ishlashi kerak.

---

### Murakkab vazifalar (Har bir uchun 25 ball)

#### 7. Vazifa: Next/Previous navigation
**Maqsad:** Keyingi va oldingi postlarga o'tish

**Bajarilishi kerak:**
```python
def post_detail(request, year, month, day, slug):
    # ... mavjud kod
    
    # Previous post
    previous_post = Post.objects.filter(
        # ...
    ).first()
    
    # Next post  
    next_post = Post.objects.filter(
        # ...
    ).first()
    
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
    }
```

**Tekshirish:** Post detail sahifasida nav linklar ishlashi kerak.

---

#### 8. Vazifa: Related posts
**Maqsad:** O'xshash postlar ko'rsatish

**Bajarilishi kerak:**
- Bir xil author yoki bir xil vaqtdagi postlar
- Template da related posts section
- Maksimal 3 ta related post

**Tekshirish:** Post ostida "Related Posts" bo'limi ko'rinishi.

---

#### 9. Vazifa: Social sharing
**Maqsad:** Social media sharing tugmalari

**Bajarilishi kerak:**
```html
<!-- Facebook, Twitter, LinkedIn sharing links -->
<div class="social-sharing">
    <a href="https://www.facebook.com/sharer/sharer.php?u={{ request.build_absolute_uri }}">Facebook</a>
    <!-- ... -->
</div>
```

**Tekshirish:** Sharing linklar to'g'ri URL bilan ishlashi kerak.

---

#### 10. Vazifa: View counter
**Maqsad:** Post ko'rilgan soni hisoblash

**Bajarilishi kerak:**
```python
# models.py
class Post(models.Model):
    # ... mavjud fieldlar
    views = models.PositiveIntegerField(default=0)

# views.py  
def post_detail(request, year, month, day, slug):
    # ... 
    post.views += 1
    post.save(update_fields=['views'])
    # ...
```

**Tekshirish:** Har safar post ochilganda view count oshishi.

---

### Bonus vazifalar 

#### 11. Bonus: Breadcrumb navigation
**Maqsad:** Breadcrumb navigation qo'shish

**Bajarilishi kerak:**
```html
<!-- Home > Blog > 2025 > March > Post Title -->
<nav class="breadcrumb">
    <a href="/">Home</a> > 
    <a href="{% url 'blog:post_list' %}">Blog</a> > 
    {{ post.publish.year }} > 
    {{ post.title }}
</nav>
```

---

#### 12. Bonus: Print-friendly version
**Maqsad:** Print uchun optimallashtirilgan versiya

**Bajarilishi kerak:**
- CSS media query (@media print)
- Print tugmasi
- Unnecessary elementlarni yashirish

---

## Test cases

### Test 1: Asosiy funksionallik
```python
def test_post_detail_view():
    # Post yaratish
    # URL ga so'rov yuborish  
    # Status code 200 ekanligini tekshirish
    # Template contentni tekshirish
```

### Test 2: 404 Error
```python
def test_post_not_found():
    # Mavjud bo'lmagan URL
    # 404 status qaytarishini tekshirish
```

### Test 3: Slug validation
```python
def test_wrong_slug():
    # Noto'g'ri slug bilan URL
    # 404 qaytarishini tekshirish
```

## Baholash mezoni

| Vazifa | Ball | Talablar |
|--------|------|----------|
| 1-3 | 30 | Asosiy BlogDetail view ishlashi |
| 4-6 | 45 | SEO, error handling, filters |
| 7-10 | 100 | Navigation, related posts, social sharing, views |
| 11-12 | 60 | Breadcrumb, print version |
| **Jami** | **235** | |

## Topshirish formati

### 1. Kod fayllari
```
blog/
├── views.py          # BlogDetail view
├── urls.py           # URL patterns  
├── models.py         # Model o'zgarishlari (agar bor)
├── templatetags/
│   └── blog_tags.py  # Custom filters
└── templates/blog/
    ├── post_detail.html
    └── 404.html      # Custom 404 page
```

### 2. Screenshots
- Post detail sahifasining screenshoti
- 404 sahifasining screenshoti
- Mobile responsive view

### 3. Test natijalar
```bash
python manage.py test blog
```

## Texnik talablar

### Minimal talablar:
- Django 4.0+
- Python 3.8+
- SQLite database
- Bootstrap yoki custom CSS

### Tavsiya etilgan:
- Code comments
- Docstring'lar
- PEP8 standartlari
- Git commit'lar

## Foydali manbalar

### Django Documentation:
- [Function-based Views](https://docs.djangoproject.com/en/stable/topics/http/views/)
- [URL Routing](https://docs.djangoproject.com/en/stable/topics/http/urls/)
- [Templates](https://docs.djangoproject.com/en/stable/topics/templates/)

### CSS Framework'lar:
- [Bootstrap 5](https://getbootstrap.com/)
- [Tailwind CSS](https://tailwindcss.com/)

## Muvaffaqiyat ko'rsatkichlari

### Yetarli
- Asosiy BlogDetail view ishlaydi
- Template to'g'ri ko'rsatiladi
- URL routing sozlangan

### Yaxshi  
- SEO optimizatsiyasi qo'shilgan
- Error handling mavjud
- Template filters ishlaydi

### A'lo
- Barcha vazifalar bajarilgan
- Code sifatli va optimallashtirilgan
- Bonus vazifalar ham bajarilgan

## ❓ Tez-tez so'raladigan savollar

**S:** URL pattern ishlamayapti, nimaga?
**J:** URL pattern sintaksisini tekshiring va `app_name` ni urls.py da belgilagan ekanligingizni tasdiqlang.

**S:** 404 sahifa ko'rsatilmayapti?
**J:** `DEBUG = False` qilib qo'ying va `ALLOWED_HOSTS` ni sozlang.

**S:** Template da ma'lumotlar ko'rsatilmayapti?
**J:** Context da ma'lumotlar to'g'ri uzatilayotganligini va template path'ini tekshiring.

---
