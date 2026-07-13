<div align="center">

# 🏥 سامانه مدیریت بیمارستان (Hospital Management System)

### یک پروژه جامع نرم‌افزاری برای مدیریت بهتر بیماران، نوبت‌ها، پرونده‌های پزشکی و فرآیندهای درمانی 🩺💻

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![REST API](https://img.shields.io/badge/API-RESTful-orange.svg)](https://en.wikipedia.org/wiki/Representational_state_transfer)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

</div>

---

## 📖 فهرست مطالب

- [معرفی پروژه](#-معرفی-پروژه)
- [امکانات اصلی](#-امکانات-اصلی)
- [فناوری‌های استفاده شده](#-فناوری‌های-استفاده-شده)
- [ساختار پروژه](#-ساختار-پروژه)
- [نصب و راه‌اندازی](#-نصب-و-راه‌اندازی)
- [ماژول‌های سیستم](#-ماژول‌های-سیستم)
- [API Endpoints](#-api-endpoints)
- [مشارکت در پروژه](#-مشارکت-در-پروژه)
- [وضعیت پروژه](#-وضعیت-پروژه)

---

## 🏥 معرفی پروژه

این مخزن شامل کدهای مربوط به یک **سامانه مدیریت بیمارستان (HMS)** است که با هدف ساده‌سازی و دیجیتالی‌کردن فرآیندهای اصلی مرکز درمانی توسعه داده شده است. این سیستم با استفاده از **Django REST Framework** پیاده‌سازی شده و امکان مدیریت کامل اطلاعات بیماران، پزشکان، نوبت‌دهی، پرونده‌های پزشکی، نسخه‌ها و شیفت‌های کاری را فراهم می‌کند.

✨ **چرا این پروژه؟**
- کاهش خطاهای انسانی در ثبت اطلاعات
- افزایش سرعت و دقت در انجام امور اداری و درمانی
- دسترسی سریع به سوابق بیماران
- مدیریت هوشمند نوبت‌ها و شیفت‌ها

---

## 🚀 امکانات اصلی

| قابلیت | توضیحات |
|--------|---------|
| 👥 **مدیریت کاربران** | ثبت و مدیریت اطلاعات بیماران، پزشکان و کارکنان |
| 📅 **نوبت‌دهی** | سیستم نوبت‌دهی آنلاین و برنامه‌ریزی مراجعه‌ها |
| 📋 **پرونده پزشکی** | ثبت کامل سوابق درمانی و تاریخچه بیماران |
| 💊 **نسخه الکترونیک** | ثبت و مدیریت نسخه‌های تجویز شده |
| 🔄 **شیفت‌بندی** | مدیریت شیفت‌های کاری پزشکان و پرسنل |
| 🔍 **Audit Log** | ثبت تمام تغییرات سیستم برای بررسی و امنیت |
| 🔐 **احراز هویت** | سیستم امنیتی با JWT Token |

---

## 🛠️ فناوری‌های استفاده شده

<div align="center">

| Backend | Database | Deployment | Tools |
|---------|----------|------------|-------|
| 🐍 Python 3.8+ | 💾 MySQL 8.0 | 🐳 Docker | 📝 python-dotenv |
| 🌐 Django 4.x | | 🚢 Docker Compose | ⏰ pytz |
| 🔌 DRF | | 🔫 Gunicorn | |
| 🔑 JWT | | 🌐 Nginx | |

</div>

### توضیحات بیشتر:

#### Backend (سمت سرور) 🖥️
- **Python 3.8+** 🐍 - زبان اصلی برنامه‌نویسی
- **Django 4.x** 🌐 - فریم‌ورک قدرتمند وب
- **Django REST Framework** 🔌 - ساخت APIهای RESTful
- **JWT Authentication** 🔑 - احراز هویت امن با توکن

#### Database (پایگاه داده) 💾
- **MySQL 8.0** - پایگاه داده رابطه‌ای قدرتمند برای ذخیره اطلاعات

#### Deployment (استقرار) 🚀
- **Docker** 🐳 - کانتینرسازی برای اجرای آسان
- **Docker Compose** 🚢 - مدیریت سرویس‌های چندگانه
- **Gunicorn** 🔫 - سرور WSGI برای تولید
- **Nginx** 🌐 - وب‌سرور و reverse proxy

---

## 📁 ساختار پروژه

```
hospital-management-system/
├── accounts/              # 👥 مدیریت کاربران و احراز هویت
│   ├── models.py          # مدل‌های Patient, Doctor, Staff
│   ├── views.py           # ویوهای ثبت‌نام، ورود، پروفایل
│   ├── serializers.py     # سریالایزرهای کاربر
│   └── urls.py            # مسیرهای API کاربران
│
├── appointments/          # 📅 سیستم نوبت‌دهی و زمان‌بندی
│   ├── models.py          # مدل‌های Appointment, Schedule
│   ├── views.py           # ویوهای رزرو، لغو، تغییر نوبت
│   ├── serializers.py     # سریالایزرهای نوبت
│   └── urls.py            # مسیرهای API نوبت‌ها
│
├── medical_records/       # 📋 پرونده‌های الکترونیک سلامت
│   ├── models.py          # مدل‌های MedicalRecord, Diagnosis
│   ├── views.py           # ویوهای ثبت و مشاهده سوابق
│   ├── serializers.py     # سریالایزرهای پرونده
│   └── urls.py            # مسیرهای API پرونده‌ها
│
├── prescriptions/         # 💊 مدیریت نسخه‌های پزشکی
│   ├── models.py          # مدل‌های Prescription, Medicine
│   ├── views.py           # ویوهای ثبت و لیست نسخه‌ها
│   ├── serializers.py     # سریالایزرهای نسخه
│   └── urls.py            # مسیرهای API نسخه‌ها
│
├── shifts/                # 🔄 برنامه‌ریزی شیفت‌های کاری
│   ├── models.py          # مدل‌های Shift, ShiftSchedule
│   ├── views.py           # ویوهای تعریف و تخصیص شیفت
│   ├── serializers.py     # سریالایزرهای شیفت
│   └── urls.py            # مسیرهای API شیفت‌ها
│
├── audit/                 # 🔍 سیستم لاگ‌گیری و نظارت
│   ├── models.py          # مدل AuditLog
│   ├── middleware.py      # میدل‌ور ثبت خودکار تغییرات
│   └── admin.py           # پنل مدیریت لاگ‌ها
│
├── hms/                   # ⚙️ تنظیمات اصلی پروژه Django
│   ├── settings.py        # تنظیمات پروژه
│   ├── urls.py            # مسیرهای اصلی
│   └── wsgi.py            # تنظیمات WSGI
│
├── manage.py              # 🔧 فایل مدیریت Django
├── requirements.txt       # 📦 وابستگی‌های پروژه
├── docker-compose.yml     # 🐳 تنظیمات Docker Compose
├── Dockerfile             # 📜 فایل ساخت Docker Image
├── .env.example           # 📝 نمونه فایل متغیرهای محیطی
├── entrypoint.sh          # 🚀 اسکریپت شروع کانتینر
└── README.md              # 📖 مستندات پروژه (همین فایل!)
```

📌 **نکته:** هر ماژول به صورت مستقل توسعه داده شده و قابلیت استفاده مجدد دارد.

---

## 🚀 نصب و راه‌اندازی

### پیش‌نیازها ⚙️

قبل از شروع، مطمئن شوید که موارد زیر را نصب کرده‌اید:

| نرم‌افزار | نسخه حداقل | لینک دانلود |
|-----------|-------------|-------------|
| 🐍 Python | 3.8+ | [python.org](https://www.python.org/downloads/) |
| 🐳 Docker | 20.10+ | [docker.com](https://www.docker.com/) |
| 📦 Git | 2.x+ | [git-scm.com](https://git-scm.com/) |

---

### روش 1: اجرای با Docker (توصیه شده) 🐳⭐

این ساده‌ترین روش برای راه‌اندازی پروژه است:

```bash
# 1️⃣ کلون کردن پروژه از گیت‌هاب
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system

# 2️⃣ ایجاد فایل .env از روی نمونه
cp .env.example .env

# 3️⃣ ویرایش فایل .env و تنظیم متغیرهای محیطی
# 🔴 مهم: حتماً رمز عبور دیتابیس را تغییر دهید!
nano .env  # یا از هر ادیتوری استفاده کنید

# 4️⃣ ساخت و اجرای کانتینرها
docker-compose up -d --build

# 5️⃣ اجرای مهاجرت‌های دیتابیس
docker-compose exec web python manage.py migrate

# 6️⃣ ایجاد کاربر سوپر (مدیر کل)
docker-compose exec web python manage.py createsuperuser

# 7️⃣ مشاهده لاگ‌ها (اختیاری)
docker-compose logs -f
```

✅ **مزایای استفاده از Docker:**
- عدم نیاز به نصب دستی dependencies
- ایزوله بودن محیط اجرا
- قابلیت انتقال آسان بین سیستم‌ها
- اجرای همزمان دیتابیس و اپلیکیشن

---

### روش 2: اجرای محلی (Local Development) 💻🔧

اگر می‌خواهید به صورت بومی توسعه دهید:

```bash
# 1️⃣ کلون کردن پروژه
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system

# 2️⃣ ساخت محیط مجازی (Virtual Environment)
python -m venv venv

# 3️⃣ فعال‌سازی محیط مجازی
# در لینوکس/مک:
source venv/bin/activate
# در ویندوز:
# venv\Scripts\activate

# 4️⃣ نصب وابستگی‌ها
pip install --upgrade pip
pip install -r requirements.txt

# 5️⃣ تنظیم متغیرهای محیطی
export DB_NAME=hms_db
export DB_USER=hms_user
export DB_PASSWORD=your_secure_password
export DB_HOST=localhost
export DB_PORT=3306

# 6️⃣ راه‌اندازی MySQL (اگر نصب نیست)
# Ubuntu/Debian:
sudo apt install mysql-server
sudo systemctl start mysql

# 7️⃣ ساخت دیتابیس
mysql -u root -p
CREATE DATABASE hms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hms_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON hms_db.* TO 'hms_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 8️⃣ اجرای مهاجرت‌ها
python manage.py migrate

# 9️⃣ ایجاد سوپر یوزر
python manage.py createsuperuser

# 🔟 اجرای سرور توسعه
python manage.py runserver
```

---

### 🎯 دسترسی به برنامه

پس از اجرای موفقیت‌آمیز، می‌توانید از طریق آدرس‌های زیر به برنامه دسترسی داشته باشید:

| سرویس | آدرس | توضیحات |
|-------|------|---------|
| 🌐 وب‌سایت | `http://localhost:8000` | صفحه اصلی |
| 🔐 پنل ادمین | `http://localhost:8000/admin` | مدیریت کاربران و داده‌ها |
| 🔌 API Base | `http://localhost:8000/api/` | نقطه شروع APIها |
| 📚 مستندات API | `http://localhost:8000/api/docs/` | Swagger UI |
| 🧪 Browserable API | `http://localhost:8000/api/auth/` | تست API مرورگر |

---

### 🔍 عیب‌یابی常见问题

<details>
<summary>❌ خطای اتصال به دیتابیس</summary>

- مطمئن شوید MySQL در حال اجراست: `sudo systemctl status mysql`
- بررسی کنید `.env` را درست تنظیم کرده‌اید
- پورت 3306 باز است: `netstat -an | grep 3306`

</details>

<details>
<summary>❌ خطای Migration</summary>

- حذف migrationهای قدیمی و ساخت مجدد:
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
python manage.py makemigrations
python manage.py migrate
```

</details>

<details>
<summary>❌ خطای Docker</summary>

- ری‌استارت کانتینرها:
```bash
docker-compose down
docker-compose up -d --build
```

</details>

---

## 🧩 ماژول‌های سیستم

<div align="center">

| # | ماژول | آیکون | توضیحات | وضعیت |
|---|-------|-------|----------|--------|
| 1 | Accounts | 👥 | مدیریت کاربران و احراز هویت | ✅ تکمیل |
| 2 | Appointments | 📅 | سیستم نوبت‌دهی آنلاین | ✅ تکمیل |
| 3 | Medical Records | 📋 | پرونده‌های الکترونیک سلامت | ✅ تکمیل |
| 4 | Prescriptions | 💊 | نسخه‌های الکترونیک | ✅ تکمیل |
| 5 | Shifts | 🔄 | مدیریت شیفت‌های کاری | ✅ تکمیل |
| 6 | Audit | 🔍 | لاگ‌گیری و نظارت | ✅ تکمیل |

</div>

---

### 1️⃣ Accounts (`accounts/`) 👥

**مدیریت کاربران، نقش‌ها و مجوزها**

#### 📦 مدل‌ها:
- `User` - کاربر اصلی سیستم (Abstract Base User)
- `Patient` - اطلاعات بیماران
- `Doctor` - اطلاعات پزشکان متخصص
- `Staff` - اطلاعات کارکنان اداری و درمانی

#### ⚡ قابلیت‌ها:
- ✅ ثبت‌نام کاربران جدید با نقش‌های مختلف
- ✅ ورود امن با JWT Token
- ✅ مدیریت پروفایل شخصی
- ✅ بازیابی رمز عبور
- ✅ تفکیک دسترسی بر اساس نقش (Role-Based Access Control)

#### 🔗 API Endpoints:
```
POST   /api/auth/register/     # ثبت‌نام
POST   /api/auth/login/        # ورود
POST   /api/auth/logout/       # خروج
GET    /api/auth/profile/      # مشاهده پروفایل
PUT    /api/auth/profile/      # ویرایش پروفایل
```

---

### 2️⃣ Appointments (`appointments/`) 📅

**سیستم نوبت‌دهی و زمان‌بندی هوشمند**

#### 📦 مدل‌ها:
- `Appointment` - نوبت‌های رزرو شده
- `Schedule` - برنامه زمانی پزشکان
- `Cancellation` - لغو نوبت‌ها

#### ⚡ قابلیت‌ها:
- ✅ رزرو نوبت آنلاین توسط بیماران
- ✅ مشاهده نوبت‌های آزاد پزشکان
- ✅ لغو نوبت با دلیل
- ✅ تغییر زمان نوبت
- ✅ ارسال یادآوری (ایمیل/پیامک) - به زودی
- ✅ جلوگیری از تداخل نوبت‌ها

#### 🔗 API Endpoints:
```
GET    /api/appointments/            # لیست نوبت‌ها
POST   /api/appointments/            # ایجاد نوبت جدید
GET    /api/appointments/{id}/       # جزئیات نوبت
PUT    /api/appointments/{id}/       # ویرایش نوبت
DELETE /api/appointments/{id}/       # لغو نوبت
GET    /api/doctors/{id}/schedule/   # برنامه پزشک
```

---

### 3️⃣ Medical Records (`medical_records/`) 📋

**پرونده‌های الکترونیک سلامت (EHR)**

#### 📦 مدل‌ها:
- `MedicalRecord` - پرونده اصلی بیمار
- `Diagnosis` - تشخیص‌های پزشکی
- `Treatment` - درمان‌های انجام شده
- `LabResult` - نتایج آزمایشگاه
- `VitalSign` - علائم حیاتی

#### ⚡ قابلیت‌ها:
- ✅ ثبت کامل سوابق پزشکی بیمار
- ✅ مشاهده تاریخچه درمانی
- ✅ ضمیمه کردن فایل (تصاویر، مدارک)
- ✅ طبقه‌بندی بر اساس نوع بیماری
- ✅ جستجوی پیشرفته در پرونده‌ها
- ✅ دسترسی مبتنی بر نقش (فقط پزشک معالج)

#### 🔗 API Endpoints:
```
GET    /api/records/                 # لیست پرونده‌ها
POST   /api/records/                 # ایجاد پرونده جدید
GET    /api/records/{id}/            # جزئیات پرونده
PUT    /api/records/{id}/            # ویرایش پرونده
GET    /api/patients/{id}/records/   # پرونده‌های یک بیمار
POST   /api/records/{id}/diagnosis/  # ثبت تشخیص
```

---

### 4️⃣ Prescriptions (`prescriptions/`) 💊

**مدیریت نسخه‌های الکترونیک**

#### 📦 مدل‌ها:
- `Prescription` - نسخه اصلی
- `PrescriptionItem` - اقلام نسخه (داروها)
- `Medicine` - بانک اطلاعاتی داروها
- `Pharmacy` - داروخانه‌ها

#### ⚡ قابلیت‌ها:
- ✅ ثبت نسخه الکترونیک توسط پزشک
- ✅ لیست کامل داروها با دوز و تعداد
- ✅ بررسی تداخلات دارویی - به زودی
- ✅ ارسال نسخه به داروخانه
- ✅ تاریخچه نسخه‌های بیمار
- ✅ چاپ نسخه با فرمت استاندارد

#### 🔗 API Endpoints:
```
GET    /api/prescriptions/           # لیست نسخه‌ها
POST   /api/prescriptions/           # ثبت نسخه جدید
GET    /api/prescriptions/{id}/      # جزئیات نسخه
PUT    /api/prescriptions/{id}/      # ویرایش نسخه
GET    /api/patients/{id}/prescriptions/  # نسخه‌های بیمار
GET    /api/medicines/               # لیست داروها
```

---

### 5️⃣ Shifts (`shifts/`) 🔄

**برنامه‌ریزی شیفت‌های کاری**

#### 📦 مدل‌ها:
- `Shift` - تعریف شیفت (صبح، عصر، شب)
- `ShiftSchedule` - برنامه شیفت‌بندی
- `ShiftAssignment` - تخصیص پرسنل به شیفت
- `TimeOff` - درخواست مرخصی

#### ⚡ قابلیت‌ها:
- ✅ تعریف انواع شیفت کاری
- ✅ تخصیص خودکار و دستی پرسنل
- ✅ مشاهده برنامه ماهانه
- ✅ مدیریت درخواست‌های مرخصی
- ✅ جایگزینی پرسنل در شیفت
- ✅ گزارش ساعات کاری

#### 🔗 API Endpoints:
```
GET    /api/shifts/                  # لیست شیفت‌ها
POST   /api/shifts/                  # ایجاد شیفت جدید
GET    /api/shifts/schedule/         # برنامه شیفت‌بندی
POST   /api/shifts/assign/           # تخصیص پرسنل
GET    /api/staff/{id}/shifts/       # شیفت‌های پرسنل
POST   /api/timeoff/                 # درخواست مرخصی
```

---

### 6️⃣ Audit (`audit/`) 🔍

**سیستم لاگ‌گیری و نظارت امنیتی**

#### 📦 مدل‌ها:
- `AuditLog` - ثبت تمام تغییرات سیستم
- `LoginHistory` - تاریخچه ورود کاربران
- `DataChange` - تغییرات داده‌های حساس

#### ⚡ قابلیت‌ها:
- ✅ ثبت خودکار تمام عملیات CRUD
- ✅ لاگ‌گیری ورود و خروج کاربران
- ✅ ردیابی تغییرات داده‌های حساس
- ✅ گزارش‌گیری از فعالیت‌ها
- ✅ هشدار برای فعالیت‌های مشکوک
- ✅ نگهداری لاگ‌ها برای ممیزی

#### 🔗 API Endpoints:
```
GET    /api/audit/logs/              # لیست لاگ‌ها
GET    /api/audit/logs/{id}/         # جزئیات لاگ
GET    /api/audit/user/{id}/         # لاگ‌های یک کاربر
GET    /api/audit/resource/{type}/   # لاگ‌های یک منبع
```

🔐 **نکته امنیتی:** دسترسی به این ماژول فقط برای مدیران سیستم امکان‌پذیر است.

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | ثبت‌نام کاربر جدید |
| `/api/auth/login/` | POST | ورود و دریافت توکن |
| `/api/patients/` | GET/POST | لیست/ایجاد بیمار |
| `/api/doctors/` | GET/POST | لیست/ایجاد پزشک |
| `/api/appointments/` | GET/POST | مدیریت نوبت‌ها |
| `/api/records/` | GET/POST | پرونده‌های پزشکی |
| `/api/prescriptions/` | GET/POST | نسخه‌ها |
| `/api/shifts/` | GET/POST | شیفت‌های کاری |

📚 **مستندات کامل API:** پس از اجرا به آدرس `/api/docs/` مراجعه کنید.

---

## 🤝 مشارکت در پروژه

ما از مشارکت شما استقبال می‌کنیم! 🎉

### چگونه مشارکت کنیم؟
1. Fork کردن پروژه 🍴
2. ایجاد برنچ جدید (`git checkout -b feature/AmazingFeature`) 🌿
3. کامیت تغییرات (`git commit -m 'Add some AmazingFeature'`) 💾
4. پوش به برنچ (`git push origin feature/AmazingFeature`) 🚀
5. باز کردن Pull Request 🔄

### راهنمای توسعه
- کدها باید تمیز و خوانا باشند
- از کامنت‌گذاری مناسب استفاده شود
- تست‌های لازم نوشته شوند

---

## 📊 وضعیت پروژه

🚧 **در حال توسعه فعال**

### Roadmap
- [x] ✅ پیاده‌سازی ماژول کاربران
- [x] ✅ سیستم نوبت‌دهی
- [x] ✅ پرونده‌های پزشکی
- [x] ✅ نسخه الکترونیک
- [x] ✅ مدیریت شیفت‌ها
- [ ] ⏳ گزارش‌گیری و آمار
- [ ] ⏳ پنل بیمار
- [ ] ⏳ نوتیفیکیشن و پیامک
- [ ] ⏳ داشبورد مدیریتی

---

## 📞 ارتباط با توسعه‌دهنده

در صورت داشتن سوال یا پیشنهاد:
- 📧 Email: your.email@example.com
- 💬 Issues: از بخش Issues گیت‌هاب استفاده کنید
- 🌐 Website: coming soon...

---

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. برای اطلاعات بیشتر به فایل LICENSE مراجعه کنید.

---

<div align="center">

### ⭐ اگر از این پروژه خوشتان آمد، حتماً ستاره بدهید! ⭐

✨ این پروژه به‌مرور تکمیل و بهینه می‌شود. از مشارکت شما سپاسگزاریم! ✨

**Made with ❤️ by the Development Team**

</div>
