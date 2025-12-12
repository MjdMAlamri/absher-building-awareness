# أبشر - لوحة التحكم الإدارية

لوحة تحكم إدارية حديثة لنظام كشف الاحتيال في أبشر.

## المميزات

- ✅ عرض جميع الزيارات مع التفاصيل الكاملة
- ✅ عرض معلومات المستخدمين (وقت تسجيل الدخول، device ID)
- ✅ عرض طريقة المصادقة (QR Code vs Biometric)
- ✅ إحصائيات شاملة
- ✅ فلاتر متقدمة للبحث
- ✅ تصميم بألوان أبشر الرسمية
- ✅ واجهة عربية واضحة وبسيطة

## التثبيت

```bash
cd frontend/admin-dashboard
npm install
```

## التشغيل

```bash
npm run dev
```

سيفتح على: http://localhost:3000

## المتطلبات

- Node.js 18+
- الخادم الخلفي يعمل على http://localhost:8000

## البنية

```
frontend/admin-dashboard/
├── src/
│   ├── components/      # مكونات React
│   ├── pages/           # الصفحات
│   ├── services/        # API services
│   └── styles/          # CSS styles
├── public/
└── package.json
```

