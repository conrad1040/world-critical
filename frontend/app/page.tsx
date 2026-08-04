import Link from "next/link";

import { getApiUrl } from "../lib/api";
import { SiteHeader } from "./components/site-header";

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
  created_at: string;
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

function parseUtcDate(dateString: string): Date {
  const hasTimezone =
    dateString.endsWith("Z") ||
    /[+-]\d{2}:\d{2}$/.test(dateString);

  return new Date(hasTimezone ? dateString : `${dateString}Z`);
}

function formatBriefingDate(dateString: string): string {
  const date = parseUtcDate(dateString);

  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(date);
}

function EventRow({
  event,
  priority,
  rank,
}: {
  event: Event;
  priority: "Critical" | "Watch";
  rank?: number;
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
      <article className="py-6 transition-colors group-hover:bg-slate-50 sm:px-3">
        <div
          className={
            rank !== undefined
              ? "flex items-start gap-3"
              : undefined
          }
        >
          {rank !== undefined && (
            <span
              className="shrink-0 text-2xl font-black tabular-nums leading-none text-red-300"
              aria-label={`Priority ${rank}`}
            >
              {rank}
            </span>
          )}

          <div className={rank !== undefined ? "min-w-0 flex-1" : undefined}>
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
            </div>

            <p className="mt-3 text-xs text-slate-400">
              First reported {formatBriefingDate(event.created_at)}
              <span className="mx-2 text-slate-300">·</span>
              Updated {formatBriefingDate(event.updated_at)}
            </p>

            <h3 className="mt-4 max-w-4xl text-3xl font-black leading-tight tracking-tight text-slate-950 transition-colors group-hover:text-slate-700 sm:text-4xl">
              {event.title}
            </h3>

            <p className="mt-4 max-w-4xl text-base leading-8 text-slate-600 sm:text-lg">
              {event.summary}
            </p>

            {event.latest_development && (
              <div className="mt-5 max-w-4xl border-l-2 border-blue-200 pl-4">
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
          </div>
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
    <main className="bg-slate-100">
      <SiteHeader />

      <div className="mx-auto max-w-6xl bg-slate-50 px-6 py-8">
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
            <div className="border-b border-slate-200 py-6">
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
              {data.critical.map((event, index) => (
                <EventRow
                  key={event.id}
                  event={event}
                  priority="Critical"
                  rank={index + 1}
                />
              ))}
            </div>
          )}
        </section>

        <section className="mt-8">
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
            <div className="py-6">
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