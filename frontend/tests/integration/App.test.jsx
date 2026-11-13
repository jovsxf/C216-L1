import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, expect, it, vi } from "vitest";
import App from "../../src/App";
import { API_URL } from "../../src/services/items";
import { jsonResponse } from "../helpers";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("mostra carregando até a API responder", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(jsonResponse([])));
  render(<App />);

  expect(screen.getByText("Carregando itens...")).toBeInTheDocument();
  expect(
    await screen.findByText("Nenhum item cadastrado."),
  ).toBeInTheDocument();
  expect(screen.queryByText("Carregando itens...")).not.toBeInTheDocument();
});

it("lista os itens vindos da API", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      jsonResponse([
        { id: 1, name: "Caneta", description: "Azul" },
        { id: 2, name: "Régua", description: null },
      ]),
    ),
  );
  render(<App />);

  expect(await screen.findByText("Caneta")).toBeInTheDocument();
  expect(screen.getByText("Azul")).toBeInTheDocument();
  expect(screen.getByText("Régua")).toBeInTheDocument();
  expect(screen.getAllByRole("listitem")).toHaveLength(2);
});

it("mostra erro quando não consegue conectar à API", async () => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("fail")));
  render(<App />);

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Não foi possível conectar à API.",
  );
});

it("cadastra um item com POST e o exibe na lista", async () => {
  const user = userEvent.setup();
  const fetchMock = vi
    .fn()
    .mockResolvedValueOnce(jsonResponse([]))
    .mockResolvedValueOnce(
      jsonResponse(
        { id: 7, name: "Notebook", description: "14 polegadas" },
        { status: 201 },
      ),
    );
  vi.stubGlobal("fetch", fetchMock);
  render(<App />);
  await screen.findByText("Nenhum item cadastrado.");

  await user.type(screen.getByLabelText("Nome"), "Notebook");
  await user.type(screen.getByLabelText(/Descrição/), "14 polegadas");
  await user.click(screen.getByRole("button", { name: "Adicionar" }));

  expect(await screen.findByText("Notebook")).toBeInTheDocument();
  expect(screen.getByText("14 polegadas")).toBeInTheDocument();
  expect(screen.queryByText("Nenhum item cadastrado.")).not.toBeInTheDocument();

  const [url, options] = fetchMock.mock.calls[1];
  expect(url).toBe(`${API_URL}/items/`);
  expect(options.method).toBe("POST");
  expect(JSON.parse(options.body)).toEqual({
    name: "Notebook",
    description: "14 polegadas",
  });
});

it("mostra o erro 409 e mantém o nome digitado", async () => {
  const user = userEvent.setup();
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValueOnce(jsonResponse([]))
      .mockResolvedValueOnce(
        jsonResponse(
          { detail: "Já existe um item com esse nome" },
          { status: 409 },
        ),
      ),
  );
  render(<App />);
  await screen.findByText("Nenhum item cadastrado.");

  await user.type(screen.getByLabelText("Nome"), "Notebook");
  await user.click(screen.getByRole("button", { name: "Adicionar" }));

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Já existe um item com esse nome",
  );
  expect(screen.getByLabelText("Nome")).toHaveValue("Notebook");
  expect(screen.getByText("Nenhum item cadastrado.")).toBeInTheDocument();
});

it("não chama a API ao cadastrar item sem nome", async () => {
  const user = userEvent.setup();
  const fetchMock = vi.fn().mockResolvedValue(jsonResponse([]));
  vi.stubGlobal("fetch", fetchMock);
  render(<App />);
  await screen.findByText("Nenhum item cadastrado.");

  await user.click(screen.getByRole("button", { name: "Adicionar" }));

  expect(screen.getByRole("alert")).toHaveTextContent("O nome é obrigatório.");
  expect(fetchMock).toHaveBeenCalledTimes(1);
});
