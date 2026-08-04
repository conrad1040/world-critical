import Link from "next/link";

import { getApiUrl } from "../../lib/api";
import { SiteHeader } from "../components/site-header";

type Event = {
  id: number;
  title: string;
  summary: string;
  latest_development: string | null;
  category: string;
  importance_score: number;
  article_count: number;
  source_count: number;
  editorial_priority: string;
  updated_at: string;
};

type SearchResponse = {
  query: string;
  results: Event[];
};

type SearchPageProps = {
  searchParams: Promise<{
    q?: string;
  }>;
};

const categoryStyles: Record<string, string> = {
  Conflict: "bg-red-100 text-red-700",
  Politics: "bg-blue-100 text-blue-700",
  Economy: "bg-amber-100 text-amber-800",
  Technology: "bg-emerald-100 text-emerald-700",
  Sports: "bg-violet-100 text-violet-700",
  Entertainment: "bg-pink-100 text-pink-700",
  Crime: "bg-slate-200 text-slate-800",
  Health: "bg-cyan-100 text-cyan-700",
  "Natural Disaster": "bg-orange-100 text-orange-700",
  Other: "bg-slate-100 text-slate-600",
};

function getPriorityClass(priority: string): string {
  if (priority === "Critical") {
    return "border-red-200 bg-red-50 text-red-700";
  }

  if (priority === "Watch") {
    return "border-amber-200 bg-amber-50 text-amber-700";
  }

  return "border-slate-200 bg-slate-100 text-slate-600";
}

function SearchResultRow({ event }: { event: Event }) {
  const priorityClass = getPriorityClass(event.editorial_priority);
  const categoryClass =
    categoryStyles[event.category] ?? categoryStyles.Other;

  return (
    <Link href={`/events/${event.id}`} className="group block">
      <article className="py-8 transition-colors group-hover:bg-slate-50 sm:px-3">
        <div className="flex flex-wrap items-center gap-3">
          <span
            className={`rounded-full border px-3 py-1 text-xs font-bold uppercase tracking-wide ${priorityClass}`}
          >
            {event.editorial_priority}
          </span>

          <span
            className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide ${categoryClass}`}
          >
            {event.category}
          </span>
        </div>

        <h3 className="mt-5 max-w-4xl text-2xl font-black leading-tight tracking-tight text-slate-950 transition-colors group-hover:text-slate-700 sm:text-3xl">
          {event.title}
        </h3>

        <p className="mt-4 max-w-3xl text-base leading-8 text-slate-600">
          {event.summary}
        </p>

        <p className="mt-6 text-sm font-semibold text-slate-700">
          Open briefing →
        </p>
      </article>
    </Link>
  );
}

export default async function SearchPage({ searchParams }: SearchPageProps) {
  const { q = "" } = await searchParams;
  const query = q.trim();

  let data: SearchResponse | null = null;

  if (query.length >= 2) {
    const response = await fetch(
      getApiUrl(`/events/search?q=${encodeURIComponent(query)}`),
      {
        cache: "no-store",
      },
    );

    if (!response.ok) {
      throw new Error("Failed to search events");
    }

    data = await response.json();
  }

  return (
    <main className="bg-slate-100">
      <SiteHeader defaultSearchQuery={query} />

      <div className="mx-auto max-w-6xl bg-slate-50 px-6 py-8">
        <Link
          href="/"
          className="text-sm font-semibold text-slate-600 transition hover:text-slate-950"
        >
          ← Back to briefing
        </Link>

        <div className="mt-8 border-b border-slate-300 pb-3">
          <p className="text-xs font-bold uppercase tracking-[0.25em] text-slate-500">
            Search
          </p>

          <h1 className="mt-2 text-3xl font-black tracking-tight text-slate-950">
            {query ? `Results for “${query}”` : "Search events"}
          </h1>
        </div>

        {query.length === 0 && (
          <p className="mt-6 max-w-2xl leading-7 text-slate-600">
            Search Critical and Watch events by keyword in titles and
            briefings.
          </p>
        )}

        {query.length === 1 && (
          <p className="mt-8 text-slate-600">
            Search terms must be at least 2 characters.
          </p>
        )}

        {data && data.results.length === 0 && (
          <p className="mt-8 text-slate-600">
            No Critical or Watch events matched your search.
          </p>
        )}

        {data && data.results.length > 0 && (
          <div className="mt-4 divide-y divide-slate-200">
            <p className="py-4 text-sm text-slate-500">
              {data.results.length} event
              {data.results.length === 1 ? "" : "s"} found
            </p>

            {data.results.map((event) => (
              <SearchResultRow key={event.id} event={event} />
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
