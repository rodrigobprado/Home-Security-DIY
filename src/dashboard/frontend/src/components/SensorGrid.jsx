import useStore from '../store/useStore'

const SENSORS = [
  { id: 'binary_sensor.porta_entrada',      label: 'Porta Entrada',  icon: '🚪' },
  { id: 'binary_sensor.porta_fundos',       label: 'Porta Fundos',   icon: '🚪' },
  { id: 'binary_sensor.janela_sala',        label: 'Janela Sala',    icon: '🪟' },
  { id: 'binary_sensor.pir_sala_occupancy', label: 'PIR Sala',       icon: '👁' },
  { id: 'binary_sensor.pir_corredor',       label: 'PIR Corredor',   icon: '👁' },
  { id: 'binary_sensor.zigbee2mqtt_connection_state', label: 'Zigbee', icon: '📡' },
]

function SensorCard({ id, label, icon }) {
  const { states } = useStore()
  const state = states[id]?.state ?? 'unavailable'
  const isActive = state === 'on'
  const isUnavailable = state === 'unavailable'
  let cardClasses = 'border-border bg-surface'
  let stateTextClass = 'text-success'
  let stateText = 'ok'
  let dotClass = 'bg-success'

  if (isUnavailable) {
    cardClasses = 'border-border bg-surface/50 opacity-50'
    stateTextClass = 'text-muted'
    stateText = 'offline'
    dotClass = 'bg-gray-600'
  } else if (isActive) {
    cardClasses = 'border-warning bg-yellow-900/20'
    stateTextClass = 'text-warning'
    stateText = 'aberto / detectado'
    dotClass = 'bg-warning'
  }

  return (
    <div className={`flex items-center gap-3 p-3 rounded-lg border transition-colors ${cardClasses}`}>
      <span className="text-xl">{icon}</span>
      <div className="min-w-0 flex-1">
        <p className="text-xs text-muted truncate">{label}</p>
        <p className={`text-sm font-medium ${stateTextClass}`}>{stateText}</p>
      </div>
      <span className={`status-dot ${dotClass}`} />
    </div>
  )
}

export default function SensorGrid() {
  return (
    <div className="card flex flex-col gap-2">
      <h2 className="text-xs font-semibold uppercase tracking-wider text-muted mb-1">Sensores</h2>
      {SENSORS.map((s) => (
        <SensorCard key={s.id} {...s} />
      ))}
    </div>
  )
}
