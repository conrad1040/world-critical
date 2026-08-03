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

  return (
    <main className="min-h-screen bg-gray-100 px-6 py-10">
      <div className="mx-auto max-w-4xl">
        <Link
          href="/"
          className="text-sm font-semibold text-gray-600 hover:text-black"
        >
          ← Back to events
        </Link>

        <article className="mt-6 rounded-xl bg-white p-8 shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-wide text-red-600">
            {event.category}
          </p>

          <h1 className="mt-2 text-4xl font-bold leading-tight">
            {event.title}
          </h1>

          <p className="mt-5 text-lg leading-8 text-gray-700">
            {event.summary}
          </p>

          <div className="mt-6 flex flex-wrap gap-5 border-t border-gray-200 pt-5 text-sm text-gray-500">
            <span>Importance: {event.importance_score}</span>
            <span>{event.article_count} articles</span>
            <span>{event.source_count} sources</span>
          </div>
        </article>

        <section className="mt-8">
          <h2 className="text-2xl font-bold">Sources</h2>

          <div className="mt-3 flex flex-wrap gap-2">
            {event.sources.map((source) => (
              <span
                key={source}
                className="rounded-full bg-white px-4 py-2 text-sm shadow-sm"
              >
                {source}
              </span>
            ))}
          </div>
        </section>

        <section className="mt-8">
          <h2 className="text-2xl font-bold">Related coverage</h2>

          <div className="mt-4 space-y-4">
            {event.articles.map((article) => (
              <a
                key={article.url}
                href={article.url}
                target="_blank"
                rel="noreferrer"
                className="block rounded-xl bg-white p-5 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
              >
                <p className="text-sm font-semibold text-red-600">
                  {article.source}
                </p>

                <h3 className="mt-1 text-lg font-bold">
                  {article.title}
                </h3>

                <p className="mt-2 text-sm text-gray-500">
                  {new Date(article.published_at).toLocaleString()}
                </p>
              </a>
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}