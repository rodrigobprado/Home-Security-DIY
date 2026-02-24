import { fireEvent, render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import QuickActionsMenu from "./QuickActionsMenu";

function renderMenu() {
  return render(
    <MemoryRouter>
      <QuickActionsMenu />
    </MemoryRouter>,
  );
}

describe("QuickActionsMenu", () => {
  it("opens and closes dropdown with button and Escape", () => {
    renderMenu();
    const button = screen.getByRole("button", { name: /Abrir menu operacional/i });

    fireEvent.click(button);
    expect(screen.getByRole("navigation", { name: /Menu Operacional/i })).toBeInTheDocument();

    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("navigation", { name: /Menu Operacional/i })).not.toBeInTheDocument();
  });

  it("closes dropdown when clicking outside", () => {
    renderMenu();
    fireEvent.click(screen.getByRole("button", { name: /Abrir menu operacional/i }));
    expect(screen.getByRole("navigation", { name: /Menu Operacional/i })).toBeInTheDocument();

    fireEvent.mouseDown(document.body);
    expect(screen.queryByRole("navigation", { name: /Menu Operacional/i })).not.toBeInTheDocument();
  });

  it("closes dropdown when clicking a menu link", () => {
    renderMenu();
    fireEvent.click(screen.getByRole("button", { name: /Abrir menu operacional/i }));
    fireEvent.click(screen.getByRole("link", { name: "Admin de Ativos" }));
    expect(screen.queryByRole("navigation", { name: /Menu Operacional/i })).not.toBeInTheDocument();
  });
});
