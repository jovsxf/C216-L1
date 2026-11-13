import { useEffect, useState } from "react";
import { ItemForm } from "./components/ItemForm";
import { ItemList } from "./components/ItemList";
import { createItem, listItems } from "./services/items";

export default function App() {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");

  useEffect(() => {
    listItems()
      .then(setItems)
      .catch((error) => setLoadError(error.message))
      .finally(() => setLoading(false));
  }, []);

  async function addItem(values) {
    const created = await createItem(values); // lança erro se falhar
    setItems((current) => [...current, created]);
  }

  function renderItems() {
    if (loading) {
      return (
        <p role="status" className="px-4 py-8 text-center text-slate-600">
          Carregando itens...
        </p>
      );
    }
    if (loadError) {
      return (
        <p
          role="alert"
          className="rounded-xl border border-red-200 bg-red-50 px-4 py-4 text-sm text-red-700"
        >
          {loadError}
        </p>
      );
    }
    return <ItemList items={items} />;
  }

  return (
    <main className="mx-auto min-h-screen max-w-2xl px-4 py-10 sm:px-6 sm:py-14">
      <header className="mb-8">
        <p className="mb-2 text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">
          C216 · Prática 7
        </p>
        <h1 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
          Gerenciador de Itens
        </h1>
        <p className="mt-3 max-w-xl leading-relaxed text-slate-600">
          Cadastre e acompanhe seus itens. Os dados são salvos pela API em um
          banco PostgreSQL.
        </p>
      </header>
      <div className="space-y-9">
        <section aria-labelledby="new-item-heading" className="space-y-3">
          <h2
            id="new-item-heading"
            className="text-lg font-semibold text-slate-900"
          >
            Novo item
          </h2>
          <ItemForm onAdd={addItem} />
        </section>
        <section aria-labelledby="items-heading" className="space-y-3">
          <div className="flex items-center justify-between gap-3">
            <h2
              id="items-heading"
              className="text-lg font-semibold text-slate-900"
            >
              Itens cadastrados
            </h2>
            <span className="rounded-full bg-slate-200 px-2.5 py-1 text-xs font-semibold text-slate-700">
              {items.length}
            </span>
          </div>
          {renderItems()}
        </section>
      </div>
      <footer className="mt-12 border-t border-slate-200 pt-4 text-xs text-slate-500">
        Os itens são persistidos via API FastAPI + PostgreSQL.
      </footer>
    </main>
  );
}
