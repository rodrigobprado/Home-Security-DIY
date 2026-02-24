import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import SensorGrid from "./SensorGrid";

const mockUseAssets = vi.fn();
const mockUseStore = vi.fn();

vi.mock("../hooks/useAssets", () => ({
  useAssets: () => mockUseAssets(),
}));

vi.mock("../store/useStore", () => ({
  default: () => mockUseStore(),
}));

describe("SensorGrid", () => {
  beforeEach(() => {
    mockUseAssets.mockReturnValue({
      sensorAssets: [],
      assetsLoading: false,
    });
    mockUseStore.mockReturnValue({ states: {} });
  });

  it("renders static fallback list when no dynamic assets", () => {
    render(<SensorGrid />);
    expect(screen.getByText("Porta Entrada")).toBeInTheDocument();
    expect(screen.getByText("Porta Fundos")).toBeInTheDocument();
  });

  it("renders dynamic sensors and active state", () => {
    mockUseAssets.mockReturnValueOnce({
      sensorAssets: [
        {
          entity_id: "binary_sensor.porta_frente",
          name: "Porta Frente",
          asset_type: "sensor",
          is_active: true,
        },
      ],
      assetsLoading: false,
    });
    mockUseStore.mockReturnValueOnce({
      states: {
        "binary_sensor.porta_frente": { state: "on" },
      },
    });

    render(<SensorGrid />);
    expect(screen.getByText("Porta Frente")).toBeInTheDocument();
    expect(screen.getByText("aberto / detectado")).toBeInTheDocument();
  });

  it("renders loading state when fetching and no sensors", () => {
    mockUseAssets.mockReturnValueOnce({
      sensorAssets: [],
      assetsLoading: true,
    });
    render(<SensorGrid />);
    expect(screen.getByText("Carregando...")).toBeInTheDocument();
  });

  it("maps icons for different sensor naming patterns", () => {
    mockUseAssets.mockReturnValueOnce({
      sensorAssets: [
        { entity_id: "binary_sensor.janela", name: "Janela", is_active: true },
        { entity_id: "binary_sensor.motion_hall", name: "Motion Hall", is_active: true },
        { entity_id: "binary_sensor.smoke", name: "Smoke", is_active: true },
        { entity_id: "binary_sensor.zigbee_status", name: "Zigbee Status", is_active: true },
        { entity_id: "binary_sensor.generic", name: "Generic", is_active: true },
      ],
      assetsLoading: false,
    });
    render(<SensorGrid />);

    expect(screen.getByText("🪟")).toBeInTheDocument();
    expect(screen.getAllByText("👁").length).toBeGreaterThan(0);
    expect(screen.getByText("🔥")).toBeInTheDocument();
    expect(screen.getByText("📡")).toBeInTheDocument();
    expect(screen.getByText("🔵")).toBeInTheDocument();
  });
});
