
# 46-dars: Yangiliklarni izlash funksiyasi (Search)

## Kirish

Ushbu darsda Django framework yordamida yangiliklarni izlash funksiyasini to'liq va mukammal tarzda yaratishni o'rganamiz. Har bir bosqichda kod misollari, izohlar, kengaytirilgan tushuntirishlar va muhim nuqtalar keltiriladi. Dars oxirida siz mustaqil ravishda izlash funksiyasini yaratishingiz mumkin bo'ladi.


## Bu darsda ko'rib chiqiladigan mavzular:
- Model yaratish (kategoriya va muallif bilan)
- Qidiruv formasi
- View yozish (pagination bilan)
- URL sozlash
- Template yaratish (Bootstrap bilan)
- Qidiruv funksiyasini takomillashtirish
- Sinab ko'rish va xatolarni tuzatish
- Qo'shimcha maslahatlar va savollar

---


## 1. Model yaratish

### 1.1. Yangiliklar modeli (kategoriya va muallif bilan)

Avvalo, yangiliklar uchun model yaratamiz. Modelda sarlavha, matn, chop etilgan vaqt, kategoriya va muallif saqlanadi.

```python
# news/models.py
from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):
  name = models.CharField(max_length=100)
  def __str__(self):
    return self.name

class News(models.Model):
  title = models.CharField(max_length=200, help_text="Yangilik sarlavhasi")
  content = models.TextField(help_text="Yangilik matni")
  published_at = models.DateTimeField(auto_now_add=True, help_text="Chop etilgan vaqt")
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
  author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.title
```

**Izoh:**
- Kategoriya va muallif maydonlari real loyihalarda juda muhim.
- `get_user_model()` — muallif uchun.


### 1.2. Migratsiya qilish

Modelni yaratganimizdan so'ng, ma'lumotlar bazasiga migratsiya qilamiz:

```bash
python manage.py makemigrations news
python manage.py migrate
```

**Eslatma:**
Xatolik bo‘lsa, model nomi va maydonlarni tekshiring.

---


## 2. Qidiruv formasi yaratish

### 2.1. Formani yozish

Yangiliklarni izlash uchun oddiy forma yaratamiz:

```python
# news/forms.py
from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        label='Qidiruv',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Qidiruv so\'zini kiriting',
            'class': 'form-control'
        })
    )
```

**Izoh:**
- `class: form-control` Bootstrap uchun.

---


## 3. Izlash view'ini yozish

### 3.1. View funksiyasi (pagination bilan)

Izlash funksiyasini viewda yozamiz:

```python
# news/views.py
from django.shortcuts import render
from .models import News
from .forms import SearchForm
from django.core.paginator import Paginator

def search_news(request):
    form = SearchForm(request.GET or None)
    results = News.objects.none()
    query = ""
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = News.objects.filter(
                title__icontains=query
            ) | News.objects.filter(
                content__icontains=query
            )
            results = results.order_by('-published_at')

    paginator = Paginator(results, 5)  # Har sahifada 5 ta natija
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/search.html', {
        'form': form,
        'page_obj': page_obj,
        'query': query
    })
```

**Izoh:**
- `Paginator` natijalarni sahifalash uchun.
- `order_by('-published_at')` — so‘nggi yangiliklar birinchi chiqadi.

---


## 4. URL sozlash

### 4.1. URL'ni bog'lash

Izlash view'ini URL'ga bog'laymiz:

```python
# news/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_news, name='search_news'),
]
```

**Izoh:**
- `name='search_news'` — URL'ni nomlash, revers uchun qulay.

---


## 5. Template yaratish (Bootstrap va pagination bilan)

### 5.1. Template fayli

Izlash formasi va natijalarni ko'rsatish uchun template yozamiz:

```html
<!-- news/templates/news/search.html -->
<div class="container mt-4">
    <h2>Yangiliklarni izlash</h2>
    <form method="get" action="{% url 'search_news' %}" class="row g-3 mb-4">
        <div class="col-md-8">
            {{ form.query }}
        </div>
        <div class="col-md-4">
            <button type="submit" class="btn btn-primary">Izlash</button>
        </div>
    </form>

    {% if query %}
        <h4>Natijalar: "{{ query }}"</h4>
        {% if page_obj.object_list %}
            <ul class="list-group mb-3">
                {% for news in page_obj %}
                <li class="list-group-item">
                    <strong>{{ news.title }}</strong>
                    {% if news.category %}<span class="badge bg-info ms-2">{{ news.category.name }}</span>{% endif %}
                    <br>
                    <small class="text-muted">{{ news.published_at|date:"Y-m-d H:i" }} | {{ news.author }}</small>
                    <p>{{ news.content|truncatewords:20 }}</p>
                </li>
                {% endfor %}
            </ul>

            <!-- Pagination -->
            <nav>
                <ul class="pagination">
                    {% if page_obj.has_previous %}
                    <li class="page-item"><a class="page-link" href="?q={{ query }}&page={{ page_obj.previous_page_number }}">Oldingi</a></li>
                    {% endif %}
                    <li class="page-item active"><span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span></li>
                    {% if page_obj.has_next %}
                    <li class="page-item"><a class="page-link" href="?q={{ query }}&page={{ page_obj.next_page_number }}">Keyingi</a></li>
                    {% endif %}
                </ul>
            </nav>
        {% else %}
            <div class="alert alert-warning">Hech qanday yangilik topilmadi.</div>
        {% endif %}
    {% endif %}
</div>
```

**Izoh:**
- Bootstrap klasslari natijalarni chiroyli ko‘rsatadi.
- Pagination natijalarni sahifalash uchun.

---


## 6. Sinab ko'rish va xatolarni tuzatish

### 6.1. Serverni ishga tushirish

```bash
python manage.py runserver
```

### 6.2. Qidiruvni tekshirish

Brauzerda `http://localhost:8000/search/` sahifasiga o'ting. Qidiruv so'zini kiriting va natijalarni ko'ring.

**Savol-javoblar:**
- **Savol:** Qidiruv natijalari chiqmayapti, nima qilish kerak?
  - Yangiliklar bazada borligiga va forma to'g'ri ishlayotganiga ishonch hosil qiling.
- **Savol:** Qidiruv faqat sarlavhada ishlayaptimi?
  - Yuqoridagi kodda sarlavha va matnda ham izlanadi.
- **Savol:** Qidiruv so‘zi bo‘sh bo‘lsa, natija chiqmaydi. Buni foydalanuvchiga xabar sifatida ko‘rsating.

---


## 7. Qo'shimcha takomillashtirishlar va maslahatlar

- **Advanced Search:** Faqat sarlavha yoki matn bo‘yicha alohida qidiruv qo‘shing.
- **Xavfsizlik:** Foydalanuvchi kiritgan so‘zlarni sanitizatsiya qiling.
- **Kategoriya bo‘yicha qidiruv:** Formaga kategoriya tanlash maydonini qo‘shing.
- **Muallif bo‘yicha qidiruv:** Faqat muallifga tegishli yangiliklarni qidirish.
- **Frontend:** Bootstrap yordamida responsive dizayn yarating.
- **Backend:** Qidiruv natijalarini tartiblash va cheklash.

---


## Xulosa

Ushbu darsda Django'da yangiliklarni izlash funksiyasini to'liq va zamonaviy usulda yaratishni o'rgandingiz. Model, forma, view, URL va template bosqichlarini keng misollar va izohlar bilan ko'rdik. Endi siz mustaqil ravishda izlash funksiyasini loyihalaringizda qo'llashingiz va takomillashtirishingiz mumkin.

### Amaliy savollar:
1. Qidiruv natijalarini qanday tartiblash mumkin?
2. Qidiruvda faqat sarlavha yoki matn bo‘yicha filter qilish uchun qanday kod yoziladi?
3. Pagination’ni o‘zgartirish uchun qaysi parametrni o‘zgartirish kerak?
4. Bootstrap yordamida formani qanday chiroyli qilish mumkin?
5. Kategoriya bo‘yicha qidiruvni qanday qo‘shish mumkin?
