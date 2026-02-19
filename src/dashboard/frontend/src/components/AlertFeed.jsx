import { useEffect } from 'react'
import useStore from '../store/useStore'

const SEVERITY_STYLE = {
  critical: 'border-l-critical text-red-300',
  warning:  'border-l-warning  text-yellow-300',
  info:     'border-l-accent   text-blue-300',
}

const ENTITY_LABEL = {
  'alarm_control_panel.alarmo':         'Alarme',
  'binary_sensor.porta_entrada':        'Porta Entrada',
  'binary_sensor.porta_fundos':         'Porta Fundos',
  'binary_sensor.janela_sala':          'Janela Sala',
  'binary_sensor.pir_sala_occupancy':   'PIR Sala',
  'binary_sensor.pir_corredor':         'PIR Corredor',
}

function formatTime(iso) {
  return new Date(iso).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

export default function AlertFeed() {
  const { alerts, setAlerts } = useStore()

  // Carrega histórico inicial via REST
  useEffect(() => {
    fetch('/api/alerts?limit=30')
      .then((r) => r.json())
      .then((data) => { if (Array.isArray(data) && alerts.length === 0) setAlerts(data) })
      .catch(() => {})
  }, [])

  return (
    <div className="card flex flex-col gap-2 overflow-hidden">
      <h2 className="text-xs font-semibold uppercase tracking-wider text-muted">Alertas Recentes</h2>
      <div className="overflow-y-auto max-h-64 flex flex-col gap-1 pr-1">
        {alerts.length === 0 ? (
          <p className="text-muted text-sm text-center py-4">Nenhum alerta registrado.</p>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id ?? alert.timestamp}
              className={`border-l-2 pl-2 py-1 text-xs ${SEVERITY_STYLE[alert.severity] ?? SEVERITY_STYLE.info}`}
            >
              <span className="text-gray-500 mr-2">{formatTime(alert.timestamp)}</span>
              <span className="font-medium">{ENTITY_LABEL[alert.entity_id] ?? alert.entity_id}</span>
              <span className="text-gray-500 ml-1">
                {alert.old_state} → {alert.new_state}
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
