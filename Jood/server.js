// server.js
const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ---- Mock "database" of appointments ----
const appointments = [
  {
    nationalId: '1234567890',
    fullName: 'سارة عبد الله السعد',
    service: 'الأحوال المدنية - تجديد بطاقة الهوية الوطنية',
    location: 'مكتب الأحوال المدنية بالرياض - فرع العليا',
    date: '2025-12-05',
    time: '10:30 ص',
    ticketNumber: 'أ-102',
    notes: 'يُرجى التوجه إلى الطابق الأول عبر المصعد الرئيسي أو الدرج المجاور للاستقبال. تقع النافذة رقم 5 في القسم الأيمن من الصالة، بجانب لوحة الإرشادات الإلكترونية. سيتم عرض رقم تذكرتكم أ-102 على الشاشة الإلكترونية عند حلول دوركم.'
  },
  {
     nationalId: '1111222233',
    fullName: 'محمد صالح القحطاني',
    service: 'مكتب الجوازات - إصدار جواز سفر',
    location: 'مكتب الجوازات بالرياض - طريق الملك فهد',
    date: '2025-12-06',
    time: '01:15 م',
    ticketNumber: 'ب-057',
    notes: 'تقع النافذة رقم 12 في الصالة الرئيسية بالطابق الأرضي، على بُعد عشرة أمتار تقريباً من المدخل الرئيسي جهة اليسار. يُمكن الوصول إليها مباشرة بعد تجاوز بوابة الأمن. راقب شاشات العرض الإلكترونية التي ستُظهر رقم تذكرتكم ب-057 عند استدعائكم.'
  },
  {
   nationalId: '9876543210',
    fullName: 'هند عبد الله',
    service: 'إدارة المرور - تجديد الرخصة',
    location: 'مكتب المرور بالرياض - ملز',
    date: '2025-12-07',
    time: '09:00 ص',
    ticketNumber: 'ج-021',
    notes: 'يُرجى التوجه إلى قسم تجديد الرخص في الجناح الأيمن من المبنى. تقع النافذة رقم 8 في نهاية الممر الأول، بالقرب من منطقة الانتظار المخصصة. تابع الشاشة الإلكترونية لظهور رقم تذكرتكم ج-021 عند حلول دوركم.'
  }
];

// ---- Routes ----

// Check if national ID exists
app.post('/api/check-id', (req, res) => {
  const { nationalId } = req.body;

  if (!nationalId) {
    return res.status(400).json({ ok: false, message: 'National ID is required.' });
  }

  const appointment = appointments.find(a => a.nationalId === nationalId);

  if (!appointment) {
    return res.status(404).json({ ok: false, message: 'No appointment found for this ID.' });
  }

  // Don't send details yet (only after verification)
  res.json({ ok: true, message: 'ID found. Choose verification method.' });
});

// Simulated selfie verification
app.post('/api/verify-selfie', (req, res) => {
  const { nationalId } = req.body;

  const appointment = appointments.find(a => a.nationalId === nationalId);
  if (!appointment) {
    return res.status(404).json({ ok: false, message: 'Appointment not found.' });
  }

  // here you could receive an image and run real face recognition (in a real system)
  // For now, we just simulate success.
  res.json({
    ok: true,
    message: 'Selfie verified successfully.',
    appointment
  });
});

// Simulated fingerprint verification
app.post('/api/verify-fingerprint', (req, res) => {
  const { nationalId } = req.body;

  const appointment = appointments.find(a => a.nationalId === nationalId);
  if (!appointment) {
    return res.status(404).json({ ok: false, message: 'Appointment not found.' });
  }

  // A real fingerprint scanner would NOT be handled here with just a browser.
  // For now, we just simulate success.
  res.json({
    ok: true,
    message: 'Fingerprint verified successfully.',
    appointment
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Gov entrance server running at http://localhost:${PORT}`);
});
