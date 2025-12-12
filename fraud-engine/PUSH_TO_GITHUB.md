# 🚀 رفع الكود على GitHub - طريقة بديلة

## الطريقة 1: استخدام GitHub CLI (أسهل)

```bash
# تثبيت GitHub CLI
brew install gh

# تسجيل الدخول
gh auth login

# رفع الكود
cd /Users/faialradhi/Documents/Absher/fraud_service
gh repo create absher-backend --public --source=. --remote=origin --push
```

---

## الطريقة 2: استخدام Personal Access Token

**1. أنشئ Token:**
- اذهب إلى: https://github.com/settings/tokens
- اضغط "Generate new token (classic)"
- اختر: `repo` permissions
- انسخ الـ token

**2. استخدم Token:**
```bash
cd /Users/faialradhi/Documents/Absher/fraud_service
git remote set-url origin https://YOUR_TOKEN@github.com/77Fayy/absher-backend.git
git push -u origin main
```

---

## الطريقة 3: رفع يدوي (من GitHub Website)

**1. اذهب إلى: https://github.com/77Fayy/absher-backend**

**2. اضغط "uploading an existing file"**

**3. اسحب مجلد `fraud_service` بالكامل**

**4. Commit changes**

---

## الطريقة 4: استخدام SSH

**1. تحقق من SSH:**
```bash
ls -la ~/.ssh/id_*.pub
```

**2. إذا موجود، استخدم:**
```bash
git remote set-url origin git@github.com:77Fayy/absher-backend.git
git push -u origin main
```

---

## ✅ الأسهل: GitHub CLI

```bash
brew install gh
gh auth login
gh repo create absher-backend --public --source=. --remote=origin --push
```

