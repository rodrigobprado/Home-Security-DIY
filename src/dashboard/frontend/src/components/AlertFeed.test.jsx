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
    mockedStore.alerts = [];
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
    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith("/api/alerts?limit=30", { headers: {} }));
    await waitFor(() => expect(setAlertsIfEmpty).toHaveBeenCalledTimes(1));
  });

  it("shows empty state", () => {
    render(<AlertFeed />);
    expect(screen.getByText("Nenhum alerta registrado.")).toBeInTheDocument();
  });

  it("renders alerts list with fallback label/style", () => {
    mockedStore.alerts = [
      {
        id: 99,
        timestamp: "2026-02-24T03:00:00.000Z",
        entity_id: "device.unknown",
        old_state: "off",
        new_state: "on",
        severity: "custom",
      },
    ];

    render(<AlertFeed />);
    expect(screen.getByText("device.unknown")).toBeInTheDocument();
    expect(screen.getByText((text) => text.includes("off") && text.includes("on"))).toBeInTheDocument();
  });

  it("ignores initial payload when API does not return array", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      json: async () => ({ alerts: [] }),
    });

    render(<AlertFeed />);
    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith("/api/alerts?limit=30", { headers: {} }));
    expect(setAlertsIfEmpty).not.toHaveBeenCalled();
  });

  it("uses timestamp as list key when id is missing", () => {
    mockedStore.alerts = [
      {
        timestamp: "2026-02-24T04:00:00.000Z",
        entity_id: "binary_sensor.porta_entrada",
        old_state: "off",
        new_state: "on",
        severity: "critical",
      },
    ];

    render(<AlertFeed />);
    expect(screen.getByText("Porta Entrada")).toBeInTheDocument();
  });
});
