import { Link } from 'react-router-dom'

const LINKS = [
  { to: '/admin/assets', label: 'Admin de Ativos', description: 'Gestão completa de sensores, câmeras e drones.' },
  { to: '/admin/assets?type=sensor', label: 'Cadastro de Sensores', description: 'Abrir cadastro já filtrado para sensores.' },
  { to: '/admin/assets?type=camera', label: 'Cadastro de Câmeras', description: 'Abrir cadastro já filtrado para câmeras.' },
  { to: '/admin/assets?type=ugv', label: 'Cadastro UGV', description: 'Abrir cadastro já filtrado para drones terrestres.' },
  { to: '/admin/assets?type=uav', label: 'Cadastro UAV', description: 'Abrir cadastro já filtrado para drones aéreos.' },
  { to: '/simplified', label: 'Modo Kiosk', description: 'Tela simplificada para monitor dedicado.' },
]

export default function QuickActionsMenu() {
  return (
    <div className="card flex flex-col gap-2">
      <h2 className="text-xs font-semibold uppercase tracking-wider text-muted">Menu Operacional</h2>
      <div className="grid gap-2">
        {LINKS.map((link) => (
          <Link
            key={link.to}
            to={link.to}
            className="block rounded border border-border bg-surface px-2 py-2 hover:border-accent/50 hover:bg-accent/5 transition-colors"
          >
            <p className="text-sm font-medium text-primary">{link.label}</p>
            <p className="text-xs text-muted">{link.description}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
