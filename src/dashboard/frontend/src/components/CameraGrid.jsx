import { useEffect, useRef, useState } from 'react'
import { useAssets } from '../hooks/useAssets'

// Fallback estático — usado quando catálogo dinâmico está vazio
const STATIC_CAMERAS = [
  { name: 'cam_entrada', label: 'Entrada' },
  { name: 'cam_fundos',  label: 'Fundos' },
  { name: 'cam_garagem', label: 'Garagem' },
  { name: 'cam_lateral', label: 'Lateral' },
]

const REFRESH_INTERVAL = 2000 // 2 segundos

function CameraFeed({ name, label }) {
  const [src, setSrc] = useState(`/api/cameras/${name}/snapshot?t=0`)
  const [error, setError] = useState(false)
  const [errorCount, setErrorCount] = useState(0)
  const intervalRef = useRef(null)

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      setSrc(`/api/cameras/${name}/snapshot?t=${Date.now()}`)
    }, REFRESH_INTERVAL)
    return () => clearInterval(intervalRef.current)
  }, [name])

  return (
    <div className="relative bg-black rounded-lg overflow-hidden aspect-video">
      <img
        src={src}
        alt={label}
        className={`w-full h-full object-cover ${error ? 'hidden' : ''}`}
        onError={() => {
          setError(true)
          setErrorCount((value) => value + 1)
        }}
        onLoad={() => {
          setError(false)
          setErrorCount(0)
        }}
      />
      {error && errorCount >= 1 ? (
        <div className="absolute inset-0 flex flex-col items-center justify-center text-muted text-sm gap-1">
          <span className="text-2xl">📷</span>
          <span>{label}</span>
          <span className="text-xs text-critical">offline</span>
        </div>
      ) : null}
      <div className="absolute bottom-0 left-0 right-0 px-2 py-1 bg-black/60 text-xs text-gray-300">
        {label}
        {!error && <span className="float-right text-success">● ao vivo</span>}
      </div>
    </div>
  )
}

export default function CameraGrid() {
  const { cameraAssets } = useAssets()

  // Usa catálogo dinâmico se disponível; fallback estático se vazio
  const cameras = cameraAssets.length > 0
    ? cameraAssets.map((a) => ({
        name: a.entity_id,
        label: a.name,
      }))
    : STATIC_CAMERAS

  return (
    <div className="card flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <h2 className="text-xs font-semibold uppercase tracking-wider text-muted">Câmeras</h2>
        {cameraAssets.length > 0 && (
          <span className="text-xs text-accent">{cameraAssets.length} cadastradas</span>
        )}
      </div>
      <div className="grid grid-cols-2 gap-2">
        {cameras.map((cam) => (
          <CameraFeed key={cam.name} {...cam} />
        ))}
      </div>
    </div>
  )
}
