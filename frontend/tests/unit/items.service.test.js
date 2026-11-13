import { afterEach, expect, it, vi } from "vitest";
import { API_URL, createItem, listItems } from "../../src/services/items";
import { jsonResponse } from "../helpers";

afterEach(() => {
  vi.unstubAllGlobals();
});

it("lista itens com GET /items/", async () => {
  const items = [{ id: 1, name: "Caneta", description: null }];
  const fetchMock = vi.fn().mockResolvedValue(jsonResponse(items));
  vi.stubGlobal("fetch", fetchMock);

  await expect(listItems()).resolves.toEqual(items);
  expect(fetchMock).toHaveBeenCalledWith(`${API_URL}/items/`, undefined);
});

it("cria item com POST e envia descrição vazia como null", async () => {
  const created = { id: 1, name: "Livro", description: null };
  const fetchMock = vi
    .fn()
    .mockResolvedValue(jsonResponse(created, { status: 201 }));
  vi.stubGlobal("fetch", fetchMock);

  await expect(createItem({ name: "Livro", description: "" })).resolves.toEqual(
    created,
  );

  const [url, options] = fetchMock.mock.calls[0];
  expect(url).toBe(`${API_URL}/items/`);
  expect(options.method).toBe("POST");
  expect(options.headers).toEqual({ "Content-Type": "application/json" });
  expect(JSON.parse(options.body)).toEqual({
    name: "Livro",
    description: null,
  });
});

it("usa o detail da API quando a resposta não é ok", async () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValue(
        jsonResponse(
          { detail: "Já existe um item com esse nome" },
          { status: 409 },
        ),
      ),
  );

  await expect(createItem({ name: "Livro", description: "" })).rejects.toThrow(
    "Já existe um item com esse nome",
  );
});

it("usa a mensagem padrão quando detail não é texto", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(jsonResponse({ detail: [{}] }, { status: 422 })),
  );

  await expect(createItem({ name: "x", description: "" })).rejects.toThrow(
    "Erro ao cadastrar o item.",
  );
});

it("informa quando a API está inacessível", async () => {
  vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new TypeError("fail")));

  await expect(listItems()).rejects.toThrow("Não foi possível conectar à API.");
});
