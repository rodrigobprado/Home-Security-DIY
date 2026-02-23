import useStore from "./useStore";

describe("useStore actions", () => {
  beforeEach(() => {
    useStore.setState({
      states: {},
      alerts: [],
      services: {},
      wsStatus: "connecting",
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
});
