import { useEffect, useState } from 'react'
import useStore from '../store/useStore'

// Posições padrão dos dispositivos (x/y em % sobre o mapa)
// Editáveis via banco de dados (tabela dashboard.device_positions)
const DEFAULT_DEVICES = [
  { entity_id: 'camera.cam_entrada',           label: 'Câm Entrada',  x: 50,  y: 5,  device_type: 'camera' },
  { entity_id: 'camera.cam_fundos',            label: 'Câm Fundos',   x: 50,  y: 95, device_type: 'camera' },
  { entity_id: 'camera.cam_garagem',           label: 'Câm Garagem',  x: 90,  y: 50, device_type: 'camera' },
  { entity_id: 'camera.cam_lateral',           label: 'Câm Lateral',  x: 10,  y: 50, device_type: 'camera' },
  { entity_id: 'binary_sensor.porta_entrada',  label: 'Porta Entrada',x: 50,  y: 10, device_type: 'sensor' },
  { entity_id: 'binary_sensor.porta_fundos',   label: 'Porta Fundos', x: 50,  y: 90, device_type: 'sensor' },
  { entity_id: 'binary_sensor.pir_sala_occupancy', label: 'PIR Sala', x: 35,  y: 45, device_type: 'sensor' },
  { entity_id: 'binary_sensor.pir_corredor',   label: 'PIR Corredor', x: 65,  y: 45, device_type: 'sensor' },
]

const ICONS = { camera: '📷', sensor: '🔵', siren: '🔔', drone: '🤖' }

const ACTIVE_ENTITIES = new Set([
  'binary_sensor.porta_entrada',
  'binary_sensor.porta_fundos',
  'binary_sensor.janela_sala',
  'binary_sensor.pir_sala_occupancy',
  'binary_sensor.pir_corredor',
])

export default function OperationalMap() {
  const { states } = useStore()
  const [devices, setDevices] = useState(DEFAULT_DEVICES)

  // Tenta carregar posições do banco de dados
  useEffect(() => {
    fetch('/api/map/devices')
      .then((r) => r.json())
      .then((data) => { if (Array.isArray(data) && data.length > 0) setDevices(data) })
      .catch(() => {})
  }, [])

  return (
    <div className="card flex flex-col gap-2 h-full">
      <h2 className="text-xs font-semibold uppercase tracking-wider text-muted">Mapa Operacional</h2>

      {/* Área do mapa */}
      <div
        className="relative flex-1 rounded-lg overflow-hidden bg-gray-900 border border-border"
        style={{ minHeight: '300px' }}
      >
        {/* Grade de referência */}
        <svg className="absolute inset-0 w-full h-full opacity-10" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#4b5563" strokeWidth="0.5" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>

        {/* Planta baixa placeholder */}
        <svg className="absolute inset-0 w-full h-full opacity-30" xmlns="http://www.w3.org/2000/svg">
          {/* Perímetro externo */}
          <rect x="10%" y="10%" width="80%" height="80%" fill="none" stroke="#3b82f6" strokeWidth="2" />
          {/* Divisões internas */}
          <line x1="10%" y1="55%" x2="90%" y2="55%" stroke="#3b82f6" strokeWidth="1" strokeDasharray="4 4" />
          <line x1="50%" y1="10%" x2="50%" y2="55%" stroke="#3b82f6" strokeWidth="1" strokeDasharray="4 4" />
          {/* Labels */}
          <text x="30%" y="35%" fill="#6b7280" fontSize="10" textAnchor="middle">Sala / Cozinha</text>
          <text x="70%" y="35%" fill="#6b7280" fontSize="10" textAnchor="middle">Quartos</text>
          <text x="50%" y="75%" fill="#6b7280" fontSize="10" textAnchor="middle">Área Externa</text>
        </svg>

        {/* Dispositivos sobrepostos */}
        {devices.map((device) => {
          const stateObj = states[device.entity_id]
          const isActive = ACTIVE_ENTITIES.has(device.entity_id) && stateObj?.state === 'on'

          return (
            <div
              key={device.entity_id}
              className="absolute transform -translate-x-1/2 -translate-y-1/2 flex flex-col items-center group cursor-default"
              style={{ left: `${device.x}%`, top: `${device.y}%` }}
              title={`${device.label}: ${stateObj?.state ?? 'desconhecido'}`}
            >
              <span
                className={`text-base transition-transform group-hover:scale-125 ${isActive ? 'filter drop-shadow-[0_0_6px_orange]' : ''}`}
              >
                {ICONS[device.device_type] ?? '●'}
              </span>
              {isActive && (
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-warning rounded-full animate-ping" />
              )}
              <span className="hidden group-hover:block absolute bottom-full mb-1 px-1.5 py-0.5 bg-black/90 text-gray-200 text-xs rounded whitespace-nowrap z-10">
                {device.label}
              </span>
            </div>
          )
        })}
      </div>

      {/* Legenda */}
      <div className="flex gap-4 text-xs text-muted">
        <span>📷 câmera</span>
        <span>🔵 sensor</span>
        <span className="text-warning">⚡ ativo/alerta</span>
      </div>
    </div>
  )
}
