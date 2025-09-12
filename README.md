# Django Lessons Repository

Bu repositoryda Django framework bo'yicha darsliklar jamlangan.  
Har bir dars alohida `lesson_xx` papkasida saqlanadi va o'z loyihasiga ega.

Ushbu repository Python va Django bo'yicha mukammal darslarni o'rganish uchun mo'ljallangan. Har bir dars alohida papkada joylashgan va unda nazariy `lesson.md` va amaliy `practice.md` fayllari mavjud.

---

## Mavzular jadvali

- [Django Lessons Repository](#django-lessons-repository)
  - [Mavzular jadvali](#mavzular-jadvali)
  - [Tuzilma. Darslar ro'yxati](#tuzilma-darslar-royxati)
    - [Boshlang‘ich va muhityaratish](#boshlangich-va-muhityaratish)
    - [Asosiy Django qismlari](#asosiy-django-qismlari)
    - [Loyihalarni yaratish va boshqarish](#loyihalarni-yaratish-va-boshqarish)
    - [Forms va user management](#forms-va-user-management)
    - [Git va CRUD amaliyotlar](#git-va-crud-amaliyotlar)
    - [Foydalanuvchi autentifikatsiyasi](#foydalanuvchi-autentifikatsiyasi)
    - [Signup va ruxsatnomalar](#signup-va-ruxsatnomalar)
    - [Izohlar va interaktivlik](#izohlar-va-interaktivlik)
    - [Tarjima va internationalization](#tarjima-va-internationalization)
    - [Deployment](#deployment)
    - [Testlash](#testlash)
  - [O'rnatish](#ornatish)
  - [Har bir yangi lesson uchun Pipenv setup qadamlar](#har-bir-yangi-lesson-uchun-pipenv-setup-qadamlar)
  - [Loyihaning tuzilishi](#loyihaning-tuzilishi)
  - [Qanday ishlatish](#qanday-ishlatish)
  - [Litsenziya](#litsenziya)
  - [Muallif](#muallif)

---

## Tuzilma. Darslar ro'yxati

### Boshlang‘ich va muhityaratish
-   `lesson_01/` → Django yangi versiyalar bilan ishlash
-   `lesson_02/` → Terminal bilan tanishish
-   `lesson_03/` → Django arxitekturasi va ishlash tamoyili
-   `lesson_04/` → Virtual muhitlar bilan tanishish. Pipenv o‘rnatish va sozlash
-   `lesson_05/` → VS Code dasturini sozlash va kengaytmalar o‘rnatish
-   `lesson_06/` → Blog loyihasini ishga tushirish

### Asosiy Django qismlari
-   `lesson_07/` → Django qismlari bilan tanishish
-   `lesson_08/` → Blog model qismi
-   `lesson_09/` → Blog loyihasi: Views va templates bilan ishlash
-   `lesson_10/` → BlogDetail: Funksiyaga asoslangan View

### Loyihalarni yaratish va boshqarish
-   `lesson_11/` → Yangiliklar sayti loyihasi bilan tanishish
-   `lesson_12/` → Loyihaning starter kodini ishga tushirish va virtual muhit o‘rnatish
-   `lesson_13/` → Database dizaynini yaratish (DrawSQL.app)
-   `lesson_14/` → Loyiha modelini tuzish
-   `lesson_15/` → Admin qismi bilan ishlash
-   `lesson_16/` → Queryset va model manager
-   `lesson_17/` → News list va detail page
-   `lesson_18/` → Template va static fayllar bilan ishlash
-   `lesson_19/` → Yangiliklar sayti shablonini Django’ga o‘rnatish

### Forms va user management
-   `lesson_20/` → Home va Contact sahifalarini ishga tushirish
-   `lesson_21/` → Formalar bilan ishlash: Contact Form
-   `lesson_22/` → Class bilan FormView yaratish
-   `lesson_23/` → ModelForm vs Form
-   `lesson_24/` → Bosh sahifada yangiliklarni kategoriya bo‘yicha ko‘rsatish (1-qism)
-   `lesson_25/` → Context manager bilan bosh sahifa (2-qism)
-   `lesson_26/` → Context_processor va get_context_data
-   `lesson_27/` → Template teglari: Loyihani to‘ldirish
-   `lesson_28/` → URLni slugga o‘zgartirish: get_absolute_url
-   `lesson_29/` → Yangiliklar sayti sahifasini yaratish

### Git va CRUD amaliyotlar
-   `lesson_30/` → Git: Loyihani GitHub’ga yuklash
-   `lesson_31/` → Yangiliklarni tahrirlash va o‘chirish funksiyalari
-   `lesson_32/` → Saytga yangilik qo‘shish: CreateView

### Foydalanuvchi autentifikatsiyasi
-   `lesson_33/` → Login va Logout
-   `lesson_34/` → Foydalanuvchi profilini yaratish
-   `lesson_35/` → Foydalanuvchi parolini o‘zgartirish
-   `lesson_36/` → Foydalanuvchi parolini qayta tiklash (1-qism)
-   `lesson_37/` → Foydalanuvchi parolini qayta tiklash (2-qism)

### Signup va ruxsatnomalar
-   `lesson_38/` → Signup: Class View orqali ro‘yxatdan o‘tish
-   `lesson_39/` → Profil modelini yaratish va tahrirlash
-   `lesson_40/` → Login_required dekoratori va LoginRequiredMixin
-   `lesson_41/` → Profilda rasm va boshqa ma’lumotlarni chiqarish
-   `lesson_42/` → Ruxsatnomalar: LoginRequiredMixin vs UserPassesTestMixin
-   `lesson_43/` → Admin sahifasi: dekoratorli ruxsatnomalar

### Izohlar va interaktivlik
-   `lesson_44/` → Django’da izoh qoldirish. Izoh modeli va formasini yaratish (1-qism)
-   `lesson_45/` → Views qismini yozish (2-qism)
-   `lesson_46/` → Template qismini yozish (3-qism)
-   `lesson_47/` → Yangiliklarni izlash funksiyasi
-   `lesson_48/` → Ko‘rishlar sonini aniqlash
-   `lesson_49/` → Ko‘rishlar sonini template’da aks ettirish
-   `lesson_50/` → Izohlar sonini template’dan chiqarish va GitHub’ga o‘zgarishlarni saqlash

### Tarjima va internationalization
-   `lesson_51/` → Veb-saytni i18n orqali tarjima qilish
-   `lesson_52/` → ModelTranslation modulidan foydalanib modelni tarjima qilish
-   `lesson_53/` → Template’dagi matnlarni tarjima qilish

### Deployment
-   `lesson_54/` → Deployment: Ahost serveriga joylash (1-qism)
-   `lesson_55/` → Deployment: Ahost serveriga joylash (2-qism)

### Testlash
-   `lesson_56/` → Django uchun testlar

---

## O'rnatish

Repositoryni klon qilish:

1. Repository’ni klonlash:

```bash
git clone https://github.com/UktamTurgun/django_lessons_new.git
cd django_lessons_new
```

2. Virtual muhit yaratish (lesson_04 uchun):

```bash
cd lesson_04/Pipenv_project
pipenv install
pipenv shell
```

3. Har bir lesson papkasida `lesson.md` va `practice.md` fayllarni o‘rganish va amaliyot qilish.

---

## Har bir yangi lesson uchun Pipenv setup qadamlar

1.  **Yangi dars papkasiga o'tish:**

    ```bash
    cd lesson_xx/project_name
    ```

2.  **Pipenv muhitini yaratish:**

    ```bash
    pipenv install django
    ```

    Agar boshqa kutubxonalar kerak bo'lsa, qo'shimcha o'rnatiladi:

    ```bash
    pipenv install requests pillow
    ```

3.  **Pipfile.lock faylini yaratish va lock qilish:**

    ```bash
    pipenv lock
    ```

4.  **Virtual environment ichida ishlash:**

    ```bash
    pipenv shell
    ```

5.  **Django loyihani ishga tushirish:**

    ```bash
    python manage.py runserver
    ```

---

✅ Shu qadamlar orqali har bir yangi `lesson_xx` uchun mustaqil virtual muhit yaratiladi va `Pipfile.lock` fayllari GitHub'ga qo'shib boriladi.  
Bu esa loyihalarning **barqarorligini**, **izolyatsiyasini** va **versiya nazoratini** ta'minlaydi.

---

## Loyihaning tuzilishi

```
django_lessons_new/
├─ lesson_01/
│   ├─ lesson.md
│   └─ practice.md
├─ lesson_04/
│   ├─ lesson.md
│   ├─ practice.md
│   └─ Pipenv_project/
│       ├─ Pipfile
│       └─ Pipfile.lock
├─ django_projects_cheetsheets.md
└─ README.md
```

## Qanday ishlatish

1. Repository’ni klonlash:

```bash
git clone https://github.com/UktamTurgun/django_lessons_new.git
cd django_lessons_new
```

2. Virtual muhit yaratish (lesson_04 uchun):

```bash
cd lesson_04/Pipenv_project
pipenv install
pipenv shell
```

3. Har bir lesson papkasida `lesson.md` va `practice.md` fayllarni o‘rganish va amaliyot qilish.

---

## Litsenziya

Ushbu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil [LICENSE](LICENSE) faylga qarang.

## Muallif
**GitHub:** [OktamTurgun](https://github.com/OktamTurgun)
