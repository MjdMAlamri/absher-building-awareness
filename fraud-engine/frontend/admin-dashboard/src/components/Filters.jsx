import React from 'react'
import { Filter, X } from 'lucide-react'

function Filters({ filters, onFilterChange, onClear }) {
  const hasActiveFilters = Object.values(filters).some(v => v !== '')

  return (
    <div className="filters-section">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <div>
          <h3 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#00A859', margin: 0 }}>
            <Filter size={20} />
            فلاتر البحث
          </h3>
          <p style={{ fontSize: '0.75rem', color: '#6B7280', margin: '0.25rem 0 0 0' }}>
            جميع الفلاتر اختيارية - يمكنك استخدام واحد أو أكثر
          </p>
        </div>
        {hasActiveFilters && (
          <button
            onClick={onClear}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '0.5rem 1rem',
              background: '#EF4444',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '0.875rem',
            }}
          >
            <X size={16} />
            مسح الفلاتر
          </button>
        )}
      </div>

      <div className="filters-grid">
        <div className="filter-group">
          <label className="filter-label">رقم الهوية (Hash)</label>
          <input
            type="text"
            className="filter-input"
            placeholder="ابحث برقم الهوية..."
            value={filters.national_id_hash}
            onChange={(e) => onFilterChange('national_id_hash', e.target.value)}
          />
        </div>

        <div className="filter-group">
          <label className="filter-label">الفرع</label>
          <input
            type="text"
            className="filter-input"
            placeholder="مثال: Riyadh-Branch, Hail-Branch, Qassim-Branch"
            value={filters.branch_id}
            onChange={(e) => onFilterChange('branch_id', e.target.value)}
          />
        </div>

        <div className="filter-group">
          <label className="filter-label">مستوى الخطر</label>
          <select
            className="filter-select"
            value={filters.risk_level}
            onChange={(e) => onFilterChange('risk_level', e.target.value)}
          >
            <option value="">الكل</option>
            <option value="low">منخفض</option>
            <option value="medium">متوسط</option>
            <option value="high">عالي</option>
            <option value="critical">حرج</option>
          </select>
        </div>

        <div className="filter-group">
          <label className="filter-label">طريقة المصادقة</label>
          <select
            className="filter-select"
            value={filters.auth_method}
            onChange={(e) => onFilterChange('auth_method', e.target.value)}
          >
            <option value="">الكل</option>
            <option value="face+fingerprint">بصمة + وجه</option>
            <option value="nafath">نفاذ</option>
            <option value="biometric_only">بيومترية فقط</option>
          </select>
        </div>

        <div className="filter-group">
          <label className="filter-label">من تاريخ</label>
          <input
            type="date"
            className="filter-input"
            value={filters.start_date}
            onChange={(e) => onFilterChange('start_date', e.target.value)}
          />
        </div>

        <div className="filter-group">
          <label className="filter-label">إلى تاريخ</label>
          <input
            type="date"
            className="filter-input"
            value={filters.end_date}
            onChange={(e) => onFilterChange('end_date', e.target.value)}
          />
        </div>
      </div>
    </div>
  )
}

export default Filters

