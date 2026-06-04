import { useEffect, useState } from 'react'
import useAdminStore from '../store/useAdminStore'

// ─── constants ───────────────────────────────────────────────────────────────

const STATUS_CONFIG = {
  pending:               { label: 'Ожидает оплаты',       color: '#8B5CF6', bg: 'rgba(139,92,246,0.12)' },
  awaiting_confirmation: { label: 'Ожидает подтверждения', color: '#F59E0B', bg: 'rgba(245,158,11,0.12)' },
  confirmed:             { label: 'Подтверждён',           color: '#3B82F6', bg: 'rgba(59,130,246,0.12)' },
  preparing:             { label: 'Готовится',             color: '#06B6D4', bg: 'rgba(6,182,212,0.12)'  },
  in_transit:            { label: 'В пути',                color: '#F97316', bg: 'rgba(249,115,22,0.12)' },
  delivered:             { label: 'Доставлен',             color: '#10B981', bg: 'rgba(16,185,129,0.12)' },
  closed:                { label: 'Закрыт',                color: '#6B7280', bg: 'rgba(107,114,128,0.12)'},
  cancelled:             { label: 'Отменён',               color: '#EF4444', bg: 'rgba(239,68,68,0.12)'  },
}

// следующие статусы для кнопок смены статуса
const NEXT_STATUSES = {
  pending:               ['awaiting_confirmation', 'cancelled'],
  awaiting_confirmation: ['confirmed', 'cancelled'],
  confirmed:             ['preparing', 'cancelled'],
  preparing:             ['in_transit', 'cancelled'],
  in_transit:            ['delivered', 'cancelled'],
  delivered:             ['closed'],
  closed:                [],
  cancelled:             [],
}

const ALL_FILTER = '__all__'

const fmt = (n) =>
  new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'UZS', maximumFractionDigits: 0 }).format(n ?? 0)

// ─── OrderModal ───────────────────────────────────────────────────────────────

function OrderModal({ order, onClose }) {
  const {
    updateOrderStatus, assignCourier, assignOperator, acceptOrder,
    fetchOrderItems, staffByRole, token,
  } = useAdminStore()

  const [items, setItems]           = useState([])
  const [itemsLoading, setItemsLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState(false)
  const [localOrder, setLocalOrder] = useState(order)

  const couriers  = staffByRole('courier')
  const operators = staffByRole('operator')

  useEffect(() => {
    fetchOrderItems(order.id)
      .then(data => setItems(data?.order_items ?? []))
      .catch(() => setItems([]))
      .finally(() => setItemsLoading(false))
  }, [order.id])

  const wrap = async (fn) => {
    setActionLoading(true)
    try {
      const updated = await fn()
      if (updated) setLocalOrder(updated)
    } finally {
      setActionLoading(false)
    }
  }

  const cfg = STATUS_CONFIG[localOrder.status] ?? { label: localOrder.status, color: '#888', bg: 'rgba(128,128,128,0.1)' }
  const nextStatuses = NEXT_STATUSES[localOrder.status] ?? []

  return (
    <div style={M.overlay} onClick={onClose}>
      <div style={M.sheet} onClick={e => e.stopPropagation()}>

        {/* handle */}
        <div style={M.handle} />

        {/* header */}
        <div style={M.header}>
          <div>
            <p style={M.orderId}>Заказ #{localOrder.id}</p>
            <span style={{ ...M.badge, background: cfg.bg, color: cfg.color }}>{cfg.label}</span>
          </div>
          <button style={M.closeBtn} onClick={onClose}>✕</button>
        </div>

        <div style={M.body}>

          {/* info rows */}
          <div style={M.infoBlock}>
            <Row icon="📍" label="Адрес" value={localOrder.address} />
            {localOrder.landmark && <Row icon="🏷️" label="Ориентир" value={localOrder.landmark} />}
            <Row icon="💳" label="Оплата" value={localOrder.payment_method} />
            <Row icon="💰" label="Сумма" value={fmt(localOrder.total_price)} />
            <Row
              icon="✅"
              label="Принят рестораном"
              value={localOrder.is_accepted ? 'Да' : 'Нет'}
              valueColor={localOrder.is_accepted ? '#10B981' : '#F59E0B'}
            />
          </div>

          {/* accept / reject */}
          {!localOrder.is_accepted && (
            <div style={M.section}>
              <p style={M.sectionTitle}>Подтверждение</p>
              <div style={M.row2}>
                <button
                  style={{ ...M.btn, ...M.btnSuccess }}
                  disabled={actionLoading}
                  onClick={() => wrap(() => acceptOrder(localOrder.id, true))}
                >
                  Принять
                </button>
                <button
                  style={{ ...M.btn, ...M.btnDanger }}
                  disabled={actionLoading}
                  onClick={() => wrap(() => acceptOrder(localOrder.id, false))}
                >
                  Отклонить
                </button>
              </div>
            </div>
          )}

          {/* change status */}
          {nextStatuses.length > 0 && (
            <div style={M.section}>
              <p style={M.sectionTitle}>Сменить статус</p>
              <div style={M.statusBtns}>
                {nextStatuses.map(s => {
                  const c = STATUS_CONFIG[s]
                  return (
                    <button
                      key={s}
                      disabled={actionLoading}
                      style={{ ...M.statusBtn, background: c.bg, color: c.color, borderColor: c.color + '40' }}
                      onClick={() => wrap(() => updateOrderStatus(localOrder.id, s))}
                    >
                      {c.label}
                    </button>
                  )
                })}
              </div>
            </div>
          )}

          {/* assign courier */}
          <div style={M.section}>
            <p style={M.sectionTitle}>Курьер</p>
            <select
              style={M.select}
              value={localOrder.courier_id ?? ''}
              disabled={actionLoading}
              onChange={e => {
                const id = Number(e.target.value)
                if (id) wrap(() => assignCourier(localOrder.id, id))
              }}
            >
              <option value="">— Не назначен —</option>
              {couriers.map(c => (
                <option key={c.id} value={c.id}>
                  {c.first_name ?? c.username ?? `Курьер #${c.id}`}
                </option>
              ))}
            </select>
          </div>

          {/* assign operator */}
          <div style={M.section}>
            <p style={M.sectionTitle}>Оператор</p>
            <select
              style={M.select}
              value={localOrder.operator_id ?? ''}
              disabled={actionLoading}
              onChange={e => {
                const id = Number(e.target.value)
                if (id) wrap(() => assignOperator(localOrder.id, id))
              }}
            >
              <option value="">— Не назначен —</option>
              {operators.map(o => (
                <option key={o.id} value={o.id}>
                  {o.first_name ?? o.username ?? `Оператор #${o.id}`}
                </option>
              ))}
            </select>
          </div>

          {/* order items */}
          <div style={M.section}>
            <p style={M.sectionTitle}>Состав заказа</p>
            {itemsLoading ? (
              <p style={M.muted}>Загрузка...</p>
            ) : items.length === 0 ? (
              <p style={M.muted}>Позиции не найдены</p>
            ) : (
              items.map(item => (
                <div key={item.id} style={M.itemRow}>
                  <p style={M.itemName}>Продукт #{item.product_id}</p>
                  <div style={M.itemRight}>
                    <p style={M.itemQty}>× {item.quantity}</p>
                    <p style={M.itemPrice}>{fmt(item.price_at_purchase * item.quantity)}</p>
                  </div>
                </div>
              ))
            )}
          </div>

        </div>
      </div>
    </div>
  )
}

function Row({ icon, label, value, valueColor }) {
  return (
    <div style={M.infoRow}>
      <span style={M.infoIcon}>{icon}</span>
      <span style={M.infoLabel}>{label}</span>
      <span style={{ ...M.infoValue, color: valueColor ?? C.text }}>{value}</span>
    </div>
  )
}

// ─── OrdersPage ───────────────────────────────────────────────────────────────

export default function OrdersPage() {
  const { fetchOrders, fetchStaff, orders, loading } = useAdminStore()
  const [filter, setFilter]       = useState(ALL_FILTER)
  const [selected, setSelected]   = useState(null)

  useEffect(() => {
    fetchOrders({ limit: 100, offset: 0 })
    fetchStaff({ limit: 100, offset: 0 })
  }, [])

  const filtered = filter === ALL_FILTER
    ? orders
    : orders.filter(o => o.status === filter)

  const sorted = [...filtered].sort((a, b) => b.id - a.id)

  return (
    <div style={S.page}>

      <p style={S.pageTitle}>Заказы</p>

      {/* filter tabs */}
      <div style={S.tabs}>
        <button
          style={{ ...S.tab, ...(filter === ALL_FILTER ? S.tabActive : {}) }}
          onClick={() => setFilter(ALL_FILTER)}
        >
          Все ({orders.length})
        </button>
        {Object.entries(STATUS_CONFIG).map(([key, cfg]) => {
          const count = orders.filter(o => o.status === key).length
          if (count === 0) return null
          return (
            <button
              key={key}
              style={{
                ...S.tab,
                ...(filter === key ? { ...S.tabActive, background: cfg.bg, color: cfg.color, borderColor: cfg.color + '40' } : {}),
              }}
              onClick={() => setFilter(key)}
            >
              {cfg.label} ({count})
            </button>
          )
        })}
      </div>

      {/* list */}
      {loading && <p style={S.muted}>Загрузка...</p>}

      <div style={S.list}>
        {sorted.length === 0 && !loading && (
          <p style={S.muted}>Нет заказов</p>
        )}
        {sorted.map(order => {
          const cfg = STATUS_CONFIG[order.status] ?? { label: order.status, color: '#888', bg: 'rgba(128,128,128,0.1)' }
          return (
            <div key={order.id} style={S.card} onClick={() => setSelected(order)}>
              <div style={S.cardTop}>
                <div style={S.cardLeft}>
                  <p style={S.cardId}>#{order.id}</p>
                  <p style={S.cardAddr}>{order.address}</p>
                </div>
                <div style={S.cardRight}>
                  <span style={{ ...S.badge, background: cfg.bg, color: cfg.color }}>{cfg.label}</span>
                  <p style={S.cardPrice}>{fmt(order.total_price)}</p>
                </div>
              </div>
              <div style={S.cardBottom}>
                <span style={S.cardMeta}>
                  {order.is_accepted ? '✅ Принят' : '⏳ Не принят'}
                </span>
                {order.courier_id && (
                  <span style={S.cardMeta}>🚴 Курьер #{order.courier_id}</span>
                )}
                {order.operator_id && (
                  <span style={S.cardMeta}>🎧 Оператор #{order.operator_id}</span>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {selected && (
        <OrderModal order={selected} onClose={() => setSelected(null)} />
      )}
    </div>
  )
}

// ─── styles ───────────────────────────────────────────────────────────────────

const C = {
  bg:      '#0F0F0F',
  surface: '#1A1A1A',
  border:  'rgba(255,255,255,0.07)',
  text:    '#F2F2F2',
  muted:   '#8A8A8A',
}

const S = {
  page: {
    minHeight: '100vh',
    background: C.bg,
    padding: '16px 16px 80px',
    fontFamily: 'system-ui, -apple-system, sans-serif',
    color: C.text,
  },
  pageTitle: {
    fontSize: 20,
    fontWeight: 700,
    marginBottom: 16,
  },
  tabs: {
    display: 'flex',
    gap: 8,
    overflowX: 'auto',
    paddingBottom: 12,
    marginBottom: 16,
    scrollbarWidth: 'none',
  },
  tab: {
    flexShrink: 0,
    fontSize: 12,
    fontWeight: 500,
    padding: '6px 12px',
    borderRadius: 20,
    border: `0.5px solid ${C.border}`,
    background: C.surface,
    color: C.muted,
    cursor: 'pointer',
    whiteSpace: 'nowrap',
  },
  tabActive: {
    background: 'rgba(59,130,246,0.12)',
    color: '#3B82F6',
    borderColor: 'rgba(59,130,246,0.3)',
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: 10,
  },
  card: {
    background: C.surface,
    border: `0.5px solid ${C.border}`,
    borderRadius: 14,
    padding: '12px 14px',
    cursor: 'pointer',
  },
  cardTop: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    gap: 10,
    marginBottom: 8,
  },
  cardLeft: { flex: 1, minWidth: 0 },
  cardId: { fontSize: 14, fontWeight: 700, marginBottom: 3 },
  cardAddr: { fontSize: 12, color: C.muted, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' },
  cardRight: { display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: 5, flexShrink: 0 },
  badge: { fontSize: 10, fontWeight: 600, padding: '3px 8px', borderRadius: 6, whiteSpace: 'nowrap' },
  cardPrice: { fontSize: 13, fontWeight: 600 },
  cardBottom: { display: 'flex', gap: 10, flexWrap: 'wrap' },
  cardMeta: { fontSize: 11, color: C.muted },
  muted: { color: C.muted, fontSize: 13, textAlign: 'center', padding: '20px 0' },
}

const M = {
  overlay: {
    position: 'fixed', inset: 0,
    background: 'rgba(0,0,0,0.7)',
    zIndex: 100,
    display: 'flex',
    alignItems: 'flex-end',
  },
  sheet: {
    width: '100%',
    background: '#161616',
    borderRadius: '20px 20px 0 0',
    maxHeight: '90vh',
    display: 'flex',
    flexDirection: 'column',
    overflow: 'hidden',
  },
  handle: {
    width: 36, height: 4,
    background: 'rgba(255,255,255,0.15)',
    borderRadius: 2,
    margin: '12px auto 0',
    flexShrink: 0,
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    padding: '12px 16px 12px',
    borderBottom: '0.5px solid rgba(255,255,255,0.07)',
    flexShrink: 0,
  },
  orderId: { fontSize: 17, fontWeight: 700, marginBottom: 6 },
  badge: { fontSize: 11, fontWeight: 600, padding: '4px 10px', borderRadius: 8 },
  closeBtn: {
    background: 'rgba(255,255,255,0.08)',
    border: 'none',
    color: '#aaa',
    width: 30, height: 30,
    borderRadius: '50%',
    cursor: 'pointer',
    fontSize: 14,
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    flexShrink: 0,
  },
  body: {
    overflowY: 'auto',
    padding: '4px 16px 32px',
    flex: 1,
  },
  infoBlock: {
    background: '#1E1E1E',
    borderRadius: 12,
    padding: '4px 0',
    marginBottom: 16,
    marginTop: 12,
  },
  infoRow: {
    display: 'flex',
    alignItems: 'center',
    gap: 10,
    padding: '9px 14px',
    borderBottom: '0.5px solid rgba(255,255,255,0.05)',
  },
  infoIcon: { fontSize: 14, flexShrink: 0 },
  infoLabel: { fontSize: 12, color: '#8A8A8A', flex: 1 },
  infoValue: { fontSize: 13, fontWeight: 500, textAlign: 'right' },
  section: { marginBottom: 16 },
  sectionTitle: { fontSize: 12, color: '#8A8A8A', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 8 },
  row2: { display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0,1fr))', gap: 8 },
  btn: {
    padding: '10px 0',
    borderRadius: 10,
    border: 'none',
    fontSize: 13,
    fontWeight: 600,
    cursor: 'pointer',
  },
  btnSuccess: { background: 'rgba(16,185,129,0.15)', color: '#10B981' },
  btnDanger:  { background: 'rgba(239,68,68,0.15)',  color: '#EF4444' },
  statusBtns: { display: 'flex', flexWrap: 'wrap', gap: 8 },
  statusBtn: {
    padding: '8px 14px',
    borderRadius: 10,
    border: '0.5px solid',
    fontSize: 12,
    fontWeight: 600,
    cursor: 'pointer',
  },
  select: {
    width: '100%',
    background: '#1E1E1E',
    border: '0.5px solid rgba(255,255,255,0.1)',
    borderRadius: 10,
    color: '#F2F2F2',
    fontSize: 13,
    padding: '10px 12px',
  },
  itemRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '8px 0',
    borderBottom: '0.5px solid rgba(255,255,255,0.05)',
  },
  itemName: { fontSize: 13, color: '#F2F2F2' },
  itemRight: { display: 'flex', alignItems: 'center', gap: 12 },
  itemQty: { fontSize: 12, color: '#8A8A8A' },
  itemPrice: { fontSize: 13, fontWeight: 600 },
  muted: { fontSize: 13, color: '#8A8A8A' },
  text: '#F2F2F2',
}