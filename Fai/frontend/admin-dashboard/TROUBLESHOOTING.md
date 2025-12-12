# 🔧 استكشاف الأخطاء - React Dashboard

## المشكلة: شاشة بيضاء بعد ثانية واحدة

### الحلول:

#### 1. تحقق من Console (المهم!)
افتح Developer Tools (F12) واذهب إلى Console. ابحث عن:
- أخطاء JavaScript (خطأ أحمر)
- أخطاء Network (طلبات فاشلة)

#### 2. تحقق من أن Backend يعمل:
```bash
curl http://localhost:8000/health
```

يجب أن يعيد:
```json
{"status": "healthy", "model_trained": true}
```

#### 3. تحقق من CORS:
إذا كان هناك خطأ CORS، تأكد من أن `app/main.py` يحتوي على:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    ...
)
```

#### 4. إعادة بناء Vite:
```bash
cd frontend/admin-dashboard
rm -rf node_modules/.vite
npm run dev
```

#### 5. تحقق من المتصفح:
- جرب Chrome/Firefox
- امسح Cache (Ctrl+Shift+R)
- افتح في Incognito mode

---

## الأخطاء الشائعة:

### خطأ: "Cannot connect to server"
**الحل:**
```bash
# Terminal 1 - Backend
cd /Users/faialradhi/Documents/Absher/fraud_service
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### خطأ: "@import must precede"
**الحل:** تم إصلاحه - @import الآن في أول ملف CSS

### خطأ: "Module not found"
**الحل:**
```bash
cd frontend/admin-dashboard
npm install
```

### خطأ: "White screen"
**الحل:**
1. افتح Console (F12)
2. ابحث عن الأخطاء
3. تحقق من Network tab
4. تأكد من أن Backend يعمل

---

## التحقق السريع:

```bash
# 1. Backend
curl http://localhost:8000/health

# 2. React
# افتح http://localhost:3000
# افتح Console (F12)
# ابحث عن أخطاء
```

---

## إذا استمرت المشكلة:

1. **افتح Console** (F12) وأرسل لي الأخطاء
2. **تحقق من Network tab** - هل الطلبات تنجح؟
3. **تحقق من Terminal** - هل هناك أخطاء في Backend؟

