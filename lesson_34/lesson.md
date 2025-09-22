# Lesson 34: Foydalanuvchi parolini qayta tiklash (1-qism)

## Kirish

Veb-ilovalar yaratishda foydalanuvchilar tez-tez parollarini unutib qolishadi. Bu holatlarda parolni qayta tiklash funksiyasi juda muhimdir. Django foydalanuvchi parolini qayta tiklash uchun tayyor funksionalni taqdim etadi.

Bu darsda biz parol qayta tiklash jarayonining birinchi qismini o'rganamiz:
- Parol qayta tiklash formalarini yaratish
- E-mail orqali tasdiqlash havolasini yuborish
- Django'ning built-in authentication viewlaridan foydalanish

## Django'da parol qayta tiklash mexanizmi

Django parol qayta tiklashni 4 bosqichda amalga oshiradi:

1. **Password Reset Form** - Foydalanuvchi email manzilini kiritadi
2. **Password Reset Done** - Email yuborilgani haqida xabar
3. **Password Reset Confirm** - Yangi parolni o'rnatish formasi
4. **Password Reset Complete** - Parol muvaffaqiyatli o'zgartirildi xabari

## 1-bosqich: URLs konfiguratsiyasi

Avval parol qayta tiklash uchun URLlarni sozlaymiz.

**accounts/urls.py** faylini yangilaymiz:

```python
# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # ... mavjud URLlar ...
    
    # Parol qayta tiklash URLlari
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
]
```

### URL parametrlarini tushuntirish:

- `<uidb64>` - Foydalanuvchi ID sining base64 ko'rinishi
- `<token>` - Parolni qayta tiklash uchun maxsus token

## 2-bosqich: Template yaratish

**templates/registration/** papkasini yaratamiz va parol qayta tiklash templatelarini qo'shamiz.

### Password Reset Form Template

**templates/registration/password_reset_form.html**:

```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Parolni qayta tiklash</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h4 class="text-center">Parolni qayta tiklash</h4>
                    </div>
                    <div class="card-body">
                        <p class="text-muted">
                            Parolingizni unutdingizmi? Email manzilingizni kiriting va biz sizga 
                            yangi parol o'rnatish uchun havola yuboramiz.
                        </p>
                        
                        <form method="post">
                            {% csrf_token %}
                            
                            {% if form.non_field_errors %}
                                <div class="alert alert-danger">
                                    {{ form.non_field_errors }}
                                </div>
                            {% endif %}
                            
                            <div class="mb-3">
                                <label for="{{ form.email.id_for_label }}" class="form-label">
                                    Email manzili
                                </label>
                                {{ form.email }}
                                {% if form.email.errors %}
                                    <div class="text-danger">
                                        {{ form.email.errors }}
                                    </div>
                                {% endif %}
                            </div>
                            
                            <div class="d-grid gap-2">
                                <button type="submit" class="btn btn-primary">
                                    Parolni qayta tiklash
                                </button>
                            </div>
                        </form>
                        
                        <div class="text-center mt-3">
                            <a href="{% url 'accounts:login' %}" class="text-decoration-none">
                                Hisobingizni eslaysizmi? Kirish
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

### Password Reset Done Template

**templates/registration/password_reset_done.html**:

```html
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email yuborildi</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h4 class="text-center text-success">Email yuborildi!</h4>
                    </div>
                    <div class="card-body text-center">
                        <div class="mb-4">
                            <i class="fas fa-envelope fa-3x text-success"></i>
                        </div>
                        
                        <p class="lead">
                            Parolni qayta tiklash bo'yicha ko'rsatmalar email manzilingizga yuborildi.
                        </p>
                        
                        <p class="text-muted">
                            Agar email kelmagan bo'lsa, spam papkasini tekshiring yoki 
                            email manzili to'g'ri kiritilganligini tasdiqlang.
                        </p>
                        
                        <div class="mt-4">
                            <a href="{% url 'accounts:login' %}" class="btn btn-outline-primary">
                                Kirish sahifasiga qaytish
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

## 3-bosqich: Email sozlamalari

Parol qayta tiklash email yuborish uchun email konfiguratsiyasini sozlash kerak.

**settings.py** fayliga quyidagilarni qo'shamiz:

```python
# settings.py

# Email sozlamalari (development uchun console backend)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Production uchun SMTP sozlamalari (ixtiyoriy)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'sizning_email@gmail.com'
# EMAIL_HOST_PASSWORD = 'sizning_parolingiz'

# Parol qayta tiklash sozlamalari
PASSWORD_RESET_TIMEOUT = 3600  # 1 soat (sekund hisobida)

# Standart email manzili
DEFAULT_FROM_EMAIL = 'noreply@saytingiz.com'
```

### Email backend turlari:

1. **Console Backend** - Emailni terminalda ko'rsatadi (development)
2. **SMTP Backend** - Haqiqiy email yuboradi (production)
3. **File Backend** - Emailni faylga saqlaydi

## 4-bosqich: Login templatega havola qo'shish

Login sahifasiga "Parolni unutdingizmi?" havolasini qo'shamiz.

**templates/registration/login.html** faylini yangilaymiz:

```html
<!-- login.html ning pastki qismiga qo'shing -->
<div class="text-center mt-3">
    <a href="{% url 'accounts:password_reset' %}" class="text-decoration-none">
        Parolni unutdingizmi?
    </a>
</div>
```

## 5-bosqich: Email template yaratish

Django avtomatik ravishda email template yaratadi, lekin biz uni o'zgartirishimiz mumkin.

**templates/registration/password_reset_email.html**:

```html
{% load i18n %}{% autoescape off %}
{% blocktrans %}{{ user.get_username }} salom,

Sizning {{ site_name }} saytidagi hisobingiz uchun parol qayta tiklash so'rovi yuborildi.

Parolni qayta tiklash uchun quyidagi havolaga bosing:
{{ protocol }}://{{ domain }}{% url 'accounts:password_reset_confirm' uidb64=uid token=token %}

Agar siz bu so'rovni yubormasangiz, bu xabarni e'tiborsiz qoldiring.

Hurmat bilan,
{{ site_name }} jamoasi
{% endblocktrans %}
{% endautoescape %}
```

**templates/registration/password_reset_subject.txt**:

```
{{ site_name }} - Parolni qayta tiklash
```

## Django'ning parol qayta tiklash viewlari

Django quyidagi tayyor viewlarni taqdim etadi:

### 1. PasswordResetView
- Foydalanuvchi email kiritadi
- Email mavjudligini tekshiradi
- Qayta tiklash emailini yuboradi

```python
# Django ichida quyidagicha ishlaydi:
class PasswordResetView(FormView):
    template_name = 'registration/password_reset_form.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')
```

### 2. PasswordResetDoneView
- Email yuborilgani haqida xabar beradi
- Oddiy template ko'rsatadi

### 3. PasswordResetConfirmView
- Email orqali kelgan havolani qayta ishlaydi
- Token va uidb64 ni tekshiradi
- Yangi parol belgilash formasini ko'rsatadi

### 4. PasswordResetCompleteView
- Parol muvaffaqiyatli o'zgartirilgani haqida xabar

## Xavfsizlik masalalari

Django parol qayta tiklashda quyidagi xavfsizlik choralarini ko'radi:

1. **Token yaratish**: Har bir so'rov uchun noyob token
2. **Vaqt chegarasi**: Token muayyan vaqtdan keyin amal qilmaydi
3. **Foydalanuvchi tekshiruvi**: Faqat mavjud email manzillari uchun
4. **CSRF himoyasi**: Formalar CSRF token bilan himoyalangan

## Test qilish

1. Serverni ishga tushiring:
```bash
python manage.py runserver
```

2. `/accounts/password-reset/` ga o'ting

3. Mavjud foydalanuvchining email manzilini kiriting

4. Terminalda email matnini ko'ring (console backend ishlatganda)

5. Emaildagi havolaga bosing

## Xatolar va ularni hal qilish

### 1. Email yuborilmaydi
```python
# settings.py da EMAIL_BACKEND ni tekshiring
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### 2. Template topilmaydi
```python
# TEMPLATES sozlamalarini tekshiring
TEMPLATES = [
    {
        'DIRS': [BASE_DIR / 'templates'],
        # ...
    }
]
```

### 3. URL xatosi
```python
# accounts/urls.py da URL nomi to'g'ri bo'lsin
path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset')
```

## Keyingi dars

Keyingi darsda (lesson_35) biz:
- Password Reset Confirm viewini batafsil o'rganamiz
- Yangi parol o'rnatish formasini yaratamiz
- Parol qayta tiklash jarayonini yakunlaymiz
- Production muhitda email sozlamalarini o'rnatamiz

## Xulosa

Bu darsda biz Django'da parol qayta tiklash funksiyasining birinchi qismini amalga oshirdik:

1. **URL konfiguratsiyasi** - Parol qayta tiklash uchun yo'llar
2. **Template yaratish** - Forma va muvaffaqiyat sahifalari
3. **Email sozlamalari** - Email yuborish konfiguratsiyasi
4. **Xavfsizlik** - Django'ning built-in himoya vositalari

Django'ning tayyor authentication viewlari ko'p vaqt va kuch tejaydi, shu bilan birga yuqori darajadagi xavfsizlikni ta'minlaydi.