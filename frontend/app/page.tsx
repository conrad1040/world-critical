import Link from "next/link";

import { getApiUrl } from "../lib/api";
import { SearchForm } from "./components/search-form";

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

type EventsResponse = {
  critical: Event[];
  watch: Event[];
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

function getRelativeTime(dateString: string): string {
  const updatedTime = new Date(dateString).getTime();

  if (Number.isNaN(updatedTime)) {
    return "Recently updated";
  }

  const seconds = Math.max(
    0,
    Math.floor((Date.now() - updatedTime) / 1000),
  );

  if (seconds < 60) {
    return "Updated just now";
  }

  const minutes = Math.floor(seconds / 60);

  if (minutes < 60) {
    return `Updated ${minutes} minute${minutes === 1 ? "" : "s"} ago`;
  }

  const hours = Math.floor(minutes / 60);

  if (hours < 24) {
    return `Updated ${hours} hour${hours === 1 ? "" : "s"} ago`;
  }

  const days = Math.floor(hours / 24);

  return `Updated ${days} day${days === 1 ? "" : "s"} ago`;
}

function EventRow({
  event,
  priority,
}: {
  event: Event;
  priority: "Critical" | "Watch";
}) {
  const isCritical = priority === "Critical";

  const priorityClass = isCritical
    ? "border-red-200 bg-red-50 text-red-700"
    : "border-amber-200 bg-amber-50 text-amber-700";

  const categoryClass =
    categoryStyles[event.category] ?? categoryStyles.Other;

  return (
    <Link
      href={`/events/${event.id}`}
      className="group block"
    >
      <article className="py-8 transition-colors group-hover:bg-slate-50 sm:px-3">
        <div className="flex flex-wrap items-center gap-3">
          <span
            className={`rounded-full border px-3 py-1 text-xs font-bold uppercase tracking-wide ${priorityClass}`}
          >
            {priority}
          </span>

          <span
            className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-wide ${categoryClass}`}
          >
            {event.category}
          </span>

          <span className="text-xs text-slate-400">
            {getRelativeTime(event.updated_at)}
          </span>
        </div>

        <h3 className="mt-5 max-w-4xl text-3xl font-black leading-tight tracking-tight text-slate-950 transition-colors group-hover:text-slate-700 sm:text-4xl">
          {event.title}
        </h3>

        <p className="mt-4 max-w-3xl text-base leading-8 text-slate-600 sm:text-lg">
          {event.summary}
        </p>

        {event.latest_development && (
          <div className="mt-5 max-w-3xl border-l-2 border-blue-200 pl-4">
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-blue-700">
              Latest development
            </p>

            <p className="mt-2 text-base leading-8 text-slate-700 sm:text-lg">
              {event.latest_development}
            </p>
          </div>
        )}

        <div className="mt-6 flex flex-wrap gap-6 text-sm font-medium text-slate-500">
          <span>
            {event.article_count} article
            {event.article_count === 1 ? "" : "s"}
          </span>

          <span>
            {event.source_count} source
            {event.source_count === 1 ? "" : "s"}
          </span>

          <span className="font-semibold text-slate-700">
            Open briefing →
          </span>
        </div>
      </article>
    </Link>
  );
}

export default async function Home() {
  const response = await fetch(getApiUrl("/events"), {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to load events");
  }

  const data: EventsResponse = await response.json();

  return (
    <main className="min-h-screen bg-white">
      <header className="border-b border-slate-800 bg-slate-950 text-white">
        <div className="mx-auto max-w-5xl px-6 py-8">
          <div className="flex items-center gap-4">
            <div className="flex h-14 w-14 items-center justify-center rounded-full bg-white text-3xl">
              🌍
            </div>

            <div>
              <h1 className="text-4xl font-black tracking-tight sm:text-5xl">
                World Critical
              </h1>

              <p className="mt-2 text-sm leading-6 text-slate-300 sm:text-base">
                The few stories that matter today.
              </p>
            </div>
          </div>

          <div className="mt-6">
            <SearchForm />
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-5xl px-6 py-10">
        <section>
          <div className="mb-2 border-b border-slate-300 pb-3">
            <p className="text-xs font-bold uppercase tracking-[0.25em] text-slate-500">
              Today
            </p>

            <h2 className="mt-2 text-3xl font-black tracking-tight text-slate-950">
              Today&apos;s Briefing
            </h2>
          </div>

          {data.critical.length === 0 ? (
            <div className="border-b border-slate-200 py-8">
              <p className="text-lg font-semibold text-slate-950">
                No world-critical events today.
              </p>

              <p className="mt-2 max-w-3xl leading-7 text-slate-600">
                That&apos;s intentional. World Critical only interrupts you
                when an event clearly deserves your attention.
              </p>

              {data.watch.length > 0 && (
                <p className="mt-2 max-w-3xl leading-7 text-slate-600">
                  Below are the stories we&apos;re actively watching.
                </p>
              )}
            </div>
          ) : (
            <div className="divide-y divide-slate-200">
              {data.critical.map((event) => (
                <EventRow
                  key={event.id}
                  event={event}
                  priority="Critical"
                />
              ))}
            </div>
          )}
        </section>

        <section className="mt-12">
          <div className="mb-2 border-b border-slate-300 pb-3">
            <p className="text-xs font-bold uppercase tracking-[0.25em] text-amber-700">
              Monitoring
            </p>

            <h2 className="mt-2 text-3xl font-black tracking-tight text-slate-950">
              Watching
            </h2>

            <p className="mt-2 max-w-2xl text-slate-600">
              Stories we&apos;re actively monitoring that could become world
              critical.
            </p>
          </div>

          {data.watch.length === 0 ? (
            <div className="py-8">
              <p className="text-slate-600">
                Nothing is currently on the watch list.
              </p>
            </div>
          ) : (
            <div className="divide-y divide-slate-200">
              {data.watch.map((event) => (
                <EventRow
                  key={event.id}
                  event={event}
                  priority="Watch"
                />
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}