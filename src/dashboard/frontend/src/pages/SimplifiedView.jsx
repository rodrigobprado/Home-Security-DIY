import { useEffect, useState } from 'react'
import useStore from '../store/useStore'
import CameraGrid from '../components/CameraGrid'
import OperationalMap from '../components/OperationalMap'

const ALARM_CONFIG = {
  triggered:    { label: 'ALARME DISPARADO', cls: 'bg-red-900 border-red-500 text-red-200 alarm-triggered' },
  armed_away:   { label: 'Armado — Ausente', cls: 'bg-green-900/30 border-green-600 text-green-200' },
  armed_night:  { label: 'Armado — Noite',   cls: 'bg-yellow-900/30 border-yellow-600 text-yellow-200' },
  armed_home:   { label: 'Armado — Perímetro', cls: 'bg-blue-900/30 border-blue-600 text-blue-200' },
  disarmed:     { label: 'Sistema Desarmado', cls: 'bg-surface border-border text-gray-400' },
}

export default function SimplifiedView() {
  const { states } = useStore()
  const [time, setTime] = useState(new Date())

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000)
    return () => clearInterval(t)
  }, [])

  const alarmState = states['alarm_control_panel.alarmo']?.state ?? 'disarmed'
  const cfg = ALARM_CONFIG[alarmState] ?? ALARM_CONFIG.disarmed

  return (
    <div className="flex-1 flex flex-col h-full p-2 gap-2">
      {/* Barra de status */}
      <div className={`flex items-center justify-between px-6 py-3 rounded-lg border-2 ${cfg.cls}`}>
        <span className="text-2xl font-bold">{cfg.label}</span>
        <span className="font-mono text-xl">{time.toLocaleTimeString('pt-BR')}</span>
      </div>

      {/* Conteúdo principal */}
      <div className="flex-1 grid grid-cols-2 gap-2 overflow-hidden">
        <OperationalMap />
        <CameraGrid />
      </div>
    </div>
  )
}
