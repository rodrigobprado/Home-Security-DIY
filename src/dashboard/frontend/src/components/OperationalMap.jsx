import { useEffect, useMemo, useState } from 'react'
import useStore from '../store/useStore'

const DEFAULT_DEVICES = [
  { entity_id: 'camera.cam_entrada', label: 'Câm Entrada', x: 50, y: 5, device_type: 'camera' },
  { entity_id: 'camera.cam_fundos', label: 'Câm Fundos', x: 50, y: 95, device_type: 'camera' },
  { entity_id: 'camera.cam_garagem', label: 'Câm Garagem', x: 90, y: 50, device_type: 'camera' },
  { entity_id: 'camera.cam_lateral', label: 'Câm Lateral', x: 10, y: 50, device_type: 'camera' },
  { entity_id: 'binary_sensor.porta_entrada', label: 'Porta Entrada', x: 50, y: 10, device_type: 'sensor' },
  { entity_id: 'binary_sensor.porta_fundos', label: 'Porta Fundos', x: 50, y: 90, device_type: 'sensor' },
  { entity_id: 'binary_sensor.pir_sala_occupancy', label: 'PIR Sala', x: 35, y: 45, device_type: 'sensor' },
  { entity_id: 'binary_sensor.pir_corredor', label: 'PIR Corredor', x: 65, y: 45, device_type: 'sensor' },
]

const DEFAULT_GEO_BOUNDS = {
  min_lat: -23.5515,
  max_lat: -23.5495,
  min_lon: -46.6345,
  max_lon: -46.6320,
}

const ACTIVE_ENTITIES = new Set([
  'binary_sensor.porta_entrada',
  'binary_sensor.porta_fundos',
  'binary_sensor.janela_sala',
  'binary_sensor.pir_sala_occupancy',
  'binary_sensor.pir_corredor',
])

const ICONS = { camera: '📷', sensor: '🔵', siren: '🔔', drone: '🤖' }
const UGV_PATROL_PATH = [
  { x: 14, y: 14 },
  { x: 86, y: 14 },
  { x: 86, y: 86 },
  { x: 14, y: 86 },
]
const HISTORY_WINDOW_MS = 24 * 60 * 60 * 1000
const MAX_HISTORY_POINTS = 5000

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value))
}

function parseNum(value) {
  const n = parseFloat(value)
  return Number.isFinite(n) ? n : null
}

function getState(states, entityIds) {
  for (const id of entityIds) {
    if (states[id]?.state !== undefined) return states[id]?.state
  }
  return null
}

function mapLatLonToPercent(lat, lon, bounds) {
  const latSpan = (bounds.max_lat - bounds.min_lat) || 1
  const lonSpan = (bounds.max_lon - bounds.min_lon) || 1
  const x = ((lon - bounds.min_lon) / lonSpan) * 100
  const y = 100 - ((lat - bounds.min_lat) / latSpan) * 100
  return { x: clamp(x, 0, 100), y: clamp(y, 0, 100) }
}

function pruneHistory(points) {
  const minTs = Date.now() - HISTORY_WINDOW_MS
  return points.filter((p) => p.ts >= minTs).slice(-MAX_HISTORY_POINTS)
}

export default function OperationalMap() {
  const { states } = useStore()
  const [devices, setDevices] = useState(DEFAULT_DEVICES)
  const [mapConfig, setMapConfig] = useState({
    floorplan_image_data_url: null,
    geo_bounds: DEFAULT_GEO_BOUNDS,
  })
  const [routeHistory, setRouteHistory] = useState({ ugv: [], uav: [] })
  const [busy, setBusy] = useState(false)
  const [flash, setFlash] = useState('')

  useEffect(() => {
    fetch('/api/map/devices')
      .then((r) => r.json())
      .then((data) => { if (Array.isArray(data) && data.length > 0) setDevices(data) })
      .catch(() => {})

    fetch('/api/map/config')
      .then((r) => r.json())
      .then((cfg) => {
        setMapConfig({
          floorplan_image_data_url: cfg.floorplan_image_data_url || null,
          geo_bounds: cfg.geo_bounds || DEFAULT_GEO_BOUNDS,
        })
      })
      .catch(() => {})
  }, [])

  const uavPosition = useMemo(() => {
    const lat = parseNum(getState(states, ['sensor.uav_latitude', 'binary_sensor.uav_latitude']))
    const lon = parseNum(getState(states, ['sensor.uav_longitude', 'binary_sensor.uav_longitude']))
    if (lat === null || lon === null) return null
    return mapLatLonToPercent(lat, lon, mapConfig.geo_bounds)
  }, [states, mapConfig.geo_bounds])

  const ugvStatus = String(getState(states, ['sensor.ugv_status', 'sensor.ugv_state']) || 'idle').toLowerCase()
  const ugvPosition = useMemo(() => {
    const ugvX = parseNum(getState(states, ['sensor.ugv_x', 'binary_sensor.ugv_x']))
    const ugvY = parseNum(getState(states, ['sensor.ugv_y', 'binary_sensor.ugv_y']))
    if (ugvX !== null && ugvY !== null) {
      return { x: clamp(ugvX, 0, 100), y: clamp(ugvY, 0, 100) }
    }
    const patrol = ugvStatus.includes('patrol')
    if (!patrol) return { x: 14, y: 14 }
    const t = Date.now() / 1000
    const edge = Math.floor((t / 8) % 4)
    const next = (edge + 1) % 4
    const local = (t % 8) / 8
    return {
      x: UGV_PATROL_PATH[edge].x + (UGV_PATROL_PATH[next].x - UGV_PATROL_PATH[edge].x) * local,
      y: UGV_PATROL_PATH[edge].y + (UGV_PATROL_PATH[next].y - UGV_PATROL_PATH[edge].y) * local,
    }
  }, [states, ugvStatus])

  useEffect(() => {
    setRouteHistory((prev) => {
      const now = Date.now()
      const next = {
        ugv: pruneHistory([...prev.ugv, { ...ugvPosition, ts: now }]),
        uav: prev.uav,
      }
      return next
    })
  }, [ugvPosition.x, ugvPosition.y])

  useEffect(() => {
    if (!uavPosition) return
    setRouteHistory((prev) => {
      const now = Date.now()
      const next = {
        ugv: prev.ugv,
        uav: pruneHistory([...prev.uav, { ...uavPosition, ts: now }]),
      }
      return next
    })
  }, [uavPosition?.x, uavPosition?.y])

  async function saveMapConfig(nextConfig) {
    const resp = await fetch('/api/map/config', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nextConfig),
    })
    if (!resp.ok) throw new Error('failed to save map config')
  }

  async function onFloorplanUpload(event) {
    const file = event.target.files?.[0]
    if (!file) return
    const reader = new FileReader()
    reader.onload = async () => {
      const dataUrl = String(reader.result || '')
      if (!dataUrl.startsWith('data:image/')) return
      setMapConfig((prev) => ({ ...prev, floorplan_image_data_url: dataUrl }))
      try {
        await saveMapConfig({ floorplan_image_data_url: dataUrl })
      } catch {
        setFlash('Falha ao salvar planta.')
      }
    }
    reader.readAsDataURL(file)
  }

  async function sendCommand(drone, action) {
    if (busy) return
    setBusy(true)
    setFlash('')
    try {
      const resp = await fetch('/api/drones/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ drone, action }),
      })
      if (!resp.ok) throw new Error('command failed')
      setFlash(`Comando enviado: ${drone.toUpperCase()} ${action}`)
    } catch {
      setFlash('Falha ao enviar comando.')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="card flex flex-col gap-2 h-full">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-xs font-semibold uppercase tracking-wider text-muted">Mapa Operacional</h2>
        <label className="text-xs text-muted cursor-pointer hover:text-gray-200">
          Upload planta
          <input type="file" accept="image/*,.svg" className="hidden" onChange={onFloorplanUpload} />
        </label>
      </div>

      <div className="relative flex-1 rounded-lg overflow-hidden bg-gray-900 border border-border" style={{ minHeight: '320px' }}>
        {mapConfig.floorplan_image_data_url ? (
          <img
            src={mapConfig.floorplan_image_data_url}
            alt="Planta baixa"
            className="absolute inset-0 w-full h-full object-cover opacity-60"
          />
        ) : (
          <svg className="absolute inset-0 w-full h-full opacity-30" xmlns="http://www.w3.org/2000/svg">
            <rect x="10%" y="10%" width="80%" height="80%" fill="none" stroke="#3b82f6" strokeWidth="2" />
            <line x1="10%" y1="55%" x2="90%" y2="55%" stroke="#3b82f6" strokeWidth="1" strokeDasharray="4 4" />
            <line x1="50%" y1="10%" x2="50%" y2="55%" stroke="#3b82f6" strokeWidth="1" strokeDasharray="4 4" />
            <text x="30%" y="35%" fill="#6b7280" fontSize="10" textAnchor="middle">Sala / Cozinha</text>
            <text x="70%" y="35%" fill="#6b7280" fontSize="10" textAnchor="middle">Quartos</text>
            <text x="50%" y="75%" fill="#6b7280" fontSize="10" textAnchor="middle">Área Externa</text>
          </svg>
        )}

        <svg className="absolute inset-0 w-full h-full">
          <polyline
            points={routeHistory.ugv.map((p) => `${p.x},${p.y}`).join(' ')}
            fill="none"
            stroke="#22c55e"
            strokeWidth="0.4"
            strokeOpacity="0.9"
          />
          <polyline
            points={routeHistory.uav.map((p) => `${p.x},${p.y}`).join(' ')}
            fill="none"
            stroke="#38bdf8"
            strokeWidth="0.4"
            strokeOpacity="0.9"
          />
        </svg>

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
              <span className={`text-base transition-transform group-hover:scale-125 ${isActive ? 'filter drop-shadow-[0_0_6px_orange]' : ''}`}>
                {ICONS[device.device_type] ?? '●'}
              </span>
              {isActive && <span className="absolute -top-1 -right-1 w-2 h-2 bg-warning rounded-full animate-ping" />}
            </div>
          )
        })}

        <div className="absolute transform -translate-x-1/2 -translate-y-1/2 text-xl" style={{ left: `${ugvPosition.x}%`, top: `${ugvPosition.y}%` }} title="UGV">
          🤖
        </div>
        {uavPosition && (
          <div className="absolute transform -translate-x-1/2 -translate-y-1/2 text-xl" style={{ left: `${uavPosition.x}%`, top: `${uavPosition.y}%` }} title="UAV">
            🚁
          </div>
        )}
      </div>

      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="rounded border border-border p-2">
          <div className="text-muted mb-1">UGV</div>
          <div className="flex gap-1">
            <button className="btn flex-1 text-xs" disabled={busy} onClick={() => sendCommand('ugv', 'start_patrol')}>Start Patrol</button>
            <button className="btn flex-1 text-xs" disabled={busy} onClick={() => sendCommand('ugv', 'return_home')}>Return</button>
            <button className="btn flex-1 text-xs" disabled={busy} onClick={() => sendCommand('ugv', 'emergency_stop')}>STOP</button>
          </div>
          <div className="mt-1 text-muted">Bateria: {getState(states, ['sensor.ugv_battery']) || '--'}%</div>
        </div>
        <div className="rounded border border-border p-2">
          <div className="text-muted mb-1">UAV</div>
          <div className="flex gap-1">
            <button className="btn flex-1 text-xs" disabled={busy} onClick={() => sendCommand('uav', 'start_patrol')}>Start Patrol</button>
            <button className="btn flex-1 text-xs" disabled={busy} onClick={() => sendCommand('uav', 'return_home')}>Return</button>
            <button className="btn flex-1 text-xs" disabled={busy} onClick={() => sendCommand('uav', 'emergency_stop')}>STOP</button>
          </div>
          <div className="mt-1 text-muted">Bateria: {getState(states, ['sensor.uav_battery']) || '--'}%</div>
        </div>
      </div>

      <div className="flex gap-4 text-xs text-muted">
        <span>🟩 trilha UGV (24h)</span>
        <span>🟦 trilha UAV (24h)</span>
        <span>WebSocket ao vivo</span>
      </div>
      {flash && <div className="text-xs text-muted">{flash}</div>}
    </div>
  )
}
