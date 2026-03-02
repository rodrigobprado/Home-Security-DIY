const TOKEN_STORAGE_KEY = "dashboard_api_key";
const ADMIN_KEY_STORAGE = "dashboard_admin_key";

function readTokenFromStorage() {
  if (typeof window === "undefined") return null;
  return (
    window.sessionStorage.getItem(TOKEN_STORAGE_KEY) ||
    window.localStorage.getItem(TOKEN_STORAGE_KEY) ||
    null
  );
}

export function getApiToken() {
  if (typeof window === "undefined") return null;

  const fromStorage = readTokenFromStorage();
  if (fromStorage) return fromStorage;

  const params = new URLSearchParams(window.location.search);
  const fromQuery = params.get("token") || params.get("api_key");
  if (!fromQuery) return null;

  window.sessionStorage.setItem(TOKEN_STORAGE_KEY, fromQuery);
  return fromQuery;
}

export function withApiAuthHeaders(headers = {}) {
  const token = getApiToken();
  if (!token) return headers;
  return {
    ...headers,
    Authorization: `Bearer ${token}`,
  };
}

export function getAdminKey() {
  if (typeof window === "undefined") return null;
  return (
    window.sessionStorage.getItem(ADMIN_KEY_STORAGE) ||
    window.localStorage.getItem(ADMIN_KEY_STORAGE) ||
    null
  );
}

export function withAdminHeaders(headers = {}) {
  const adminKey = getAdminKey();
  if (!adminKey) return headers;
  return {
    ...headers,
    "X-Admin-Key": adminKey,
  };
}

export async function apiFetch(input, init = {}) {
  const mergedHeaders = withApiAuthHeaders(init.headers || {});
  return fetch(input, { ...init, headers: mergedHeaders });
}

export function buildWsUrl() {
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
