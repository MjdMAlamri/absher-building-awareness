# ⚡ حل سريع - 3 دقائق!

## الحل 1: ngrok (فوري - مؤقت)

### الخطوات:

**1. تثبيت ngrok:**
```bash
brew install ngrok
```

**2. شغّل Backend محلياً:**
```bash
cd /Users/faialradhi/Documents/Absher/fraud_service
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**3. في terminal آخر، شغّل ngrok:**
```bash
ngrok http 8000
```

**4. ستحصل على رابط مثل:**
```
https://abc123.ngrok.io
```

**5. حدث Netlify:**
- `VITE_API_URL` = `https://abc123.ngrok.io`

✅ **جاهز في 2 دقيقة!**

---

## الحل 2: Render (دائم - 5 دقائق)

### بدون GitHub (أسرع):

**1. اذهب إلى [render.com](https://render.com)**

**2. اضغط "New +" → "Web Service"**

**3. اضغط "Public Git repository"**

**4. أدخل:**
- Repository: `https://github.com/YOUR_USERNAME/absher-backend`
- (أو أنشئ repo جديد على GitHub أولاً)

**5. إعدادات:**
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**6. Deploy!**

---

## الحل 3: PythonAnywhere (سريع)

**1. اذهب إلى [pythonanywhere.com](https://www.pythonanywhere.com)**

**2. سجل دخول مجاني**

**3. ارفع الكود**

**4. شغّل:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🎯 الأسرع: ngrok (2 دقيقة)

```bash
# Terminal 1
cd /Users/faialradhi/Documents/Absher/fraud_service
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2
ngrok http 8000
```

**انسخ الرابط من ngrok وضعه في Netlify!**

