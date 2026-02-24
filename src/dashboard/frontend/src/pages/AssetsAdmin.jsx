/**
 * Página de Administração de Ativos — Issue #337.
 * Permite listar, cadastrar, editar e desativar sensores, câmeras, UGV e UAV.
 */
import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import useStore from '../store/useStore'
import { useAssets } from '../hooks/useAssets'

const ASSET_TYPE_LABELS = {
  sensor: 'Sensor',
  camera: 'Câmera',
  ugv: 'UGV',
  uav: 'UAV',
}

const STATUS_LABELS = {
  active: 'Ativo',
  inactive: 'Inativo',
  offline: 'Offline',
  maintenance: 'Manutenção',
}

const STATUS_COLORS = {
  active: 'text-green-400',
  inactive: 'text-gray-400',
  offline: 'text-red-400',
  maintenance: 'text-yellow-400',
}

const EMPTY_FORM = {
  asset_type: 'sensor',
  name: '',
  entity_id: '',
  status: 'active',
  location: '',
  description: '',
  config_json: '',
}

// ---------------------------------------------------------------------------
// Formulário de criação/edição
// ---------------------------------------------------------------------------
function AssetForm({ initial, onSave, onCancel, adminKey }) {
  const [form, setForm] = useState(initial ?? EMPTY_FORM)
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)

  const isEdit = Boolean(initial?.id)
  let submitLabel = 'Cadastrar'
  if (saving) submitLabel = 'Salvando...'
  else if (isEdit) submitLabel = 'Atualizar'

  async function handleSubmit(e) {
    e.preventDefault()
    if (!adminKey) {
      setError('Informe a chave de administrador para salvar.')
      return
    }
    setSaving(true)
    setError(null)
    try {
      const body = {
        asset_type: form.asset_type,
        name: form.name,
        entity_id: form.entity_id,
        status: form.status,
        location: form.location || null,
        description: form.description || null,
        config_json: form.config_json || null,
      }

      if (form.config_json) {
        try { JSON.parse(form.config_json) } catch {
          setError('config_json deve ser JSON válido.')
          setSaving(false)
          return
        }
      }

      const url = isEdit ? `/api/assets/${initial.id}` : '/api/assets'
      const method = isEdit ? 'PUT' : 'POST'
      const resp = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'X-Admin-Key': adminKey,
        },
        body: JSON.stringify(body),
      })

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({ detail: `HTTP ${resp.status}` }))
        throw new Error(err.detail ?? `HTTP ${resp.status}`)
      }

      const saved = await resp.json()
      onSave(saved)
    } catch (err) {
      setError(err.message)
    } finally {
      setSaving(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-xs text-muted">Tipo *</label>
          <select
            value={form.asset_type}
            onChange={(e) => setForm((f) => ({ ...f, asset_type: e.target.value }))}
            className="w-full bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary mt-1"
            required
          >
            {Object.entries(ASSET_TYPE_LABELS).map(([v, l]) => (
              <option key={v} value={v}>{l}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="text-xs text-muted">Status *</label>
          <select
            value={form.status}
            onChange={(e) => setForm((f) => ({ ...f, status: e.target.value }))}
            className="w-full bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary mt-1"
          >
            {Object.entries(STATUS_LABELS).map(([v, l]) => (
              <option key={v} value={v}>{l}</option>
            ))}
          </select>
        </div>
      </div>

      <div>
        <label className="text-xs text-muted">Nome *</label>
        <input
          type="text"
          value={form.name}
          onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
          className="w-full bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary mt-1"
          placeholder="ex: Sensor Porta Entrada"
          required
          maxLength={200}
        />
      </div>

      <div>
        <label className="text-xs text-muted">Entity ID *</label>
        <input
          type="text"
          value={form.entity_id}
          onChange={(e) => setForm((f) => ({ ...f, entity_id: e.target.value }))}
          className="w-full bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary mt-1 font-mono"
          placeholder="ex: binary_sensor.porta_entrada"
          required
          maxLength={200}
          disabled={isEdit}
        />
        {isEdit && <p className="text-xs text-muted mt-1">Entity ID não pode ser alterado.</p>}
      </div>

      <div>
        <label className="text-xs text-muted">Localização</label>
        <input
          type="text"
          value={form.location}
          onChange={(e) => setForm((f) => ({ ...f, location: e.target.value }))}
          className="w-full bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary mt-1"
          placeholder="ex: Entrada principal"
          maxLength={200}
        />
      </div>

      <div>
        <label className="text-xs text-muted">Descrição</label>
        <textarea
          value={form.description}
          onChange={(e) => setForm((f) => ({ ...f, description: e.target.value }))}
          className="w-full bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary mt-1 resize-none"
          rows={2}
          placeholder="Descrição opcional do ativo"
        />
      </div>

      <div>
        <label className="text-xs text-muted">Config JSON (opcional)</label>
        <textarea
          value={form.config_json}
          onChange={(e) => setForm((f) => ({ ...f, config_json: e.target.value }))}
          className="w-full bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary mt-1 font-mono resize-none"
          rows={3}
          placeholder='{"topic": "cmnd/ugv/command"}'
        />
      </div>

      {error && (
        <p className="text-xs text-critical bg-red-900/20 border border-red-800 rounded p-2">
          {error}
        </p>
      )}

      <div className="flex gap-2 justify-end">
        <button
          type="button"
          onClick={onCancel}
          className="px-3 py-1.5 text-sm text-muted border border-border rounded hover:bg-surface transition-colors"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={saving}
          className="px-4 py-1.5 text-sm bg-accent text-white rounded hover:bg-accent/80 transition-colors disabled:opacity-50"
        >
          {submitLabel}
        </button>
      </div>
    </form>
  )
}

// ---------------------------------------------------------------------------
// Linha da tabela de ativos
// ---------------------------------------------------------------------------
function AssetRow({ asset, onEdit, onDelete, onRestore }) {
  return (
    <tr className={`border-b border-border transition-colors ${!asset.is_active ? 'opacity-50' : ''}`}>
      <td className="px-3 py-2 text-sm text-primary">
        <span className="font-medium">{asset.name}</span>
        <br />
        <span className="text-xs text-muted font-mono">{asset.entity_id}</span>
      </td>
      <td className="px-3 py-2 text-sm">
        <span className="text-xs bg-surface border border-border rounded px-1.5 py-0.5">
          {ASSET_TYPE_LABELS[asset.asset_type] ?? asset.asset_type}
        </span>
      </td>
      <td className={`px-3 py-2 text-sm ${STATUS_COLORS[asset.status] ?? 'text-muted'}`}>
        {STATUS_LABELS[asset.status] ?? asset.status}
      </td>
      <td className="px-3 py-2 text-xs text-muted">{asset.location ?? '—'}</td>
      <td className="px-3 py-2 text-xs">
        <span className={asset.is_active ? 'text-green-400' : 'text-gray-500'}>
          {asset.is_active ? 'Ativo' : 'Inativo'}
        </span>
      </td>
      <td className="px-3 py-2">
        <div className="flex gap-1">
          <button
            onClick={() => onEdit(asset)}
            className="text-xs px-2 py-1 text-accent border border-accent/40 rounded hover:bg-accent/10 transition-colors"
          >
            Editar
          </button>
          {asset.is_active ? (
            <button
              onClick={() => onDelete(asset)}
              className="text-xs px-2 py-1 text-critical border border-critical/40 rounded hover:bg-red-900/20 transition-colors"
            >
              Desativar
            </button>
          ) : (
            <button
              onClick={() => onRestore(asset)}
              className="text-xs px-2 py-1 text-success border border-success/40 rounded hover:bg-green-900/20 transition-colors"
            >
              Restaurar
            </button>
          )}
        </div>
      </td>
    </tr>
  )
}

// ---------------------------------------------------------------------------
// Página principal
// ---------------------------------------------------------------------------
export default function AssetsAdmin() {
  const { assets, assetsLoading, assetsError, refetch } = useAssets()
  const { addAsset, updateAsset } = useStore()
  const [searchParams, setSearchParams] = useSearchParams()

  const typeParam = (searchParams.get('type') || '').toLowerCase()
  const initialType = Object.hasOwn(ASSET_TYPE_LABELS, typeParam) ? typeParam : ''

  const [showForm, setShowForm] = useState(false)
  const [editTarget, setEditTarget] = useState(null)
  const [adminKey, setAdminKey] = useState('')
  const [filterType, setFilterType] = useState(initialType)
  const [filterStatus, setFilterStatus] = useState('')
  const [filterSearch, setFilterSearch] = useState('')
  const [feedback, setFeedback] = useState(null)

  useEffect(() => {
    setFilterType(initialType)
  }, [initialType])

  function showFeedback(msg, isError = false) {
    setFeedback({ msg, isError })
    setTimeout(() => setFeedback(null), 4000)
  }

  function handleSave(saved) {
    if (editTarget) {
      updateAsset(saved)
      showFeedback(`Ativo "${saved.name}" atualizado.`)
    } else {
      addAsset(saved)
      showFeedback(`Ativo "${saved.name}" cadastrado.`)
    }
    setShowForm(false)
    setEditTarget(null)
  }

  async function handleDelete(asset) {
    if (!adminKey) { showFeedback('Informe a chave de administrador.', true); return }
    const confirmed = window.confirm(
      `Desativar ativo "${asset.name}"? O ativo ficará inativo mas não será removido permanentemente.`,
    )
    if (!confirmed) return

    try {
      const resp = await fetch(`/api/assets/${asset.id}`, {
        method: 'DELETE',
        headers: { 'X-Admin-Key': adminKey },
      })
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      updateAsset({ ...asset, is_active: false, status: 'inactive' })
      showFeedback(`Ativo "${asset.name}" desativado.`)
    } catch (err) {
      showFeedback(`Erro ao desativar: ${err.message}`, true)
    }
  }

  async function handleRestore(asset) {
    if (!adminKey) { showFeedback('Informe a chave de administrador.', true); return }
    try {
      const resp = await fetch(`/api/assets/${asset.id}/restore`, {
        method: 'POST',
        headers: { 'X-Admin-Key': adminKey },
      })
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      const restored = await resp.json()
      updateAsset(restored)
      showFeedback(`Ativo "${asset.name}" restaurado.`)
    } catch (err) {
      showFeedback(`Erro ao restaurar: ${err.message}`, true)
    }
  }

  // Filtros locais
  const filtered = assets.filter((a) => {
    if (filterType && a.asset_type !== filterType) return false
    if (filterStatus && a.status !== filterStatus) return false
    if (filterSearch) {
      const q = filterSearch.toLowerCase()
      return a.name.toLowerCase().includes(q) || a.entity_id.toLowerCase().includes(q)
    }
    return true
  })

  function handleFilterTypeChange(nextType) {
    setFilterType(nextType)
    const next = new URLSearchParams(searchParams)
    if (nextType) next.set('type', nextType)
    else next.delete('type')
    setSearchParams(next, { replace: true })
  }

  function renderTableContent() {
    if (assetsLoading) {
      return <p className="text-muted text-sm text-center py-6">Carregando ativos...</p>
    }

    if (assetsError) {
      return <p className="text-critical text-sm text-center py-6">Erro: {assetsError}</p>
    }

    if (filtered.length === 0) {
      const emptyMessage = assets.length === 0
        ? 'Nenhum ativo cadastrado. Clique em "+ Novo Ativo" para começar.'
        : 'Nenhum ativo encontrado com os filtros aplicados.'
      return <p className="text-muted text-sm text-center py-6">{emptyMessage}</p>
    }

    return (
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-border">
              <th className="px-3 py-2 text-xs font-semibold text-muted uppercase">Nome / Entity ID</th>
              <th className="px-3 py-2 text-xs font-semibold text-muted uppercase">Tipo</th>
              <th className="px-3 py-2 text-xs font-semibold text-muted uppercase">Status</th>
              <th className="px-3 py-2 text-xs font-semibold text-muted uppercase">Local</th>
              <th className="px-3 py-2 text-xs font-semibold text-muted uppercase">Visível</th>
              <th className="px-3 py-2 text-xs font-semibold text-muted uppercase">Ações</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((asset) => (
              <AssetRow
                key={asset.id}
                asset={asset}
                onEdit={(a) => { setEditTarget(a); setShowForm(true) }}
                onDelete={handleDelete}
                onRestore={handleRestore}
              />
            ))}
          </tbody>
        </table>
        <p className="text-xs text-muted px-3 py-2 border-t border-border">
          {filtered.length} de {assets.length} ativos
        </p>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-4 p-4 overflow-y-auto h-full">
      {/* Cabeçalho */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-lg font-semibold text-primary">Cadastro de Ativos</h1>
          <p className="text-xs text-muted">Sensores, Câmeras, UGV e UAV</p>
        </div>
        <button
          onClick={() => { setEditTarget(null); setShowForm(true) }}
          className="px-3 py-1.5 text-sm bg-accent text-white rounded hover:bg-accent/80 transition-colors"
        >
          + Novo Ativo
        </button>
      </div>

      {/* Chave de administrador */}
      <div className="card">
        <label className="text-xs text-muted">Chave de Administrador (X-Admin-Key)</label>
        <div className="flex gap-2 mt-1">
          <input
            type="password"
            value={adminKey}
            onChange={(e) => setAdminKey(e.target.value)}
            className="flex-1 bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary font-mono"
            placeholder="Necessária para criar, editar ou desativar ativos"
            autoComplete="off"
          />
        </div>
        <p className="text-xs text-muted mt-1">
          A chave admin nunca é enviada ao backend em requisições de leitura.
        </p>
      </div>

      {/* Feedback */}
      {feedback && (
        <div
          className={`px-3 py-2 rounded text-sm border ${
            feedback.isError
              ? 'bg-red-900/20 border-red-800 text-critical'
              : 'bg-green-900/20 border-green-800 text-success'
          }`}
        >
          {feedback.msg}
        </div>
      )}

      {/* Formulário */}
      {showForm && (
        <div className="card">
          <h2 className="text-sm font-semibold text-primary mb-3">
            {editTarget ? `Editar: ${editTarget.name}` : 'Novo Ativo'}
          </h2>
          <AssetForm
            initial={editTarget}
            adminKey={adminKey}
            onSave={handleSave}
            onCancel={() => { setShowForm(false); setEditTarget(null) }}
          />
        </div>
      )}

      {/* Filtros */}
      <div className="flex flex-wrap gap-2">
        <input
          type="text"
          value={filterSearch}
          onChange={(e) => setFilterSearch(e.target.value)}
          placeholder="Buscar por nome ou entity_id..."
          className="flex-1 min-w-48 bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary"
        />
        <select
          value={filterType}
          onChange={(e) => handleFilterTypeChange(e.target.value)}
          className="bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary"
        >
          <option value="">Todos os tipos</option>
          {Object.entries(ASSET_TYPE_LABELS).map(([v, l]) => (
            <option key={v} value={v}>{l}</option>
          ))}
        </select>
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="bg-surface border border-border rounded px-2 py-1.5 text-sm text-primary"
        >
          <option value="">Todos os status</option>
          {Object.entries(STATUS_LABELS).map(([v, l]) => (
            <option key={v} value={v}>{l}</option>
          ))}
        </select>
        <button
          onClick={() => refetch()}
          className="px-3 py-1.5 text-sm text-muted border border-border rounded hover:bg-surface transition-colors"
        >
          ↻ Atualizar
        </button>
      </div>

      {/* Tabela */}
      <div className="card overflow-hidden">
        {renderTableContent()}
      </div>
    </div>
  )
}
