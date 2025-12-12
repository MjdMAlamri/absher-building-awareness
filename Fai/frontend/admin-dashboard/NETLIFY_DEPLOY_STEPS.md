# 🚀 خطوات النشر على Netlify

## الخيار 1: إنشاء موقع جديد (موصى به)

في Terminal، عندما يسألك Netlify:
```
? What would you like to do?
```

**اختر:** `+ Create & configure a new project`

ثم:
- سيطلب منك **Site name**: اكتب `absher-dashboard` (أو أي اسم تريده)
- سيطلب **Publish directory**: اضغط Enter (سيستخدم `dist` تلقائياً)

---

## الخيار 2: استخدام الأمر المباشر

```bash
cd /Users/faialradhi/Documents/Absher/fraud_service/frontend/admin-dashboard
netlify deploy --create-site absher-dashboard --prod
```

سيطلب منك:
- **Site name**: اضغط Enter (سيستخدم `absher-dashboard`)
- **Publish directory**: اضغط Enter (سيستخدم `dist`)

---

## بعد النشر:

1. ستحصل على رابط مثل: `https://absher-dashboard.netlify.app`
2. اذهب إلى Netlify Dashboard
3. Site settings → Environment variables
4. أضف: `VITE_API_URL` = `http://YOUR_BACKEND_URL:8000`

---

## ✅ جاهز!

بعد النشر، افتح الرابط وستجد Dashboard يعمل بدون 404!

