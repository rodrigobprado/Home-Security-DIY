import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import OperationalMap from "./OperationalMap";

const apiFetch = vi.fn();

vi.mock("../store/useStore", () => ({
  default: () => ({
    states: {
      "sensor.ugv_battery": { state: "81" },
      "sensor.uav_battery": { state: "72" },
    },
  }),
}));

vi.mock("../utils/auth", () => ({
  apiFetch: (...args) => apiFetch(...args),
  withAdminHeaders: (headers) => headers,
}));

function setupDefaultApiFetch() {
  apiFetch.mockImplementation(async (url, options = {}) => {
    if (url === "/api/map/devices") {
      return { ok: true, json: async () => [] };
    }
    if (url === "/api/map/config" && !options.method) {
      return {
        ok: true,
        json: async () => ({
          floorplan_image_data_url: null,
          geo_bounds: { min_lat: -23.5515, max_lat: -23.5495, min_lon: -46.6345, max_lon: -46.632 },
        }),
      };
    }
    if (url === "/api/drones/command") {
      return { ok: true, json: async () => ({ status: "ok" }) };
    }
    if (url === "/api/map/config" && options.method === "PUT") {
      return { ok: true, json: async () => ({ status: "ok" }) };
    }
    return { ok: true, json: async () => ({}) };
  });
}

describe("OperationalMap", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    setupDefaultApiFetch();
  });

  it("sends drone command and shows success message", async () => {
    render(<OperationalMap />);
    const startButtons = await screen.findAllByRole("button", { name: "Start Patrol" });
    fireEvent.click(startButtons[0]);

    await waitFor(() =>
      expect(apiFetch).toHaveBeenCalledWith(
        "/api/drones/command",
        expect.objectContaining({ method: "POST" }),
      ),
    );
    expect(screen.getByText(/Comando enviado:/)).toBeInTheDocument();
  });

  it("shows error feedback when drone command fails", async () => {
    apiFetch.mockImplementation(async (url) => {
      if (url === "/api/map/devices" || url === "/api/map/config") {
        return { ok: true, json: async () => ({ floorplan_image_data_url: null, geo_bounds: null }) };
      }
      if (url === "/api/drones/command") {
        return { ok: false, json: async () => ({}) };
      }
      return { ok: true, json: async () => ({}) };
    });

    render(<OperationalMap />);
    const startButtons = await screen.findAllByRole("button", { name: "Start Patrol" });
    fireEvent.click(startButtons[0]);

    await waitFor(() => expect(screen.getByText("Falha ao enviar comando.")).toBeInTheDocument());
  });

  it("shows error feedback when map save fails", async () => {
    class MockFileReader {
      constructor() {
        this.result = "data:image/png;base64,AAA";
      }
      readAsDataURL() {
        queueMicrotask(() => this.onload && this.onload());
      }
    }
    global.FileReader = MockFileReader;

    apiFetch.mockImplementation(async (url, options = {}) => {
      if (url === "/api/map/devices") {
        return { ok: true, json: async () => [] };
      }
      if (url === "/api/map/config" && !options.method) {
        return {
          ok: true,
          json: async () => ({
            floorplan_image_data_url: null,
            geo_bounds: { min_lat: -23.5515, max_lat: -23.5495, min_lon: -46.6345, max_lon: -46.632 },
          }),
        };
      }
      if (url === "/api/map/config" && options.method === "PUT") {
        return { ok: false, json: async () => ({}) };
      }
      return { ok: true, json: async () => ({}) };
    });

    const { container } = render(<OperationalMap />);
    const input = container.querySelector('input[type="file"]');
    fireEvent.change(input, {
      target: { files: [new File(["x"], "floorplan.png", { type: "image/png" })] },
    });

    await waitFor(() => expect(screen.getByText("Falha ao salvar planta.")).toBeInTheDocument());
  });
});
