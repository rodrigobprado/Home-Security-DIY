import AlertFeed from '../components/AlertFeed'
import AlarmStatus from '../components/AlarmStatus'
import CameraGrid from '../components/CameraGrid'
import DroneStatus from '../components/DroneStatus'
import OperationalMap from '../components/OperationalMap'
import SensorGrid from '../components/SensorGrid'
import ServiceStatus from '../components/ServiceStatus'

export default function Dashboard() {
  return (
    <div className="flex-1 grid grid-cols-[280px_1fr_280px] gap-3 p-3 overflow-hidden h-full">
      {/* Coluna Esquerda */}
      <div className="flex flex-col gap-3 overflow-y-auto">
        <AlarmStatus />
        <SensorGrid />
        <AlertFeed />
      </div>

      {/* Coluna Central — Mapa */}
      <div className="flex flex-col overflow-hidden">
        <OperationalMap />
      </div>

      {/* Coluna Direita */}
      <div className="flex flex-col gap-3 overflow-y-auto">
        <DroneStatus />
        <ServiceStatus />
        <CameraGrid />
      </div>
    </div>
  )
}
