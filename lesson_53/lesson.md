# Lesson 55: Deployment - Ahost serveriga joylash (2-qism)

## Kirish

Oldingi darsda biz loyihamizni Ahost serveriga joylashtirish uchun boshlang'ich sozlamalarni amalga oshirdik: server yaratdik, SSH orqali ulanish sozladik, kerakli dasturlarni o'rnatdik va loyihamizni serverga yukladik. Ushbu darsda esa loyihamizni to'liq ishga tushirish uchun qolgan muhim sozlamalarni bajaramiz: ma'lumotlar bazasini sozlash va migratsiya qilish, statik fayllarni to'plash, Gunicorn va Nginx sozlash, HTTPS (SSL sertifikat) o'rnatish va oxirida loyihamizni avtomatik qayta ishga tushirish mexanizmini o'rnatamiz.

## Maqsadlar

Ushbu darsda quyidagilarni o'rganamiz:

- PostgreSQL ma'lumotlar bazasini yaratish va sozlash
- Database migratsiyalarini serverda bajarish
- Statik va media fayllarni to'plash va sozlash
- Gunicorn (WSGI server) ni sozlash va systemd service yaratish
- Nginx konfiguratsiyasi va domen sozlash
- SSL sertifikat (Let's Encrypt) o'rnatish va HTTPS ni yoqish
- Loyihani yangilash va qayta ishga tushirish jarayoni

---

## 1. PostgreSQL ma'lumotlar bazasini sozlash

### 1.1. PostgreSQL ma'lumotlar bazasi va foydalanuvchi yaratish

SSH orqali serverga ulaning va PostgreSQL ga kiring:

```bash
# PostgreSQL ga kirish
sudo -u postgres psql
```

Ma'lumotlar bazasi va foydalanuvchi yaratish:

```sql
-- Database yaratish
CREATE DATABASE news_db;

-- Foydalanuvchi yaratish (parolni o'zgartiring!)
CREATE USER news_user WITH PASSWORD 'kuchli_parol_123!';

-- Foydalanuvchiga kerakli sozlamalarni berish
ALTER ROLE news_user SET client_encoding TO 'utf8';
ALTER ROLE news_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE news_user SET timezone TO 'UTC';

-- Database ustidan to'liq huquq berish
GRANT ALL PRIVILEGES ON DATABASE news_db TO news_user;

-- PostgreSQL dan chiqish
\q
```

**Tushuntirish:**
- `CREATE DATABASE news_db` - yangi ma'lumotlar bazasini yaratadi
- `CREATE USER` - ma'lumotlar bazasi foydalanuvchisini yaratadi va parol belgilaydi
- `ALTER ROLE` - foydalanuvchi uchun default sozlamalarni belgilaydi (encoding, transaction isolation, timezone)
- `GRANT ALL PRIVILEGES` - foydalanuvchiga ma'lumotlar bazasi ustidan barcha huquqlarni beradi

**Muhim:** `kuchli_parol_123!` ni o'zingizning xavfsiz parolingizga almashtiring!

### 1.2. Django settings.py da database sozlamasini yangilash

Serverda joylashgan loyihangizning `settings.py` faylini tahrirlang:

```bash
# Loyiha papkasiga o'ting
cd ~/myproject

# Virtual muhitni aktivlashtiring
source venv/bin/activate

# settings.py ni tahrirlash
nano config/settings.py
```

**Database sozlamasini quyidagicha o'zgartiring:**

```python
# settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'news_db',
        'USER': 'news_user',
        'PASSWORD': 'kuchli_parol_123!',  # Yuqorida yaratgan parol
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Tushuntirish:**
- `ENGINE` - PostgreSQL database engine'ini ko'rsatadi
- `NAME` - ma'lumotlar bazasi nomi
- `USER` - ma'lumotlar bazasi foydalanuvchisi
- `PASSWORD` - foydalanuvchi paroli
- `HOST` - database server manzili (localhost - bu serverning o'zi)
- `PORT` - PostgreSQL default porti

Faylni saqlang: `Ctrl + O`, `Enter`, `Ctrl + X`

---

## 2. Django migratsiyalarini bajarish

### 2.1. Migratsiyalarni amalga oshirish

```bash
# Loyiha papkasida bo'lganingizga ishonch hosil qiling
cd ~/myproject

# Virtual muhitni aktivlashtiring (agar hali faol bo'lmasa)
source venv/bin/activate

# Migratsiyalarni bajarish
python manage.py migrate
```

**Natija:**

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, news, sessions, users
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
```

**Tushuntirish:**
Bu buyruq barcha modellar uchun ma'lumotlar bazasida jadvallarni yaratadi.

### 2.2. Superuser yaratish

```bash
python manage.py createsuperuser
```

Kerakli ma'lumotlarni kiriting:

```
Username: admin
Email: admin@example.com
Password: ***
Password (again): ***
```

**Tushuntirish:**
Bu admin panelga kirish uchun foydalanuvchi yaratadi.

### 2.3. Test qilish

Django development serverini ishga tushirib ko'ring:

```bash
python manage.py runserver 0.0.0.0:8000
```

Brauzerda `http://server_ip:8000` ga kirib ko'ring. Agar sahifa ochilsa, database to'g'ri sozlangan!

**Muhim:** Test qilgandan keyin `Ctrl + C` bilan serverni to'xtating.

---

## 3. Statik va Media fayllarni sozlash

### 3.1. settings.py da statik va media sozlamalari

`settings.py` faylida quyidagi sozlamalarni tekshiring yoki qo'shing:

```python
# settings.py

import os

# Static fayllar sozlamalari
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Media fayllar sozlamalari
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**Tushuntirish:**
- `STATIC_URL` - statik fayllar uchun URL prefiksi
- `STATIC_ROOT` - `collectstatic` buyrug'i statik fayllarni bu yerga to'playdi
- `STATICFILES_DIRS` - Django qaysi papkalardan statik fayllarni qidiradi
- `MEDIA_URL` - foydalanuvchi yuklagan fayllar uchun URL prefiksi
- `MEDIA_ROOT` - foydalanuvchi yuklagan fayllar saqlanadigan papka

### 3.2. Statik fayllarni to'plash

```bash
# Statik fayllarni to'plash
python manage.py collectstatic
```

**Natija:**

```
You have requested to collect static files at the destination
location as specified in your settings:

    /home/username/myproject/staticfiles

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: yes

120 static files copied to '/home/username/myproject/staticfiles'.
```

**Tushuntirish:**
Bu buyruq barcha statik fayllarni (CSS, JS, images) bir joyga to'playdi. Nginx shu papkadan statik fayllarni serve qiladi.

### 3.3. Media papkasini yaratish

```bash
# Media papkasini yaratish
mkdir -p ~/myproject/media

# Ruxsatlarni sozlash
chmod 755 ~/myproject/media
```

**Tushuntirish:**
Bu papkaga foydalanuvchilar rasm va boshqa fayllarni yuklaydi.

---

## 4. Gunicorn sozlash va systemd service yaratish

### 4.1. Gunicorn o'rnatish

```bash
# Virtual muhit faol bo'lganiga ishonch hosil qiling
source ~/myproject/venv/bin/activate

# Gunicorn o'rnatish
pip install gunicorn
```

**Tushuntirish:**
Gunicorn - bu Python WSGI HTTP server. U Django applicationni production muhitida ishga tushiradi.

### 4.2. Gunicorn ni test qilish

```bash
cd ~/myproject

# Gunicorn orqali ishga tushirish
gunicorn --bind 0.0.0.0:8000 config.wsgi:application
```

Brauzerda `http://server_ip:8000` ga kirib ko'ring. Agar ishlasa, `Ctrl + C` bilan to'xtating.

**Tushuntirish:**
- `--bind 0.0.0.0:8000` - barcha IP manzillarda 8000 portni tinglaydi
- `config.wsgi:application` - Django WSGI application joylashuvi

### 4.3. Gunicorn socket fayl yaratish

```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Quyidagi kodni kiriting:

```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

**Tushuntirish:**
- `ListenStream` - socket fayl manzili
- Socket orqali Nginx va Gunicorn o'rtasida aloqa o'rnatiladi

Saqlang: `Ctrl + O`, `Enter`, `Ctrl + X`

### 4.4. Gunicorn service fayl yaratish

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Quyidagi kodni kiriting (**username va myproject nomlarini o'zgartirishni unutmang!**):

```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=username
Group=www-data
WorkingDirectory=/home/username/myproject
ExecStart=/home/username/myproject/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Tushuntirish:**
- `User=username` - Linux foydalanuvchi nomi (o'zgartiring!)
- `Group=www-data` - Nginx bilan birga ishlash uchun guruh
- `WorkingDirectory` - loyiha papkasi (o'zgartiring!)
- `ExecStart` - Gunicorn buyrug'i va parametrlari
- `--workers 3` - 3 ta worker process (CPU core soniga qarab)
- `--bind unix:/run/gunicorn.sock` - socket orqali ulanish

Saqlang: `Ctrl + O`, `Enter`, `Ctrl + X`

### 4.5. Gunicorn xizmatlarini ishga tushirish

```bash
# Systemd daemonni qayta yuklash
sudo systemctl daemon-reload

# Gunicorn socket va serviceni ishga tushirish
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

# Statusni tekshirish
sudo systemctl status gunicorn.socket
```

**Natija:**

```
● gunicorn.socket - gunicorn socket
     Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled)
     Active: active (listening)
```

**Socket faylni tekshirish:**

```bash
file /run/gunicorn.sock
```

**Natija:**

```
/run/gunicorn.sock: socket
```

### 4.6. Gunicorn serviceni ishga tushirish

```bash
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

**Natija:**

```
● gunicorn.service - gunicorn daemon
     Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled)
     Active: active (running)
```

**Agar xatolik bo'lsa:**

```bash
# Loglarni ko'rish
sudo journalctl -u gunicorn

# Xatolikni tuzatgandan keyin
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

---

## 5. Nginx sozlash

### 5.1. Nginx konfiguratsiya fayl yaratish

```bash
sudo nano /etc/nginx/sites-available/myproject
```

Quyidagi konfiguratsiyani kiriting (**domen va papka nomlarini o'zgartiring!**):

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/username/myproject/staticfiles/;
    }

    location /media/ {
        alias /home/username/myproject/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

**Tushuntirish:**
- `listen 80` - HTTP portda tinglash (keyinchalik HTTPS ga o'tamiz)
- `server_name` - domen nomingiz (o'zgartiring!)
- `location /static/` - statik fayllar uchun yo'l (papka nomini o'zgartiring!)
- `location /media/` - media fayllar uchun yo'l (papka nomini o'zgartiring!)
- `location /` - boshqa barcha so'rovlarni Gunicorn ga yo'naltirish
- `proxy_pass` - Gunicorn socket manzili

Saqlang: `Ctrl + O`, `Enter`, `Ctrl + X`

### 5.2. Konfiguratsiyani faollashtirish

```bash
# Symbolic link yaratish
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled/

# Nginx konfiguratsiyasini tekshirish
sudo nginx -t
```

**Natija:**

```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### 5.3. Nginx ni qayta ishga tushirish

```bash
sudo systemctl restart nginx
```

### 5.4. Firewall sozlash

```bash
# HTTP va HTTPS portlarni ochish
sudo ufw allow 'Nginx Full'

# Statusni tekshirish
sudo ufw status
```

**Natija:**

```
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
Nginx Full                 ALLOW       Anywhere
```

### 5.5. Test qilish

Brauzerda `http://yourdomain.com` ga kiring. Saytingiz ochilishi kerak!

**Agar sahifa ochilmasa:**

```bash
# Nginx loglarini ko'rish
sudo tail -f /var/log/nginx/error.log

# Gunicorn loglarini ko'rish
sudo journalctl -u gunicorn -f
```

---

## 6. HTTPS (SSL sertifikat) o'rnatish

### 6.1. Certbot o'rnatish

```bash
# Certbot o'rnatish
sudo apt install certbot python3-certbot-nginx -y
```

**Tushuntirish:**
Certbot - Let's Encrypt dan bepul SSL sertifikat olish va avtomatik yangilash uchun dastur.

### 6.2. SSL sertifikat olish

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

**Jarayon:**

```
Enter email address (used for urgent renewal and security notices): your@email.com

Please read the Terms of Service...
(A)gree/(C)ancel: A

Would you be willing to share your email address...
(Y)es/(N)o: N

Please choose whether or not to redirect HTTP traffic to HTTPS...
1: No redirect
2: Redirect
Select the appropriate number [1-2]: 2
```

**Tushuntirish:**
- Email manzilingizni kiriting (SSL muddati tugashidan oldin xabar keladi)
- Shartlarga rozi bo'ling
- HTTP dan HTTPS ga avtomatik yo'naltirish uchun `2` ni tanlang

### 6.3. SSL sertifikatni tekshirish

Brauzerda `https://yourdomain.com` ga kiring. Manzil qatorida qulf belgisi ko'rinishi kerak!

### 6.4. SSL avtomatik yangilanishini tekshirish

```bash
# Test qilish (aslida yangilamaydi, faqat simulyatsiya)
sudo certbot renew --dry-run
```

**Natija:**

```
Congratulations, all simulated renewals succeeded
```

**Tushuntirish:**
Certbot har 60 kunda avtomatik SSL sertifikatni yangilaydi. Bu buyruq jarayonning to'g'ri ishlashini tekshiradi.

---

## 7. Django production sozlamalari

### 7.1. settings.py da xavfsizlik sozlamalari

```bash
nano ~/myproject/config/settings.py
```

Quyidagi sozlamalarni qo'shing yoki o'zgartiring:

```python
# settings.py

# DEBUG ni o'chirish (MUHIM!)
DEBUG = False

# ALLOWED_HOSTS ni sozlash
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'server_ip']

# HTTPS sozlamalari
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 yil
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

**Tushuntirish:**
- `DEBUG = False` - production muhitda debug rejimi o'chiriladi
- `ALLOWED_HOSTS` - faqat ko'rsatilgan domenlar saytga kirishi mumkin
- `SECURE_SSL_REDIRECT` - HTTP so'rovlarni avtomatik HTTPS ga yo'naltiradi
- `SESSION_COOKIE_SECURE` va `CSRF_COOKIE_SECURE` - cookie'lar faqat HTTPS orqali yuboriladi
- `SECURE_HSTS_SECONDS` - brauzerga sayt faqat HTTPS orqali ochilishini bildiradi

Saqlang: `Ctrl + O`, `Enter`, `Ctrl + X`

### 7.2. O'zgarishlarni saqlash va Gunicorn ni qayta ishga tushirish

```bash
# Gunicorn ni qayta ishga tushirish
sudo systemctl restart gunicorn

# Nginx ni qayta ishga tushirish
sudo systemctl restart nginx
```

---

## 8. Loyihani yangilash jarayoni

Kelajakda loyihangizda o'zgarishlar qilganingizda quyidagi qadamlarni bajaring:

### 8.1. Local kompyuterda o'zgarishlarni GitHub ga yuklash

```bash
# Local kompyuterda
git add .
git commit -m "Yangi funksiyalar qo'shildi"
git push origin main
```

### 8.2. Serverda o'zgarishlarni tortib olish

```bash
# Serverga SSH orqali ulaning
ssh username@server_ip

# Loyiha papkasiga o'ting
cd ~/myproject

# Virtual muhitni aktivlashtiring
source venv/bin/activate

# O'zgarishlarni GitHub dan tortib olish
git pull origin main

# Yangi paketlar o'rnatilgan bo'lsa
pip install -r requirements.txt

# Yangi migratsiyalar bo'lsa
python manage.py migrate

# Statik fayllar o'zgarganda
python manage.py collectstatic --noinput

# Gunicorn ni qayta ishga tushirish
sudo systemctl restart gunicorn

# Nginx ni qayta ishga tushirish (agar kerak bo'lsa)
sudo systemctl restart nginx
```

**Tushuntirish:**
Bu qadamlar orqali loyihadagi barcha yangilanishlar serverda ham qo'llaniladi.

---

## 9. Foydali buyruqlar va troubleshooting

### 9.1. Xizmatlar statusini tekshirish

```bash
# Gunicorn statusi
sudo systemctl status gunicorn

# Nginx statusi
sudo systemctl status nginx

# PostgreSQL statusi
sudo systemctl status postgresql
```

### 9.2. Loglarni ko'rish

```bash
# Gunicorn loglari
sudo journalctl -u gunicorn -f

# Nginx access loglari
sudo tail -f /var/log/nginx/access.log

# Nginx error loglari
sudo tail -f /var/log/nginx/error.log

# Django loglari (agar sozlangan bo'lsa)
tail -f ~/myproject/logs/django.log
```

### 9.3. Xizmatlarni qayta ishga tushirish

```bash
# Gunicorn
sudo systemctl restart gunicorn

# Nginx
sudo systemctl restart nginx

# PostgreSQL
sudo systemctl restart postgresql
```

### 9.4. Keng tarqalgan muammolar va yechimlari

**Muammo 1:** 502 Bad Gateway xatosi

**Yechim:**

```bash
# Gunicorn ishlaganini tekshiring
sudo systemctl status gunicorn

# Socket fayl mavjudligini tekshiring
file /run/gunicorn.sock

# Agar ishlamasa, qayta ishga tushiring
sudo systemctl restart gunicorn
```

**Muammo 2:** Statik fayllar yuklanmayapti

**Yechim:**

```bash
# Statik fayllarni qayta to'plash
cd ~/myproject
source venv/bin/activate
python manage.py collectstatic --noinput

# Ruxsatlarni tekshirish
sudo chown -R username:www-data ~/myproject/staticfiles
sudo chmod -R 755 ~/myproject/staticfiles

# Nginx ni qayta ishga tushirish
sudo systemctl restart nginx
```

**Muammo 3:** Database ulanish xatosi

**Yechim:**

```bash
# PostgreSQL ishlaganini tekshiring
sudo systemctl status postgresql

# Database ulanishini test qilish
sudo -u postgres psql -d news_db -U news_user

# settings.py da database sozlamalarini tekshiring
nano ~/myproject/config/settings.py
```

**Muammo 4:** Permission denied xatosi

**Yechim:**

```bash
# Loyiha papkasiga ruxsatlar berish
sudo chown -R username:www-data ~/myproject
sudo chmod -R 755 ~/myproject

# Media papkaga ruxsatlar
sudo chown -R username:www-data ~/myproject/media
sudo chmod -R 775 ~/myproject/media
```

---

## 10. Xavfsizlik bo'yicha maslahatlar

### 10.1. SSH xavfsizligi

```bash
# Root login ni o'chirish
sudo nano /etc/ssh/sshd_config
```

Quyidagi qatorni toping va o'zgartiring:

```
PermitRootLogin no
```

SSH ni qayta ishga tushiring:

```bash
sudo systemctl restart sshd
```

### 10.2. Firewall sozlamalari

```bash
# Faqat kerakli portlarni ochish
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### 10.3. Environment variables (muhit o'zgaruvchilari)

SECRET_KEY va boshqa maxfiy ma'lumotlarni alohida faylda saqlash:

```bash
# .env fayl yaratish
nano ~/myproject/.env
```

```env
SECRET_KEY=your-secret-key-here
DB_NAME=news_db
DB_USER=news_user
DB_PASSWORD=kuchli_parol_123!
DB_HOST=localhost
DB_PORT=5432
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

**settings.py da o'qish:**

```python
# settings.py

import os
from pathlib import Path
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}
```

**python-dotenv o'rnatish:**

```bash
pip install python-dotenv
pip freeze > requirements.txt
```

### 10.4. Regular backup

Ma'lumotlar bazasini muntazam zaxiralash:

```bash
# Backup yaratish
pg_dump -U news_user -h localhost news_db > ~/backups/news_db_$(date +%Y%m%d).sql

# Cron job orqali avtomatlashtirish (har kuni tunda 2 da)
crontab -e
```

Quyidagi qatorni qo'shing:

```
0 2 * * * pg_dump -U news_user -h localhost news_db > ~/backups/news_db_$(date +\%Y\%m\%d).sql
```

---

## 11. Monitoring va performance

### 11.1. Nginx access loglarini tahlil qilish

```bash
# Eng ko'p kirilgan sahifalar
sudo cat /var/log/nginx/access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -10

# Eng ko'p so'rov yuborgan IP manzillar
sudo cat /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```

### 11.2. Django debug toolbar o'rnatish (development muhit uchun)

```bash
pip install django-debug-toolbar
```

### 11.3. Server resurslarini monitoring qilish

```bash
# CPU va RAM holati
htop

# Disk holati
df -h

# Running processlar
ps aux | grep gunicorn
```

---

## Xulosa

Ushbu darsda biz Django loyihamizni Ahost serverida to'liq ishga tushirdik:

✅ PostgreSQL ma'lumotlar bazasini yaratdik va sozladik
✅ Database migratsiyalarini bajardik
✅ Statik va media fayllarni to'pladik
✅ Gunicorn WSGI serverni sozladik va systemd service yaratdik
✅ Nginx reverse proxy serverni sozladik
✅ Let's Encrypt SSL sertifikat o'rnatib HTTPS ni yoqdik
✅ Django production sozlamalarini amalga oshirdik
✅ Loyihani yangilash jarayonini o'rgandik
✅ Xavfsizlik va monitoring bo'yicha maslahatlar oldik

Endi loyihangiz professional darajada serverda ishlayapti va foydalanuvchilar uchun ochiq!

---

## Keyingi qadamlar

- **Monitoring:** Server va application monitoring tizimlarini o'rnating (Sentry, New Relic)
- **CDN:** Statik fayllar uchun CDN xizmatidan foydalaning (Cloudflare)
- **Caching:** Redis yoki Memcached orqali caching mexanizmini qo'shing
- **Load Balancing:** Trafik oshganda load balancer o'rnating
- **CI/CD:** GitHub Actions yoki GitLab CI orqali avtomatik deployment sozlang
- **Backup strategiya:** Ma'lumotlar va fayllar uchun muntazam backup tizimini joriy eting

**Tabriklayman!** Siz Django loyihangizni muvaffaqiyatli serverga joylashtirdingiz! 🎉🚀