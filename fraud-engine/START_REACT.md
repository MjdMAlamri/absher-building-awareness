# 🚀 كيفية تشغيل React Dashboard

## الخطوات السريعة

### 1. تشغيل الخادم الخلفي (Backend)

```bash
cd /Users/faialradhi/Documents/Absher/fraud_service

# إيقاف أي عملية سابقة
lsof -ti:8000 | xargs kill -9 2>/dev/null

# تشغيل الخادم
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &
```

**التحقق:**
```bash
curl http://localhost:8000/health
```

---

### 2. تشغيل React Dashboard

```bash
cd /Users/faialradhi/Documents/Absher/fraud_service/frontend/admin-dashboard

# تثبيت المكتبات (أول مرة فقط)
npm install

# تشغيل Dashboard
npm run dev
```

---

### 3. افتح المتصفح

افتح: **http://localhost:3000**

---

## ✅ التحقق من أن كل شيء يعمل

### Backend (Python):
```bash
# Terminal 1
cd /Users/faialradhi/Documents/Absher/fraud_service
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend (React):
```bash
# Terminal 2
cd /Users/faialradhi/Documents/Absher/fraud_service/frontend/admin-dashboard
npm run dev
```

---

## 🎯 الروابط

- **React Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🛑 إيقاف الخوادم

```bash
# إيقاف Backend
lsof -ti:8000 | xargs kill -9

# إيقاف React (اضغط Ctrl+C في terminal)
```

---

## ⚠️ استكشاف الأخطاء

### Port 8000 مستخدم:
```bash
lsof -ti:8000 | xargs kill -9
```

### React لا يتصل بالخادم:
- تأكد أن Backend يعمل على port 8000
- تحقق من `vite.config.js` - proxy settings

### npm install فشل:
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## 📝 ملاحظات

- React Dashboard يستخدم Vite (سريع جداً)
- Hot Module Replacement (HMR) مفعل - التغييرات تظهر فوراً
- Backend يجب أن يعمل قبل React

