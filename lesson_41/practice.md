# Amaliyot: Lesson 41: Ruxsatnomalar. LoginRequiredMixin vs UserPassesTestMixin

## Amaliyot: Lesson 42: Superuser va Staff foydalanuvchilarni boshqarish

Ushbu amaliyotda Django'da `superuser` va `staff` foydalanuvchilarni yaratish, ularga ruxsatlar berish va admin panel orqali boshqarish usullarini o'rganamiz.

---

### 1. Superuser va Staff foydalanuvchilar nima?

- **Superuser** — barcha ruxsatlarga ega bo'lgan administrator.
- **Staff** — admin panelga kira oladigan, lekin barcha ruxsatlarga ega bo'lmasligi mumkin bo'lgan foydalanuvchi.

---

### 2. Superuser yaratish

Terminalda quyidagi buyruqni bajaring:

```bash
python manage.py createsuperuser
```

So'rovga binoan foydalanuvchi nomi, email va parol kiriting.

---

### 3. Staff foydalanuvchi yaratish

1. Oddiy foydalanuvchi yarating (masalan, sayt orqali yoki shell yordamida):

```python
from django.contrib.auth.models import User
user = User.objects.create_user(username='staffuser', password='parol123')
user.is_staff = True
user.save()
```

2. Yoki admin panelda foydalanuvchini tanlab, **Staff status** ni belgilang.

---

### 4. Foydalanuvchi ruxsatlarini tekshirish

Django admin paneliga faqat `is_staff=True` foydalanuvchilar kira oladi.

- `is_superuser=True` bo'lsa, barcha ruxsatlar ochiq.
- `is_staff=True` bo'lsa, admin panelga kirish mumkin, lekin ruxsatlar cheklangan bo'lishi mumkin.

---

### 5. Foydalanuvchi ruxsatlarini kodda tekshirish

Misol uchun, faqat staff foydalanuvchilar uchun view yozish:

```python
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def my_view(request):
  # Faqat staff foydalanuvchilar uchun
  ...
```

Yoki superuser uchun:

```python
from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func):
  return user_passes_test(lambda u: u.is_superuser)(view_func)
```

---

### 6. Admin panelda ruxsatlarni boshqarish

- Admin panelda foydalanuvchini tanlang.
- **Permissions** bo'limida kerakli ruxsatlarni belgilang.
- **Staff status** va **Superuser status** ni sozlang.

---

## Maslahatlar va Best Practices

- Har doim superuser parolini kuchli va maxfiy saqlang.
- Staff foydalanuvchilarga faqat kerakli ruxsatlarni bering.
- Ruxsatlarni kodda ham, admin panelda ham boshqarishni o'rganing.
- Foydalanuvchi ruxsatlarini sinovdan o'tkazib ko'ring.

---

**Qo'shimcha:**  
Django ruxsatnomalari haqida rasmiy hujjatlarni o'qing:  
https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization

---

## Qo'shimcha amaliy mashqlar

### 7. Foydalanuvchi ruxsatlarini sinab ko'rish

1. **Yangi oddiy foydalanuvchi** yarating va unga admin panelga kirishga harakat qiling. Kirish mumkin emasligini tekshiring.
2. **Staff status** ni yoqing va yana admin panelga kirishga harakat qiling.
3. **Superuser status** ni yoqing va barcha ruxsatlar ochilganini tekshiring.

### 8. Maxsus ruxsatlar bilan view yozish

Faqat ma'lum ruxsatga ega foydalanuvchilar uchun view yozing:

```python
from django.contrib.auth.decorators import permission_required

@permission_required('auth.view_user', raise_exception=True)
def user_list(request):
  # Faqat 'view_user' ruxsatiga ega foydalanuvchilar uchun
  ...
```

### 9. Guruhlar (Groups) orqali ruxsatlarni boshqarish

1. Admin panelda yangi **Group** yarating (masalan, "Moderators").
2. Guruhga kerakli ruxsatlarni biriktiring.
3. Foydalanuvchini ushbu guruhga qo'shing.
4. Kodda yoki admin panelda ushbu guruhga tegishli ruxsatlarni tekshirib ko'ring.

### 10. Amaliy topshiriqlar

- Yangi staff foydalanuvchi yarating va unga faqat bitta model ustidan o'qish ruxsatini bering.
- Yangi superuser yarating va barcha ruxsatlarni tekshirib chiqing.
- Guruhlar orqali ruxsatlarni boshqarib, har xil foydalanuvchilar uchun turli imkoniyatlarni sinab ko'ring.

---

**Foydali havolalar:**
- [Django permissions documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization)
- [Django groups documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#groups)

---