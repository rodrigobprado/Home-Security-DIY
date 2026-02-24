import { create } from 'zustand'

const useStore = create((set) => ({
  // Estados das entidades HA (entity_id → state object)
  states: {},

  // Alertas recentes (do WebSocket, mais recente primeiro)
  alerts: [],

  // Status dos serviços
  services: {},

  // Status de conexão WebSocket
  wsStatus: 'connecting', // connecting | connected | disconnected

  // Catálogo de ativos (Issue #337)
  assets: [],
  assetsLoading: false,
  assetsError: null,

  // Actions
  setStates: (states) => set({ states }),

  updateState: (entity_id, stateObj) =>
    set((s) => ({
      states: { ...s.states, [entity_id]: stateObj },
    })),

  addAlert: (alert) =>
    set((s) => ({
      alerts: [alert, ...s.alerts].slice(0, 100), // mantém últimos 100
    })),

  setAlerts: (alerts) => set({ alerts }),
  setAlertsIfEmpty: (alerts) =>
    set((s) => ({
      alerts: s.alerts.length === 0 ? alerts : s.alerts,
    })),

  setServices: (services) => set({ services }),

  setWsStatus: (wsStatus) => set({ wsStatus }),

  // Assets actions
  setAssets: (assets) => set({ assets }),
  setAssetsLoading: (assetsLoading) => set({ assetsLoading }),
  setAssetsError: (assetsError) => set({ assetsError }),

  addAsset: (asset) =>
    set((s) => ({ assets: [asset, ...s.assets] })),

  updateAsset: (updatedAsset) =>
    set((s) => ({
      assets: s.assets.map((a) => (a.id === updatedAsset.id ? updatedAsset : a)),
    })),

  removeAsset: (assetId) =>
    set((s) => ({
      assets: s.assets.filter((a) => a.id !== assetId),
    })),
}))

export default useStore
