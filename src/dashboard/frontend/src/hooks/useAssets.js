/**
 * Hook para buscar e gerenciar o catálogo de ativos — Issue #337.
 * Lê de /api/assets e sincroniza com o Zustand store.
 */
import { useCallback, useEffect } from 'react'
import useStore from '../store/useStore'
import { apiFetch } from '../utils/auth'

export function useAssets() {
  const { assets, assetsLoading, assetsError, setAssets, setAssetsLoading, setAssetsError } =
    useStore()

  const fetchAssets = useCallback(async ({ assetType, isActive } = {}) => {
    setAssetsLoading(true)
    setAssetsError(null)
    try {
      const params = new URLSearchParams({ limit: '200' })
      if (assetType) params.set('asset_type', assetType)
      if (isActive !== undefined) params.set('is_active', String(isActive))

      const resp = await apiFetch(`/api/assets?${params}`)
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`)
      const data = await resp.json()
      setAssets(data.items ?? [])
    } catch (err) {
      setAssetsError(err.message)
    } finally {
      setAssetsLoading(false)
    }
  }, [])

  // Carrega catálogo na montagem
  useEffect(() => {
    fetchAssets()
  }, [])

  // Filtra por tipo
  const sensorAssets = assets.filter((a) => a.asset_type === 'sensor' && a.is_active)
  const cameraAssets = assets.filter((a) => a.asset_type === 'camera' && a.is_active)
  const droneAssets = assets.filter(
    (a) => (a.asset_type === 'ugv' || a.asset_type === 'uav') && a.is_active,
  )

  return {
    assets,
    sensorAssets,
    cameraAssets,
    droneAssets,
    assetsLoading,
    assetsError,
    refetch: fetchAssets,
  }
}
