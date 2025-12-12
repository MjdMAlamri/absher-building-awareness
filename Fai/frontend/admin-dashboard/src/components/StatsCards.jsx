import React from 'react'
import { Users, AlertTriangle, Shield, Smartphone, Activity } from 'lucide-react'

function StatsCards({ statistics }) {
  if (!statistics) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: '#6B7280' }}>
        <p>جاري تحميل الإحصائيات...</p>
      </div>
    )
  }

  const stats = [
    {
      title: 'إجمالي الزيارات',
      value: statistics.total_visits?.toLocaleString('ar-SA') || 0,
      icon: <Activity size={24} />,
      color: '#00A859',
    },
    {
      title: 'إجمالي المستخدمين',
      value: statistics.total_users?.toLocaleString('ar-SA') || 0,
      icon: <Users size={24} />,
      color: '#3B82F6',
    },
    {
      title: 'زيارات مشبوهة',
      value: statistics.suspicious_visits?.toLocaleString('ar-SA') || 0,
      icon: <AlertTriangle size={24} />,
      color: '#EF4444',
    },
    {
      title: 'استخدام أجهزة متعددة',
      value: statistics.device_reuse_count?.toLocaleString('ar-SA') || 0,
      icon: <Smartphone size={24} />,
      color: '#F59E0B',
    },
  ]

  return (
    <div className="stats-grid">
      {stats.map((stat, index) => (
        <div key={index} className="stat-card" style={{ borderRightColor: stat.color }}>
          <div className="stat-card-title">{stat.title}</div>
          <div className="stat-card-value" style={{ color: stat.color }}>
            {stat.value}
          </div>
          <div style={{ marginTop: '0.5rem', color: stat.color }}>
            {stat.icon}
          </div>
        </div>
      ))}
    </div>
  )
}

export default StatsCards

