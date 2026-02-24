import useStore from "./useStore";

describe("useStore actions", () => {
  beforeEach(() => {
    useStore.setState({
      states: {},
      alerts: [],
      services: {},
      wsStatus: "connecting",
      assets: [],
      assetsLoading: false,
      assetsError: null,
    });
  });

  it("updates entity states and websocket status", () => {
    useStore.getState().setStates({ "sensor.a": { state: "on" } });
    expect(useStore.getState().states["sensor.a"].state).toBe("on");

    useStore.getState().updateState("sensor.b", { state: "off" });
    expect(useStore.getState().states["sensor.b"].state).toBe("off");

    useStore.getState().setWsStatus("connected");
    expect(useStore.getState().wsStatus).toBe("connected");
  });

  it("manages alerts and keeps max history", () => {
    for (let i = 0; i < 120; i += 1) {
      useStore.getState().addAlert({ id: i });
    }
    expect(useStore.getState().alerts.length).toBe(100);

    useStore.getState().setAlertsIfEmpty([{ id: "seed" }]);
    expect(useStore.getState().alerts.length).toBe(100);

    useStore.getState().setAlerts([]);
    useStore.getState().setAlertsIfEmpty([{ id: "seed" }]);
    expect(useStore.getState().alerts).toEqual([{ id: "seed" }]);
  });

  it("sets services payload", () => {
    useStore.getState().setServices({ mqtt: "online" });
    expect(useStore.getState().services.mqtt).toBe("online");
  });

  // --- Testes de assets (Issue #337) ---

  it("setAssets replaces the assets array", () => {
    const assets = [{ id: "1", name: "Sensor A", asset_type: "sensor" }];
    useStore.getState().setAssets(assets);
    expect(useStore.getState().assets).toEqual(assets);
  });

  it("addAsset prepends a new asset", () => {
    const existing = { id: "1", name: "Sensor A", asset_type: "sensor" };
    useStore.setState({ assets: [existing] });

    const newAsset = { id: "2", name: "Camera B", asset_type: "camera" };
    useStore.getState().addAsset(newAsset);

    const assets = useStore.getState().assets;
    expect(assets[0]).toEqual(newAsset);
    expect(assets[1]).toEqual(existing);
  });

  it("updateAsset replaces asset with matching id", () => {
    const original = { id: "1", name: "Sensor A", status: "active" };
    useStore.setState({ assets: [original] });

    const updated = { id: "1", name: "Sensor A", status: "inactive" };
    useStore.getState().updateAsset(updated);

    expect(useStore.getState().assets[0].status).toBe("inactive");
  });

  it("updateAsset keeps array untouched when id does not match", () => {
    const original = { id: "1", name: "Sensor A", status: "active" };
    useStore.setState({ assets: [original] });

    useStore.getState().updateAsset({ id: "2", name: "Outro", status: "inactive" });
    expect(useStore.getState().assets).toEqual([original]);
  });

  it("removeAsset removes asset by id", () => {
    const assets = [
      { id: "1", name: "Sensor A" },
      { id: "2", name: "Camera B" },
    ];
    useStore.setState({ assets });
    useStore.getState().removeAsset("1");

    expect(useStore.getState().assets).toHaveLength(1);
    expect(useStore.getState().assets[0].id).toBe("2");
  });

  it("setAssetsLoading and setAssetsError manage loading state", () => {
    useStore.getState().setAssetsLoading(true);
    expect(useStore.getState().assetsLoading).toBe(true);

    useStore.getState().setAssetsError("Network error");
    expect(useStore.getState().assetsError).toBe("Network error");

    useStore.getState().setAssetsLoading(false);
    expect(useStore.getState().assetsLoading).toBe(false);
  });
});
