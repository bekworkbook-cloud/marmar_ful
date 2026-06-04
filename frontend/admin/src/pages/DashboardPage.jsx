import { useEffect } from 'react'
import useAdminStore from '../store/useAdminStore'

const STATUS_CONFIG = {
  new:       { label: 'Новые',     color: '#3B82F6', bg: 'rgba(59,130,246,0.12)' },
  preparing: { label: 'Готовится', color: '#F59E0B', bg: 'rgba(245,158,11,0.12)' },
  delivered: { label: 'Доставлен', color: '#10B981', bg: 'rgba(16,185,129,0.12)' },
  cancelled: { label: 'Отменён',   color: '#EF4444', bg: 'rgba(239,68,68,0.12)'  },
}

const fmt = (n) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(n)

const timeAgo = (dateStr) => {
  if (!dateStr) return ''
  const diff = Math.floor((Date.now() - new Date(dateStr)) / 60000)
  if (diff < 1)  return 'только что'
  if (diff < 60) return `${diff} мин назад`
  const h = Math.floor(diff / 60)
  if (h < 24)   return `${h} ч назад`
  return `${Math.floor(h / 24)} дн назад`
}

export default function DashboardPage() {
  const { fetchOrders, fetchBranches, orders, branches, loading, totalRevenue, avgOrderValue, ordersByStatus } = useAdminStore()

  useEffect(() => {
    fetchBranches()
    fetchOrders({ limit: 50, offset: 0 })
  }, [])

  const revenue     = totalRevenue()
  const avg         = avgOrderValue()
  const byStatus    = ordersByStatus()
  const recentOrders = [...orders]
    .sort((a, b) => b.id - a.id)
    .slice(0, 8)

  const statusCounts = Object.entries(STATUS_CONFIG).map(([key, cfg]) => ({
    key,
    ...cfg,
    count: byStatus[key]?.length ?? 0,
  }))

  const tg = window.Telegram?.WebApp
  const adminName = tg?.initDataUnsafe?.user?.first_name ?? 'Админ'

  return (
    <div style={styles.page}>

      {/* header */}
      <div style={styles.header}>
        <div>
          <p style={styles.greeting}>Привет, {adminName} 👋</p>
          <p style={styles.subtitle}>Обзор на сегодня</p>
        </div>
        <div style={styles.avatar}>
          {adminName[0]?.toUpperCase()}
        </div>
      </div>

      {loading && <div style={styles.loader}>Загрузка...</div>}

      {/* metric cards */}
      <div style={styles.metricsGrid}>
        <div style={styles.metricCard}>
          <p style={styles.metricLabel}>Выручка</p>
          <p style={styles.metricValue}>{fmt(revenue)}</p>
          <p style={styles.metricSub}>{orders.length} заказов</p>
        </div>
        <div style={styles.metricCard}>
          <p style={styles.metricLabel}>Средний чек</p>
          <p style={styles.metricValue}>{fmt(avg)}</p>
          <p style={styles.metricSub}>за заказ</p>
        </div>
      </div>

      {/* status breakdown */}
      <p style={styles.sectionTitle}>Заказы по статусам</p>
      <div style={styles.statusGrid}>
        {statusCounts.map(s => (
          <div key={s.key} style={{ ...styles.statusCard, background: s.bg }}>
            <p style={{ ...styles.statusCount, color: s.color }}>{s.count}</p>
            <p style={{ ...styles.statusLabel, color: s.color }}>{s.label}</p>
          </div>
        ))}
      </div>

      {/* recent orders */}
      <p style={styles.sectionTitle}>Последние заказы</p>
      <div style={styles.ordersList}>
        {recentOrders.length === 0 && !loading && (
          <p style={styles.empty}>Заказов пока нет</p>
        )}
        {recentOrders.map(order => {
          const cfg = STATUS_CONFIG[order.status] ?? { label: order.status, color: '#888', bg: 'rgba(128,128,128,0.1)' }
          return (
            <div key={order.id} style={styles.orderRow}>
              <div style={styles.orderLeft}>
                <p style={styles.orderId}>#{order.id}</p>
                <p style={styles.orderAddr} numberOfLines={1}>{order.address}</p>
              </div>
              <div style={styles.orderRight}>
                <span style={{ ...styles.badge, background: cfg.bg, color: cfg.color }}>
                  {cfg.label}
                </span>
                <p style={styles.orderPrice}>{fmt(order.total_price)}</p>
              </div>
            </div>
          )
        })}
      </div>

    </div>
  )
}

const C = {
  bg:       '#0F0F0F',
  surface:  '#1A1A1A',
  surface2: '#242424',
  border:   'rgba(255,255,255,0.07)',
  text:     '#F2F2F2',
  muted:    '#8A8A8A',
  accent:   '#3B82F6',
}

const styles = {
  page: {
    minHeight: '100vh',
    background: C.bg,
    padding: '16px 16px 80px',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    color: C.text,
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 24,
    paddingTop: 8,
  },
  greeting: {
    margin: 0,
    fontSize: 20,
    fontWeight: 600,
    color: C.text,
  },
  subtitle: {
    margin: '4px 0 0',
    fontSize: 13,
    color: C.muted,
  },
  avatar: {
    width: 40,
    height: 40,
    borderRadius: '50%',
    background: 'rgba(59,130,246,0.2)',
    border: `1px solid rgba(59,130,246,0.4)`,
    color: C.accent,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 16,
    fontWeight: 600,
  },
  loader: {
    textAlign: 'center',
    color: C.muted,
    fontSize: 13,
    marginBottom: 16,
  },
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, minmax(0, 1fr))',
    gap: 12,
    marginBottom: 28,
  },
  metricCard: {
    background: C.surface,
    border: `0.5px solid ${C.border}`,
    borderRadius: 16,
    padding: '16px 14px',
  },
  metricLabel: {
    margin: '0 0 6px',
    fontSize: 12,
    color: C.muted,
    textTransform: 'uppercase',
    letterSpacing: '0.06em',
  },
  metricValue: {
    margin: '0 0 4px',
    fontSize: 18,
    fontWeight: 700,
    color: C.text,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  metricSub: {
    margin: 0,
    fontSize: 12,
    color: C.muted,
  },
  sectionTitle: {
    margin: '0 0 12px',
    fontSize: 15,
    fontWeight: 600,
    color: C.text,
  },
  statusGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, minmax(0, 1fr))',
    gap: 10,
    marginBottom: 28,
  },
  statusCard: {
    borderRadius: 14,
    padding: '14px 16px',
    display: 'flex',
    flexDirection: 'column',
    gap: 4,
  },
  statusCount: {
    margin: 0,
    fontSize: 28,
    fontWeight: 700,
    lineHeight: 1,
  },
  statusLabel: {
    margin: 0,
    fontSize: 13,
    fontWeight: 500,
  },
  ordersList: {
    display: 'flex',
    flexDirection: 'column',
    gap: 8,
  },
  orderRow: {
    background: C.surface,
    border: `0.5px solid ${C.border}`,
    borderRadius: 14,
    padding: '12px 14px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    gap: 12,
  },
  orderLeft: {
    flex: 1,
    minWidth: 0,
  },
  orderId: {
    margin: '0 0 4px',
    fontSize: 14,
    fontWeight: 600,
    color: C.text,
  },
  orderAddr: {
    margin: 0,
    fontSize: 12,
    color: C.muted,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  orderRight: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-end',
    gap: 6,
    flexShrink: 0,
  },
  badge: {
    fontSize: 11,
    fontWeight: 600,
    padding: '3px 8px',
    borderRadius: 6,
    whiteSpace: 'nowrap',
  },
  orderPrice: {
    margin: 0,
    fontSize: 13,
    fontWeight: 600,
    color: C.text,
  },
  empty: {
    textAlign: 'center',
    color: C.muted,
    fontSize: 14,
    padding: '24px 0',
  },
}