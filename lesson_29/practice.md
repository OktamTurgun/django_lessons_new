
# Amaliyot: Yangiliklarni tahrirlash va o'chirish

Ushbu amaliyotda siz Django’da yangiliklarni tahrirlash va o‘chirish funksiyalarini mustaqil qo‘shasiz. Har bir bosqich uchun misol kodlar, yechimlar, maslahatlar va tafsiflar keltirilgan.

---

## 1. Model va test ma'lumotlar

**Tavsif:** Yangiliklar modelini to‘g‘ri to‘ldiring va test ma'lumotlar kiriting.

**Maslahat:** Admin panelda bir nechta yangilik, kategoriya va muallif yarating.

**Yechim:**
1. `python manage.py createsuperuser` buyrug‘i bilan superuser yarating.
2. `python manage.py runserver` orqali serverni ishga tushiring.
3. `http://localhost:8000/admin` ga kirib, yangiliklar, kategoriyalar va mualliflarni kiriting.

---

## 2. URL'larni qo‘shish

**Tavsif:** Yangilikni tahrirlash va o‘chirish uchun URL yo‘llarini yarating.

**Maslahat:** URL’larda `<int:pk>` primary key orqali yangilikni aniqlash uchun ishlatiladi.

**Misol kod:**
```python
# news/urls.py
from django.urls import path
from .views import NewsUpdateView, NewsDeleteView

urlpatterns = [
  path('edit/<int:pk>/', NewsUpdateView.as_view(), name='edit_news'),
  path('delete/<int:pk>/', NewsDeleteView.as_view(), name='delete_news'),
]
```

---

## 3. View'larni yozish

**Tafsif:** Class-based view’lar yordamida tahrirlash va o‘chirish funksiyalarini yozing.

**Maslahat:** CBV’lar kodni soddalashtiradi va ko‘p funksiyani avtomatik bajaradi.

**Misol kod:**
```python
# news/views.py
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import News
from .forms import NewsForm

class NewsUpdateView(UpdateView):
  model = News
  form_class = NewsForm
  template_name = 'news/edit_news.html'
  def get_success_url(self):
    return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})

class NewsDeleteView(DeleteView):
  model = News
  template_name = 'news/delete_news.html'
  success_url = reverse_lazy('news_list')
```

---

## 4. Formani yaratish

**Tafsif:** ModelForm yordamida yangilikni tahrirlash formasini yarating.

**Maslahat:** ModelForm model maydonlarini avtomatik formaga aylantiradi.

**Misol kod:**
```python
# news/forms.py
from django import forms
from .models import News

class NewsForm(forms.ModelForm):
  class Meta:
    model = News
    fields = ['title', 'body', 'category', 'photo']
```

---

## 5. Template'larni yaratish

**Tafsif:** Tahrirlash va o‘chirish uchun HTML template’lar yarating.

**Maslahat:** Formani to‘ldirishda xatoliklar bo‘lsa, foydalanuvchiga ko‘rsating.

**Misol kodlar:**

**edit_news.html**
```html
{% extends 'base.html' %}
{% block title %}Yangilikni tahrirlash{% endblock %}
{% block content %}
<div class="container">
  <h2>Yangilikni tahrirlash</h2>
  <form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    {% if form.errors %}
    <div class="alert alert-danger">
      {{ form.errors }}
    </div>
    {% endif %}
    <button type="submit" class="btn btn-success">Saqlash</button>
    <a href="{% url 'news_detail' object.pk %}" class="btn btn-secondary">Orqaga</a>
  </form>
</div>
{% endblock %}
```

**delete_news.html**
```html
{% extends 'base.html' %}
{% block title %}Yangilikni o'chirish{% endblock %}
{% block content %}
<div class="container">
  <h2>Yangilikni o'chirish</h2>
  <p>Haqiqatan ham "{{ object.title }}" yangiligini o'chirmoqchimisiz?</p>
  <form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">O'chirish</button>
    <a href="{% url 'news_detail' object.pk %}" class="btn btn-secondary">Bekor qilish</a>
  </form>
</div>
{% endblock %}
```

---

## 6. Yangiliklar ro‘yxatida tugmalar

**Tafsif:** Har bir yangilik yonida tahrirlash va o‘chirish tugmalari chiqaring.

**Maslahat:** Tugmalarni faqat admin yoki muallif ko‘ra oladigan qilib cheklash mumkin.

**Misol kod:**
```html
<a href="{% url 'edit_news' news.pk %}" class="btn btn-warning btn-sm">Tahrirlash</a>
<a href="{% url 'delete_news' news.pk %}" class="btn btn-danger btn-sm">O'chirish</a>
```

---

## 7. Test va tekshirish

**Tafsif:** Tahrirlash va o‘chirish funksiyalarini sinab ko‘ring.

**Maslahat:** Har bir bosqichdan so‘ng serverni qayta ishga tushiring va natijani tekshiring.

**Yechim:**
```bash
python manage.py runserver
```
Admin panel orqali yangiliklar qo‘shing va ro‘yxatdan tahrirlash/o‘chirish tugmalarini bosib, natijani tekshiring.

---

## 8. Qo‘shimcha topshiriqlar

**Tafsif:** Funksiyalarni yanada mukammallashtiring.

**Maslahatlar:**
- Tahrirlash va o‘chirishni faqat admin yoki muallifga ruxsat bering:
```python
# NewsUpdateView va NewsDeleteView da dispatch metodini override qiling
from django.core.exceptions import PermissionDenied
def dispatch(self, request, *args, **kwargs):
  obj = self.get_object()
  if not request.user.is_superuser and obj.author != request.user:
    raise PermissionDenied
  return super().dispatch(request, *args, **kwargs)
```
- O‘chirishdan oldin modal yoki alert chiqaring (JavaScript yordamida).
- Formani to‘ldirishda xatoliklar bo‘lsa, alert orqali ko‘rsating.

---

## 9. Savollar va yechimlar

1. **UpdateView va DeleteView’ning asosiy farqlari nimada?**
   - UpdateView obyektni tahrirlash uchun, DeleteView esa o‘chirish uchun ishlatiladi.
2. **ModelForm qanday ishlaydi?**
   - Model maydonlarini avtomatik formaga aylantiradi va validatsiya qiladi.
3. **URL routingda `<int:pk>` nimani anglatadi?**
   - Obyektning primary key (id) ni URL orqali uzatadi.
4. **Tahrirlash va o‘chirish funksiyalarini qanday qilib faqat muallifga ruxsat berish mumkin?**
   - View’larda dispatch metodini override qilib, muallifni tekshirish orqali.

---

**Amaliyot yakuni:** Ushbu amaliyotdan so‘ng siz Django’da yangiliklarni tahrirlash va o‘chirish funksiyalarini mustaqil va professional tarzda qo‘sha olasiz.
