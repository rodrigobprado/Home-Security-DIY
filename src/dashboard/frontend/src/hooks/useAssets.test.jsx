import { renderHook, act, waitFor } from "@testing-library/react";
import { vi } from "vitest";
import { useAssets } from "./useAssets";
import useStore from "../store/useStore";

describe("useAssets hook", () => {
  beforeEach(() => {
    useStore.setState({
      assets: [],
      assetsLoading: false,
      assetsError: null,
    });
    vi.clearAllMocks();
  });

  it("fetches assets on mount and updates store", async () => {
    const mockAssets = [
      { id: "1", name: "Sensor A", asset_type: "sensor", is_active: true },
      { id: "2", name: "Camera B", asset_type: "camera", is_active: true },
    ];

    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ items: mockAssets, total: 2 }),
    });

    const { result } = renderHook(() => useAssets());

    await waitFor(() => {
      expect(result.current.assets).toHaveLength(2);
    });

    expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining("/api/assets"));
    expect(result.current.assetsError).toBeNull();
    expect(result.current.assetsLoading).toBe(false);
  });

  it("sets error state on fetch failure", async () => {
    global.fetch = vi.fn().mockRejectedValueOnce(new Error("Network error"));

    const { result } = renderHook(() => useAssets());

    await waitFor(() => {
      expect(result.current.assetsError).toBe("Network error");
    });

    expect(result.current.assetsLoading).toBe(false);
  });

  it("sets error state on non-ok response", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: false,
      status: 403,
    });

    const { result } = renderHook(() => useAssets());

    await waitFor(() => {
      expect(result.current.assetsError).toBeTruthy();
    });
  });

  it("filters sensorAssets correctly", async () => {
    const mockAssets = [
      { id: "1", name: "Sensor A", asset_type: "sensor", is_active: true },
      { id: "2", name: "Camera B", asset_type: "camera", is_active: true },
      { id: "3", name: "UGV", asset_type: "ugv", is_active: true },
      { id: "4", name: "UAV", asset_type: "uav", is_active: true },
      { id: "5", name: "Sensor Inativo", asset_type: "sensor", is_active: false },
    ];

    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({ items: mockAssets }),
    });

    const { result } = renderHook(() => useAssets());

    await waitFor(() => {
      expect(result.current.assets).toHaveLength(5);
    });

    // Apenas ativos ativos do tipo sensor
    expect(result.current.sensorAssets).toHaveLength(1);
    expect(result.current.sensorAssets[0].name).toBe("Sensor A");

    // Camera
    expect(result.current.cameraAssets).toHaveLength(1);
    expect(result.current.cameraAssets[0].name).toBe("Camera B");

    // Drones (ugv + uav)
    expect(result.current.droneAssets).toHaveLength(2);
  });

  it("refetch loads assets again", async () => {
    global.fetch = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ items: [{ id: "1", name: "A", asset_type: "sensor", is_active: true }] }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          items: [
            { id: "1", name: "A", asset_type: "sensor", is_active: true },
            { id: "2", name: "B", asset_type: "camera", is_active: true },
          ],
        }),
      });

    const { result } = renderHook(() => useAssets());

    await waitFor(() => {
      expect(result.current.assets).toHaveLength(1);
    });

    act(() => {
      result.current.refetch();
    });

    await waitFor(() => {
      expect(result.current.assets).toHaveLength(2);
    });
  });

  it("refetch accepts filters and appends query params", async () => {
    global.fetch = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ items: [] }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ items: [] }),
      });

    const { result } = renderHook(() => useAssets());
    await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(1));

    act(() => {
      result.current.refetch({ assetType: "sensor", isActive: false });
    });

    await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(2));
    const secondUrl = global.fetch.mock.calls[1][0];
    expect(secondUrl).toContain("asset_type=sensor");
    expect(secondUrl).toContain("is_active=false");
  });
});
