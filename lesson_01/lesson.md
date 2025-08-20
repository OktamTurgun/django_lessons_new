# Lesson_01: Django yangi versiyalari bilan ishlash

## Reja
1. Versiya yangilanishi o'zi nima?
2. Katta va kichik o'zgarishlar
3. Yangi va eski versiyalar bilan ishlash

---

### 1. Versiya yangilanishi o'zi nima?
Django doimiy ravishda rivojlanib boradi. Har yangi versiya:
- Yangi funksiyalar qo‘shadi
- Xavfsizlikni mustahkamlaydi
- Xatolarni tuzatadi
- Ba’zan eski funksiyalarni olib tashlaydi

Masalan, **Django 4.x** dan **Django 5.x** ga o‘tishda katta o‘zgarishlar bo‘lishi mumkin.

---

### 2. Katta va kichik o'zgarishlar
- **Major (katta) versiya**:  
  Django 4.x → Django 5.0  
  Bu katta yangiliklar va o‘zgarishlarni anglatadi. Eski kod ba’zida ishlamay qolishi mumkin.
  
- **Minor (kichik) versiya**:  
  Django 5.0 → Django 5.1  
  Bu kichik yangilanish bo‘lib, yangi imkoniyatlar qo‘shiladi, ammo mavjud kod odatda buzilmaydi.

- **Patch (xato tuzatish)**:  
  Django 5.1.1 → Django 5.1.2  
  Bu faqat xatolar va xavfsizlikni tuzatish uchun chiqariladi.

---

### 3. Yangi va eski versiyalar bilan ishlash
Bir vaqtning o‘zida turli loyihalarda turli Django versiyalaridan foydalanish mumkin.  
Buning uchun **virtual environment** ishlatiladi.

Misollar:
- Eski versiyani o‘rnatish:  
  ```bash
  pip install django==4.2   # Django 4.2 versiyasi
  ```
Yangi versiyani o‘rnatish:

```bash

pip install django==5.0.2   # Django 5.0.2 versiyasi
```
### Django versiyasini tekshirish:

```bash

python -m django --version
```

**Keyingi dars:** 
02-dars: Terminal bilan ishalash

