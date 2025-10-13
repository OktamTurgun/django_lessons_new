# 📰 News Project

Django asosida yaratilgan professional yangiliklar sayti loyihasi.  
Bu loyiha orqali foydalanuvchilar yangiliklarni ko'rishlari, kategoriyalar bo'yicha saralashlari va batafsil ma'lumot olishlari mumkin.

## 🚀 Asosiy imkoniyatlar

- ✨ Yangiliklarni qo'shish, o'chirish va tahrirlash (admin panel orqali)
- 📱 Responsive (moslashuvchan) frontend dizayn
- 🗂 Kategoriyalar bo'yicha yangiliklarni saralash
- 🏠 Bosh sahifada barcha yangiliklar ko'rinishi
- 🖼 Media fayllar bilan ishlash (rasmlar)
- 📞 Aloqa formasi
- 🔍 Qidiruv imkoniyati

## 🛠 Texnologiyalar

- **Backend:** Python 3.13+, Django 5.x
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Database:** SQLite (development)
- **Media:** Image handling with Django

## ⚙️ O'rnatish va ishga tushirish

### 1. Repozitoriyani klonlash
```bash
git clone https://github.com/<username>/news-project.git
cd news-project
```

### 2. Virtual muhit yaratish
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Zarur kutubxonalarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Ma'lumotlar bazasini sozlash
```bash
python manage.py migrate
```

### 5. Superuser yaratish
```bash
python manage.py createsuperuser
```

### 6. Serverni ishga tushirish
```bash
python manage.py runserver
```

### 7. Saytni ko'rish
Brauzeringizda quyidagi manzilni oching: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Admin panel: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## 📂 Loyiha tuzilmasi

```
news-project/
├── manage.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── news_project/          # Asosiy loyiha sozlamalari
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── news_app/              # Yangiliklar ilovasi
│   ├── models.py          # Ma'lumotlar modellari
│   ├── views.py           # Ko'rinishlar
│   ├── urls.py            # URL marshrutlari
│   ├── forms.py           # Formalar
│   └── admin.py           # Admin panel sozlamalari
│
├── templates/news/        # HTML shablonlari
│   ├── base.html
│   ├── home.html
│   ├── news_detail.html
│   └── category_detail.html
│
├── static/                # Statik fayllar
│   ├── css/
│   ├── js/
│   ├── images/
│   └── fonts/
│
└── media/news/images/     # Yuklangan rasmlar
```

## 🎯 Asosiy funksiyalar

### Models
- **News** - Yangiliklar modeli
- **Category** - Kategoriyalar modeli  
- **Contact** - Aloqa so'rovlari modeli

### Views
- Bosh sahifa
- Yangilik tafsilotlari
- Kategoriya bo'yicha yangliklar
- Aloqa sahifasi

### Admin Panel
Admin panel orqali quyidagilarni boshqarish mumkin:
- Yangiliklarni qo'shish, tahrirlash, o'chirish
- Kategoriyalarni boshqarish
- Foydalanuvchi so'rovlarini ko'rish

## 🔧 Sozlash

### Media fayllar
Media fayllar `media/news/images/` papkasida saqlanadi. Production muhitida buni cloud storage (AWS S3, Cloudinary) bilan almashtirishni tavsiya qilamiz.

### Static fayllar
Development muhitida Django static fayllarni avtomatik xizmat qiladi. Production uchun `collectstatic` buyrug'ini ishga tushiring:

```bash
python manage.py collectstatic
```

## 📱 Responsive dizayn

Sayt barcha qurilmalarda (desktop, tablet, mobil) to'g'ri ishlaydi va Bootstrap framework asosida yaratilgan.

## 🤝 Hissa qo'shish

1. Fork qiling
2. Feature branch yarating (`git checkout -b feature/AmazingFeature`)
3. O'zgarishlaringizni commit qiling (`git commit -m 'Add some AmazingFeature'`)
4. Branch'ni push qiling (`git push origin feature/AmazingFeature`)
5. Pull Request oching

## 🐛 Xatoliklar haqida xabar berish

Agar xatolik topsangiz, GitHub Issues bo'limida xabar bering.

## 👨‍💻 Muallif

**Uktam Turg'unov**
- GitHub: [@OktamTurgun](https://github.com/OktamTurgun)
- Email: uktamturgunov30@gmail.com

## 📄 Litsenziya

Ushbu loyiha MIT litsenziyasi asosida tarqatiladi. Batafsil ma'lumot uchun [LICENSE](LICENSE) faylini ko'ring.

## Minnatdorchilik

- Django jamoasiga framework uchun
- Bootstrap jamoasiga UI components uchun
- Barcha open-source kutubxona mualliflariga

---

⭐ Agar loyiha sizga yoqsa, star bosishni unutmang!