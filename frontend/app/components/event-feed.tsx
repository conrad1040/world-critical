"use client";

import Link from "next/link";
import { useMemo, useState } from "react";

type Event = {
  id: number;
  title: string;
  summary: string;
  category: string;
  importance_score: number;
  article_count: number;
  source_count: number;
  updated_at: string;
};

type EventFeedProps = {
  events: Event[];
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

function getImportanceStyle(score: number) {
  if (score >= 90) {
    return {
      label: "Breaking",
      accent: "bg-red-600",
      text: "text-red-700",
    };
  }

  if (score >= 75) {
    return {
      label: "Major",
      accent: "bg-orange-500",
      text: "text-orange-700",
    };
  }

  if (score >= 60) {
    return {
      label: "Important",
      accent: "bg-yellow-400",
      text: "text-yellow-700",
    };
  }

  return {
    label: "Developing",
    accent: "bg-slate-400",
    text: "text-slate-600",
  };
}

function getRelativeTime(dateString: string): string {
  const updatedTime = new Date(dateString).getTime();
  const differenceInSeconds = Math.max(
    0,
    Math.floor((Date.now() - updatedTime) / 1000),
  );

  if (differenceInSeconds < 60) {
    return "Updated just now";
  }

  const minutes = Math.floor(differenceInSeconds / 60);

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

export default function EventFeed({ events }: EventFeedProps) {
  const [selectedCategory, setSelectedCategory] = useState("All");

  const categories = useMemo(
    () => ["All", ...Array.from(new Set(events.map((event) => event.category)))],
    [events],
  );

  const filteredEvents = useMemo(() => {
    if (selectedCategory === "All") {
      return events;
    }

    return events.filter((event) => event.category === selectedCategory);
  }, [events, selectedCategory]);

  return (
    <>
      <div className="mb-4 flex flex-wrap gap-2">
        {categories.map((category) => {
          const isActive = selectedCategory === category;

          return (
            <button
              key={category}
              type="button"
              onClick={() => setSelectedCategory(category)}
              className={`rounded-full px-4 py-2 text-sm font-semibold transition ${
                isActive
                  ? "bg-slate-950 text-white"
                  : "bg-slate-100 text-slate-600 hover:bg-slate-200"
              }`}
            >
              {category}
            </button>
          );
        })}
      </div>

      {filteredEvents.length === 0 ? (
        <section className="py-12">
          <h3 className="text-xl font-bold text-slate-900">
            No events in this category
          </h3>
        </section>
      ) : (
        <div className="divide-y divide-slate-200">
          {filteredEvents.map((event, index) => {
            const importance = getImportanceStyle(event.importance_score);
            const categoryClass =
              categoryStyles[event.category] ?? categoryStyles.Other;

            return (
              <Link
                key={event.id}
                href={`/events/${event.id}`}
                className="group block"
              >
                <article className="grid gap-6 py-7 transition-colors group-hover:bg-slate-50 sm:grid-cols-[72px_1fr] sm:px-4">                  <div className="flex items-start gap-3 sm:block">
                    <div
                      className={`h-3 w-3 rounded-full ${importance.accent} sm:mt-2`}
                    />

                    <p className="text-xs font-bold uppercase tracking-[0.18em] text-slate-400 sm:mt-4">
                      #{index + 1}
                    </p>
                  </div>

                  <div>
                    <div className="flex flex-wrap items-center gap-3">
                      <span
                        className={`rounded-full px-3 py-1 text-xs font-bold uppercase tracking-wide ${categoryClass}`}
                      >
                        {event.category}
                      </span>

                      <span
                        className={`text-xs font-bold uppercase tracking-wide ${importance.text}`}
                      >
                        {importance.label}
                      </span>

                      <span className="text-xs text-slate-400">
                        {getRelativeTime(event.updated_at)}
                      </span>
                    </div>

                    <h3 className="mt-4 max-w-4xl text-3xl font-black leading-tight tracking-tight text-slate-950 transition-colors group-hover:text-slate-700 sm:text-4xl">
                      {event.title}
                    </h3>

                    <p className="mt-4 max-w-3xl text-base leading-8 text-slate-600 sm:text-lg">
                      {event.summary}
                    </p>

                    <div className="mt-6 flex flex-wrap gap-6 text-sm font-medium text-slate-500">
                      <span>{event.article_count} articles</span>
                      <span>{event.source_count} sources</span>
                      <span className="font-semibold text-slate-700">
                        Open event →
                      </span>
                    </div>
                  </div>
                </article>
              </Link>
            );
          })}
        </div>
      )}
    </>
  );
}