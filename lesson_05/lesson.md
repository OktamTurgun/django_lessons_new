
# Lesson 05: Blog loyihasini ishga tushirish

## Maqsad
Ushbu darsning maqsadi — Django loyihasini ishga tushirish jarayonini o‘rganish va asosiy blog loyihasi starter kodini yaratish.

---

## 1. Django loyihasini yaratish

1. Terminalni oching va loyiha papkasiga kiring:

```bash
cd django_lessons_new
```

2. Yangi Django loyihasini yaratish:

```bash
django-admin startproject blog_project
```

blog_project — loyihaning nomi. Siz xohlagan nomni berishingiz mumkin.

3. Loyihani tekshirish:

```bash
cd blog_project
python manage.py runserver
```

Brauzerda http://127.0.0.1:8000/ ni oching. Django start sahifasi chiqsa, loyiha muvaffaqiyatli ishga tushdi.

### 2. Blog ilovasini yaratish
Django ilovasini yaratish:

```bash
python manage.py startapp blog
```

blog — ilova nomi.

`settings.py` faylida **INSTALLED_APPS** ga blog ilovasini qo‘shish:

```python
INSTALLED_APPS = [
    ...
    'blog',
]
```

### 3. Starter kod strukturasini ko‘rish

```
blog_project/
├─ blog_project/
│  ├─ settings.py
│  ├─ urls.py
│  └─ wsgi.py
├─ blog/
│  ├─ models.py
│  ├─ views.py
│  ├─ urls.py   # keyin qo‘shiladi
│  └─ templates/
├─ manage.py
```

### 4. Ishga tushirish bo‘yicha amaliy maslahatlar
- Har doim virtual muhitda ishlang (pipenv shell yoki venv).
- Loyihani GitHub-ga yuklashdan oldin `git init` va `.gitignore` faylini tekshiring.
- Django serverini ishga tushirish uchun:

```bash
python manage.py runserver
```

Xatolar bo‘lsa, terminaldagi xabarlarni diqqat bilan o‘qing.

**Xulosa**

- Django loyihasi va ilovasini yaratish, asosiy strukturasini ko‘rish, serverni ishga tushirish darsning asosiy qismi hisoblanadi.