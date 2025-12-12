import React from 'react'
import { Brain, AlertTriangle, TrendingUp, Activity } from 'lucide-react'

function MLAnalysis({ mlAnalysis, visitId }) {
  if (!mlAnalysis) return null

  const getFeatureLabel = (featureName) => {
    const labels = {
      'repeated_attempts_last_24h': 'محاولات متكررة (24 ساعة)',
      'multi_branch_same_day': 'فروع متعددة في نفس اليوم',
      'device_reuse_score': 'إعادة استخدام الجهاز',
      'time_anomaly_score': 'شذوذ الوقت',
      'auth_method_risk': 'مخاطر طريقة المصادقة',
      'visit_frequency_score': 'تكرار الزيارات',
    }
    return labels[featureName] || featureName
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'high': return '#EF4444'
      case 'medium': return '#F59E0B'
      case 'low': return '#10B981'
      default: return '#6B7280'
    }
  }

  return (
    <div style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      borderRadius: '12px',
      padding: '1.5rem',
      color: 'white',
      marginTop: '1.5rem',
      boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
        <Brain size={28} />
        <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: '700' }}>
          تحليل ML المتقدم - Expert Fraud Analysis
        </h2>
      </div>

      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
        marginBottom: '1.5rem'
      }}>
        <div style={{
          background: 'rgba(255, 255, 255, 0.15)',
          backdropFilter: 'blur(10px)',
          borderRadius: '8px',
          padding: '1rem',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <Activity size={20} />
            <span style={{ fontSize: '0.875rem', opacity: 0.9 }}>ML Score</span>
          </div>
          <div style={{ fontSize: '2rem', fontWeight: '700' }}>
            {(mlAnalysis.ml_score * 100).toFixed(1)}%
          </div>
        </div>

        <div style={{
          background: 'rgba(255, 255, 255, 0.15)',
          backdropFilter: 'blur(10px)',
          borderRadius: '8px',
          padding: '1rem',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <AlertTriangle size={20} />
            <span style={{ fontSize: '0.875rem', opacity: 0.9 }}>Anomaly Probability</span>
          </div>
          <div style={{ fontSize: '2rem', fontWeight: '700' }}>
            {mlAnalysis.anomaly_probability?.toFixed(1) || '0'}%
          </div>
        </div>

        <div style={{
          background: mlAnalysis.is_anomaly ? 'rgba(239, 68, 68, 0.3)' : 'rgba(16, 185, 129, 0.3)',
          backdropFilter: 'blur(10px)',
          borderRadius: '8px',
          padding: '1rem',
          border: `1px solid ${mlAnalysis.is_anomaly ? '#EF4444' : '#10B981'}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column'
        }}>
          <div style={{ fontSize: '0.875rem', marginBottom: '0.5rem', opacity: 0.9 }}>
            Anomaly Detection
          </div>
          <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>
            {mlAnalysis.is_anomaly ? '⚠️ Detected' : '✓ Normal'}
          </div>
        </div>

        <div style={{
          background: 'rgba(255, 255, 255, 0.15)',
          backdropFilter: 'blur(10px)',
          borderRadius: '8px',
          padding: '1rem',
          border: '1px solid rgba(255, 255, 255, 0.2)'
        }}>
          <div style={{ fontSize: '0.875rem', marginBottom: '0.5rem', opacity: 0.9 }}>
            Model Type
          </div>
          <div style={{ fontSize: '1rem', fontWeight: '600' }}>
            {mlAnalysis.model_type}
          </div>
          <div style={{ fontSize: '0.75rem', opacity: 0.8, marginTop: '0.25rem' }}>
            Confidence: {mlAnalysis.model_confidence}
          </div>
        </div>
      </div>

      {mlAnalysis.feature_analysis && Object.keys(mlAnalysis.feature_analysis).length > 0 && (
        <div style={{
          background: 'rgba(255, 255, 255, 0.1)',
          borderRadius: '8px',
          padding: '1rem',
          marginTop: '1rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <TrendingUp size={20} />
            <h3 style={{ margin: 0, fontSize: '1.125rem', fontWeight: '600' }}>
              Feature Analysis (تحليل الميزات)
            </h3>
          </div>
          
          <div style={{ display: 'grid', gap: '0.75rem' }}>
            {Object.entries(mlAnalysis.feature_analysis).map(([feature, data]) => (
              <div key={feature} style={{
                background: 'rgba(255, 255, 255, 0.1)',
                borderRadius: '6px',
                padding: '0.75rem',
                borderRight: `3px solid ${getStatusColor(data.status)}`
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                  <span style={{ fontWeight: '600' }}>{getFeatureLabel(feature)}</span>
                  <span style={{
                    background: getStatusColor(data.status),
                    color: 'white',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    fontSize: '0.75rem',
                    fontWeight: '600'
                  }}>
                    {data.status.toUpperCase()}
                  </span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.875rem', opacity: 0.9 }}>
                  <span>Value: {data.value}</span>
                  <span>Contribution: {data.contribution}%</span>
                </div>
                <div style={{
                  marginTop: '0.5rem',
                  height: '4px',
                  background: 'rgba(255, 255, 255, 0.2)',
                  borderRadius: '2px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    height: '100%',
                    width: `${Math.min(data.contribution, 100)}%`,
                    background: getStatusColor(data.status),
                    transition: 'width 0.3s'
                  }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={{
        marginTop: '1rem',
        padding: '0.75rem',
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '6px',
        fontSize: '0.75rem',
        opacity: 0.8
      }}>
        <strong>Model Info:</strong> {mlAnalysis.model_type} | 
        Features Used: {mlAnalysis.features_used?.length || 0} | 
        Visit ID: {visitId}
      </div>
    </div>
  )
}

export default MLAnalysis

