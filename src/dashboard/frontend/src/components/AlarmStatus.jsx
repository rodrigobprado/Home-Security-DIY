import useStore from '../store/useStore'

const ALARM_CONFIG = {
  triggered:    { label: 'ALARME DISPARADO', color: 'bg-red-900 border-red-500 text-red-200', dot: 'bg-red-400', pulse: true },
  armed_away:   { label: 'Armado — Ausente', color: 'bg-green-900/40 border-green-600 text-green-200', dot: 'bg-green-400', pulse: false },
  armed_night:  { label: 'Armado — Noite',   color: 'bg-yellow-900/40 border-yellow-600 text-yellow-200', dot: 'bg-yellow-400', pulse: false },
  armed_home:   { label: 'Armado — Perímetro', color: 'bg-blue-900/40 border-blue-600 text-blue-200', dot: 'bg-blue-400', pulse: false },
  disarmed:     { label: 'Desarmado',        color: 'bg-surface border-border text-gray-400', dot: 'bg-gray-500', pulse: false },
}

export default function AlarmStatus() {
  const { states } = useStore()
  const state = states['alarm_control_panel.alarmo']?.state ?? 'desconhecido'
  const cfg = ALARM_CONFIG[state] ?? { label: state, color: 'bg-surface border-border text-gray-400', dot: 'bg-gray-500', pulse: false }

  return (
    <div className={`card border-2 ${cfg.color} ${cfg.pulse ? 'alarm-triggered' : ''}`}>
      <div className="flex items-center gap-3">
        <span className={`status-dot w-3 h-3 ${cfg.dot} ${cfg.pulse ? 'animate-pulse' : ''}`} />
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wider">Alarme</p>
          <p className="text-lg font-bold">{cfg.label}</p>
        </div>
      </div>
    </div>
  )
}
