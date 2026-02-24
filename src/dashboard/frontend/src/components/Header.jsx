import { useEffect, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import QuickActionsMenu from './QuickActionsMenu'
import useStore from '../store/useStore'

export default function Header() {
  const [time, setTime] = useState(new Date())
  const { states, wsStatus } = useStore()
  const location = useLocation()

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(t)
  }, [])

  const alarmState = states['alarm_control_panel.alarmo']?.state ?? 'desconhecido'
  const isTriggered = alarmState === 'triggered'
  const isSimplified = location.pathname === '/simplified'

  const alarmLabel = {
    triggered: '🔴 ALARME DISPARADO',
    armed_away: '🟢 Armado Total',
    armed_night: '🟡 Armado Noite',
    armed_home: '🔵 Armado Perímetro',
    disarmed: '⚪ Desarmado',
  }[alarmState] ?? `⚪ ${alarmState}`

  const wsColor = { connected: 'text-success', connecting: 'text-warning', disconnected: 'text-critical' }[wsStatus]

  return (
    <header className={`flex items-center justify-between px-4 py-2 border-b border-border ${isTriggered ? 'bg-red-950 alarm-triggered' : 'bg-surface'}`}>
      <div className="flex items-center gap-4">
        <span className="text-lg font-bold tracking-widest text-accent">🛡 HOME SECURITY</span>
        <span className={`text-sm font-semibold ${isTriggered ? 'text-red-300 animate-pulse' : 'text-gray-300'}`}>
          {alarmLabel}
        </span>
      </div>

      <div className="flex items-center gap-4 text-sm">
        <span className={`text-xs ${wsColor}`}>
          ● {wsStatus === 'connected' ? 'ao vivo' : wsStatus}
        </span>
        <span className="font-mono text-gray-300">
          {time.toLocaleTimeString('pt-BR')}
        </span>
        <QuickActionsMenu />
        <Link
          to={isSimplified ? '/' : '/simplified'}
          className="px-2 py-1 rounded bg-border hover:bg-accent/20 text-xs transition-colors"
          title={isSimplified ? 'Modo completo' : 'Modo simplificado (kiosk)'}
        >
          {isSimplified ? '⊞ Completo' : '⊟ Kiosk'}
        </Link>
      </div>
    </header>
  )
}
