import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import Header from "./Header";

const mockStore = {
  states: {},
  wsStatus: "connected",
};

vi.mock("../store/useStore", () => ({
  default: () => mockStore,
}));

vi.mock("./QuickActionsMenu", () => ({
  default: () => <div data-testid="quick-actions-stub" />,
}));

describe("Header", () => {
  it("renders triggered alarm and connected websocket label on dashboard route", () => {
    mockStore.states = {
      "alarm_control_panel.alarmo": { state: "triggered" },
    };
    mockStore.wsStatus = "connected";

    render(
      <MemoryRouter initialEntries={["/"]}>
        <Header />
      </MemoryRouter>,
    );

    expect(screen.getByText("🔴 ALARME DISPARADO")).toBeInTheDocument();
    expect(screen.getByText(/ao vivo/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /⊟ Kiosk/i })).toHaveAttribute("href", "/simplified");
    expect(screen.getByTestId("quick-actions-stub")).toBeInTheDocument();
  });

  it("renders fallback alarm label and full-mode link on simplified route", () => {
    mockStore.states = {
      "alarm_control_panel.alarmo": { state: "custom_state" },
    };
    mockStore.wsStatus = "disconnected";

    render(
      <MemoryRouter initialEntries={["/simplified"]}>
        <Header />
      </MemoryRouter>,
    );

    expect(screen.getByText("⚪ custom_state")).toBeInTheDocument();
    expect(screen.getByText(/disconnected/i)).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /⊞ Completo/i })).toHaveAttribute("href", "/");
  });
});
