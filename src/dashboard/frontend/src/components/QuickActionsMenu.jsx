import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'

const LINKS = [
  { to: '/', label: 'Home' },
  { to: '/admin/assets', label: 'Admin de Ativos' },
  { to: '/admin/assets?type=sensor', label: 'Cadastro de Sensores' },
  { to: '/admin/assets?type=camera', label: 'Cadastro de Câmeras' },
  { to: '/admin/assets?type=ugv', label: 'Cadastro UGV' },
  { to: '/admin/assets?type=uav', label: 'Cadastro UAV' },
  { to: '/simplified', label: 'Modo Kiosk' },
]

export default function QuickActionsMenu() {
  const [open, setOpen] = useState(false)
  const containerRef = useRef(null)

  useEffect(() => {
    function onDocumentClick(event) {
      if (!containerRef.current) return
      if (!containerRef.current.contains(event.target)) setOpen(false)
    }
    function onEscape(event) {
      if (event.key === 'Escape') setOpen(false)
    }
    document.addEventListener('mousedown', onDocumentClick)
    document.addEventListener('keydown', onEscape)
    return () => {
      document.removeEventListener('mousedown', onDocumentClick)
      document.removeEventListener('keydown', onEscape)
    }
  }, [])

  return (
    <div ref={containerRef} className="relative">
      <button
        type="button"
        aria-label="Abrir menu operacional"
        aria-expanded={open ? 'true' : 'false'}
        onClick={() => setOpen((prev) => !prev)}
        className="h-11 w-11 rounded bg-[#1f2125] border border-border text-[#56c6b3] hover:bg-[#2a2d31] transition-colors flex items-center justify-center"
      >
        <span className="text-xl leading-none">☰</span>
      </button>

      {open && (
        <nav
          aria-label="Menu Operacional"
          className="absolute right-0 top-14 z-50 min-w-[260px] rounded bg-[#24262b] border border-[#30323a] py-2 shadow-xl"
        >
          {LINKS.map((link) => (
            <Link
              key={link.to}
              to={link.to}
              onClick={() => setOpen(false)}
              className="block px-4 py-2 text-lg text-[#7a7d84] hover:text-[#56c6b3] hover:bg-[#2b2d33] transition-colors"
            >
              {link.label}
            </Link>
          ))}
        </nav>
      )}
    </div>
  )
}
