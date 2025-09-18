
# 29-dars: Yangiliklarni tahrirlash va o'chirish funksiyalari

## Dars maqsadi
Ushbu darsda biz yangiliklarni tahrirlash (update) va o'chirish (delete) funksiyalarini Django’da **class-based views** yordamida to‘liq va zamonaviy usulda qo‘shamiz. Amaliy misollar, kodlar, template va URL’lar bilan to‘liq o‘rganamiz.

## Nazariy qism

### CRUD operatsiyalari
Django’da CRUD (Create, Read, Update, Delete) operatsiyalari har bir web loyihaning asosi hisoblanadi. Bugun biz **Update** va **Delete** funksiyalarini class-based views yordamida o‘rganamiz.

### Class-based views
- **UpdateView** — obyektni tahrirlash uchun
- **DeleteView** — obyektni o‘chirish uchun

### URL routing
Har bir view uchun URL yo‘li yaratiladi. Bu `urls.py` faylida amalga oshiriladi.

## Amaliy qism

### 1-bosqich: URLs.py fayllarini yaratish

**news/urls.py:**
```python
from django.urls import path
from .views import NewsUpdateView, NewsDeleteView

urlpatterns = [
	# Yangilikni tahrirlash
	path('edit/<int:pk>/', NewsUpdateView.as_view(), name='edit_news'),
	# Yangilikni o'chirish
	path('delete/<int:pk>/', NewsDeleteView.as_view(), name='delete_news'),
]
```

### 2-bosqich: View'larni yaratish

**news/views.py:**
```python
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

### 3-bosqich: Form yaratish

**news/forms.py:**
```python
from django import forms
from .models import News

class NewsForm(forms.ModelForm):
	class Meta:
		model = News
		fields = ['title', 'body', 'category', 'photo']
```

### 4-bosqich: Template'lar yaratish

#### Yangilikni tahrirlash

**templates/news/edit_news.html:**
```html
{% extends 'base.html' %}
{% block title %}Yangilikni tahrirlash{% endblock %}
{% block content %}
<div class="container">
	<h2>Yangilikni tahrirlash</h2>
	<form method="post" enctype="multipart/form-data">
		{% csrf_token %}
		{{ form.as_p }}
		<button type="submit" class="btn btn-success">Saqlash</button>
		<a href="{% url 'news_detail' object.pk %}" class="btn btn-secondary">Orqaga</a>
	</form>
</div>
{% endblock %}
```

#### Yangilikni o'chirish

**templates/news/delete_news.html:**
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

#### Yangiliklar ro'yxatida tahrirlash va o'chirish tugmalari

**templates/news/news_list.html** (asosiy yangiliklar ro'yxati):
```html
<!-- ...existing code... -->
<a href="{% url 'edit_news' news.pk %}" class="btn btn-warning btn-sm">Tahrirlash</a>
<a href="{% url 'delete_news' news.pk %}" class="btn btn-danger btn-sm">O'chirish</a>
<!-- ...existing code... -->
```

### 5-bosqich: Migration va test

```bash
# Model va forma o'zgarishlari uchun migration
python manage.py makemigrations
python manage.py migrate

# Superuser yaratish (agar hali yo'q bo'lsa)
python manage.py createsuperuser

# Serverni ishga tushirish
python manage.py runserver
```

### 6-bosqich: Test ma'lumotlar qo'shish
Admin panelga kirib, test uchun bir nechta yangilik qo'shing va tahrirlash/o'chirishni sinab ko'ring.

## Xulosa

Ushbu darsda siz Django’da yangiliklarni tahrirlash va o‘chirish funksiyalarini **class-based views** yordamida to‘liq o‘rganib oldingiz. Kodlar, template’lar va URL’lar misolida amaliyot qilindi.

### Muhim tushunchalar:
- **UpdateView** va **DeleteView**
- **ModelForm** bilan ishlash
- **URL routing**
- **Template inheritance**
- **CRUD operatsiyalari**

### Keyingi qadamlar:
1. Tahrirlash va o'chirish funksiyalarini foydalanuvchi huquqlari bilan cheklash
2. Xatoliklarni va validatsiyani yaxshilash
3. AJAX yordamida dinamik tahrirlash/o'chirish
4. Test yozish va kodni optimallashtirish

**Dars yakuni:** Endi siz yangiliklarni tahrirlash va o'chirish funksiyalarini professional darajada qo'sha olasiz!

