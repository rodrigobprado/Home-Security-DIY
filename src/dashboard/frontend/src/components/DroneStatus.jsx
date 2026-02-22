import useStore from '../store/useStore'

function BatteryBar({ percent }) {
  const pct = parseFloat(percent) || 0
  const color = pct > 50 ? 'bg-success' : pct > 20 ? 'bg-warning' : 'bg-critical'
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 bg-border rounded-full h-1.5 overflow-hidden">
        <div className={`h-full ${color} transition-all`} style={{ width: `${Math.min(pct, 100)}%` }} />
      </div>
      <span className="text-xs text-muted w-8 text-right">{pct.toFixed(0)}%</span>
    </div>
  )
}

function DroneCard({ title, icon, isOnlineEntity, batteryEntity, stateEntity, extraEntities = [] }) {
  const { states } = useStore()
  const isOnline = states[isOnlineEntity]?.state === 'on' || states[isOnlineEntity]?.state === 'true'
  const battery = states[batteryEntity]?.state ?? '--'
  const droneState = states[stateEntity]?.state ?? 'desconhecido'

  return (
    <div className={`card border ${isOnline ? 'border-border' : 'border-red-900/50 opacity-60'}`}>
      <div className="flex items-center justify-between mb-2">
        <span className="font-semibold text-sm">{icon} {title}</span>
        <span className={`text-xs ${isOnline ? 'text-success' : 'text-critical'}`}>
          {isOnline ? 'online' : 'offline'}
        </span>
      </div>
      <p className="text-xs text-muted mb-1">{droneState}</p>
      <BatteryBar percent={battery} />
      {extraEntities.map(({ id, label }) => (
        <div key={id} className="flex justify-between text-xs text-muted mt-1">
          <span>{label}</span>
          <span className="text-gray-300">{states[id]?.state ?? '--'}</span>
        </div>
      ))}
    </div>
  )
}

export default function DroneStatus() {
  return (
    <div className="flex flex-col gap-3">
      <h2 className="text-xs font-semibold uppercase tracking-wider text-muted">Drones</h2>
      <DroneCard
        title="UGV"
        icon="🤖"
        isOnlineEntity="binary_sensor.ugv_online"
        batteryEntity="sensor.ugv_battery"
        stateEntity="sensor.ugv_status"
        extraEntities={[
          { id: 'sensor.ugv_detections', label: 'Detecções' },
          { id: 'sensor.ugv_wi_fi_signal', label: 'Wi-Fi (dBm)' },
        ]}
      />
      <DroneCard
        title="UAV"
        icon="🚁"
        isOnlineEntity="binary_sensor.uav_armed"
        batteryEntity="sensor.uav_battery"
        stateEntity="sensor.uav_status"
        extraEntities={[
          { id: 'binary_sensor.uav_altitude', label: 'Altitude (m)' },
        ]}
      />
    </div>
  )
}
