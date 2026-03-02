import { describe, it, expect, beforeEach, vi } from "vitest";
import {
  getApiToken,
  withApiAuthHeaders,
  getAdminKey,
  withAdminHeaders,
  apiFetch,
  buildWsUrl,
} from "./auth";

describe("auth utils", () => {
  beforeEach(() => {
    window.sessionStorage.clear();
    window.localStorage.clear();
    // Reset window.location to default
    Object.defineProperty(window, "location", {
      value: { search: "", protocol: "http:", host: "localhost" },
      writable: true,
    });
  });

  describe("getApiToken", () => {
    it("returns null when no token stored", () => {
      expect(getApiToken()).toBeNull();
    });

    it("returns token from sessionStorage", () => {
      window.sessionStorage.setItem("dashboard_api_key", "session-token");
      expect(getApiToken()).toBe("session-token");
    });

    it("returns token from localStorage when not in sessionStorage", () => {
      window.localStorage.setItem("dashboard_api_key", "local-token");
      expect(getApiToken()).toBe("local-token");
    });

    it("reads token from query param and stores it in sessionStorage", () => {
      Object.defineProperty(window, "location", {
        value: { search: "?token=query-token", protocol: "http:", host: "localhost" },
        writable: true,
      });
      expect(getApiToken()).toBe("query-token");
      expect(window.sessionStorage.getItem("dashboard_api_key")).toBe("query-token");
    });

    it("reads token from api_key query param", () => {
      Object.defineProperty(window, "location", {
        value: { search: "?api_key=apikey-token", protocol: "http:", host: "localhost" },
        writable: true,
      });
      expect(getApiToken()).toBe("apikey-token");
    });
  });

  describe("withApiAuthHeaders", () => {
    it("returns empty headers when no token", () => {
      expect(withApiAuthHeaders({})).toEqual({});
    });

    it("adds Authorization header when token exists", () => {
      window.sessionStorage.setItem("dashboard_api_key", "my-token");
      expect(withApiAuthHeaders({})).toEqual({
        Authorization: "Bearer my-token",
      });
    });

    it("merges with existing headers", () => {
      window.sessionStorage.setItem("dashboard_api_key", "my-token");
      const result = withApiAuthHeaders({ "Content-Type": "application/json" });
      expect(result).toEqual({
        "Content-Type": "application/json",
        Authorization: "Bearer my-token",
      });
    });
  });

  describe("getAdminKey", () => {
    it("returns null when no admin key stored", () => {
      expect(getAdminKey()).toBeNull();
    });

    it("returns admin key from sessionStorage", () => {
      window.sessionStorage.setItem("dashboard_admin_key", "admin-session");
      expect(getAdminKey()).toBe("admin-session");
    });

    it("returns admin key from localStorage when not in sessionStorage", () => {
      window.localStorage.setItem("dashboard_admin_key", "admin-local");
      expect(getAdminKey()).toBe("admin-local");
    });
  });

  describe("withAdminHeaders", () => {
    it("returns empty headers when no admin key", () => {
      expect(withAdminHeaders({})).toEqual({});
    });

    it("adds X-Admin-Key header when admin key exists", () => {
      window.sessionStorage.setItem("dashboard_admin_key", "admin-key");
      expect(withAdminHeaders({})).toEqual({ "X-Admin-Key": "admin-key" });
    });
  });

  describe("apiFetch", () => {
    it("calls fetch with auth headers when token exists", async () => {
      window.sessionStorage.setItem("dashboard_api_key", "test-token");
      global.fetch = vi.fn().mockResolvedValue({ ok: true });

      await apiFetch("/api/test");

      expect(global.fetch).toHaveBeenCalledWith("/api/test", {
        headers: { Authorization: "Bearer test-token" },
      });
    });

    it("calls fetch with empty headers when no token", async () => {
      global.fetch = vi.fn().mockResolvedValue({ ok: true });

      await apiFetch("/api/test");

      expect(global.fetch).toHaveBeenCalledWith("/api/test", { headers: {} });
    });

    it("merges init options with auth headers", async () => {
      window.sessionStorage.setItem("dashboard_api_key", "test-token");
      global.fetch = vi.fn().mockResolvedValue({ ok: true });

      await apiFetch("/api/test", { method: "POST", body: "data" });

      expect(global.fetch).toHaveBeenCalledWith("/api/test", {
        method: "POST",
        body: "data",
        headers: { Authorization: "Bearer test-token" },
      });
    });
  });

  describe("buildWsUrl", () => {
    it("builds basic WebSocket URL without token", () => {
      const url = buildWsUrl();
      expect(url).toBe("ws://localhost/ws");
    });

    it("builds WebSocket URL with token appended as query param", () => {
      window.sessionStorage.setItem("dashboard_api_key", "ws-token");
      const url = buildWsUrl();
      expect(url).toBe("ws://localhost/ws?token=ws-token");
    });

    it("uses wss scheme for https", () => {
      Object.defineProperty(window, "location", {
        value: { search: "", protocol: "https:", host: "example.com" },
        writable: true,
      });
      const url = buildWsUrl();
      expect(url).toBe("wss://example.com/ws");
    });
  });
});
