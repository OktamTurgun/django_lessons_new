# Lesson 55: Deployment Practice - Amaliy mashqlar

## Kirish

Ushbu amaliy mashg'ulotda siz o'zingizning Django loyihangizni to'liq ishga tushirish uchun barcha qadamlarni bosqichma-bosqich amalga oshirasiz. Bu mashq sizga real production muhitda loyihangizni deploy qilish tajribasini beradi.

---

## Mashq 1: PostgreSQL ma'lumotlar bazasini sozlash

### Bosqich 1: SSH orqali serverga ulaning

```bash
ssh username@your_server_ip
```

### Bosqich 2: PostgreSQL ga kiring va database yarating

```bash
sudo -u postgres psql
```

### Bosqich 3: Quyidagi SQL buyruqlarini bajaring

```sql
-- 1. Database yaratish
CREATE DATABASE my_news_site;

-- 2. Foydalanuvchi yaratish
CREATE USER newsadmin WITH PASSWORD 'SecurePass2024!';

-- 3. Encoding va timezone sozlash
ALTER ROLE newsadmin SET client_encoding TO 'utf8';
ALTER ROLE newsadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE newsadmin SET timezone TO 'Asia/Tashkent';

-- 4. Ruxsatlar berish
GRANT ALL PRIVILEGES ON DATABASE my_news_site TO newsadmin;

-- 5. Chiqish
\q
```

### Bosqich 4: settings.py ni yangilang

```bash
cd ~/myproject
nano config/settings.py
```

**Database sozlamasini qo'shing:**

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'my_news_site',
        'USER': 'newsadmin',
        'PASSWORD': 'SecurePass2024!',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Bosqich 5: Migratsiyalarni bajaring

```bash
source venv/bin/activate
python manage.py migrate
```

**✅ Natija:** Barcha jadvallar muvaffaqiyatli yaratilishi kerak.

### Bosqich 6: Superuser yarating

```bash
python manage.py createsuperuser
```

**Tekshirish:**
- Username: `admin`
- Email: `admin@mynewssite.uz`
- Password: kuchli parol kiriting

---

## Mashq 2: Statik va media fayllarni to'plash

### Bosqich 1: settings.py da statik sozlamalarni tekshiring

```python
# settings.py

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Statik fayllar
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media fayllar
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Bosqich 2: Statik fayllarni to'plang

```bash
cd ~/myproject
source venv/bin/activate
python manage.py collectstatic --noinput
```

**✅ Kutilayotgan natija:**

```
120 static files copied to '/home/username/myproject/staticfiles'.
```

### Bosqich 3: Media papkasini yaratish va ruxsatlar berish

```bash
mkdir -p ~/myproject/media
chmod 755 ~/myproject/media
```

### Bosqich 4: Fayllar strukturasini tekshirish

```bash
tree -L 2 ~/myproject
```

**Ko'rinishi:**

```
myproject/
├── config/
├── news/
├── static/
├── staticfiles/    ← Yangi
├── media/          ← Yangi
├── venv/
├── manage.py
└── requirements.txt
```

---

## Mashq 3: Gunicorn sozlash va systemd service yaratish

### Bosqich 1: Gunicorn o'rnatish

```bash
source ~/myproject/venv/bin/activate
pip install gunicorn
pip freeze > requirements.txt
```

### Bosqich 2: Gunicorn ni test qilish

```bash
cd ~/myproject
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```

**Brauzerda test qiling:** `http://your_server_ip:8000`

**✅ Natija:** Sayt ochilishi kerak (lekin statik faylsiz)

`Ctrl + C` bilan to'xtating.

### Bosqich 3: Gunicorn socket yaratish

```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

**Kodni kiriting:**

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### Bosqich 4: Gunicorn service yaratish

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

**Kodni kiriting (username va papka nomlarini almashtiring!):**

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/myproject
ExecStart=/home/ubuntu/myproject/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Bosqich 5: Xizmatlarni ishga tushirish

```bash
# Daemon reload
sudo systemctl daemon-reload

# Socket ishga tushirish
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

# Statusni tekshirish
sudo systemctl status gunicorn.socket
```

**✅ Kutilayotgan natija:**

```
● gunicorn.socket - gunicorn socket
   Loaded: loaded
   Active: active (listening)
```

### Bosqich 6: Socket faylni tekshirish

```bash
file /run/gunicorn.sock
```

**Natija:**

```
/run/gunicorn.sock: socket
```

### Bosqich 7: Gunicorn serviceni ishga tushirish

```bash
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

**Agar xatolik bo'lsa:**

```bash
sudo journalctl -u gunicorn --no-pager
```

---

## Mashq 4: Nginx sozlash

### Bosqich 1: Nginx konfiguratsiya fayl yaratish

```bash
sudo nano /etc/nginx/sites-available/mynewssite
```

**Konfiguratsiya (domen va papka nomlarini almashtiring!):**

```nginx
server {
    listen 80;
    server_name mynewssite.uz www.mynewssite.uz;

    client_max_body_size 20M;

    location = /favicon.ico { 
        access_log off; 
        log_not_found off; 
    }
    
    location /static/ {
        alias /home/ubuntu/myproject/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/ubuntu/myproject/media/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

### Bosqich 2: Konfiguratsiyani faollashtirish

```bash
sudo ln -s /etc/nginx/sites-available/mynewssite /etc/nginx/sites-enabled/
```

### Bosqich 3: Nginx sintaksisni tekshirish

```bash
sudo nginx -t
```

**✅ Kutilayotgan natija:**

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### Bosqich 4: Default saytni o'chirish (agar kerak bo'lsa)

```bash
sudo rm /etc/nginx/sites-enabled/default
```

### Bosqich 5: Nginx ni qayta ishga tushirish

```bash
sudo systemctl restart nginx
```

### Bosqich 6: Firewall sozlash

```bash
sudo ufw allow 'Nginx Full'
sudo ufw status
```

### Bosqich 7: Test qilish

**Brauzerda ochish:** `http://mynewssite.uz` yoki `http://your_server_ip`

**✅ Natija:** Sayt to'liq statik fayllar bilan ochilishi kerak!

---

## Mashq 5: SSL sertifikat (HTTPS) o'rnatish

### Bosqich 1: Certbot o'rnatish

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```

### Bosqich 2: SSL sertifikat olish

```bash
sudo certbot --nginx -d mynewssite.uz -d www.mynewssite.uz
```

**Jarayonda:**
1. Email manzilingizni kiriting
2. Shartlarga rozi bo'ling (`A`)
3. HTTP dan HTTPS ga redirect uchun `2` ni tanlang

**✅ Kutilayotgan natija:**

```
Congratulations! You have successfully enabled HTTPS on https://mynewssite.uz
```

### Bosqich 3: HTTPS ni test qilish

**Brauzerda ochish:** `https://mynewssite.uz`

**Tekshirish:**
- Manzil qatorida qulf belgisi ko'rinishi kerak
- Sertifikat ma'lumotlarini ko'rish uchun qulfga bosing

### Bosqich 4: SSL avtomatik yangilanishini test qilish

```bash
sudo certbot renew --dry-run
```

**✅ Natija:**

```
Congratulations, all simulated renewals succeeded
```

---

## Mashq 6: Django production sozlamalarini qo'llash

### Bosqich 1: settings.py ni tahrirlash

```bash
nano ~/myproject/config/settings.py
```

**Quyidagi o'zgarishlarni kiriting:**

```python
# DEBUG ni o'chirish
DEBUG = False

# ALLOWED_HOSTS
ALLOWED_HOSTS = ['mynewssite.uz', 'www.mynewssite.uz', 'your_server_ip']

# HTTPS sozlamalari
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging (ixtiyoriy)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/home/ubuntu/myproject/logs/django.log',
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

### Bosqich 2: Logs papkasini yaratish

```bash
mkdir -p ~/myproject/logs
chmod 755 ~/myproject/logs
```

### Bosqich 3: Xizmatlarni qayta ishga tushirish

```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Bosqich 4: Test qilish

**Brauzerda ochish:** `https://mynewssite.uz`

**Tekshirish:**
- HTTP `http://mynewssite.uz` avtomatik HTTPS ga yo'naltirilishi kerak
- Barcha sahifalar va statik fayllar ishlashi kerak
- Admin panel: `https://mynewssite.uz/admin/`

---

## Mashq 7: .env fayl orqali maxfiy ma'lumotlarni saqlash

### Bosqich 1: python-dotenv o'rnatish

```bash
source ~/myproject/venv/bin/activate
pip install python-dotenv
pip freeze > requirements.txt
```

### Bosqich 2: .env fayl yaratish

```bash
nano ~/myproject/.env
```

**Kodni kiriting:**

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=False
ALLOWED_HOSTS=mynewssite.uz,www.mynewssite.uz,your_server_ip

DB_NAME=my_news_site
DB_USER=newsadmin
DB_PASSWORD=SecurePass2024!
DB_HOST=localhost
DB_PORT=5432
```

### Bosqich 3: settings.py ni yangilash

```python
# settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY')

# DEBUG
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

### Bosqich 4: .env faylni .gitignore ga qo'shish

```bash
nano ~/myproject/.gitignore
```

**Qo'shing:**

```
.env
*.pyc
__pycache__/
db.sqlite3
/staticfiles/
/media/
/logs/
```

### Bosqich 5: Test qilish

```bash
python manage.py check
sudo systemctl restart gunicorn
```

---

## Mashq 8: Loyihani yangilash jarayonini amalda qo'llash

### Bosqich 1: Local kompyuterda o'zgarish qilish

Masalan, `news/models.py` da yangi field qo'shing:

```python
# news/models.py

class News(models.Model):
    # ... mavjud fieldlar
    views_count = models.IntegerField(default=0, verbose_name="Ko'rishlar soni")
    is_featured = models.BooleanField(default=False, verbose_name="Asosiy yangilik")
```

### Bosqich 2: Migratsiya yaratish va test qilish

```bash
# Local kompyuterda
python manage.py makemigrations
python manage.py migrate
python manage.py runserver  # Test qilish
```

### Bosqich 3: GitHub ga yuklash

```bash
git add .
git commit -m "Yangi fieldlar qo'shildi: views_count va is_featured"
git push origin main
```

### Bosqich 4: Serverda yangilash

```bash
# Serverga SSH orqali ulaning
ssh ubuntu@your_server_ip

# Loyiha papkasiga o'ting
cd ~/myproject

# Virtual muhitni aktivlashtiring
source venv/bin/activate

# O'zgarishlarni tortib olish
git pull origin main

# Yangi paketlar o'rnatish (agar bor bo'lsa)
pip install -r requirements.txt

# Migratsiyalarni bajarish
python manage.py migrate

# Statik fayllar o'zgarganda
python manage.py collectstatic --noinput

# Gunicorn ni qayta ishga tushirish
sudo systemctl restart gunicorn

# Nginx ni qayta ishga tushirish (kerak bo'lsa)
sudo systemctl restart nginx
```

### Bosqich 5: Tekshirish

```bash
# Xizmatlar statusini tekshirish
sudo systemctl status gunicorn
sudo systemctl status nginx

# Loglarni ko'rish
sudo journalctl -u gunicorn -n 50
```

**Brauzerda test qiling:** `https://mynewssite.uz`

---

## Mashq 9: Database backup yaratish

### Bosqich 1: Backup papkasini yaratish

```bash
mkdir -p ~/backups
chmod 700 ~/backups
```

### Bosqich 2: Manual backup yaratish

```bash
pg_dump -U newsadmin -h localhost my_news_site > ~/backups/my_news_site_$(date +%Y%m%d_%H%M%S).sql
```

### Bosqich 3: Backup faylni tekshirish

```bash
ls -lh ~/backups/
```

### Bosqich 4: Backup script yaratish

```bash
nano ~/backup_db.sh
```

**Kodni kiriting:**

```bash
#!/bin/bash

# O'zgaruvchilar
DB_NAME="my_news_site"
DB_USER="newsadmin"
BACKUP_DIR="/home/ubuntu/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_${DATE}.sql"

# Backup yaratish
pg_dump -U $DB_USER -h localhost $DB_NAME > $BACKUP_FILE

# 7 kundan eski backuplarni o'chirish
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete

echo "Backup yaratildi: $BACKUP_FILE"
```

### Bosqich 5: Scriptga ruxsat berish

```bash
chmod +x ~/backup_db.sh
```

### Bosqich 6: Script ni test qilish

```bash
~/backup_db.sh
```

### Bosqich 7: Cron job orqali avtomatlashtirish

```bash
crontab -e
```

**Qo'shing (har kuni soat 2 da):**

```
0 2 * * * /home/ubuntu/backup_db.sh >> /home/ubuntu/backups/backup.log 2>&1
```

### Bosqich 8: Backup restore qilish (agar kerak bo'lsa)

```bash
# Database ni restore qilish
psql -U newsadmin -h localhost -d my_news_site < ~/backups/my_news_site_20240115_020000.sql
```

---

## Mashq 10: Monitoring va troubleshooting

### Bosqich 1: Xizmatlar statusini tekshirish

```bash
# Gunicorn
sudo systemctl status gunicorn

# Nginx
sudo systemctl status nginx

# PostgreSQL
sudo systemctl status postgresql
```

### Bosqich 2: Loglarni real-time ko'rish

**Terminal 1 - Gunicorn loglari:**

```bash
sudo journalctl -u gunicorn -f
```

**Terminal 2 - Nginx error loglari:**

```bash
sudo tail -f /var/log/nginx/error.log
```

**Terminal 3 - Nginx access loglari:**

```bash
sudo tail -f /var/log/nginx/access.log
```

### Bosqich 3: Server resurslarini monitoring

```bash
# CPU va RAM
htop

# Disk space
df -h

# Running processlar
ps aux | grep gunicorn
ps aux | grep nginx
```

### Bosqich 4: Test so'rov yuborish

```bash
# Sayt statusini tekshirish
curl -I https://mynewssite.uz

# API endpoint test qilish
curl https://mynewssite.uz/api/news/
```

### Bosqich 5: 502 Bad Gateway xatosini hal qilish

**Agar 502 xatosi paydo bo'lsa:**

```bash
# 1. Gunicorn ishlaganini tekshiring
sudo systemctl status gunicorn

# 2. Socket fayl mavjudligini tekshiring
file /run/gunicorn.sock
ls -l /run/gunicorn.sock

# 3. Gunicorn loglarini ko'ring
sudo journalctl -u gunicorn -n 100

# 4. Qayta ishga tushiring
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### Bosqich 6: Statik fayllar yuklanmasa

```bash
# 1. Statik fayllar to'plandimi?
ls -la ~/myproject/staticfiles/

# 2. Ruxsatlar to'g'rimi?
sudo chown -R ubuntu:www-data ~/myproject/staticfiles
sudo chmod -R 755 ~/myproject/staticfiles

# 3. Nginx konfiguratsiyasida yo'l to'g'rimi?
sudo nano /etc/nginx/sites-available/mynewssite

# 4. Qayta ishga tushiring
sudo systemctl restart nginx
```

---

## Qo'shimcha mashqlar

### Mashq A: Custom 404 va 500 sahifalar

**1. Template yaratish:**

```bash
mkdir -p ~/myproject/templates/errors
nano ~/myproject/templates/errors/404.html
```

```html
<!DOCTYPE html>
<html>
<head>
    <title>Sahifa topilmadi - 404</title>
</head>
<body>
    <h1>404 - Sahifa topilmadi</h1>
    <p>Kechirasiz, siz qidirayotgan sahifa mavjud emas.</p>
    <a href="/">Bosh sahifaga qaytish</a>
</body>
</html>
```

**2. settings.py da sozlash:**

```python
TEMPLATES = [
    {
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # ...
    },
]
```

**3. urls.py da handler qo'shish:**

```python
# config/urls.py

handler404 = 'news.views.custom_404'
handler500 = 'news.views.custom_500'
```

**4. Views yaratish:**

```python
# news/views.py

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    return render(request, 'errors/500.html', status=500)
```

### Mashq B: Redis cache sozlash

**1. Redis o'rnatish:**

```bash
sudo apt install redis-server -y
sudo systemctl start redis
sudo systemctl enable redis
```

**2. Python paketini o'rnatish:**

```bash
pip install django-redis
pip freeze > requirements.txt
```

**3. settings.py da sozlash:**

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session backendni cache ga o'zgartirish
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

**4. Qayta ishga tushirish:**

```bash
sudo systemctl restart gunicorn
```

---

## Yakuniy tekshiruv (Checklist)

Quyidagi barcha bandlar ✅ bo'lishi kerak:

### Server va xizmatlar
- [ ] SSH orqali serverga ulanish ishlayapti
- [ ] PostgreSQL database yaratildi va ishlayapti
- [ ] Gunicorn socket va service faol
- [ ] Nginx to'g'ri sozlangan va ishlayapti
- [ ] Firewall kerakli portlarni ochgan

### Django loyiha
- [ ] Virtual muhit yaratildi va faol
- [ ] requirements.txt dan barcha paketlar o'rnatildi
- [ ] Database migratsiyalari bajarildi
- [ ] Superuser yaratildi
- [ ] Statik fayllar to'plandi
- [ ] Media papkasi yaratildi

### Xavfsizlik
- [ ] DEBUG = False
- [ ] ALLOWED_HOSTS to'g'ri sozlangan
- [ ] SECRET_KEY .env faylda
- [ ] SSL sertifikat o'rnatildi (HTTPS)
- [ ] HTTPS redirect yoqildi
- [ ] HSTS sozlamalari qo'shildi

### Funksionallik
- [ ] Bosh sahifa ochiladi
- [ ] Admin panel ishlaydi
- [ ] Statik fayllar yuklanadi
- [ ] Media fayllar yuklanadi
- [ ] Formalar ishlaydi
- [ ] Database operatsiyalari ishlaydi

### Monitoring va backup
- [ ] Loglar to'g'ri yozilayapti
- [ ] Backup script yaratildi
- [ ] Cron job sozlandi

---

## Xulosa

Tabriklayman! Siz Django loyihangizni muvaffaqiyatli production serveriga joylashtirdingiz. Endi sizda:

✅ To'liq ishlaydigan web sayt
✅ HTTPS (SSL) bilan xavfsiz aloqa
✅ Professional darajadagi server sozlamalari
✅ Backup va monitoring tizimi
✅ Loyihani yangilash uchun tayyor jarayon

**Keyingi qadamlar:**
- Monitoring tizimlarini o'rnating (Sentry, New Relic)
- CDN sozlang (Cloudflare)
- CI/CD pipeline yarating (GitHub Actions)
- Load testing o'tkazing
- SEO optimizatsiya qiling

**Muvaffaqiyatlar! 🚀🎉**