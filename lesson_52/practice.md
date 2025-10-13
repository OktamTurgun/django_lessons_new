# Dars 52: Practice - Deployment: Ahost serveriga joylash (1-qism)

## Amaliyot maqsadi

Bu amaliyotda siz o'z Django loyihangizni to'liq deployment uchun tayyorlab, Ahost serveriga joylashtirish jarayonini bosqichma-bosqich bajarasiz.

## Boshlash oldidan tekshiring

- [ ] Django loyihangiz to'liq ishlayotganligini tekshiring
- [ ] GitHub akkauntingiz bor
- [ ] Ahost.uz da akkaunt ochganingizni tekshiring
- [ ] VPS server sotib olganingizni yoki test serveringiz borligini tekshiring

---

## 1-Mashq: Loyihani deployment uchun tayyorlash

### 1.1: requirements.txt yaratish

**Vazifa:** Barcha kerakli kutubxonalarni ro'yxatga oling.

```bash
# Terminalda
cd /loyihangiz/papkasi

# Agar Pipenv ishlatayotgan bo'lsangiz
pipenv lock -r > requirements.txt

# Agar pip ishlatayotgan bo'lsangiz
pip freeze > requirements.txt
```

**Tekshirish:** requirements.txt faylini oching va quyidagilar borligini tekshiring:

```text
Django>=5.0
gunicorn>=21.0
psycopg2-binary>=2.9
python-decouple>=3.8
Pillow>=10.0
django-crispy-forms>=2.0
```

### 1.2: .env faylini yaratish

**Vazifa:** Loyiha ildiz papkasida `.env` faylini yarating.

```bash
# .env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (hozircha local)
DB_NAME=newsdb
DB_USER=newsuser
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```

**Muhim:** SECRET_KEY ni yangi qiymat bilan almashtiring.

```python
# Python console da yangi SECRET_KEY yaratish
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 1.3: settings.py ni o'zgartirish

**Vazifa:** `config/settings.py` faylini o'zgartiring.

```python
# config/settings.py

from pathlib import Path
from decouple import config, Csv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY ni .env dan olish
SECRET_KEY = config('SECRET_KEY')

# DEBUG
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
```

**Tekshirish:** Loyihani ishga tushiring va xato yo'qligini tekshiring.

```bash
python manage.py runserver
```

### 1.4: .gitignore faylini to'ldirish

**Vazifa:** `.gitignore` faylini yarating yoki to'ldiring.

```gitignore
# .gitignore

# Python
*.pyc
__pycache__/
*.py[cod]
*$py.class
*.so

# Django
*.log
db.sqlite3
db.sqlite3-journal
/media
/staticfiles

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
htmlcov/
.pytest_cache/
```

### 1.5: Deployment checklist

**Vazifa:** Django'ning deployment checklist'ini ishga tushiring.

```bash
python manage.py check --deploy
```

**Natija:** Barcha ogohlantirishlarni o'qing va tushunib oling.

---

## 2-Mashq: GitHub'ga yuklash

### 2.1: Git repository yaratish

```bash
# Git boshlash
git init

# Fayllarni qo'shish
git add .

# Commit qilish
git commit -m "Deployment uchun tayyor: settings, requirements, .env sozlandi"
```

### 2.2: GitHub'ga yuklash

```bash
# GitHub repository yaratganingizdan keyin
git remote add origin https://github.com/username/newssite.git
git branch -M main
git push -u origin main
```

**Tekshirish:** GitHub'da repository ochilganini va `.env` fayli yuklanmaganini tekshiring.

---

## 3-Mashq: Ahost serveriga ulanish

### 3.1: Server ma'lumotlarini to'plash

Ahost'dan kelgan ma'lumotlarni yozib oling:

```
IP Address: ___________________
Username: root
Password: ___________________
SSH Port: 22
```

### 3.2: SSH orqali ulanish

**Windows (PowerShell/CMD):**

```bash
ssh root@YOUR_SERVER_IP
```

**Mac/Linux (Terminal):**

```bash
ssh root@YOUR_SERVER_IP
```

**Birinchi ulanish:**
- Parolni kiriting (ko'rinmaydi)
- "yes" deb fingerprint ni tasdiqlang

**Muvaffaqiyatli ulanish:**

```bash
root@server:~#
```

### 3.3: Parolni o'zgartirish (tavsiya etiladi)

```bash
passwd
```

Yangi parolni 2 marta kiriting va yozib qo'ying!

---

## 4-Mashq: Serverni sozlash

### 4.1: Tizimni yangilash

```bash
# Sistema paketlarini yangilash
apt update
apt upgrade -y
```

**Kutish vaqti:** 5-10 daqiqa

### 4.2: Zarur paketlarni o'rnatish

```bash
# Barcha kerakli paketlarni o'rnatish
apt install -y python3-pip python3-dev python3-venv libpq-dev postgresql postgresql-contrib nginx curl git
```

### 4.3: Python versiyasini tekshirish

```bash
python3 --version
pip3 --version
```

**Kutilgan natija:** Python 3.8+ va pip3

---

## 5-Mashq: PostgreSQL ni sozlash

### 5.1: PostgreSQL ni ishga tushirish

```bash
# PostgreSQL ni ishga tushirish
systemctl start postgresql
systemctl enable postgresql

# Statusni tekshirish
systemctl status postgresql
```

**Kutilgan natija:** `active (running)`

### 5.2: Ma'lumotlar bazasi yaratish

```bash
# PostgreSQL ga kirish
sudo -u postgres psql
```

PostgreSQL ichida:

```sql
-- Ma'lumotlar bazasi yaratish
CREATE DATABASE newsdb;

-- Foydalanuvchi yaratish (KUCHLI parol kiriting!)
CREATE USER newsuser WITH PASSWORD 'Quvv@tliP@rol123!';

-- Sozlamalar
ALTER ROLE newsuser SET client_encoding TO 'utf8';
ALTER ROLE newsuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE newsuser SET timezone TO 'Asia/Tashkent';

-- Ruxsatlar berish
GRANT ALL PRIVILEGES ON DATABASE newsdb TO newsuser;

-- Chiqish
\q
```

### 5.3: Ma'lumotlar bazasini tekshirish

```bash
# newsuser sifatida ulanish
psql -U newsuser -d newsdb -h localhost

# Ichida:
\dt  # Jadvallarni ko'rish (hali bo'sh)
\q   # Chiqish
```

**Tekshirish:** Xatosiz ulanish.

---

## 6-Mashq: Loyiha papkasini yaratish

### 6.1: Papka strukturasini yaratish

```bash
# Home papkasiga o'tish
cd /home

# Loyiha papkasini yaratish
mkdir newssite
cd newssite
```

### 6.2: Virtual muhit yaratish

```bash
# Virtual muhit yaratish
python3 -m venv venv

# Faollashtirish
source venv/bin/activate
```

**Kutilgan natija:** Prompt o'zgaradi:

```bash
(venv) root@server:/home/newssite#
```

---

## 7-Mashq: Loyihani serverga yuklash

### 7.1: Git orqali clone qilish

```bash
# Loyiha papkasida ekanligingizga ishonch hosil qiling
cd /home/newssite

# GitHub'dan clone qilish (o'z repository manzilingizni yozing)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .

# Nuqta (.) muhim - joriy papkaga clone qiladi
```

**Tekshirish:** Fayllar ko'rinishini tekshiring:

```bash
ls -la
```

Natija:
```
manage.py
config/
news/
accounts/
pages/
templates/
static/
requirements.txt
.gitignore
```

### 7.2: Requirements o'rnatish

```bash
# Virtual muhit faol ekanligini tekshiring
source venv/bin/activate

# Paketlarni o'rnatish
pip install -r requirements.txt

# Qo'shimcha paketlar
pip install gunicorn psycopg2-binary
```

**Kutish vaqti:** 3-5 daqiqa

**Tekshirish:**

```bash
pip list | grep Django
pip list | grep gunicorn
```

---

## 8-Mashq: .env faylini serverda sozlash

### 8.1: .env faylini yaratish

```bash
cd /home/newssite
nano .env
```

### 8.2: Ma'lumotlarni to'ldirish

```bash
# Production settings
SECRET_KEY=YANGI-QUVVATLI-SECRET-KEY-YARATING
DEBUG=False
ALLOWED_HOSTS=YOUR_SERVER_IP,yourdomain.uz

# Database
DB_NAME=newsdb
DB_USER=newsuser
DB_PASSWORD=Quvv@tliP@rol123!
DB_HOST=localhost
DB_PORT=5432
```

**Saqlash:** Ctrl + X, keyin Y, keyin Enter

**Tekshirish:**

```bash
cat .env
```

---

## 9-Mashq: Migratsiyalar va static fayllar

### 9.1: Database migratsiyalari

```bash
# Virtual muhit faol ekanligini tekshiring
cd /home/newssite
source venv/bin/activate

# Migratsiyalarni tekshirish
python manage.py makemigrations

# Migratsiyalarni bajarish
python manage.py migrate
```

**Kutilgan natija:**

```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
```

### 9.2: Superuser yaratish

```bash
python manage.py createsuperuser
```

Ma'lumotlarni kiriting:
- Username: admin
- Email: admin@example.com
- Password: (kuchli parol)

### 9.3: Static fayllarni yig'ish

```bash
python manage.py collectstatic --no-input
```

**Kutilgan natija:**

```
123 static files copied to '/home/newssite/staticfiles'
```

**Tekshirish:**

```bash
ls -la staticfiles/
```

---

## 10-Mashq: Gunicorn bilan test qilish

### 10.1: Gunicorn ni ishga tushirish

```bash
cd /home/newssite
source venv/bin/activate

# Gunicorn ni test qilish
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```

**Kutilgan natija:**

```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 12345
```

### 10.2: Brauzerda ochish

Yangi brauzer oynasida:

```
http://YOUR_SERVER_IP:8000
```

**Kutilgan natija:** Saytingiz ochilishi kerak (lekin CSS/JS ishlamasligi mumkin)

### 10.3: Admin panelni tekshirish

```
http://YOUR_SERVER_IP:8000/admin
```

Superuser bilan login qiling.

### 10.4: Gunicorn ni to'xtatish

Terminal oynasida: **Ctrl + C**

---

## 11-Mashq: Muammolarni hal qilish

### Agar ulanish xatosi bo'lsa:

```bash
# Database ulanishini tekshirish
python manage.py check --database default

# Loglarni ko'rish
tail -f /var/log/postgresql/postgresql-14-main.log
```

### Agar static fayllar yuklanmasa:

```bash
# Static fayllar yo'lini tekshirish
python manage.py findstatic admin/css/base.css

# Yana collectstatic qilish
python manage.py collectstatic --clear --no-input
```

### Agar permission xatosi bo'lsa:

```bash
# Fayllar ega va ruxsatlarini o'zgartirish
chown -R www-data:www-data /home/newssite
chmod -R 755 /home/newssite
```

---

## Qo'shimcha topshiriqlar

### Bonus 1: Loglarni sozlash

`config/settings.py` ga qo'shing:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/newssite/logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

Logs papkasini yarating:

```bash
mkdir -p /home/newssite/logs
touch /home/newssite/logs/django.log
chmod 666 /home/newssite/logs/django.log
```

### Bonus 2: Server vaqt zonasini o'rnatish

```bash
# Tashkent vaqt zonasini o'rnatish
timedatectl set-timezone Asia/Tashkent

# Tekshirish
timedatectl
```

### Bonus 3: Firewall sozlash

```bash
# UFW firewall o'rnatish
apt install ufw -y

# Asosiy portlarni ochish
ufw allow 22    # SSH
ufw allow 80    # HTTP
ufw allow 443   # HTTPS
ufw allow 8000  # Gunicorn (test uchun)

# Firewall ni yoqish
ufw enable

# Statusni ko'rish
ufw status
```

---

## Yakuniy tekshiruv ro'yxati

Quyidagilarni bajarganingizni belgilang:

- [ ] requirements.txt yaratildi
- [ ] .env fayli sozlandi (local va server)
- [ ] settings.py production uchun tayyor
- [ ] .gitignore to'g'ri sozlandi
- [ ] Loyiha GitHub'ga yuklandi
- [ ] Serverga SSH orqali ulana oldim
- [ ] Server yangilandi va zarur paketlar o'rnatildi
- [ ] PostgreSQL o'rnatildi va sozlandi
- [ ] Ma'lumotlar bazasi va foydalanuvchi yaratildi
- [ ] Virtual muhit yaratildi
- [ ] Loyiha serverga clone qilindi
- [ ] requirements.txt dan paketlar o'rnatildi
- [ ] .env fayli serverda yaratildi
- [ ] Migratsiyalar muvaffaqiyatli bajarildi
- [ ] Superuser yaratildi
- [ ] Static fayllar yig'ildi
- [ ] Gunicorn orqali sayt ochildi
- [ ] Admin panel ishlaydi

---

## Kelajakdagi qadamlar (53-darsda)

Keyingi darsda biz:

1. **Gunicorn'ni systemd service sifatida sozlaymiz** - avtomatik ishga tushishi uchun
2. **Nginx'ni o'rnatamiz va sozlaymiz** - reverse proxy sifatida
3. **SSL sertifikatini o'rnatamiz** - HTTPS uchun
4. **Domain'ni serverga ulaymiz** - IP o'rniga domen nomi
5. **Monitoring va logging sozlaymiz** - xatolarni kuzatish uchun

---

## Foydali buyruqlar

### Server boshqaruvi

```bash
# Serverni qayta ishga tushirish
reboot

# Server diskini tekshirish
df -h

# RAM holatini ko'rish
free -h

# Jarayonlarni ko'rish
htop  # yoki
top
```

### PostgreSQL boshqaruvi

```bash
# PostgreSQL ni qayta ishga tushirish
systemctl restart postgresql

# Statusni tekshirish
systemctl status postgresql

# Ma'lumotlar bazasiga ulanish
psql -U newsuser -d newsdb
```

### Virtual muhit

```bash
# Faollashtirish
source /home/newssite/venv/bin/activate

# Deaktivatsiya qilish
deactivate

# Virtual muhitdagi paketlarni ko'rish
pip list
```

### Git bilan ishlash

```bash
# O'zgarishlarni tortib olish
git pull origin main

# Statusni ko'rish
git status

# Loglarni ko'rish
git log --oneline
```

---

## Xulosa

Tabriklayman! Siz:

✅ Django loyihasini deployment uchun to'liq tayyorladingiz
✅ Ahost serveriga ulandingiz va sozladingiz
✅ PostgreSQL ma'lumotlar bazasini sozladingiz
✅ Loyihani serverga joylashtirdingiz
✅ Gunicorn orqali saytni ishga tushirdingiz

Keyingi darsda biz saytni to'liq production rejimiga o'tkazamiz va domain bilan ulaymiz!

## Maslahatlar

1. **Parollaringizni xavfsiz saqlang** - Password manager ishlatish tavsiya etiladi
2. **Backup oling** - har hafta ma'lumotlar bazasi va media fayllardan
3. **Loglarni tekshiring** - har kuni kam-kamida bir marta
4. **Yangilanmalarni o'rnating** - haftada bir marta `apt update && apt upgrade`
5. **Monitoring o'rnating** - server resurslarini kuzatish uchun
