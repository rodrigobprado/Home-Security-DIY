import { render, screen, waitFor } from "@testing-library/react";
import ServiceStatus from "./ServiceStatus";

describe("ServiceStatus", () => {
  it("loads service status from API", async () => {
    global.fetch = vi.fn().mockResolvedValue({
      json: async () => ({
        services: {
          home_assistant: "online",
          frigate: "degraded",
        },
      }),
    });

    render(<ServiceStatus />);

    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith("/api/services/status"));
    expect(screen.getByText("Home Assistant")).toBeInTheDocument();
    expect(screen.getByText("Frigate NVR")).toBeInTheDocument();
    expect(screen.getByText("online")).toBeInTheDocument();
    expect(screen.getByText("degraded")).toBeInTheDocument();
  });

  it("falls back to checking state when request fails", async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error("network"));

    render(<ServiceStatus />);

    await waitFor(() => expect(global.fetch).toHaveBeenCalledWith("/api/services/status"));
    expect(screen.getByText("Verificando...")).toBeInTheDocument();
  });
});
