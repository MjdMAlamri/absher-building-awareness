# 🔧 إصلاح مشكلة 404 في Netlify

## المشكلة:
عند فتح الموقع على Netlify، يظهر "Page not found"

## الحل:

### 1. تأكد من ملف `_redirects` في مجلد `dist`

بعد `npm run build`، انسخ ملف `_redirects` إلى `dist`:

```bash
cd /Users/faialradhi/Documents/Absher/fraud_service/frontend/admin-dashboard
npm run build
cp _redirects dist/_redirects
```

### 2. أو أعد البناء مع نسخ الملف تلقائياً

أضف script في `package.json`:

```json
"scripts": {
  "build": "vite build && cp _redirects dist/_redirects"
}
```

### 3. تحقق من محتوى `dist/_redirects`

يجب أن يحتوي على:
```
/*    /index.html   200
```

### 4. أعد النشر على Netlify

```bash
netlify deploy --prod
```

أو ارفع مجلد `dist` من جديد.

---

## ✅ الحل السريع:

```bash
cd /Users/faialradhi/Documents/Absher/fraud_service/frontend/admin-dashboard

# 1. أعد البناء
npm run build

# 2. انسخ _redirects إلى dist
cp _redirects dist/_redirects

# 3. أعد النشر
netlify deploy --prod
```

---

## 🔍 التحقق:

بعد النشر، افتح:
- `https://your-site.netlify.app/` ✅
- `https://your-site.netlify.app/dashboard` ✅ (يجب أن يعمل)

إذا استمرت المشكلة، تحقق من:
1. ملف `_redirects` موجود في `dist/`
2. محتوى الملف صحيح
3. `netlify.toml` موجود في root المشروع

