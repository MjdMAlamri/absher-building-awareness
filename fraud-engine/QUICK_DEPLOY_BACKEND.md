# ⚡ نشر سريع - Backend

## 🚀 Railway (أسهل طريقة - 5 دقائق)

### 1. تثبيت Railway CLI:
```bash
npm install -g @railway/cli
```

### 2. تسجيل الدخول:
```bash
railway login
```

### 3. النشر:
```bash
cd /Users/faialradhi/Documents/Absher/fraud_service
railway init
railway up
```

### 4. احصل على الرابط:
```bash
railway domain
```

**ستحصل على رابط مثل:** `https://your-app.railway.app`

---

## 🔧 تحديث Netlify:

بعد الحصول على Backend URL:

1. اذهب إلى Netlify Dashboard
2. Site settings → Environment variables
3. أضف: `VITE_API_URL` = `https://your-app.railway.app`
4. أعد النشر

---

## ✅ جاهز!

Dashboard على Netlify سيعمل مع Backend على Railway!

