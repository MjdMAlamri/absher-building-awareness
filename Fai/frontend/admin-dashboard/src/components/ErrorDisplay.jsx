import React from 'react'
import { AlertCircle, RefreshCw } from 'lucide-react'

function ErrorDisplay({ error, onRetry }) {
  return (
    <div style={{
      background: '#FEE2E2',
      color: '#991B1B',
      padding: '2rem',
      borderRadius: '12px',
      margin: '2rem',
      border: '2px solid #EF4444',
      textAlign: 'center'
    }}>
      <AlertCircle size={48} style={{ marginBottom: '1rem' }} />
      <h2 style={{ marginBottom: '1rem' }}>خطأ في تحميل البيانات</h2>
      <p style={{ marginBottom: '1.5rem', fontSize: '1rem' }}>{error}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            padding: '0.75rem 1.5rem',
            background: '#00A859',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            fontSize: '1rem',
            fontWeight: '600'
          }}
        >
          <RefreshCw size={20} />
          إعادة المحاولة
        </button>
      )}
      <div style={{ marginTop: '1.5rem', fontSize: '0.875rem', color: '#6B7280' }}>
        <p>تأكد من:</p>
        <ul style={{ listStyle: 'none', padding: 0, marginTop: '0.5rem' }}>
          <li>✓ الخادم يعمل على port 8000</li>
          <li>✓ البيانات موجودة في sample_data/</li>
          <li>✓ لا توجد مشاكل في الشبكة</li>
        </ul>
      </div>
    </div>
  )
}

export default ErrorDisplay

