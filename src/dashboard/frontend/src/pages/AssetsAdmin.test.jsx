import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { vi } from "vitest";
import AssetsAdmin from "./AssetsAdmin";

// Mock do hook useAssets
vi.mock("../hooks/useAssets", () => ({
  useAssets: vi.fn(),
}));

import { useAssets } from "../hooks/useAssets";

const mockRefetch = vi.fn();

function setupMockAssets(overrides = {}) {
  useAssets.mockReturnValue({
    assets: [],
    sensorAssets: [],
    cameraAssets: [],
    droneAssets: [],
    assetsLoading: false,
    assetsError: null,
    refetch: mockRefetch,
    ...overrides,
  });
}

function renderWithRouter(initialEntries = ["/admin/assets"]) {
  return render(
    <MemoryRouter initialEntries={initialEntries}>
      <AssetsAdmin />
    </MemoryRouter>,
  );
}

describe("AssetsAdmin", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    setupMockAssets();
  });

  it("renders the page title and empty state message", () => {
    renderWithRouter();
    expect(screen.getByText("Cadastro de Ativos")).toBeInTheDocument();
    expect(screen.getByText(/Nenhum ativo cadastrado/)).toBeInTheDocument();
  });

  it("shows loading state", () => {
    setupMockAssets({ assetsLoading: true });
    renderWithRouter();
    expect(screen.getByText("Carregando ativos...")).toBeInTheDocument();
  });

  it("shows error state", () => {
    setupMockAssets({ assetsError: "Network error" });
    renderWithRouter();
    expect(screen.getByText(/Erro: Network error/)).toBeInTheDocument();
  });

  it("renders asset rows when assets are loaded", () => {
    setupMockAssets({
      assets: [
        {
          id: "uuid-1",
          name: "Sensor Porta",
          entity_id: "binary_sensor.porta",
          asset_type: "sensor",
          status: "active",
          is_active: true,
          location: "entrada",
        },
        {
          id: "uuid-2",
          name: "Camera Entrada",
          entity_id: "camera.entrada",
          asset_type: "camera",
          status: "active",
          is_active: true,
          location: null,
        },
      ],
    });
    renderWithRouter();
    expect(screen.getByText("Sensor Porta")).toBeInTheDocument();
    expect(screen.getByText("Camera Entrada")).toBeInTheDocument();
    expect(screen.getByText(/binary_sensor.porta/)).toBeInTheDocument();
  });

  it("shows the form when clicking Novo Ativo", () => {
    renderWithRouter();
    const btn = screen.getByText("+ Novo Ativo");
    fireEvent.click(btn);
    expect(screen.getByText("Novo Ativo")).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/ex: Sensor Porta Entrada/)).toBeInTheDocument();
  });

  it("closes the form when clicking Cancelar", () => {
    renderWithRouter();
    fireEvent.click(screen.getByText("+ Novo Ativo"));
    expect(screen.getByPlaceholderText(/ex: Sensor Porta Entrada/)).toBeInTheDocument();
    fireEvent.click(screen.getByText("Cancelar"));
    expect(screen.queryByPlaceholderText(/ex: Sensor Porta Entrada/)).not.toBeInTheDocument();
  });

  it("shows admin key input field", () => {
    renderWithRouter();
    expect(
      screen.getByPlaceholderText(/Necessária para criar, editar ou desativar ativos/),
    ).toBeInTheDocument();
  });

  it("shows filter controls", () => {
    renderWithRouter();
    expect(screen.getByPlaceholderText(/Buscar por nome ou entity_id/)).toBeInTheDocument();
    expect(screen.getByText("Todos os tipos")).toBeInTheDocument();
    expect(screen.getByText("Todos os status")).toBeInTheDocument();
  });

  it("calls refetch when clicking Atualizar", () => {
    renderWithRouter();
    const btn = screen.getByText("↻ Atualizar");
    fireEvent.click(btn);
    expect(mockRefetch).toHaveBeenCalledOnce();
  });

  it("shows inactive asset row with reduced opacity", () => {
    setupMockAssets({
      assets: [
        {
          id: "uuid-1",
          name: "Sensor Inativo",
          entity_id: "binary_sensor.inativo",
          asset_type: "sensor",
          status: "inactive",
          is_active: false,
          location: null,
        },
      ],
    });
    renderWithRouter();
    expect(screen.getByText("Sensor Inativo")).toBeInTheDocument();
    // Ativo inativo deve ter botão Restaurar, não Desativar
    expect(screen.getByText("Restaurar")).toBeInTheDocument();
    expect(screen.queryByText("Desativar")).not.toBeInTheDocument();
  });

  it("shows form validation error for missing admin key", async () => {
    renderWithRouter();
    fireEvent.click(screen.getByText("+ Novo Ativo"));

    const nameInput = screen.getByPlaceholderText(/ex: Sensor Porta Entrada/);
    const entityIdInput = screen.getByPlaceholderText(/ex: binary_sensor.porta_entrada/);

    fireEvent.change(nameInput, { target: { value: "Sensor Teste" } });
    fireEvent.change(entityIdInput, { target: { value: "binary_sensor.teste" } });

    fireEvent.click(screen.getByText("Cadastrar"));

    await waitFor(() => {
      expect(
        screen.getByText(/Informe a chave de administrador/),
      ).toBeInTheDocument();
    });
  });

  it("filters assets by search term", () => {
    setupMockAssets({
      assets: [
        {
          id: "uuid-1",
          name: "Sensor Porta",
          entity_id: "binary_sensor.porta",
          asset_type: "sensor",
          status: "active",
          is_active: true,
          location: null,
        },
        {
          id: "uuid-2",
          name: "Camera Entrada",
          entity_id: "camera.entrada",
          asset_type: "camera",
          status: "active",
          is_active: true,
          location: null,
        },
      ],
    });
    renderWithRouter();

    const searchInput = screen.getByPlaceholderText(/Buscar por nome ou entity_id/);
    fireEvent.change(searchInput, { target: { value: "Camera" } });

    expect(screen.getByText("Camera Entrada")).toBeInTheDocument();
    expect(screen.queryByText("Sensor Porta")).not.toBeInTheDocument();
  });

  it("applies filterType from query param", () => {
    setupMockAssets({
      assets: [
        {
          id: "uuid-1",
          name: "Sensor Porta",
          entity_id: "binary_sensor.porta",
          asset_type: "sensor",
          status: "active",
          is_active: true,
          location: null,
        },
        {
          id: "uuid-2",
          name: "Camera Entrada",
          entity_id: "camera.entrada",
          asset_type: "camera",
          status: "active",
          is_active: true,
          location: null,
        },
      ],
    });

    renderWithRouter(["/admin/assets?type=camera"]);
    expect(screen.getByText("Camera Entrada")).toBeInTheDocument();
    expect(screen.queryByText("Sensor Porta")).not.toBeInTheDocument();
  });
});
