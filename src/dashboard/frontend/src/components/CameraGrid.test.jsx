import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import CameraGrid from "./CameraGrid";

// Mock do hook useAssets para isolar o componente
vi.mock("../hooks/useAssets", () => ({
  useAssets: () => ({
    cameraAssets: [],
    sensorAssets: [],
    droneAssets: [],
    assets: [],
    assetsLoading: false,
    assetsError: null,
    refetch: vi.fn(),
  }),
}));

describe("CameraGrid", () => {
  it("renders static fallback cameras when no dynamic assets", () => {
    render(<CameraGrid />);
    // Com cameraAssets vazio, deve usar STATIC_CAMERAS (fallback)
    expect(screen.getByText("Entrada")).toBeInTheDocument();
    expect(screen.getByText("Fundos")).toBeInTheDocument();
    expect(screen.getByText("Garagem")).toBeInTheDocument();
    expect(screen.getByText("Lateral")).toBeInTheDocument();
  });

  it("renders dynamic cameras when assets loaded", () => {
    vi.mocked(require("../hooks/useAssets").useAssets).mockReturnValueOnce({
      cameraAssets: [
        { entity_id: "cam_frente", name: "Frente", asset_type: "camera", is_active: true },
        { entity_id: "cam_quintal", name: "Quintal", asset_type: "camera", is_active: true },
      ],
      sensorAssets: [],
      droneAssets: [],
      assets: [],
      assetsLoading: false,
      assetsError: null,
      refetch: vi.fn(),
    });
    render(<CameraGrid />);
    expect(screen.getByText("Frente")).toBeInTheDocument();
    expect(screen.getByText("Quintal")).toBeInTheDocument();
  });
});
