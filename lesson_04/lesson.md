# Lesson 04: Virtual muhitlar bilan tanishish. Pipenv o'rnatish va sozlash

## Maqsad
Ushbu darsning maqsadi — Python loyihalarida virtual muhit (virtual environment) tushunchasini tushunish va `Pipenv` yordamida uni yaratish, boshqarish va sozlashni o’rganish.

---

## 1. Nima uchun virtual muhit kerak?

Python loyihalarida turli kutubxonalar va ularning versiyalari bir-biriga ta’sir qilmasligi uchun virtual muhitlar ishlatiladi.

**Masalan:**
```bash
project1/venv/
project2/venv/
```
Har bir loyiha o‘zining bog‘liq paketlarini o‘rnatadi va boshqa loyihalarga ta’sir qilmaydi.

---

## 2. Virtual muhitlarni boshqarish usullari

Pythonda virtual muhit yaratish uchun bir nechta usullar mavjud:

### 2.1 `venv` (standart kutubxona)
```bash
python -m venv venv
```

### 2.2 `virtualenv` (ko‘p qo‘shimcha imkoniyatlar)
```bash
pip install virtualenv
virtualenv venv
```

### 2.3 `Pipenv` (virtual muhit + dependency management)
```bash
pip install pipenv
```
> Ushbu dars davomida **Pipenv** bilan ishlaymiz.

---

## 3. Pipenv o'rnatish

Terminalda quyidagi buyruqni bajaring:
```bash
pip install pipenv
```

O‘rnatilganini tekshirish:
```bash
pipenv --version
```

---

## 4. Loyihada Pipenv yordamida virtual muhit yaratish

Loyihaning asosiy papkasiga kiring:
```bash
cd my_project
```

### 4.1 Virtual muhitni yaratish
```bash
pipenv install
```
- Bu buyruq **Pipfile** yaratadi (agar yo‘q bo‘lsa) va virtual muhit hosil qiladi.

### 4.2 Paket o‘rnatish
```bash
pipenv install requests
```
- `requests` paketi virtual muhitga o‘rnatiladi.
- **Pipfile** va **Pipfile.lock** avtomatik yangilanadi.

### 4.3 Virtual muhitga kirish
```bash
pipenv shell
```
- Terminal endi virtual muhitda ishlaydi.
- Chiqarish: `exit` buyrug‘i bilan.

---

## 5. Pipenv bilan loyihani boshqarish

### 5.1 Paketlarni ko‘rish
```bash
pipenv graph
```

### 5.2 Paketni olib tashlash
```bash
pipenv uninstall requests
```

### 5.3 Loyihani boshqa kompyuterga ko‘chirish
```bash
pipenv install --dev
```
- Bu **Pipfile.lock** asosida barcha paketlarni o‘rnatadi.

---

## 6. Amaliy maslahatlar
- **Har doim** loyiha boshlashdan oldin `pipenv shell` orqali virtual muhitga kiring.
- **Pipfile** va **Pipfile.lock** fayllarini GitHub ga qo‘shing, virtual muhit papkasini emas (`venv/`).
- **Pipenv** Python versiyasini ham boshqarishi mumkin:
```bash
pipenv --python 3.11
```

---

## Xulosa
- Virtual muhitlar Python loyihalarini toza va tartibli qiladi.
- Pipenv yordamida virtual muhit yaratish, paketlarni boshqarish va dependency’larni izchil saqlash oson.
