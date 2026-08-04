import Link from "next/link";

type Article = {
  title: string;
  url: string;
  source: string;
  published_at: string;
};

type EventDetail = {
  id: number;
  title: string;
  summary: string;
  latest_development: string | null;
  why_it_matters: string | null;
  what_happens_next: string | null;
  impact_scope: string;
  confidence: string;
  homepage: boolean;
  editorial_priority: string;
  category: string;
  importance_score: number;
  status: string;
  article_count: number;
  source_count: number;
  created_at: string;
  updated_at: string;
  sources: string[];
  articles: Article[];
};

type EventPageProps = {
  params: Promise<{
    eventId: string;
  }>;
};

function parseUtcDate(dateString: string): Date {
  const hasTimezone =
    dateString.endsWith("Z") ||
    /[+-]\d{2}:\d{2}$/.test(dateString);

  return new Date(hasTimezone ? dateString : `${dateString}Z`);
}

function formatDate(dateString: string): string {
  const date = parseUtcDate(dateString);

  return new Intl.DateTimeFormat("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "numeric",
    minute: "2-digit",
    timeZoneName: "short",
  }).format(date);
}

function getPriorityMessage(priority: string): string {
  if (priority === "Critical") {
    return "This event crossed the World Critical threshold and belongs in today’s briefing.";
  }

  if (priority === "Watch") {
    return "We’re monitoring this story because it could become world critical as more facts become available.";
  }

  return "This event is being tracked for background and context.";
}

function getPriorityClass(priority: string): string {
  if (priority === "Critical") {
    return "border-red-200 bg-red-50 text-red-700";
  }

  if (priority === "Watch") {
    return "border-amber-200 bg-amber-50 text-amber-700";
  }

  return "border-slate-200 bg-slate-100 text-slate-600";
}

function getConfidenceClass(confidence: string): string {
  if (confidence === "High") {
    return "bg-emerald-50 text-emerald-700";
  }

  if (confidence === "Medium") {
    return "bg-amber-50 text-amber-700";
  }

  return "bg-slate-100 text-slate-600";
}

function getImpactClass(impactScope: string): string {
  if (impactScope === "Global") {
    return "bg-violet-50 text-violet-700";
  }

  if (impactScope === "National") {
    return "bg-blue-50 text-blue-700";
  }

  if (impactScope === "Regional") {
    return "bg-cyan-50 text-cyan-700";
  }

  if (impactScope === "Industry") {
    return "bg-indigo-50 text-indigo-700";
  }

  return "bg-slate-100 text-slate-600";
}

export default async function EventPage({ params }: EventPageProps) {
  const { eventId } = await params;

  const response = await fetch(
    `http://127.0.0.1:8000/events/${eventId}`,
    {
      cache: "no-store",
    },
  );

  if (!response.ok) {
    throw new Error("Failed to load event");
  }

  const event: EventDetail = await response.json();

  const priorityClass = getPriorityClass(event.editorial_priority);
  const confidenceClass = getConfidenceClass(event.confidence);
  const impactClass = getImpactClass(event.impact_scope);

  return (
    <main className="min-h-screen bg-white">
      <header className="border-b border-slate-800 bg-slate-950 text-white">
        <div className="mx-auto max-w-5xl px-6 py-6">
          <Link href="/" className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-full bg-white text-2xl">
              🌍
            </div>

            <div>
              <p className="text-2xl font-black tracking-tight">
                World Critical
              </p>

              <p className="text-sm text-slate-300">
                The few stories that matter today.
              </p>
            </div>
          </Link>
        </div>
      </header>

      <div className="mx-auto max-w-5xl px-6 py-10">
        <Link
          href="/"
          className="text-sm font-semibold text-slate-600 transition hover:text-slate-950"
        >
          ← Back to briefing
        </Link>

        <article className="mt-8">
          <div className="flex flex-wrap items-center gap-3">
            <span
              className={`rounded-full border px-4 py-1.5 text-sm font-bold uppercase tracking-wide ${priorityClass}`}
            >
              {event.editorial_priority}
            </span>

            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-slate-600">
              {event.category}
            </span>

            <span className="text-xs text-slate-400">
              Updated {formatDate(event.updated_at)}
            </span>
          </div>

          <h1 className="mt-6 max-w-3xl text-4xl font-black leading-tight tracking-tight text-slate-950 sm:text-5xl">
            {event.title}
          </h1>

          <p className="mt-5 max-w-3xl text-base font-medium leading-7 text-slate-500">
            {getPriorityMessage(event.editorial_priority)}
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3 border-y border-slate-200 py-5">
            <a
              href="#original-reporting"
              className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
            >
              {event.article_count} article
              {event.article_count === 1 ? "" : "s"} ↓
            </a>

            <a
              href="#sources"
              className="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:bg-slate-50"
            >
              {event.source_count} source
              {event.source_count === 1 ? "" : "s"} ↓
            </a>

            <span
              className={`rounded-full px-4 py-2 text-sm font-semibold ${impactClass}`}
            >
              {event.impact_scope} impact
            </span>

            <span
              className={`rounded-full px-4 py-2 text-sm font-semibold ${confidenceClass}`}
            >
              {event.confidence} confidence
            </span>
          </div>
        </article>

        <div className="mt-14 max-w-3xl space-y-14">
          <section>
            <p className="text-xs font-bold uppercase tracking-[0.25em] text-slate-500">
              What happened
            </p>

            <p className="mt-4 text-lg leading-8 text-slate-700">
              {event.summary}
            </p>
          </section>

          {event.latest_development && (
            <section>
              <p className="text-xs font-bold uppercase tracking-[0.25em] text-blue-700">
                Latest development
              </p>

              <p className="mt-4 text-lg leading-8 text-slate-700">
                {event.latest_development}
              </p>
            </section>
          )}

          {event.why_it_matters && (
            <section>
              <p className="text-xs font-bold uppercase tracking-[0.25em] text-red-700">
                Why it matters
              </p>

              <p className="mt-4 text-lg leading-8 text-slate-700">
                {event.why_it_matters}
              </p>
            </section>
          )}

          {event.what_happens_next && (
            <section>
              <p className="text-xs font-bold uppercase tracking-[0.25em] text-amber-700">
                What happens next
              </p>

              <p className="mt-4 text-lg leading-8 text-slate-700">
                {event.what_happens_next}
              </p>
            </section>
          )}
        </div>

        <section
          id="sources"
          className="mt-16 scroll-mt-8 border-t border-slate-300 pt-8"
        >
          <p className="text-xs font-bold uppercase tracking-[0.25em] text-slate-500">
            Sources
          </p>

          <div className="mt-5 flex flex-wrap gap-3">
            {event.sources.map((source) => (
              <span
                key={source}
                className="rounded-full bg-slate-100 px-4 py-2 text-sm font-semibold text-slate-700"
              >
                {source}
              </span>
            ))}
          </div>
        </section>

        <section
          id="original-reporting"
          className="mt-12 scroll-mt-8 border-t border-slate-300 pt-8"
        >
          <p className="text-xs font-bold uppercase tracking-[0.25em] text-slate-500">
            Original reporting
          </p>

          <div className="mt-5 divide-y divide-slate-200 border-y border-slate-200">
            {event.articles.map((article) => (
              <a
                key={article.url}
                href={article.url}
                target="_blank"
                rel="noreferrer"
                className="group block py-6 transition hover:bg-slate-50 sm:px-3"
              >
                <p className="text-sm font-bold text-slate-500">
                  {article.source}
                </p>

                <h2 className="mt-2 text-xl font-bold text-slate-950 transition group-hover:text-slate-600">
                  {article.title}
                </h2>

                <p className="mt-2 text-sm text-slate-400">
                  {formatDate(article.published_at)}
                </p>
              </a>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}