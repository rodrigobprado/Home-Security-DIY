import { render, screen } from "@testing-library/react";
import AlarmStatus from "./AlarmStatus";

const mockStore = {
  states: {},
};

vi.mock("../store/useStore", () => ({
  default: () => mockStore,
}));

describe("AlarmStatus", () => {
  it("renders triggered alarm style and label", () => {
    mockStore.states = {
      "alarm_control_panel.alarmo": { state: "triggered" },
    };

    render(<AlarmStatus />);

    expect(screen.getByText("ALARME DISPARADO")).toBeInTheDocument();
  });

  it("renders disarmed label", () => {
    mockStore.states = {
      "alarm_control_panel.alarmo": { state: "disarmed" },
    };

    render(<AlarmStatus />);

    expect(screen.getByText("Desarmado")).toBeInTheDocument();
  });
});
