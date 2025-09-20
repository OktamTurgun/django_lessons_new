# Lesson 33: Login va Logout

## Kirish

Django'da foydalanuvchi autentifikatsiyasi veb-dasturlashning eng muhim qismlaridan biridir. Bu darsda biz Django'ning o'rnatilgan autentifikatsiya tizimi yordamida login va logout funksiyalarini qanday yaratishni o'rganamiz.

Django bizga tayyor authentication views va formalarni taqdim etadi, bu esa juda tez va xavfsiz tarzda login/logout funksiyalarini amalga oshirishga yordam beradi.

## Django Authentication Tizimi

Django'da autentifikatsiya tizimi quyidagi komponentlardan iborat:

- **User model** - foydalanuvchi ma'lumotlarini saqlash
- **Authentication views** - login, logout kabi sahifalar
- **Forms** - login formasini yaratish
- **Middleware** - so'rovlarni qayta ishlash
- **Decorators** - sahifalarni himoyalash

## 1. URLs ni sozlash

Avval loyihamizning asosiy `urls.py` faylida authentication URL'larini qo'shamiz:

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Yangi qo'shilgan
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Nima qildi?

- `path('accounts/', include('django.contrib.auth.urls'))` - Django'ning o'rnatilgan authentication URL'larini qo'shdik
- Bu bizga quyidagi URL'larni beradi:
  - `/accounts/login/` - login sahifasi
  - `/accounts/logout/` - logout
  - `/accounts/password_change/` - parol o'zgartirish
  - `/accounts/password_reset/` - parol qayta tiklash
  - va boshqalar

## 2. Login Template yaratish

Django authentication views uchun template yaratishimiz kerak. `templates/registration/` papka yarating va ichida login.html faylini yarating:

```html
<!-- templates/registration/login.html -->
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Saytga kirish</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-md-6">
                <div class="card shadow">
                    <div class="card-header bg-primary text-white">
                        <h4 class="mb-0">Saytga kirish</h4>
                    </div>
                    <div class="card-body">
                        {% if form.errors %}
                            <div class="alert alert-danger">
                                <strong>Xato!</strong> Foydalanuvchi nomi yoki parol noto'g'ri.
                            </div>
                        {% endif %}

                        <form method="post">
                            {% csrf_token %}
                            <div class="mb-3">
                                <label for="{{ form.username.id_for_label }}" class="form-label">
                                    Foydalanuvchi nomi:
                                </label>
                                {{ form.username }}
                            </div>
                            
                            <div class="mb-3">
                                <label for="{{ form.password.id_for_label }}" class="form-label">
                                    Parol:
                                </label>
                                {{ form.password }}
                            </div>

                            <div class="d-grid">
                                <button type="submit" class="btn btn-primary">Kirish</button>
                            </div>
                            
                            <input type="hidden" name="next" value="{{ next }}" />
                        </form>
                        
                        <div class="text-center mt-3">
                            <a href="{% url 'news:home' %}" class="btn btn-outline-secondary">
                                Bosh sahifaga qaytish
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### Kod tushuntirish:

- `{% csrf_token %}` - CSRF (Cross-Site Request Forgery) hujumlardan himoyalaydi
- `{{ form.username }}` va `{{ form.password }}` - Django forma maydonlari
- `{{ next }}` - login qilgandan keyin qaysi sahifaga yo'naltirishni ko'rsatadi
- `form.errors` - forma xatolarini ko'rsatadi

## 3. Logout funksiyasini qo'shish

Base template'da login/logout havolalarini qo'shamiz:

```html
<!-- templates/base.html -->
<!-- Navigation qismida qo'shish -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">
        <a class="navbar-brand" href="{% url 'news:home' %}">Yangiliklar</a>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav me-auto">
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'news:home' %}">Bosh sahifa</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'news:category_list' %}">Kategoriyalar</a>
                </li>
            </ul>
            
            <!-- Authentication links -->
            <ul class="navbar-nav">
                {% if user.is_authenticated %}
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                            {{ user.username }}
                        </a>
                        <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#">Profil</a></li>
                            <li><a class="dropdown-item" href="#">Sozlamalar</a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{% url 'logout' %}">Chiqish</a></li>
                        </ul>
                    </li>
                {% else %}
                    <li class="nav-item">
                        <a class="nav-link" href="{% url 'login' %}">Kirish</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Ro'yxatdan o'tish</a>
                    </li>
                {% endif %}
            </ul>
        </div>
    </div>
</nav>
```

### Kod tushuntirish:

- `user.is_authenticated` - foydalanuvchi login qilganligini tekshiradi
- `{{ user.username }}` - foydalanuvchi nomini ko'rsatadi
- `{% url 'login' %}` va `{% url 'logout' %}` - login va logout sahifalariga havola

## 4. Settings.py ni sozlash

Login va logout'dan keyin qaysi sahifaga yo'naltirishni sozlash:

```python
# config/settings.py

# ... boshqa sozlamalar

# Authentication sozlamalari
LOGIN_URL = 'login'  # Login qilish sahifasi URL nomi
LOGIN_REDIRECT_URL = '/'  # Login qilgandan keyin yo'naltirish
LOGOUT_REDIRECT_URL = '/'  # Logout qilgandan keyin yo'naltirish
```

### Nima qiladi?

- `LOGIN_URL` - himoyalangan sahifaga kirishga urinishda qaysi sahifaga yo'naltirishni ko'rsatadi
- `LOGIN_REDIRECT_URL` - login qilgandan keyin qaysi sahifaga borishni belgilaydi
- `LOGOUT_REDIRECT_URL` - logout qilgandan keyin qaysi sahifaga borishni belgilaydi

## 5. Himoyalangan sahifalar yaratish

Faqat login qilgan foydalanuvchilar ko'ra oladigan sahifa yarataylik:

```python
# news/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Funksiya view uchun
@login_required
def add_news(request):
    """Faqat login qilgan foydalanuvchilar yangilik qo'sha oladi"""
    if request.method == 'POST':
        # Yangilik qo'shish logikasi
        pass
    return render(request, 'news/add_news.html')

# Class view uchun
class NewsCreateView(LoginRequiredMixin, CreateView):
    """Faqat login qilgan foydalanuvchilar uchun"""
    model = News
    fields = ['title', 'slug', 'body', 'category', 'photo']
    template_name = 'news/news_form.html'
```

### Kod tushuntirish:

- `@login_required` - funksiya uchun login talab qiladigan dekorator
- `LoginRequiredMixin` - class view uchun login talab qiladigan mixin
- Agar foydalanuvchi login qilmagan bo'lsa, login sahifasiga yo'naltiriladi

## 6. Template'da foydalanuvchi holatini tekshirish

```html
<!-- news/templates/news/news_detail.html -->
<div class="article-actions">
    {% if user.is_authenticated %}
        <!-- Login qilgan foydalanuvchilar uchun -->
        <div class="btn-group" role="group">
            {% if user == object.author %}
                <!-- Faqat muallif ko'ra oladi -->
                <a href="#" class="btn btn-warning btn-sm">Tahrirlash</a>
                <a href="#" class="btn btn-danger btn-sm">O'chirish</a>
            {% endif %}
            <button class="btn btn-success btn-sm">Like</button>
            <button class="btn btn-primary btn-sm">Izoh qoldirish</button>
        </div>
    {% else %}
        <!-- Login qilmagan foydalanuvchilar uchun -->
        <div class="alert alert-info">
            Izoh qoldirish uchun <a href="{% url 'login' %}">saytga kiring</a>.
        </div>
    {% endif %}
</div>
```

## 7. Superuser yaratish

Login qilish uchun foydalanuvchi yaratamiz:

```bash
# Terminal'da
python manage.py createsuperuser
```

Keyin quyidagi ma'lumotlarni kiriting:
- Username: admin
- Email: admin@example.com
- Password: (xavfsiz parol)

## 8. Test qilish

1. Serverni ishga tushiring:
```bash
python manage.py runserver
```

2. Brauzerda quyidagi sahifalarni sinab ko'ring:
   - `http://127.0.0.1:8000/accounts/login/` - Login sahifasi
   - `http://127.0.0.1:8000/admin/` - Admin sahifa
   - Login qiling va navigation'da o'z ismingizni ko'ring
   - "Chiqish" tugmasini bosib logout qiling

## Xatolarni tuzatish

### Keng uchraydigan xatolar:

1. **Template topilmadi xatosi:**
```
TemplateDoesNotExist: registration/login.html
```
**Yechim:** `templates/registration/` papkasini to'g'ri yaratganligingizni tekshiring.

2. **CSRF token xatosi:**
```
Forbidden (403) CSRF verification failed
```
**Yechim:** Formaga `{% csrf_token %}` qo'shganligingizni tekshiring.

3. **URL topilmadi xatosi:**
```
NoReverseMatch: Reverse for 'login' not found
```
**Yechim:** `config/urls.py` faylida authentication URL'larini qo'shganligingizni tekshiring.

## Xulosa

Bu darsda biz Django'da login va logout funksiyalarini qanday amalga oshirishni o'rgandik:

1. Django'ning o'rnatilgan authentication tizimini ishlatdik
2. Login template yaratdik
3. Navigation'da login/logout havolalarini qo'shdik
4. Settings.py'da redirect URL'larni sozladik
5. Himoyalangan sahifalar yaratdik
6. Template'da foydalanuvchi holatini tekshirishni o'rgandik

Keyingi darsda foydalanuvchi profilini yaratish va tahrirlash bilan ishlashni o'rganamiz.

## Dars jarayonida o'rganilgan asosiy tushunchalar

- **Authentication** - foydalanuvchini aniqlash jarayoni
- **Authorization** - foydalanuvchi huquqlarini tekshirish
- **Session** - foydalanuvchi ma'lumotlarini vaqtinchalik saqlash
- **CSRF Token** - Cross-Site Request Forgery hujumlardan himoya
- **LoginRequiredMixin** - class view'lar uchun login talab qiluvchi mixin
- **@login_required** - funksiya view'lar uchun login dekorator

## Keyingi darsda

Keyingi 34-darsda biz quyidagilarni o'rganamiz:
- Foydalanuvchi profilini yaratish va sozlash
- Profile model yaratish
- Foydalanuvchi ma'lumotlarini ko'rsatish va tahrirlash
- Avatar (profil rasmi) qo'shish funksiyasi

## Best Practices (Eng yaxshi amaliyotlar)

1. **Xavfsizlik:**
   - Har doim CSRF protection ishlatish
   - LOGIN_URL ni to'g'ri sozlash
   - Himoyalangan sahifalar uchun decoratorlar ishlatish
   - Kuchli parollar talab qilish
   - Session timeout ni moslashtirish

2. **Foydalanuvchi tajribasi:**
   - Login forma xatolarini aniq ko'rsatish
   - Login qilgandan keyin to'g'ri sahifaga yo'naltirish
   - Navigation'da foydalanuvchi holatini aniq ko'rsatish
   - "Remember me" funksiyasini qo'shish
   - Logout dan keyin tasdiqlash xabari

3. **Kod tashkil etish:**
   - Authentication template'larini `registration/` papkasida saqlash
   - URL pattern'larni mantiqiy tarzda tashkil etish
   - Himoyalangan view'lar uchun mixin'larni ishlatish
   - Custom authentication backend yaratish (kerak bo'lganda)
   - Signal'lardan foydalanib user yaratilganda qo'shimcha amallar

4. **Template dizayni:**
   - Bootstrap yoki boshqa CSS framework ishlatish
   - Responsive dizayn yaratish
   - Accessibility (qo'llanuvchilik) qoidalariga rioya qilish
   - Form validatsiya xabarlari uchun JavaScript qo'shish
   - Loading state'larni ko'rsatish

5. **Performance:**
   - Session ma'lumotlarini database'da saqlash (production uchun)
   - Static fayllarni CDN orqali yuklash
   - Template caching ishlatish
   - Database query'larni optimizatsiya qilish

## Takrorlash savollari

1. Django'da authentication URL'lari qanday qo'shiladi?
2. `LOGIN_REDIRECT_URL` va `LOGOUT_REDIRECT_URL` ning vazifasi nima?
3. `@login_required` dekorator qachon va qanday ishlatiladi?
4. CSRF token nima uchun kerak va qanday ishlatiladi?
5. `LoginRequiredMixin` va `@login_required` orasidagi farq nima?

Bu savollarning javoblarini bilsangiz, darsni yaxshi o'zlashtirganingizni anglatadi!