import React, { useState, useEffect } from 'react'
import { adminAPI } from '../services/api'
import StatsCards from '../components/StatsCards'
import QuickStats from '../components/QuickStats'
import DashboardCharts from '../components/DashboardCharts'
import Filters from '../components/Filters'
import VisitsTable from '../components/VisitsTable'
import ErrorDisplay from '../components/ErrorDisplay'
import { Shield } from 'lucide-react'

function Dashboard() {
  const [visits, setVisits] = useState([])
  const [statistics, setStatistics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [filters, setFilters] = useState({
    national_id_hash: '',
    branch_id: '',
    start_date: '',
    end_date: '',
    risk_level: '',
    auth_method: '',
  })

  useEffect(() => {
    loadData()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.national_id_hash, filters.branch_id, filters.start_date, filters.end_date, filters.risk_level, filters.auth_method])

  const loadData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Check if backend is available first
      try {
        await fetch('http://localhost:8000/health')
      } catch (e) {
        setError('الخادم الخلفي غير متاح. تأكد من تشغيل: python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000')
        setLoading(false)
        return
      }
      
      const [visitsData, statsData] = await Promise.all([
        adminAPI.getVisits(filters),
        adminAPI.getStatistics(),
      ])
      console.log('Visits data:', visitsData)
      console.log('Statistics data:', statsData)
      setVisits(visitsData.visits || [])
      setStatistics(statsData)
    } catch (error) {
      console.error('Error loading data:', error)
      setError(error.message || 'حدث خطأ في تحميل البيانات. تحقق من أن الخادم يعمل على port 8000')
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }))
  }

  const clearFilters = () => {
    setFilters({
      national_id_hash: '',
      branch_id: '',
      start_date: '',
      end_date: '',
      risk_level: '',
      auth_method: '',
    })
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>
          <Shield size={32} />
          لوحة التحكم الإدارية - نظام أبشر
        </h1>
      </header>

      <div className="dashboard-content">
        {error ? (
          <ErrorDisplay error={error} onRetry={loadData} />
        ) : (
          <>
            {/* Main Stats Cards */}
            {statistics && <StatsCards statistics={statistics} />}
            
            {/* Quick Stats */}
            {statistics && <QuickStats statistics={statistics} />}
            
            {/* Dashboard Charts - Visual Analytics */}
            {statistics && <DashboardCharts statistics={statistics} />}
            
            {/* Filters Section */}
            <Filters
              filters={filters}
              onFilterChange={handleFilterChange}
              onClear={clearFilters}
            />
            
            {/* Visits Table - Detailed List */}
            {loading ? (
              <div className="loading-container">
                <div className="loading-spinner"></div>
                <p>جاري تحميل البيانات...</p>
              </div>
            ) : (
              <VisitsTable visits={visits} loading={false} onVisitsUpdate={setVisits} />
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default Dashboard

