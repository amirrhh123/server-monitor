باشه، یک README حرفه‌ای، تمیز و استاندارد برات می‌نویسم؛ هم مناسب GitHub، هم قابل توسعه برای آیندهٔ پروژه.این نسخه شامل: توضیح، نصب، اجرا، ساختار پروژه، لاگ‌ها و TODO است.

اگر خواستی می‌توانم نسخهٔ انگلیسی هم بسازم.

📘 README پیشنهادی برای پروژهٔ Server Monitor CLI

# Server Monitor CLI

ابزار خط فرمان (CLI) برای مانیتورینگ سرویس‌ها، منابع سیستم و وضعیت HTTP endpoints.  
این پروژه با Python نوشته شده و شامل قابلیت‌هایی مثل logging، health check، بررسی سرویس‌های systemd و چک منابع CPU است.

---

## ✨ قابلیت‌ها

- بررسی وضعیت سرویس‌ها (systemd)
- بررسی سلامت HTTP endpoints
- مانیتورینگ CPU
- پشتیبانی از فایل تنظیمات JSON
- خروجی لاگ در فایل و ترمینال
- حالت verbose برای دیباگ بهتر

---

## 📦 نصب و اجرا

### 1) کلون کردن پروژه

git clone https://github.com/amirrhh123/server-monitor.git cd server-monitor


### 2) اجرای برنامه

python3 monitor.py check --all --verbose


### مثال‌ها

چک همهٔ سرویس‌ها:

python3 monitor.py check --all


چک یک سرویس خاص:

python3 monitor.py check --service nginx


اجرای report (فعلاً خالی):

python3 monitor.py report


---

## ⚙️ ساختار پروژه


server-monitor/ │ ├── monitor.py ├── config/ │   └── settings.json └── monitoring-app/ └── logs/ └── monitor.log


---

## 📝 فایل تنظیمات (settings.json)


{ "services": ["nginx", "sshd"], "thresholds": { "cpu": 85, "mem": 90 }, "endpoints": [ "http://localhost:8080/health" ] }


---

## 📄 نمونه خروجی لاگ


2026-06-02 23:37:42 [INFO    ] [SERVICE] nginx: running ✓ 2026-06-02 23:37:42 [ERROR   ] [SERVICE] sshd: DOWN ✗ 2026-06-02 23:37:42 [INFO    ] [CPU] 25% OK 2026-06-02 23:37:43 [ERROR   ] [HTTP] http://localhost:8080/health → Connection refused


---

## 🚀 TODO (برنامهٔ توسعه)

- اضافه کردن چک RAM و Disk
- اضافه کردن خروجی JSON
- ارسال هشدار تلگرام/ایمیل
- تبدیل به systemd service
- پشتیبانی از Docker health checks

---
