import { create } from 'zustand'

export interface EntityState {
  entity_id: string;
  state: string;
  attributes: Record<string, any>;
  last_changed?: string;
  last_updated?: string;
}

export interface Alert {
  id?: number;
  timestamp: string;
  entity_id: string;
  event_type: string;
  old_state: string | null;
  new_state: string;
  severity: 'info' | 'warning' | 'critical';
  message: string | null;
}

export interface ServiceStatus {
  status: 'online' | 'offline' | 'error' | 'unknown';
  message?: string;
  last_check?: string;
}

export interface Asset {
  id: string;
  asset_type: 'sensor' | 'camera' | 'ugv' | 'uav';
  name: string;
  entity_id: string;
  status: 'active' | 'inactive' | 'offline' | 'maintenance';
  location?: string;
  description?: string;
  config_json?: string;
  is_active: boolean;
  created_at?: string;
  updated_at?: string;
}

export type WebSocketStatus = 'connecting' | 'connected' | 'disconnected';

interface StoreState {
  states: Record<string, EntityState>;
  alerts: Alert[];
  services: Record<string, ServiceStatus>;
  wsStatus: WebSocketStatus;
  assets: Asset[];
  assetsLoading: boolean;
  assetsError: string | null;

  setStates: (states: Record<string, EntityState>) => void;
  updateState: (entity_id: string, stateObj: EntityState) => void;
  addAlert: (alert: Alert) => void;
  setAlerts: (alerts: Alert[]) => void;
  setAlertsIfEmpty: (alerts: Alert[]) => void;
  setServices: (services: Record<string, ServiceStatus>) => void;
  setWsStatus: (wsStatus: WebSocketStatus) => void;
  setAssets: (assets: Asset[]) => void;
  setAssetsLoading: (loading: boolean) => void;
  setAssetsError: (error: string | null) => void;
  addAsset: (asset: Asset) => void;
  updateAsset: (updatedAsset: Asset) => void;
  removeAsset: (assetId: string) => void;
}

const useStore = create<StoreState>((set) => ({
  states: {},
  alerts: [],
  services: {},
  wsStatus: 'connecting',
  assets: [],
  assetsLoading: false,
  assetsError: null,

  setStates: (states) => set({ states }),

  updateState: (entity_id, stateObj) =>
    set((s) => ({
      states: { ...s.states, [entity_id]: stateObj },
    })),

  addAlert: (alert) =>
    set((s) => ({
      alerts: [alert, ...s.alerts].slice(0, 100),
    })),

  setAlerts: (alerts) => set({ alerts }),
  setAlertsIfEmpty: (alerts) =>
    set((s) => ({
      alerts: s.alerts.length === 0 ? alerts : s.alerts,
    })),

  setServices: (services) => set({ services }),

  setWsStatus: (wsStatus) => set({ wsStatus }),

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
