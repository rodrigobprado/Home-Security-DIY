import useStore from '../store/useStore'
import { useAssets } from '../hooks/useAssets'

// Fallback estático — usado quando catálogo dinâmico está vazio
const STATIC_SENSORS = [
  { id: 'binary_sensor.porta_entrada',      label: 'Porta Entrada',  icon: '🚪' },
  { id: 'binary_sensor.porta_fundos',       label: 'Porta Fundos',   icon: '🚪' },
  { id: 'binary_sensor.janela_sala',        label: 'Janela Sala',    icon: '🪟' },
  { id: 'binary_sensor.pir_sala_occupancy', label: 'PIR Sala',       icon: '👁' },
  { id: 'binary_sensor.pir_corredor',       label: 'PIR Corredor',   icon: '👁' },
  { id: 'binary_sensor.zigbee2mqtt_connection_state', label: 'Zigbee', icon: '📡' },
]

function getSensorIcon(asset) {
  const lower = (asset.entity_id + asset.name).toLowerCase()
  if (lower.includes('porta') || lower.includes('door')) return '🚪'
  if (lower.includes('janela') || lower.includes('window')) return '🪟'
  if (lower.includes('pir') || lower.includes('motion')) return '👁'
  if (lower.includes('smoke') || lower.includes('fumaca')) return '🔥'
  if (lower.includes('zigbee')) return '📡'
  return '🔵'
}

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
  const { sensorAssets, assetsLoading } = useAssets()

  // Usa catálogo dinâmico se disponível; fallback estático se vazio
  const sensors = sensorAssets.length > 0
    ? sensorAssets.map((a) => ({
        id: a.entity_id,
        label: a.name,
        icon: getSensorIcon(a),
      }))
    : STATIC_SENSORS

  return (
    <div className="card flex flex-col gap-2">
      <div className="flex items-center justify-between mb-1">
        <h2 className="text-xs font-semibold uppercase tracking-wider text-muted">Sensores</h2>
        {sensorAssets.length > 0 && (
          <span className="text-xs text-accent">{sensorAssets.length} cadastrados</span>
        )}
      </div>
      {assetsLoading && sensorAssets.length === 0 ? (
        <p className="text-xs text-muted text-center py-2">Carregando...</p>
      ) : (
        sensors.map((s) => (
          <SensorCard key={s.id} {...s} />
        ))
      )}
    </div>
  )
}
