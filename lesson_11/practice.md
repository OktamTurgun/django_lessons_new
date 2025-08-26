# Lesson 11: Amaliy mashq - Virtual muhit va Django loyiha yaratish

## Mashq 1: Virtual muhit yaratish

### Vazifa 1.1: Virtual muhit o'rnatish
1. Kompyuteringizda yangi papka yarating: `django_news_project`
2. Terminal orqali shu papkaga kiring
3. `news_env` nomli virtual muhit yarating
4. Virtual muhitni faollashting
5. Faollashtirish natijasini screenshot qiling

**Windows:**
```bash
mkdir django_news_project
cd django_news_project
python -m venv news_env
news_env\Scripts\activate
```

**Mac/Linux:**
```bash
mkdir django_news_project
cd django_news_project
python3 -m venv news_env
source news_env/bin/activate
```

### Vazifa 1.2: Virtual muhit tekshiruvi
1. `pip list` buyrug'i bilan o'rnatilgan kutubxonalarni ko'ring
2. Python versiyasini tekshiring: `python --version`
3. Natijalarni yozib oling

**Kutilgan natija:**
- Terminal oldida `(news_env)` ko'rinishi
- Minimal kutubxonalar ro'yxati (pip, setuptools)

## Mashq 2: Django o'rnatish va sozlash

### Vazifa 2.1: Django o'rnatish
1. Virtual muhit faollashtirilganligiga ishonch hosil qiling
2. Django'ning eng so'nggi versiyasini o'rnating
3. O'rnatilgan versiyani tekshiring
4. Kutubxonalar ro'yxatini ko'ring

```bash
pip install django
django-admin --version
pip list
```

### Vazifa 2.2: Loyiha yaratish
1. `news_site` nomli Django loyiha yarating
2. Loyiha tuzilishini o'rganing
3. Har bir faylning vazifasini yozing

```bash
django-admin startproject news_site
cd news_site
dir  # Windows uchun yoki ls # Mac/Linux uchun
```

**Tekshirish:** Quyidagi fayllar yaratilgan bo'lishi kerak:
- `manage.py`
- `news_site/` papka ichida: `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`

## Mashq 3: Loyihani ishga tushirish

### Vazifa 3.1: Dastlabki migratsiya
1. Loyiha papkasida ekanligingizga ishonch hosil qiling
2. Dastlabki migratsiyalarni bajaring
3. Yaratilgan `db.sqlite3` faylini toping

```bash
python manage.py migrate
```

**Kutilgan natija:** "Applying..." xabarlari va yangi `db.sqlite3` fayl

### Vazifa 3.2: Development server ishga tushirish
1. Django development server'ni ishga tushiring
2. Brauzerda `http://127.0.0.1:8000` ga kiring
3. Django welcome sahifasini ko'ring
4. Screenshot oling

```bash
python manage.py runserver
```

**Kutilgan natija:** 
- Terminal: "Starting development server at http://127.0.0.1:8000/"
- Brauzer: Django welcome sahifa (ruxsat yil roket bilan)

### Vazifa 3.3: Boshqa portda ishga tushirish
1. Server'ni to'xtating (Ctrl+C)
2. 8080 portida qayta ishga tushiring
3. Yangi URL da ochib ko'ring

```bash
python manage.py runserver 8080
```

## Mashq 4: Loyiha sozlamalari

### Vazifa 4.1: settings.py o'rganish
1. `news_site/settings.py` faylini oching
2. Quyidagi sozlamalarni toping va qiymatlarini yozing:
   - `DEBUG`
   - `ALLOWED_HOSTS`
   - `DATABASES`
   - `LANGUAGE_CODE`
   - `TIME_ZONE`

### Vazifa 4.2: Sozlamalarni o'zgartirish
1. `LANGUAGE_CODE` ni `'uz-uz'` ga o'zgartiring
2. `TIME_ZONE` ni `'Asia/Tashkent'` ga o'zgartiring
3. Faylni saqlang va server'ni qayta ishga tushiring

```python
LANGUAGE_CODE = 'uz-uz'
TIME_ZONE = 'Asia/Tashkent'
```

## Mashq 5: Admin panel sozlash

### Vazifa 5.1: Superuser yaratish
1. Superuser yarating quyidagi ma'lumotlar bilan:
   - Username: `admin`
   - Email: `admin@news.com`
   - Password: `admin123` (yoki boshqa xavfsiz parol)

```bash
python manage.py createsuperuser
```

### Vazifa 5.2: Admin panelga kirish
1. Server ishga tushirilganligiga ishonch hosil qiling
2. `http://127.0.0.1:8000/admin/` ga kiring
3. Yaratilgan login ma'lumotlar bilan kiring
4. Admin paneli interfeysi screenshot'ini oling

**Kutilgan natija:** Django admin interfeysi, Users va Groups ro'yxati

## Mashq 6: Requirements fayl yaratish

### Vazifa 6.1: Requirements.txt yaratish
1. Joriy loyihadagi barcha kutubxonalar ro'yxatini saqlang
2. Yaratilgan faylni ko'ring va mazmunini tekshiring

```bash
pip freeze > requirements.txt
type requirements.txt  # Windows
# yoki
cat requirements.txt   # Mac/Linux
```

### Vazifa 6.2: Yangi virtual muhitda test qilish
1. Virtual muhitni o'chiring (`deactivate`)
2. Yangi `test_env` virtual muhit yarating va faollashting
3. Requirements.txt orqali kutubxonalarni o'rnating
4. Django versiyasini tekshiring

```bash
deactivate
python -m venv test_env
test_env\Scripts\activate  # Windows
pip install -r requirements.txt
django-admin --version
```

## Mashq 7: Loyiha tuzilishini o'rganish

### Vazifa 7.1: Fayl va papkalar tahlili
Loyiha tuzilishini chizing va har bir element uchun qisqa tavsif yozing:

```
django_news_project/
├── news_env/          # Sizning tavsifingiz
├── test_env/          # Sizning tavsifingiz
├── news_site/         # Sizning tavsifingiz
│   ├── manage.py      # Sizning tavsifingiz
│   ├── db.sqlite3     # Sizning tavsifingiz
│   ├── requirements.txt # Sizning tavsifingiz
│   └── news_site/     # Sizning tavsifingiz
│       ├── __init__.py
│       ├── settings.py
│       ├── urls.py
│       ├── wsgi.py
│       └── asgi.py
```

### Vazifa 7.2: Buyruqlar jadvalini to'ldiring

| Buyruq | Vazifasi | Natija |
|--------|----------|---------|
| `python -m venv env_name` | Virtual muhit yaratish | ... |
| `env_name\Scripts\activate` | ... | ... |
| `pip install django` | ... | ... |
| `django-admin startproject name` | ... | ... |
| `python manage.py migrate` | ... | ... |
| `python manage.py runserver` | ... | ... |
| `python manage.py createsuperuser` | ... | ... |

## Masala yechimlari tekshirish

### Mashq 1 tekshiruvi:
- [ ] Virtual muhit yaratilgan
- [ ] Terminal oldida `(news_env)` ko'rinadi
- [ ] `pip list` minimal kutubxonalar ko'rsatadi

### Mashq 2 tekshiruvi:
- [ ] Django o'rnatilgan
- [ ] Loyiha yaratilgan
- [ ] Barcha kerakli fayllar mavjud

### Mashq 3 tekshiruvi:
- [ ] Migratsiya muvaffaqiyatli
- [ ] Server ishlayapti
- [ ] Django welcome sahifa ko'rinapti
- [ ] Boshqa portda ham ishlamoqda

### Mashq 4 tekshiruvi:
- [ ] settings.py o'qilgan
- [ ] Til va vaqt zonasi o'zgartirilgan

### Mashq 5 tekshiruvi:
- [ ] Superuser yaratilgan
- [ ] Admin panelga kirish mumkin

### Mashq 6 tekshiruvi:
- [ ] requirements.txt yaratilgan
- [ ] Yangi muhitda test qilingan

### Mashq 7 tekshiruvi:
- [ ] Loyiha tuzilishi tushunilgan
- [ ] Buyruqlar jadvali to'ldirilgan

## Qo'shimcha vazifalar (ixtiyoriy)

### Vazifa A: Xato tuzatish mashqi
Quyidagi xatolarni toping va tuzating:
1. Virtual muhit faollashtirilmagan holda Django o'rnatish
2. Loyiha papkasida bo'lmagan holda `runserver` bajarish
3. Noto'g'ri port raqami kiritish

### Vazifa B: Konfiguratsiya o'zgartirishlari
1. ALLOWED_HOSTS ga o'zingizning IP manzilingizni qo'shing
2. Debug rejimini o'chiring va nimalar o'zgarishini kuzating
3. Ma'lumotlar bazasi nomini o'zgartiring

### Vazifa C: Loyiha klonlash mashqi
1. Ushbu loyihani boshqa papkaga nusxalang
2. Yangi virtual muhit yarating
3. Requirements orqali kutubxonalar o'rnating
4. Loyihani ishga tushiring

## Kelajakdagi darslar uchun tayyorlik

Keyingi darsda biz quyidagilarni o'rganamiz:
- Django app yaratish
- Models yaratish va migratsiya qilish
- Views va URL routing
- Templates bilan ishlash

Shu sababli loyihangizni saqlab qo'ying va virtual muhitni faol holatda qoldiring!