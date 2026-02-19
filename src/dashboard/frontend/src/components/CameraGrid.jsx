import { useEffect, useRef, useState } from 'react'

const CAMERAS = [
  { name: 'cam_entrada', label: 'Entrada' },
  { name: 'cam_fundos',  label: 'Fundos' },
  { name: 'cam_garagem', label: 'Garagem' },
  { name: 'cam_lateral', label: 'Lateral' },
]

const REFRESH_INTERVAL = 2000 // 2 segundos

function CameraFeed({ name, label }) {
  const [src, setSrc] = useState(`/api/cameras/${name}/snapshot?t=0`)
  const [error, setError] = useState(false)
  const intervalRef = useRef(null)

  useEffect(() => {
    setError(false)
    intervalRef.current = setInterval(() => {
      setSrc(`/api/cameras/${name}/snapshot?t=${Date.now()}`)
    }, REFRESH_INTERVAL)
    return () => clearInterval(intervalRef.current)
  }, [name])

  return (
    <div className="relative bg-black rounded-lg overflow-hidden aspect-video">
      {error ? (
        <div className="absolute inset-0 flex flex-col items-center justify-center text-muted text-sm gap-1">
          <span className="text-2xl">📷</span>
          <span>{label}</span>
          <span className="text-xs text-critical">offline</span>
        </div>
      ) : (
        <img
          src={src}
          alt={label}
          className="w-full h-full object-cover"
          onError={() => setError(true)}
          onLoad={() => setError(false)}
        />
      )}
      <div className="absolute bottom-0 left-0 right-0 px-2 py-1 bg-black/60 text-xs text-gray-300">
        {label}
        {!error && <span className="float-right text-success">● ao vivo</span>}
      </div>
    </div>
  )
}

export default function CameraGrid() {
  return (
    <div className="card flex flex-col gap-3">
      <h2 className="text-xs font-semibold uppercase tracking-wider text-muted">Câmeras</h2>
      <div className="grid grid-cols-2 gap-2">
        {CAMERAS.map((cam) => (
          <CameraFeed key={cam.name} {...cam} />
        ))}
      </div>
    </div>
  )
}
