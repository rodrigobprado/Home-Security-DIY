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
}))

export default useStore
