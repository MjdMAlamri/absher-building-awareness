# كيفية التحقق من النظام (How to Check the System)

## ✅ النظام يعمل الآن!

### طريقة 1: استخدام المتصفح (الأسهل)

افتح المتصفح واذهب إلى:
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

في صفحة `/docs` يمكنك:
- رؤية جميع الـ endpoints
- تجربة API مباشرة من المتصفح
- إرسال طلبات واختبار النظام

---

### طريقة 2: استخدام Terminal (curl)

```bash
# 1. Health Check
curl http://localhost:8000/health

# 2. Test Low Risk Visit
curl -X POST "http://localhost:8000/evaluate-risk" \
  -H "Content-Type: application/json" \
  -d '{
    "visit_id": "VIS-001",
    "national_id_hash": "ID-123456",
    "branch_id": "BR-001",
    "gate_id": "GATE-01",
    "visit_time": "2024-01-15T10:30:00",
    "channel": "main_gate",
    "auth_method": "face+fingerprint",
    "device_id": "DEV-001",
    "repeated_attempts_last_24h": 0,
    "multi_branch_same_day": 0
  }'

# 3. Test High Risk Visit
curl -X POST "http://localhost:8000/evaluate-risk" \
  -H "Content-Type: application/json" \
  -d '{
    "visit_id": "VIS-002",
    "national_id_hash": "ID-999999",
    "branch_id": "BR-001",
    "gate_id": "GATE-01",
    "visit_time": "2024-01-15T14:00:00",
    "channel": "side_gate",
    "auth_method": "manual_review",
    "device_id": "DEV-SUSPICIOUS",
    "repeated_attempts_last_24h": 8,
    "multi_branch_same_day": 1
  }'
```

---

### طريقة 3: استخدام Script

```bash
cd fraud_service
./test_api.sh
```

أو:

```bash
cd fraud_service
bash test_api.sh
```

---

### طريقة 4: استخدام Python Demo

```bash
cd fraud_service
python3 demo.py
```

---

### طريقة 5: استخدام Python Requests

```python
import requests

# Test API
response = requests.post(
    "http://localhost:8000/evaluate-risk",
    json={
        "visit_id": "VIS-001",
        "national_id_hash": "ID-123456",
        "branch_id": "BR-001",
        "gate_id": "GATE-01",
        "visit_time": "2024-01-15T10:30:00",
        "channel": "main_gate",
        "auth_method": "face+fingerprint",
        "device_id": "DEV-001",
        "repeated_attempts_last_24h": 0,
        "multi_branch_same_day": 0,
    }
)

print(response.json())
```

---

## 📊 النتائج المتوقعة

### Low Risk Visit:
- **Risk Score**: ~0.12 - 0.40
- **Risk Level**: "low" or "medium"
- **Reasons**: قليلة أو فارغة

### High Risk Visit:
- **Risk Score**: > 0.60
- **Risk Level**: "high" or "critical"
- **Reasons**: متعددة (محاولات متكررة، فروع متعددة، إلخ)

---

## 🔍 التحقق من حالة الخادم

```bash
# Check if server is running
curl http://localhost:8000/health

# Check process
ps aux | grep uvicorn

# Check logs (if using nohup)
tail -f fraud_service/server.log
```

---

## 🛑 إيقاف الخادم

```bash
# Find and kill the process
pkill -f uvicorn

# Or find the PID first
ps aux | grep uvicorn
kill <PID>
```

---

## ✅ Checklist للتحقق:

- [ ] الخادم يعمل على port 8000
- [ ] `/health` يعيد `{"status": "healthy"}`
- [ ] `/docs` يفتح في المتصفح
- [ ] `/evaluate-risk` يقبل الطلبات ويعيد نتائج
- [ ] النموذج مدرب (`model_trained: true`)

---

## 🎯 للعرض (Demo):

1. افتح http://localhost:8000/docs في المتصفح
2. اضغط على `POST /evaluate-risk`
3. اضغط "Try it out"
4. عدّل البيانات أو استخدم المثال الافتراضي
5. اضغط "Execute"
6. شاهد النتيجة!

