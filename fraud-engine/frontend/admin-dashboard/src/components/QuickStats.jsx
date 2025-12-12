import React from 'react'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

function QuickStats({ statistics }) {
  if (!statistics) return null

  const totalVisits = statistics.total_visits || 1
  const totalUsers = statistics.total_users || 1
  
  const stats = [
    {
      label: 'نسبة الزيارات المشبوهة',
      value: `${((statistics.suspicious_visits || 0) / totalVisits * 100).toFixed(1)}%`,
      trend: (statistics.suspicious_visits || 0) > totalVisits * 0.1 ? 'up' : 'down',
      color: (statistics.suspicious_visits || 0) > totalVisits * 0.1 ? '#EF4444' : '#10B981'
    },
    {
      label: 'متوسط الزيارات لكل مستخدم',
      value: (totalVisits / totalUsers).toFixed(1),
      trend: 'neutral',
      color: '#3B82F6'
    },
    {
      label: 'نسبة استخدام أجهزة متعددة',
      value: `${((statistics.device_reuse_count || 0) / totalUsers * 100).toFixed(1)}%`,
      trend: 'up',
      color: '#F59E0B'
    }
  ]

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up': return <TrendingUp size={16} />
      case 'down': return <TrendingDown size={16} />
      default: return <Minus size={16} />
    }
  }

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
      gap: '1rem',
      marginBottom: '2rem'
    }}>
      {stats.map((stat, index) => (
        <div
          key={index}
          style={{
            background: 'white',
            borderRadius: '8px',
            padding: '1rem',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
            borderRight: `3px solid ${stat.color}`
          }}
        >
          <div style={{ fontSize: '0.875rem', color: '#6B7280', marginBottom: '0.5rem' }}>
            {stat.label}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.5rem', fontWeight: '700', color: stat.color }}>
              {stat.value}
            </span>
            <span style={{ color: stat.color }}>
              {getTrendIcon(stat.trend)}
            </span>
          </div>
        </div>
      ))}
    </div>
  )
}

export default QuickStats

