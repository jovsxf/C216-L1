import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, it, vi } from "vitest";
import { ItemForm } from "../../src/components/ItemForm";

it("mostra erro e não chama onAdd com nome vazio", async () => {
  const user = userEvent.setup();
  const onAdd = vi.fn();
  render(<ItemForm onAdd={onAdd} />);

  await user.click(screen.getByRole("button", { name: "Adicionar" }));

  expect(screen.getByRole("alert")).toHaveTextContent("O nome é obrigatório.");
  expect(onAdd).not.toHaveBeenCalled();
});

it("envia valores normalizados e limpa o formulário", async () => {
  const user = userEvent.setup();
  const onAdd = vi.fn().mockResolvedValue(undefined);
  render(<ItemForm onAdd={onAdd} />);

  await user.type(screen.getByLabelText("Nome"), "  Livro  ");
  await user.type(screen.getByLabelText(/Descrição/), "  Ficção  ");
  await user.click(screen.getByRole("button", { name: "Adicionar" }));

  expect(onAdd).toHaveBeenCalledWith({ name: "Livro", description: "Ficção" });
  expect(screen.getByLabelText("Nome")).toHaveValue("");
  expect(screen.getByLabelText(/Descrição/)).toHaveValue("");
});

it("mostra o erro de onAdd e mantém o que foi digitado", async () => {
  const user = userEvent.setup();
  const onAdd = vi
    .fn()
    .mockRejectedValue(new Error("Já existe um item com esse nome"));
  render(<ItemForm onAdd={onAdd} />);

  await user.type(screen.getByLabelText("Nome"), "Livro");
  await user.click(screen.getByRole("button", { name: "Adicionar" }));

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Já existe um item com esse nome",
  );
  expect(screen.getByLabelText("Nome")).toHaveValue("Livro");
  expect(screen.getByRole("button", { name: "Adicionar" })).toBeEnabled();
});

it("desabilita o botão enquanto salva", async () => {
  const user = userEvent.setup();
  let finishSaving;
  const onAdd = vi.fn(
    () =>
      new Promise((resolve) => {
        finishSaving = resolve;
      }),
  );
  render(<ItemForm onAdd={onAdd} />);

  await user.type(screen.getByLabelText("Nome"), "Livro");
  await user.click(screen.getByRole("button", { name: "Adicionar" }));

  expect(screen.getByRole("button", { name: "Adicionar" })).toBeDisabled();
  finishSaving();
  await vi.waitFor(() =>
    expect(screen.getByRole("button", { name: "Adicionar" })).toBeEnabled(),
  );
});
