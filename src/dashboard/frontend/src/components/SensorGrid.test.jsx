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
});
