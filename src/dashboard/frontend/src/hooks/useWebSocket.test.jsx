import { render } from "@testing-library/react";
import { useWebSocket } from "./useWebSocket";

const setStates = vi.fn();
const updateState = vi.fn();
const addAlert = vi.fn();
const setWsStatus = vi.fn();

vi.mock("../store/useStore", () => ({
  default: () => ({
    setStates,
    updateState,
    addAlert,
    setWsStatus,
  }),
}));

class MockWebSocket {
  static instances = [];

  constructor(url) {
    this.url = url;
    this.onopen = null;
    this.onmessage = null;
    this.onclose = null;
    this.onerror = null;
    MockWebSocket.instances.push(this);
    queueMicrotask(() => this.onopen && this.onopen());
  }

  close() {
    if (this.onclose) this.onclose();
  }
}

function TestComponent() {
  useWebSocket();
  return null;
}

describe("useWebSocket", () => {
  beforeEach(() => {
    MockWebSocket.instances = [];
    setStates.mockClear();
    updateState.mockClear();
    addAlert.mockClear();
    setWsStatus.mockClear();
    window.sessionStorage.clear();
    window.localStorage.clear();
    global.WebSocket = MockWebSocket;
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("opens socket and updates ws status", async () => {
    window.sessionStorage.setItem("dashboard_api_key", "browser-token");
    render(<TestComponent />);
    await Promise.resolve();
    expect(MockWebSocket.instances.length).toBe(1);
    expect(MockWebSocket.instances[0].url).toContain("/ws?token=browser-token");
    expect(setWsStatus).toHaveBeenCalledWith("connecting");
    expect(setWsStatus).toHaveBeenCalledWith("connected");
  });

  it("handles initial state and state_changed messages", async () => {
    render(<TestComponent />);
    await Promise.resolve();
    const ws = MockWebSocket.instances[0];

    ws.onmessage({
      data: JSON.stringify({
        type: "initial_state",
        states: { "binary_sensor.porta_entrada": { state: "off" } },
      }),
    });
    ws.onmessage({
      data: JSON.stringify({
        type: "state_changed",
        entity_id: "binary_sensor.porta_entrada",
        old_state: "off",
        new_state: "on",
        attributes: { friendly_name: "Porta Entrada" },
        last_changed: "2026-03-02T16:00:00Z",
      }),
    });

    expect(setStates).toHaveBeenCalledWith({
      "binary_sensor.porta_entrada": { state: "off" },
    });
    expect(updateState).toHaveBeenCalledWith(
      "binary_sensor.porta_entrada",
      expect.objectContaining({ state: "on" }),
    );
    expect(addAlert).toHaveBeenCalled();
  });

  it("ignores malformed websocket payloads", async () => {
    render(<TestComponent />);
    await Promise.resolve();
    const ws = MockWebSocket.instances[0];
    ws.onmessage({ data: "{invalid-json" });
    expect(setStates).not.toHaveBeenCalled();
    expect(updateState).not.toHaveBeenCalled();
  });

  it("reconnects after close with backoff", async () => {
    vi.useFakeTimers();
    render(<TestComponent />);
    await Promise.resolve();
    const first = MockWebSocket.instances[0];
    first.onclose();
    vi.advanceTimersByTime(1000);
    expect(MockWebSocket.instances.length).toBe(2);
  });
});
