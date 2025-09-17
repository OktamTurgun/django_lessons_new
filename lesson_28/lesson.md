# 28-dars: Git. Loyihani GitHub'ga yuklash

## Kirish

Bu darsda biz Git versiya nazorat tizimi bilan tanishamiz va loyihamizni GitHub'ga qanday yuklashni o'rganamiz. Git dasturchilar uchun eng muhim vositalardan biri bo'lib, kodlarimizni saqlash, o'zgarishlarni kuzatish va boshqa dasturchilar bilan hamkorlik qilish imkonini beradi.

## Git nima?

**Git** - bu distributed version control system (tarqatilgan versiya nazorat tizimi) bo'lib, kodlarnizdagi o'zgarishlarni kuzatib borish uchun ishlatiladi. U quyidagi afzalliklarga ega:

- Kodlaringizning barcha versiyalarini saqlaydi
- Bir nechta dasturchi bir loyihada ishlashi mumkin
- O'zgarishlarni qaytarish va taqqoslash imkoniyati
- Kodlarni xavfsiz saqlash

## GitHub nima?

**GitHub** - bu Git repozitoriyalarini saqlash uchun bulut xizmati. U quyidagi imkoniyatlarni taqdim etadi:

- Kodlarni onlayn saqlash
- Boshqa dasturchilar bilan hamkorlik
- Open source loyihalarda ishtirok etish
- Portfolio yaratish

## 1-qadam: Git o'rnatish

### Windows uchun:
1. [git-scm.com](https://git-scm.com) saytiga o'ting
2. "Download for Windows" tugmasini bosing
3. Yuklab olingan faylni ishga tushiring va o'rnatishni bajaring

### macOS uchun:
```bash
# Homebrew orqali
brew install git

# Yoki Xcode Command Line Tools orqali
xcode-select --install
```

### Linux (Ubuntu/Debian) uchun:
```bash
sudo apt update
sudo apt install git
```

**O'rnatishni tekshirish:**
```bash
git --version
```

## 2-qadam: Git konfiguratsiyasi

Git'ni birinchi marta ishlatishdan oldin, o'zingiz haqingizda ma'lumot berishing kerak:

```bash
# Ismingizni o'rnatish
git config --global user.name "Sizning Ismingiz"

# Email manzilingizni o'rnatish
git config --global user.email "sizning-email@example.com"

# Konfiguratsiyani tekshirish
git config --list
```

**Misol:**
```bash
git config --global user.name "Akmal Karimov"
git config --global user.email "akmal@example.com"
```

## 3-qadam: Loyiha papkasida Git repozitoriya yaratish

Loyiha papkangizga o'ting va Git repozitoriyasini ishga tushiring:

```bash
# Loyiha papkasiga o'tish
cd yangiliklar_sayti

# Git repozitoriyasini boshlash
git init
```

Bu yerda `.git` nomi bilan yashirin papka yaratiladi, u barcha Git ma'lumotlarini saqlaydi.

## 4-qadam: .gitignore fayl yaratish

Ba'zi fayllar va papkalarni Git'ga qo'shmaslik kerak. Buning uchun `.gitignore` fayl yaratamiz:

```bash
# .gitignore fayl yaratish
touch .gitignore
```

**.gitignore** fayl mazmuni:
```gitignore
# Django
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Secret keys
.env
secrets.json

# Static files (development)
staticfiles/
```

**Izoh:** Bu fayl Django loyihasi uchun standart .gitignore shablon hisoblanadi.

## 5-qadam: Fayllarni qo'shish va commit qilish

```bash
# Barcha fayllarni qo'shish
git add .

# Yoki alohida fayl qo'shish
git add manage.py

# Holat tekshirish
git status

# Commit qilish
git commit -m "Initial commit: Django loyihasi yaratildi"
```

**Git add tushuntirish:**
- `git add .` - barcha o'zgargan fayllarni staging area'ga qo'shadi
- `git add fayl_nomi` - ma'lum bir faylni qo'shadi
- `git add *.py` - barcha Python fayllarini qo'shadi

**Commit message yozish qoidalari:**
- Qisqa va aniq bo'lsin (50 belgidan kam)
- Imperativ formada yozing ("Added" emas, "Add" deb yozing)
- O'zbekcha yoki inglizcha ishlatishingiz mumkin

```bash
# Yaxshi commit message'lar:
git commit -m "Add news model"
git commit -m "Fix contact form validation"
git commit -m "Yangilik sahifasi yaratildi"

# Yomon commit message'lar:
git commit -m "changes"
git commit -m "bug fix"
git commit -m "asdasd"
```

## 6-qadam: GitHub'da yangi repozitoriya yaratish

1. [GitHub.com](https://github.com) saytiga o'ting
2. Ro'yxatdan o'ting (agar hisobingiz bo'lmasa)
3. "New" yoki "+" belgisini bosing
4. "New repository" tanlang
5. Repository ma'lumotlarini kiriting:
   - **Repository name**: `yangiliklar-sayti`
   - **Description**: "Django bilan yaratilgan yangiliklar sayti"
   - **Public** yoki **Private** tanlang
   - "Create repository" tugmasini bosing

## 7-qadam: Local repozitoriyani GitHub'ga ulash

GitHub yangi repozitoriya yaratganingizdan keyin, sizga quyidagi kodlarni beradi:

```bash
# Remote repository qo'shish
git remote add origin https://github.com/sizning-username/yangiliklar-sayti.git

# Branch nomini o'rnatish (zamonaviy GitHub main ishlatadi)
git branch -M main

# Kodlarni GitHub'ga yuklash
git push -u origin main
```

**Misol:**
```bash
git remote add origin https://github.com/akmalkarimov/yangiliklar-sayti.git
git branch -M main
git push -u origin main
```

## 8-qadam: Keyingi o'zgarishlarni yuklash

Loyihangizda o'zgarish qilganingizdan keyin, uni GitHub'ga yuklash:

```bash
# O'zgarishlarni ko'rish
git status

# Fayllarni qo'shish
git add .

# Commit qilish
git commit -m "Contact form validatsiyasi qo'shildi"

# GitHub'ga yuklash
git push
```

## Asosiy Git buyruqlari

### Repository boshqaruvi
```bash
# Yangi repozitoriya yaratish
git init

# Mavjud repozitoriyani klonlash
git clone https://github.com/username/repository.git

# Remote repository ma'lumotini ko'rish
git remote -v
```

### Fayllar bilan ishlash
```bash
# Holat ko'rish
git status

# Fayllarni staging area'ga qo'shish
git add filename.txt
git add .
git add *.py

# Faylni staging area'dan olib tashlash
git reset filename.txt

# O'zgarishlarni commit qilish
git commit -m "Commit message"
```

### Tarix va o'zgarishlar
```bash
# Commit tarixini ko'rish
git log
git log --oneline

# Fayldagi o'zgarishlarni ko'rish
git diff filename.txt

# Oxirgi commit bilan taqqoslash
git diff HEAD filename.txt
```

### Branch'lar bilan ishlash
```bash
# Branch'larni ko'rish
git branch

# Yangi branch yaratish
git branch feature-branch

# Branch'ga o'tish
git checkout feature-branch

# Yangi branch yaratish va unga o'tish
git checkout -b feature-branch

# Branch'ni o'chirish
git branch -d feature-branch
```

### Remote repository bilan ishlash
```bash
# O'zgarishlarni yuklash
git push

# O'zgarishlarni olish
git pull

# Remote repository qo'shish
git remote add origin URL
```

## Amaliy misol: Yangilik qo'shish

Loyihangizga yangi funksiya qo'shayotganingizni tasavvur qiling:

```bash
# 1. Yangi branch yaratish
git checkout -b yangi-funksiya

# 2. Kodlarda o'zgarish qilish
# models.py, views.py, templates'larni o'zgartirish

# 3. O'zgarishlarni ko'rish
git status

# 4. Fayllarni qo'shish
git add models.py views.py templates/

# 5. Commit qilish
git commit -m "Yangilik kategoriyalari qo'shildi"

# 6. Main branch'ga o'tish
git checkout main

# 7. O'zgarishlarni merge qilish
git merge yangi-funksiya

# 8. GitHub'ga yuklash
git push

# 9. Ishlatilmagan branch'ni o'chirish
git branch -d yangi-funksiya
```

## Xatolarni tuzatish

### Commit message'ni o'zgartirish
```bash
# Oxirgi commit message'ni o'zgartirish
git commit --amend -m "Yangi commit message"
```

### Faylni commit'dan olib tashlash
```bash
# Faylni oxirgi commit'dan olib tashlash
git reset HEAD~1 filename.txt
```

### O'zgarishlarni bekor qilish
```bash
# Fayldagi o'zgarishlarni bekor qilish
git checkout -- filename.txt

# Barcha o'zgarishlarni bekor qilish
git checkout -- .
```

## Xavfsizlik masalalari

### SSH kalitlari sozlash (tavsiya etiladi)

HTTPS o'rniga SSH ishlatish xavfsizroq:

```bash
# SSH kalit yaratish
ssh-keygen -t rsa -b 4096 -C "sizning-email@example.com"

# SSH kalitni clipboard'ga ko'chirish
cat ~/.ssh/id_rsa.pub
```

Kalitni GitHub Settings > SSH and GPG keys bo'limiga qo'shing.

### Personal Access Token

Agar HTTPS ishlatayotgan bo'lsangiz, GitHub parolingiz o'rniga Personal Access Token ishlatishingiz kerak:

1. GitHub Settings > Developer settings > Personal access tokens
2. "Generate new token" tugmasini bosing
3. Token ma'lumotlarini kiriting
4. "Generate token" tugmasini bosing
5. Tokenni xavfsiz joyda saqlang

## Best Practices (Eng yaxshi amaliyotlar)

### 1. Commit message yozish qoidalari
```bash
# Yaxshi misollar:
git commit -m "Add user authentication"
git commit -m "Fix email validation in contact form"
git commit -m "Update Django to version 4.2"

# Yomon misollar:
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

### 2. Kichik va ma'noli commit'lar qiling
Bir commit'da faqat bir xil turdagi o'zgarishlarni qiling:

```bash
# Yaxshi:
git commit -m "Add News model"
git commit -m "Add News admin configuration"

# Yomon:
git commit -m "Add News model, fix contact form, update templates"
```

### 3. .gitignore faylini to'g'ri sozlang
Quyidagi fayllarni hech qachon Git'ga qo'shmang:
- Parollar va secret key'lar
- Database fayllari
- Virtual environment
- IDE konfiguratsiya fayllari
- Log fayllari

### 4. Branch'lardan foydalaning
```bash
# Har bir yangi funksiya uchun alohida branch yarating
git checkout -b contact-form
git checkout -b news-pagination
git checkout -b user-profile
```

### 5. Muntazam ravishda push qiling
```bash
# Har kuni oxirida yoki muhim o'zgarishdan keyin
git push
```

## Maslahatlar

1. **Git GUI ishlatishingiz mumkin**: GitKraken, SourceTree kabi dasturlar Git'ni vizual ko'rinishda boshqarish imkonini beradi.

2. **Commit'dan oldin doim tekshiring**: `git status` va `git diff` buyruqlarini ishlating.

3. **README.md fayl yarating**: Loyiha haqida ma'lumot beruvchi fayl yarating.

4. **GitHub Issues ishlatish**: Muammolarni va yangi funksiyalarni GitHub Issues orqali boshqaring.

5. **Pull Request'lardan foydalaning**: Katta loyihalarda o'zgarishlarni Pull Request orqali kiritish yaxshi amaliyot.

6. **Git hook'lardan foydalaning**: Avtomatik test va deploy uchun Git hook'larni sozlang.

## Xulosa

Git va GitHub zamonaviy dasturlashda ajralmas qism hisoblanadi. Bu darsda biz quyidagilarni o'rgandik:

- Git nima va nima uchun kerak
- Git'ni o'rnatish va sozlash
- Asosiy Git buyruqlari
- GitHub bilan ishlash
- Loyihani GitHub'ga yuklash jarayoni
- Best practice'lar va maslahatlar

Keyingi darslarimizda biz yangiliklar sayti loyihamizni rivojlantirishda davom etamiz va Git'dan foydalanib o'zgarishlarni kuzatib boramiz.

## Qo'shimcha materiallar

- [Git rasmiy dokumentatsiyasi](https://git-scm.com/doc)
- [GitHub Learning Lab](https://lab.github.com/)
- [Atlassian Git tutorials](https://www.atlassian.com/git/tutorials)
- [Pro Git kitob](https://git-scm.com/book) - bepul onlayn kitob