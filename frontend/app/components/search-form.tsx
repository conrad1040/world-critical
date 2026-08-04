type SearchFormProps = {
  defaultQuery?: string;
  variant?: "default" | "header";
};

export function SearchForm({
  defaultQuery = "",
  variant = "default",
}: SearchFormProps) {
  const isHeader = variant === "header";

  return (
    <form
      action="/search"
      method="get"
      className={
        isHeader
          ? "flex w-full gap-2"
          : "flex w-full max-w-xl gap-2"
      }
    >
      <label htmlFor="search-query" className="sr-only">
        Search events
      </label>

      <input
        id="search-query"
        name="q"
        type="search"
        defaultValue={defaultQuery}
        placeholder="Search events..."
        minLength={2}
        className={
          isHeader
            ? "min-w-0 flex-1 rounded-lg border border-slate-600 bg-slate-700 px-3 py-2 text-sm text-white outline-none transition placeholder:text-slate-300 focus:border-slate-400 focus:bg-slate-700"
            : "min-w-0 flex-1 rounded-full border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-slate-500"
        }
      />

      <button
        type="submit"
        className={
          isHeader
            ? "shrink-0 rounded-lg bg-sky-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-sky-400"
            : "rounded-full bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800"
        }
      >
        Search
      </button>
    </form>
  );
}
