export function ItemList({ items }) {
  if (items.length === 0) {
    return (
      <p className="rounded-xl border border-dashed border-slate-300 bg-white/70 px-4 py-8 text-center text-slate-600">
        Nenhum item cadastrado.
      </p>
    );
  }

  return (
    <ul className="space-y-3">
      {items.map((item) => (
        <li
          key={item.id}
          className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
        >
          <p className="font-semibold text-slate-900">{item.name}</p>
          {item.description && (
            <p className="mt-1 whitespace-pre-wrap text-sm leading-relaxed text-slate-600">
              {item.description}
            </p>
          )}
        </li>
      ))}
    </ul>
  );
}
