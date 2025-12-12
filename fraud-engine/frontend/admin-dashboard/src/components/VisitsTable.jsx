import React, { useState } from 'react'
import { Calendar, MapPin, Smartphone, Shield, User, Brain } from 'lucide-react'
import MLAnalysis from './MLAnalysis'
import { adminAPI } from '../services/api'

function VisitsTable({ visits, loading, onVisitsUpdate }) {
  const [selectedVisit, setSelectedVisit] = useState(null)
  const [mlAnalysisCache, setMlAnalysisCache] = useState({})
  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return new Intl.DateTimeFormat('ar-SA', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date)
  }

  const getRiskBadgeClass = (riskLevel) => {
    switch (riskLevel) {
      case 'low': return 'badge badge-low'
      case 'medium': return 'badge badge-medium'
      case 'high': return 'badge badge-high'
      case 'critical': return 'badge badge-critical'
      default: return 'badge'
    }
  }

  const getRiskLabel = (riskLevel) => {
    const labels = {
      low: 'منخفض',
      medium: 'متوسط',
      high: 'عالي',
      critical: 'حرج',
    }
    return labels[riskLevel] || riskLevel
  }

  const getAuthMethodLabel = (method) => {
    const labels = {
      'face+fingerprint': 'بصمة + وجه',
      'qr+otp': 'QR Code',
      'biometric_only': 'بيومترية',
      'manual_review': 'مراجعة يدوية',
    }
    return labels[method] || method
  }

  const getAuthBadgeClass = (method) => {
    if (method.includes('qr')) return 'auth-badge auth-badge-qr'
    if (method.includes('face') || method.includes('fingerprint') || method.includes('biometric')) {
      return 'auth-badge auth-badge-biometric'
    }
    return 'auth-badge auth-badge-manual'
  }

  if (loading) {
    return (
      <div className="visits-table-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>جاري تحميل الزيارات...</p>
        </div>
      </div>
    )
  }

  if (visits.length === 0) {
    return (
      <div className="visits-table-container">
        <div className="empty-container">
          <p>لا توجد زيارات متطابقة مع الفلاتر المحددة</p>
        </div>
      </div>
    )
  }

  return (
    <div className="visits-table-container">
      <div style={{ padding: '1rem', background: '#00A859', color: 'white', fontWeight: '600' }}>
        <Shield size={20} style={{ display: 'inline', marginLeft: '0.5rem' }} />
        قائمة الزيارات ({visits.length})
      </div>
      <div style={{ overflowX: 'auto', maxHeight: '600px', overflowY: 'auto' }}>
        <table className="visits-table">
          <thead style={{ position: 'sticky', top: 0, zIndex: 10, background: '#00A859' }}>
            <tr>
              <th>وقت الزيارة</th>
              <th>المستخدم</th>
              <th>الفرع / البوابة</th>
              <th>طريقة المصادقة</th>
              <th>جهاز</th>
              <th>مستوى الخطر</th>
              <th>نقاط الخطر</th>
              <th>المحاولات</th>
            </tr>
          </thead>
          <tbody>
            {visits.map((visit) => (
              <tr key={visit.visit_id}>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Calendar size={16} color="#6B7280" />
                    <span>{formatDate(visit.visit_time)}</span>
                  </div>
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <User size={16} color="#6B7280" />
                    <span style={{ fontFamily: 'monospace', fontSize: '0.75rem' }}>
                      {visit.national_id_hash.substring(0, 12)}...
                    </span>
                  </div>
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <MapPin size={16} color="#6B7280" />
                    <div>
                      <div style={{ fontWeight: '600' }}>{visit.branch_id}</div>
                      <div style={{ fontSize: '0.75rem', color: '#6B7280' }}>{visit.gate_id}</div>
                    </div>
                  </div>
                </td>
                <td>
                  <span className={getAuthBadgeClass(visit.auth_method)}>
                    {getAuthMethodLabel(visit.auth_method)}
                  </span>
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <Smartphone size={16} color="#6B7280" />
                    <div>
                      <div style={{ fontFamily: 'monospace', fontSize: '0.75rem' }}>
                        {visit.device_id}
                      </div>
                      {visit.is_same_device ? (
                        <span className="device-status device-same">نفس الجهاز</span>
                      ) : visit.device_count > 1 ? (
                        <span className="device-status device-different">
                          {visit.device_count} أجهزة مختلفة
                        </span>
                      ) : (
                        <span className="device-status device-new">جهاز جديد</span>
                      )}
                    </div>
                  </div>
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span className={getRiskBadgeClass(visit.risk_level)}>
                      {getRiskLabel(visit.risk_level)}
                    </span>
                    <button
                      onClick={async () => {
                        if (selectedVisit === visit.visit_id) {
                          setSelectedVisit(null)
                        } else {
                          setSelectedVisit(visit.visit_id)
                          // Load ML analysis on-demand if not cached
                          if (!visit.ml_analysis && !mlAnalysisCache[visit.visit_id]) {
                            try {
                              const mlData = await adminAPI.getMLAnalysis(visit.visit_id)
                              setMlAnalysisCache(prev => ({
                                ...prev,
                                [visit.visit_id]: mlData.ml_analysis
                              }))
                            } catch (error) {
                              console.error('Error loading ML analysis:', error)
                            }
                          }
                        }
                      }}
                      style={{
                        background: '#667eea',
                        color: 'white',
                        border: 'none',
                        borderRadius: '6px',
                        padding: '0.25rem 0.5rem',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.25rem',
                        fontSize: '0.75rem'
                      }}
                      title="عرض تحليل ML"
                    >
                      <Brain size={14} />
                      ML
                    </button>
                  </div>
                </td>
                <td>
                  <div style={{ fontWeight: '600', color: '#1F2937' }}>
                    {(visit.risk_score * 100).toFixed(1)}%
                  </div>
                </td>
                <td>
                  <div>
                    {visit.repeated_attempts_last_24h > 0 && (
                      <div style={{ color: '#EF4444', fontWeight: '600' }}>
                        {visit.repeated_attempts_last_24h} محاولة
                      </div>
                    )}
                    {visit.multi_branch_same_day > 0 && (
                      <div style={{ color: '#F59E0B', fontSize: '0.75rem' }}>
                        فروع متعددة
                      </div>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {selectedVisit && (visits.find(v => v.visit_id === selectedVisit)?.ml_analysis || mlAnalysisCache[selectedVisit]) && (
        <MLAnalysis
          mlAnalysis={visits.find(v => v.visit_id === selectedVisit)?.ml_analysis || mlAnalysisCache[selectedVisit]}
          visitId={selectedVisit}
        />
      )}
    </div>
  )
}

export default VisitsTable

