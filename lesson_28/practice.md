# 28-dars: Git va GitHub - Amaliy mashg'ulot

Bu amaliy mashg'ulotda siz o'z yangiliklar sayti loyihangizni Git bilan boshqarish va GitHub'ga yuklashni amalda o'rganasiz.

## Vazifa 1: Git o'rnatish va sozlash

### 1.1. Git o'rnatilganligini tekshirish
Terminal/Command Prompt'ni oching va quyidagi buyruqni yozing:

```bash
git --version
```

**Kutilgan natija:** Git versiya raqami ko'rsatilishi kerak (masalan: `git version 2.39.1`)

Agar Git o'rnatilmagan bo'lsa, [git-scm.com](https://git-scm.com) saytidan yuklab oling.

### 1.2. Git konfiguratsiyasi
```bash
# O'zingizning haqiqiy ismingizni yozing
git config --global user.name "Sizning Ismingiz"

# O'zingizning email manzilingizni yozing
git config --global user.email "sizning.email@gmail.com"

# Sozlamalarni tekshirish
git config --list
```

**Misollar:**
```bash
git config --global user.name "Akmal Karimov"
git config --global user.email "akmal.karimov@gmail.com"
```

## Vazifa 2: Loyiha uchun Git repozitoriyasi yaratish

### 2.1. Loyiha papkasiga o'tish
```bash
# Yangiliklar sayti loyihasi papkasiga o'ting
cd /path/to/yangiliklar_sayti

# Yoki Windows'da:
cd C:\Users\Username\yangiliklar_sayti
```

### 2.2. Git repozitoriyasi boshlash
```bash
# Git repozitoriyasini boshlash
git init

# Natijani tekshirish
ls -la  # Linux/Mac uchun
dir /a  # Windows uchun
```

**Kutilgan natija:** `.git` papkasi yaratilgan bo'lishi kerak.

### 2.3. .gitignore fayl yaratish
`.gitignore` fayl yarating va quyidagi mazmunni yozing:

```gitignore
# Django
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
db.sqlite3-journal
media/uploaded_files/

# Virtual Environment
venv/
env/
ENV/
myenv/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Secret keys va environment o'zgaruvchilar
.env
secrets.json

# Static files
staticfiles/
static_root/

# Migrations (ixtiyoriy - ba'zan migration'larni saqlash kerak)
# */migrations/*.py
# !*/migrations/__init__.py
```

## Vazifa 3: Birinchi commit

### 3.1. Loyiha holati tekshirish
```bash
git status
```

**Izoh:** Qizil rangda ko'rsatilgan fayllar hali Git'ga qo'shilmagan fayllar.

### 3.2. Fayllarni staging area'ga qo'shish
```bash
# Barcha fayllarni qo'shish
git add .

# Holat tekshirish
git status
```

**Kutilgan natija:** Yashil rangda fayllar ko'rsatilishi kerak.

### 3.3. Birinchi commit
```bash
git commit -m "Initial commit: Django yangiliklar sayti loyihasi"
```

### 3.4. Commit tarixini ko'rish
```bash
git log --oneline
```

## Vazifa 4: GitHub'da repozitoriya yaratish

### 4.1. GitHub'ga kirish
1. [GitHub.com](https://github.com) saytiga o'ting
2. Akkauntingizga kiring (yo'q bo'lsa ro'yxatdan o'ting)

### 4.2. Yangi repozitoriya yaratish
1. "+" belgisini bosing (yuqori o'ng burchakda)
2. "New repository" tanlang
3. Quyidagi ma'lumotlarni kiriting:
   - **Repository name:** `yangiliklar-sayti`
   - **Description:** `Django bilan yaratilgan yangiliklar sayti loyihasi`
   - **Public** yoki **Private** tanlang
   - **Initialize this repository with** qismlarni bo'sh qoldiring (README, .gitignore, license)
4. "Create repository" tugmasini bosing

## Vazifa 5: Local repozitoriyani GitHub'ga ulash

GitHub yangi repozitoriya sahifasida bergan kodlarni ishlating:

### 5.1. Remote origin qo'shish
```bash
# GitHub'dan olgan URL'ni qo'ying
git remote add origin https://github.com/SIZNING_USERNAME/yangiliklar-sayti.git

# Remote'ni tekshirish
git remote -v
```

**Misol:**
```bash
git remote add origin https://github.com/akmalkarimov/yangiliklar-sayti.git
```

### 5.2. Main branch yaratish va yuklash
```bash
# Branch nomini main qilish
git branch -M main

# GitHub'ga yuklash
git push -u origin main
```

**Kutilgan natija:** GitHub'da loyiha kodlari ko'rinishi kerak.

## Vazifa 6: Yangi o'zgarish kiritish va yuklash

### 6.1. README.md fayl yaratish
Loyiha papkasida `README.md` fayl yarating va quyidagi mazmunni yozing:

```markdown
# Yangiliklar Sayti

Django framework yordamida yaratilgan yangiliklar sayti loyihasi.

## Loyiha haqida

Bu loyiha Django web framework'i yordamida yaratilgan to'liq funksional yangiliklar sayti hisoblanadi.

## Xususiyatlar

- Yangiliklar ro'yxati
- Yangilik detali sahifasi
- Kategoriyalar bo'yicha filterlash
- Contact forma
- Admin panel

## O'rnatish

1. Virtual muhit yaratish:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Kerakli paketlarni o'rnatish:
```bash
pip install -r requirements.txt
```

3. Database migration:
```bash
python manage.py migrate
```

4. Serverni ishga tushirish:
```bash
python manage.py runserver
```

## Texnologiyalar

- Python 3.x
- Django 4.x
- SQLite
- Bootstrap 5
- HTML/CSS/JavaScript

## Muallif

Sizning ismingiz
```

### 6.2. O'zgarishlarni commit qilish
```bash
# Holat tekshirish
git status

# README.md faylini qo'shish
git add README.md

# Commit qilish
git commit -m "Add README.md with project information"

# GitHub'ga yuklash
git push
```

## Vazifa 7: Model'larda o'zgarish va commit

### 7.1. News model'iga slug field qo'shish
`news/models.py` faylini oching va News model'ini o'zgartiring:

```python
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # Yangi qo'shildi
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):  # Yangi qo'shildi
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):  # Yangi qo'shildi
        return reverse('news_detail', args=[self.slug])
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
```

### 7.2. Migration yaratish
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7.3. O'zgarishlarni commit qilish
```bash
# O'zgargan fayllarni ko'rish
git status

# O'zgarishlarni batafsil ko'rish
git diff news/models.py

# Fayllarni qo'shish
git add news/models.py
git add */migrations/

# Commit qilish
git commit -m "Add slug field to News model with auto-generation"

# GitHub'ga yuklash
git push
```

## Vazifa 8: Branch bilan ishlash

### 8.1. Feature branch yaratish
```bash
# Yangi branch yaratish va unga o'tish
git checkout -b contact-form-improvement

# Branch'larni ko'rish
git branch
```

### 8.2. Contact form'ni yaxshilash
`news/forms.py` faylini oching va quyidagi o'zgarishni qiling:

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ismingizni kiriting'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email manzilingizni kiriting'
        })
    )
    subject = forms.CharField(  # Yangi field
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xabar mavzusi'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Xabaringizni yozing'
        })
    )
    
    def clean_name(self):  # Yangi validation
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError("Ism kamida 2 ta belgidan iborat bo'lishi kerak")
        return name
```

### 8.3. Branch'dagi o'zgarishni commit qilish
```bash
git add news/forms.py
git commit -m "Improve contact form: add subject field and name validation"
```

### 8.4. Main branch'ga merge qilish
```bash
# Main branch'ga o'tish
git checkout main

# Feature branch'ni merge qilish
git merge contact-form-improvement

# Feature branch'ni o'chirish
git branch -d contact-form-improvement

# GitHub'ga yuklash
git push
```

## Vazifa 9: Git log va diff bilan ishlash

### 9.1. Commit tarixini ko'rish
```bash
# Barcha commit'lar
git log

# Qisqa format
git log --oneline

# Oxirgi 3 ta commit
git log --oneline -3

# Statistika bilan
git log --stat
```

### 9.2. O'zgarishlarni taqqoslash
```bash
# Oxirgi commit bilan hozirgi holat
git diff HEAD

# Ikki commit orasidagi farq
git diff HEAD~2 HEAD

# Ma'lum fayl uchun
git diff HEAD~1 HEAD news/models.py
```

## Vazifa 10: GitHub'da loyiha ko'rinishini yaxshilash

### 10.1. Requirements.txt yaratish
```bash
# Virtual muhitdagi paketlar ro'yxati
pip freeze > requirements.txt

# Faylni qo'shish
git add requirements.txt
git commit -m "Add requirements.txt file"
git push
```

### 10.2. .github papka yaratish
Loyiha ildizida `.github` papka yarating va ichiga `PULL_REQUEST_TEMPLATE.md` fayl:

```markdown
## Pull Request tavsifi

Bu PR quyidagilarni amalga oshiradi:

- [ ] Yangi funksiya qo'shish
- [ ] Bug fix
- [ ] Documentation yangilash
- [ ] Code refactoring

## O'zgarishlar ro'yxati

- 
- 
- 

## Test qilish

- [ ] Unit testlar o'tdi
- [ ] Manual test qilindi
- [ ] Cross-browser test

## Screenshot (agar kerak bo'lsa)

## Qo'shimcha izohlar
```

```bash
git add .github/
git commit -m "Add GitHub templates"
git push
```

## Vazifa 11: Xato holatlarni simulation qilish va tuzatish

### 11.1. Xato commit yasash
Biror faylni o'zgartirib, xato commit message bilan commit qiling:

```bash
git add .
git commit -m "fix"  # Yomon commit message
```

### 11.2. Commit message'ni tuzatish
```bash
git commit --amend -m "Fix contact form subject field display issue"
```

### 11.3. Faylni commit'dan olib tashlash
```bash
# Agar biror faylni noto'g'ri commit qilgan bo'lsangiz
git reset HEAD~1 filename.txt
```

## Bonus Vazifa: GitHub SSH kalitlari

### SSH kalit yaratish (Linux/Mac)
```bash
ssh-keygen -t ed25519 -C "sizning-email@example.com"

# Kalitni clipboard'ga ko'chirish
cat ~/.ssh/id_ed25519.pub
```

### Windows uchun
```bash
ssh-keygen -t ed25519 -C "sizning-email@example.com"

# Kalitni ko'rish
type C:\Users\username\.ssh\id_ed25519.pub
```

1. GitHub Settings > SSH and GPG keys > New SSH key
2. Kalitni qo'shish
3. Remote URL'ni HTTPS'dan SSH'ga o'zgartirish:

```bash
git remote set-url origin git@github.com:username/yangiliklar-sayti.git
```

## Tekshiruv va Baholash

### ✅ Tekshiruv ro'yxati

Quyidagi barcha vazifalarni bajarganingizni tekshiring:

- [ ] Git o'rnatildi va sozlandi
- [ ] Local Git repozitoriya yaratildi
- [ ] .gitignore fayl yaratildi va to'g'ri sozlandi
- [ ] GitHub'da repozitoriya yaratildi
- [ ] Local repozitoriya GitHub'ga ulandi
- [ ] Kamida 5 ta meaningful commit qilindi
- [ ] README.md fayl yaratildi
- [ ] Branch yaratildi va merge qilindi
- [ ] Git log va diff buyruqlari ishlatildi
- [ ] Requirements.txt yaratildi

### 🎯 Yakuniy natija

Muvaffaqiyatli bajargan bo'lsangiz, sizda quyidagilar bo'lishi kerak:

1. **GitHub'dagi repozitoriya:**
   - Barcha loyiha fayllari
   - README.md fayl bilan
   - Kamida 5-6 ta commit tarixi
   - To'g'ri .gitignore fayl

2. **Local kompyuter:**
   - Git bilan sozlangan loyiha
   - Commit tarixi
   - Remote origin GitHub'ga ulangan

## Keng tarqalgan xatolar va ularni tuzatish

### ❌ Xato 1: "fatal: not a git repository"
**Sabab:** Git repozitoriya yaratilmagan
**Yechim:**
```bash
git init
```

### ❌ Xato 2: "Author identity unknown"
**Sabab:** Git user ma'lumotlari sozlanmagan
**Yechim:**
```bash
git config --global user.name "Ismingiz"
git config --global user.email "email@example.com"
```

### ❌ Xato 3: "remote origin already exists"
**Sabab:** Origin allaqachon qo'shilgan
**Yechim:**
```bash
git remote rm origin
git remote add origin YOUR_GITHUB_URL
```

### ❌ Xato 4: "Authentication failed"
**Sabab:** GitHub parol yoki token noto'g'ri
**Yechim:**
- Personal Access Token yarating
- SSH kalit sozlang
- Git Credential Manager ishlatib ko'ring

### ❌ Xato 5: "Merge conflict"
**Sabab:** Bir xil faylning ikki xil versiyasi
**Yechim:**
```bash
# Conflict'li fayllarni ko'rish
git status

# Fayllarni qo'lda tahrirlash
# Conflict markerlarini (<<<<, ====, >>>>) o'chirish

# Hal qilingan fayllarni qo'shish
git add fayl_nomi.py
git commit -m "Resolve merge conflict"
```

## Qo'shimcha amaliyot vazifalari

### 💡 Vazifa A: .gitignore testlash
1. Yangi fayl yarating: `test_secret.env`
2. .gitignore'ga `.env` qo'shing
3. `git status` bilan tekshiring - fayl ko'rinmasligi kerak

### 💡 Vazifa B: Multiple files commit
1. 3 ta har xil fayl yarating
2. Har birini alohida commit qiling
3. `git log --oneline` bilan tarixni ko'ring

### 💡 Vazifa C: Commit message convention
Quyidagi formatda commit message'lar yozing:
```bash
feat: yangi funksiya qo'shish
fix: xato tuzatish  
docs: dokumentatsiya yangilash
style: kod formatlash
refactor: kod qayta yozish
test: test qo'shish
```

Misol:
```bash
git commit -m "feat: add pagination to news list"
git commit -m "fix: contact form validation error"
git commit -m "docs: update README with installation guide"
```

### 💡 Vazifa D: Tag yaratish
```bash
# Version tag yaratish
git tag -a v1.0.0 -m "First stable version"

# Tag'larni GitHub'ga yuklash
git push --tags

# Tag'larni ko'rish
git tag
```

## Loyiha rivojlantirish rejasi

Keyingi darslar uchun Git workflow:

### 🔄 Har safar kod yozishdan oldin:
```bash
git status          # Holat tekshirish
git pull            # Yangilanishlarni olish
```

### 🔄 Kod yozishdan keyin:
```bash
git add .           # Fayllarni qo'shish
git status          # Tekshirish
git commit -m "..."  # Commit
git push            # GitHub'ga yuklash
```

### 🔄 Yangi funksiya uchun:
```bash
git checkout -b feature-name    # Yangi branch
# kod yozish...
git add . && git commit -m "..." 
git checkout main              # Main'ga qaytish
git merge feature-name         # Merge
git branch -d feature-name     # Branch o'chirish
git push                       # Yuklash
```

## Homework (Uy vazifasi)

### 📝 1-vazifa: Portfolio repozitoriyasi
1. GitHub'da `mening-portfolio` nomli yangi repozitoriya yarating
2. HTML/CSS bilan oddiy portfolio sahifa yarating
3. Kamida 3 ta commit qiling
4. README.md fayl qo'shing

### 📝 2-vazifa: Git cheat sheet
O'zingiz uchun Git buyruqlari cheat sheet yarating va GitHub gist sifatida saqlang.

### 📝 3-vazifa: Open source loyihaga contribute
1. GitHub'da Django'ga oid kichik open source loyiha toping
2. Uni fork qiling
3. Kichik o'zgarish kiriting (dokumentatsiya, typo fix)
4. Pull request yuboring

### 📝 4-vazifa: Avtomatlashtirish
`.github/workflows` papka yarating va GitHub Actions yordamida oddiy CI/CD sozlang:

```yaml
# .github/workflows/django.yml
name: Django CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python 3.11
      uses: actions/setup-python@v3
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test
```

## Muvaffaqiyat mezonlari

Bu amaliyotni muvaffaqiyatli yakunlash uchun:

### ⭐ Minimal daraja (3 ball):
- Git o'rnatilgan va sozlangan
- GitHub'da repozitoriya yaratilgan
- Loyiha yuklangan va kamida 3 ta commit

### ⭐⭐ O'rta daraja (4 ball):
- Yuqoridagilar + README.md
- .gitignore to'g'ri sozlangan
- Branch yaratilgan va merge qilingan
- 5+ meaningful commit

### ⭐⭐⭐ Yuqori daraja (5 ball):
- Yuqoridagilar + SSH kalitlar sozlangan
- GitHub templates qo'shilgan
- Git hook yoki GitHub Actions qo'shilgan
- Clean commit history

## Xulosa

Bu amaliyot orqali siz:
- Git asoslarini amalda o'rgandingiz
- GitHub bilan ishlashni o'rgandingiz  
- Version control tizimining ahamiyatini tushundingiz
- Professional development workflow'ni boshladingiz

Git - bu dasturchi karrierangizda eng muhim skill'lardan biri. Uni har kuni ishlatishingiz orqali ustunlikka erishasiz.

**Keyingi dars:** Yangiliklar sayti loyihasiga CRUD amaliyotlarini qo'shish va Git bilan kuzatib borish.