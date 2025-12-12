import React from 'react'
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp, Users, AlertTriangle } from 'lucide-react'

const COLORS = ['#00A859', '#3B82F6', '#F59E0B', '#EF4444']

function DashboardCharts({ statistics }) {
  if (!statistics) return null

  // Prepare data for charts
  const riskDistributionData = Object.entries(statistics.risk_distribution || {}).map(([name, value]) => ({
    name: name === 'low' ? 'منخفض' : name === 'medium' ? 'متوسط' : name === 'high' ? 'عالي' : 'حرج',
    value: Number(value) || 0,
    label: name
  })).filter(item => item.value > 0)

  const authMethodData = Object.entries(statistics.auth_method_distribution || {}).map(([name, value]) => ({
    name: name === 'face+fingerprint' ? 'بصمة + وجه' : 
          name === 'qr+otp' ? 'QR Code' : 
          name === 'qr_code' ? 'QR Code' :
          name === 'biometric_only' ? 'بيومترية' : 
          name === 'manual_review' ? 'يدوية' : name,
    value: Number(value) || 0
  })).filter(item => item.value > 0)

  const timeSeriesData = [
    { name: 'اليوم', visits: statistics.total_visits || 0, suspicious: statistics.suspicious_visits || 0 },
    { name: 'أمس', visits: Math.floor((statistics.total_visits || 0) * 0.9), suspicious: Math.floor((statistics.suspicious_visits || 0) * 0.85) },
    { name: 'منذ يومين', visits: Math.floor((statistics.total_visits || 0) * 0.8), suspicious: Math.floor((statistics.suspicious_visits || 0) * 0.75) },
  ]

  return (
    <div style={{ marginBottom: '2rem' }}>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '1.5rem' }}>
        {/* Risk Distribution Chart */}
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '1.5rem',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <AlertTriangle size={20} color="#00A859" />
            <h3 style={{ margin: 0, color: '#1F2937', fontWeight: '600' }}>توزيع مستويات الخطر</h3>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={riskDistributionData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {riskDistributionData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Auth Methods Chart */}
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '1.5rem',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <Users size={20} color="#3B82F6" />
            <h3 style={{ margin: 0, color: '#1F2937', fontWeight: '600' }}>طرق المصادقة</h3>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={authMethodData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#00A859" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Time Series Chart */}
        <div style={{
          background: 'white',
          borderRadius: '12px',
          padding: '1.5rem',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
          gridColumn: 'span 2'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <TrendingUp size={20} color="#F59E0B" />
            <h3 style={{ margin: 0, color: '#1F2937', fontWeight: '600' }}>الاتجاهات الزمنية</h3>
          </div>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={timeSeriesData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="visits" stroke="#00A859" strokeWidth={2} name="إجمالي الزيارات" />
              <Line type="monotone" dataKey="suspicious" stroke="#EF4444" strokeWidth={2} name="مشبوهة" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default DashboardCharts

