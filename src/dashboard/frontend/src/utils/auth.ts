const TOKEN_STORAGE_KEY = "dashboard_api_key";
const ADMIN_KEY_STORAGE = "dashboard_admin_key";

function readTokenFromStorage(): string | null {
  if (typeof window === "undefined") return null;
  return (
    window.sessionStorage.getItem(TOKEN_STORAGE_KEY) ||
    window.localStorage.getItem(TOKEN_STORAGE_KEY) ||
    null
  );
}

export function getApiToken(): string | null {
  if (typeof window === "undefined") return null;

  const fromStorage = readTokenFromStorage();
  if (fromStorage) return fromStorage;

  const params = new URLSearchParams(window.location.search);
  const fromQuery = params.get("token") || params.get("api_key");
  if (!fromQuery) return null;

  window.sessionStorage.setItem(TOKEN_STORAGE_KEY, fromQuery);
  return fromQuery;
}

export function withApiAuthHeaders(headers: Record<string, string> = {}): Record<string, string> {
  const token = getApiToken();
  if (!token) return headers;
  return {
    ...headers,
    Authorization: `Bearer ${token}`,
  };
}

export function getAdminKey(): string | null {
  if (typeof window === "undefined") return null;
  return (
    window.sessionStorage.getItem(ADMIN_KEY_STORAGE) ||
    window.localStorage.getItem(ADMIN_KEY_STORAGE) ||
    null
  );
}

export function withAdminHeaders(headers: Record<string, string> = {}): Record<string, string> {
  const adminKey = getAdminKey();
  if (!adminKey) return headers;
  return {
    ...headers,
    "X-Admin-Key": adminKey,
  };
}

export async function apiFetch(input: RequestInfo | URL, init: RequestInit = {}): Promise<Response> {
  const headers = (init.headers as Record<string, string>) || {};
  const mergedHeaders = withApiAuthHeaders(headers);
  return fetch(input, { ...init, headers: mergedHeaders });
}

export function buildWsUrl(): string {
  if (typeof window === "undefined") {
    return "ws://localhost:8000/ws";
  }
  const wsScheme = window.location.protocol === "https:" ? "wss" : "ws";
  const token = getApiToken();
  const base = `${wsScheme}://${window.location.host}/ws`;
  if (!token) return base;
  const params = new URLSearchParams({ token });
  return `${base}?${params.toString()}`;
}
