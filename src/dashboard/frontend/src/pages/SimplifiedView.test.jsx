import { render, screen } from "@testing-library/react";
import SimplifiedView from "./SimplifiedView";

const mockStore = {
  states: {},
};

vi.mock("../store/useStore", () => ({
  default: () => mockStore,
}));

vi.mock("../components/OperationalMap", () => ({
  default: () => <div>Mapa Mock</div>,
}));

vi.mock("../components/CameraGrid", () => ({
  default: () => <div>CameraGrid Mock</div>,
}));

describe("SimplifiedView", () => {
  it("renders triggered status style and embedded components", () => {
    mockStore.states = {
      "alarm_control_panel.alarmo": { state: "triggered" },
    };

    render(<SimplifiedView />);
    expect(screen.getByText("ALARME DISPARADO")).toBeInTheDocument();
    expect(screen.getByText("Mapa Mock")).toBeInTheDocument();
    expect(screen.getByText("CameraGrid Mock")).toBeInTheDocument();
  });

  it("falls back to disarmed config when alarm state is unknown", () => {
    mockStore.states = {
      "alarm_control_panel.alarmo": { state: "unknown_state" },
    };

    render(<SimplifiedView />);
    expect(screen.getByText("Sistema Desarmado")).toBeInTheDocument();
  });
});
