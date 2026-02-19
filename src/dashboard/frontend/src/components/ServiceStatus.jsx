import { useEffect, useState } from 'react'

const SERVICE_LABELS = {
  home_assistant: 'Home Assistant',
  frigate:        'Frigate NVR',
  ha_websocket:   'HA WebSocket',
}

export default function ServiceStatus() {
  const [services, setServices] = useState({})

  useEffect(() => {
    async function fetch_status() {
      try {
        const resp = await fetch('/api/services/status')
        const data = await resp.json()
        setServices(data.services ?? {})
      } catch {
        setServices({})
      }
    }
    fetch_status()
    const t = setInterval(fetch_status, 30_000)
    return () => clearInterval(t)
  }, [])

  const dotClass = { online: 'status-dot-online', offline: 'status-dot-offline', degraded: 'status-dot-warning', connecting: 'status-dot-warning' }

  return (
    <div className="card">
      <h2 className="text-xs font-semibold uppercase tracking-wider text-muted mb-2">Serviços</h2>
      <div className="flex flex-col gap-2">
        {Object.entries(services).length === 0 ? (
          <p className="text-muted text-xs">Verificando...</p>
        ) : (
          Object.entries(services).map(([key, status]) => (
            <div key={key} className="flex items-center justify-between text-xs">
              <span className="text-gray-300">{SERVICE_LABELS[key] ?? key}</span>
              <div className="flex items-center gap-1.5">
                <span className={`status-dot ${dotClass[status] ?? 'status-dot-offline'}`} />
                <span className="text-muted">{status}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
