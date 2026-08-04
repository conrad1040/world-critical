type SearchFormProps = {
  defaultQuery?: string;
};

export function SearchForm({ defaultQuery = "" }: SearchFormProps) {
  return (
    <form action="/search" method="get" className="flex w-full max-w-xl gap-2">
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
        className="min-w-0 flex-1 rounded-full border border-slate-300 bg-white px-4 py-2.5 text-sm text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-slate-500"
      />

      <button
        type="submit"
        className="rounded-full bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800"
      >
        Search
      </button>
    </form>
  );
}
