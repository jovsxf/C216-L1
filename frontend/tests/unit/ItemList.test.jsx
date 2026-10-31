import { render, screen } from "@testing-library/react";
import { expect, it } from "vitest";
import { ItemList } from "../../src/components/ItemList";

it("mostra o estado vazio", () => {
  render(<ItemList items={[]} />);
  expect(screen.getByText("Nenhum item cadastrado.")).toBeInTheDocument();
});

it("lista itens e omite a descrição vazia", () => {
  render(
    <ItemList
      items={[
        { id: "1", name: "Caneta", description: "Azul" },
        { id: "2", name: "Régua", description: "" },
      ]}
    />,
  );
  expect(screen.getByText("Caneta")).toBeInTheDocument();
  expect(screen.getByText("Azul")).toBeInTheDocument();
  expect(screen.getByText("Régua")).toBeInTheDocument();
  expect(screen.getAllByRole("listitem")).toHaveLength(2);
});
