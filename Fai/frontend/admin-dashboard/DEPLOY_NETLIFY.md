# 🚀 نشر Dashboard على Netlify

## الطريقة السريعة (Netlify CLI)

### 1. تثبيت Netlify CLI
```bash
npm install -g netlify-cli
```

### 2. تسجيل الدخول
```bash
netlify login
```

### 3. الانتقال لمجلد Dashboard
```bash
cd /Users/faialradhi/Documents/Absher/fraud_service/frontend/admin-dashboard
```

### 4. بناء المشروع
```bash
npm run build
```

### 5. النشر
```bash
netlify deploy --prod
```

---

## الطريقة الثانية (Netlify Dashboard)

### 1. اذهب إلى [netlify.com](https://netlify.com)
- سجل دخول أو أنشئ حساب

### 2. اضغط "Add new site" → "Deploy manually"

### 3. ارفع مجلد `dist`:
```bash
cd /Users/faialradhi/Documents/Absher/frontend/admin-dashboard
npm run build
# ثم ارفع مجلد dist كامل
```

### 4. إعداد Environment Variables:
- اذهب إلى Site settings → Environment variables
- أضف:
  - `VITE_API_URL` = `http://your-backend-url.com:8000`
  - أو إذا كان Backend على Heroku/Railway: `https://your-backend.herokuapp.com`

---

## الطريقة الثالثة (GitHub + Netlify)

### 1. ارفع الكود على GitHub
```bash
cd /Users/faialradhi/Documents/Absher/fraud_service
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 2. في Netlify:
- اضغط "Add new site" → "Import an existing project"
- اختر GitHub
- اختر Repository
- Build settings:
  - **Base directory**: `frontend/admin-dashboard`
  - **Build command**: `npm run build`
  - **Publish directory**: `frontend/admin-dashboard/dist`

### 3. Environment Variables:
- `VITE_API_URL` = `https://your-backend-url.com`

---

## ⚠️ مهم: Backend يجب أن يكون متاح على الإنترنت

### خيارات Backend:

#### 1. Railway (موصى به - مجاني)
```bash
# تثبيت Railway CLI
npm i -g @railway/cli

# تسجيل الدخول
railway login

# نشر
cd /Users/faialradhi/Documents/Absher/fraud_service
railway init
railway up
```

#### 2. Render
- اذهب إلى render.com
- أنشئ Web Service
- ارفع `fraud_service` folder
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 3. Heroku
```bash
heroku create your-app-name
git push heroku main
```

---

## 🔧 إعداد CORS في Backend

تأكد من أن `app/main.py` يحتوي على:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # أو ["https://your-netlify-app.netlify.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## ✅ بعد النشر

1. افتح Netlify Dashboard
2. اذهب إلى Site settings → Domain
3. يمكنك إضافة custom domain أو استخدام `your-app.netlify.app`

---

## 📝 ملاحظات

- **Backend URL**: يجب تحديث `VITE_API_URL` في Netlify Environment Variables
- **CORS**: تأكد من أن Backend يسمح بطلبات من Netlify domain
- **Build**: تأكد من أن `npm run build` يعمل بدون أخطاء

---

## 🐛 استكشاف الأخطاء

### Dashboard لا يتصل بالBackend
- تحقق من `VITE_API_URL` في Environment Variables
- تحقق من CORS settings في Backend
- افتح Browser Console (F12) وابحث عن أخطاء

### Build فاشل
- تأكد من تثبيت جميع dependencies: `npm install`
- تحقق من الأخطاء في Netlify Build logs

