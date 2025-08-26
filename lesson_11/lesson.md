# Lesson 11: Loyihaning starter codini ishga tushirish va virtual muhit o'rnatsish

## Maqsad
Ushbu darsda siz o'rganasiz:
- Virtual muhit (Virtual Environment) nima va nima uchun kerak
- Python virtual muhitini yaratish va faollashtirish
- Django loyihasining starter kodini ishga tushirish
- Kerakli kutubxonalarni o'rnatish va loyihani sozlash

## 1. Virtual Muhit (Virtual Environment) haqida

### Virtual muhit nima?
Virtual muhit - bu Python loyihalari uchun alohida, izolyatsiya qilingan muhit yaratish usuli. Har bir loyiha o'zining kutubxonalari va Python versiyasiga ega bo'ladi.

### Nima uchun virtual muhit kerak?

**Muammolar:**
- Turli loyihalar turli versiyali kutubxonalar talab qilishi
- Global Python muhitida kutubxonalar to'qnashuvi
- Loyiha boshqa kompyuterda ishlamaslik xavfi

**Yechim - Virtual muhit:**
```
Kompyuter
├── Python (global)
│   ├── Django 4.0
│   └── requests 2.25
├── Virtual Env 1 (news_project)
│   ├── Django 4.2
│   └── requests 2.28
└── Virtual Env 2 (blog_project)
    ├── Django 3.2
    └── requests 2.26
```

## 2. Virtual muhitni yaratish va faollashtirish

### Windows uchun:

#### 1-qadam: Virtual muhit yaratish
```bash
# Loyiha papkasiga kiring
cd path/to/your/project

# Virtual muhit yaratish
python -m venv news_env
```

#### 2-qadam: Virtual muhitni faollashtirish
```bash
# Windows CMD
news_env\Scripts\activate

# Windows PowerShell
news_env\Scripts\Activate.ps1

# Git Bash
source news_env/Scripts/activate
```

### Mac/Linux uchun:

#### 1-qadam: Virtual muhit yaratish
```bash
# Loyiha papkasiga kiring
cd path/to/your/project

# Virtual muhit yaratish
python3 -m venv news_env
```

#### 2-qadam: Virtual muhitni faollashtirish
```bash
source news_env/bin/activate
```

### Faollashtirish tekshiruvi
Virtual muhit faollashganda terminal oldida `(news_env)` ko'rinadi:
```bash
(news_env) C:\Users\Username\project>
```

## 3. Django o'rnatish va loyiha yaratish

### Django o'rnatish
```bash
# Virtual muhit faollashtirilgan holda
pip install django

# Ma'lum versiyani o'rnatish
pip install django==4.2
```

### O'rnatilgan kutubxonalarni ko'rish
```bash
pip list
```

### Django versiyasini tekshirish
```bash
django-admin --version
```

## 4. Yangi Django loyiha yaratish

### Loyiha yaratish
```bash
# Yangi loyiha yaratish
django-admin startproject news_project

# Yoki joriy papkada yaratish
django-admin startproject news_project .
```

### Loyiha tuzilishi
```
news_project/
├── manage.py
└── news_project/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── asgi.py
```

### Fayllarning vazifasi:
- **manage.py** - Loyiha boshqaruv buyruqlari
- **settings.py** - Loyiha sozlamalari
- **urls.py** - URL marshrutlari
- **wsgi.py** - Web server uchun konfiguratsiya
- **asgi.py** - Asinxron server uchun konfiguratsiya

## 5. Loyihani ishga tushirish

### Ma'lumotlar bazasini tayyorlash
```bash
# Loyiha papkasiga kiring
cd news_project

# Migratsiyalar qilish
python manage.py migrate
```

### Development server ishga tushirish
```bash
python manage.py runserver
```

### Brauzerda ochish
```
http://127.0.0.1:8000/
yoki
http://localhost:8000/
```

### Boshqa portda ishga tushirish
```bash
python manage.py runserver 8080
python manage.py runserver 0.0.0.0:8000  # barcha IP manzillarda
```

## 6. Loyiha sozlamalari (settings.py)

### Muhim sozlamalar:

#### Debug rejimi
```python
# Development uchun
DEBUG = True

# Production uchun
DEBUG = False
```

#### Ruxsat etilgan hostlar
```python
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'your-domain.com'
]
```

#### Ma'lumotlar bazasi
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Til va vaqt zonasi
```python
LANGUAGE_CODE = 'uz-uz'  # o'zbek tili
TIME_ZONE = 'Asia/Tashkent'  # Toshkent vaqti
USE_I18N = True
USE_TZ = True
```

## 7. Requirements.txt yaratish

### Kutubxonalar ro'yxatini saqlash
```bash
pip freeze > requirements.txt
```

### Requirements.txt misoli
```
Django==4.2.7
asgiref==3.7.2
sqlparse==0.4.4
tzdata==2023.3
```

### Kutubxonalarni o'rnatish (boshqa kompyuterda)
```bash
pip install -r requirements.txt
```

## 8. Superuser yaratish

### Admin paneli uchun foydalanuvchi yaratish
```bash
python manage.py createsuperuser
```

Kerakli ma'lumotlar:
- Username
- Email address (ixtiyoriy)
- Password

### Admin panelga kirish
```
http://127.0.0.1:8000/admin/
```

## 9. Loyiha fayl tuzilishi

### To'liq loyiha tuzilishi
```
news_project/
├── news_env/                 # Virtual muhit
│   ├── Scripts/              # Windows
│   └── Lib/
├── news_project/             # Loyiha papkasi
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── manage.py
├── db.sqlite3               # Ma'lumotlar bazasi
└── requirements.txt         # Kutubxonalar ro'yxati
```

## 10. Muhim buyruqlar ro'yxati

### Virtual muhit bilan ishlash
```bash
# Yaratish
python -m venv env_name

# Faollashtirish (Windows)
env_name\Scripts\activate

# Faollashtirish (Mac/Linux)
source env_name/bin/activate

# O'chirish
deactivate
```

### Django buyruqlari
```bash
# Loyiha yaratish
django-admin startproject project_name

# Server ishga tushirish
python manage.py runserver

# Migratsiya qilish
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# App yaratish
python manage.py startapp app_name
```

### Pip buyruqlari
```bash
# Kutubxona o'rnatish
pip install package_name

# Requirements saqlash
pip freeze > requirements.txt

# Requirements o'rnatish
pip install -r requirements.txt

# O'rnatilgan kutubxonalar
pip list
```

## Xulosa

Ushbu darsda siz o'rgandingiz:
- Virtual muhit yaratish va faollashtirish
- Django o'rnatish va loyiha yaratish  
- Development server ishga tushirish
- Asosiy Django sozlamalari
- Requirements.txt bilan ishlash
- Superuser yaratish

Keyingi darsda biz Django loyihasida app yaratish va asosiy komponentlar bilan tanishishni o'rganamiz.