# ⚡ حل فوري - Render (5 دقائق)

## الخطوات السريعة:

### 1. ارفع الكود على GitHub (دقيقة واحدة):

```bash
cd /Users/faialradhi/Documents/Absher/fraud_service
git init
git add .
git commit -m "Initial commit"
```

**ثم:**
- اذهب إلى [github.com](https://github.com)
- أنشئ repository جديد اسمه `absher-backend`
- ارفع الكود:
```bash
git remote add origin https://github.com/YOUR_USERNAME/absher-backend.git
git branch -M main
git push -u origin main
```

---

### 2. نشر على Render (3 دقائق):

**1. اذهب إلى [render.com](https://render.com)**
- سجل دخول بحساب GitHub

**2. اضغط "New +" → "Web Service"**

**3. اختر Repository: `absher-backend`**

**4. إعدادات:**
- **Name**: `absher-backend`
- **Environment**: `Python 3`
- **Region**: اختر الأقرب
- **Branch**: `main`
- **Root Directory**: (اتركه فارغ)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**5. Plan:**
- اختر **Free**

**6. اضغط "Create Web Service"**

---

### 3. انتظر النشر (2-3 دقائق)

ستحصل على رابط مثل: `https://absher-backend.onrender.com`

---

### 4. حدث Netlify:

**1. اذهب إلى [app.netlify.com](https://app.netlify.com)**

**2. اختر موقعك**

**3. Site settings → Environment variables**

**4. أضف:**
- Key: `VITE_API_URL`
- Value: `https://absher-backend.onrender.com`

**5. أعد النشر:**
```bash
cd frontend/admin-dashboard
netlify deploy --prod
```

---

## ✅ جاهز!

Dashboard على Netlify سيعمل مع Backend على Render!

---

## 🎯 أو استخدم ngrok (إذا كان لديك حساب):

```bash
# 1. سجل في ngrok.com
# 2. احصل على authtoken
ngrok config add-authtoken YOUR_TOKEN
# 3. شغّل
ngrok http 8000
```

لكن Render أسهل وأسرع!

