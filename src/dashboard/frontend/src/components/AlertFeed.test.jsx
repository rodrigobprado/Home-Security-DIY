import { render, screen, waitFor } from "@testing-library/react";
import AlertFeed from "./AlertFeed";

const setAlertsIfEmpty = vi.fn();
const mockedStore = {
  alerts: [],
  setAlertsIfEmpty,
};

vi.mock("../store/useStore", () => ({
  default: () => mockedStore,
}));

describe("AlertFeed", () => {
  beforeEach(() => {
    setAlertsIfEmpty.mockClear();
    global.fetch = vi.fn().mockResolvedValue({
      json: async () => [
        {
          id: 1,
          timestamp: new Date().toISOString(),
          entity_id: "alarm_control_panel.alarmo",
          old_state: "disarmed",
          new_state: "armed_home",
          severity: "warning",
        },
      ],
    });
  });

  it("requests initial alerts from REST API", async () => {
    render(<AlertFeed />);
    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith("/api/alerts?limit=30"));
    await waitFor(() => expect(setAlertsIfEmpty).toHaveBeenCalledTimes(1));
  });

  it("shows empty state", () => {
    render(<AlertFeed />);
    expect(screen.getByText("Nenhum alerta registrado.")).toBeInTheDocument();
  });
});
