# 🔧 إصلاح مشكلة GitHub

## المشكلة:
`Permission denied` - المستخدم `shaykhahalmaani` ليس لديه صلاحية على `77Fayy/absher-backend`

## الحلول:

### الحل 1: استخدام SSH (موصى به)

**1. تحقق من SSH keys:**
```bash
ls -la ~/.ssh
```

**2. إذا لم يكن لديك SSH key:**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**3. أضف SSH key إلى GitHub:**
- اذهب إلى: https://github.com/settings/keys
- اضغط "New SSH key"
- انسخ محتوى: `cat ~/.ssh/id_ed25519.pub`

**4. استخدم SSH URL:**
```bash
git remote add origin git@github.com:77Fayy/absher-backend.git
git push -u origin main
```

---

### الحل 2: استخدام Personal Access Token

**1. أنشئ Token:**
- اذهب إلى: https://github.com/settings/tokens
- اضغط "Generate new token (classic)"
- اختر: `repo` permissions
- انسخ الـ token

**2. استخدم Token:**
```bash
git remote add origin https://YOUR_TOKEN@github.com/77Fayy/absher-backend.git
git push -u origin main
```

---

### الحل 3: إنشاء Repo جديد باسمك

**1. اذهب إلى [github.com](https://github.com)**
- أنشئ repository جديد باسم `absher-backend`

**2. استخدم رابطك:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/absher-backend.git
git push -u origin main
```

---

## الأسرع: استخدم SSH

```bash
git remote add origin git@github.com:77Fayy/absher-backend.git
git push -u origin main
```

