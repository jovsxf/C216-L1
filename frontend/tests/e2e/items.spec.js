import { expect, test } from "@playwright/test";

function uniqueName(prefix) {
  return `${prefix} ${Date.now()}-${Math.floor(Math.random() * 1000)}`;
}

test("carrega a interface a partir da API", async ({ page }) => {
  await page.goto("/");

  await expect(
    page.getByRole("heading", { name: "Gerenciador de Itens" }),
  ).toBeVisible();
  await expect(page.getByText("Carregando itens...")).toHaveCount(0);
  await expect(page.getByRole("alert")).toHaveCount(0);
});

test("valida nome vazio sem chamar a API", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Adicionar" }).click();

  await expect(page.getByRole("alert")).toHaveText("O nome é obrigatório.");
});

test("cadastra um item e ele persiste após recarregar a página", async ({
  page,
}) => {
  const name = uniqueName("Notebook");
  await page.goto("/");
  await page.getByLabel("Nome").fill(name);
  await page.getByLabel(/Descrição/).fill("14 polegadas");
  await page.getByRole("button", { name: "Adicionar" }).click();

  const item = page.getByRole("listitem").filter({ hasText: name });
  await expect(item).toBeVisible();
  await expect(item).toContainText("14 polegadas");
  await expect(page.getByLabel("Nome")).toHaveValue("");

  await page.reload();
  await expect(item).toBeVisible(); // veio do PostgreSQL
});

test("mostra erro ao cadastrar nome duplicado", async ({ page }) => {
  const name = uniqueName("Mouse");
  const items = page.getByRole("listitem").filter({ hasText: name });
  await page.goto("/");

  await page.getByLabel("Nome").fill(name);
  await page.getByRole("button", { name: "Adicionar" }).click();
  await expect(items).toBeVisible();

  await page.getByLabel("Nome").fill(name);
  await page.getByRole("button", { name: "Adicionar" }).click();

  await expect(page.getByRole("alert")).toHaveText(
    "Já existe um item com esse nome",
  );
  await expect(page.getByLabel("Nome")).toHaveValue(name);
  await expect(items).toHaveCount(1);
});
