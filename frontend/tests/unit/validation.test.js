import { describe, expect, it } from "vitest";
import { NAME_MAX_LENGTH, validateItem } from "../../src/validation";

describe("validateItem", () => {
  it("rejeita nome vazio ou só com espaços", () => {
    const { errors } = validateItem({ name: "   ", description: "" });
    expect(errors.name).toBe("O nome é obrigatório.");
  });

  it("rejeita nome acima do limite", () => {
    const { errors } = validateItem({
      name: "a".repeat(NAME_MAX_LENGTH + 1),
      description: "",
    });
    expect(errors.name).toBe(
      `O nome deve ter no máximo ${NAME_MAX_LENGTH} caracteres.`,
    );
  });

  it("normaliza os espaços e aceita descrição vazia", () => {
    expect(
      validateItem({ name: "  Caderno  ", description: "  pauta azul  " }),
    ).toEqual({
      errors: {},
      values: { name: "Caderno", description: "pauta azul" },
    });
    expect(
      validateItem({ name: "Estojo", description: "  " }).values.description,
    ).toBe("");
  });
});
