# 🚀 نشر سريع على Netlify

## الخطوات (5 دقائق):

### 1. تثبيت Netlify CLI
```bash
npm install -g netlify-cli
```

### 2. تسجيل الدخول
```bash
netlify login
```

### 3. الانتقال للمجلد
```bash
cd /Users/faialradhi/Documents/Absher/fraud_service/frontend/admin-dashboard
```

### 4. النشر مباشرة
```bash
netlify deploy --prod
```

سيطلب منك:
- **Site name**: اختر اسماً (مثل: `absher-dashboard`)
- **Publish directory**: اضغط Enter (سيستخدم `dist` تلقائياً)

---

## ⚙️ إعداد Environment Variable

بعد النشر، اذهب إلى:
1. Netlify Dashboard → Your Site → Site settings
2. Environment variables → Add variable
3. أضف:
   - **Key**: `VITE_API_URL`
   - **Value**: `https://your-backend-url.com` (أو `http://your-ip:8000` إذا كان Backend على server)

---

## 🌐 بدون CLI (من الموقع)

1. اذهب إلى [app.netlify.com](https://app.netlify.com)
2. اضغط "Add new site" → "Deploy manually"
3. ارفع مجلد `dist` (اسحبه وأفلته)
4. اضغط "Deploy site"

---

## ✅ جاهز!

بعد النشر، ستحصل على رابط مثل:
`https://your-site-name.netlify.app`

---

## ⚠️ مهم: Backend يجب أن يكون متاح

إذا كان Backend على `localhost`، لن يعمل من Netlify.

**الحلول:**
1. **نشر Backend على Railway/Render/Heroku**
2. **أو استخدام IP عام** (إذا كان Backend على server)

---

## 🔧 إذا كان Backend على server:

في `VITE_API_URL` استخدم:
- `http://YOUR_SERVER_IP:8000`
- أو `https://your-domain.com:8000`

