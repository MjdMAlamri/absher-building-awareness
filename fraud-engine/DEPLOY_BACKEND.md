# 🚀 نشر Backend على الإنترنت

## الطريقة 1: Railway (موصى به - مجاني)

### الخطوات:

**1. تثبيت Railway CLI:**
```bash
npm install -g @railway/cli
```

**2. تسجيل الدخول:**
```bash
railway login
```

**3. الانتقال لمجلد المشروع:**
```bash
cd /Users/faialradhi/Documents/Absher/fraud_service
```

**4. تهيئة المشروع:**
```bash
railway init
```

**5. رفع البيانات:**
```bash
# رفع sample_data folder
railway add
```

**6. النشر:**
```bash
railway up
```

**7. الحصول على الرابط:**
```bash
railway domain
```

---

## الطريقة 2: Render (مجاني أيضاً)

### الخطوات:

**1. اذهب إلى [render.com](https://render.com)**

**2. أنشئ Web Service جديد**

**3. اربط GitHub Repository:**
- ارفع الكود على GitHub أولاً
- ثم اربطه في Render

**4. إعدادات Build:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**5. Environment Variables:**
- لا حاجة (الكود يستخدم CSV files)

**6. Deploy!**

---

## الطريقة 3: Heroku

### الخطوات:

**1. تثبيت Heroku CLI:**
```bash
brew install heroku/brew/heroku
```

**2. تسجيل الدخول:**
```bash
heroku login
```

**3. إنشاء App:**
```bash
cd /Users/faialradhi/Documents/Absher/fraud_service
heroku create absher-backend
```

**4. النشر:**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

---

## ⚙️ بعد النشر:

### 1. احصل على Backend URL:
- Railway: `https://your-app.railway.app`
- Render: `https://your-app.onrender.com`
- Heroku: `https://your-app.herokuapp.com`

### 2. حدث Netlify Environment Variable:
- اذهب إلى Netlify Dashboard
- Site settings → Environment variables
- أضف: `VITE_API_URL` = `https://your-backend-url.com`

### 3. أعد بناء Dashboard:
```bash
cd frontend/admin-dashboard
npm run build
netlify deploy --prod
```

---

## 📝 ملاحظات مهمة:

1. **البيانات**: تأكد من رفع `sample_data/` folder
2. **CORS**: الكود يدعم CORS بالفعل (`allow_origins=["*"]`)
3. **Port**: استخدم `$PORT` environment variable
4. **Dependencies**: تأكد من `requirements.txt` محدث

---

## ✅ جاهز!

بعد النشر، Dashboard على Netlify سيعمل مع Backend على الإنترنت!

