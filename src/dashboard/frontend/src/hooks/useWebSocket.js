import { useEffect, useRef } from 'react'
import useStore from '../store/useStore'

const WS_URL =
  typeof window !== 'undefined'
    ? `${window.location.protocol === 'https:' ? 'wss' : 'ws'}://${window.location.host}/ws`
    : 'ws://localhost:8000/ws'

export function useWebSocket() {
  const wsRef = useRef(null)
  const reconnectTimer = useRef(null)
  const { setStates, updateState, addAlert, setWsStatus } = useStore()

  useEffect(() => {
    let backoff = 1000

    function connect() {
      setWsStatus('connecting')
      const ws = new WebSocket(WS_URL)
      wsRef.current = ws

      ws.onopen = () => {
        setWsStatus('connected')
        backoff = 1000
      }

      ws.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data)

          if (msg.type === 'initial_state') {
            setStates(msg.states || {})
          } else if (msg.type === 'state_changed') {
            updateState(msg.entity_id, {
              state: msg.new_state,
              attributes: msg.attributes,
              last_changed: msg.last_changed,
              entity_id: msg.entity_id,
            })

            // Gera alerta local para entidades relevantes
            const relevant = [
              'alarm_control_panel.alarmo',
              'binary_sensor.porta_entrada',
              'binary_sensor.porta_fundos',
              'binary_sensor.janela_sala',
              'binary_sensor.pir_sala_occupancy',
              'binary_sensor.pir_corredor',
            ]
            if (relevant.includes(msg.entity_id) && msg.old_state !== msg.new_state) {
              addAlert({
                id: Date.now(),
                timestamp: new Date().toISOString(),
                entity_id: msg.entity_id,
                old_state: msg.old_state,
                new_state: msg.new_state,
                severity: getSeverity(msg.entity_id, msg.new_state),
              })
            }
          }
        } catch {
          // ignora erros de parse
        }
      }

      ws.onclose = () => {
        setWsStatus('disconnected')
        reconnectTimer.current = setTimeout(() => {
          backoff = Math.min(backoff * 2, 30000)
          connect()
        }, backoff)
      }

      ws.onerror = () => ws.close()
    }

    connect()

    return () => {
      clearTimeout(reconnectTimer.current)
      wsRef.current?.close()
    }
  }, [])
}

function getSeverity(entityId, newState) {
  if (entityId === 'alarm_control_panel.alarmo') {
    if (newState === 'triggered') return 'critical'
    if (newState.startsWith('armed')) return 'warning'
  }
  if (entityId.startsWith('binary_sensor.') && newState === 'on') return 'warning'
  return 'info'
}
