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
    global.WebSocket = MockWebSocket;
  });

  it("opens socket and updates ws status", async () => {
    render(<TestComponent />);
    await Promise.resolve();
    expect(MockWebSocket.instances.length).toBe(1);
    expect(setWsStatus).toHaveBeenCalledWith("connecting");
    expect(setWsStatus).toHaveBeenCalledWith("connected");
  });
});
