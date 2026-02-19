import { render, screen } from "@testing-library/react";
import CameraGrid from "./CameraGrid";

describe("CameraGrid", () => {
  it("renders all configured cameras", () => {
    render(<CameraGrid />);
    expect(screen.getByText("Entrada")).toBeInTheDocument();
    expect(screen.getByText("Fundos")).toBeInTheDocument();
    expect(screen.getByText("Garagem")).toBeInTheDocument();
    expect(screen.getByText("Lateral")).toBeInTheDocument();
  });
});
