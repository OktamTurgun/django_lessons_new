
# Amaliyot: Yangiliklarni izlash funksiyasi

Ushbu amaliyotda siz Django’da yangiliklarni izlash funksiyasini mustaqil yaratib, takomillashtirasiz. Har bir bosqichda misol kodlar, yechimlar, maslahatlar, best practice’lar va turli holatlar uchun misollar keltirilgan.

---


## 1. Model yaratish va test ma'lumotlar

**Tavsif:** Yangiliklar, kategoriya va muallif maydonlari bilan model yarating. Har xil holatlar uchun misollar:

**Misol kod (oddiy):**
```python
# news/models.py
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
```

**Misol kod (kategoriya va muallif bilan):**
```python
from django.db import models
from django.contrib.auth import get_user_model
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.title
```

**Yechim:**
- `python manage.py makemigrations news`
- `python manage.py migrate`
- Admin panel orqali test yangiliklar, kategoriya va muallif kiriting.

**Best practice:**
- Model maydonlarini to‘g‘ri nomlang va verbose_name qo‘shing.
- Kategoriya va muallif bo‘lmasa, null=True, blank=True ishlating.

---


## 2. Qidiruv formasi yaratish

**Tavsif:** Qidiruv uchun forma yarating. Har xil holatlar uchun misollar:

**Misol kod (faqat matn):**
```python
class SearchForm(forms.Form):
    query = forms.CharField(label='Qidiruv', max_length=100, required=False)
```

**Misol kod (kategoriya tanlash bilan):**
```python
class SearchForm(forms.Form):
    query = forms.CharField(label='Qidiruv', max_length=100, required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
```

**Yechim:**
- Formani viewda ishlatish uchun import qiling.

**Best practice:**
- Bootstrap klasslarini inputga qo‘shing.
- Placeholder va required parametrlardan foydalaning.

---


## 3. View yozish (pagination va turli holatlar bilan)

**Tavsif:** Qidiruv view’ini pagination bilan yozing. Har xil holatlar uchun misollar:

**Misol kod (oddiy):**
```python
def search_news(request):
    form = SearchForm(request.GET or None)
    results = News.objects.none()
    query = ""
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = News.objects.filter(title__icontains=query) | News.objects.filter(content__icontains=query)
            results = results.order_by('-published_at')
    paginator = Paginator(results, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/search.html', {'form': form, 'page_obj': page_obj, 'query': query})
```

**Misol kod (kategoriya bo‘yicha filter):**
```python
def search_news(request):
    form = SearchForm(request.GET or None)
    results = News.objects.all()
    query = form.cleaned_data.get('query', '') if form.is_valid() else ''
    category = form.cleaned_data.get('category', None) if form.is_valid() else None
    if query:
        results = results.filter(title__icontains=query) | results.filter(content__icontains=query)
    if category:
        results = results.filter(category=category)
    results = results.order_by('-published_at')
    paginator = Paginator(results, 5)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'news/search.html', {'form': form, 'page_obj': page_obj, 'query': query, 'category': category})
```

**Yechim:**
- Har sahifada 5 ta natija chiqadi.
- Kategoriya bo‘yicha filter qilish mumkin.

**Best practice:**
- Query bo‘sh bo‘lsa, natija chiqmasin va xabar ko‘rsating.
- Foydalanuvchi xatoliklarini alert orqali ko‘rsating.

---


## 4. URL sozlash

**Tavsif:** Qidiruv view’ini URL’ga bog‘lang.

**Misol kod:**
```python
urlpatterns = [
    path('search/', views.search_news, name='search_news'),
]
```

**Yechim:**
- URL nomini `name='search_news'` deb belgilang.

**Best practice:**
- URL nomlash revers uchun qulay.

---


## 5. Template yaratish (Bootstrap, pagination va turli holatlar bilan)

**Tavsif:** Qidiruv formasi va natijalarni chiroyli ko‘rsating. Har xil holatlar uchun misollar:

**Misol kod (oddiy):**
```html
<form method="get" action="{% url 'search_news' %}">
    {{ form.query }}
    <button type="submit">Izlash</button>
</form>
```

**Misol kod (kategoriya tanlash bilan):**
```html
<form method="get" action="{% url 'search_news' %}" class="row g-3 mb-4">
    <div class="col-md-6">{{ form.query }}</div>
    <div class="col-md-4">{{ form.category }}</div>
    <div class="col-md-2"><button type="submit" class="btn btn-primary">Izlash</button></div>
</form>
```

**Natijalar va pagination:**
```html
{% if query or category %}
    <h4>Natijalar: "{{ query }}" {% if category %}({{ category.name }}){% endif %}</h4>
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
        <nav>
            <ul class="pagination">
                {% if page_obj.has_previous %}
                <li class="page-item"><a class="page-link" href="?q={{ query }}{% if category %}&category={{ category.pk }}{% endif %}&page={{ page_obj.previous_page_number }}">Oldingi</a></li>
                {% endif %}
                <li class="page-item active"><span class="page-link">{{ page_obj.number }} / {{ page_obj.paginator.num_pages }}</span></li>
                {% if page_obj.has_next %}
                <li class="page-item"><a class="page-link" href="?q={{ query }}{% if category %}&category={{ category.pk }}{% endif %}&page={{ page_obj.next_page_number }}">Keyingi</a></li>
                {% endif %}
            </ul>
        </nav>
    {% else %}
        <div class="alert alert-warning">Hech qanday yangilik topilmadi.</div>
    {% endif %}
{% endif %}
```

**Best practice:**
- Foydalanuvchi xatoliklarini alert orqali ko‘rsating.
- Responsive dizayn uchun Bootstrap’dan foydalaning.

---


## 6. Sinab ko‘rish va xatolarni tuzatish

**Tavsif:** Qidiruv funksiyasini test qiling. Har xil holatlar uchun misollar:

- Qidiruv so‘zi bo‘sh bo‘lsa, natija chiqmasin va xabar ko‘rsating.
- Kategoriya tanlanmasa, barcha yangiliklar chiqsin.
- Qidiruv natijalari chiqmasa, test ma’lumotlar borligini tekshiring.

**Yechim:**
- `python manage.py runserver` orqali serverni ishga tushiring.
- Brauzerda `http://localhost:8000/search/` sahifasiga o‘ting.
- Qidiruv so‘zini kiriting va natijalarni ko‘ring.

**Best practice:**
- Foydalanuvchi xatoliklarini alert orqali ko‘rsating.

---


## 7. Qo‘shimcha topshiriqlar, maslahatlar va holatlar

- Kategoriya bo‘yicha qidiruv qo‘shing (formaga select maydon).
- Faqat muallifga tegishli yangiliklarni qidirish.
- Qidiruv natijalarini tartiblash va cheklash.
- Bootstrap yordamida responsive dizayn yarating.
- Foydalanuvchi xatoliklarini to‘g‘ri ko‘rsating.
- Qidiruv natijalarini AJAX yordamida dinamik yuklash misolini ko‘rib chiqing.
- Qidiruvda bir nechta so‘z bo‘yicha filter qilish uchun Q() obyektidan foydalaning:
```python
from django.db.models import Q
results = News.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
```

---


## 8. Amaliy savollar va holatlar

1. Qidiruv natijalarini qanday tartiblash mumkin?
2. Qidiruvda faqat sarlavha yoki matn bo‘yicha filter qilish uchun qanday kod yoziladi?
3. Pagination’ni o‘zgartirish uchun qaysi parametrni o‘zgartirish kerak?
4. Bootstrap yordamida formani qanday chiroyli qilish mumkin?
5. Kategoriya bo‘yicha qidiruvni qanday qo‘shish mumkin?
6. AJAX yordamida qidiruv natijalarini dinamik yuklash misolini yozing.
7. Qidiruvda bir nechta so‘z bo‘yicha filter qilish uchun Q() obyektidan qanday foydalaniladi?

---

**Amaliyot yakuni:** Ushbu amaliyotdan so‘ng siz Django’da yangiliklarni izlash funksiyasini mustaqil, professional va turli holatlar uchun moslashtirib qo‘sha olasiz.
