import { act, fireEvent, render, screen } from "@testing-library/react";
import { vi } from "vitest";
import CameraGrid from "./CameraGrid";
import { useAssets } from "../hooks/useAssets";

// Mock do hook useAssets para isolar o componente
vi.mock("../hooks/useAssets", () => ({
  useAssets: vi.fn(() => ({
    cameraAssets: [],
    sensorAssets: [],
    droneAssets: [],
    assets: [],
    assetsLoading: false,
    assetsError: null,
    refetch: vi.fn(),
  })),
}));

describe("CameraGrid", () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it("renders static fallback cameras when no dynamic assets", () => {
    render(<CameraGrid />);
    // Com cameraAssets vazio, deve usar STATIC_CAMERAS (fallback)
    expect(screen.getByText("Entrada")).toBeInTheDocument();
    expect(screen.getByText("Fundos")).toBeInTheDocument();
    expect(screen.getByText("Garagem")).toBeInTheDocument();
    expect(screen.getByText("Lateral")).toBeInTheDocument();
  });

  it("renders dynamic cameras when assets loaded", () => {
    vi.mocked(useAssets).mockReturnValueOnce({
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

  it("shows offline fallback when snapshot fails and recovers on load", () => {
    render(<CameraGrid />);
    const firstImage = screen.getAllByRole("img")[0];

    fireEvent.error(firstImage);
    expect(screen.getByText("offline")).toBeInTheDocument();

    fireEvent.load(firstImage);
    expect(screen.queryByText("offline")).not.toBeInTheDocument();
  });

  it("refreshes snapshot URL on interval tick", () => {
    vi.useFakeTimers();
    render(<CameraGrid />);
    const firstImage = screen.getAllByRole("img")[0];
    const initialSrc = firstImage.getAttribute("src");

    act(() => {
      vi.advanceTimersByTime(2100);
    });
    const updatedSrc = screen.getAllByRole("img")[0].getAttribute("src");

    expect(updatedSrc).not.toEqual(initialSrc);
    expect(updatedSrc).toContain("/api/cameras/");
  });
});
