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

  it("filters assets by status", () => {
    setupMockAssets({
      assets: [
        {
          id: "uuid-1",
          name: "Sensor Ativo",
          entity_id: "binary_sensor.ativo",
          asset_type: "sensor",
          status: "active",
          is_active: true,
          location: null,
        },
        {
          id: "uuid-2",
          name: "Camera Offline",
          entity_id: "camera.offline",
          asset_type: "camera",
          status: "offline",
          is_active: true,
          location: null,
        },
      ],
    });
    renderWithRouter();

    const statusSelect = screen.getByDisplayValue("Todos os status");
    fireEvent.change(statusSelect, { target: { value: "offline" } });

    expect(screen.getByText("Camera Offline")).toBeInTheDocument();
    expect(screen.queryByText("Sensor Ativo")).not.toBeInTheDocument();
  });

  it("shows no-match message when filter eliminates all assets", () => {
    setupMockAssets({
      assets: [
        {
          id: "uuid-1",
          name: "Sensor Ativo",
          entity_id: "binary_sensor.ativo",
          asset_type: "sensor",
          status: "active",
          is_active: true,
          location: null,
        },
      ],
    });
    renderWithRouter();

    const searchInput = screen.getByPlaceholderText(/Buscar por nome ou entity_id/);
    fireEvent.change(searchInput, { target: { value: "xyz-nao-existe" } });

    expect(screen.getByText(/Nenhum ativo encontrado com os filtros aplicados/)).toBeInTheDocument();
  });

  it("creates an asset via API and shows success feedback", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        id: "new-id",
        name: "Sensor Novo",
        asset_type: "sensor",
        entity_id: "binary_sensor.novo",
        status: "active",
        is_active: true,
        location: null,
      }),
    });

    renderWithRouter();

    const adminKeyInput = screen.getByPlaceholderText(/Necessária para criar, editar ou desativar ativos/);
    fireEvent.change(adminKeyInput, { target: { value: "test-admin-key" } });

    fireEvent.click(screen.getByText("+ Novo Ativo"));

    fireEvent.change(screen.getByPlaceholderText(/ex: Sensor Porta Entrada/), {
      target: { value: "Sensor Novo" },
    });
    fireEvent.change(screen.getByPlaceholderText(/ex: binary_sensor.porta_entrada/), {
      target: { value: "binary_sensor.novo" },
    });

    fireEvent.click(screen.getByText("Cadastrar"));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        "/api/assets",
        expect.objectContaining({ method: "POST" }),
      );
    });

    await waitFor(() => {
      expect(screen.getByText(/Ativo "Sensor Novo" cadastrado/)).toBeInTheDocument();
    });
  });

  it("shows API error in form when create fails", async () => {
    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({ detail: "entity_id already exists" }),
    });

    renderWithRouter();

    const adminKeyInput = screen.getByPlaceholderText(/Necessária para criar, editar ou desativar ativos/);
    fireEvent.change(adminKeyInput, { target: { value: "test-admin-key" } });

    fireEvent.click(screen.getByText("+ Novo Ativo"));

    fireEvent.change(screen.getByPlaceholderText(/ex: Sensor Porta Entrada/), {
      target: { value: "Sensor Duplicado" },
    });
    fireEvent.change(screen.getByPlaceholderText(/ex: binary_sensor.porta_entrada/), {
      target: { value: "binary_sensor.duplicado" },
    });

    fireEvent.click(screen.getByText("Cadastrar"));

    await waitFor(() => {
      expect(screen.getByText("entity_id already exists")).toBeInTheDocument();
    });
  });

  it("opens edit form with asset data pre-filled", () => {
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
      ],
    });

    renderWithRouter();

    const adminKeyInput = screen.getByPlaceholderText(/Necessária para criar, editar ou desativar ativos/);
    fireEvent.change(adminKeyInput, { target: { value: "admin-key" } });
    fireEvent.click(screen.getByText("Editar"));

    expect(screen.getByText(/Editar: Sensor Porta/)).toBeInTheDocument();
    expect(screen.getByDisplayValue("binary_sensor.porta")).toBeInTheDocument();
  });

  it("shows error feedback when admin key is missing for deactivation", async () => {
    setupMockAssets({
      assets: [
        {
          id: "uuid-1",
          name: "Sensor Ativo",
          entity_id: "binary_sensor.ativo",
          asset_type: "sensor",
          status: "active",
          is_active: true,
          location: null,
        },
      ],
    });

    renderWithRouter();

    fireEvent.click(screen.getByText("Desativar"));

    await waitFor(() => {
      expect(screen.getByText(/Informe a chave de administrador/)).toBeInTheDocument();
    });
  });

  it("deactivates an asset via API and shows success feedback", async () => {
    setupMockAssets({
      assets: [
        {
          id: "uuid-1",
          name: "Sensor Ativo",
          entity_id: "binary_sensor.ativo",
          asset_type: "sensor",
          status: "active",
          is_active: true,
          location: null,
        },
      ],
    });

    global.fetch = vi.fn().mockResolvedValueOnce({ ok: true });
    vi.spyOn(window, "confirm").mockReturnValueOnce(true);

    renderWithRouter();

    const adminKeyInput = screen.getByPlaceholderText(/Necessária para criar, editar ou desativar ativos/);
    fireEvent.change(adminKeyInput, { target: { value: "test-admin-key" } });

    fireEvent.click(screen.getByText("Desativar"));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        "/api/assets/uuid-1",
        expect.objectContaining({ method: "DELETE" }),
      );
    });

    await waitFor(() => {
      expect(screen.getByText(/Ativo "Sensor Ativo" desativado/)).toBeInTheDocument();
    });
  });

  it("shows error feedback when admin key is missing for restore", async () => {
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

    fireEvent.click(screen.getByText("Restaurar"));

    await waitFor(() => {
      expect(screen.getByText(/Informe a chave de administrador/)).toBeInTheDocument();
    });
  });

  it("restores an asset via API and shows success feedback", async () => {
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

    global.fetch = vi.fn().mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        id: "uuid-1",
        name: "Sensor Inativo",
        asset_type: "sensor",
        entity_id: "binary_sensor.inativo",
        status: "active",
        is_active: true,
        location: null,
      }),
    });

    renderWithRouter();

    const adminKeyInput = screen.getByPlaceholderText(/Necessária para criar, editar ou desativar ativos/);
    fireEvent.change(adminKeyInput, { target: { value: "test-admin-key" } });

    fireEvent.click(screen.getByText("Restaurar"));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        "/api/assets/uuid-1/restore",
        expect.objectContaining({ method: "POST" }),
      );
    });

    await waitFor(() => {
      expect(screen.getByText(/Ativo "Sensor Inativo" restaurado/)).toBeInTheDocument();
    });
  });
});
