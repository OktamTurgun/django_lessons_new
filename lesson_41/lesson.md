# Lesson 41: Ruxsatnomalar. LoginRequiredMixin vs UserPassesTestMixin

## Maqsad:
Ushbu darsda Django'da ruxsatnomalar (permissions) bilan ishlash, xususan, `LoginRequiredMixin` va `UserPassesTestMixin` mixinlari yordamida sahifalarga kirishni cheklashni o'rganamiz. Dars davomida har bir mixinning vazifasi, ishlatilishi, kod misollari va ularni birga ishlatish usullari ko'rsatiladi. Har bir bosqichda kodlar izohlanadi va yakunda foydali maslahatlar, best practice'lar bilan dars yakunlanadi.

## 1. Kirish: Ruxsatnomalar va Mixins

Django'da ruxsatnomalar yordamida foydalanuvchilarning sahifalarga yoki funksiyalarga kirishini cheklash mumkin. Buning uchun mixinlardan foydalaniladi:

- **LoginRequiredMixin** — faqat login qilgan foydalanuvchilar uchun sahifani ochadi.
- **UserPassesTestMixin** — foydalanuvchi maxsus shartga javob bersagina sahifani ochadi.

## 2. LoginRequiredMixin bilan ishlash

### 2.1. Nazariya

`LoginRequiredMixin` yordamida faqat tizimga kirgan (login qilgan) foydalanuvchilarga sahifani ko'rsatish mumkin.

### 2.2. Kod misoli

```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Post

class PostListView(LoginRequiredMixin, ListView):
  model = Post
  template_name = 'posts/post_list.html'
  context_object_name = 'posts'
```

**Izoh:** Agar foydalanuvchi login qilmagan bo'lsa, uni avtomatik ravishda login sahifasiga yo'naltiradi.

### 2.3. Sozlamalar

`settings.py` faylida quyidagilar bo'lishi kerak:

```python
LOGIN_URL = '/login/'
```

Bu login qilmagan foydalanuvchilar qaysi sahifaga yo'naltirilishini belgilaydi.

## 3. UserPassesTestMixin bilan ishlash

### 3.1. Nazariya

`UserPassesTestMixin` yordamida foydalanuvchi maxsus shartga javob bersagina sahifani ko'rsatish mumkin. Masalan, faqat adminlar yoki post muallifi ko'ra oladi.

### 3.2. Kod misoli

```python
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import UpdateView
from .models import Post

class PostUpdateView(UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['title', 'content']
  template_name = 'posts/post_form.html'

  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
```

**Izoh:** `test_func` metodi orqali shart yoziladi. Bu misolda faqat post muallifi postni tahrirlashi mumkin.

## 4. Ikkala mixinni birga ishlatish

Ko'pincha, foydalanuvchi login qilgan va shartga javob berishi kerak bo'ladi. Bunda ikkala mixinni birga ishlatamiz:

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from .models import Post

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = 'posts/post_confirm_delete.html'
  success_url = '/'

  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
```

**Muhim:** Mixinlar har doim chapdan o'ngga ishlaydi, ya'ni avval `LoginRequiredMixin`, keyin `UserPassesTestMixin`.

## 5. Amaliy misol: Foydalanuvchi o'z postini tahrirlashi va o'chirishi

### 5.1. Model

```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
  title = models.CharField(max_length=100)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
```

### 5.2. Viewlar

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from .models import Post

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
  model = Post
  fields = ['title', 'content']
  template_name = 'posts/post_form.html'

  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
  model = Post
  template_name = 'posts/post_confirm_delete.html'
  success_url = '/'

  def test_func(self):
    post = self.get_object()
    return self.request.user == post.author
```

### 5.3. URLlar

```python
from django.urls import path
from .views import PostUpdateView, PostDeleteView

urlpatterns = [
  path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
  path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
```

## 6. Maslahatlar va Best Practices

- Mixinlarni har doim chapdan o'ngga to'g'ri tartibda yozing: avval `LoginRequiredMixin`, keyin `UserPassesTestMixin`.
- `test_func` metodida aniq va xavfsiz shartlar yozing.
- Ruxsatnomalarni har doim view darajasida tekshiring, shunda foydalanuvchi URL orqali kirishga harakat qilsa ham, ruxsat bo'lmasa, kirita olmaysiz.
- `get_login_url()` va `get_permission_denied_message()` metodlarini override qilib, foydalanuvchiga aniq xabarlar ko'rsatishingiz mumkin.
- Kodni DRY (Don't Repeat Yourself) tamoyiliga amal qilib yozing.

---
## 7. Qo'shimcha: Funksional viewlarda ruxsatlarni tekshirish

Agar klass-based view emas, funksional view ishlatsangiz, quyidagi dekoratorlardan foydalanishingiz mumkin:

```python
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required(login_url='/login/')
def my_view(request):
  # Faqat login qilgan foydalanuvchi kiradi
  ...

def is_author(user):
  return user.is_superuser

@user_passes_test(is_author, login_url='/login/')
def admin_view(request):
  # Faqat adminlar kiradi
  ...
```

## 8. UserPassesTestMixin uchun kengroq misollar

`UserPassesTestMixin` yordamida turli shartlarni tekshirishingiz mumkin:

- Foydalanuvchi guruh a'zosi bo'lishi kerak:
  ```python
  def test_func(self):
    return self.request.user.groups.filter(name='moderator').exists()
  ```
- Foydalanuvchi emaili tasdiqlangan bo'lishi kerak:
  ```python
  def test_func(self):
    return self.request.user.is_authenticated and self.request.user.email
  ```

## 9. Ruxsatnoma xatolari va foydalanuvchiga xabar berish

Agar foydalanuvchi ruxsatga ega bo'lmasa, unga maxsus xabar ko'rsatish uchun `get_permission_denied_message` metodini override qilishingiz mumkin:

```python
class MyView(LoginRequiredMixin, UserPassesTestMixin, View):
  ...
  def get_permission_denied_message(self):
    return "Sizda ushbu amal uchun ruxsat yo'q."
```

## 10. Testlar yozish

Ruxsatnomalar to'g'ri ishlashini tekshirish uchun test yozish muhim:

```python
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class PostPermissionTests(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(username='user1', password='pass')
    self.other_user = User.objects.create_user(username='user2', password='pass')
    # Post yaratish va h.k.

  def test_only_author_can_edit(self):
    self.client.login(username='user2', password='pass')
    response = self.client.get(reverse('post_edit', args=[1]))
    self.assertEqual(response.status_code, 403)
```

## 11. Xatoliklarni oldini olish uchun maslahatlar

- Har doim mixinlar tartibiga e'tibor bering.
- `test_func` metodida faqatgina `True` yoki `False` qaytaring.
- Ruxsatnoma xatolarini foydalanuvchiga tushunarli qilib ko'rsating.
- Kodni qisqa va aniq yozing, DRY tamoyiliga amal qiling.

---

**Mukammal dars uchun tavsiya:**  
Darslik yangi o'rganuvchilar uchun yetarlicha asosiy tushunchalarni beradi. Lekin, funksional viewlar uchun misollar, kengroq testlar, foydalanuvchiga xabar berish, va real hayotdan kengroq misollar qo'shilsa, darslik yanada mukammal va amaliy bo'ladi. Har bir kod misoliga qisqa izoh va kengaytirilgan variantlar berish, xatoliklarni oldini olish uchun maslahatlar yozish ham foydali.

---

**Keyingi o'qish uchun:**  
- Django rasmiy hujjatlarida [authentication and authorization](https://docs.djangoproject.com/en/4.2/topics/auth/default/) bo'limini o'qing.
- [Django permissions](https://docs.djangoproject.com/en/4.2/topics/auth/default/#permissions-and-authorization) haqida chuqurroq o'rganing.
- Django REST Framework uchun ruxsatnomalar: [DRF permissions](https://www.django-rest-framework.org/api-guide/permissions/)

**Xulosa:** Ushbu darsda Django'da ruxsatnomalar bilan ishlash, `LoginRequiredMixin` va `UserPassesTestMixin` yordamida sahifalarga kirishni cheklash, kod misollari va best practice'larni o'rgandingiz. Amaliyotda ushbu mixinlardan to'g'ri foydalanish xavfsizlik va qulaylik uchun juda muhim.

**Keyingi dars:**
42-darsda Ruxsatnomalar. Admin sahifasini ochish, Decoratorli ruxsatnomalar.