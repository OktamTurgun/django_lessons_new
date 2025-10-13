# Dars 52: Deployment - Ahost serveriga joylash (1-qism)

## Kirish

Siz Django loyihangizni yaratdingiz, barcha funksiyalarni qo'shdingiz va local serverda test qildingiz. Endi vaqti keldi uni real serverga joylash va butun dunyoga ko'rsatish. Bu jarayon **Deployment** deb ataladi.

Bu darsda biz Django loyihasini **Ahost** serveriga qanday joylashtirish kerakligini o'rganamiz. Bu jarayon bir necha bosqichlardan iborat bo'lgani uchun, biz uni 2 qismga bo'lamiz.

## Deployment nima?

**Deployment** - bu dasturni ishlab chiqish muhitidan (development) ishlab chiqarish muhitiga (production) o'tkazish jarayoni. Ya'ni, siz o'z kompyuteringizda ishlab chiqqan loyihani real serverga joylashtirish va uni internetda ishlashiga erishish.

### Development vs Production

**Development (Ishlab chiqish muhiti):**
- `DEBUG = True`
- SQLite ma'lumotlar bazasi
- Django'ning o'z serveri (`runserver`)
- Xavfsizlik unchalik muhim emas
- Xatolarni ko'rish oson

**Production (Ishlab chiqarish muhiti):**
- `DEBUG = False`
- PostgreSQL/MySQL kabi kuchli ma'lumotlar bazasi
- Gunicorn/uWSGI + Nginx
- Xavfsizlik juda muhim
- Xatolar yashirin bo'lishi kerak

## Nima uchun Ahost?

**Ahost** - O'zbekistondagi mashhur hosting provayderlaridan biri. Afzalliklari:

- O'zbek loyihalar uchun qulay
- Yetarlicha arzon narxlar
- So'm valyutasida to'lov
- O'zbekcha qo'llab-quvvatlash
- Django va Python ni qo'llab-quvvatlaydi
- SSH dostup mavjud

## Tayyorgarlik bosqichlari

### 1-bosqich: Loyihani GitHub'ga yuklash

Agar hali qilmagan bo'lsangiz, loyihangizni GitHub'ga yuklang (30-darsda ko'rgandek):

```bash
# Git boshlash (agar hali qilmagan bo'lsangiz)
git init
git add .
git commit -m "Deployment uchun tayyor"

# GitHub'ga yuklash
git remote add origin https://github.com/username/repository-name.git
git branch -M main
git push -u origin main
```

### 2-bosqich: requirements.txt faylini yaratish

Loyihangiz uchun zarur bo'lgan barcha kutubxonalarni sanab o'tuvchi fayl yarating:

```bash
# Agar Pipenv ishlatayotgan bo'lsangiz
pipenv lock -r > requirements.txt

# Agar oddiy pip ishlatayotgan bo'lsangiz
pip freeze > requirements.txt
```

Bu fayl quyidagicha ko'rinishda bo'ladi:

```text
Django==5.1
psycopg2-binary==2.9.9
gunicorn==21.2.0
python-decouple==3.8
Pillow==10.2.0
django-crispy-forms==2.1
crispy-bootstrap4==2.0
```

**Muhim:** `requirements.txt` faylini loyiha ildiz papkasiga saqlang.

### 3-bosqich: .env faylini yaratish

Xavfsizlik uchun muhim ma'lumotlarni (SECRET_KEY, ma'lumotlar bazasi paroli va h.k.) `.env` faylida saqlash kerak.

#### python-decouple ni o'rnatish

```bash
pipenv install python-decouple
```

#### .env faylini yaratish

Loyiha ildiz papkasida `.env` faylini yarating:

```bash
# .env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.uz,www.yourdomain.uz
DATABASE_URL=postgresql://user:password@localhost/dbname
```

#### settings.py ni o'zgartirish

```python
# config/settings.py
from decouple import config, Csv

# SECRET_KEY ni .env dan olish
SECRET_KEY = config('SECRET_KEY')

# DEBUG
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Database configuration
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
```

### 4-bosqich: STATIC va MEDIA sozlamalari

Production muhitida static va media fayllarni to'g'ri sozlash juda muhim.

```python
# config/settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 5-bosqich: Gunicorn o'rnatish

Gunicorn - bu Python WSGI HTTP serveri, production uchun juda mos keladi.

```bash
pipenv install gunicorn
```

## Settings.py ni production uchun sozlash

### SECURITY sozlamalari

```python
# config/settings.py

# Production uchun xavfsizlik sozlamalari
if not DEBUG:
    # HTTPS sozlamalari
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS sozlamalari
    SECURE_HSTS_SECONDS = 31536000  # 1 yil
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Boshqa xavfsizlik sozlamalari
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
```

### ALLOWED_HOSTS sozlash

```python
# config/settings.py

# Development uchun
if DEBUG:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# Production uchun
else:
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
```

### Database sozlamalari (PostgreSQL)

```python
# config/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='newsdb'),
        'USER': config('DB_USER', default='newsuser'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

## .gitignore faylini to'ldirish

Muhim fayllarni GitHub'ga yuklamaslik uchun `.gitignore` faylini to'ldiring:

```gitignore
# .gitignore

# Python
*.pyc
__pycache__/
*.py[cod]
*$py.class

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

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Migrations (ixtiyoriy)
# */migrations/*.py
# !*/migrations/__init__.py
```

## Loyihani tekshirish

Deployment qilishdan oldin loyihani tekshirish:

```bash
# Django'ning deployment checklist
python manage.py check --deploy

# Static fayllarni yig'ish
python manage.py collectstatic

# Migrations tekshirish
python manage.py makemigrations --check --dry-run
```

## Ahost haqida ma'lumot

### Ahost tariflar

Ahost turli xil tariflarni taklif qiladi:

1. **Shared hosting** - oddiy saytlar uchun
2. **VPS hosting** - o'rta darajadagi loyihalar uchun
3. **Dedicated server** - katta loyihalar uchun

Django loyihalar uchun kamida **VPS hosting** tavsiya etiladi.

### Minimal server talablar

Django loyiha uchun minimal server talablar:

- **RAM:** Kamida 1GB (tavsiya: 2GB+)
- **CPU:** 1 core (tavsiya: 2+ cores)
- **Disk:** 20GB (loyiha hajmiga qarab)
- **OS:** Ubuntu 20.04/22.04 yoki CentOS
- **Python:** 3.8+
- **PostgreSQL:** 12+

## Ahost'da akkaunt yaratish

### 1. Ahost.uz saytiga kirish

1. Brauzeringizda `https://ahost.uz` saytiga kiring
2. "Ro'yxatdan o'tish" tugmasini bosing
3. Zarur ma'lumotlarni to'ldiring:
   - Ism va familiya
   - Email
   - Telefon raqam
   - Parol

### 2. Tarif tanlash

1. Kabinetga kirganingizdan keyin "VPS" bo'limiga o'ting
2. O'zingizga mos tarifni tanlang
3. Operatsion tizimni tanlang (Ubuntu 22.04 tavsiya etiladi)
4. To'lovni amalga oshiring

### 3. Server ma'lumotlarini olish

Server yaratilganidan keyin sizga quyidagi ma'lumotlar keladi:

```
IP Address: 123.456.789.012
Username: root
Password: your_temp_password
SSH Port: 22
```

**Muhim:** Bu ma'lumotlarni xavfsiz joyda saqlang!

## SSH orqali serverga ulanish

### Windows uchun

Windows 10/11 da SSH o'rnatilgan. PowerShell yoki CMD da:

```bash
ssh root@123.456.789.012
```

Agar SSH yo'q bo'lsa, **PuTTY** dasturini o'rnating.

### Mac/Linux uchun

Terminal da:

```bash
ssh root@123.456.789.012
```

### Birinchi ulanish

Birinchi marta ulanganingizda:

1. Parolni kiriting (ko'rinmaydi, bu normal)
2. "Yes" deb fingerprint ni tasdiqlang
3. Serverga muvaffaqiyatli ulandingiz!

```bash
root@server:~#
```

## Serverni yangilash

Serverga ulanganingizdan keyin, birinchi ish - tizimni yangilash:

```bash
# Sistema paketlarini yangilash
apt update
apt upgrade -y

# Zarur paketlarni o'rnatish
apt install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
```

Bu jarayon 5-10 daqiqa davom etishi mumkin.

## PostgreSQL ni sozlash

### 1. PostgreSQL xizmatini ishga tushirish

```bash
# PostgreSQL ni ishga tushirish
systemctl start postgresql
systemctl enable postgresql

# Statusni tekshirish
systemctl status postgresql
```

### 2. Ma'lumotlar bazasi va foydalanuvchi yaratish

```bash
# PostgreSQL ga kirish
sudo -u postgres psql

# Ichkarida quyidagi buyruqlarni bajaring:
```

```sql
-- Ma'lumotlar bazasi yaratish
CREATE DATABASE newsdb;

-- Foydalanuvchi yaratish
CREATE USER newsuser WITH PASSWORD 'quvvatli_parol_123';

-- Foydalanuvchiga ruxsat berish
ALTER ROLE newsuser SET client_encoding TO 'utf8';
ALTER ROLE newsuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE newsuser SET timezone TO 'Asia/Tashkent';

-- Ma'lumotlar bazasiga to'liq ruxsat berish
GRANT ALL PRIVILEGES ON DATABASE newsdb TO newsuser;

-- Chiqish
\q
```

### 3. PostgreSQL ni tashqaridan ulanishga ruxsat berish (agar kerak bo'lsa)

```bash
# postgresql.conf faylini tahrirlash
nano /etc/postgresql/14/main/postgresql.conf

# Quyidagi qatorni toping va o'zgartiring:
# listen_addresses = 'localhost' ni
listen_addresses = '*'

# pg_hba.conf faylini tahrirlash
nano /etc/postgresql/14/main/pg_hba.conf

# Eng oxiriga qo'shing:
host    all             all             0.0.0.0/0               md5

# PostgreSQL ni qayta ishga tushirish
systemctl restart postgresql
```

## Python muhitini sozlash

### 1. Python 3 va pip ni tekshirish

```bash
# Python versiyasini tekshirish
python3 --version

# pip versiyasini tekshirish
pip3 --version
```

### 2. virtualenv o'rnatish

```bash
# virtualenv o'rnatish
pip3 install virtualenv

# yoki
apt install python3-venv
```

## Loyiha papkasini yaratish

```bash
# Home papkasiga o'tish
cd /home

# Loyiha uchun papka yaratish
mkdir myproject
cd myproject

# Virtual muhit yaratish
python3 -m venv venv

# Virtual muhitni faollashtirish
source venv/bin/activate
```

Virtual muhit faollashganda prompt quyidagicha ko'rinadi:

```bash
(venv) root@server:/home/myproject#
```

## Loyihani serverga yuklash

### 1-usul: Git orqali (tavsiya etiladi)

```bash
# Git o'rnatish (agar o'rnatilmagan bo'lsa)
apt install git -y

# GitHub'dan loyihani clone qilish
cd /home/myproject
git clone https://github.com/username/repository-name.git .

# Nuqta (.) - joriy papkaga clone qilish uchun
```

### 2-usul: FTP/SFTP orqali

FileZilla yoki boshqa FTP client orqali fayllarni yuklashingiz mumkin:

- **Host:** 123.456.789.012
- **Username:** root
- **Password:** your_password
- **Port:** 22
- **Protocol:** SFTP

## Requirements.txt dan paketlarni o'rnatish

```bash
# Virtual muhitda bo'lganingizga ishonch hosil qiling
source venv/bin/activate

# Paketlarni o'rnatish
pip install -r requirements.txt

# Gunicorn o'rnatish (agar requirements.txt da bo'lmasa)
pip install gunicorn psycopg2-binary
```

## .env faylini serverda sozlash

```bash
# .env faylini yaratish
cd /home/myproject
nano .env
```

Quyidagilarni yozing:

```bash
SECRET_KEY=yangi-quvvatli-secret-key-yarating
DEBUG=False
ALLOWED_HOSTS=123.456.789.012,yourdomain.uz,www.yourdomain.uz

# Database
DB_NAME=newsdb
DB_USER=newsuser
DB_PASSWORD=quvvatli_parol_123
DB_HOST=localhost
DB_PORT=5432
```

**Ctrl + X**, keyin **Y**, keyin **Enter** bosib saqlang.

## Database migratsiyalarini bajarish

```bash
# Migrations yaratish
python manage.py makemigrations

# Migratsiyalarni bajarish
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Static fayllarni yig'ish
python manage.py collectstatic --no-input
```

## Gunicorn ni test qilish

```bash
# Gunicorn ni test rejimida ishga tushirish
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```

Agar hamma narsa to'g'ri bo'lsa, quyidagi xabarni ko'rasiz:

```
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:8000
[INFO] Using worker: sync
[INFO] Booting worker with pid: 12345
```

Brauzerda `http://123.456.789.012:8000` manziliga kiring va saytingiz ishlayotganini tekshiring.

**Ctrl + C** bosib to'xtating.

## Xulosa

Bu darsda biz quyidagilarni o'rgandik:

1. **Deployment** nima va nima uchun kerak
2. **Development** va **Production** muhitlari orasidagi farqlar
3. Loyihani deployment uchun tayyorlash:
   - requirements.txt yaratish
   - .env fayli va xavfsizlik sozlamalari
   - Static va media fayllar sozlamalari
4. **Ahost** haqida ma'lumot va akkaunt yaratish
5. Serverga SSH orqali ulanish
6. Serverni sozlash:
   - Sistema yangilanmalari
   - PostgreSQL o'rnatish va sozlash
   - Python muhitini tayyorlash
7. Loyihani serverga yuklash
8. Django loyihasini sozlash va migratsiyalar
9. Gunicorn bilan test qilish

## Keyingi darsda

Keyingi (53-dars)da biz:

- Gunicorn'ni systemd service sifatida sozlaymiz
- Nginx'ni o'rnatamiz va sozlaymiz
- SSL sertifikatini o'rnatamiz (HTTPS)
- Domain ni serverga ulash
- Monitoring va logging sozlash

## Maslahatlar

1. **Parollaringizni himoyalang** - hech qachon GitHub'ga yuklmang
2. **Backup oling** - muntazam ravishda ma'lumotlar bazasi va media fayllardan backup oling
3. **Loglarni kuzating** - xatolarni tezroq topish uchun
4. **Server xavfsizligi** - firewall, SSH kalit autentifikatsiyasi va boshqalarni sozlang
5. **Ma'lumotlar bazasi backup** - har kuni avtomatik backup sozlang
6. **Monitoring** - server resurslarini kuzatib boring
7. **Documentation** - barcha sozlamalaringizni hujjatlang

## Foydali havolalar

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Ahost.uz](https://ahost.uz)

## Qo'shimcha eslatmalar

### DEBUG = False bo'lganda nimalar o'zgaradi?

- Xatolar batafsil ko'rsatilmaydi
- Static fayllar Django orqali serve qilinmaydi
- ALLOWED_HOSTS majburiy bo'ladi
- Xavfsizlik tekshiruvlari qattiqroq bo'ladi

### SECRET_KEY'ni qanday yaratish mumkin?

```python
# Python console da
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Ma'lumotlar bazasi ulanishini qanday tekshirish?

```bash
# Server terminalida
python manage.py dbshell

# Yoki
python manage.py check --database default
```

Muvaffaqiyatli deployment!