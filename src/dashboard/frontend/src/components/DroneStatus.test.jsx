import { render, screen } from "@testing-library/react";
import DroneStatus from "./DroneStatus";

const mockStore = { states: {} };

vi.mock("../store/useStore", () => ({
  default: () => mockStore,
}));

describe("DroneStatus", () => {
  it("renders online/offline cards and battery levels", () => {
    mockStore.states = {
      "binary_sensor.ugv_online": { state: "off" },
      "sensor.ugv_battery": { state: "10" },
      "sensor.ugv_status": { state: "idle" },
      "binary_sensor.uav_armed": { state: "true" },
      "sensor.uav_battery": { state: "30" },
      "sensor.uav_status": { state: "patrol" },
    };

    render(<DroneStatus />);
    expect(screen.getByText("🤖 UGV")).toBeInTheDocument();
    expect(screen.getByText("🚁 UAV")).toBeInTheDocument();
    expect(screen.getByText("offline")).toBeInTheDocument();
    expect(screen.getByText("online")).toBeInTheDocument();
    expect(screen.getByText("10%")).toBeInTheDocument();
    expect(screen.getByText("30%")).toBeInTheDocument();
  });

  it("handles non-numeric battery value as 0", () => {
    mockStore.states = {
      "binary_sensor.ugv_online": { state: "on" },
      "sensor.ugv_battery": { state: "--" },
      "sensor.ugv_status": { state: "idle" },
      "binary_sensor.uav_armed": { state: "on" },
      "sensor.uav_battery": { state: "80" },
      "sensor.uav_status": { state: "ok" },
    };

    render(<DroneStatus />);
    expect(screen.getByText("0%")).toBeInTheDocument();
    expect(screen.getByText("80%")).toBeInTheDocument();
  });

  it("shows default placeholders when state entities are missing", () => {
    mockStore.states = {};
    render(<DroneStatus />);

    expect(screen.getAllByText("desconhecido").length).toBeGreaterThan(0);
    expect(screen.getAllByText("--").length).toBeGreaterThan(0);
  });
});
