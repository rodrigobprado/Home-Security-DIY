import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import App from "./App";
import useStore from "./store/useStore";

class MockWebSocket {
  static instances = [];

  constructor(url) {
    this.url = url;
    this.readyState = 1;
    this.onopen = null;
    this.onmessage = null;
    this.onclose = null;
    this.onerror = null;
    MockWebSocket.instances.push(this);
    queueMicrotask(() => this.onopen && this.onopen());
  }

  close() {
    this.readyState = 3;
    if (this.onclose) this.onclose();
  }
}

function mockFetchForDashboard() {
  global.fetch = vi.fn(async (url, options = {}) => {
    if (url === "/api/alerts?limit=30") {
      return { ok: true, json: async () => [] };
    }
    if (url === "/api/services/status") {
      return {
        ok: true,
        json: async () => ({
          services: { home_assistant: "online", frigate: "online" },
        }),
      };
    }
    if (url === "/api/map/devices") {
      return {
        ok: true,
        json: async () => [
          { entity_id: "binary_sensor.porta_entrada", label: "Porta Entrada", x: 40, y: 20, device_type: "sensor" },
          { entity_id: "camera.cam_entrada", label: "Câmera", x: 20, y: 20, device_type: "camera" },
        ],
      };
    }
    if (url === "/api/map/config") {
      return {
        ok: true,
        json: async () => ({
          floorplan_image_data_url: null,
          geo_bounds: {
            min_lat: -23.5515,
            max_lat: -23.5495,
            min_lon: -46.6345,
            max_lon: -46.632,
          },
        }),
      };
    }
    if (url === "/api/drones/command") {
      return { ok: true, json: async () => ({ status: "ok" }) };
    }
    return { ok: true, json: async () => ({}) };
  });
}

describe("App routing and dashboard", () => {
  beforeEach(() => {
    MockWebSocket.instances = [];
    global.WebSocket = MockWebSocket;
    mockFetchForDashboard();
    useStore.setState({
      wsStatus: "connected",
      alerts: [],
      services: {},
      states: {
        "alarm_control_panel.alarmo": { state: "disarmed" },
        "binary_sensor.porta_entrada": { state: "on" },
        "binary_sensor.ugv_online": { state: "on" },
        "sensor.ugv_battery": { state: "81" },
        "sensor.ugv_status": { state: "patrol" },
        "binary_sensor.uav_armed": { state: "true" },
        "sensor.uav_battery": { state: "72" },
        "sensor.uav_status": { state: "auto" },
        "sensor.uav_latitude": { state: "-23.5500" },
        "sensor.uav_longitude": { state: "-46.6330" },
      },
    });
  });

  it("renders dashboard and sends drone command from operational map", async () => {
    window.history.pushState({}, "", "/");
    render(<App />);

    expect(await screen.findByText(/HOME SECURITY/i)).toBeInTheDocument();
    expect(screen.getByText("Mapa Operacional")).toBeInTheDocument();
    expect(screen.getByText("Drones")).toBeInTheDocument();

    fireEvent.click(screen.getAllByText("Start Patrol")[0]);
    await waitFor(() =>
      expect(global.fetch).toHaveBeenCalledWith(
        "/api/drones/command",
        expect.objectContaining({ method: "POST" }),
      ),
    );
  });

  it("renders simplified route", async () => {
    window.history.pushState({}, "", "/simplified");
    render(<App />);

    expect(await screen.findByText("Sistema Desarmado")).toBeInTheDocument();
    expect(screen.getByText("Mapa Operacional")).toBeInTheDocument();
  });
});
