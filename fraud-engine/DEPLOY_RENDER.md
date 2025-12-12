# 🚀 نشر Backend على Render (بديل مجاني)

## Railway لديه خطة محدودة، استخدم Render بدلاً منه:

### الخطوات:

**1. اذهب إلى [render.com](https://render.com)**
- سجل دخول بحساب GitHub

**2. اضغط "New +" → "Web Service"**

**3. اربط GitHub Repository:**
- إذا لم ترفع الكود على GitHub:
  ```bash
  cd /Users/faialradhi/Documents/Absher/fraud_service
  git init
  git add .
  git commit -m "Initial commit"
  # ارفع على GitHub أولاً
  ```

**4. إعدادات Build:**
- **Name**: `absher-backend`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**5. Environment Variables:**
- لا حاجة (الكود يعمل بدونها)

**6. Plan:**
- اختر **Free** plan

**7. اضغط "Create Web Service"**

---

## ⏱️ الانتظار:

- Build: ~5-10 دقائق
- Deploy: ~2-3 دقائق

---

## ✅ بعد النشر:

ستحصل على رابط مثل: `https://absher-backend.onrender.com`

**حدث Netlify:**
- `VITE_API_URL` = `https://absher-backend.onrender.com`

---

## 🔧 إذا كان Railway يعمل:

جرب:
```bash
railway up --detach
```

أو تحقق من الرابط في Railway Dashboard.

