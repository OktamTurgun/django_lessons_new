# Lesson 06 Practice: Django qismlari bilan tanishish

## Maqsad
Ushbu mashqlar orqali siz Django loyihasining asosiy qismlari bilan amaliy tarzda tanishasiz:  
- **Model** (ma’lumotlar qismi)  
- **View** (logika qismi)  
- **Template** (foydalanuvchiga ko‘rinadigan qism)  
- **URLconf** (so‘rovni to‘g‘ri view’ga yo‘naltirish)  

---

## 1 Loyiha strukturasini ko‘rib chiqish
Avval loyihada asosiy fayllarni toping:

- `manage.py` → loyiha boshqaruvi  
- `settings.py` → sozlamalar  
- `urls.py` → URL xaritasi  
- `views.py` → logika funksiyalari  
- `models.py` → ma’lumotlar bazasi modellari  
- `templates/` → HTML sahifalar saqlanadigan joy  

👉 Bu fayllarni ko‘rib chiqing va ularning vazifasini eslab qolishga harakat qiling.  

---

## 2 Birinchi View yozish
Endi oddiy **view** yozamiz.

`blog/views.py` fayliga quyidagini yozing:

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Salom, bu mening birinchi view funksiyam!")
```

 Izoh:

- `request` → foydalanuvchidan kelayotgan so‘rov.  
- `HttpResponse` → oddiy matn ko‘rinishida javob qaytaradi.  

---

## 3️⃣ URL bilan bog‘lash
View ishlashi uchun uni urls.py ga ulash kerak.

👉 `blog/urls.py` faylini yarating:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
```

👉 Endi asosiy `blog_project/urls.py` faylini ochib, blog app’ni ulab qo‘ying:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # blog app'ni ulash
]
```

---

## 4 Serverni ishga tushirish
Terminalda quyidagilarni yozing:

```bash
python manage.py runserver
```

👉 Brauzerda http://127.0.0.1:8000/ manzilini oching.

 Siz quyidagi natijani ko‘rasiz:

```
Salom, bu mening birinchi view funksiyam!
```

---

## 5 Amaliy natija
Siz Django loyihasidagi asosiy qismlar bilan tanishdingiz.

Oddiy oqimni ko‘rdingiz:  
**URL → View → Javob (HTML yoki matn)**

---

## Qo‘shimcha mashq
1. `about` nomli yangi view yarating va `"Bu About sahifa"` degan matn chiqaring.  
2. Uni `urls.py` ga ulab, brauzerda `/about/` manzilini sinab ko‘ring.  
3. `templates/` papkasini yarating va `home.html` faylida HTML sahifa yasang.  
4. `views.py` da `render()` funksiyasi yordamida shuni qaytaring.  

---

## Xulosa
Siz bugun:

- Django loyihasi asosiy qismlarini ko‘rdingiz.  
- Oddiy view yozdingiz va uni URL bilan bog‘ladingiz.  
- Serverni ishga tushirib, birinchi natijani brauzerda ko‘rdingiz.  

👉 Endi siz Django **MVT oqimi** qanday ishlashini tushundingiz:  
**So‘rov → URLconf → View → Template/Response**
