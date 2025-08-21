# Lesson 05 Practice: Blog loyihasini ishga tushirish

## Amaliy mashqlar

1. Django loyihasini yaratish:

```bash
django-admin startproject blog_project
cd blog_project
python manage.py runserver
```

Brauzerda start sahifasi chiqishini tekshiring.

### Blog ilovasini yaratish:

```bash
python manage.py startapp blog
```

`INSTALLED_APPS` ga blog ilovasini qo‘shing va `python manage.py runserver` orqali serverni qayta ishga tushiring.

Starter kod strukturasini terminal orqali tekshiring:

```bash
tree
```
(yoki Windows uchun `dir /s`)

Virtual muhitni ishga tushiring (agar Pipenv ishlatayotgan bo‘lsangiz):

```bash
cd ../lesson_04/Pipenv_project
pipenv shell
```

**Natija:**

- Django loyihasi va blog ilovasi muvaffaqiyatli ishga tushdi.
- Brauzerda Django start sahifasi ochiladi.