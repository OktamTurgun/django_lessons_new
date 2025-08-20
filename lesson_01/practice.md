# Practice_01: Django versiyalari bilan ishlash

Bu amaliy mashqda biz **virtual environment yaratish**, **turli Django versiyalarini o‘rnatish** va **versiyani tekshirish** qadamlarini bajaramiz.

---

## 1. Virtual environment yaratish

Avvalo loyihamiz uchun alohida muhit (virtual environment) yarataylik:

```bash
python -m venv venv
➡️ Bu buyruq venv nomli virtual environment yaratadi.

Faollashtirish:

Windows:

```bash

venv\Scripts\activate
```
Mac/Linux:

```bash

source venv/bin/activate
```
### 👉 Muhim: Terminalda (venv) belgisi chiqsa, virtual environment muvaffaqiyatli faollashgan.

## 2. Django eski versiyasini o‘rnatish
Misol uchun, barqaror ishlatiladigan Django 4.2 versiyasini o‘rnatamiz:

```bash

pip install django==4.2
```
## 3. Django yangi versiyasini o‘rnatish
Endi yangiroq Django versiyasini o‘rnatib ko‘ramiz (masalan, 5.0.2):

```bash

pip install django==5.0.2
```
### - Bu orqali siz eski va yangi versiyalarni solishtirib ko‘rishingiz mumkin.

## 4. Django versiyasini tekshirish
O‘rnatilgan versiyani tekshirish uchun:

```bash

python -m django --version
```
 - Natijada terminalda hozirgi Django versiyasi chiqadi (masalan, 5.0.2).

## 5. Muhim qo‘shimcha buyruqlar
Django’ni yangilash:

```bash

pip install --upgrade django
```
Django’ni o‘chirish:

```bash

pip uninstall django
```
### Xulosa
 - Amaliy mashq davomida siz:

- **Virtual environment yaratishni,**

- **Django’ning eski va yangi versiyalarini o‘rnatishni,**

- **Django versiyasini tekshirishni o‘rgandingiz.**

- **Endi siz turli loyihalarda turli versiyalar bilan mustaqil ishlashingiz mumkin.** 
